"""O'Reilly Auto Parts root taxonomy and hydration helpers."""

from __future__ import annotations

import re
from html import unescape
from urllib.parse import urljoin

BASE_URL = "https://www.oreillyauto.com"
TAXONOMY_URL = f"{BASE_URL}/shop/b"

_ROOTS = {
    "Brakes": "/shop/b/brakes/b6d08f551887",
    "Battery & Accessories": "/shop/b/battery---accessories/e34ce9cab50d",
    "Oil, Chemicals & Fluids": "/shop/b/oil--chemicals---fluids/738983331189",
    "Filters": "/shop/b/filters/a33cc96e8cbd",
    "Engine Cooling": "/shop/b/engine-cooling/f16216eddf0b",
    "Ignition & Tune-Up": "/shop/b/ignition---tune-up/fa0bd697c4a4",
    "Alternators & Starters": "/shop/b/alternators---starters/58e8697eda89",
    "Engine Sensors & Emissions": "/shop/b/engine-sensors---emissions/f86377960d7d",
    "Accessories": "/shop/b/accessories/95397663b44a",
    "Air Conditioning & Heating": "/shop/b/air-conditioning---heating/4a2cd316965f",
    "Bearings & Seals": "/shop/b/bearings---seals/974c885c6e92",
    "Belts & Hoses": "/shop/b/belts---hoses/82cfa559d937",
    "CV, Driveshaft & Axle": "/shop/b/cv--driveshaft---axle/9d4c03dabbbc",
    "Chassis & Steering": "/shop/b/chassis---steering/66a05f5c0d20",
    "Detailing": "/shop/b/detailing/f84be123a823",
    "Engines & Transmissions": "/shop/b/engines---transmissions/f92b326ad189",
    "Exhaust": "/shop/b/exhaust/48d3bc1698db",
    "Fuel Delivery": "/shop/b/fuel-delivery/aa01378fb768",
    "Gaskets": "/shop/b/gaskets/0bfffccd28d3",
    "Hardware & Fasteners": "/shop/b/hardware---fasteners/9d359669ef3c",
    "Heavy Duty, Ag & Fleet": "/shop/b/heavy-duty--ag---fleet/bb87ab4ec32d",
    "Lawn and Garden": "/shop/b/lawn-and-garden/04d6d1a70c9c",
    "Lighting & Electrical": "/shop/b/lighting---electrical/ed67eafa9682",
    "Marine & Boat": "/shop/b/marine---boat/cac8941580dc",
    "More Powersport": "/shop/b/more-powersport/8d753a62dd89",
    "Paint & Body": "/shop/b/paint---body/4708c4d5edec",
    "Performance": "/shop/b/performance/2fa4e31cd340",
    "Recreational Vehicle": "/shop/b/recreational-vehicle/ebee19ea9559",
    "Shocks & Struts": "/shop/b/shocks---struts/3f97252e3df6",
    "Tire & Wheel": "/shop/b/tire---wheel/b52728c6ff53",
    "Tools & Equipment": "/shop/b/tools---equipment/f2b563093bad",
    "Trailer & Towing": "/shop/b/trailer---towing/afaee06e338b",
    "Turbocharger & Supercharger": "/shop/b/turbocharger---supercharger/56ca8d9a1f2d",
    "Wipers & Components": "/shop/b/wipers---components/f2ff19411853",
}

OREILLY_CATEGORIES = [
    {"category": re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"),
     "category_path": name, "url": urljoin(BASE_URL, path)}
    for name, path in _ROOTS.items()
]


def child_categories(text: str) -> list[dict[str, str]]:
    """Decode the authoritative ``window._ost.childCategories`` assignment."""
    marker = re.search(r"window\._ost\.childCategories\s*=\s*\[", text)
    if not marker:
        return []
    end = text.find("</script>", marker.end())
    source = text[marker.end(): end if end >= 0 else len(text)]
    out = []
    for obj in re.findall(r"\{[^{}]*\}", source, re.S):
        name = re.search(r"['\"]hierarchyDescription['\"]\s*:\s*['\"](.*?)['\"]", obj, re.S)
        url = re.search(r"['\"]url['\"]\s*:\s*['\"](.*?)['\"]", obj, re.S)
        if name and url:
            out.append({"name": unescape(name.group(1)), "url": urljoin(BASE_URL, url.group(1))})
    return sorted(out, key=lambda item: (item["name"].lower(), item["url"]))
