"""Homepage destination inventory captured from Klook (2026-10-13)."""


def _destination(path: str) -> str:
    return f"https://www.klook.com/en-US/destination/{path}/"


KLOOK_CATEGORIES = {
    "popular-regions": {
        "japan": _destination("co1012-japan"),
        "south-korea": _destination("co1010-south-korea"),
        "singapore": _destination("co1015-singapore"),
        "thailand": _destination("co1004-thailand"),
        "united-states": _destination("co1028-united-states"),
        "philippines": _destination("co1016-philippines"),
        "vietnam": _destination("co1013-vietnam"),
        "malaysia": _destination("co1019-malaysia"),
        "mainland-china": _destination("co1020-mainland-china"),
        "france": _destination("co1033-france"),
        "australia": _destination("co1022-australia"),
        "italy": _destination("co1027-italy"),
    },
    "popular-destinations": {
        "tokyo": _destination("c28-tokyo"),
        "osaka": _destination("c29-osaka"),
        "hong-kong": _destination("c2-hong-kong"),
        "kyoto": _destination("c30-kyoto"),
        "bangkok": _destination("c4-bangkok"),
        "dubai": _destination("c78-dubai"),
        "taipei": _destination("c19-taipei"),
        "seoul": _destination("c13-seoul"),
        "los-angeles": _destination("c124-los-angeles"),
        "shanghai": _destination("c59-shanghai"),
        "paris": _destination("c107-paris"),
        "kuala-lumpur": _destination("c49-kuala-lumpur"),
        "narita": _destination("c18170-narita"),
        "yokohama": _destination("c26895-yokohama"),
        "phuket": _destination("c7-phuket"),
        "sapporo": _destination("c133938-sapporo"),
        "new-york": _destination("c93-new-york"),
        "ho-chi-minh": _destination("c33-ho-chi-minh-city"),
        "pattaya": _destination("c17-pattaya"),
        "orlando": _destination("c700841-orlando"),
        "da-nang": _destination("c74-da-nang"),
        "abu-dhabi": _destination("c131-abu-dhabi"),
        "nagoya": _destination("c71-nagoya"),
        "manila": _destination("c96-manila"),
        "queenstown": _destination("c83-queenstown"),
        "kaohsiung": _destination("c22-kaohsiung"),
        "hanoi": _destination("c34-hanoi"),
        "phu-quoc": _destination("c130-phu-quoc"),
    },
}
