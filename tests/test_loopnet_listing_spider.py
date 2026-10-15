import json
import unittest

from scrapy.http import HtmlResponse, Request

from common.spiders.loopnet_listing_spider import LoopnetListingSpider

GSTATE = json.dumps({
    "as": {
        "sc": {"pagingCriteria": {"page": 1, "pageSize": 40}},
        "sp": "42148644||33.065662|-96.838581|1|1|0|~37936068||38.354241|-122.524183|1|1|0|",
        "mrc": 750,
        "count": 750,
    }
})


def _obfuscate(value: str) -> str:
    out = []
    for char in value:
        code = ord(char)
        if 32 <= code <= 126:
            shifted = code + 3
            out.append(chr(shifted if shifted <= 126 else shifted - 95))
        else:
            out.append(char)
    return "".join(out)


def _page(html: str, gstate: str = GSTATE) -> str:
    blob = _obfuscate(gstate).replace("\\", "\\\\").replace('"', '\\"')
    return f"<html><script>window.gState = \"{blob}\";</script>{html}</html>"


class LoopnetListingSpiderTests(unittest.TestCase):
    def response(self, body, url="https://www.loopnet.com/search/commercial-real-estate/usa/for-sale/", page=1):
        request = Request(url, meta={"page": page, "proxy": None})
        return HtmlResponse(url, request=request, body=body.encode(), encoding="utf-8")

    def test_search_state_decodes_obfuscated_gstate(self):
        state = LoopnetListingSpider._search_state(_page(""))
        self.assertEqual(state["as"]["sc"]["pagingCriteria"]["pageSize"], 40)
        self.assertEqual(LoopnetListingSpider._total_results(state), 750)

    def test_coordinates_join_from_map_pin_string(self):
        state = LoopnetListingSpider._search_state(_page(""))
        coords = LoopnetListingSpider._coordinates(state)
        self.assertEqual(coords["42148644"], (33.065662, -96.838581))

    def test_challenge_fails_loudly(self):
        with self.assertRaisesRegex(RuntimeError, "challenge"):
            LoopnetListingSpider._search_state(
                "<html>Access Denied</html>",
            )

    def test_missing_gstate_fails_loudly(self):
        with self.assertRaisesRegex(RuntimeError, "gState"):
            LoopnetListingSpider._search_state("<html><body>nothing</body></html>")

    def test_parses_placard_cards(self):
        card = """
        <article class="placard-card" data-lk="42148644"
          data-gtm-listing_id="777" data-gtm-listing_position="1"
          data-automation-city="Plano" data-automation-state="TX"
          data-automation-postal-code="75024" data-automation-country="US"
          data-automation-property-type="Flex"
          data-automation-transaction-type="ForSale">
          <a class="placard-link" href="https://www.loopnet.com/Listing/x/42148644/"
             title="More details"></a>
          <div class="placard-image"><img class="embla__slide__img" src="https://img/1.png"/></div>
          <div class="placard-title"><span class="building-name">THE GARAGE Luxury Condos</span></div>
          <p class="placard-address">W Spring Creek Pkwy, Plano, TX 75024</p>
          <p class="data-row"><span>Flex Condos</span><span class="data-sep">·</span><span>$765,050 - $2,069,200</span></p>
          <p class="data-row"><span>1,177 - 2,956 SF</span><span class="data-sep">·</span><span>16 Units</span></p>
        </article>"""
        records = LoopnetListingSpider._placard_records(card)
        self.assertEqual(len(records), 1)
        row = records[0]
        self.assertEqual(row["ListingId"], "42148644")
        self.assertEqual(row["Title"], "THE GARAGE Luxury Condos")
        self.assertEqual(row["City"], "Plano")
        self.assertEqual(row["Price"], 765050.0)
        self.assertEqual(row["Size"], 1177.0)
        self.assertEqual(row["ImageUrl"], "https://img/1.png")

    def test_parse_page_yields_items_with_coordinates(self):
        card = """
        <article class="placard-card" data-lk="42148644"
          data-gtm-listing_position="1" data-automation-city="Plano"
          data-automation-state="TX" data-automation-transaction-type="ForSale">
          <a class="placard-link" href="https://www.loopnet.com/Listing/x/42148644/"></a>
          <span class="building-name">THE GARAGE</span>
          <p class="data-row"><span>$765,050</span></p>
        </article>"""
        spider = LoopnetListingSpider(category="commercial-real-estate-for-sale", max_pages=1)
        items = list(spider.parse_page(self.response(_page(card))))
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item["item_id"], "42148644")
        self.assertEqual(item["latitude"], 33.065662)
        self.assertEqual(item["longitude"], -96.838581)
        self.assertEqual(item["total_count"], 750)
        self.assertEqual(item["source"], "loopnet_placard_html")

    def test_parse_page_paginates(self):
        card = """
        <article class="placard-card" data-lk="42148644" data-gtm-listing_position="1">
          <span class="building-name">A</span><p class="data-row"><span>$1</span></p>
        </article>"""
        spider = LoopnetListingSpider(category="commercial-real-estate-for-sale", max_pages=2)
        out = list(spider.parse_page(self.response(_page(card), page=1)))
        item = out[0]
        requests = [o for o in out if isinstance(o, Request)]
        self.assertEqual(item["page"], 1)
        self.assertEqual(len(requests), 1)
        self.assertTrue(requests[0].url.endswith("/2/"))


if __name__ == "__main__":
    unittest.main()
