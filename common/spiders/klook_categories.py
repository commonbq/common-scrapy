"""Homepage popular-destination inventory captured from Klook (2026-10-06)."""

KLOOK_CATEGORIES = [
    {"category": slug, "url": f"https://www.klook.com/en-US/destination/{path}/"}
    for slug, path in (
        ("japan", "co1012-japan"), ("south-korea", "co1010-south-korea"),
        ("singapore", "co1015-singapore"), ("thailand", "co1004-thailand"),
        ("united-states", "co1028-united-states"), ("philippines", "co1016-philippines"),
        ("vietnam", "co1013-vietnam"), ("malaysia", "co1019-malaysia"),
        ("mainland-china", "co1020-mainland-china"), ("france", "co1033-france"),
        ("australia", "co1022-australia"), ("italy", "co1027-italy"),
        ("tokyo", "c28-tokyo"), ("osaka", "c29-osaka"),
        ("hong-kong", "c2-hong-kong"), ("kyoto", "c30-kyoto"),
        ("bangkok", "c4-bangkok"), ("dubai", "c78-dubai"),
        ("taipei", "c19-taipei"), ("seoul", "c13-seoul"),
    )
]
