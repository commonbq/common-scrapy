"""Ordered Agoda destination inventory refreshed from the live homepage.

Source: https://www.agoda.com homepage (fetched 2026-10-15).
The homepage exposes 56 destination city pages; the previous inventory
held only a curated 20. Every entry below is a live
``/city/<slug>-<country>.html`` route, kept in alphabetical order and
preserved as the base spider's dict contract
(``{"destinations": {"<slug>": "<url>"}}``).
"""

from __future__ import annotations

AGODA_CATEGORIES = {
    "destinations": {
        "bali": "https://www.agoda.com/city/bali-id.html",
        "bandung": "https://www.agoda.com/city/bandung-id.html",
        "bangkok": "https://www.agoda.com/city/bangkok-th.html",
        "boracay-island": "https://www.agoda.com/city/boracay-island-ph.html",
        "busan": "https://www.agoda.com/city/busan-kr.html",
        "cebu": "https://www.agoda.com/city/cebu-ph.html",
        "chiang-mai": "https://www.agoda.com/city/chiang-mai-th.html",
        "da-nang": "https://www.agoda.com/city/da-nang-vn.html",
        "dubai": "https://www.agoda.com/city/dubai-ae.html",
        "fukuoka": "https://www.agoda.com/city/fukuoka-jp.html",
        "hanoi": "https://www.agoda.com/city/hanoi-vn.html",
        "hat-yai": "https://www.agoda.com/city/hat-yai-th.html",
        "ho-chi-minh-city": "https://www.agoda.com/city/ho-chi-minh-city-vn.html",
        "hoi-an": "https://www.agoda.com/city/hoi-an-vn.html",
        "hong-kong": "https://www.agoda.com/city/hong-kong-hk.html",
        "hua-hin": "https://www.agoda.com/city/hua-hin-cha-am-th.html",
        "hualien": "https://www.agoda.com/city/hualien-tw.html",
        "ipoh": "https://www.agoda.com/city/ipoh-my.html",
        "jakarta": "https://www.agoda.com/city/jakarta-id.html",
        "jeju-island": "https://www.agoda.com/city/jeju-island-kr.html",
        "johor-bahru": "https://www.agoda.com/city/johor-bahru-my.html",
        "kaohsiung": "https://www.agoda.com/city/kaohsiung-tw.html",
        "koh-kood": "https://www.agoda.com/city/koh-kood-th.html",
        "koh-lanta": "https://www.agoda.com/city/koh-lanta-th.html",
        "koh-phangan": "https://www.agoda.com/city/koh-phangan-th.html",
        "koh-samet": "https://www.agoda.com/city/koh-samet-th.html",
        "kota-kinabalu": "https://www.agoda.com/city/kota-kinabalu-my.html",
        "krabi": "https://www.agoda.com/city/krabi-th.html",
        "kuala-lumpur": "https://www.agoda.com/city/kuala-lumpur-my.html",
        "kuantan": "https://www.agoda.com/city/kuantan-my.html",
        "kyoto": "https://www.agoda.com/city/kyoto-jp.html",
        "london": "https://www.agoda.com/city/london-gb.html",
        "macau": "https://www.agoda.com/city/macau-mo.html",
        "malacca": "https://www.agoda.com/city/malacca-my.html",
        "manila": "https://www.agoda.com/city/manila-ph.html",
        "nagoya": "https://www.agoda.com/city/nagoya-jp.html",
        "nha-trang": "https://www.agoda.com/city/nha-trang-vn.html",
        "okinawa-main-island": "https://www.agoda.com/city/okinawa-main-island-jp.html",
        "osaka": "https://www.agoda.com/city/osaka-jp.html",
        "paris": "https://www.agoda.com/city/paris-fr.html",
        "pattaya": "https://www.agoda.com/city/pattaya-th.html",
        "penang": "https://www.agoda.com/city/penang-my.html",
        "phuket": "https://www.agoda.com/city/phuket-th.html",
        "phu-quoc-island": "https://www.agoda.com/city/phu-quoc-island-vn.html",
        "port-dickson": "https://www.agoda.com/city/port-dickson-my.html",
        "sapporo": "https://www.agoda.com/city/sapporo-jp.html",
        "seoul": "https://www.agoda.com/city/seoul-kr.html",
        "shanghai": "https://www.agoda.com/city/shanghai-cn.html",
        "singapore": "https://www.agoda.com/city/singapore-sg.html",
        "surabaya": "https://www.agoda.com/city/surabaya-id.html",
        "taichung": "https://www.agoda.com/city/taichung-tw.html",
        "tainan": "https://www.agoda.com/city/tainan-tw.html",
        "taipei": "https://www.agoda.com/city/taipei-tw.html",
        "tokyo": "https://www.agoda.com/city/tokyo-jp.html",
        "yilan": "https://www.agoda.com/city/yilan-tw.html",
        "yogyakarta": "https://www.agoda.com/city/yogyakarta-id.html",
    },
}
