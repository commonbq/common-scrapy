"""Menards US crawlable category inventory from the live homepage mega-navigation.

Each group is a "Shop > Departments" navigation department from the
server-rendered ``mcom-header`` menu JSON on the Menards homepage.
The leaf key is the crawl-target name (a slug of the navigation label)
that ``-a category=<leaf>`` selects; the value carries the canonical
``/main/.../c-<id>.htm`` listing URL. Leaf keys are globally unique so a
bare category remains a safe Airflow task / GCS output path.

Captured from https://www.menards.com/main/ on 2026-10-14; all 25
department URLs returned HTTP 200 through the configured US proxy.
Non-catalog navigation destinations (custom measurement entry pages and a
marketing landing page) are excluded because the spider needs a resolvable
``c-<id>`` category id. 13 destinations exposed under two departments are
kept once, under their canonical URL.
"""

from __future__ import annotations

MENARDS_CATEGORIES: dict[str, dict[str, dict[str, str]]] = {
    "halloween": {
        "halloween-animated-decorations": {
            "name": "Halloween Animated Decorations",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/halloween-animated-decorations/c-19081.htm",
        },
        "halloween-candy": {
            "name": "Halloween Candy",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/halloween-candy/c-12841.htm",
        },
        "halloween-safety-tips": {
            "name": "Halloween Safety Tips",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/halloween-articles/c-13563.htm",
        },
        "halloween-indoor-decorations": {
            "name": "Halloween Indoor Decorations",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/halloween-indoor-decorations/c-12272.htm",
        },
        "halloween-village": {
            "name": "Halloween Village",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/halloween-village/c-12271.htm",
        },
        "halloween-lights": {
            "name": "Halloween Lights",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/halloween-lights/c-12274.htm",
        },
        "halloween-outdoor-decorations": {
            "name": "Halloween Outdoor Decorations",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/halloween-outdoor-decorations/c-12273.htm",
        },
        "fall-decorations": {
            "name": "Fall Decorations",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/halloween-decorations/c-12275.htm",
        },
        "pumpkin-carving": {
            "name": "Pumpkin Carving",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/pumpkin-carving/c-12346.htm",
        },
        "trick-or-treat-containers": {
            "name": "Trick-or-Treat Containers",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/trick-or-treat-containers/c-12277.htm",
        },
        "party-accessories": {
            "name": "Party Accessories",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/party-accessories/c-12276.htm",
        },
        "halloween-inflatables": {
            "name": "Halloween Inflatables",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/halloween-inflatables/c-642874317074394.htm",
        },
        "shop-all-halloween": {
            "name": "Shop All Halloween",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/shop-all-halloween/c-1642874323404220.htm",
        },
    },
    "appliances": {
        "shop-all-appliances": {
            "name": "Shop All Appliances",
            "url": "https://www.menards.com/main/appliances/c-5570.htm",
        },
        "appliance-parts-accessories": {
            "name": "Appliance Parts & Accessories",
            "url": "https://www.menards.com/main/appliances/appliance-parts-accessories/c-9332.htm",
        },
        "cooktops": {
            "name": "Cooktops",
            "url": "https://www.menards.com/main/appliances/cooktops/c-14092.htm",
        },
        "dishwashers": {
            "name": "Dishwashers",
            "url": "https://www.menards.com/main/appliances/dishwashers/c-19790.htm",
        },
        "freezers": {
            "name": "Freezers",
            "url": "https://www.menards.com/main/appliances/freezers-ice-makers/c-7214.htm",
        },
        "ice-makers": {
            "name": "Ice Makers",
            "url": "https://www.menards.com/main/appliances/ice-makers/c-1642874270694520.htm",
        },
        "microwaves": {
            "name": "Microwaves",
            "url": "https://www.menards.com/main/appliances/microwaves/c-1526071950674.htm",
        },
        "range-hoods": {
            "name": "Range Hoods",
            "url": "https://www.menards.com/main/appliances/range-hoods/c-9571.htm",
        },
        "ranges": {
            "name": "Ranges",
            "url": "https://www.menards.com/main/appliances/ranges/c-5585.htm",
        },
        "refrigerators": {
            "name": "Refrigerators",
            "url": "https://www.menards.com/main/appliances/refrigerators/c-14090.htm",
        },
        "small-appliances": {
            "name": "Small Appliances",
            "url": "https://www.menards.com/main/appliances/small-appliances/c-19832.htm",
        },
        "trash-compactors": {
            "name": "Trash Compactors",
            "url": "https://www.menards.com/main/appliances/trash-compactors/c-1501685855351.htm",
        },
        "vacuum-cleaners-floor-care": {
            "name": "Vacuum Cleaners & Floor Care",
            "url": "https://www.menards.com/main/appliances/vacuum-cleaners-floor-care/c-14094.htm",
        },
        "wall-ovens": {
            "name": "Wall Ovens",
            "url": "https://www.menards.com/main/appliances/wall-ovens/c-14089.htm",
        },
        "washing-machines-dryers": {
            "name": "Washing Machines & Dryers",
            "url": "https://www.menards.com/main/appliances/washers-dryers/c-14095.htm",
        },
    },
    "automotive": {
        "shop-all-automotive": {
            "name": "Shop All Automotive",
            "url": "https://www.menards.com/main/tools/automotive/c-9097.htm",
        },
        "automotive-accessories": {
            "name": "Automotive Accessories",
            "url": "https://www.menards.com/main/tools/automotive/automotive-accessories/c-9098.htm",
        },
        "automotive-batteries": {
            "name": "Automotive Batteries",
            "url": "https://www.menards.com/main/tools/automotive/automotive-batteries/c-1516819218414.htm",
        },
        "automotive-cleaning-detailing": {
            "name": "Automotive Cleaning & Detailing",
            "url": "https://www.menards.com/main/tools/automotive/automotive-cleaning-detailing/c-9102.htm",
        },
        "automotive-fluids-chemicals": {
            "name": "Automotive Fluids & Chemicals",
            "url": "https://www.menards.com/main/tools/automotive/automotive-maintenance/automotive-fluids-chemicals/c-10098.htm",
        },
        "automotive-grease-lubricants": {
            "name": "Automotive Grease & Lubricants",
            "url": "https://www.menards.com/main/tools/automotive/automotive-maintenance/automotive-grease-lubricants/c-9104.htm",
        },
        "automotive-light-bulbs-fuses": {
            "name": "Automotive Light Bulbs & Fuses",
            "url": "https://www.menards.com/main/tools/automotive/automotive-maintenance/automotive-light-bulbs/c-9110.htm",
        },
        "automotive-maintenance": {
            "name": "Automotive Maintenance",
            "url": "https://www.menards.com/main/tools/automotive/automotive-maintenance/c-1527112433739.htm",
        },
        "automotive-safety": {
            "name": "Automotive Safety",
            "url": "https://www.menards.com/main/tools/automotive/automotive-safety/c-1497895319158.htm",
        },
        "automotive-tools-shop-equipment": {
            "name": "Automotive Tools & Shop Equipment",
            "url": "https://www.menards.com/main/tools/automotive/automotive-tools-shop-equipment/c-9113.htm",
        },
        "battery-chargers-jumper-cables": {
            "name": "Battery Chargers & Jumper Cables",
            "url": "https://www.menards.com/main/tools/automotive/chargers-jumper-cables/c-9100.htm",
        },
        "car-covers": {
            "name": "Car Covers",
            "url": "https://www.menards.com/main/tools/automotive/car-covers/c-1497371000608.htm",
        },
        "electric-car-chargers": {
            "name": "Electric Car Chargers",
            "url": "https://www.menards.com/main/tools/automotive/electric-car-chargers/c-13417.htm",
        },
        "lawn-mower-atv-attachments": {
            "name": "Lawn Mower & ATV Attachments",
            "url": "https://www.menards.com/main/tools/automotive/atv-accessories/c-1527167451382.htm",
        },
        "motor-oil-filters": {
            "name": "Motor Oil & Filters",
            "url": "https://www.menards.com/main/tools/automotive/automotive-maintenance/motor-oil-filters/c-9112.htm",
        },
        "tires-tire-care": {
            "name": "Tires & Tire Care",
            "url": "https://www.menards.com/main/tools/automotive/tires-tire-care/c-1487166914220.htm",
        },
        "towing-cargo-management": {
            "name": "Towing & Cargo Management",
            "url": "https://www.menards.com/main/tools/automotive/towing-cargo-management/c-12171.htm",
        },
        "windshield-wiper-blades": {
            "name": "Windshield Wiper Blades",
            "url": "https://www.menards.com/main/tools/automotive/windshield-wiper-blades/c-1486994582435.htm",
        },
        "battery-components-accessories": {
            "name": "Battery Components & Accessories",
            "url": "https://www.menards.com/c-4489435076251695.htm",
        },
    },
    "bath": {
        "shop-all-bath": {
            "name": "Shop All Bath",
            "url": "https://www.menards.com/main/bath/c-5867.htm",
        },
        "bath-towels-washcloths": {
            "name": "Bath Towels & Washcloths",
            "url": "https://www.menards.com/main/bath/bathroom-hardware-coordinates/bath-towels-washcloths/c-14054.htm",
        },
        "bathroom-cabinets-storage": {
            "name": "Bathroom Cabinets & Storage",
            "url": "https://www.menards.com/main/bath/bathroom-cabinets-storage/c-9450.htm",
        },
        "bathroom-fan-accessories": {
            "name": "Bathroom Fan Accessories",
            "url": "https://www.menards.com/main/bath/bathroom-fan-accessories/c-1453749026746.htm",
        },
        "bathroom-fans-ventilators": {
            "name": "Bathroom Fans & Ventilators",
            "url": "https://www.menards.com/main/bath/bathroom-fans-ventilators/c-5869.htm",
        },
        "bathroom-faucets": {
            "name": "Bathroom Faucets",
            "url": "https://www.menards.com/main/bath/bathroom-faucets-showerheads/c-5904.htm",
        },
        "bathroom-hardware-coordinates": {
            "name": "Bathroom Hardware & Coordinates",
            "url": "https://www.menards.com/main/bath/bathroom-hardware-coordinates/c-5913.htm",
        },
        "bathroom-rugs": {
            "name": "Bathroom Rugs",
            "url": "https://www.menards.com/main/flooring-rugs/area-rugs-mats-runners/bathroom-rugs/c-12414.htm",
        },
        "bathroom-safety": {
            "name": "Bathroom Safety",
            "url": "https://www.menards.com/main/bath/bathroom-safety/c-6052.htm",
        },
        "bathroom-sinks": {
            "name": "Bathroom Sinks",
            "url": "https://www.menards.com/main/bath/bathroom-sinks/c-1451416484952.htm",
        },
        "bathroom-vanities-tops": {
            "name": "Bathroom Vanities & Tops",
            "url": "https://www.menards.com/main/bath/bathroom-vanities-tops/c-5898.htm",
        },
        "bathtubs-whirlpool-tubs": {
            "name": "Bathtubs & Whirlpool Tubs",
            "url": "https://www.menards.com/main/bath/bathtubs-whirlpool-tubs/c-13927.htm",
        },
        "mirrors": {
            "name": "Mirrors",
            "url": "https://www.menards.com/main/grocery-home/decorative-accents/mirrors/c-6937.htm",
        },
        "restroom-supplies": {
            "name": "Restroom Supplies",
            "url": "https://www.menards.com/main/bath/restroom-supplies/c-6197.htm",
        },
        "showers-shower-doors": {
            "name": "Showers & Shower Doors",
            "url": "https://www.menards.com/main/bath/showers-shower-doors/c-8350.htm",
        },
        "toilets": {
            "name": "Toilets",
            "url": "https://www.menards.com/main/bath/toilets/c-5967.htm",
        },
        "towel-warmers": {
            "name": "Towel Warmers",
            "url": "https://www.menards.com/main/bath/towel-warmers/c-9933.htm",
        },
        "showerheads": {
            "name": "Showerheads",
            "url": "https://www.menards.com/main/bath/bathroom-faucets/showerheads/c-5907.htm",
        },
        "showerheads-showerhead-accessories": {
            "name": "Showerheads & Showerhead Accessories",
            "url": "https://www.menards.com/main/bath/showerheads-showerhead-accessories/c-4324134937613739.htm",
        },
    },
    "building-materials": {
        "shop-all-building-materials": {
            "name": "Shop All Building Materials",
            "url": "https://www.menards.com/main/building-materials/c-5640.htm",
        },
        "acrylic-glass-sheets": {
            "name": "Acrylic & Glass Sheets",
            "url": "https://www.menards.com/main/doors-windows-millwork/acrylic-glass-sheets/c-7551.htm",
        },
        "books-building-plans": {
            "name": "Books & Building Plans",
            "url": "https://www.menards.com/main/building-materials/books-building-plans/c-5788.htm",
        },
        "columns-accessories": {
            "name": "Columns & Accessories",
            "url": "https://www.menards.com/main/building-materials/columns-accessories/c-5721.htm",
        },
        "concrete-cement-masonry": {
            "name": "Concrete, Cement & Masonry",
            "url": "https://www.menards.com/main/building-materials/concrete-cement-masonry/c-5641.htm",
        },
        "decking-deck-materials": {
            "name": "Decking & Deck Materials",
            "url": "https://www.menards.com/main/building-materials/decking-deck-materials/c-5727.htm",
        },
        "drywall": {
            "name": "Drywall",
            "url": "https://www.menards.com/main/building-materials/drywall/c-5654.htm",
        },
        "fencing": {
            "name": "Fencing",
            "url": "https://www.menards.com/main/building-materials/fencing/c-5734.htm",
        },
        "glass-blocks-glass-block-panels": {
            "name": "Glass Blocks & Glass Block Panels",
            "url": "https://www.menards.com/main/doors-windows-millwork/windows/glass-blocks-glass-block-panels/c-7685.htm",
        },
        "gutters-accessories": {
            "name": "Gutters & Accessories",
            "url": "https://www.menards.com/main/building-materials/gutters-accessories/c-5811.htm",
        },
        "homes": {
            "name": "Homes",
            "url": "https://www.menards.com/main/landing-pages/homes/c-1642874255983027.htm",
        },
        "insulation": {
            "name": "Insulation",
            "url": "https://www.menards.com/main/building-materials/insulation/c-5775.htm",
        },
        "landscape-block": {
            "name": "Landscape Block",
            "url": "https://www.menards.com/main/building-materials/landscape-block/c-12987.htm",
        },
        "landscaping-materials": {
            "name": "Landscaping Materials",
            "url": "https://www.menards.com/main/building-materials/landscaping-materials/c-5781.htm",
        },
        "lumber-boards": {
            "name": "Lumber & Boards",
            "url": "https://www.menards.com/main/building-materials/lumber-boards/c-5666.htm",
        },
        "metal-framing": {
            "name": "Metal Framing",
            "url": "https://www.menards.com/main/building-materials/metal-framing/c-5695.htm",
        },
        "plywood-and-panel-products": {
            "name": "Plywood and Panel Products",
            "url": "https://www.menards.com/main/building-materials/panel-products/c-5696.htm",
        },
        "post-frame": {
            "name": "Post Frame",
            "url": "https://www.menards.com/main/building-materials/pole-barn-post-frame-materials/c-5712.htm",
        },
        "roofing": {
            "name": "Roofing",
            "url": "https://www.menards.com/main/building-materials/roofing/c-5809.htm",
        },
        "roofing-tape": {
            "name": "Roofing Tape",
            "url": "https://www.menards.com/main/paint/adhesives-glue-tape/tape/roofing-tape/c-13189.htm",
        },
        "sheds-accessories": {
            "name": "Sheds & Accessories",
            "url": "https://www.menards.com/main/outdoors/sheds-accessories/c-9482.htm",
        },
        "siding": {
            "name": "Siding",
            "url": "https://www.menards.com/main/building-materials/siding/c-5823.htm",
        },
        "soffit": {
            "name": "Soffit",
            "url": "https://www.menards.com/main/building-materials/soffit/c-1488981946224.htm",
        },
        "steel-roofing": {
            "name": "Steel Roofing",
            "url": "https://www.menards.com/main/building-materials/steel-roofing/c-1539610070430.htm",
        },
        "treated-lumber": {
            "name": "Treated Lumber",
            "url": "https://www.menards.com/main/building-materials/lumber-boards/treated-wood-products/c-13123.htm",
        },
        "trusses-i-joists-engineered-lumber": {
            "name": "Trusses, I-Joists & Engineered Lumber",
            "url": "https://www.menards.com/main/building-materials/trusses-i-joists-engineered-lumber/c-5657.htm",
        },
        "wall-paneling-planking": {
            "name": "Wall Paneling & Planking",
            "url": "https://www.menards.com/main/paint/paneling-planking/c-8162.htm",
        },
    },
    "clothing": {
        "shop-all-clothing": {
            "name": "Shop All Clothing",
            "url": "https://www.menards.com/main/clothing/c-7079.htm",
        },
        "belts": {
            "name": "Belts",
            "url": "https://www.menards.com/main/home-decor/apparel/belts/c-12937.htm",
        },
        "footwear-footwear-accessories": {
            "name": "Footwear & Footwear Accessories",
            "url": "https://www.menards.com/main/grocery-home/clothing-accessories/footwear-footwear-accessories/c-7093.htm",
        },
        "gloves": {
            "name": "Gloves",
            "url": "https://www.menards.com/main/grocery-home/clothing-accessories/gloves/c-7080.htm",
        },
        "headwear": {
            "name": "Headwear",
            "url": "https://www.menards.com/main/grocery-home/clothing-accessories/headwear/c-7087.htm",
        },
        "outerwear": {
            "name": "Outerwear",
            "url": "https://www.menards.com/main/grocery-home/clothing-accessories/jackets/c-9443.htm",
        },
        "pants": {
            "name": "Pants",
            "url": "https://www.menards.com/main/clothing/pants/c-7089.htm",
        },
        "raingear-umbrellas": {
            "name": "Raingear & Umbrellas",
            "url": "https://www.menards.com/main/grocery-home/clothing-accessories/raincoats-umbrellas/c-7090.htm",
        },
        "shirts": {
            "name": "Shirts",
            "url": "https://www.menards.com/main/grocery-home/clothing-accessories/shirts/c-7091.htm",
        },
        "shorts": {
            "name": "Shorts",
            "url": "https://www.menards.com/main/home-decor/apparel/shorts/c-12303.htm",
        },
        "underwear-undershirts": {
            "name": "Underwear & Undershirts",
            "url": "https://www.menards.com/main/clothing/underwear-undershirts/c-4364363663421587.htm",
        },
        "wallets": {
            "name": "Wallets",
            "url": "https://www.menards.com/main/home-decor/apparel/wallets/c-12990.htm",
        },
    },
    "doors-windows-millwork": {
        "shop-all-doors-windows-millwork": {
            "name": "Shop All Doors, Windows, & Millwork",
            "url": "https://www.menards.com/main/doors-windows-millwork/c-7550.htm",
        },
        "air-curtains-impact-doors-vinyl-strip-doors": {
            "name": "Air Curtains, Impact Doors & Vinyl Strip Doors",
            "url": "https://www.menards.com/main/maintenance-repair-operations/office-commercial/air-curtains-impact-doors-vinyl-strip-doors/c-12508.htm",
        },
        "awnings": {
            "name": "Awnings",
            "url": "https://www.menards.com/main/outdoors/patios-structures/awnings/c-13308.htm",
        },
        "commercial-sliding-doors": {
            "name": "Commercial Sliding Doors",
            "url": "https://www.menards.com/main/doors-windows-millwork/commercial-sliding-doors/c-1522847152982.htm",
        },
        "door-window-hardware": {
            "name": "Door & Window Hardware",
            "url": "https://www.menards.com/main/hardware/door-window-hardware/c-7575.htm",
        },
        "door-locks": {
            "name": "Door Locks",
            "url": "https://www.menards.com/main/hardware/door-locks/c-7597.htm",
        },
        "door-store-by-menards": {
            "name": "Door Store by Menards®",
            "url": "https://www.menards.com/main/door-store-by-menards/c-1554909130155.htm",
        },
        "dowels-pins-plugs-hobby-wood": {
            "name": "Dowels, Pins, Plugs & Hobby Wood",
            "url": "https://www.menards.com/main/doors-windows-millwork/dowels-wooden-pins-plugs/c-12188.htm",
        },
        "exterior-doors": {
            "name": "Exterior Doors",
            "url": "https://www.menards.com/main/doors-windows-millwork/exterior-doors/c-7562.htm",
        },
        "garage-doors-openers": {
            "name": "Garage Doors & Openers",
            "url": "https://www.menards.com/main/doors-windows-millwork/garage-doors-openers/c-3611.htm",
        },
        "interior-doors": {
            "name": "Interior Doors",
            "url": "https://www.menards.com/main/doors-windows-millwork/interior-doors/c-6257.htm",
        },
        "millwork-staircase-systems-accessories": {
            "name": "Millwork Staircase Systems & Accessories",
            "url": "https://www.menards.com/main/doors-windows-millwork/staircase-systems-parts/c-7671.htm",
        },
        "mobile-home-parts": {
            "name": "Mobile Home Parts",
            "url": "https://www.menards.com/main/doors-windows-millwork/mobile-home-parts/c-12533.htm",
        },
        "moulding": {
            "name": "Moulding",
            "url": "https://www.menards.com/main/doors-windows-millwork/moulding-trim/c-13427.htm",
        },
        "standard-window-door-screens": {
            "name": "Standard Window & Door Screens",
            "url": "https://www.menards.com/main/doors-windows-millwork/window-door-screening-supplies/screens/c-7666.htm",
        },
        "windows": {
            "name": "Windows",
            "url": "https://www.menards.com/main/doors-windows-millwork/windows/c-7681.htm",
        },
        "weather-stripping": {
            "name": "Weather Stripping",
            "url": "https://www.menards.com/main/hardware/weather-stripping/c-3624.htm",
        },
    },
    "electrical": {
        "shop-all-electrical": {
            "name": "Shop All Electrical",
            "url": "https://www.menards.com/main/electrical/c-6290.htm",
        },
        "alarms-security-systems": {
            "name": "Alarms & Security Systems",
            "url": "https://www.menards.com/main/electrical/doorbells-alarms-security-systems/c-6463.htm",
        },
        "batteries": {
            "name": "Batteries",
            "url": "https://www.menards.com/main/electrical/batteries/c-6303.htm",
        },
        "cable-ties": {
            "name": "Cable Ties",
            "url": "https://www.menards.com/main/electrical/electrical-tools-accessories/cable-ties/c-6443.htm",
        },
        "circuit-protection-power-distribution": {
            "name": "Circuit Protection & Power Distribution",
            "url": "https://www.menards.com/main/electrical/circuit-protection-distribution/c-14266.htm",
        },
        "conduit-conduit-fittings-raceways": {
            "name": "Conduit, Conduit Fittings & Raceways",
            "url": "https://www.menards.com/main/electrical/conduit-conduit-fittings-raceways/c-14265.htm",
        },
        "doorbells": {
            "name": "Doorbells",
            "url": "https://www.menards.com/main/electrical/doorbells/c-6466.htm",
        },
        "electrical-boxes-covers": {
            "name": "Electrical Boxes & Covers",
            "url": "https://www.menards.com/main/electrical/electrical-boxes-covers/c-14182.htm",
        },
        "electrical-tools": {
            "name": "Electrical Tools",
            "url": "https://www.menards.com/main/electrical/electrical-tools-accessories/c-6453.htm",
        },
        "extension-cords-surge-protectors": {
            "name": "Extension Cords & Surge Protectors",
            "url": "https://www.menards.com/main/electrical/electrical-cords-surge-protectors/c-9480.htm",
        },
        "fire-safety": {
            "name": "Fire Safety",
            "url": "https://www.menards.com/main/electrical/fire-safety/c-1475583176027.htm",
        },
        "home-electronics": {
            "name": "Home Electronics",
            "url": "https://www.menards.com/main/electrical/electronics/c-6294.htm",
        },
        "light-bulbs": {
            "name": "Light Bulbs",
            "url": "https://www.menards.com/main/electrical/light-bulbs/c-7477.htm",
        },
        "light-switches-dimmers-outlets": {
            "name": "Light Switches, Dimmers & Outlets",
            "url": "https://www.menards.com/main/electrical/light-switches-dimmers-outlets/c-6319.htm",
        },
        "lighting-ceiling-fans": {
            "name": "Lighting & Ceiling Fans",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/c-7476.htm",
        },
        "smart-home": {
            "name": "Smart Home",
            "url": "https://www.menards.com/main/electrical/smart-home/c-19772.htm",
        },
        "solar-wind-power": {
            "name": "Solar & Wind Power",
            "url": "https://www.menards.com/main/electrical/solar-wind-power/c-6292.htm",
        },
        "wall-plates": {
            "name": "Wall Plates",
            "url": "https://www.menards.com/main/electrical/wall-plates/c-1489667504662.htm",
        },
        "electrical-tape": {
            "name": "Electrical Tape",
            "url": "https://www.menards.com/main/paint/adhesives-glue-tape/tape/electrical-tape/c-6482.htm",
        },
        "electrical-wire-cable": {
            "name": "Electrical Wire & Cable",
            "url": "https://www.menards.com/main/electrical/electrical-wire-cable/c-1461705595760.htm",
        },
        "terminals-connectors": {
            "name": "Terminals & Connectors",
            "url": "https://www.menards.com/main/electrical/electrical-tools-accessories/terminals-connectors/c-13817.htm",
        },
        "wiring-fasteners": {
            "name": "Wiring Fasteners",
            "url": "https://www.menards.com/main/electrical/electrical-tools-accessories/wiring-fasteners/c-6448.htm",
        },
    },
    "flooring-rugs": {
        "shop-all-flooring-rugs": {
            "name": "Shop All Flooring & Rugs",
            "url": "https://www.menards.com/main/flooring-rugs/c-6512.htm",
        },
        "area-rugs-mats-runners": {
            "name": "Area Rugs, Mats & Runners",
            "url": "https://www.menards.com/main/flooring-rugs/area-rugs-mats-runners/c-6513.htm",
        },
        "carpet-carpet-tiles": {
            "name": "Carpet & Carpet Tiles",
            "url": "https://www.menards.com/main/flooring-rugs/carpet-carpet-tiles/c-6536.htm",
        },
        "exercise-gym-flooring": {
            "name": "Exercise & Gym Flooring",
            "url": "https://www.menards.com/main/flooring-rugs/exercise-gym-flooring/c-1536584011607.htm",
        },
        "fan-shop": {
            "name": "Fan Shop",
            "url": "https://www.menards.com/main/flooring-rugs/fan-shop/c-12716.htm",
        },
        "floor-wall-tile": {
            "name": "Floor & Wall Tile",
            "url": "https://www.menards.com/main/flooring-rugs/tile-stone/c-6546.htm",
        },
        "flooring-trims-edgings": {
            "name": "Flooring Trims & Edgings",
            "url": "https://www.menards.com/main/flooring-rugs/flooring-trims-edgings/c-12603.htm",
        },
        "garage-flooring": {
            "name": "Garage Flooring",
            "url": "https://www.menards.com/main/flooring-rugs/garage-flooring/c-6614.htm",
        },
        "hybrid-resilient-flooring": {
            "name": "Hybrid Resilient Flooring",
            "url": "https://www.menards.com/main/flooring-rugs/hybrid-resilient-flooring/c-4420330306932606.htm",
        },
        "laminate-flooring": {
            "name": "Laminate Flooring",
            "url": "https://www.menards.com/main/flooring-rugs/laminate-flooring/c-6606.htm",
        },
        "shop-all-hardwood-flooring": {
            "name": "Shop All Hardwood Flooring",
            "url": "https://www.menards.com/main/flooring-rugs/hardwood-flooring/c-6572.htm",
        },
        "under-floor-heating": {
            "name": "Under Floor Heating",
            "url": "https://www.menards.com/main/flooring-rugs/tile-stone/under-floor-heating/c-6331.htm",
        },
        "vinyl-flooring": {
            "name": "Vinyl Flooring",
            "url": "https://www.menards.com/main/flooring-rugs/vinyl-flooring/c-6615.htm",
        },
        "wall-base": {
            "name": "Wall Base",
            "url": "https://www.menards.com/main/flooring-rugs/wall-base/c-6613.htm",
        },
    },
    "furniture-home": {
        "shop-all-furniture-home": {
            "name": "Shop All Furniture & Home",
            "url": "https://www.menards.com/main/grocery-home/c-19741.htm",
        },
        "as-seen-on-tv": {
            "name": "As Seen on TV",
            "url": "https://www.menards.com/main/as-seen-on-tv/c-1489409021704.htm",
        },
        "books": {
            "name": "Books",
            "url": "https://www.menards.com/main/grocery-home/books/c-6484.htm",
        },
        "cleaning-supplies": {
            "name": "Cleaning Supplies",
            "url": "https://www.menards.com/main/grocery-home/cleaners-household-essentials/cleaning-supplies/c-14255.htm",
        },
        "craft-supplies": {
            "name": "Craft Supplies",
            "url": "https://www.menards.com/main/grocery-home/craft-supplies/c-6961.htm",
        },
        "decorative-accents": {
            "name": "Decorative Accents",
            "url": "https://www.menards.com/main/grocery-home/decorative-accents/c-6921.htm",
        },
        "furniture": {
            "name": "Furniture",
            "url": "https://www.menards.com/main/grocery-home/furniture/c-7707.htm",
        },
        "health-beauty": {
            "name": "Health & Beauty",
            "url": "https://www.menards.com/main/grocery-home/health-beauty/c-19744.htm",
        },
        "home-accessibility": {
            "name": "Home Accessibility",
            "url": "https://www.menards.com/main/grocery-home/home-accessibility/c-12376.htm",
        },
        "household-essentials": {
            "name": "Household Essentials",
            "url": "https://www.menards.com/main/grocery-home/cleaners-household-essentials/household-essentials/c-14254.htm",
        },
        "laundry-care": {
            "name": "Laundry Care",
            "url": "https://www.menards.com/main/grocery-home/cleaners-household-essentials/laundry-care/c-14256.htm",
        },
        "menards-collectibles": {
            "name": "Menards Collectibles",
            "url": "https://www.menards.com/main/grocery-home/menards-collectibles/c-13317.htm",
        },
        "office-supplies": {
            "name": "Office Supplies",
            "url": "https://www.menards.com/main/grocery-home/office-supplies/c-7152.htm",
        },
        "toys-games": {
            "name": "Toys & Games",
            "url": "https://www.menards.com/main/grocery-home/toys-games/c-12325.htm",
        },
        "jewelry": {
            "name": "Jewelry",
            "url": "https://www.menards.com/main/grocery-home/jewelry/c-12797.htm",
        },
        "bedding": {
            "name": "Bedding",
            "url": "https://www.menards.com/main/grocery-home/bedding/c-1642874339328192.htm",
        },
    },
    "grocery": {
        "shop-all-grocery": {
            "name": "Shop All Grocery",
            "url": "https://www.menards.com/main/grocery-home/grocery/c-1552918768160.htm",
        },
        "baking-cooking-essentials": {
            "name": "Baking & Cooking Essentials",
            "url": "https://www.menards.com/main/grocery-home/grocery/baking-cooking-essentials/c-6621.htm",
        },
        "beverages": {
            "name": "Beverages",
            "url": "https://www.menards.com/main/grocery-home/grocery/beverages/c-6635.htm",
        },
        "bread": {
            "name": "Bread",
            "url": "https://www.menards.com/main/grocery-home/grocery/bread/c-6647.htm",
        },
        "canned-fruits-vegetables": {
            "name": "Canned Fruits & Vegetables",
            "url": "https://www.menards.com/main/grocery-home/grocery/canned-fruits-vegetables/c-5239772153260391.htm",
        },
        "canning-supplies": {
            "name": "Canning Supplies",
            "url": "https://www.menards.com/main/grocery-home/grocery/canning-supplies/c-1462209588021.htm",
        },
        "cereal-breakfast-food": {
            "name": "Cereal & Breakfast Food",
            "url": "https://www.menards.com/main/grocery-home/grocery/cereal-breakfast-food/c-6651.htm",
        },
        "concession-equipment": {
            "name": "Concession Equipment",
            "url": "https://www.menards.com/main/grocery-home/grocery/concession-equipment/c-13204.htm",
        },
        "condiments": {
            "name": "Condiments",
            "url": "https://www.menards.com/main/grocery-home/grocery/condiments/c-12342.htm",
        },
        "dairy": {
            "name": "Dairy",
            "url": "https://www.menards.com/main/grocery-home/grocery/dairy-eggs/c-1479303583387.htm",
        },
        "emergency-food": {
            "name": "Emergency Food",
            "url": "https://www.menards.com/main/grocery-home/grocery/emergency-food/c-13097.htm",
        },
        "frozen-foods": {
            "name": "Frozen Foods",
            "url": "https://www.menards.com/main/grocery-home/grocery/frozen-foods/c-13380.htm",
        },
        "packaged-meals-canned-meats-seafood": {
            "name": "Packaged Meals, Canned Meats & Seafood",
            "url": "https://www.menards.com/main/grocery-home/grocery/packaged-meals-canned-meats-seafood/c-14058.htm",
        },
        "pasta-sauces": {
            "name": "Pasta & Sauces",
            "url": "https://www.menards.com/main/grocery-home/grocery/pasta-sauces/c-1528988295731.htm",
        },
        "snack-food": {
            "name": "Snack Food",
            "url": "https://www.menards.com/main/grocery-home/grocery/snack-food/c-6687.htm",
        },
        "soups-broths": {
            "name": "Soups & Broths",
            "url": "https://www.menards.com/main/grocery-home/grocery/soups-broths/c-1528988295732.htm",
        },
    },
    "hardware": {
        "shop-all-hardware": {
            "name": "Shop All Hardware",
            "url": "https://www.menards.com/main/hardware/c-8693.htm",
        },
        "cabinet-hardware": {
            "name": "Cabinet Hardware",
            "url": "https://www.menards.com/main/hardware/cabinet-hardware/c-9341.htm",
        },
        "casters-furniture-hardware": {
            "name": "Casters & Furniture Hardware",
            "url": "https://www.menards.com/main/hardware/casters-furniture-hardware/c-13087.htm",
        },
        "fasteners-connectors": {
            "name": "Fasteners & Connectors",
            "url": "https://www.menards.com/main/hardware/fasteners-connectors/c-8706.htm",
        },
        "garage-door-parts-accessories": {
            "name": "Garage Door Parts & Accessories",
            "url": "https://www.menards.com/main/hardware/garage-door-parts-accessories/c-7577.htm",
        },
        "gate-hardware": {
            "name": "Gate Hardware",
            "url": "https://www.menards.com/main/hardware/gate-hardware/c-9691.htm",
        },
        "hand-knobs-handwheels": {
            "name": "Hand Knobs & Handwheels",
            "url": "https://www.menards.com/main/hardware/hand-knobs-handwheels/c-19659.htm",
        },
        "indoor-outdoor-signs": {
            "name": "Indoor/Outdoor Signs",
            "url": "https://www.menards.com/main/hardware/indoor-outdoor-signs/c-13840.htm",
        },
        "mailboxes-mailbox-posts": {
            "name": "Mailboxes & Mailbox Posts",
            "url": "https://www.menards.com/main/hardware/mailboxes-mailbox-posts/c-1482431821539.htm",
        },
        "ornamental-wood-ties": {
            "name": "Ornamental Wood Ties",
            "url": "https://www.menards.com/main/building-materials/decking-deck-products/ornamental-wood-ties/c-19116.htm",
        },
        "picture-mirror-hanging-hardware": {
            "name": "Picture & Mirror Hanging Hardware",
            "url": "https://www.menards.com/main/hardware/picture-mirror-hanging-hardware/c-13085.htm",
        },
        "safes": {
            "name": "Safes",
            "url": "https://www.menards.com/main/hardware/safes/c-7717.htm",
        },
        "sheet-metal-rods": {
            "name": "Sheet Metal & Rods",
            "url": "https://www.menards.com/main/hardware/sheet-metal-rods/c-9215.htm",
        },
        "tool-rental": {
            "name": "Tool Rental",
            "url": "https://www.menards.com/main/rental-equipment/c-13371.htm",
        },
        "utility-hardware": {
            "name": "Utility Hardware",
            "url": "https://www.menards.com/main/hardware/utility-hardware/c-9696.htm",
        },
    },
    "heating-cooling": {
        "shop-all-heating-cooling": {
            "name": "Shop All Heating & Cooling",
            "url": "https://www.menards.com/main/heating-cooling/c-6796.htm",
        },
        "air-conditioners-accessories": {
            "name": "Air Conditioners & Accessories",
            "url": "https://www.menards.com/main/heating-cooling/air-conditioners-accessories/c-1497103338431.htm",
        },
        "air-filters": {
            "name": "Air Filters",
            "url": "https://www.menards.com/main/heating-cooling/air-filters/c-6856.htm",
        },
        "air-purifiers-accessories": {
            "name": "Air Purifiers & Accessories",
            "url": "https://www.menards.com/main/heating-cooling/indoor-air-quality/air-purifiers-accessories/c-5614.htm",
        },
        "chimney-caps": {
            "name": "Chimney Caps",
            "url": "https://www.menards.com/main/heating-cooling/chimney-caps/c-6799.htm",
        },
        "dehumidifiers": {
            "name": "Dehumidifiers",
            "url": "https://www.menards.com/main/heating-cooling/dehumidifiers/c-1497103338432.htm",
        },
        "ductwork": {
            "name": "Ductwork",
            "url": "https://www.menards.com/main/heating-cooling/ductwork/c-6805.htm",
        },
        "fireplaces-stoves": {
            "name": "Fireplaces & Stoves",
            "url": "https://www.menards.com/main/heating-cooling/fireplaces-stoves/c-12883.htm",
        },
        "heat-energy-recovery-ventilators": {
            "name": "Heat & Energy Recovery Ventilators",
            "url": "https://www.menards.com/main/heating-cooling/indoor-air-quality/heat-energy-recovery-ventilators/c-3149259782980204.htm",
        },
        "heaters": {
            "name": "Heaters",
            "url": "https://www.menards.com/main/heating-cooling/heaters/c-6858.htm",
        },
        "humidifiers-diffusers-accessories": {
            "name": "Humidifiers, Diffusers & Accessories",
            "url": "https://www.menards.com/main/heating-cooling/indoor-air-quality/humidifiers-accessories/c-9507.htm",
        },
        "hydronic-radiant-heat": {
            "name": "Hydronic Radiant Heat",
            "url": "https://www.menards.com/main/plumbing/hydronic-radiant-heat/c-8517.htm",
        },
        "mini-split-air-conditioners": {
            "name": "Mini-Split Air Conditioners",
            "url": "https://www.menards.com/main/heating-cooling/mini-split-air-conditioners/c-1642874294161258.htm",
        },
        "portable-fans": {
            "name": "Portable Fans",
            "url": "https://www.menards.com/main/heating-cooling/portable-fans/c-12727.htm",
        },
        "propane-tanks": {
            "name": "Propane Tanks",
            "url": "https://www.menards.com/main/heating-cooling/propane-tanks/c-6878.htm",
        },
        "registers-grilles": {
            "name": "Registers & Grilles",
            "url": "https://www.menards.com/main/heating-cooling/registers-grilles/c-6879.htm",
        },
        "thermostats-freeze-alarms": {
            "name": "Thermostats & Freeze Alarms",
            "url": "https://www.menards.com/main/heating-cooling/thermostats-freeze-alarms/c-12864.htm",
        },
        "venting": {
            "name": "Venting",
            "url": "https://www.menards.com/main/heating-cooling/venting/c-6889.htm",
        },
        "indoor-air-quality": {
            "name": "Indoor Air Quality",
            "url": "https://www.menards.com/main/heating-cooling/indoor-air-quality/c-13880.htm",
        },
    },
    "holiday-decorations": {
        "halloween": {
            "name": "Halloween",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/c-12270.htm",
        },
        "christmas": {
            "name": "Christmas",
            "url": "https://www.menards.com/main/holiday-decorations/christmas/c-12282.htm",
        },
        "additional-holidays": {
            "name": "Additional Holidays",
            "url": "https://www.menards.com/main/holiday-decorations/easter-decorations/c-1550679444820.htm",
        },
        "thanksgiving-tablescape-ideas": {
            "name": "Thanksgiving Tablescape Ideas",
            "url": "https://www.menards.com/main/holiday-decorations/halloween/thanksgiving-tablescape-ideas/c-1507315087973.htm",
        },
        "fall-decor": {
            "name": "Fall Decor",
            "url": "https://www.menards.com/main/holiday-decorations/fall-decor/c-1642874317166386.htm",
        },
    },
    "kitchen": {
        "shop-all-kitchen": {
            "name": "Shop All Kitchen",
            "url": "https://www.menards.com/main/kitchen/c-7200.htm",
        },
        "backsplashes-wall-tiles": {
            "name": "Backsplashes & Wall Tiles",
            "url": "https://www.menards.com/main/kitchen/backsplashes-wall-tiles/c-8163.htm",
        },
        "bar-equipment-cocktail-stations": {
            "name": "Bar Equipment & Cocktail Stations",
            "url": "https://www.menards.com/main/kitchen/bar-equipment-cocktail-stations/c-14187.htm",
        },
        "cabinet-organization-accessories": {
            "name": "Cabinet Organization & Accessories",
            "url": "https://www.menards.com/main/kitchen/cabinet-organization-accessories/c-9348.htm",
        },
        "cabinet-store": {
            "name": "Cabinet Store",
            "url": "https://www.menards.com/main/landing-pages/cabinet-store/c-60892455609.htm",
        },
        "countertops": {
            "name": "Countertops",
            "url": "https://www.menards.com/main/kitchen/countertops-laminate/c-14116.htm",
        },
        "garbage-disposals": {
            "name": "Garbage Disposals",
            "url": "https://www.menards.com/main/kitchen/garbage-disposals/c-8508.htm",
        },
        "hot-water-dispensers": {
            "name": "Hot Water Dispensers",
            "url": "https://www.menards.com/main/kitchen/hot-water-dispensers/c-8677.htm",
        },
        "kitchen-cabinets": {
            "name": "Kitchen Cabinets",
            "url": "https://www.menards.com/main/kitchen/kitchen-cabinets/c-12410.htm",
        },
        "kitchen-essentials": {
            "name": "Kitchen Essentials",
            "url": "https://www.menards.com/main/kitchen/kitchen-essentials/c-7249.htm",
        },
        "kitchen-faucets": {
            "name": "Kitchen Faucets",
            "url": "https://www.menards.com/main/kitchen/kitchen-faucets/c-8509.htm",
        },
        "kitchen-sinks": {
            "name": "Kitchen Sinks",
            "url": "https://www.menards.com/main/kitchen/kitchen-sinks/c-1451416484953.htm",
        },
        "restaurant-supplies": {
            "name": "Restaurant Supplies",
            "url": "https://www.menards.com/main/kitchen/restaurant-supplies/c-6202.htm",
        },
        "sink-sprayers-strainer-baskets": {
            "name": "Sink Sprayers & Strainer Baskets",
            "url": "https://www.menards.com/main/kitchen/sink-sprayers-strainer-baskets/c-8506.htm",
        },
    },
    "lawn-garden": {
        "shop-all-lawn-garden": {
            "name": "Shop All Lawn & Garden",
            "url": "https://www.menards.com/main/bath/c-4324230408371061.htm",
        },
        "gardening": {
            "name": "Gardening",
            "url": "https://www.menards.com/main/outdoors/gardening/c-12577.htm",
        },
        "insect-pest-control": {
            "name": "Insect & Pest Control",
            "url": "https://www.menards.com/main/outdoors/insect-pest-control/c-10117.htm",
        },
        "outdoor-power-equipment": {
            "name": "Outdoor Power Equipment",
            "url": "https://www.menards.com/main/outdoors/outdoor-power-equipment/c-10104.htm",
        },
        "planters-hanging-basket-accessories": {
            "name": "Planters & Hanging Basket Accessories",
            "url": "https://www.menards.com/main/outdoors/planters-hanging-basket-accessories/c-2654092911144963.htm",
        },
        "planters-hanging-baskets": {
            "name": "Planters & Hanging Baskets",
            "url": "https://www.menards.com/main/outdoors/planters-hanging-baskets/c-10138.htm",
        },
        "snow-ice-removal": {
            "name": "Snow & Ice Removal",
            "url": "https://www.menards.com/main/outdoors/snow-ice-removal/c-12409.htm",
        },
        "watering-irrigation": {
            "name": "Watering & Irrigation",
            "url": "https://www.menards.com/main/outdoors/watering-irrigation/c-8648.htm",
        },
    },
    "lighting-ceiling-fans": {
        "ceiling-fans": {
            "name": "Ceiling Fans",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/ceiling-fans/c-7483.htm",
        },
        "flashlights-accessories": {
            "name": "Flashlights & Accessories",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/flashlights-accessories/c-6314.htm",
        },
        "indoor-lighting": {
            "name": "Indoor Lighting",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/indoor-lighting/c-7489.htm",
        },
        "lighting-collections": {
            "name": "Lighting Collections",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/indoor-lighting/lighting-collections/c-1462309966110.htm",
        },
        "lighting-deals": {
            "name": "Lighting Deals",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/lighting-deals/c-1642874315059063.htm",
        },
        "lighting-hardware-accessories": {
            "name": "Lighting Hardware & Accessories",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/lighting-hardware-accessories/c-7516.htm",
        },
        "novelty-lights": {
            "name": "Novelty Lights",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/indoor-lighting/novelty-lights/c-7501.htm",
        },
        "outdoor-lighting": {
            "name": "Outdoor Lighting",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/outdoor-lighting/c-7528.htm",
        },
        "replacement-glass-shades": {
            "name": "Replacement Glass & Shades",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/replacement-glass-shades/c-7509.htm",
        },
        "rope-string-lights": {
            "name": "Rope & String Lights",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/outdoor-lighting/rope-string-lights/c-14318.htm",
        },
        "shop-all-lighting-ceiling-fans": {
            "name": "Shop All Lighting & Ceiling Fans",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/c-7476.htm",
        },
        "shop-all-patriot-lighting": {
            "name": "Shop All Patriot Lighting",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/shop-all-patriot-lighting/c-1642874323006033.htm",
        },
        "utility-commercial-lighting": {
            "name": "Utility & Commercial Lighting",
            "url": "https://www.menards.com/main/lighting-ceiling-fans/Utility-Commercial-Lighting/c-1642874277599006.htm",
        },
    },
    "outdoor-living-patio": {
        "shop-all-outdoor-living-patio": {
            "name": "Shop All Outdoor Living & Patio",
            "url": "https://www.menards.com/main/outdoors/c-7727.htm",
        },
        "address-numbers-letters": {
            "name": "Address Numbers & Letters",
            "url": "https://www.menards.com/main/outdoors/outdoor-decor/address-numbers-letters/c-10139.htm",
        },
        "docks-accessories": {
            "name": "Docks & Accessories",
            "url": "https://www.menards.com/main/outdoors/docks-dock-accessories/c-19470.htm",
        },
        "fire-pits-outdoor-heating": {
            "name": "Fire Pits & Outdoor Heating",
            "url": "https://www.menards.com/main/outdoors/fire-pits-outdoor-heating/c-12918.htm",
        },
        "grills-outdoor-cooking": {
            "name": "Grills & Outdoor Cooking",
            "url": "https://www.menards.com/main/outdoors/grills-outdoor-cooking/c-13365.htm",
        },
        "master-garden": {
            "name": "Master Garden",
            "url": "https://www.menards.com/main/master-garden/c-1841405561305173.htm",
        },
        "outdoor-decor": {
            "name": "Outdoor Decor",
            "url": "https://www.menards.com/main/outdoors/outdoor-decor/c-13140.htm",
        },
        "outdoor-recreation-sports": {
            "name": "Outdoor Recreation & Sports",
            "url": "https://www.menards.com/main/outdoors/outdoor-recreation-sports/c-13175.htm",
        },
        "patio-furniture": {
            "name": "Patio Furniture",
            "url": "https://www.menards.com/main/outdoors/patio-furniture/c-10136.htm",
        },
        "patio-structures": {
            "name": "Patio Structures",
            "url": "https://www.menards.com/main/outdoors/patio-structures/c-7556.htm",
        },
        "pools-accessories": {
            "name": "Pools & Accessories",
            "url": "https://www.menards.com/main/outdoors/pools-accessories/c-10137.htm",
        },
        "spas-saunas": {
            "name": "Spas & Saunas",
            "url": "https://www.menards.com/main/outdoors/pools-spas-saunas/c-7846.htm",
        },
        "swing-sets-playsets": {
            "name": "Swing Sets & Playsets",
            "url": "https://www.menards.com/main/outdoors/swing-sets-playsets/c-9592.htm",
        },
    },
    "paint": {
        "shop-all-paint": {
            "name": "Shop All Paint",
            "url": "https://www.menards.com/main/paint/c-7918.htm",
        },
        "adhesives-glue-tape": {
            "name": "Adhesives, Glue & Tape",
            "url": "https://www.menards.com/main/paint/adhesives-glue-tape/c-7919.htm",
        },
        "caulks-sealants": {
            "name": "Caulks & Sealants",
            "url": "https://www.menards.com/main/paint/caulks-sealants/c-7929.htm",
        },
        "ceiling-tiles-grid-systems-planks-accessories": {
            "name": "Ceiling Tiles, Grid Systems, Planks & Accessories",
            "url": "https://www.menards.com/main/paint/ceilings/c-7938.htm",
        },
        "cleaners-thinners-removers": {
            "name": "Cleaners, Thinners & Removers",
            "url": "https://www.menards.com/main/paint/cleaners-thinners-removers/c-8152.htm",
        },
        "concrete-blacktop-sealers": {
            "name": "Concrete & Blacktop Sealers",
            "url": "https://www.menards.com/main/paint/concrete-blacktop-sealers/c-8189.htm",
        },
        "exterior-paint": {
            "name": "Exterior Paint",
            "url": "https://www.menards.com/main/paint/exterior-paint-stain/c-8005.htm",
        },
        "exterior-wood-stain": {
            "name": "Exterior Wood Stain",
            "url": "https://www.menards.com/main/paint/exterior-paint-stain/exterior-wood-stains/c-7954.htm",
        },
        "interior-paint": {
            "name": "Interior Paint",
            "url": "https://www.menards.com/main/paint/interior-paint-stain/c-8015.htm",
        },
        "interior-wood-stain": {
            "name": "Interior Wood Stain",
            "url": "https://www.menards.com/main/paint/interior-paint-stain/interior-stain/c-7968.htm",
        },
        "ladders-scaffolding": {
            "name": "Ladders & Scaffolding",
            "url": "https://www.menards.com/main/paint/ladders-scaffolding/c-7975.htm",
        },
        "paint-additives": {
            "name": "Paint Additives",
            "url": "https://www.menards.com/main/paint/interior-paint-stain/paint-additives/c-8034.htm",
        },
        "paint-sprayers-applicators": {
            "name": "Paint Sprayers & Applicators",
            "url": "https://www.menards.com/main/paint/paint-sprayers-applicators/c-8088.htm",
        },
        "painting-protection": {
            "name": "Painting Protection",
            "url": "https://www.menards.com/main/paint/painting-protection/c-8058.htm",
        },
        "painting-tools": {
            "name": "Painting Tools",
            "url": "https://www.menards.com/main/paint/painting-tools/c-8076.htm",
        },
        "primers-sealers": {
            "name": "Primers & Sealers",
            "url": "https://www.menards.com/main/paint/interior-paint-stain/primers-sealers/c-8028.htm",
        },
        "sandpaper-abrasives": {
            "name": "Sandpaper & Abrasives",
            "url": "https://www.menards.com/main/paint/sandpaper-abrasives/c-8190.htm",
        },
        "spray-paint": {
            "name": "Spray Paint",
            "url": "https://www.menards.com/main/paint/spray-paint/c-8041.htm",
        },
        "wallpaper-appliques": {
            "name": "Wallpaper & Appliques",
            "url": "https://www.menards.com/main/home-decor/wallpaper-appliques/c-8228.htm",
        },
    },
    "pet-wildlife": {
        "shop-all-pet-wildlife": {
            "name": "Shop All Pet & Wildlife",
            "url": "https://www.menards.com/main/pet-wildlife/c-19743.htm",
        },
        "bird-wildlife-supplies": {
            "name": "Bird & Wildlife Supplies",
            "url": "https://www.menards.com/main/pet-wildlife/bird-wildlife-supplies/c-7865.htm",
        },
        "cat-supplies": {
            "name": "Cat Supplies",
            "url": "https://www.menards.com/main/pet-wildlife/cat-supplies/c-8280.htm",
        },
        "dog-supplies": {
            "name": "Dog Supplies",
            "url": "https://www.menards.com/main/pet-wildlife/dog-supplies/c-8297.htm",
        },
        "pet-bird-fish-supplies": {
            "name": "Pet Bird & Fish Supplies",
            "url": "https://www.menards.com/main/pet-wildlife/pet-bird-fish-supplies/c-8340.htm",
        },
        "pet-food-bowls-food-storage-mats": {
            "name": "Pet Food Bowls, Food Storage & Mats",
            "url": "https://www.menards.com/main/pet-wildlife/pet-food-bowls-food-storage-mats/c-8330.htm",
        },
        "stock-tank-deicers": {
            "name": "Stock Tank Deicers",
            "url": "https://www.menards.com/main/pet-wildlife/stock-tank-deicers/c-9558.htm",
        },
        "poultry-feed-supplies": {
            "name": "Poultry Feed & Supplies",
            "url": "https://www.menards.com/main/pet-wildlife/poultry-feed-supplies/c-1642874349488496.htm",
        },
    },
    "plumbing": {
        "shop-all-plumbing": {
            "name": "Shop All Plumbing",
            "url": "https://www.menards.com/main/plumbing/c-8342.htm",
        },
        "drain-cleaning-tools": {
            "name": "Drain Cleaning Tools",
            "url": "https://www.menards.com/main/plumbing/drain-cleaning-tools/c-8512.htm",
        },
        "faucets": {
            "name": "Faucets",
            "url": "https://www.menards.com/main/plumbing/faucets/c-12340.htm",
        },
        "hoses-tubing": {
            "name": "Hoses & Tubing",
            "url": "https://www.menards.com/main/plumbing/hoses-tubing/c-1463242261165.htm",
        },
        "pipe-fittings": {
            "name": "Pipe & Fittings",
            "url": "https://www.menards.com/main/plumbing/pipe-fittings/c-1463242261164.htm",
        },
        "pipe-insulation-heat-cables": {
            "name": "Pipe Insulation & Heat Cables",
            "url": "https://www.menards.com/main/plumbing/pipe-insulation-heat-cables/c-8586.htm",
        },
        "plumbing-installation-repair": {
            "name": "Plumbing Installation & Repair",
            "url": "https://www.menards.com/main/plumbing/plumbing-installation-repair/c-8524.htm",
        },
        "plumbing-tools": {
            "name": "Plumbing Tools",
            "url": "https://www.menards.com/main/plumbing/plumbing-tools/c-1463242261168.htm",
        },
        "pumps-tanks": {
            "name": "Pumps & Tanks",
            "url": "https://www.menards.com/main/plumbing/pumps-tanks/c-8671.htm",
        },
        "sinks": {
            "name": "Sinks",
            "url": "https://www.menards.com/main/plumbing/sinks/c-13048.htm",
        },
        "utility-sinks-accessories": {
            "name": "Utility Sinks & Accessories",
            "url": "https://www.menards.com/main/plumbing/utility-sinks-accessories/c-9447.htm",
        },
        "valves": {
            "name": "Valves",
            "url": "https://www.menards.com/main/plumbing/valves/c-1463242261167.htm",
        },
        "water-filtration-softeners": {
            "name": "Water Filtration & Softeners",
            "url": "https://www.menards.com/main/plumbing/water-filtration-softeners/c-12822.htm",
        },
        "water-heaters": {
            "name": "Water Heaters",
            "url": "https://www.menards.com/main/plumbing/water-heaters/c-8686.htm",
        },
    },
    "storage-organization": {
        "shop-all-storage-organization": {
            "name": "Shop All Storage & Organization",
            "url": "https://www.menards.com/main/storage-organization/c-12633.htm",
        },
        "closet-organizers": {
            "name": "Closet Organizers",
            "url": "https://www.menards.com/main/storage-organization/closet-organizers/c-12634.htm",
        },
        "dakota": {
            "name": "Dakota",
            "url": "https://www.menards.com/main/brands/dakota/c-13978.htm",
        },
        "garage-outdoor-storage": {
            "name": "Garage & Outdoor Storage",
            "url": "https://www.menards.com/main/storage-organization/garage-outdoor-storage/c-12635.htm",
        },
        "kitchen-cabinets-organizers-food-storage": {
            "name": "Kitchen Cabinets, Organizers & Food Storage",
            "url": "https://www.menards.com/main/kitchen/kitchen-cabinets-organizers-food-storage/c-12639.htm",
        },
        "laundry-organizers": {
            "name": "Laundry Organizers",
            "url": "https://www.menards.com/main/storage-organization/laundry-organizers/c-12641.htm",
        },
        "shelves-shelving-units": {
            "name": "Shelves & Shelving Units",
            "url": "https://www.menards.com/main/storage-organization/shelves-shelving-units/c-12636.htm",
        },
        "shoe-racks-organizers": {
            "name": "Shoe Racks & Organizers",
            "url": "https://www.menards.com/main/storage-organization/closet-organizers/shoe-racks-organizers/c-12647.htm",
        },
        "storage-cubes-drawers": {
            "name": "Storage Cubes & Drawers",
            "url": "https://www.menards.com/main/storage-organization/shelves-shelving-units/storage-cubes-drawers/c-12646.htm",
        },
        "storage-totes-bins": {
            "name": "Storage Totes & Bins",
            "url": "https://www.menards.com/main/storage-organization/storage-totes-bins/c-12637.htm",
        },
        "tool-chests": {
            "name": "Tool Chests",
            "url": "https://www.menards.com/main/tools/tool-storage/tool-chests/c-9188.htm",
        },
    },
    "tools": {
        "shop-all-tools": {
            "name": "Shop All Tools",
            "url": "https://www.menards.com/main/tools/c-13067.htm",
        },
        "air-compressors-tools": {
            "name": "Air Compressors & Tools",
            "url": "https://www.menards.com/main/tools/power-tools/pneumatic-tools/c-9076.htm",
        },
        "concrete-masonry-tools": {
            "name": "Concrete & Masonry Tools",
            "url": "https://www.menards.com/main/tools/hand-tools/concrete-masonry-tools/c-8954.htm",
        },
        "drywall-tools": {
            "name": "Drywall Tools",
            "url": "https://www.menards.com/main/tools/hand-tools/drywall-tools/c-8951.htm",
        },
        "flooring-tools": {
            "name": "Flooring Tools",
            "url": "https://www.menards.com/main/tools/flooring-tools/c-1470857353466.htm",
        },
        "hand-carts-trucks-dollies": {
            "name": "Hand Carts, Trucks & Dollies",
            "url": "https://www.menards.com/main/tools/hand-carts-trucks-dollies/c-12175.htm",
        },
        "hand-tools": {
            "name": "Hand Tools",
            "url": "https://www.menards.com/main/tools/hand-tools/c-8950.htm",
        },
        "masterforce": {
            "name": "Masterforce",
            "url": "https://www.menards.com/main/brands/masterforce/c-13923.htm",
        },
        "measuring-layout-tools": {
            "name": "Measuring & Layout Tools",
            "url": "https://www.menards.com/main/tools/hand-tools/measuring-layout-tools/c-9149.htm",
        },
        "power-tool-accessories": {
            "name": "Power Tool Accessories",
            "url": "https://www.menards.com/main/tools/power-tool-accessories/c-10078.htm",
        },
        "power-tools": {
            "name": "Power Tools",
            "url": "https://www.menards.com/main/tools/power-tools/c-9033.htm",
        },
        "roofing-tools": {
            "name": "Roofing Tools",
            "url": "https://www.menards.com/main/tools/roofing-tools/c-13081.htm",
        },
        "siding-tools": {
            "name": "Siding Tools",
            "url": "https://www.menards.com/main/building-materials/siding/siding-tools/c-13071.htm",
        },
        "tile-installation-tools": {
            "name": "Tile Installation Tools",
            "url": "https://www.menards.com/main/flooring-rugs/tile-stone/tile-installation-maintenance/tile-installation-tools/c-6599.htm",
        },
        "tool-storage": {
            "name": "Tool Storage",
            "url": "https://www.menards.com/main/tools/tool-storage/c-9185.htm",
        },
        "torches-soldering-tools": {
            "name": "Torches & Soldering Tools",
            "url": "https://www.menards.com/main/tools/torches-soldering-tools/c-8533.htm",
        },
        "welders-accessories": {
            "name": "Welders & Accessories",
            "url": "https://www.menards.com/main/tools/welders-accessories/c-10163.htm",
        },
        "wet-dry-vacuums-accessories": {
            "name": "Wet/Dry Vacuums & Accessories",
            "url": "https://www.menards.com/main/tools/wet-dry-vacuums-accessories/c-10092.htm",
        },
        "workwear-safety-gear": {
            "name": "Workwear & Safety Gear",
            "url": "https://www.menards.com/main/tools/workwear-safety-gear/c-13834.htm",
        },
    },
    "window-treatments": {
        "shop-all-window-treatments": {
            "name": "Shop All Window Treatments",
            "url": "https://www.menards.com/main/window-treatments/c-9225.htm",
        },
        "blind-cleaners": {
            "name": "Blind Cleaners",
            "url": "https://www.menards.com/main/window-treatments/blind-cleaners/c-9263.htm",
        },
        "blinds-shades": {
            "name": "Blinds & Shades",
            "url": "https://www.menards.com/main/window-treatments/blinds-shades/c-9229.htm",
        },
        "curtain-drapery-hardware": {
            "name": "Curtain & Drapery Hardware",
            "url": "https://www.menards.com/main/window-treatments/curtains-drapery-hardware/c-9260.htm",
        },
        "curtains-drapes": {
            "name": "Curtains & Drapes",
            "url": "https://www.menards.com/main/window-treatments/curtains-drapes/c-9261.htm",
        },
        "custom-blinds-shades": {
            "name": "Custom Blinds & Shades",
            "url": "https://www.menards.com/main/window-treatments/custom-blinds-shades/c-9237.htm",
        },
        "custom-interior-shutters": {
            "name": "Custom Interior Shutters",
            "url": "https://www.menards.com/main/window-treatments/custom-interior-shutters/c-13566.htm",
        },
        "interior-shutters": {
            "name": "Interior Shutters",
            "url": "https://www.menards.com/main/window-treatments/interior-shutters/c-14051.htm",
        },
        "window-film-appliques": {
            "name": "Window Film & Appliques",
            "url": "https://www.menards.com/main/window-treatments/window-film-appliques/c-9262.htm",
        },
    },
    "sale-items": {
        "shop-all-sale-items": {
            "name": "Shop All Sale Items",
            "url": "https://www.menards.com/main/c-1642874320226744.htm",
        },
        "appliances-sale-items": {
            "name": "Appliances - Sale Items",
            "url": "https://www.menards.com/main/sale-items/appliances-sale-items/c-1642874323047993.htm",
        },
        "bath-sale-items": {
            "name": "Bath - Sale Items",
            "url": "https://www.menards.com/main/sale-items/bath-sale-items/c-1642874323047999.htm",
        },
        "building-materials-sale-items": {
            "name": "Building Materials -Sale Items",
            "url": "https://www.menards.com/main/sale-items/building-materials-sale-items/c-1642874323047992.htm",
        },
        "clothing-sale-items": {
            "name": "Clothing - Sale Items",
            "url": "https://www.menards.com/main/sale-items/clothing-sale-items/c-1642874323051002.htm",
        },
        "doors-on-sale": {
            "name": "Doors on Sale",
            "url": "https://www.menards.com/main/sale-items/doors-on-sale/c-1642874326714314.htm",
        },
        "flooring-sale-items": {
            "name": "Flooring - Sale Items",
            "url": "https://www.menards.com/main/sale-items/flooring-sale-items/c-1642874323047998.htm",
        },
        "furniture-home-sale-items": {
            "name": "Furniture & Home - Sale Items",
            "url": "https://www.menards.com/main/sale-items/furniture-home-sale-items/c-1642874323088728.htm",
        },
        "kitchen-sale-items": {
            "name": "Kitchen - Sale Items",
            "url": "https://www.menards.com/main/sale-items/kitchen-sale-items/c-1642874323097773.htm",
        },
        "lighting-sale-items": {
            "name": "Lighting - Sale Items",
            "url": "https://www.menards.com/main/sale-items/lighting-sale-items/c-1642874323047996.htm",
        },
        "outdoors-sale-items": {
            "name": "Outdoors - Sale Items",
            "url": "https://www.menards.com/main/sale-items/outdoors-sale-items/c-1642874323047995.htm",
        },
        "paint-sale-items": {
            "name": "Paint - Sale Items",
            "url": "https://www.menards.com/main/sale-items/paint-sale-items/c-1642874323051003.htm",
        },
        "pet-supplies-sale-items": {
            "name": "Pet Supplies - Sale Items",
            "url": "https://www.menards.com/main/sale-items/pet-supplies-sale-items/c-1642874323051001.htm",
        },
        "tools-hardware-sale-items": {
            "name": "Tools & Hardware - Sale Items",
            "url": "https://www.menards.com/main/sale-items/tools-hardware-sale-items/c-1642874323047994.htm",
        },
        "toys-sale-items": {
            "name": "Toys - Sale Items",
            "url": "https://www.menards.com/main/sale-items/toys-sale-items/c-1642874323047997.htm",
        },
    },
}
