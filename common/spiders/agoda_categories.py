"""Agoda destination-city inventory captured from the live homepage.

Source: https://www.agoda.com (fetched 2026-10-19, en-us).
The homepage ``footerSeoLinksGroups`` payload carries a ``Destination Cities``
group whose ``Asia`` / ``Europe`` / ``Middle East`` sections link 50
``/city/<slug>-<country>.html`` pages. Six more destination pages that the
homepage only surfaces through its Agoda Homes sections (Koh Kood, Koh Lanta,
Koh Phangan, Koh Samet, Phu Quoc Island, Port Dickson) are kept because they
still serve a full ``geoPageParams`` destination page, giving **56 destinations
across 15 countries**.

Every URL was verified live on 2026-10-19: HTTP 200 with a decodable
``geoPageParams = JSON.parse(...)`` hydration, which the spider needs to
discover the destination's ``pageTypeId`` / ``objectId``.
``jeju-island`` / ``koh-phangan`` / ``koh-samet`` were repointed at the slugs
Agoda now redirects to (``jeju-kr`` / ``ko-pha-ngan-th`` / ``ko-samet-th``).

``AGODA_CATEGORIES`` exposes the inventory in the grouped mapping contract
consumed by ``BaseListingSpider``: ``{country: {leaf: {url, city, country,
region}}}``. Leaf keys stay the bare city slug, so the documented
``-a category=bali`` command is unchanged; the DAG groups the tasks by
``country``.
"""

from __future__ import annotations

# (leaf, city, country, region, agoda url slug)
_AGODA_DESTINATIONS = (
    ("shanghai", "Shanghai", "China", "Asia", "shanghai-cn"),
    ("hong-kong", "Hong Kong", "Hong Kong", "Asia", "hong-kong-hk"),
    ("bali", "Bali", "Indonesia", "Asia", "bali-id"),
    ("bandung", "Bandung", "Indonesia", "Asia", "bandung-id"),
    ("jakarta", "Jakarta", "Indonesia", "Asia", "jakarta-id"),
    ("surabaya", "Surabaya", "Indonesia", "Asia", "surabaya-id"),
    ("yogyakarta", "Yogyakarta", "Indonesia", "Asia", "yogyakarta-id"),
    ("fukuoka", "Fukuoka", "Japan", "Asia", "fukuoka-jp"),
    ("kyoto", "Kyoto", "Japan", "Asia", "kyoto-jp"),
    ("nagoya", "Nagoya", "Japan", "Asia", "nagoya-jp"),
    ("okinawa-main-island", "Okinawa", "Japan", "Asia", "okinawa-main-island-jp"),
    ("osaka", "Osaka", "Japan", "Asia", "osaka-jp"),
    ("sapporo", "Sapporo", "Japan", "Asia", "sapporo-jp"),
    ("tokyo", "Tokyo", "Japan", "Asia", "tokyo-jp"),
    ("macau", "Macau", "Macau", "Asia", "macau-mo"),
    ("ipoh", "Ipoh", "Malaysia", "Asia", "ipoh-my"),
    ("johor-bahru", "Johor Bahru", "Malaysia", "Asia", "johor-bahru-my"),
    ("kota-kinabalu", "Kota Kinabalu", "Malaysia", "Asia", "kota-kinabalu-my"),
    ("kuala-lumpur", "Kuala Lumpur", "Malaysia", "Asia", "kuala-lumpur-my"),
    ("kuantan", "Kuantan", "Malaysia", "Asia", "kuantan-my"),
    ("malacca", "Malacca", "Malaysia", "Asia", "malacca-my"),
    ("penang", "Penang", "Malaysia", "Asia", "penang-my"),
    ("port-dickson", "Port Dickson", "Malaysia", "Asia", "port-dickson-my"),
    ("boracay-island", "Boracay Island", "Philippines", "Asia", "boracay-island-ph"),
    ("cebu", "Cebu", "Philippines", "Asia", "cebu-ph"),
    ("manila", "Manila", "Philippines", "Asia", "manila-ph"),
    ("singapore", "Singapore", "Singapore", "Asia", "singapore-sg"),
    ("busan", "Busan", "South Korea", "Asia", "busan-kr"),
    ("jeju-island", "Jeju Island", "South Korea", "Asia", "jeju-kr"),
    ("seoul", "Seoul", "South Korea", "Asia", "seoul-kr"),
    ("hualien", "Hualien", "Taiwan", "Asia", "hualien-tw"),
    ("kaohsiung", "Kaohsiung", "Taiwan", "Asia", "kaohsiung-tw"),
    ("taichung", "Taichung", "Taiwan", "Asia", "taichung-tw"),
    ("tainan", "Tainan", "Taiwan", "Asia", "tainan-tw"),
    ("taipei", "Taipei", "Taiwan", "Asia", "taipei-tw"),
    ("yilan", "Yilan", "Taiwan", "Asia", "yilan-tw"),
    ("bangkok", "Bangkok", "Thailand", "Asia", "bangkok-th"),
    ("chiang-mai", "Chiang Mai", "Thailand", "Asia", "chiang-mai-th"),
    ("hat-yai", "Hat Yai", "Thailand", "Asia", "hat-yai-th"),
    ("hua-hin-cha-am", "Hua Hin", "Thailand", "Asia", "hua-hin-cha-am-th"),
    ("koh-kood", "Koh Kood", "Thailand", "Asia", "koh-kood-th"),
    ("koh-lanta", "Koh Lanta", "Thailand", "Asia", "koh-lanta-th"),
    ("koh-phangan", "Koh Phangan", "Thailand", "Asia", "ko-pha-ngan-th"),
    ("koh-samet", "Koh Samet", "Thailand", "Asia", "ko-samet-th"),
    ("krabi", "Krabi", "Thailand", "Asia", "krabi-th"),
    ("pattaya", "Pattaya", "Thailand", "Asia", "pattaya-th"),
    ("phuket", "Phuket", "Thailand", "Asia", "phuket-th"),
    ("da-nang", "Da Nang", "Vietnam", "Asia", "da-nang-vn"),
    ("hanoi", "Hanoi", "Vietnam", "Asia", "hanoi-vn"),
    ("ho-chi-minh-city", "Ho Chi Minh City", "Vietnam", "Asia", "ho-chi-minh-city-vn"),
    ("hoi-an", "Hoi An", "Vietnam", "Asia", "hoi-an-vn"),
    ("nha-trang", "Nha Trang", "Vietnam", "Asia", "nha-trang-vn"),
    ("phu-quoc-island", "Phu Quoc Island", "Vietnam", "Asia", "phu-quoc-island-vn"),
    ("paris", "Paris", "France", "Europe", "paris-fr"),
    ("london", "London", "United Kingdom", "Europe", "london-gb"),
    ("dubai", "Dubai", "United Arab Emirates", "Middle East", "dubai-ae"),
)


def _group_destinations() -> dict[str, dict[str, dict[str, str]]]:
    """Group the destination table into the spider's categories contract."""
    grouped: dict[str, dict[str, dict[str, str]]] = {}
    for leaf, city, country, region, slug in _AGODA_DESTINATIONS:
        grouped.setdefault(country, {})[leaf] = {
            "url": f"https://www.agoda.com/city/{slug}.html",
            "city": city,
            "country": country,
            "region": region,
        }
    return grouped


AGODA_CATEGORIES = _group_destinations()
