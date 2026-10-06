"""CVS.com shop category inventory captured from the storefront bootstrap state.

The taxonomy is not hand-maintained and not read from presentation markup: it comes
from the same SSR hydration payload the spider parses products out of::

    var initialState = {
      "allCategories": {"allCategories": {"children": [...]}},
      "productIndexData": {...}
    };

Specifically ``initialState.allCategories.allCategories.children`` -- the live named
shop hierarchy CVS ships with every shop page (15 roots, 856 nodes, 730 distinct
browse URLs before filtering).

Captured: 2026-10-04 (US storefront, ``https://www.cvs.com/shop/health-medicine``).

Filtering applied when generating this module:

* Each node's first child repeats the parent as an "All <department>" landing link
  (``{"id": "cat1", "title": "Health & Medicine", "allCat": true}``). Those
  self-links are dropped; the parent entry keeps that URL and id.
* Non-shop navigation is excluded: the whole ``/shop/brand-directory`` tree and
  content pages such as ``/shop/content/fsa`` are not product listings.

Result: 13 departments and 715 category/subcategory URLs through L4, each carrying
its CVS ``cat*`` id (the same ids the ``facets.facetFields`` category refinements use).
"""

from __future__ import annotations

CVS_CATEGORY_INVENTORY: dict[str, dict] = {
    "Health & Medicine": {
        "url": "/shop/health-medicine",
        "id": "cat1",
        "subcategories": {
            "Allergy & Sinus": {
                "url": "/shop/health-medicine/allergy-sinus",
                "id": "cat510006",
                "subcategories": {
                    "Allergy Medicine": {"url": "/shop/health-medicine/allergy-sinus/allergy-medicine", "id": "cat510010"},
                    "Sinus & Congestion Relief": {"url": "/shop/health-medicine/allergy-sinus/sinus-congestion-relief", "id": "cat1690023"},
                    "Allergy Eye Drops": {"url": "/shop/health-medicine/allergy-sinus/allergy-eye-drops", "id": "cat510012"},
                    "Baby & Kids Allergy": {"url": "/shop/health-medicine/allergy-sinus/baby-kids-allergy", "id": "cat225226833"},
                    "Asthma Treatment": {"url": "/shop/health-medicine/allergy-sinus/asthma-treatment", "id": "cat510014"},
                    "Humidifiers": {"url": "/shop/health-medicine/allergy-sinus/humidifiers", "id": "cat510016"},
                },
            },
            "Cough, Cold & Flu": {
                "url": "/shop/health-medicine/cough-cold-flu",
                "id": "cat510034",
                "subcategories": {
                    "Cold & Flu Medicine": {"url": "/shop/health-medicine/cough-cold-flu/cold-flu-medicine", "id": "cat510044"},
                    "Cough Medicine": {
                        "url": "/shop/health-medicine/cough-cold-flu/cough-medicine",
                        "id": "cat510042",
                        "subcategories": {
                            "Cough Syrup": {"url": "/shop/health-medicine/cough-cold-flu/cough-medicine/cough-syrup", "id": "cat3010006"},
                            "Cough Pills": {"url": "/shop/health-medicine/cough-cold-flu/cough-medicine/cough-pills", "id": "cat3010007"},
                            "Cough Drops": {"url": "/shop/health-medicine/cough-cold-flu/cough-medicine/cough-drops", "id": "cat510040"},
                            "Sore Throat Relief": {"url": "/shop/health-medicine/cough-cold-flu/cough-medicine/sore-throat-relief", "id": "cat3010008"},
                        },
                    },
                    "Baby & Kids Cough, Cold & Flu": {"url": "/shop/health-medicine/cough-cold-flu/baby-kids-cough-cold-flu", "id": "cat225226845"},
                    "Sinus Relief": {"url": "/shop/health-medicine/cough-cold-flu/sinus-relief", "id": "cat510050"},
                    "Chest Rub": {"url": "/shop/health-medicine/cough-cold-flu/chest-rub", "id": "cat510036"},
                    "Immune Support": {"url": "/shop/health-medicine/cough-cold-flu/immune-support", "id": "cat510046"},
                    "Humidifiers": {"url": "/shop/health-medicine/cough-cold-flu/humidifiers", "id": "cat2190003"},
                    "Sleep & Snoring Aids": {
                        "url": "/shop/health-medicine/cough-cold-flu/sleep-snoring-aids",
                        "id": "cat2190002",
                        "subcategories": {
                            "Nasal Strips & Snoring Aids": {"url": "/shop/health-medicine/cough-cold-flu/sleep-snoring-aids/nasal-strips-snoring-aids", "id": "cat2190014"},
                            "Ear Plugs": {"url": "/shop/health-medicine/cough-cold-flu/sleep-snoring-aids/ear-plugs", "id": "cat2190012"},
                            "Sleep Medicine & Supplements": {"url": "/shop/health-medicine/cough-cold-flu/sleep-snoring-aids/sleep-medicine-supplements", "id": "cat2190013"},
                        },
                    },
                    "Cold Sore Treatment": {"url": "/shop/health-medicine/cough-cold-flu/cold-sore-treatment", "id": "cat510048"},
                    "At-Home COVID-19 Tests": {"url": "/shop/health-medicine/cough-cold-flu/at-home-covid-19-tests", "id": "cat3030039"},
                },
            },
            "Pain & Fever": {
                "url": "/shop/health-medicine/pain-fever",
                "id": "cat510098",
                "subcategories": {
                    "Pain Relievers": {"url": "/shop/health-medicine/pain-fever/pain-relievers", "id": "cat510114"},
                    "Arthritis Relief": {"url": "/shop/health-medicine/pain-fever/arthritis-relief", "id": "cat510100"},
                    "External Relief": {"url": "/shop/health-medicine/pain-fever/external-relief", "id": "cat510106"},
                    "Oral Pain Relief": {"url": "/shop/health-medicine/pain-fever/oral-pain-relief", "id": "cat1460001"},
                    "Hemorrhoid Treatment": {"url": "/shop/health-medicine/pain-fever/hemorrhoid-treatment", "id": "cat2190005"},
                    "Hot or Cold Therapy": {"url": "/shop/health-medicine/pain-fever/hot-or-cold-therapy", "id": "cat510104"},
                    "Pain Relief Devices": {"url": "/shop/health-medicine/pain-fever/pain-relief-devices", "id": "cat510116"},
                    "Migraine Relief": {"url": "/shop/health-medicine/pain-fever/migraine-relief", "id": "cat510110"},
                    "Menstrual Pain Relief": {"url": "/shop/health-medicine/pain-fever/menstrual-pain-relief", "id": "cat510108"},
                    "Baby & Kids Pain & Fever": {"url": "/shop/health-medicine/pain-fever/baby-kids-pain-fever", "id": "cat225226847"},
                    "Heart Health": {"url": "/shop/health-medicine/pain-fever/heart-health", "id": "cat510102"},
                    "Urinary Tract Infection": {"url": "/shop/health-medicine/pain-fever/urinary-tract-infection", "id": "cat1460002"},
                },
            },
            "First Aid": {
                "url": "/shop/health-medicine/first-aid",
                "id": "cat510074",
                "subcategories": {
                    "Bandages, Gauze & Tape": {"url": "/shop/health-medicine/first-aid/bandages-gauze-tape", "id": "cat510078"},
                    "Antibiotic & Antiseptic": {"url": "/shop/health-medicine/first-aid/antibiotic-antiseptic", "id": "cat510076"},
                    "Itch & Rash Treatment": {"url": "/shop/health-medicine/first-aid/itch-rash-treatment", "id": "cat510088"},
                    "Burn Treatment": {"url": "/shop/health-medicine/first-aid/burn-treatment", "id": "cat510080"},
                    "Lice Treatment": {"url": "/shop/health-medicine/first-aid/lice-treatment", "id": "cat510090"},
                    "Scar Treatment": {"url": "/shop/health-medicine/first-aid/scar-treatment", "id": "cat510092"},
                    "Wart Removal": {"url": "/shop/health-medicine/first-aid/wart-removal", "id": "cat510096"},
                    "First Aid Kits & Accessories": {"url": "/shop/health-medicine/first-aid/first-aid-kits-accessories", "id": "cat510082"},
                    "Masks & Gloves": {"url": "/shop/health-medicine/first-aid/masks-gloves", "id": "cat510094"},
                },
            },
            "Digestive Health": {
                "url": "/shop/health-medicine/digestive-health",
                "id": "cat510052",
                "subcategories": {
                    "Laxatives & Constipation Relief": {"url": "/shop/health-medicine/digestive-health/laxatives-constipation-relief", "id": "cat1450002"},
                    "Heartburn Relief": {"url": "/shop/health-medicine/digestive-health/heartburn-relief", "id": "cat510064"},
                    "Antacid": {"url": "/shop/health-medicine/digestive-health/antacid", "id": "cat510054"},
                    "Probiotics": {"url": "/shop/health-medicine/digestive-health/probiotics", "id": "cat510072"},
                    "Fiber": {"url": "/shop/health-medicine/digestive-health/fiber", "id": "cat1450001"},
                    "Anti-Diarrhea": {"url": "/shop/health-medicine/digestive-health/anti-diarrhea", "id": "cat510056"},
                    "Gas Relief": {"url": "/shop/health-medicine/digestive-health/gas-relief", "id": "cat510066"},
                    "Motion Sickness & Nausea": {"url": "/shop/health-medicine/digestive-health/motion-sickness-nausea", "id": "cat510070"},
                    "Lactose Intolerance": {"url": "/shop/health-medicine/digestive-health/lactose-intolerance", "id": "cat510068"},
                    "Baby & Kids Digestive Health": {"url": "/shop/health-medicine/digestive-health/baby-kids-digestive-health", "id": "cat225226846"},
                },
            },
            "Braces & Supports": {
                "url": "/shop/health-medicine/braces-supports",
                "id": "cat510020",
                "subcategories": {
                    "Foot & Ankle Braces": {"url": "/shop/health-medicine/braces-supports/foot-ankle-braces", "id": "cat510024"},
                    "Hand & Wrist Braces": {"url": "/shop/health-medicine/braces-supports/hand-wrist-braces", "id": "cat510026"},
                    "Thigh & Knee Braces": {"url": "/shop/health-medicine/braces-supports/thigh-knee-braces", "id": "cat510030"},
                    "Arm & Elbow Braces": {"url": "/shop/health-medicine/braces-supports/arm-elbow-braces", "id": "cat510022"},
                    "Compression Hosiery & Stockings": {"url": "/shop/health-medicine/braces-supports/compression-hosiery-stockings", "id": "cat2190001"},
                    "Waist & Back Braces": {"url": "/shop/health-medicine/braces-supports/waist-back-braces", "id": "cat510032"},
                    "Shoulder & Neck Braces": {"url": "/shop/health-medicine/braces-supports/shoulder-neck-braces", "id": "cat510028"},
                },
            },
            "Sleep & Snoring Aids": {
                "url": "/shop/health-medicine/sleep-snoring-aids",
                "id": "cat510124",
                "subcategories": {
                    "Sleep Medicine & Supplements": {"url": "/shop/health-medicine/sleep-snoring-aids/sleep-medicine-supplements", "id": "cat510130"},
                    "Nasal Strips & Snoring Aids": {"url": "/shop/health-medicine/sleep-snoring-aids/nasal-strips-snoring-aids", "id": "cat510132"},
                    "Ear Plugs": {"url": "/shop/health-medicine/sleep-snoring-aids/ear-plugs", "id": "cat510126"},
                },
            },
            "Home Tests": {
                "url": "/shop/health-medicine/home-tests",
                "id": "cat2210001",
                "subcategories": {
                    "At-Home COVID-19 Tests": {"url": "/shop/health-medicine/home-tests/at-home-covid-19-tests", "id": "cat2320003"},
                    "STD & HIV Tests": {"url": "/shop/health-medicine/home-tests/std-hiv-tests", "id": "cat2210010"},
                    "Alcohol & Drug Tests": {"url": "/shop/health-medicine/home-tests/alcohol-drug-tests", "id": "cat2210002"},
                    "Cholesterol & Dietary Tests": {"url": "/shop/health-medicine/home-tests/cholesterol-dietary-tests", "id": "cat2210004"},
                    "Fertility & Pregnancy Tests": {"url": "/shop/health-medicine/home-tests/fertility-pregnancy-tests", "id": "cat2210006"},
                    "Parental, DNA & Gender Tests": {"url": "/shop/health-medicine/home-tests/parental-dna-gender-tests", "id": "cat2210009"},
                },
            },
            "Stop Smoking": {
                "url": "/shop/health-medicine/stop-smoking",
                "id": "cat510134",
                "subcategories": {
                    "Nicotine Gum": {"url": "/shop/health-medicine/stop-smoking/nicotine-gum", "id": "cat510136"},
                    "Nicotine Lozenges": {"url": "/shop/health-medicine/stop-smoking/nicotine-lozenges", "id": "cat510138"},
                    "Nicotine Patches": {"url": "/shop/health-medicine/stop-smoking/nicotine-patches", "id": "cat510140"},
                },
            },
            "Trial & Travel Size Health & Medicine": {"url": "/shop/health-medicine/trial-travel-size-health-medicine", "id": "cat1870005"},
        },
    },
    "Beauty": {
        "url": "/shop/beauty",
        "id": "cat3361",
        "subcategories": {
            "Makeup": {
                "url": "/shop/beauty/makeup",
                "id": "cat900027",
                "subcategories": {
                    "Face": {
                        "url": "/shop/beauty/makeup/face",
                        "id": "cat900029",
                        "subcategories": {
                            "Foundation": {"url": "/shop/beauty/makeup/face/foundation", "id": "cat1500020"},
                            "Concealers & Correctors": {"url": "/shop/beauty/makeup/face/concealers-correctors", "id": "cat1500018"},
                            "Blush": {"url": "/shop/beauty/makeup/face/blush", "id": "cat1500022"},
                            "BB & CC Creams": {"url": "/shop/beauty/makeup/face/bb-cc-creams", "id": "cat1500019"},
                            "Setting Spray & Powder": {"url": "/shop/beauty/makeup/face/setting-spray-powder", "id": "cat1500023"},
                            "Face Primer": {"url": "/shop/beauty/makeup/face/face-primer", "id": "cat1500017"},
                            "Contouring & Highlighting": {"url": "/shop/beauty/makeup/face/contouring-highlighting", "id": "cat1500021"},
                            "Bronzer": {"url": "/shop/beauty/makeup/face/bronzer", "id": "cat3090004"},
                            "Kits & Palettes": {"url": "/shop/beauty/makeup/face/kits-palettes", "id": "cat1500025"},
                        },
                    },
                    "Eyes": {
                        "url": "/shop/beauty/makeup/eyes",
                        "id": "cat900028",
                        "subcategories": {
                            "Mascara": {"url": "/shop/beauty/makeup/eyes/mascara", "id": "cat1500011"},
                            "Eyeshadow & Palettes": {"url": "/shop/beauty/makeup/eyes/eyeshadow-palettes", "id": "cat1500010"},
                            "Eyeliner": {"url": "/shop/beauty/makeup/eyes/eyeliner", "id": "cat1500012"},
                            "Eyebrows": {"url": "/shop/beauty/makeup/eyes/eyebrows", "id": "cat1500013"},
                            "Fake Eyelashes": {"url": "/shop/beauty/makeup/eyes/fake-eyelashes", "id": "cat1500015"},
                            "Eye Primer & Base": {"url": "/shop/beauty/makeup/eyes/eye-primer-base", "id": "cat1500014"},
                        },
                    },
                    "Lips": {
                        "url": "/shop/beauty/makeup/lips",
                        "id": "cat900030",
                        "subcategories": {
                            "Lipstick": {"url": "/shop/beauty/makeup/lips/lipstick", "id": "cat1500005"},
                            "Lip Gloss & Plumpers": {"url": "/shop/beauty/makeup/lips/lip-gloss-plumpers", "id": "cat1500006"},
                            "Lip Tints & Stains": {"url": "/shop/beauty/makeup/lips/lip-tints-stains", "id": "cat1500009"},
                            "Lip Liner": {"url": "/shop/beauty/makeup/lips/lip-liner", "id": "cat1500007"},
                            "Lip Balm & Treatments": {"url": "/shop/beauty/makeup/lips/lip-balm-treatments", "id": "cat1500008"},
                        },
                    },
                    "Makeup Removers & Wipes": {"url": "/shop/beauty/makeup/makeup-removers-wipes", "id": "cat2450012"},
                    "Makeup Bags & Cases": {"url": "/shop/beauty/makeup/makeup-bags-cases", "id": "cat2450011"},
                },
            },
            "Hair Care": {
                "url": "/shop/beauty/hair-care",
                "id": "cat900022",
                "subcategories": {
                    "Shampoo & Conditioner": {
                        "url": "/shop/beauty/hair-care/shampoo-conditioner",
                        "id": "cat900024",
                        "subcategories": {
                            "Shampoo": {"url": "/shop/beauty/hair-care/shampoo-conditioner/shampoo", "id": "cat1910005"},
                            "Conditioner": {"url": "/shop/beauty/hair-care/shampoo-conditioner/conditioner", "id": "cat1910006"},
                            "Dry Shampoo": {"url": "/shop/beauty/hair-care/shampoo-conditioner/dry-shampoo", "id": "cat1910007"},
                        },
                    },
                    "Hair Color": {
                        "url": "/shop/beauty/hair-care/hair-color",
                        "id": "cat900023",
                        "subcategories": {
                            "Permanent Hair Color": {"url": "/shop/beauty/hair-care/hair-color/permanent-hair-color", "id": "cat2250001"},
                            "Root Touch Up": {"url": "/shop/beauty/hair-care/hair-color/root-touch-up", "id": "cat2250003"},
                            "Semi-Permanent Hair Color": {"url": "/shop/beauty/hair-care/hair-color/semi-permanent-hair-color", "id": "cat2250002"},
                            "Color Care": {"url": "/shop/beauty/hair-care/hair-color/color-care", "id": "cat2250006"},
                            "Bold Hair Color": {"url": "/shop/beauty/hair-care/hair-color/bold-hair-color", "id": "cat2250004"},
                            "Men's Hair Color": {"url": "/shop/beauty/hair-care/hair-color/mens-hair-color", "id": "cat2250005"},
                        },
                    },
                    "Styling": {
                        "url": "/shop/beauty/hair-care/styling",
                        "id": "cat900025",
                        "subcategories": {
                            "Hair Spray": {"url": "/shop/beauty/hair-care/styling/hair-spray", "id": "cat1910009"},
                            "Hair Gel, Wax, & Pomades": {"url": "/shop/beauty/hair-care/styling/hair-gel-wax-pomades", "id": "cat1910011"},
                            "Heat Protectants": {"url": "/shop/beauty/hair-care/styling/heat-protectants", "id": "cat1910012"},
                            "Hair Mousse & Creams": {"url": "/shop/beauty/hair-care/styling/hair-mousse-creams", "id": "cat1910010"},
                        },
                    },
                    "Treatments": {
                        "url": "/shop/beauty/hair-care/treatments",
                        "id": "cat900026",
                        "subcategories": {
                            "Hair Regrowth": {"url": "/shop/beauty/hair-care/treatments/hair-regrowth", "id": "cat1540003"},
                            "Hair Oils & Serums": {"url": "/shop/beauty/hair-care/treatments/hair-oils-serums", "id": "cat1910013"},
                            "Hair Masks": {"url": "/shop/beauty/hair-care/treatments/hair-masks", "id": "cat1910016"},
                            "Leave-in Treatments": {"url": "/shop/beauty/hair-care/treatments/leave-in-treatments", "id": "cat1910015"},
                            "Scalp Treatments": {"url": "/shop/beauty/hair-care/treatments/scalp-treatments", "id": "cat1910014"},
                        },
                    },
                    "Hair Tools & Appliances": {
                        "url": "/shop/beauty/hair-care/hair-tools-appliances",
                        "id": "cat2450013",
                        "subcategories": {
                            "Hair Dryers & Stylers": {"url": "/shop/beauty/hair-care/hair-tools-appliances/hair-dryers-stylers", "id": "cat3070028"},
                            "Curling Irons": {"url": "/shop/beauty/hair-care/hair-tools-appliances/curling-irons", "id": "cat3070029"},
                            "Flat Irons": {"url": "/shop/beauty/hair-care/hair-tools-appliances/flat-irons", "id": "cat3070030"},
                        },
                    },
                    "Textured Hair": {
                        "url": "/shop/beauty/hair-care/textured-hair",
                        "id": "cat1910004",
                        "subcategories": {
                            "Curl Creams & Polishers": {"url": "/shop/beauty/hair-care/textured-hair/curl-creams-polishers", "id": "cat2150009"},
                            "Styling Gels": {"url": "/shop/beauty/hair-care/textured-hair/styling-gels", "id": "cat2150010"},
                            "Leave-In Conditioners": {"url": "/shop/beauty/hair-care/textured-hair/leave-in-conditioners", "id": "cat2150007"},
                            "Hair Moisturizers": {"url": "/shop/beauty/hair-care/textured-hair/hair-moisturizers", "id": "cat2150008"},
                            "Deep Conditioners": {"url": "/shop/beauty/hair-care/textured-hair/deep-conditioners", "id": "cat2150006"},
                            "Shampoo & Co-Washes": {"url": "/shop/beauty/hair-care/textured-hair/shampoo-co-washes", "id": "cat2150005"},
                        },
                    },
                    "Hair Brushes & Combs": {"url": "/shop/beauty/hair-care/hair-brushes-combs", "id": "cat900016"},
                    "Hair Accessories": {
                        "url": "/shop/beauty/hair-care/hair-accessories",
                        "id": "cat900015",
                        "subcategories": {
                            "Hair Clips, Pins & Barrettes": {"url": "/shop/beauty/hair-care/hair-accessories/hair-clips-pins-barrettes", "id": "cat3070026"},
                            "Hair Elastics": {"url": "/shop/beauty/hair-care/hair-accessories/hair-elastics", "id": "cat3070024"},
                            "Headbands": {"url": "/shop/beauty/hair-care/hair-accessories/headbands", "id": "cat3070025"},
                            "Headwraps": {"url": "/shop/beauty/hair-care/hair-accessories/headwraps", "id": "cat3070027"},
                        },
                    },
                    "Men's Hair Care": {"url": "/shop/beauty/hair-care/mens-hair-care", "id": "cat1910018"},
                    "Trial & Travel Size Hair Care": {"url": "/shop/beauty/hair-care/trial-travel-size-hair-care", "id": "cat1870003"},
                },
            },
            "Skin Care": {
                "url": "/shop/beauty/skin-care",
                "id": "cat3369",
                "subcategories": {
                    "Lotions & Moisturizers": {
                        "url": "/shop/beauty/skin-care/lotions-moisturizers",
                        "id": "cat3100003",
                        "subcategories": {
                            "Face Creams & Moisturizers": {"url": "/shop/beauty/skin-care/lotions-moisturizers/face-creams-moisturizers", "id": "cat900034"},
                            "Body Lotions & Moisturizers": {"url": "/shop/beauty/skin-care/lotions-moisturizers/body-lotions-moisturizers", "id": "cat900032"},
                            "Eye Cream": {"url": "/shop/beauty/skin-care/lotions-moisturizers/eye-cream", "id": "cat1510018"},
                            "Hand Cream": {"url": "/shop/beauty/skin-care/lotions-moisturizers/hand-cream", "id": "cat1510006"},
                            "Lip Balm & Treatments": {"url": "/shop/beauty/skin-care/lotions-moisturizers/lip-balm-treatments", "id": "cat2450016"},
                            "Foot Cream": {"url": "/shop/beauty/skin-care/lotions-moisturizers/foot-cream", "id": "cat1510005"},
                        },
                    },
                    "Serums & Treatments": {"url": "/shop/beauty/skin-care/serums-treatments", "id": "cat1510024"},
                    "Cleansers & Exfoliants": {
                        "url": "/shop/beauty/skin-care/cleansers-exfoliants",
                        "id": "cat3100012",
                        "subcategories": {
                            "Face Wash": {"url": "/shop/beauty/skin-care/cleansers-exfoliants/face-wash", "id": "cat1510025"},
                            "Face Scrubs & Exfoliators": {"url": "/shop/beauty/skin-care/cleansers-exfoliants/face-scrubs-exfoliators", "id": "cat1510017"},
                            "Makeup Removers & Wipes": {"url": "/shop/beauty/skin-care/cleansers-exfoliants/makeup-removers-wipes", "id": "cat1510021"},
                            "Cleansing Oils & Balms": {"url": "/shop/beauty/skin-care/cleansers-exfoliants/cleansing-oils-balms", "id": "cat3100013"},
                            "Face Toners": {"url": "/shop/beauty/skin-care/cleansers-exfoliants/face-toners", "id": "cat1510026"},
                        },
                    },
                    "Sun & Tanning": {
                        "url": "/shop/beauty/skin-care/sun-tanning",
                        "id": "cat900037",
                        "subcategories": {
                            "Sunscreen": {"url": "/shop/beauty/skin-care/sun-tanning/sunscreen", "id": "cat1910002"},
                            "Self Tanner": {"url": "/shop/beauty/skin-care/sun-tanning/self-tanner", "id": "cat1910003"},
                            "After-Sun Care": {"url": "/shop/beauty/skin-care/sun-tanning/after-sun-care", "id": "cat1910001"},
                        },
                    },
                    "Dermatologist Tested Skin Care": {"url": "/shop/beauty/skin-care/dermatologist-tested-skin-care", "id": "cat1770002"},
                    "Acne Treatments": {"url": "/shop/beauty/skin-care/acne-treatments", "id": "cat1510015"},
                    "Body & Face Masks": {"url": "/shop/beauty/skin-care/body-face-masks", "id": "cat1510020"},
                    "Skin Care Tools": {"url": "/shop/beauty/skin-care/skin-care-tools", "id": "cat2450017"},
                    "Men's Skin Care": {
                        "url": "/shop/beauty/skin-care/mens-skin-care",
                        "id": "cat1970001",
                        "subcategories": {
                            "Men's Creams & Lotions": {"url": "/shop/beauty/skin-care/mens-skin-care/mens-creams-lotions", "id": "cat130007"},
                            "Men's Face Wash": {"url": "/shop/beauty/skin-care/mens-skin-care/mens-face-wash", "id": "cat1820001"},
                        },
                    },
                    "Eczema Treatments": {"url": "/shop/beauty/skin-care/eczema-treatments", "id": "cat1510011"},
                    "Trial & Travel Size Facial Skin Care": {"url": "/shop/beauty/skin-care/trial-travel-size-facial-skin-care", "id": "cat1870001"},
                },
            },
            "Nails": {
                "url": "/shop/beauty/nails",
                "id": "cat900031",
                "subcategories": {
                    "Nail Polish": {"url": "/shop/beauty/nails/nail-polish", "id": "cat1500031"},
                    "Fake Nails & Nail Art": {"url": "/shop/beauty/nails/fake-nails-nail-art", "id": "cat1500035"},
                    "Nail Tools": {"url": "/shop/beauty/nails/nail-tools", "id": "cat1500034"},
                    "Nail Polish Remover": {"url": "/shop/beauty/nails/nail-polish-remover", "id": "cat1500033"},
                    "Nail Treatments": {"url": "/shop/beauty/nails/nail-treatments", "id": "cat2120004"},
                    "Top & Base Coat": {"url": "/shop/beauty/nails/top-base-coat", "id": "cat1500032"},
                },
            },
            "Beauty Tools & Accessories": {
                "url": "/shop/beauty/beauty-tools-accessories",
                "id": "cat900010",
                "subcategories": {
                    "Hair Tools & Appliances": {"url": "/shop/beauty/beauty-tools-accessories/hair-tools-appliances", "id": "cat900017"},
                    "Skin Care Tools": {"url": "/shop/beauty/beauty-tools-accessories/skin-care-tools", "id": "cat900021"},
                    "Brow Tools & Tweezers": {"url": "/shop/beauty/beauty-tools-accessories/brow-tools-tweezers", "id": "cat900013"},
                    "Cotton Balls & Swabs": {"url": "/shop/beauty/beauty-tools-accessories/cotton-balls-swabs", "id": "cat900014"},
                    "Makeup Tools & Applicators": {
                        "url": "/shop/beauty/beauty-tools-accessories/makeup-tools-applicators",
                        "id": "cat900018",
                        "subcategories": {
                            "Blenders & Sponges": {"url": "/shop/beauty/beauty-tools-accessories/makeup-tools-applicators/blenders-sponges", "id": "cat2120007"},
                            "Eyelash Curlers": {"url": "/shop/beauty/beauty-tools-accessories/makeup-tools-applicators/eyelash-curlers", "id": "cat2120008"},
                            "Makeup Brushes": {"url": "/shop/beauty/beauty-tools-accessories/makeup-tools-applicators/makeup-brushes", "id": "cat2120003"},
                        },
                    },
                    "Makeup Bags & Cases": {"url": "/shop/beauty/beauty-tools-accessories/makeup-bags-cases", "id": "cat900011"},
                    "Nail Tools": {"url": "/shop/beauty/beauty-tools-accessories/nail-tools", "id": "cat900020"},
                    "Mirrors": {"url": "/shop/beauty/beauty-tools-accessories/mirrors", "id": "cat900019"},
                    "Trial & Travel Size Storage & Containers": {"url": "/shop/beauty/beauty-tools-accessories/trial-travel-size-storage-containers", "id": "cat1870004"},
                    "Bra Alternatives": {"url": "/shop/beauty/beauty-tools-accessories/bra-alternatives", "id": "cat900110"},
                },
            },
            "Fragrance": {
                "url": "/shop/beauty/fragrance",
                "id": "cat3363",
                "subcategories": {
                    "Men's Fragrance": {
                        "url": "/shop/beauty/fragrance/mens-fragrance",
                        "id": "cat3110024",
                        "subcategories": {
                            "Cologne": {"url": "/shop/beauty/fragrance/mens-fragrance/cologne", "id": "cat3377"},
                            "Men's Body Mists & Sprays": {"url": "/shop/beauty/fragrance/mens-fragrance/mens-body-mists-sprays", "id": "cat3110026"},
                        },
                    },
                    "Women's Fragrance": {
                        "url": "/shop/beauty/fragrance/womens-fragrance",
                        "id": "cat3110025",
                        "subcategories": {
                            "Perfume": {"url": "/shop/beauty/fragrance/womens-fragrance/perfume", "id": "cat3378"},
                            "Women's Body Mists & Sprays​": {"url": "/shop/beauty/fragrance/womens-fragrance/womens-body-mists-sprays", "id": "cat3110027"},
                        },
                    },
                },
            },
            "Bath & Body": {
                "url": "/shop/beauty/bath-body",
                "id": "cat900001",
                "subcategories": {
                    "Body Wash & Shower Gel": {"url": "/shop/beauty/bath-body/body-wash-shower-gel", "id": "cat900005"},
                    "Body Lotions & Moisturizers": {"url": "/shop/beauty/bath-body/body-lotions-moisturizers", "id": "cat2270021"},
                    "Bar Soap": {"url": "/shop/beauty/bath-body/bar-soap", "id": "cat2720001"},
                    "Men's Bath & Body Wash": {"url": "/shop/beauty/bath-body/mens-bath-body-wash", "id": "cat1910019"},
                    "Bath Salts & Bubble Bath": {"url": "/shop/beauty/bath-body/bath-salts-bubble-bath", "id": "cat900003"},
                    "Bath & Body Accessories": {"url": "/shop/beauty/bath-body/bath-body-accessories", "id": "cat2450014"},
                    "Foot Cream": {"url": "/shop/beauty/bath-body/foot-cream", "id": "cat2260011"},
                    "Hand Cream": {"url": "/shop/beauty/bath-body/hand-cream", "id": "cat2260012"},
                    "Trial & Travel Size Bath & Body": {"url": "/shop/beauty/bath-body/trial-travel-size-bath-body", "id": "cat1870002"},
                },
            },
            "Trial & Travel Size Beauty": {"url": "/shop/beauty/trial-travel-size-beauty", "id": "cat1830011"},
        },
    },
    "Personal Care": {
        "url": "/shop/personal-care",
        "id": "cat3",
        "subcategories": {
            "Oral Care": {
                "url": "/shop/personal-care/oral-care",
                "id": "cat33",
                "subcategories": {
                    "Toothpaste": {"url": "/shop/personal-care/oral-care/toothpaste", "id": "cat396"},
                    "Toothbrushes": {"url": "/shop/personal-care/oral-care/toothbrushes", "id": "cat397"},
                    "Electric Toothbrushes": {"url": "/shop/personal-care/oral-care/electric-toothbrushes", "id": "cat3471"},
                    "Electric Toothbrush Heads": {"url": "/shop/personal-care/oral-care/electric-toothbrush-heads", "id": "cat2207"},
                    "Mouthwash": {"url": "/shop/personal-care/oral-care/mouthwash", "id": "cat399"},
                    "Teeth Whitening": {"url": "/shop/personal-care/oral-care/teeth-whitening", "id": "cat405"},
                    "Dental Floss": {"url": "/shop/personal-care/oral-care/dental-floss", "id": "cat398"},
                    "Water Flossers": {"url": "/shop/personal-care/oral-care/water-flossers", "id": "cat3110021"},
                    "Breath Fresheners": {"url": "/shop/personal-care/oral-care/breath-fresheners", "id": "cat403"},
                    "Denture Care": {"url": "/shop/personal-care/oral-care/denture-care", "id": "cat402"},
                    "Oral Pain Relief": {"url": "/shop/personal-care/oral-care/oral-pain-relief", "id": "cat404"},
                    "Dental Guards": {"url": "/shop/personal-care/oral-care/dental-guards", "id": "cat3110022"},
                    "Baby & Kids Oral Care": {"url": "/shop/personal-care/oral-care/baby-kids-oral-care", "id": "cat2144"},
                },
            },
            "Deodorant & Antiperspirant": {
                "url": "/shop/personal-care/deodorant-antiperspirant",
                "id": "cat27",
                "subcategories": {
                    "Men's Deodorant & Antiperspirant": {"url": "/shop/personal-care/deodorant-antiperspirant/mens-deodorant-antiperspirant", "id": "cat3455"},
                    "Women's Deodorant & Antiperspirant": {"url": "/shop/personal-care/deodorant-antiperspirant/womens-deodorant-antiperspirant", "id": "cat3456"},
                    "Whole Body Deodorant": {"url": "/shop/personal-care/deodorant-antiperspirant/whole-body-deodorant", "id": "cat3457"},
                },
            },
            "Bath & Body": {
                "url": "/shop/personal-care/bath-body",
                "id": "cat2270001",
                "subcategories": {
                    "Body Wash & Shower Gel": {"url": "/shop/personal-care/bath-body/body-wash-shower-gel", "id": "cat2270004"},
                    "Body Lotions & Moisturizers": {"url": "/shop/personal-care/bath-body/body-lotions-moisturizers", "id": "cat2270026"},
                    "Bath Salts & Bubble Bath": {"url": "/shop/personal-care/bath-body/bath-salts-bubble-bath", "id": "cat2270003"},
                    "Bath & Body Accessories": {"url": "/shop/personal-care/bath-body/bath-body-accessories", "id": "cat2270002"},
                    "Bar Soap": {"url": "/shop/personal-care/bath-body/bar-soap", "id": "cat2720002"},
                    "Men's Bath & Body Wash": {"url": "/shop/personal-care/bath-body/mens-bath-body-wash", "id": "cat2270006"},
                    "Foot Cream": {"url": "/shop/personal-care/bath-body/foot-cream", "id": "cat2270009"},
                    "Hand Cream": {"url": "/shop/personal-care/bath-body/hand-cream", "id": "cat2270008"},
                    "Trial & Travel Size Bath & Body": {"url": "/shop/personal-care/bath-body/trial-travel-size-bath-body", "id": "cat2270007"},
                },
            },
            "Feminine Care": {
                "url": "/shop/personal-care/feminine-care",
                "id": "cat29",
                "subcategories": {
                    "Pads": {"url": "/shop/personal-care/feminine-care/pads", "id": "cat363"},
                    "Panty Liners": {"url": "/shop/personal-care/feminine-care/panty-liners", "id": "cat364"},
                    "Tampons": {"url": "/shop/personal-care/feminine-care/tampons", "id": "cat362"},
                    "Intimate Cleansing": {"url": "/shop/personal-care/feminine-care/intimate-cleansing", "id": "cat366"},
                    "Yeast Infection Treatments": {"url": "/shop/personal-care/feminine-care/yeast-infection-treatments", "id": "cat365"},
                    "Personal Lubricants": {"url": "/shop/personal-care/feminine-care/personal-lubricants", "id": "cat361"},
                    "Menopause Relief": {"url": "/shop/personal-care/feminine-care/menopause-relief", "id": "cat3458"},
                    "Menstrual & Pain Relief": {"url": "/shop/personal-care/feminine-care/menstrual-pain-relief", "id": "cat369"},
                    "Menstrual Cup": {"url": "/shop/personal-care/feminine-care/menstrual-cup", "id": "cat1500001"},
                },
            },
            "Incontinence": {
                "url": "/shop/personal-care/incontinence",
                "id": "cat32",
                "subcategories": {
                    "Men's Incontinence": {
                        "url": "/shop/personal-care/incontinence/mens-incontinence",
                        "id": "cat3110020",
                        "subcategories": {
                            "Guards & Shields": {"url": "/shop/personal-care/incontinence/mens-incontinence/guards-shields", "id": "cat1630002"},
                            "Men's Incontinence Underwear": {"url": "/shop/personal-care/incontinence/mens-incontinence/mens-incontinence-underwear", "id": "cat1630003"},
                        },
                    },
                    "Women's Incontinence": {
                        "url": "/shop/personal-care/incontinence/womens-incontinence",
                        "id": "cat3110019",
                        "subcategories": {
                            "Incontinence Pads": {"url": "/shop/personal-care/incontinence/womens-incontinence/incontinence-pads", "id": "cat3466"},
                            "Women's Incontinence Underwear": {"url": "/shop/personal-care/incontinence/womens-incontinence/womens-incontinence-underwear", "id": "cat395"},
                        },
                    },
                    "Bedding Protection": {"url": "/shop/personal-care/incontinence/bedding-protection", "id": "cat3465"},
                    "Skin Care & Medication": {"url": "/shop/personal-care/incontinence/skin-care-medication", "id": "cat1630005"},
                },
            },
            "Hair Removal & Shave": {
                "url": "/shop/personal-care/hair-removal-shave",
                "id": "cat34",
                "subcategories": {
                    "Razors & Blades": {
                        "url": "/shop/personal-care/hair-removal-shave/razors-blades",
                        "id": "cat3110015",
                        "subcategories": {
                            "Men's Razors & Blades": {"url": "/shop/personal-care/hair-removal-shave/razors-blades/mens-razors-blades", "id": "cat408"},
                            "Women's Razors & Blades": {"url": "/shop/personal-care/hair-removal-shave/razors-blades/womens-razors-blades", "id": "cat2118"},
                        },
                    },
                    "Disposable Razors": {
                        "url": "/shop/personal-care/hair-removal-shave/disposable-razors",
                        "id": "cat3110017",
                        "subcategories": {
                            "Men's Disposable Razors": {"url": "/shop/personal-care/hair-removal-shave/disposable-razors/mens-disposable-razors", "id": "cat2113"},
                            "Women's Disposable Razors": {"url": "/shop/personal-care/hair-removal-shave/disposable-razors/womens-disposable-razors", "id": "cat2120"},
                        },
                    },
                    "Shaving Creams & Gels": {
                        "url": "/shop/personal-care/hair-removal-shave/shaving-creams-gels",
                        "id": "cat3110018",
                        "subcategories": {
                            "Men's Shaving Creams & Gels": {"url": "/shop/personal-care/hair-removal-shave/shaving-creams-gels/mens-shaving-creams-gels", "id": "cat406"},
                            "Women's Shaving Creams & Gels": {"url": "/shop/personal-care/hair-removal-shave/shaving-creams-gels/womens-shaving-creams-gels", "id": "cat407"},
                        },
                    },
                    "Electric Shavers": {"url": "/shop/personal-care/hair-removal-shave/electric-shavers", "id": "cat2112"},
                    "After Shave Care": {"url": "/shop/personal-care/hair-removal-shave/after-shave-care", "id": "cat2111"},
                    "Waxing & Hair Removal Treatments": {"url": "/shop/personal-care/hair-removal-shave/waxing-hair-removal-treatments", "id": "cat2574"},
                    "Groomers & Trimmers": {"url": "/shop/personal-care/hair-removal-shave/groomers-trimmers", "id": "cat2981"},
                },
            },
            "Men's Grooming": {
                "url": "/shop/personal-care/mens-grooming",
                "id": "cat130001",
                "subcategories": {
                    "Beard Care": {"url": "/shop/personal-care/mens-grooming/beard-care", "id": "cat1540012"},
                    "Men's Bath & Body Wash": {"url": "/shop/personal-care/mens-grooming/mens-bath-body-wash", "id": "cat2260003"},
                    "Men's Skin Care": {
                        "url": "/shop/personal-care/mens-grooming/mens-skin-care",
                        "id": "cat2260005",
                        "subcategories": {
                            "Men's Creams & Lotions": {"url": "/shop/personal-care/mens-grooming/mens-skin-care/mens-creams-lotions", "id": "cat2260006"},
                            "Men's Face Wash": {"url": "/shop/personal-care/mens-grooming/mens-skin-care/mens-face-wash", "id": "cat2260007"},
                        },
                    },
                    "Men's Hair Care": {"url": "/shop/personal-care/mens-grooming/mens-hair-care", "id": "cat2260004"},
                    "Men's Fragrance​": {
                        "url": "/shop/personal-care/mens-grooming/mens-fragrance",
                        "id": "cat2260002",
                        "subcategories": {
                            "Cologne": {"url": "/shop/personal-care/mens-grooming/mens-fragrance/cologne", "id": "cat3110028"},
                            "Men's Body Mists & Sprays​": {"url": "/shop/personal-care/mens-grooming/mens-fragrance/mens-body-mists-sprays", "id": "cat3110029"},
                        },
                    },
                },
            },
            "Eye Care": {
                "url": "/shop/personal-care/eye-care",
                "id": "cat3701",
                "subcategories": {
                    "Drops & Lubricants": {"url": "/shop/personal-care/eye-care/drops-lubricants", "id": "cat345"},
                    "Contact Lens Solution": {"url": "/shop/personal-care/eye-care/contact-lens-solution", "id": "cat348"},
                    "Eye Wash & Solutions": {"url": "/shop/personal-care/eye-care/eye-wash-solutions", "id": "cat346"},
                    "Reading Glasses": {"url": "/shop/personal-care/eye-care/reading-glasses", "id": "cat347"},
                    "Eyeglass Cleaners & Kits": {"url": "/shop/personal-care/eye-care/eyeglass-cleaners-kits", "id": "cat3070003"},
                    "Sunglasses": {"url": "/shop/personal-care/eye-care/sunglasses", "id": "cat220467483"},
                },
            },
            "Foot Care": {
                "url": "/shop/personal-care/foot-care",
                "id": "cat30",
                "subcategories": {
                    "Shoe Inserts & Insoles": {"url": "/shop/personal-care/foot-care/shoe-inserts-insoles", "id": "cat3461"},
                    "Antifungal & Athlete's Foot": {"url": "/shop/personal-care/foot-care/antifungal-athletes-foot", "id": "cat372"},
                    "Corn, Callus, Blister & Bunion": {"url": "/shop/personal-care/foot-care/corn-callus-blister-bunion", "id": "cat373"},
                    "Foot Cream": {"url": "/shop/personal-care/foot-care/foot-cream", "id": "cat377"},
                    "Wart Removal": {"url": "/shop/personal-care/foot-care/wart-removal", "id": "cat2110"},
                    "Foot Odor Control": {"url": "/shop/personal-care/foot-care/foot-odor-control", "id": "cat371"},
                    "Foot Spa": {"url": "/shop/personal-care/foot-care/foot-spa", "id": "cat3459"},
                },
            },
            "Ear Care": {
                "url": "/shop/personal-care/ear-care",
                "id": "cat13",
                "subcategories": {
                    "Wax Removal": {"url": "/shop/personal-care/ear-care/wax-removal", "id": "cat343"},
                    "Cotton Balls & Swabs": {"url": "/shop/personal-care/ear-care/cotton-balls-swabs", "id": "cat2260001"},
                    "Ear Drops": {"url": "/shop/personal-care/ear-care/ear-drops", "id": "cat341"},
                    "Ear Plugs": {"url": "/shop/personal-care/ear-care/ear-plugs", "id": "cat342"},
                },
            },
            "Massage & Relaxation": {
                "url": "/shop/personal-care/massage-relaxation",
                "id": "cat270002",
                "subcategories": {
                    "Massagers": {"url": "/shop/personal-care/massage-relaxation/massagers", "id": "cat270004"},
                    "Massage Oil & Lotion": {"url": "/shop/personal-care/massage-relaxation/massage-oil-lotion", "id": "cat270006"},
                    "Aromatherapy & Essential Oils": {
                        "url": "/shop/personal-care/massage-relaxation/aromatherapy-essential-oils",
                        "id": "cat1220001",
                        "subcategories": {
                            "Diffusers": {"url": "/shop/personal-care/massage-relaxation/aromatherapy-essential-oils/diffusers", "id": "cat1590001"},
                            "Essential Oils": {"url": "/shop/personal-care/massage-relaxation/aromatherapy-essential-oils/essential-oils", "id": "cat1220002"},
                        },
                    },
                },
            },
            "Hand Sanitizer & Soap": {
                "url": "/shop/personal-care/hand-sanitizer-soap",
                "id": "cat2260009",
                "subcategories": {
                    "Hand Soap": {"url": "/shop/personal-care/hand-sanitizer-soap/hand-soap", "id": "cat900009"},
                    "Bar Soap": {"url": "/shop/personal-care/hand-sanitizer-soap/bar-soap", "id": "cat2720003"},
                    "Hand Sanitizer": {"url": "/shop/personal-care/hand-sanitizer-soap/hand-sanitizer", "id": "cat900007"},
                },
            },
            "Cotton Balls & Swabs": {"url": "/shop/personal-care/cotton-balls-swabs", "id": "cat2489"},
            "Sun & Tanning": {
                "url": "/shop/personal-care/sun-tanning",
                "id": "cat2270011",
                "subcategories": {
                    "Sunscreen": {"url": "/shop/personal-care/sun-tanning/sunscreen", "id": "cat2270017"},
                    "After-Sun Care": {"url": "/shop/personal-care/sun-tanning/after-sun-care", "id": "cat2270012"},
                    "Self Tanner": {"url": "/shop/personal-care/sun-tanning/self-tanner", "id": "cat2270016"},
                },
            },
            "Lip Balm & Treatments": {"url": "/shop/personal-care/lip-balm-treatments", "id": "cat2260008"},
            "CBD": {"url": "/shop/personal-care/cbd", "id": "cat1750001"},
            "Trial & Travel Size Personal Care": {"url": "/shop/personal-care/trial-travel-size-personal-care", "id": "cat1870006"},
        },
    },
    "Vitamins": {
        "url": "/shop/vitamins",
        "id": "cat2",
        "subcategories": {
            "Multivitamins": {
                "url": "/shop/vitamins/multivitamins",
                "id": "cat320022",
                "subcategories": {
                    "Multivitamins for Adults 50+": {"url": "/shop/vitamins/multivitamins/multivitamins-for-adults-50", "id": "cat320030"},
                    "Multivitamins for Women": {"url": "/shop/vitamins/multivitamins/multivitamins-for-women", "id": "cat320026"},
                    "Multivitamins for Men": {"url": "/shop/vitamins/multivitamins/multivitamins-for-men", "id": "cat320024"},
                    "Multivitamins for Kids": {"url": "/shop/vitamins/multivitamins/multivitamins-for-kids", "id": "cat320028"},
                    "Prenatal Multivitamins": {"url": "/shop/vitamins/multivitamins/prenatal-multivitamins", "id": "cat3070015"},
                },
            },
            "Letter Vitamins": {
                "url": "/shop/vitamins/letter-vitamins",
                "id": "cat3488",
                "subcategories": {
                    "Vitamin A": {"url": "/shop/vitamins/letter-vitamins/vitamin-a", "id": "cat310002"},
                    "Vitamin B": {"url": "/shop/vitamins/letter-vitamins/vitamin-b", "id": "cat310004"},
                    "Vitamin C": {"url": "/shop/vitamins/letter-vitamins/vitamin-c", "id": "cat310006"},
                    "Vitamin D": {"url": "/shop/vitamins/letter-vitamins/vitamin-d", "id": "cat310008"},
                    "Vitamin E": {"url": "/shop/vitamins/letter-vitamins/vitamin-e", "id": "cat310010"},
                    "Vitamin K": {"url": "/shop/vitamins/letter-vitamins/vitamin-k", "id": "cat880001"},
                },
            },
            "Fish Oil & Omegas": {
                "url": "/shop/vitamins/fish-oil-omegas",
                "id": "cat3100018",
                "subcategories": {
                    "Fish Oil": {"url": "/shop/vitamins/fish-oil-omegas/fish-oil", "id": "cat320016"},
                    "Omegas": {"url": "/shop/vitamins/fish-oil-omegas/omegas", "id": "cat3100022"},
                    "Flaxseed Oil": {"url": "/shop/vitamins/fish-oil-omegas/flaxseed-oil", "id": "cat320020"},
                },
            },
            "Supplements": {
                "url": "/shop/vitamins/supplements",
                "id": "cat320010",
                "subcategories": {
                    "Prebiotics & Probiotics": {"url": "/shop/vitamins/supplements/prebiotics-probiotics", "id": "cat1680017"},
                    "CoQ10": {"url": "/shop/vitamins/supplements/coq10", "id": "cat320014"},
                    "Brain and Memory Support": {"url": "/shop/vitamins/supplements/brain-and-memory-support", "id": "cat1760001"},
                    "Glucosamine": {"url": "/shop/vitamins/supplements/glucosamine", "id": "cat630026"},
                    "Biotin": {"url": "/shop/vitamins/supplements/biotin", "id": "cat1920024"},
                    "Melatonin": {"url": "/shop/vitamins/supplements/melatonin", "id": "cat630028"},
                    "Collagen": {"url": "/shop/vitamins/supplements/collagen", "id": "cat1920020"},
                    "Lutein": {"url": "/shop/vitamins/supplements/lutein", "id": "cat1590005"},
                    "Urinary Tract Health": {"url": "/shop/vitamins/supplements/urinary-tract-health", "id": "cat3100017"},
                    "Apple Cider Vinegar": {"url": "/shop/vitamins/supplements/apple-cider-vinegar", "id": "cat3070009"},
                },
            },
            "Minerals": {
                "url": "/shop/vitamins/minerals",
                "id": "cat25",
                "subcategories": {
                    "Magnesium": {"url": "/shop/vitamins/minerals/magnesium", "id": "cat248"},
                    "Calcium": {"url": "/shop/vitamins/minerals/calcium", "id": "cat244"},
                    "Iron": {"url": "/shop/vitamins/minerals/iron", "id": "cat247"},
                    "Zinc": {"url": "/shop/vitamins/minerals/zinc", "id": "cat251"},
                    "Potassium": {"url": "/shop/vitamins/minerals/potassium", "id": "cat249"},
                },
            },
            "Herbals": {
                "url": "/shop/vitamins/herbals",
                "id": "cat26",
                "subcategories": {
                    "Ashwagandha": {"url": "/shop/vitamins/herbals/ashwagandha", "id": "cat3070014"},
                    "Turmeric": {"url": "/shop/vitamins/herbals/turmeric", "id": "cat1590002"},
                    "Cinnamon": {"url": "/shop/vitamins/herbals/cinnamon", "id": "cat630006"},
                    "Milk Thistle": {"url": "/shop/vitamins/herbals/milk-thistle", "id": "cat630018"},
                    "Cranberry": {"url": "/shop/vitamins/herbals/cranberry", "id": "cat630008"},
                    "Herbal Teas": {"url": "/shop/vitamins/herbals/herbal-teas", "id": "cat3070013"},
                    "Elderberry": {"url": "/shop/vitamins/herbals/elderberry", "id": "cat3070012"},
                    "Gingko Biloba": {"url": "/shop/vitamins/herbals/gingko-biloba", "id": "cat630014"},
                    "Garlic": {"url": "/shop/vitamins/herbals/garlic", "id": "cat630012"},
                },
            },
            "Superfoods": {"url": "/shop/vitamins/superfoods", "id": "cat3070011"},
        },
    },
    "Grocery": {
        "url": "/shop/grocery",
        "id": "cat2000008",
        "subcategories": {
            "Candy, Gum & Mints": {
                "url": "/shop/grocery/candy-gum-mints",
                "id": "cat2000013",
                "subcategories": {
                    "Chocolates": {"url": "/shop/grocery/candy-gum-mints/chocolates", "id": "cat240011"},
                    "Chewy & Gummy Candy": {"url": "/shop/grocery/candy-gum-mints/chewy-gummy-candy", "id": "cat2290001"},
                    "Gum & Mints": {"url": "/shop/grocery/candy-gum-mints/gum-mints", "id": "cat240013"},
                    "Hard Candy": {"url": "/shop/grocery/candy-gum-mints/hard-candy", "id": "cat2290002"},
                    "Sugar Free Candy": {"url": "/shop/grocery/candy-gum-mints/sugar-free-candy", "id": "cat2010003"},
                },
            },
            "Snacks": {
                "url": "/shop/grocery/snacks",
                "id": "cat2000015",
                "subcategories": {
                    "Nuts": {"url": "/shop/grocery/snacks/nuts", "id": "cat2010009"},
                    "Snack & Trail Mix": {"url": "/shop/grocery/snacks/snack-trail-mix", "id": "cat3080002"},
                    "Chips & Pretzels": {"url": "/shop/grocery/snacks/chips-pretzels", "id": "cat2010006"},
                    "Popcorn": {"url": "/shop/grocery/snacks/popcorn", "id": "cat2010011"},
                    "Cookies": {"url": "/shop/grocery/snacks/cookies", "id": "cat3559"},
                    "Crackers": {"url": "/shop/grocery/snacks/crackers", "id": "cat3284"},
                    "Healthy Snacks": {"url": "/shop/grocery/snacks/healthy-snacks", "id": "cat3070036"},
                    "Granola & Snack Bars": {"url": "/shop/grocery/snacks/granola-snack-bars", "id": "cat2010013"},
                    "Fruit Snacks": {"url": "/shop/grocery/snacks/fruit-snacks", "id": "cat2010007"},
                    "Jerky & Meat Snacks": {"url": "/shop/grocery/snacks/jerky-meat-snacks", "id": "cat2010008"},
                },
            },
            "Cereal & Breakfast": {
                "url": "/shop/grocery/cereal-breakfast",
                "id": "cat3014",
                "subcategories": {
                    "Cereal": {"url": "/shop/grocery/cereal-breakfast/cereal", "id": "cat3070033"},
                    "Oatmeal & Granola": {"url": "/shop/grocery/cereal-breakfast/oatmeal-granola", "id": "cat3070034"},
                    "Pancakes & Waffles": {"url": "/shop/grocery/cereal-breakfast/pancakes-waffles", "id": "cat3070035"},
                },
            },
            "Beverages": {
                "url": "/shop/grocery/beverages",
                "id": "cat950001",
                "subcategories": {
                    "Coffee": {
                        "url": "/shop/grocery/beverages/coffee",
                        "id": "cat3013",
                        "subcategories": {
                            "Ground Coffee": {"url": "/shop/grocery/beverages/coffee/ground-coffee", "id": "cat3110009"},
                            "Coffee Pods": {"url": "/shop/grocery/beverages/coffee/coffee-pods", "id": "cat3110008"},
                            "Instant Coffee": {"url": "/shop/grocery/beverages/coffee/instant-coffee", "id": "cat3110011"},
                            "Bottled Coffee": {"url": "/shop/grocery/beverages/coffee/bottled-coffee", "id": "cat3110010"},
                            "Coffee Creamers": {"url": "/shop/grocery/beverages/coffee/coffee-creamers", "id": "cat3110013"},
                        },
                    },
                    "Soda": {"url": "/shop/grocery/beverages/soda", "id": "cat1270012"},
                    "Water": {"url": "/shop/grocery/beverages/water", "id": "cat1230001"},
                    "Juices": {"url": "/shop/grocery/beverages/juices", "id": "cat950002"},
                    "Sport & Energy Drinks": {"url": "/shop/grocery/beverages/sport-energy-drinks", "id": "cat2010002"},
                    "Tea": {"url": "/shop/grocery/beverages/tea", "id": "cat3110007"},
                    "Milk & Creamers": {"url": "/shop/grocery/beverages/milk-creamers", "id": "cat2010001"},
                    "Non-Alcoholic Drinks": {"url": "/shop/grocery/beverages/non-alcoholic-drinks", "id": "cat3110023"},
                },
            },
            "Pantry": {
                "url": "/shop/grocery/pantry",
                "id": "cat2000014",
                "subcategories": {
                    "Canned & Packaged Food": {"url": "/shop/grocery/pantry/canned-packaged-food", "id": "cat2010005"},
                    "Baking Supplies": {"url": "/shop/grocery/pantry/baking-supplies", "id": "cat3036"},
                    "Condiments & Spreads": {"url": "/shop/grocery/pantry/condiments-spreads", "id": "cat3034"},
                    "Spices & Seasonings": {"url": "/shop/grocery/pantry/spices-seasonings", "id": "cat3295"},
                    "Sugar & Sweeteners": {"url": "/shop/grocery/pantry/sugar-sweeteners", "id": "cat2810"},
                },
            },
            "Frozen Food": {"url": "/shop/grocery/frozen-food", "id": "cat1280001"},
        },
    },
    "Household": {
        "url": "/shop/household",
        "id": "cat2000007",
        "subcategories": {
            "Laundry Supplies": {
                "url": "/shop/household/laundry-supplies",
                "id": "cat3250",
                "subcategories": {
                    "Laundry Detergents": {"url": "/shop/household/laundry-supplies/laundry-detergents", "id": "cat2010035"},
                    "Scent Boosters": {"url": "/shop/household/laundry-supplies/scent-boosters", "id": "cat1920031"},
                    "Fabric Softeners": {"url": "/shop/household/laundry-supplies/fabric-softeners", "id": "cat3303"},
                    "Dryer Sheets": {"url": "/shop/household/laundry-supplies/dryer-sheets", "id": "cat1920032"},
                    "Stain Removers": {"url": "/shop/household/laundry-supplies/stain-removers", "id": "cat3306"},
                    "Laundry Accessories": {"url": "/shop/household/laundry-supplies/laundry-accessories", "id": "cat380003"},
                },
            },
            "Paper & Plastic": {
                "url": "/shop/household/paper-plastic",
                "id": "cat2000012",
                "subcategories": {
                    "Toilet Paper": {"url": "/shop/household/paper-plastic/toilet-paper", "id": "cat2010039"},
                    "Paper Towels": {"url": "/shop/household/paper-plastic/paper-towels", "id": "cat2070035"},
                    "Facial Tissue": {"url": "/shop/household/paper-plastic/facial-tissue", "id": "cat2818"},
                    "Disposable Tableware": {"url": "/shop/household/paper-plastic/disposable-tableware", "id": "cat2010036"},
                    "Trash Bags": {"url": "/shop/household/paper-plastic/trash-bags", "id": "cat3263"},
                    "Storage Bags": {"url": "/shop/household/paper-plastic/storage-bags", "id": "cat3261"},
                    "Plastic Wrap & Foil": {"url": "/shop/household/paper-plastic/plastic-wrap-foil", "id": "cat2010038"},
                    "Food Storage Containers": {"url": "/shop/household/paper-plastic/food-storage-containers", "id": "cat2010037"},
                },
            },
            "Cleaning Supplies": {
                "url": "/shop/household/cleaning-supplies",
                "id": "cat2784",
                "subcategories": {
                    "All Purpose Cleaners": {"url": "/shop/household/cleaning-supplies/all-purpose-cleaners", "id": "cat3270"},
                    "Dish Detergents": {"url": "/shop/household/cleaning-supplies/dish-detergents", "id": "cat2010024"},
                    "Air Fresheners": {"url": "/shop/household/cleaning-supplies/air-fresheners", "id": "cat3017"},
                    "Floor & Carpet Cleaners": {"url": "/shop/household/cleaning-supplies/floor-carpet-cleaners", "id": "cat2010025"},
                    "Cleaning Tools": {"url": "/shop/household/cleaning-supplies/cleaning-tools", "id": "cat950013"},
                    "Glass Cleaners": {"url": "/shop/household/cleaning-supplies/glass-cleaners", "id": "cat2010027"},
                    "Bathroom Cleaners": {"url": "/shop/household/cleaning-supplies/bathroom-cleaners", "id": "cat3088"},
                    "Kitchen Cleaners": {"url": "/shop/household/cleaning-supplies/kitchen-cleaners", "id": "cat3070016"},
                    "Drain Cleaners": {"url": "/shop/household/cleaning-supplies/drain-cleaners", "id": "cat2010026"},
                },
            },
            "School & Office Supplies": {
                "url": "/shop/household/school-office-supplies",
                "id": "cat3192",
                "subcategories": {
                    "Notebooks & Planners": {"url": "/shop/household/school-office-supplies/notebooks-planners", "id": "cat2010043"},
                    "Pens & Pencils": {"url": "/shop/household/school-office-supplies/pens-pencils", "id": "cat3194"},
                    "Binders & Folders": {"url": "/shop/household/school-office-supplies/binders-folders", "id": "cat3196"},
                    "Printer Ink & Paper": {"url": "/shop/household/school-office-supplies/printer-ink-paper", "id": "cat3070017"},
                    "Mailing & Packing Supplies": {"url": "/shop/household/school-office-supplies/mailing-packing-supplies", "id": "cat3317"},
                    "Desk Supplies": {"url": "/shop/household/school-office-supplies/desk-supplies", "id": "cat3200"},
                    "Arts & Crafts": {"url": "/shop/household/school-office-supplies/arts-crafts", "id": "cat3330"},
                    "Markers & Highlighters": {"url": "/shop/household/school-office-supplies/markers-highlighters", "id": "cat3336"},
                    "Tape & Glue": {"url": "/shop/household/school-office-supplies/tape-glue", "id": "cat2010042"},
                    "Calculators": {"url": "/shop/household/school-office-supplies/calculators", "id": "cat3197"},
                },
            },
            "Batteries & Electronics": {
                "url": "/shop/household/batteries-electronics",
                "id": "cat2000009",
                "subcategories": {
                    "Batteries": {"url": "/shop/household/batteries-electronics/batteries", "id": "cat3100014"},
                    "Chargers & Phone Accessories": {"url": "/shop/household/batteries-electronics/chargers-phone-accessories", "id": "cat3100016"},
                    "Computer Accessories": {"url": "/shop/household/batteries-electronics/computer-accessories", "id": "cat3100019"},
                    "Headphones": {"url": "/shop/household/batteries-electronics/headphones", "id": "cat3100020"},
                    "Portable Speakers": {"url": "/shop/household/batteries-electronics/portable-speakers", "id": "cat3100021"},
                },
            },
            "Pet Supplies": {
                "url": "/shop/household/pet-supplies",
                "id": "cat2789",
                "subcategories": {
                    "Dog Food & Treats": {"url": "/shop/household/pet-supplies/dog-food-treats", "id": "cat3324"},
                    "Cat Food & Treats": {"url": "/shop/household/pet-supplies/cat-food-treats", "id": "cat3320"},
                    "Pet Grooming & Accessories": {"url": "/shop/household/pet-supplies/pet-grooming-accessories", "id": "cat2010040"},
                    "Pet Toys": {"url": "/shop/household/pet-supplies/pet-toys", "id": "cat2010041"},
                    "Pet Flea & Tick Treatment": {"url": "/shop/household/pet-supplies/pet-flea-tick-treatment", "id": "cat3070023"},
                    "Pet Healthcare": {"url": "/shop/household/pet-supplies/pet-healthcare", "id": "cat3070022"},
                    "Small Pet Supplies": {"url": "/shop/household/pet-supplies/small-pet-supplies", "id": "cat420001"},
                },
            },
            "Home & Kitchen": {
                "url": "/shop/household/home-kitchen",
                "id": "cat2000011",
                "subcategories": {
                    "Small Appliances": {"url": "/shop/household/home-kitchen/small-appliances", "id": "cat3204"},
                    "Kitchen Accessories": {"url": "/shop/household/home-kitchen/kitchen-accessories", "id": "cat2010034"},
                    "Drinkware": {"url": "/shop/household/home-kitchen/drinkware", "id": "cat229338189"},
                    "Picture Frames": {"url": "/shop/household/home-kitchen/picture-frames", "id": "cat120004"},
                    "Candles": {"url": "/shop/household/home-kitchen/candles", "id": "cat3219"},
                    "Lighting": {"url": "/shop/household/home-kitchen/lighting", "id": "cat190003"},
                },
            },
            "Toys & Books": {
                "url": "/shop/household/toys-books",
                "id": "cat3350",
                "subcategories": {
                    "Toys": {"url": "/shop/household/toys-books/toys", "id": "cat3070020"},
                    "Games & Puzzles": {"url": "/shop/household/toys-books/games-puzzles", "id": "cat3070019"},
                    "Activity Books": {"url": "/shop/household/toys-books/activity-books", "id": "cat3070018"},
                },
            },
            "Clothing & Accessories": {
                "url": "/shop/household/clothing-accessories",
                "id": "cat2000010",
                "subcategories": {
                    "Women's Hosiery": {"url": "/shop/household/clothing-accessories/womens-hosiery", "id": "cat3356"},
                    "Women's Socks & Underwear": {"url": "/shop/household/clothing-accessories/womens-socks-underwear", "id": "cat2010029"},
                    "Men's Undergarments": {"url": "/shop/household/clothing-accessories/mens-undergarments", "id": "cat2010028"},
                    "Rain & Umbrellas": {"url": "/shop/household/clothing-accessories/rain-umbrellas", "id": "cat3252"},
                    "Shoe Care": {"url": "/shop/household/clothing-accessories/shoe-care", "id": "cat3229"},
                    "Sewing Supplies": {"url": "/shop/household/clothing-accessories/sewing-supplies", "id": "cat2770003"},
                    "Jewelry": {"url": "/shop/household/clothing-accessories/jewelry", "id": "cat2770002"},
                },
            },
            "Insect & Pest Control": {"url": "/shop/household/insect-pest-control", "id": "cat950009"},
            "Hardware": {
                "url": "/shop/household/hardware",
                "id": "cat3234",
                "subcategories": {
                    "Tool Box Supplies": {"url": "/shop/household/hardware/tool-box-supplies", "id": "cat2010033"},
                    "Electrical Supplies": {"url": "/shop/household/hardware/electrical-supplies", "id": "cat2010031"},
                    "Adhesives": {"url": "/shop/household/hardware/adhesives", "id": "cat2010030"},
                    "Security & Locks": {"url": "/shop/household/hardware/security-locks", "id": "cat2010032"},
                },
            },
            "Automotive": {"url": "/shop/household/automotive", "id": "cat3240"},
        },
    },
    "Sexual Wellness": {
        "url": "/shop/sexual-wellness",
        "id": "cat2609",
        "subcategories": {
            "Sexual Enhancers": {"url": "/shop/sexual-wellness/sexual-enhancers", "id": "cat550210"},
            "Vibrators & Adult Toys": {
                "url": "/shop/sexual-wellness/vibrators-adult-toys",
                "id": "cat550196",
                "subcategories": {
                    "Vibrators": {"url": "/shop/sexual-wellness/vibrators-adult-toys/vibrators", "id": "cat550208"},
                    "Vibrating Rings": {"url": "/shop/sexual-wellness/vibrators-adult-toys/vibrating-rings", "id": "cat550204"},
                    "Kegel": {"url": "/shop/sexual-wellness/vibrators-adult-toys/kegel", "id": "cat550200"},
                    "Cleaners & Accessories": {"url": "/shop/sexual-wellness/vibrators-adult-toys/cleaners-accessories", "id": "cat550198"},
                },
            },
            "Condoms & Contraceptives": {
                "url": "/shop/sexual-wellness/condoms-contraceptives",
                "id": "cat2610",
                "subcategories": {
                    "Condoms": {"url": "/shop/sexual-wellness/condoms-contraceptives/condoms", "id": "cat550192"},
                    "Emergency Contraceptives": {"url": "/shop/sexual-wellness/condoms-contraceptives/emergency-contraceptives", "id": "cat1580002"},
                    "Female Contraceptives": {"url": "/shop/sexual-wellness/condoms-contraceptives/female-contraceptives", "id": "cat550194"},
                    "Latex-free Condoms": {"url": "/shop/sexual-wellness/condoms-contraceptives/latex-free-condoms", "id": "cat1580001"},
                },
            },
            "Lube": {
                "url": "/shop/sexual-wellness/lube",
                "id": "cat550234",
                "subcategories": {
                    "Water Based": {"url": "/shop/sexual-wellness/lube/water-based", "id": "cat550244"},
                    "Natural Lubricants": {"url": "/shop/sexual-wellness/lube/natural-lubricants", "id": "cat1570004"},
                    "Silicone-Based": {"url": "/shop/sexual-wellness/lube/silicone-based", "id": "cat550240"},
                    "Desensitizers": {"url": "/shop/sexual-wellness/lube/desensitizers", "id": "cat1570003"},
                },
            },
            "Family Planning": {
                "url": "/shop/sexual-wellness/family-planning",
                "id": "cat550222",
                "subcategories": {
                    "Pregnancy & Fertility Tests": {"url": "/shop/sexual-wellness/family-planning/pregnancy-fertility-tests", "id": "cat550226"},
                    "Men's Fertility": {"url": "/shop/sexual-wellness/family-planning/mens-fertility", "id": "cat3070005"},
                    "Parental & Gender Tests": {"url": "/shop/sexual-wellness/family-planning/parental-gender-tests", "id": "cat550230"},
                    "Prenatal Supplements": {"url": "/shop/sexual-wellness/family-planning/prenatal-supplements", "id": "cat550232"},
                },
            },
            "Trial & Travel Size Personal Intimacy": {"url": "/shop/sexual-wellness/trial-travel-size-personal-intimacy", "id": "cat2760001"},
            "Erectile Dysfunction Treatment": {"url": "/shop/sexual-wellness/erectile-dysfunction-treatment", "id": "cat2611"},
        },
    },
    "Home Health Care": {
        "url": "/shop/home-health-care",
        "id": "cat2227",
        "subcategories": {
            "Home Tests": {
                "url": "/shop/home-health-care/home-tests",
                "id": "cat550010",
                "subcategories": {
                    "At-Home COVID-19 Tests": {"url": "/shop/home-health-care/home-tests/at-home-covid-19-tests", "id": "cat2310002"},
                    "STD & HIV Tests": {"url": "/shop/home-health-care/home-tests/std-hiv-tests", "id": "cat1680007"},
                    "Alcohol & Drug Tests": {"url": "/shop/home-health-care/home-tests/alcohol-drug-tests", "id": "cat550112"},
                    "Cholesterol & Dietary Tests": {"url": "/shop/home-health-care/home-tests/cholesterol-dietary-tests", "id": "cat550122"},
                    "Fertility & Pregnancy Tests": {"url": "/shop/home-health-care/home-tests/fertility-pregnancy-tests", "id": "cat550126"},
                    "Parental, DNA & Gender Tests": {"url": "/shop/home-health-care/home-tests/parental-dna-gender-tests", "id": "cat550130"},
                },
            },
            "Monitors": {
                "url": "/shop/home-health-care/monitors",
                "id": "cat550006",
                "subcategories": {
                    "Blood Pressure Monitors": {"url": "/shop/home-health-care/monitors/blood-pressure-monitors", "id": "cat550050"},
                    "Pulse Oximeters": {"url": "/shop/home-health-care/monitors/pulse-oximeters", "id": "cat550098"},
                    "Thermometers": {"url": "/shop/home-health-care/monitors/thermometers", "id": "cat550138"},
                    "Diabetic Monitors": {"url": "/shop/home-health-care/monitors/diabetic-monitors", "id": "cat550076"},
                    "Heart Rate Monitors & Stethoscopes": {"url": "/shop/home-health-care/monitors/heart-rate-monitors-stethoscopes", "id": "cat550068"},
                    "Fitness Trackers & Scales": {"url": "/shop/home-health-care/monitors/fitness-trackers-scales", "id": "cat550102"},
                },
            },
            "Daily Living Aids": {
                "url": "/shop/home-health-care/daily-living-aids",
                "id": "cat550024",
                "subcategories": {
                    "Respiratory Therapy": {"url": "/shop/home-health-care/daily-living-aids/respiratory-therapy", "id": "cat550108"},
                    "Medicine Accessories": {"url": "/shop/home-health-care/daily-living-aids/medicine-accessories", "id": "cat550104"},
                    "Cushions, Pillows & Neck Supports": {"url": "/shop/home-health-care/daily-living-aids/cushions-pillows-neck-supports", "id": "cat550088"},
                    "Bath & Body Products": {"url": "/shop/home-health-care/daily-living-aids/bath-body-products", "id": "cat550078"},
                    "Reachers": {"url": "/shop/home-health-care/daily-living-aids/reachers", "id": "cat550092"},
                    "Beds & Accessories": {"url": "/shop/home-health-care/daily-living-aids/beds-accessories", "id": "cat550086"},
                    "Patient Room Accessories": {"url": "/shop/home-health-care/daily-living-aids/patient-room-accessories", "id": "cat1430010"},
                    "Seating & Tables": {"url": "/shop/home-health-care/daily-living-aids/seating-tables", "id": "cat1430007"},
                    "Light Therapy": {"url": "/shop/home-health-care/daily-living-aids/light-therapy", "id": "cat550100"},
                    "Electrotherapy": {"url": "/shop/home-health-care/daily-living-aids/electrotherapy", "id": "cat550090"},
                    "Medical Totes & Bags": {"url": "/shop/home-health-care/daily-living-aids/medical-totes-bags", "id": "cat550110"},
                    "Sensory Aids": {"url": "/shop/home-health-care/daily-living-aids/sensory-aids", "id": "cat1430009"},
                    "Adaptive Eating Utensils": {"url": "/shop/home-health-care/daily-living-aids/adaptive-eating-utensils", "id": "cat1440001"},
                },
            },
            "Diabetes Care": {
                "url": "/shop/home-health-care/diabetes-care",
                "id": "cat550014",
                "subcategories": {
                    "Diabetic Monitors": {"url": "/shop/home-health-care/diabetes-care/diabetic-monitors", "id": "cat550180"},
                    "Diabetic Blood Test Strips": {"url": "/shop/home-health-care/diabetes-care/diabetic-blood-test-strips", "id": "cat550176"},
                    "Lancets & Accessories": {"url": "/shop/home-health-care/diabetes-care/lancets-accessories", "id": "cat550184"},
                    "Nutrition & Food": {"url": "/shop/home-health-care/diabetes-care/nutrition-food", "id": "cat550186"},
                    "Diabetic Skin Care": {"url": "/shop/home-health-care/diabetes-care/diabetic-skin-care", "id": "cat550188"},
                    "Glucose Tablets": {"url": "/shop/home-health-care/diabetes-care/glucose-tablets", "id": "cat1680010"},
                    "Sugar Free Medicines & Supplements": {"url": "/shop/home-health-care/diabetes-care/sugar-free-medicines-supplements", "id": "cat550190"},
                    "Compression Hosiery & Stockings": {"url": "/shop/home-health-care/diabetes-care/compression-hosiery-stockings", "id": "cat550178"},
                },
            },
            "Braces & Supports": {
                "url": "/shop/home-health-care/braces-supports",
                "id": "cat550012",
                "subcategories": {
                    "Foot & Ankle Braces": {"url": "/shop/home-health-care/braces-supports/foot-ankle-braces", "id": "cat550148"},
                    "Hand & Wrist Braces": {"url": "/shop/home-health-care/braces-supports/hand-wrist-braces", "id": "cat550152"},
                    "Thigh & Knee Braces": {"url": "/shop/home-health-care/braces-supports/thigh-knee-braces", "id": "cat550164"},
                    "Arm & Elbow Braces": {"url": "/shop/home-health-care/braces-supports/arm-elbow-braces", "id": "cat550144"},
                    "Compression Hosiery & Stockings": {"url": "/shop/home-health-care/braces-supports/compression-hosiery-stockings", "id": "cat550172"},
                    "Waist & Back Braces": {"url": "/shop/home-health-care/braces-supports/waist-back-braces", "id": "cat550168"},
                    "Shoulder & Neck Braces": {"url": "/shop/home-health-care/braces-supports/shoulder-neck-braces", "id": "cat550160"},
                    "Slings & Splints": {"url": "/shop/home-health-care/braces-supports/slings-splints", "id": "cat3070006"},
                },
            },
            "Bathroom Safety": {
                "url": "/shop/home-health-care/bathroom-safety",
                "id": "cat550004",
                "subcategories": {
                    "Commodes & Raised Toilet Seats": {"url": "/shop/home-health-care/bathroom-safety/commodes-raised-toilet-seats", "id": "cat550036"},
                    "Shower & Bath Seats": {"url": "/shop/home-health-care/bathroom-safety/shower-bath-seats", "id": "cat550028"},
                    "Shower & Bath Accessories": {"url": "/shop/home-health-care/bathroom-safety/shower-bath-accessories", "id": "cat550038"},
                    "Bathtub Safety Rails & Grab Bars": {"url": "/shop/home-health-care/bathroom-safety/bathtub-safety-rails-grab-bars", "id": "cat550034"},
                    "Bedpans & Urinals": {"url": "/shop/home-health-care/bathroom-safety/bedpans-urinals", "id": "cat1630001"},
                },
            },
            "Canes & Crutches": {
                "url": "/shop/home-health-care/canes-crutches",
                "id": "cat550026",
                "subcategories": {
                    "Canes": {"url": "/shop/home-health-care/canes-crutches/canes", "id": "cat550072"},
                    "Crutches": {"url": "/shop/home-health-care/canes-crutches/crutches", "id": "cat550074"},
                    "Cane & Crutches Accessories": {"url": "/shop/home-health-care/canes-crutches/cane-crutches-accessories", "id": "cat550070"},
                },
            },
            "Hearing Aids & Accessories": {
                "url": "/shop/home-health-care/hearing-aids-accessories",
                "id": "cat1640001",
                "subcategories": {
                    "Hearing Aids": {"url": "/shop/home-health-care/hearing-aids-accessories/hearing-aids", "id": "cat2710001"},
                    "Hearing Aid Batteries": {"url": "/shop/home-health-care/hearing-aids-accessories/hearing-aid-batteries", "id": "cat2010020"},
                    "Hearing Aid Accessories": {"url": "/shop/home-health-care/hearing-aids-accessories/hearing-aid-accessories", "id": "cat1640004"},
                },
            },
            "Fitness & Rehab": {
                "url": "/shop/home-health-care/fitness-rehab",
                "id": "cat550016",
                "subcategories": {
                    "Fitness & Rehab Equipment": {"url": "/shop/home-health-care/fitness-rehab/fitness-rehab-equipment", "id": "cat550154"},
                    "Heart Rate Monitors & Stethoscopes": {"url": "/shop/home-health-care/fitness-rehab/heart-rate-monitors-stethoscopes", "id": "cat550158"},
                    "Fitness Trackers & Scales": {"url": "/shop/home-health-care/fitness-rehab/fitness-trackers-scales", "id": "cat550166"},
                },
            },
            "Foot Care": {
                "url": "/shop/home-health-care/foot-care",
                "id": "cat2368",
                "subcategories": {
                    "Shoe Inserts & Insoles": {"url": "/shop/home-health-care/foot-care/shoe-inserts-insoles", "id": "cat3602"},
                    "Antifungal & Athlete's Foot": {"url": "/shop/home-health-care/foot-care/antifungal-athletes-foot", "id": "cat3597"},
                },
            },
            "Walkers & Rollators": {
                "url": "/shop/home-health-care/walkers-rollators",
                "id": "cat550030",
                "subcategories": {
                    "Walkers": {"url": "/shop/home-health-care/walkers-rollators/walkers", "id": "cat550056"},
                    "Rollators": {"url": "/shop/home-health-care/walkers-rollators/rollators", "id": "cat550058"},
                    "Walker & Rollator Accessories": {"url": "/shop/home-health-care/walkers-rollators/walker-rollator-accessories", "id": "cat550062"},
                },
            },
            "Wheelchairs & Accessories": {
                "url": "/shop/home-health-care/wheelchairs-accessories",
                "id": "cat550032",
                "subcategories": {
                    "Wheelchairs": {"url": "/shop/home-health-care/wheelchairs-accessories/wheelchairs", "id": "cat550042"},
                    "Wheelchair Accessories": {"url": "/shop/home-health-care/wheelchairs-accessories/wheelchair-accessories", "id": "cat550052"},
                },
            },
            "Scooters & Accessories": {
                "url": "/shop/home-health-care/scooters-accessories",
                "id": "cat550022",
                "subcategories": {
                    "Scooters": {"url": "/shop/home-health-care/scooters-accessories/scooters", "id": "cat550080"},
                    "Scooter Accessories": {"url": "/shop/home-health-care/scooters-accessories/scooter-accessories", "id": "cat550082"},
                },
            },
        },
    },
    "Baby & Kids": {
        "url": "/shop/baby-kids",
        "id": "cat2024",
        "subcategories": {
            "Baby & Kids Health": {
                "url": "/shop/baby-kids/baby-kids-health",
                "id": "cat2025",
                "subcategories": {
                    "Baby & Kids Cough, Cold & Flu": {"url": "/shop/baby-kids/baby-kids-health/baby-kids-cough-cold-flu", "id": "cat2032"},
                    "Baby & Kids Pain & Fever": {"url": "/shop/baby-kids/baby-kids-health/baby-kids-pain-fever", "id": "cat2131"},
                    "Baby & Kids Allergy": {"url": "/shop/baby-kids/baby-kids-health/baby-kids-allergy", "id": "cat2132"},
                    "Baby & Kids Digestive Health": {"url": "/shop/baby-kids/baby-kids-health/baby-kids-digestive-health", "id": "cat2037"},
                    "Baby & Kids Vitamins": {"url": "/shop/baby-kids/baby-kids-health/baby-kids-vitamins", "id": "cat2033"},
                    "Baby & Kids Sleep": {"url": "/shop/baby-kids/baby-kids-health/baby-kids-sleep", "id": "cat3070001"},
                    "Baby & Kids Electrolytes": {"url": "/shop/baby-kids/baby-kids-health/baby-kids-electrolytes", "id": "cat1590006"},
                    "Baby & Kids Oral Care": {"url": "/shop/baby-kids/baby-kids-health/baby-kids-oral-care", "id": "cat2039"},
                    "Teething": {"url": "/shop/baby-kids/baby-kids-health/teething", "id": "cat3100004"},
                    "Thermometers": {"url": "/shop/baby-kids/baby-kids-health/thermometers", "id": "cat2035"},
                },
            },
            "Baby & Kids Bath & Skin Care": {
                "url": "/shop/baby-kids/baby-kids-bath-skin-care",
                "id": "cat2026",
                "subcategories": {
                    "Baby & Kids Skin Care": {
                        "url": "/shop/baby-kids/baby-kids-bath-skin-care/baby-kids-skin-care",
                        "id": "cat3100001",
                        "subcategories": {
                            "Baby & Kids Sunscreen": {"url": "/shop/baby-kids/baby-kids-bath-skin-care/baby-kids-skin-care/baby-kids-sunscreen", "id": "cat2133"},
                            "Baby Creams & Ointments": {"url": "/shop/baby-kids/baby-kids-bath-skin-care/baby-kids-skin-care/baby-creams-ointments", "id": "cat2124"},
                            "Baby Lotion": {"url": "/shop/baby-kids/baby-kids-bath-skin-care/baby-kids-skin-care/baby-lotion", "id": "cat2046"},
                            "Baby Oil": {"url": "/shop/baby-kids/baby-kids-bath-skin-care/baby-kids-skin-care/baby-oil", "id": "cat2108"},
                            "Baby Powder": {"url": "/shop/baby-kids/baby-kids-bath-skin-care/baby-kids-skin-care/baby-powder", "id": "cat2047"},
                            "Diaper Rash Treatments": {"url": "/shop/baby-kids/baby-kids-bath-skin-care/baby-kids-skin-care/diaper-rash-treatments", "id": "cat1590010"},
                        },
                    },
                    "Baby & Kids Bath & Grooming Accessories": {"url": "/shop/baby-kids/baby-kids-bath-skin-care/baby-kids-bath-grooming-accessories", "id": "cat2043"},
                    "Baby & Kids Wash & Shampoo": {"url": "/shop/baby-kids/baby-kids-bath-skin-care/baby-kids-wash-shampoo", "id": "cat2044"},
                },
            },
            "Diapers & Wipes": {
                "url": "/shop/baby-kids/diapers-wipes",
                "id": "cat2027",
                "subcategories": {
                    "Wipes": {"url": "/shop/baby-kids/diapers-wipes/wipes", "id": "cat2049"},
                    "Diapers": {
                        "url": "/shop/baby-kids/diapers-wipes/diapers",
                        "id": "cat2048",
                        "subcategories": {
                            "Daytime Diapers": {"url": "/shop/baby-kids/diapers-wipes/diapers/daytime-diapers", "id": "cat3100005"},
                            "Overnight Diapers": {"url": "/shop/baby-kids/diapers-wipes/diapers/overnight-diapers", "id": "cat3100006"},
                            "Training Pants": {"url": "/shop/baby-kids/diapers-wipes/diapers/training-pants", "id": "cat2055"},
                            "Bedwetting Underwear": {"url": "/shop/baby-kids/diapers-wipes/diapers/bedwetting-underwear", "id": "cat1590008"},
                            "Swim Diapers": {"url": "/shop/baby-kids/diapers-wipes/diapers/swim-diapers", "id": "cat1590009"},
                        },
                    },
                },
            },
            "Feeding & Nursing": {
                "url": "/shop/baby-kids/feeding-nursing",
                "id": "cat2028",
                "subcategories": {
                    "Baby Formula": {"url": "/shop/baby-kids/feeding-nursing/baby-formula", "id": "cat3100011"},
                    "Baby Food": {"url": "/shop/baby-kids/feeding-nursing/baby-food", "id": "cat2060"},
                    "Bottles & Nipples": {"url": "/shop/baby-kids/feeding-nursing/bottles-nipples", "id": "cat2059"},
                    "Breast Pumps & Accessories": {"url": "/shop/baby-kids/feeding-nursing/breast-pumps-accessories", "id": "cat3438"},
                    "Bibs": {"url": "/shop/baby-kids/feeding-nursing/bibs", "id": "cat30003"},
                    "Sippy Cups": {"url": "/shop/baby-kids/feeding-nursing/sippy-cups", "id": "cat3100009"},
                    "Pacifiers": {"url": "/shop/baby-kids/feeding-nursing/pacifiers", "id": "cat2062"},
                },
            },
            "Gifts & Toys": {
                "url": "/shop/baby-kids/gifts-toys",
                "id": "cat3441",
                "subcategories": {
                    "Toys": {"url": "/shop/baby-kids/gifts-toys/toys", "id": "cat1590012"},
                    "Gift Sets": {"url": "/shop/baby-kids/gifts-toys/gift-sets", "id": "cat3444"},
                    "Sound Machines": {"url": "/shop/baby-kids/gifts-toys/sound-machines", "id": "cat3100007"},
                },
            },
            "Prenatal & Postpartum Care": {"url": "/shop/baby-kids/prenatal-postpartum-care", "id": "cat3070002"},
        },
    },
    "Diet & Nutrition": {
        "url": "/shop/diet-nutrition",
        "id": "cat2781",
        "subcategories": {
            "Protein": {
                "url": "/shop/diet-nutrition/protein",
                "id": "cat1210001",
                "subcategories": {
                    "Protein Drinks & Shakes": {"url": "/shop/diet-nutrition/protein/protein-drinks-shakes", "id": "cat3090002"},
                    "Protein Powders": {"url": "/shop/diet-nutrition/protein/protein-powders", "id": "cat3090003"},
                    "Protein Bars & Snacks": {"url": "/shop/diet-nutrition/protein/protein-bars-snacks", "id": "cat1210006"},
                },
            },
            "Balanced Nutrition": {
                "url": "/shop/diet-nutrition/balanced-nutrition",
                "id": "cat2828",
                "subcategories": {
                    "Nutrition Shakes": {"url": "/shop/diet-nutrition/balanced-nutrition/nutrition-shakes", "id": "cat2838"},
                    "Nutrition Powders": {"url": "/shop/diet-nutrition/balanced-nutrition/nutrition-powders", "id": "cat2839"},
                },
            },
            "Weight Management": {
                "url": "/shop/diet-nutrition/weight-management",
                "id": "cat2827",
                "subcategories": {
                    "Weight Loss & Detox Supplements": {"url": "/shop/diet-nutrition/weight-management/weight-loss-detox-supplements", "id": "cat2844"},
                },
            },
            "Sports & Workout Supplements": {
                "url": "/shop/diet-nutrition/sports-workout-supplements",
                "id": "cat2829",
                "subcategories": {
                    "Energy Supplements": {"url": "/shop/diet-nutrition/sports-workout-supplements/energy-supplements", "id": "cat830001"},
                    "Hydration": {"url": "/shop/diet-nutrition/sports-workout-supplements/hydration", "id": "cat3090001"},
                    "Pre-Workout": {"url": "/shop/diet-nutrition/sports-workout-supplements/pre-workout", "id": "cat3070031"},
                    "Post-Workout & Recovery": {"url": "/shop/diet-nutrition/sports-workout-supplements/post-workout-recovery", "id": "cat3070032"},
                },
            },
            "Fitness & Exercise": {
                "url": "/shop/diet-nutrition/fitness-exercise",
                "id": "cat3475",
                "subcategories": {
                    "Fitness & Exercise Equipment": {"url": "/shop/diet-nutrition/fitness-exercise/fitness-exercise-equipment", "id": "cat1690026"},
                    "Fitness Trackers & Scales": {"url": "/shop/diet-nutrition/fitness-exercise/fitness-trackers-scales", "id": "cat3479"},
                },
            },
        },
    },
    "Party Supplies & Gifts": {
        "url": "/shop/party-supplies-gifts",
        "id": "cat226646184",
        "subcategories": {
            "Balloons": {"url": "/shop/party-supplies-gifts/balloons", "id": "cat226646213"},
            "Party Decorations": {"url": "/shop/party-supplies-gifts/party-decorations", "id": "cat226646265"},
            "Gift Wrap & Accessories": {"url": "/shop/party-supplies-gifts/gift-wrap-accessories", "id": "cat226646226"},
            "Greeting Cards": {"url": "/shop/party-supplies-gifts/greeting-cards", "id": "cat226646254"},
            "Flowers": {"url": "/shop/party-supplies-gifts/flowers", "id": "cat226646222"},
        },
    },
    "Seasonal Shops": {
        "url": "/shop/seasonal-shops",
        "id": "cat3333",
        "subcategories": {
            "Summer": {
                "url": "/shop/seasonal-shops/summer",
                "id": "cat313151",
                "subcategories": {
                    "Coolers & Tumblers": {"url": "/shop/seasonal-shops/summer/coolers-tumblers", "id": "cat226475444"},
                    "Beach & Pool": {"url": "/shop/seasonal-shops/summer/beach-pool", "id": "cat226475476"},
                    "Summer Toys & Games": {"url": "/shop/seasonal-shops/summer/summer-toys-games", "id": "cat226475504"},
                    "Fans": {"url": "/shop/seasonal-shops/summer/fans", "id": "cat226475459"},
                    "Summer Apparel": {"url": "/shop/seasonal-shops/summer/summer-apparel", "id": "cat226475489"},
                    "Americana": {"url": "/shop/seasonal-shops/summer/americana", "id": "cat226394839"},
                },
            },
            "Halloween": {
                "url": "/shop/seasonal-shops/halloween",
                "id": "cat313152",
                "subcategories": {
                    "Halloween Candy": {"url": "/shop/seasonal-shops/halloween/halloween-candy", "id": "cat313155"},
                    "Halloween Decor": {"url": "/shop/seasonal-shops/halloween/halloween-decor", "id": "cat313156"},
                    "Halloween Beauty": {"url": "/shop/seasonal-shops/halloween/halloween-beauty", "id": "cat313159"},
                    "Halloween Toys & Activities": {"url": "/shop/seasonal-shops/halloween/halloween-toys-activities", "id": "cat313162"},
                    "Candy Baskets & Bowls": {"url": "/shop/seasonal-shops/halloween/candy-baskets-bowls", "id": "cat222006762"},
                    "Halloween Costumes & Accessories": {"url": "/shop/seasonal-shops/halloween/halloween-costumes-accessories", "id": "cat230145103"},
                },
            },
            "Fall": {"url": "/shop/seasonal-shops/fall", "id": "cat313173"},
            "Hanukkah": {"url": "/shop/seasonal-shops/hanukkah", "id": "cat313153"},
            "St. Patrick's Day": {"url": "/shop/seasonal-shops/st-patricks-day", "id": "cat313131"},
            "Holiday": {
                "url": "/shop/seasonal-shops/holiday",
                "id": "cat313154",
                "subcategories": {
                    "Holiday Gifts": {
                        "url": "/shop/seasonal-shops/holiday/holiday-gifts",
                        "id": "cat313165",
                        "subcategories": {
                            "Gift Sets": {"url": "/shop/seasonal-shops/holiday/holiday-gifts/gift-sets", "id": "cat313174"},
                            "Gifts for Her": {"url": "/shop/seasonal-shops/holiday/holiday-gifts/gifts-for-her", "id": "cat313171"},
                            "Gifts for Him": {"url": "/shop/seasonal-shops/holiday/holiday-gifts/gifts-for-him", "id": "cat313172"},
                            "Gifts for Kids": {"url": "/shop/seasonal-shops/holiday/holiday-gifts/gifts-for-kids", "id": "cat313170"},
                        },
                    },
                    "Stocking Stuffers": {"url": "/shop/seasonal-shops/holiday/stocking-stuffers", "id": "cat313168"},
                    "Holiday Candy": {"url": "/shop/seasonal-shops/holiday/holiday-candy", "id": "cat313157"},
                    "Holiday Decor": {"url": "/shop/seasonal-shops/holiday/holiday-decor", "id": "cat313158"},
                    "Advent Calendars": {"url": "/shop/seasonal-shops/holiday/advent-calendars", "id": "cat233114748"},
                    "Gift Wrapping": {"url": "/shop/seasonal-shops/holiday/gift-wrapping", "id": "cat313169"},
                    "Holiday Snacks": {"url": "/shop/seasonal-shops/holiday/holiday-snacks", "id": "cat234120304"},
                },
            },
            "Valentine's Day": {"url": "/shop/seasonal-shops/valentines-day", "id": "cat313144"},
            "Party Supplies": {
                "url": "/shop/seasonal-shops/party-supplies",
                "id": "cat131314",
                "subcategories": {
                    "Party Decorations": {"url": "/shop/seasonal-shops/party-supplies/party-decorations", "id": "cat313183"},
                    "Balloons": {"url": "/shop/seasonal-shops/party-supplies/balloons", "id": "cat313182"},
                    "Gift Wrap & Accessories": {"url": "/shop/seasonal-shops/party-supplies/gift-wrap-accessories", "id": "cat313184"},
                    "Greeting Cards": {"url": "/shop/seasonal-shops/party-supplies/greeting-cards", "id": "cat313181"},
                    "Flowers": {"url": "/shop/seasonal-shops/party-supplies/flowers", "id": "cat313180"},
                },
            },
            "Mother's Day": {"url": "/shop/seasonal-shops/mothers-day", "id": "cat313149"},
            "Easter": {
                "url": "/shop/seasonal-shops/easter",
                "id": "cat313137",
                "subcategories": {
                    "Easter Candy": {"url": "/shop/seasonal-shops/easter/easter-candy", "id": "cat313138"},
                    "Easter Toys & Gifts": {"url": "/shop/seasonal-shops/easter/easter-toys-gifts", "id": "cat313140"},
                    "Easter Decor": {"url": "/shop/seasonal-shops/easter/easter-decor", "id": "cat313141"},
                    "Easter Baskets": {"url": "/shop/seasonal-shops/easter/easter-baskets", "id": "cat313139"},
                    "Easter Activities": {"url": "/shop/seasonal-shops/easter/easter-activities", "id": "cat3131342"},
                },
            },
            "Father's Day": {"url": "/shop/seasonal-shops/fathers-day", "id": "cat313150"},
        },
    },
    "Health Benefits": {
        "url": "/shop/health-benefits",
        "id": "cat233970",
        "subcategories": {
            "OTC Eligible": {"url": "/shop/health-benefits/otc-eligible", "id": "cat234241"},
            "SNAP Eligible": {"url": "/shop/health-benefits/snap-eligible", "id": "cat234243"},
            "FSA HSA Eligible": {"url": "/shop/health-benefits/fsa-hsa-eligible", "id": "cat234239"},
        },
    },
}
