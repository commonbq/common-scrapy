"""Lowe's complete, live department -> subcategory inventory.

Captured 2026-10-15 from Lowe's server-rendered Departments taxonomy
(https://www.lowes.com/c/Departments), ``window['__PRELOADED_STATE__'].taxonomy.departments``.
That payload is the storefront's own navigation tree: 32 departments and
359 product-bearing subcategories. Every subcategory is a runnable crawl
target -- its ``/pl/<slug>/<id>`` (or ``/c/<slug>``) page hydrates the
``itemList`` product records the spider reads (verified live: the
Beverage & Wine Chillers leaf returned 24 ``itemList`` records).

Grouped ``{department: {leaf: {name, department, url}}}`` mapping as
required by the base listing-spider contract. Leaf keys are the cleaned
storefront path slug, which is globally unique across departments (so the
Airflow task ids and GCS output paths cannot collide).
``-a category=<department name>`` expands to every leaf in that department
through the base-class parent-selector support.
"""

LOWES_CATEGORIES = {
    "Accessible Home": {
        "accessible-bathroom-accessible-home": {
            "name": "Accessible Bathroom",
            "department": "Accessible Home",
            "url": "https://www.lowes.com/pl/Accessible-bathroom-Accessible-home/37721669146437",
        },
        "accessible-bedroom-accessible-home": {
            "name": "Accessible Bedroom",
            "department": "Accessible Home",
            "url": "https://www.lowes.com/pl/Accessible-bedroom-Accessible-home/4294644781",
        },
        "accessible-entry-home-accessible-home": {
            "name": "Accessible Entry & Home",
            "department": "Accessible Home",
            "url": "https://www.lowes.com/pl/Accessible-entry-home-Accessible-home/37721669146444",
        },
        "accessible-kitchen-accessible-home": {
            "name": "Accessible Kitchen",
            "department": "Accessible Home",
            "url": "https://www.lowes.com/pl/Accessible-kitchen-Accessible-home/1111913019980",
        },
        "daily-assistance-accessible-home": {
            "name": "Daily Assistance",
            "department": "Accessible Home",
            "url": "https://www.lowes.com/pl/Daily-assistance-Accessible-home/4294644797",
        },
        "injury-relief-physical-therapy-accessible-home": {
            "name": "Injury Relief & Physical Therapy",
            "department": "Accessible Home",
            "url": "https://www.lowes.com/pl/Injury-relief-physical-therapy-Accessible-home/4294644776",
        },
        "wheelchairs-mobility-aids-accessible-home": {
            "name": "Wheelchairs & Mobility Aids",
            "department": "Accessible Home",
            "url": "https://www.lowes.com/pl/Wheelchairs-mobility-aids-Accessible-home/4294644793",
        },
    },
    "Animal & Pet Care": {
        "livestock-supplies-animal-pet-care": {
            "name": "Livestock Supplies",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Livestock-supplies-Animal-pet-care/1697941494",
        },
        "pet-beds-houses-furniture-animal-pet-care": {
            "name": "Pet Beds, Houses, & Furniture",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-beds-houses-furniture-Animal-pet-care/2544332199",
        },
        "pet-cleaning-waste-supplies-animal-pet-care": {
            "name": "Pet Cleaning & Waste Supplies",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-cleaning-waste-supplies-Animal-pet-care/2318112555",
        },
        "pet-clippers-scissors-brushes-animal-pet-care": {
            "name": "Pet Clippers, Scissors & Brushes",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-clippers-scissors-brushes-Animal-pet-care/3121493845732",
        },
        "pet-clothing-accessories-animal-pet-care": {
            "name": "Pet Clothing & Accessories",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-clothing-accessories-Animal-pet-care/2921724317701",
        },
        "pet-doors-gates-animal-pet-care": {
            "name": "Pet Doors & Gates",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-doors-gates-Animal-pet-care/4294610550",
        },
        "pet-feeding-supplies-animal-pet-care": {
            "name": "Pet Feeding Supplies",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-feeding-supplies-Animal-pet-care/2510803352",
        },
        "pet-fencing-training-animal-pet-care": {
            "name": "Pet Fencing & Training",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-fencing-training-Animal-pet-care/3583519698",
        },
        "pet-grooming-health-animal-pet-care": {
            "name": "Pet Grooming & Health",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-grooming-health-Animal-pet-care/4294610546",
        },
        "pet-kennels-crates-animal-pet-care": {
            "name": "Pet Kennels & Crates",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-kennels-crates-Animal-pet-care/778128516",
        },
        "pet-leashes-collars-harnesses-animal-pet-care": {
            "name": "Pet Leashes, Collars & Harnesses",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-leashes-collars-harnesses-Animal-pet-care/4233103602",
        },
        "pet-toys-treats-animal-pet-care": {
            "name": "Pet Toys & Treats",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-toys-treats-Animal-pet-care/4294610530",
        },
        "pet-travel-transportation-animal-pet-care": {
            "name": "Pet Travel & Transportation",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-travel-transportation-Animal-pet-care/2620088367057",
        },
        "pet-vitamins-supplements-animal-pet-care": {
            "name": "Pet Vitamins & Supplements",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Pet-vitamins-supplements-Animal-pet-care/2620555201638",
        },
        "terrariums-habitats-animal-pet-care": {
            "name": "Terrariums & Habitats",
            "department": "Animal & Pet Care",
            "url": "https://www.lowes.com/pl/Terrariums-habitats-Animal-pet-care/2311219941942",
        },
    },
    "Appliances": {
        "appliance-parts-accessories-appliances": {
            "name": "Appliance Parts & Accessories",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Appliance-parts-accessories-Appliances",
        },
        "beverage-wine-chillers-appliances": {
            "name": "Beverage & Wine Chillers",
            "department": "Appliances",
            "url": "https://www.lowes.com/pl/Beverage-wine-chillers-Appliances/2352008713",
        },
        "commercial-appliances-appliances": {
            "name": "Commercial Appliances",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Commercial-appliances-Appliances",
        },
        "cooktops-appliances": {
            "name": "Cooktops",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Cooktops-Appliances",
        },
        "crafting-machines-accessories-appliances": {
            "name": "Crafting Machines & Accessories",
            "department": "Appliances",
            "url": "https://www.lowes.com/pl/Crafting-machines-accessories-Appliances/37721669146480",
        },
        "dishwashers-appliances": {
            "name": "Dishwashers",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Dishwashers-Appliances",
        },
        "freezers-appliances": {
            "name": "Freezers",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Freezers-Appliances",
        },
        "garbage-disposals-appliances": {
            "name": "Garbage Disposals",
            "department": "Appliances",
            "url": "https://www.lowes.com/pl/Garbage-disposals-Appliances/4294639585",
        },
        "ice-makers-appliances": {
            "name": "Ice Makers",
            "department": "Appliances",
            "url": "https://www.lowes.com/pl/Ice-makers-Appliances/4294796261",
        },
        "kitchen-appliance-packages-appliances": {
            "name": "Kitchen Appliance Packages",
            "department": "Appliances",
            "url": "https://www.lowes.com/pl/Kitchen-appliance-packages-Appliances/2020942007672",
        },
        "kitchenettes-appliances": {
            "name": "Kitchenettes",
            "department": "Appliances",
            "url": "https://www.lowes.com/pl/Kitchenettes-Appliances/1511792640827",
        },
        "microwaves-appliances": {
            "name": "Microwaves",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Microwaves-Appliances",
        },
        "range-hoods-appliances": {
            "name": "Range Hoods",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Range-hoods-Appliances",
        },
        "ranges-appliances": {
            "name": "Ranges",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Ranges-Appliances",
        },
        "refrigerators-appliances": {
            "name": "Refrigerators",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Refrigerators-Appliances",
        },
        "sewing-machines-accessories-appliances": {
            "name": "Sewing Machines & Accessories",
            "department": "Appliances",
            "url": "https://www.lowes.com/pl/Sewing-machines-accessories-Appliances/37721669146479",
        },
        "small-appliances-appliances": {
            "name": "Small Appliances",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Small-appliances-Appliances",
        },
        "trash-compactors-appliances": {
            "name": "Trash Compactors",
            "department": "Appliances",
            "url": "https://www.lowes.com/pl/Trash-compactors-Appliances/4294639583",
        },
        "vacuum-cleaners-floor-care-appliances": {
            "name": "Vacuum Cleaners & Floor Care",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Vacuum-cleaners-floor-care-Appliances",
        },
        "wall-ovens-appliances": {
            "name": "Wall Ovens",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Wall-ovens-Appliances",
        },
        "washers-dryers-appliances": {
            "name": "Washers & Dryers",
            "department": "Appliances",
            "url": "https://www.lowes.com/c/Washers-dryers-Appliances",
        },
        "water-coolers-pitchers-appliances": {
            "name": "Water Coolers & Pitchers",
            "department": "Appliances",
            "url": "https://www.lowes.com/pl/Water-coolers-pitchers-Appliances/479649473",
        },
    },
    "Automotive": {
        "autobody-parts-mirrors-automotive": {
            "name": "Autobody Parts & Mirrors",
            "department": "Automotive",
            "url": "https://www.lowes.com/pl/Autobody-parts-mirrors-Automotive/2011320042600",
        },
        "automotive-care-cleaning-automotive": {
            "name": "Automotive Care & Cleaning",
            "department": "Automotive",
            "url": "https://www.lowes.com/pl/Automotive-care-cleaning-Automotive/4294642659",
        },
        "automotive-exterior-accessories-automotive": {
            "name": "Automotive Exterior Accessories",
            "department": "Automotive",
            "url": "https://www.lowes.com/pl/Automotive-exterior-accessories-Automotive/2411820450012",
        },
        "automotive-hardware-automotive": {
            "name": "Automotive Hardware",
            "department": "Automotive",
            "url": "https://www.lowes.com/pl/Automotive-hardware-Automotive/4294644699",
        },
        "automotive-interior-accessories-automotive": {
            "name": "Automotive Interior Accessories",
            "department": "Automotive",
            "url": "https://www.lowes.com/pl/Automotive-interior-accessories-Automotive/4294644698",
        },
        "automotive-lighting-electrical-automotive": {
            "name": "Automotive Lighting & Electrical",
            "department": "Automotive",
            "url": "https://www.lowes.com/pl/Automotive-lighting-electrical-Automotive/2410166515848",
        },
        "automotive-oils-fluids-automotive": {
            "name": "Automotive Oils & Fluids",
            "department": "Automotive",
            "url": "https://www.lowes.com/pl/Automotive-oils-fluids-Automotive/4294542211",
        },
        "automotive-tools-equipment-automotive": {
            "name": "Automotive Tools & Equipment",
            "department": "Automotive",
            "url": "https://www.lowes.com/pl/Automotive-tools-equipment-Automotive/2772213972",
        },
        "electric-vehicle-charging-equipment-automotive": {
            "name": "Electric Vehicle Charging Equipment",
            "department": "Automotive",
            "url": "https://www.lowes.com/pl/Electric-vehicle-charging-equipment-Automotive/2610766954329",
        },
        "spark-plugs-automotive": {
            "name": "Spark Plugs",
            "department": "Automotive",
            "url": "https://www.lowes.com/pl/Spark-plugs-Automotive/4294641547",
        },
        "truck-towing-automotive": {
            "name": "Truck & Towing",
            "department": "Automotive",
            "url": "https://www.lowes.com/pl/Truck-towing-Automotive/2247165814",
        },
    },
    "Bathroom": {
        "bathroom-pedestal-sinks-bathroom": {
            "name": "Bathroom & Pedestal Sinks",
            "department": "Bathroom",
            "url": "https://www.lowes.com/c/Bathroom-pedestal-sinks-Bathroom",
        },
        "bathroom-accessories-hardware-bathroom": {
            "name": "Bathroom Accessories & Hardware",
            "department": "Bathroom",
            "url": "https://www.lowes.com/c/Bathroom-accessories-hardware-Bathroom",
        },
        "bathroom-exhaust-fans-parts-bathroom": {
            "name": "Bathroom Exhaust Fans & Parts",
            "department": "Bathroom",
            "url": "https://www.lowes.com/c/Bathroom-exhaust-fans-parts-Bathroom",
        },
        "bathroom-faucets-shower-heads-bathroom": {
            "name": "Bathroom Faucets & Shower Heads",
            "department": "Bathroom",
            "url": "https://www.lowes.com/c/Bathroom-faucets-shower-heads-Bathroom",
        },
        "bathroom-mirrors-bathroom": {
            "name": "Bathroom Mirrors",
            "department": "Bathroom",
            "url": "https://www.lowes.com/pl/Bathroom-mirrors-Bathroom/4294737205",
        },
        "bathroom-safety-bathroom": {
            "name": "Bathroom Safety",
            "department": "Bathroom",
            "url": "https://www.lowes.com/c/Bathroom-safety-Bathroom",
        },
        "bathroom-sets-bathroom": {
            "name": "Bathroom Sets",
            "department": "Bathroom",
            "url": "https://www.lowes.com/pl/Bathroom-sets-Bathroom/1511187220575",
        },
        "bathroom-storage-bathroom": {
            "name": "Bathroom Storage",
            "department": "Bathroom",
            "url": "https://www.lowes.com/c/Bathroom-storage-Bathroom",
        },
        "bathroom-vanities-vanity-tops-bathroom": {
            "name": "Bathroom Vanities & Vanity Tops",
            "department": "Bathroom",
            "url": "https://www.lowes.com/c/Bathroom-vanities-vanity-tops-Bathroom",
        },
        "bathtubs-whirlpool-tubs-bathroom": {
            "name": "Bathtubs & Whirlpool Tubs",
            "department": "Bathroom",
            "url": "https://www.lowes.com/c/Bathtubs-whirlpool-tubs-Bathroom",
        },
        "commercial-bathroom-components-bathroom": {
            "name": "Commercial Bathroom Components",
            "department": "Bathroom",
            "url": "https://www.lowes.com/pl/Commercial-bathroom-components-Bathroom/4294737179",
        },
        "saunas-components-bathroom": {
            "name": "Saunas & Components",
            "department": "Bathroom",
            "url": "https://www.lowes.com/pl/Saunas-components-Bathroom/4294736334",
        },
        "showers-bathroom": {
            "name": "Showers",
            "department": "Bathroom",
            "url": "https://www.lowes.com/c/Showers-Bathroom",
        },
        "toilets-toilet-seats-bathroom": {
            "name": "Toilets & Toilet Seats",
            "department": "Bathroom",
            "url": "https://www.lowes.com/c/Toilets-toilet-seats-Bathroom",
        },
    },
    "Building Supplies": {
        "asphalt-repair-tools-building-supplies": {
            "name": "Asphalt Repair & Tools",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/pl/Asphalt-repair-tools-Building-supplies/953779431",
        },
        "ceilings-building-supplies": {
            "name": "Ceilings",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/c/Ceilings-Building-supplies",
        },
        "columns-porch-posts-accessories-building-supplies": {
            "name": "Columns, Porch Posts & Accessories",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/pl/Columns-porch-posts-accessories-Building-supplies/4294425046",
        },
        "concrete-cement-masonry-building-supplies": {
            "name": "Concrete, Cement & Masonry",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/c/Concrete-cement-masonry-Building-supplies",
        },
        "decking-building-supplies": {
            "name": "Decking",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/c/Decking-Building-supplies",
        },
        "drywall-building-supplies": {
            "name": "Drywall",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/c/Drywall-Building-supplies",
        },
        "erosion-control-building-supplies": {
            "name": "Erosion Control",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/pl/Erosion-control-Building-supplies/4294653871",
        },
        "fencing-gates-building-supplies": {
            "name": "Fencing & Gates",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/c/Fencing-gates-Building-supplies",
        },
        "glass-acrylic-building-supplies": {
            "name": "Glass & Acrylic",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/pl/Glass-acrylic-Building-supplies/4294713161",
        },
        "gutters-accessories-building-supplies": {
            "name": "Gutters & Accessories",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/c/Gutters-accessories-Building-supplies",
        },
        "insulation-accessories-building-supplies": {
            "name": "Insulation & Accessories",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/c/Insulation-accessories-Building-supplies",
        },
        "jack-posts-building-supplies": {
            "name": "Jack Posts",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/pl/Jack-posts-Building-supplies/4294515331",
        },
        "lumber-composites-building-supplies": {
            "name": "Lumber & Composites",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/c/Lumber-composites-Building-supplies",
        },
        "roofing-building-supplies": {
            "name": "Roofing",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/c/Roofing-Building-supplies",
        },
        "siding-stone-veneer-building-supplies": {
            "name": "Siding & Stone Veneer",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/c/Siding-stone-veneer-Building-supplies",
        },
        "stairs-railings-building-supplies": {
            "name": "Stairs & Railings",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/c/Stairs-railings-Building-supplies",
        },
        "ventilation-building-supplies": {
            "name": "Ventilation",
            "department": "Building Supplies",
            "url": "https://www.lowes.com/pl/Ventilation-Building-supplies/4294858190",
        },
    },
    "Cleaning Supplies": {
        "air-fresheners-cleaning-supplies": {
            "name": "Air Fresheners",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Air-fresheners-Cleaning-supplies/4294386817",
        },
        "all-purpose-cleaners-cleaning-supplies": {
            "name": "All-Purpose Cleaners",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/All-purpose-cleaners-Cleaning-supplies/4294599038",
        },
        "appliance-cleaners-cleaning-supplies": {
            "name": "Appliance Cleaners",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Appliance-cleaners-Cleaning-supplies/3108509681",
        },
        "bleach-cleaning-supplies": {
            "name": "Bleach",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Bleach-Cleaning-supplies/4294599022",
        },
        "cleaning-tools-cleaning-supplies": {
            "name": "Cleaning Tools",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/c/Cleaning-tools-Cleaning-supplies",
        },
        "drain-septic-cleaners-cleaning-supplies": {
            "name": "Drain & Septic Cleaners",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Drain-septic-cleaners-Cleaning-supplies/4294598965",
        },
        "floor-cleaning-cleaning-supplies": {
            "name": "Floor Cleaning",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Floor-cleaning-Cleaning-supplies/2719770657",
        },
        "glass-window-cleaners-cleaning-supplies": {
            "name": "Glass & Window Cleaners",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Glass-window-cleaners-Cleaning-supplies/1920333672",
        },
        "household-cleaners-cleaning-supplies": {
            "name": "Household Cleaners",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Household-cleaners-Cleaning-supplies/4294599039",
        },
        "household-essentials-cleaning-supplies": {
            "name": "Household Essentials",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Household-essentials-Cleaning-supplies/3618734417",
        },
        "janitorial-supplies-cleaning-supplies": {
            "name": "Janitorial Supplies",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Janitorial-supplies-Cleaning-supplies/3757293999",
        },
        "kitchen-bathroom-cleaners-cleaning-supplies": {
            "name": "Kitchen & Bathroom Cleaners",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Kitchen-bathroom-cleaners-Cleaning-supplies/2532134782",
        },
        "laundry-supplies-cleaning-supplies": {
            "name": "Laundry Supplies",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/c/Laundry-supplies-Cleaning-supplies",
        },
        "moisture-absorbers-cleaning-supplies": {
            "name": "Moisture Absorbers",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Moisture-absorbers-Cleaning-supplies/2428286844",
        },
        "mold-removers-cleaning-supplies": {
            "name": "Mold Removers",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Mold-removers-Cleaning-supplies/4294729409",
        },
        "mold-test-kits-cleaning-supplies": {
            "name": "Mold Test Kits",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Mold-test-kits-Cleaning-supplies/4294518335",
        },
        "outdoor-cleaners-cleaning-supplies": {
            "name": "Outdoor Cleaners",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Outdoor-cleaners-Cleaning-supplies/2033510625",
        },
        "trash-recycling-cleaning-supplies": {
            "name": "Trash & Recycling",
            "department": "Cleaning Supplies",
            "url": "https://www.lowes.com/pl/Trash-recycling-Cleaning-supplies/4294599026",
        },
    },
    "Clothing & Work Apparel": {
        "activewear-clothing-work-apparel": {
            "name": "Activewear",
            "department": "Clothing & Work Apparel",
            "url": "https://www.lowes.com/pl/Activewear-Clothing-work-apparel/37721669146478",
        },
        "clothing-clothing-work-apparel": {
            "name": "Clothing",
            "department": "Clothing & Work Apparel",
            "url": "https://www.lowes.com/pl/Clothing-Clothing-work-apparel/15211541027983",
        },
        "footwear-accessories-clothing-work-apparel": {
            "name": "Footwear & Accessories",
            "department": "Clothing & Work Apparel",
            "url": "https://www.lowes.com/pl/Footwear-accessories-Clothing-work-apparel/2711368754867",
        },
        "workwear-clothing-work-apparel": {
            "name": "Workwear",
            "department": "Clothing & Work Apparel",
            "url": "https://www.lowes.com/pl/Workwear-Clothing-work-apparel/2220616391790",
        },
    },
    "Dining & Entertaining": {
        "beverage-dispensers-dining-entertaining": {
            "name": "Beverage Dispensers",
            "department": "Dining & Entertaining",
            "url": "https://www.lowes.com/pl/Beverage-dispensers-Dining-entertaining/4294644703",
        },
        "ice-buckets-dining-entertaining": {
            "name": "Ice Buckets",
            "department": "Dining & Entertaining",
            "url": "https://www.lowes.com/pl/Ice-buckets-Dining-entertaining/4294644705",
        },
        "party-supplies-dining-entertaining": {
            "name": "Party Supplies",
            "department": "Dining & Entertaining",
            "url": "https://www.lowes.com/pl/Party-supplies-Dining-entertaining/4294599098",
        },
        "serveware-accessories-dining-entertaining": {
            "name": "Serveware Accessories",
            "department": "Dining & Entertaining",
            "url": "https://www.lowes.com/pl/Serveware-accessories-Dining-entertaining/4294644701",
        },
        "serving-baskets-dining-entertaining": {
            "name": "Serving Baskets",
            "department": "Dining & Entertaining",
            "url": "https://www.lowes.com/pl/Serving-baskets-Dining-entertaining/4294606037",
        },
        "serving-trays-caddies-dining-entertaining": {
            "name": "Serving Trays & Caddies",
            "department": "Dining & Entertaining",
            "url": "https://www.lowes.com/pl/Serving-trays-caddies-Dining-entertaining/4294644702",
        },
        "table-covers-dining-entertaining": {
            "name": "Table Covers",
            "department": "Dining & Entertaining",
            "url": "https://www.lowes.com/pl/Table-covers-Dining-entertaining/4294606036",
        },
    },
    "Drinks & Snacks": {
        "books-magazines-drinks-snacks": {
            "name": "Books & Magazines",
            "department": "Drinks & Snacks",
            "url": "https://www.lowes.com/pl/Books-magazines-Drinks-snacks/4294859018",
        },
        "coffee-drinks-snacks": {
            "name": "Coffee",
            "department": "Drinks & Snacks",
            "url": "https://www.lowes.com/pl/Coffee-Drinks-snacks/4294606035",
        },
        "gift-center-drinks-snacks": {
            "name": "Gift Center",
            "department": "Drinks & Snacks",
            "url": "https://www.lowes.com/pl/Gift-center-Drinks-snacks/4294625950",
        },
        "snacks-candy-drinks-snacks": {
            "name": "Snacks & Candy",
            "department": "Drinks & Snacks",
            "url": "https://www.lowes.com/pl/Snacks-candy-Drinks-snacks/4294618078",
        },
        "soft-drinks-drinks-snacks": {
            "name": "Soft Drinks",
            "department": "Drinks & Snacks",
            "url": "https://www.lowes.com/pl/Soft-drinks-Drinks-snacks/4294633169",
        },
        "sports-drinks-drinks-snacks": {
            "name": "Sports Drinks",
            "department": "Drinks & Snacks",
            "url": "https://www.lowes.com/pl/Sports-drinks-Drinks-snacks/4294633168",
        },
        "water-drinks-snacks": {
            "name": "Water",
            "department": "Drinks & Snacks",
            "url": "https://www.lowes.com/pl/Water-Drinks-snacks/4294633170",
        },
    },
    "Electrical": {
        "batteries-electrical": {
            "name": "Batteries",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Batteries-Electrical",
        },
        "cable-wire-connectors-electrical": {
            "name": "Cable & Wire Connectors",
            "department": "Electrical",
            "url": "https://www.lowes.com/pl/Cable-wire-connectors-Electrical/4294722554",
        },
        "conduit-conduit-fittings-electrical": {
            "name": "Conduit & Conduit Fittings",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Conduit-conduit-fittings-Electrical",
        },
        "doorbells-electrical": {
            "name": "Doorbells",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Doorbells-Electrical",
        },
        "drones-drone-accessories-electrical": {
            "name": "Drones & Drone Accessories",
            "department": "Electrical",
            "url": "https://www.lowes.com/pl/Drones-drone-accessories-Electrical/1236481888",
        },
        "electrical-boxes-covers-electrical": {
            "name": "Electrical Boxes & Covers",
            "department": "Electrical",
            "url": "https://www.lowes.com/pl/Electrical-boxes-covers-Electrical/4294653960",
        },
        "electrical-outlets-plugs-electrical": {
            "name": "Electrical Outlets & Plugs",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Electrical-outlets-plugs-Electrical",
        },
        "electrical-testers-tools-electrical": {
            "name": "Electrical Testers & Tools",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Electrical-testers-tools-Electrical",
        },
        "electrical-wire-cable-electrical": {
            "name": "Electrical Wire & Cable",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Electrical-wire-cable-Electrical",
        },
        "electronics-electrical": {
            "name": "Electronics",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Electronics-Electrical",
        },
        "extension-cords-surge-protectors-electrical": {
            "name": "Extension Cords & Surge Protectors",
            "department": "Electrical",
            "url": "https://www.lowes.com/pl/Extension-cords-surge-protectors-Electrical/4294542242",
        },
        "fire-safety-electrical": {
            "name": "Fire Safety",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Fire-safety-Electrical",
        },
        "generators-electrical": {
            "name": "Generators",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Generators-Electrical",
        },
        "light-sockets-adapters-electrical": {
            "name": "Light Sockets & Adapters",
            "department": "Electrical",
            "url": "https://www.lowes.com/pl/Light-sockets-adapters-Electrical/4294722560",
        },
        "light-switches-dimmers-electrical": {
            "name": "Light Switches & Dimmers",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Light-switches-dimmers-Electrical",
        },
        "power-distribution-circuit-protection-electrical": {
            "name": "Power Distribution & Circuit Protection",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Power-distribution-circuit-protection-Electrical",
        },
        "solar-power-electrical": {
            "name": "Solar Power",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Solar-power-Electrical",
        },
        "wall-plates-inserts-electrical": {
            "name": "Wall Plates & Inserts",
            "department": "Electrical",
            "url": "https://www.lowes.com/c/Wall-plates-inserts-Electrical",
        },
    },
    "Flooring": {
        "carpet-carpet-tile-flooring": {
            "name": "Carpet & Carpet Tile",
            "department": "Flooring",
            "url": "https://www.lowes.com/c/Carpet-carpet-tile-Flooring",
        },
        "floor-wall-tile-flooring": {
            "name": "Floor & Wall Tile",
            "department": "Flooring",
            "url": "https://www.lowes.com/c/Floor-wall-tile-Flooring",
        },
        "flooring-tools-supplies-flooring": {
            "name": "Flooring Tools & Supplies",
            "department": "Flooring",
            "url": "https://www.lowes.com/c/Flooring-tools-supplies-Flooring",
        },
        "garage-flooring-flooring": {
            "name": "Garage Flooring",
            "department": "Flooring",
            "url": "https://www.lowes.com/pl/Garage-flooring-Flooring/4294642654",
        },
        "gym-flooring-flooring": {
            "name": "Gym Flooring",
            "department": "Flooring",
            "url": "https://www.lowes.com/pl/Gym-flooring-Flooring/4294515431",
        },
        "hardwood-flooring": {
            "name": "Hardwood",
            "department": "Flooring",
            "url": "https://www.lowes.com/c/Hardwood-Flooring",
        },
        "hybrid-resilient-flooring": {
            "name": "Hybrid Resilient",
            "department": "Flooring",
            "url": "https://www.lowes.com/pl/Hybrid-resilient-Flooring/1411043670781",
        },
        "laminate-flooring": {
            "name": "Laminate",
            "department": "Flooring",
            "url": "https://www.lowes.com/c/Laminate-Flooring",
        },
        "vinyl-flooring-flooring": {
            "name": "Vinyl Flooring",
            "department": "Flooring",
            "url": "https://www.lowes.com/c/Vinyl-flooring-Flooring",
        },
    },
    "Glues & Tapes": {
        "glues-glues-tapes": {
            "name": "Glues",
            "department": "Glues & Tapes",
            "url": "https://www.lowes.com/c/Glues-Glues-tapes",
        },
        "tapes-glues-tapes": {
            "name": "Tapes",
            "department": "Glues & Tapes",
            "url": "https://www.lowes.com/c/Tapes-Glues-tapes",
        },
    },
    "Hardware": {
        "cabinet-hardware-hardware": {
            "name": "Cabinet Hardware",
            "department": "Hardware",
            "url": "https://www.lowes.com/c/Cabinet-hardware-Hardware",
        },
        "chains-ropes-tie-downs-hardware": {
            "name": "Chains, Ropes & Tie-Downs",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Chains-ropes-tie-downs-Hardware/4294934403",
        },
        "door-hardware-hardware": {
            "name": "Door Hardware",
            "department": "Hardware",
            "url": "https://www.lowes.com/c/Door-hardware-Hardware",
        },
        "fasteners-hardware": {
            "name": "Fasteners",
            "department": "Hardware",
            "url": "https://www.lowes.com/c/Fasteners-Hardware",
        },
        "furniture-hardware-hardware": {
            "name": "Furniture Hardware",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Furniture-hardware-Hardware/4294711128",
        },
        "gate-hardware-hardware": {
            "name": "Gate Hardware",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Gate-hardware-Hardware/4294856551",
        },
        "hardware-lubricants-hardware": {
            "name": "Hardware Lubricants",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Hardware-lubricants-Hardware/4294607587",
        },
        "hooks-hardware": {
            "name": "Hooks",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Hooks-Hardware/4294710936",
        },
        "keys-key-safes-hardware": {
            "name": "Keys & Key Safes",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Keys-key-safes-Hardware/4294711033",
        },
        "locks-hardware": {
            "name": "Locks",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Locks-Hardware/4294400565",
        },
        "mailboxes-mailbox-posts-hardware": {
            "name": "Mailboxes & Mailbox Posts",
            "department": "Hardware",
            "url": "https://www.lowes.com/c/Mailboxes-mailbox-posts-Hardware",
        },
        "marine-hardware-hardware": {
            "name": "Marine Hardware",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Marine-hardware-Hardware/4294710793",
        },
        "metal-rods-shapes-sheets-hardware": {
            "name": "Metal Rods, Shapes & Sheets",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Metal-rods-shapes-sheets-Hardware/2922688282",
        },
        "picture-hangers-hardware": {
            "name": "Picture Hangers",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Picture-hangers-Hardware/4294710790",
        },
        "safes-hardware": {
            "name": "Safes",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Safes-Hardware/4294806353",
        },
        "signs-letters-numbers-hardware": {
            "name": "Signs, Letters & Numbers",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Signs-letters-numbers-Hardware/4294711114",
        },
        "specialty-hardware-hardware": {
            "name": "Specialty Hardware",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Specialty-hardware-Hardware/4294711047",
        },
        "structural-hardware-hardware": {
            "name": "Structural Hardware",
            "department": "Hardware",
            "url": "https://www.lowes.com/c/Structural-hardware-Hardware",
        },
        "window-hardware-hardware": {
            "name": "Window Hardware",
            "department": "Hardware",
            "url": "https://www.lowes.com/pl/Window-hardware-Hardware/4294711110",
        },
    },
    "Heating & Cooling": {
        "air-conditioners-fans-heating-cooling": {
            "name": "Air Conditioners & Fans",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/c/Air-conditioners-fans-Heating-cooling",
        },
        "air-filters-accessories-heating-cooling": {
            "name": "Air Filters & Accessories",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/c/Air-filters-accessories-Heating-cooling",
        },
        "air-purifiers-accessories-heating-cooling": {
            "name": "Air Purifiers & Accessories",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/c/Air-purifiers-accessories-Heating-cooling",
        },
        "boilers-heating-cooling": {
            "name": "Boilers",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/pl/Boilers-Heating-cooling/1794897186",
        },
        "ductless-mini-splits-heating-cooling": {
            "name": "Ductless Mini Splits",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/c/Ductless-mini-splits-Heating-cooling",
        },
        "fireplaces-stoves-heating-cooling": {
            "name": "Fireplaces & Stoves",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/c/Fireplaces-stoves-Heating-cooling",
        },
        "furnaces-furnace-accessories-heating-cooling": {
            "name": "Furnaces & Furnace Accessories",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/pl/Furnaces-furnace-accessories-Heating-cooling/4294618086",
        },
        "hvac-components-heating-cooling": {
            "name": "HVAC Components",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/pl/HVAC-components-Heating-cooling/542366694",
        },
        "hvac-duct-fittings-heating-cooling": {
            "name": "HVAC Duct & Fittings",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/pl/HVAC-duct-fittings-Heating-cooling/4294512241",
        },
        "heat-pumps-heating-cooling": {
            "name": "Heat Pumps",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/pl/Heat-pumps-Heating-cooling/4294618089",
        },
        "humidifiers-dehumidifiers-heating-cooling": {
            "name": "Humidifiers & Dehumidifiers",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/c/Humidifiers-dehumidifiers-Heating-cooling",
        },
        "portable-space-heaters-heating-cooling": {
            "name": "Portable & Space Heaters",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/c/Portable-space-heaters-Heating-cooling",
        },
        "radiator-covers-heating-cooling": {
            "name": "Radiator Covers",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/pl/Radiator-covers-Heating-cooling/4294395587",
        },
        "registers-grilles-heating-cooling": {
            "name": "Registers & Grilles",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/c/Registers-grilles-Heating-cooling",
        },
        "thermostats-heating-cooling": {
            "name": "Thermostats",
            "department": "Heating & Cooling",
            "url": "https://www.lowes.com/c/Thermostats-Heating-cooling",
        },
    },
    "Holiday Decorations": {
        "christmas-decorations-holiday-decorations": {
            "name": "Christmas Decorations",
            "department": "Holiday Decorations",
            "url": "https://www.lowes.com/c/Christmas-decorations-Holiday-decorations",
        },
        "fall-decorations-holiday-decorations": {
            "name": "Fall Decorations",
            "department": "Holiday Decorations",
            "url": "https://www.lowes.com/pl/Fall-decorations-Holiday-decorations/914756848",
        },
        "fourth-of-july-decorations-holiday-decorations": {
            "name": "Fourth of July Decorations",
            "department": "Holiday Decorations",
            "url": "https://www.lowes.com/pl/Fourth-of-july-decorations-Holiday-decorations/3007020135",
        },
        "halloween-decorations-holiday-decorations": {
            "name": "Halloween Decorations",
            "department": "Holiday Decorations",
            "url": "https://www.lowes.com/pl/Halloween-decorations-Holiday-decorations/4294586669",
        },
        "hanukkah-decorations-holiday-decorations": {
            "name": "Hanukkah Decorations",
            "department": "Holiday Decorations",
            "url": "https://www.lowes.com/pl/Hanukkah-decorations-Holiday-decorations/4294586675",
        },
        "kwanzaa-decorations-holiday-decorations": {
            "name": "Kwanzaa Decorations",
            "department": "Holiday Decorations",
            "url": "https://www.lowes.com/pl/Kwanzaa-decorations-Holiday-decorations/1310306088830",
        },
        "seasonal-decorations-holiday-decorations": {
            "name": "Seasonal Decorations",
            "department": "Holiday Decorations",
            "url": "https://www.lowes.com/pl/Seasonal-decorations-Holiday-decorations/2850470667",
        },
    },
    "Home Decor": {
        "area-rugs-mats-home-decor": {
            "name": "Area Rugs & Mats",
            "department": "Home Decor",
            "url": "https://www.lowes.com/c/Area-rugs-mats-Home-decor",
        },
        "bed-bath-home-decor": {
            "name": "Bed & Bath",
            "department": "Home Decor",
            "url": "https://www.lowes.com/pl/Bed-bath-Home-decor/3596460801",
        },
        "furniture-home-decor": {
            "name": "Furniture",
            "department": "Home Decor",
            "url": "https://www.lowes.com/c/Furniture-Home-decor",
        },
        "home-accents-home-decor": {
            "name": "Home Accents",
            "department": "Home Decor",
            "url": "https://www.lowes.com/c/Home-accents-Home-decor",
        },
        "home-decor-collections-home-decor": {
            "name": "Home Decor Collections",
            "department": "Home Decor",
            "url": "https://www.lowes.com/pl/Home-decor-collections-Home-decor/2111568621127",
        },
        "luggage-travel-home-decor": {
            "name": "Luggage & Travel",
            "department": "Home Decor",
            "url": "https://www.lowes.com/pl/Luggage-travel-Home-decor/255140825",
        },
        "mirrors-mirror-accessories-home-decor": {
            "name": "Mirrors & Mirror Accessories",
            "department": "Home Decor",
            "url": "https://www.lowes.com/c/Mirrors-mirror-accessories-Home-decor",
        },
        "pillows-throws-home-decor": {
            "name": "Pillows & Throws",
            "department": "Home Decor",
            "url": "https://www.lowes.com/pl/Pillows-throws-Home-decor/902277247",
        },
        "wall-art-decor-home-decor": {
            "name": "Wall Art & Decor",
            "department": "Home Decor",
            "url": "https://www.lowes.com/c/Wall-art-decor-Home-decor",
        },
        "wallpaper-accessories-home-decor": {
            "name": "Wallpaper & Accessories",
            "department": "Home Decor",
            "url": "https://www.lowes.com/c/Wallpaper-accessories-Home-decor",
        },
        "window-treatments-home-decor": {
            "name": "Window Treatments",
            "department": "Home Decor",
            "url": "https://www.lowes.com/c/Window-treatments-Home-decor",
        },
    },
    "Kitchen": {
        "backsplash-panels-kitchen": {
            "name": "Backsplash Panels",
            "department": "Kitchen",
            "url": "https://www.lowes.com/pl/Backsplash-panels-Kitchen/4294395588",
        },
        "kitchen-bar-sinks-kitchen": {
            "name": "Kitchen & Bar Sinks",
            "department": "Kitchen",
            "url": "https://www.lowes.com/c/Kitchen-bar-sinks-Kitchen",
        },
        "kitchen-cabinetry-kitchen": {
            "name": "Kitchen Cabinetry",
            "department": "Kitchen",
            "url": "https://www.lowes.com/c/Kitchen-cabinetry-Kitchen",
        },
        "kitchen-countertops-accessories-kitchen": {
            "name": "Kitchen Countertops & Accessories",
            "department": "Kitchen",
            "url": "https://www.lowes.com/c/Kitchen-countertops-accessories-Kitchen",
        },
        "kitchen-faucets-water-dispensers-kitchen": {
            "name": "Kitchen Faucets & Water Dispensers",
            "department": "Kitchen",
            "url": "https://www.lowes.com/c/Kitchen-faucets-water-dispensers-Kitchen",
        },
        "kitchenware-kitchen": {
            "name": "Kitchenware",
            "department": "Kitchen",
            "url": "https://www.lowes.com/c/Kitchenware-Kitchen",
        },
    },
    "Lawn & Garden": {
        "garden-decor-lawn-garden": {
            "name": "Garden Decor",
            "department": "Lawn & Garden",
            "url": "https://www.lowes.com/c/Garden-decor-Lawn-garden",
        },
        "garden-hoses-accessories-lawn-garden": {
            "name": "Garden Hoses & Accessories",
            "department": "Lawn & Garden",
            "url": "https://www.lowes.com/c/Garden-hoses-accessories-Lawn-garden",
        },
        "greenhouses-accessories-lawn-garden": {
            "name": "Greenhouses & Accessories",
            "department": "Lawn & Garden",
            "url": "https://www.lowes.com/pl/Greenhouses-accessories-Lawn-garden/4294512248",
        },
        "insect-pest-control-lawn-garden": {
            "name": "Insect & Pest Control",
            "department": "Lawn & Garden",
            "url": "https://www.lowes.com/c/Insect-pest-control-Lawn-garden",
        },
        "irrigation-lawn-garden": {
            "name": "Irrigation",
            "department": "Lawn & Garden",
            "url": "https://www.lowes.com/c/Irrigation-Lawn-garden",
        },
        "landscaping-lawn-garden": {
            "name": "Landscaping",
            "department": "Lawn & Garden",
            "url": "https://www.lowes.com/c/Landscaping-Lawn-garden",
        },
        "lawn-care-lawn-garden": {
            "name": "Lawn Care",
            "department": "Lawn & Garden",
            "url": "https://www.lowes.com/c/Lawn-care-Lawn-garden",
        },
        "outdoor-drainage-lawn-garden": {
            "name": "Outdoor Drainage",
            "department": "Lawn & Garden",
            "url": "https://www.lowes.com/c/Outdoor-drainage-Lawn-garden",
        },
        "pavers-retaining-walls-lawn-garden": {
            "name": "Pavers & Retaining Walls",
            "department": "Lawn & Garden",
            "url": "https://www.lowes.com/c/Pavers-retaining-walls-Lawn-garden",
        },
        "plant-care-supplies-lawn-garden": {
            "name": "Plant Care & Supplies",
            "department": "Lawn & Garden",
            "url": "https://www.lowes.com/pl/Plant-care-supplies-Lawn-garden/4294612534",
        },
        "planters-stands-garden-beds-lawn-garden": {
            "name": "Planters, Stands & Garden Beds",
            "department": "Lawn & Garden",
            "url": "https://www.lowes.com/c/Planters-stands-garden-beds-Lawn-garden",
        },
        "plants-bulbs-seeds-lawn-garden": {
            "name": "Plants, Bulbs & Seeds",
            "department": "Lawn & Garden",
            "url": "https://www.lowes.com/c/Plants-bulbs-seeds-Lawn-garden",
        },
    },
    "Lighting & Ceiling Fans": {
        "bathroom-wall-lighting-lighting-ceiling-fans": {
            "name": "Bathroom & Wall Lighting",
            "department": "Lighting & Ceiling Fans",
            "url": "https://www.lowes.com/c/Bathroom-wall-lighting-Lighting-ceiling-fans",
        },
        "ceiling-fan-parts-accessories-lighting-ceiling-fans": {
            "name": "Ceiling Fan Parts & Accessories",
            "department": "Lighting & Ceiling Fans",
            "url": "https://www.lowes.com/pl/Ceiling-fan-parts-accessories-Lighting-ceiling-fans/4294395603",
        },
        "ceiling-fans-lighting-ceiling-fans": {
            "name": "Ceiling Fans",
            "department": "Lighting & Ceiling Fans",
            "url": "https://www.lowes.com/c/Ceiling-fans-Lighting-ceiling-fans",
        },
        "ceiling-lights-lighting-ceiling-fans": {
            "name": "Ceiling Lights",
            "department": "Lighting & Ceiling Fans",
            "url": "https://www.lowes.com/pl/Ceiling-lights-Lighting-ceiling-fans/1514558678",
        },
        "commercial-lighting-lighting-ceiling-fans": {
            "name": "Commercial Lighting",
            "department": "Lighting & Ceiling Fans",
            "url": "https://www.lowes.com/c/Commercial-lighting-Lighting-ceiling-fans",
        },
        "lamps-lamp-shades-lighting-ceiling-fans": {
            "name": "Lamps & Lamp Shades",
            "department": "Lighting & Ceiling Fans",
            "url": "https://www.lowes.com/pl/Lamps-lamp-shades-Lighting-ceiling-fans/4294925668",
        },
        "light-bulbs-lighting-ceiling-fans": {
            "name": "Light Bulbs",
            "department": "Lighting & Ceiling Fans",
            "url": "https://www.lowes.com/c/Light-bulbs-Lighting-ceiling-fans",
        },
        "lighting-parts-accessories-lighting-ceiling-fans": {
            "name": "Lighting Parts & Accessories",
            "department": "Lighting & Ceiling Fans",
            "url": "https://www.lowes.com/pl/Lighting-parts-accessories-Lighting-ceiling-fans/4294925669",
        },
        "night-lights-lighting-ceiling-fans": {
            "name": "Night Lights",
            "department": "Lighting & Ceiling Fans",
            "url": "https://www.lowes.com/pl/Night-lights-Lighting-ceiling-fans/4294857028",
        },
        "novelty-lighting-lighting-ceiling-fans": {
            "name": "Novelty Lighting",
            "department": "Lighting & Ceiling Fans",
            "url": "https://www.lowes.com/pl/Novelty-lighting-Lighting-ceiling-fans/4294566036",
        },
        "outdoor-lighting-lighting-ceiling-fans": {
            "name": "Outdoor Lighting",
            "department": "Lighting & Ceiling Fans",
            "url": "https://www.lowes.com/c/Outdoor-lighting-Lighting-ceiling-fans",
        },
        "under-cabinet-lighting-lighting-ceiling-fans": {
            "name": "Under Cabinet Lighting",
            "department": "Lighting & Ceiling Fans",
            "url": "https://www.lowes.com/c/Under-cabinet-lighting-Lighting-ceiling-fans",
        },
    },
    "Moulding & Millwork": {
        "corbels-brackets-braces-moulding-millwork": {
            "name": "Corbels, Brackets & Braces",
            "department": "Moulding & Millwork",
            "url": "https://www.lowes.com/pl/Corbels-brackets-braces-Moulding-millwork/4294518237",
        },
        "dowels-dowel-pins-moulding-millwork": {
            "name": "Dowels & Dowel Pins",
            "department": "Moulding & Millwork",
            "url": "https://www.lowes.com/pl/Dowels-dowel-pins-Moulding-millwork/4294402555",
        },
        "moulding-moulding-millwork": {
            "name": "Moulding",
            "department": "Moulding & Millwork",
            "url": "https://www.lowes.com/pl/Moulding-Moulding-millwork/1237671492",
        },
        "wall-panels-planks-moulding-millwork": {
            "name": "Wall Panels & Planks",
            "department": "Moulding & Millwork",
            "url": "https://www.lowes.com/c/Wall-panels-planks-Moulding-millwork",
        },
    },
    "Outdoor Recreation": {
        "bike-accessories-outdoor-recreation": {
            "name": "Bike Accessories",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/Bike-accessories-Outdoor-recreation/2321646038739",
        },
        "bikes-outdoor-recreation": {
            "name": "Bikes",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/Bikes-Outdoor-recreation/2426769188",
        },
        "boating-outdoor-recreation": {
            "name": "Boating",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/Boating-Outdoor-recreation/2764575254",
        },
        "camping-hunting-fishing-outdoor-recreation": {
            "name": "Camping, Hunting & Fishing",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/Camping-hunting-fishing-Outdoor-recreation/3172089732",
        },
        "fireworks-outdoor-recreation": {
            "name": "Fireworks",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/Fireworks-Outdoor-recreation/1820112634192",
        },
        "game-room-outdoor-recreation": {
            "name": "Game Room",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/Game-room-Outdoor-recreation/4294610499",
        },
        "golf-outdoor-recreation": {
            "name": "Golf",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/Golf-Outdoor-recreation/3515281005",
        },
        "metal-detectors-outdoor-recreation": {
            "name": "Metal Detectors",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/Metal-detectors-Outdoor-recreation/2321957009384",
        },
        "rv-accessories-outdoor-recreation": {
            "name": "RV Accessories",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/RV-accessories-Outdoor-recreation/1403527902",
        },
        "recreational-vehicles-outdoor-recreation": {
            "name": "Recreational Vehicles",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/Recreational-vehicles-Outdoor-recreation/2510965754766",
        },
        "scooters-outdoor-recreation": {
            "name": "Scooters",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/Scooters-Outdoor-recreation/537872457",
        },
        "water-sports-outdoor-recreation": {
            "name": "Water Sports",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/Water-sports-Outdoor-recreation/4294599090",
        },
        "winter-sports-outdoor-recreation": {
            "name": "Winter Sports",
            "department": "Outdoor Recreation",
            "url": "https://www.lowes.com/pl/Winter-sports-Outdoor-recreation/4294610308",
        },
    },
    "Outdoors": {
        "commercial-park-equipment-outdoors": {
            "name": "Commercial Park Equipment",
            "department": "Outdoors",
            "url": "https://www.lowes.com/pl/Commercial-park-equipment-Outdoors/4294610286",
        },
        "fire-pits-patio-heaters-outdoors": {
            "name": "Fire Pits & Patio Heaters",
            "department": "Outdoors",
            "url": "https://www.lowes.com/c/Fire-pits-patio-heaters-Outdoors",
        },
        "grills-outdoor-cooking-outdoors": {
            "name": "Grills & Outdoor Cooking",
            "department": "Outdoors",
            "url": "https://www.lowes.com/c/Grills-outdoor-cooking-Outdoors",
        },
        "hot-tubs-spas-components-outdoors": {
            "name": "Hot Tubs, Spas & Components",
            "department": "Outdoors",
            "url": "https://www.lowes.com/pl/Hot-tubs-spas-components-Outdoors/4294610266",
        },
        "outdoor-games-toys-outdoors": {
            "name": "Outdoor Games & Toys",
            "department": "Outdoors",
            "url": "https://www.lowes.com/c/Outdoor-games-toys-Outdoors",
        },
        "outdoor-tools-equipment-outdoors": {
            "name": "Outdoor Tools & Equipment",
            "department": "Outdoors",
            "url": "https://www.lowes.com/c/Outdoor-tools-equipment-Outdoors",
        },
        "patio-furniture-outdoors": {
            "name": "Patio Furniture",
            "department": "Outdoors",
            "url": "https://www.lowes.com/c/Patio-furniture-Outdoors",
        },
        "playsets-outdoors": {
            "name": "Playsets",
            "department": "Outdoors",
            "url": "https://www.lowes.com/c/Playsets-Outdoors",
        },
        "pools-outdoors": {
            "name": "Pools",
            "department": "Outdoors",
            "url": "https://www.lowes.com/c/Pools-Outdoors",
        },
        "sheds-outdoor-storage-outdoors": {
            "name": "Sheds & Outdoor Storage",
            "department": "Outdoors",
            "url": "https://www.lowes.com/c/Sheds-outdoor-storage-Outdoors",
        },
    },
    "Paint": {
        "caulking-paint": {
            "name": "Caulking",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Caulking-Paint",
        },
        "ceiling-paint-paint": {
            "name": "Ceiling Paint",
            "department": "Paint",
            "url": "https://www.lowes.com/pl/Ceiling-paint-Paint/611625339713",
        },
        "craft-paint-supplies-paint": {
            "name": "Craft Paint & Supplies",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Craft-paint-supplies-Paint",
        },
        "door-trim-paint-paint": {
            "name": "Door & Trim Paint",
            "department": "Paint",
            "url": "https://www.lowes.com/pl/Door-trim-paint-Paint/861738257",
        },
        "exterior-paint-paint": {
            "name": "Exterior Paint",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Exterior-paint-Paint",
        },
        "exterior-wood-coatings-paint": {
            "name": "Exterior Wood Coatings",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Exterior-wood-coatings-Paint",
        },
        "floor-coatings-paint": {
            "name": "Floor Coatings",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Floor-coatings-Paint",
        },
        "interior-paint-paint": {
            "name": "Interior Paint",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Interior-paint-Paint",
        },
        "interior-stains-finishes-paint": {
            "name": "Interior Stains & Finishes",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Interior-stains-finishes-Paint",
        },
        "paint-cleaners-chemicals-additives-paint": {
            "name": "Paint Cleaners, Chemicals & Additives",
            "department": "Paint",
            "url": "https://www.lowes.com/pl/Paint-cleaners-chemicals-additives-Paint/2521972965619",
        },
        "paint-samples-paint": {
            "name": "Paint Samples",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Paint-samples-Paint",
        },
        "paint-supplies-paint": {
            "name": "Paint Supplies",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Paint-supplies-Paint",
        },
        "patching-repair-paint": {
            "name": "Patching & Repair",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Patching-repair-Paint",
        },
        "primer-paint": {
            "name": "Primer",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Primer-Paint",
        },
        "specialty-commercial-paint-paint": {
            "name": "Specialty & Commercial Paint",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Specialty-commercial-paint-Paint",
        },
        "spray-paint-accessories-paint": {
            "name": "Spray Paint & Accessories",
            "department": "Paint",
            "url": "https://www.lowes.com/c/Spray-paint-accessories-Paint",
        },
    },
    "Personal Care & Grooming": {
        "electric-razors-personal-care-grooming": {
            "name": "Electric Razors",
            "department": "Personal Care & Grooming",
            "url": "https://www.lowes.com/pl/Electric-razors-Personal-care-grooming/4294599074",
        },
        "hair-styling-tools-personal-care-grooming": {
            "name": "Hair Styling Tools",
            "department": "Personal Care & Grooming",
            "url": "https://www.lowes.com/pl/Hair-styling-tools-Personal-care-grooming/2021690876378",
        },
        "health-diagnostic-tools-personal-care-grooming": {
            "name": "Health Diagnostic Tools",
            "department": "Personal Care & Grooming",
            "url": "https://www.lowes.com/pl/Health-diagnostic-tools-Personal-care-grooming/2721237196131",
        },
        "light-sound-therapy-personal-care-grooming": {
            "name": "Light & Sound Therapy",
            "department": "Personal Care & Grooming",
            "url": "https://www.lowes.com/pl/Light-sound-therapy-Personal-care-grooming/1047779848",
        },
        "oral-care-personal-care-grooming": {
            "name": "Oral Care",
            "department": "Personal Care & Grooming",
            "url": "https://www.lowes.com/pl/Oral-care-Personal-care-grooming/1920577020870",
        },
        "skin-care-personal-care-grooming": {
            "name": "Skin Care",
            "department": "Personal Care & Grooming",
            "url": "https://www.lowes.com/pl/Skin-care-Personal-care-grooming/1542383729",
        },
    },
    "Plumbing": {
        "augers-plungers-drain-openers-plumbing": {
            "name": "Augers, Plungers & Drain Openers",
            "department": "Plumbing",
            "url": "https://www.lowes.com/c/Augers-plungers-drain-openers-Plumbing",
        },
        "pipe-fittings-plumbing": {
            "name": "Pipe & Fittings",
            "department": "Plumbing",
            "url": "https://www.lowes.com/c/Pipe-fittings-Plumbing",
        },
        "plumbing-parts-repair-plumbing": {
            "name": "Plumbing Parts & Repair",
            "department": "Plumbing",
            "url": "https://www.lowes.com/pl/Plumbing-parts-repair-Plumbing/4294935833",
        },
        "plumbing-tools-cements-plumbing": {
            "name": "Plumbing Tools & Cements",
            "department": "Plumbing",
            "url": "https://www.lowes.com/pl/Plumbing-tools-cements-Plumbing/4294607602",
        },
        "septic-tanks-accessories-plumbing": {
            "name": "Septic Tanks & Accessories",
            "department": "Plumbing",
            "url": "https://www.lowes.com/pl/Septic-tanks-accessories-Plumbing/1352416560",
        },
        "supply-lines-plumbing": {
            "name": "Supply Lines",
            "department": "Plumbing",
            "url": "https://www.lowes.com/pl/Supply-lines-Plumbing/1149069550",
        },
        "utility-sinks-faucets-plumbing": {
            "name": "Utility Sinks & Faucets",
            "department": "Plumbing",
            "url": "https://www.lowes.com/pl/Utility-sinks-faucets-Plumbing/4294639563",
        },
        "valves-valve-repair-plumbing": {
            "name": "Valves & Valve Repair",
            "department": "Plumbing",
            "url": "https://www.lowes.com/c/Valves-valve-repair-Plumbing",
        },
        "water-filtration-water-softeners-plumbing": {
            "name": "Water Filtration & Water Softeners",
            "department": "Plumbing",
            "url": "https://www.lowes.com/c/Water-filtration-water-softeners-Plumbing",
        },
        "water-heater-parts-accessories-plumbing": {
            "name": "Water Heater Parts & Accessories",
            "department": "Plumbing",
            "url": "https://www.lowes.com/pl/Water-heater-parts-accessories-Plumbing/2310003785690",
        },
        "water-heaters-plumbing": {
            "name": "Water Heaters",
            "department": "Plumbing",
            "url": "https://www.lowes.com/c/Water-heaters-Plumbing",
        },
        "water-pumps-tanks-plumbing": {
            "name": "Water Pumps & Tanks",
            "department": "Plumbing",
            "url": "https://www.lowes.com/c/Water-pumps-tanks-Plumbing",
        },
    },
    "Safety": {
        "child-safety-safety": {
            "name": "Child Safety",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Child-safety-Safety/4294644944",
        },
        "eye-protection-safety": {
            "name": "Eye Protection",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Eye-protection-Safety/4294644951",
        },
        "first-aid-safety": {
            "name": "First Aid",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/First-aid-Safety/4294644939",
        },
        "hard-hat-accessories-safety": {
            "name": "Hard Hat Accessories",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Hard-hat-accessories-Safety/4294482086",
        },
        "hard-hats-safety": {
            "name": "Hard Hats",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Hard-hats-Safety/4294644957",
        },
        "hearing-protection-safety": {
            "name": "Hearing Protection",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Hearing-protection-Safety/4294644955",
        },
        "ice-melt-safety": {
            "name": "Ice Melt",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Ice-melt-Safety/4294414320",
        },
        "knee-pads-safety": {
            "name": "Knee Pads",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Knee-pads-Safety/4294644960",
        },
        "marking-flags-safety": {
            "name": "Marking Flags",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Marking-flags-Safety/4294559264",
        },
        "pepper-spray-safety": {
            "name": "Pepper Spray",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Pepper-spray-Safety/1221059300625",
        },
        "protective-clothing-safety": {
            "name": "Protective Clothing",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Protective-clothing-Safety/4294625947",
        },
        "respiratory-protection-safety": {
            "name": "Respiratory Protection",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Respiratory-protection-Safety/721068286897",
        },
        "safety-accessories-safety": {
            "name": "Safety Accessories",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Safety-accessories-Safety/4294644945",
        },
        "safety-tape-safety": {
            "name": "Safety Tape",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Safety-tape-Safety/4294644907",
        },
        "safety-vests-safety": {
            "name": "Safety Vests",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Safety-vests-Safety/4294644952",
        },
        "test-kits-safety": {
            "name": "Test Kits",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Test-kits-Safety/3385023924",
        },
        "traffic-safety-equipment-safety": {
            "name": "Traffic Safety Equipment",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Traffic-safety-equipment-Safety/4294644940",
        },
        "weather-radios-safety": {
            "name": "Weather Radios",
            "department": "Safety",
            "url": "https://www.lowes.com/pl/Weather-radios-Safety/4294644967",
        },
    },
    "Smart Home, Security, Wi-Fi": {
        "home-security-smart-home-security-wi-fi": {
            "name": "Home Security",
            "department": "Smart Home, Security, Wi-Fi",
            "url": "https://www.lowes.com/pl/Home-security-Smart-home-security-wi-fi/2957059063",
        },
        "smart-home-smart-home-security-wi-fi": {
            "name": "Smart Home",
            "department": "Smart Home, Security, Wi-Fi",
            "url": "https://www.lowes.com/pl/Smart-home-Smart-home-security-wi-fi/37721669146452",
        },
        "wi-fi-networking-devices-smart-home-security-wi-fi": {
            "name": "Wi-Fi & Networking Devices",
            "department": "Smart Home, Security, Wi-Fi",
            "url": "https://www.lowes.com/pl/Wi-fi-networking-devices-Smart-home-security-wi-fi/2821202638033",
        },
    },
    "Sports & Fitness": {
        "basketball-systems-sports-fitness": {
            "name": "Basketball Systems",
            "department": "Sports & Fitness",
            "url": "https://www.lowes.com/pl/Basketball-systems-Sports-fitness/4294506781",
        },
        "bleacher-cushions-seats-sports-fitness": {
            "name": "Bleacher Cushions & Seats",
            "department": "Sports & Fitness",
            "url": "https://www.lowes.com/pl/Bleacher-cushions-seats-Sports-fitness/407195896",
        },
        "coolers-water-bottles-sports-fitness": {
            "name": "Coolers & Water Bottles",
            "department": "Sports & Fitness",
            "url": "https://www.lowes.com/c/Coolers-water-bottles-Sports-fitness",
        },
        "fitness-exercise-equipment-sports-fitness": {
            "name": "Fitness & Exercise Equipment",
            "department": "Sports & Fitness",
            "url": "https://www.lowes.com/pl/Fitness-exercise-equipment-Sports-fitness/4294546188",
        },
        "sports-equipment-sports-fitness": {
            "name": "Sports Equipment",
            "department": "Sports & Fitness",
            "url": "https://www.lowes.com/pl/Sports-equipment-Sports-fitness/2108258635",
        },
    },
    "Storage & Organization": {
        "baskets-storage-containers-storage-organization": {
            "name": "Baskets & Storage Containers",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/c/Baskets-storage-containers-Storage-organization",
        },
        "closet-organization-storage-organization": {
            "name": "Closet Organization",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/c/Closet-organization-Storage-organization",
        },
        "garage-organization-storage-organization": {
            "name": "Garage Organization",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/c/Garage-organization-Storage-organization",
        },
        "hooks-racks-storage-organization": {
            "name": "Hooks & Racks",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/pl/Hooks-racks-Storage-organization/4294936564",
        },
        "kitchen-organization-storage-organization": {
            "name": "Kitchen Organization",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/pl/Kitchen-organization-Storage-organization/4294857701",
        },
        "laundry-organization-storage-organization": {
            "name": "Laundry Organization",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/pl/Laundry-organization-Storage-organization/4294857708",
        },
        "lockers-storage-organization": {
            "name": "Lockers",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/pl/Lockers-Storage-organization/855642652",
        },
        "moving-boxes-supplies-storage-organization": {
            "name": "Moving Boxes & Supplies",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/c/Moving-boxes-supplies-Storage-organization",
        },
        "office-school-supplies-storage-organization": {
            "name": "Office & School Supplies",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/pl/Office-school-supplies-Storage-organization/2611667535867",
        },
        "shelves-shelving-storage-organization": {
            "name": "Shelves & Shelving",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/c/Shelves-shelving-Storage-organization",
        },
        "shoe-storage-storage-organization": {
            "name": "Shoe Storage",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/pl/Shoe-storage-Storage-organization/688954782",
        },
        "small-parts-organizers-storage-organization": {
            "name": "Small Parts Organizers",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/pl/Small-parts-organizers-Storage-organization/4211758077",
        },
        "utility-storage-cabinets-storage-organization": {
            "name": "Utility Storage Cabinets",
            "department": "Storage & Organization",
            "url": "https://www.lowes.com/pl/Utility-storage-cabinets-Storage-organization/3721327500",
        },
    },
    "Tools": {
        "air-tools-compressors-tools": {
            "name": "Air Tools & Compressors",
            "department": "Tools",
            "url": "https://www.lowes.com/c/Air-tools-compressors-Tools",
        },
        "flashlights-tools": {
            "name": "Flashlights",
            "department": "Tools",
            "url": "https://www.lowes.com/pl/Flashlights-Tools/2018528687",
        },
        "hand-tools-tools": {
            "name": "Hand Tools",
            "department": "Tools",
            "url": "https://www.lowes.com/c/Hand-tools-Tools",
        },
        "home-3d-printers-filament-tools": {
            "name": "Home 3D Printers & Filament",
            "department": "Tools",
            "url": "https://www.lowes.com/pl/Home-3d-printers-filament-Tools/4294482089",
        },
        "jobsite-radios-tools": {
            "name": "Jobsite Radios",
            "department": "Tools",
            "url": "https://www.lowes.com/pl/Jobsite-radios-Tools/195306503",
        },
        "ladders-scaffolding-tools": {
            "name": "Ladders & Scaffolding",
            "department": "Tools",
            "url": "https://www.lowes.com/c/Ladders-scaffolding-Tools",
        },
        "levels-measuring-tools-tools": {
            "name": "Levels & Measuring Tools",
            "department": "Tools",
            "url": "https://www.lowes.com/pl/Levels-measuring-tools-Tools/4294607864",
        },
        "power-tool-accessories-tools": {
            "name": "Power Tool Accessories",
            "department": "Tools",
            "url": "https://www.lowes.com/c/Power-tool-accessories-Tools",
        },
        "power-tools-tools": {
            "name": "Power Tools",
            "department": "Tools",
            "url": "https://www.lowes.com/pl/Power-tools-Tools/4294607842",
        },
        "shop-vacuums-accessories-tools": {
            "name": "Shop Vacuums & Accessories",
            "department": "Tools",
            "url": "https://www.lowes.com/pl/Shop-vacuums-accessories-Tools/4294857473",
        },
        "tool-storage-work-benches-tools": {
            "name": "Tool Storage & Work Benches",
            "department": "Tools",
            "url": "https://www.lowes.com/c/Tool-storage-work-benches-Tools",
        },
        "walkie-talkies-tools": {
            "name": "Walkie Talkies",
            "department": "Tools",
            "url": "https://www.lowes.com/pl/Walkie-talkies-Tools/1332684016",
        },
        "welding-soldering-tools": {
            "name": "Welding & Soldering",
            "department": "Tools",
            "url": "https://www.lowes.com/c/Welding-soldering-Tools",
        },
    },
    "Windows & Doors": {
        "awnings-accessories-windows-doors": {
            "name": "Awnings & Accessories",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/pl/Awnings-accessories-Windows-doors/4294858045",
        },
        "exterior-doors-windows-doors": {
            "name": "Exterior Doors",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/c/Exterior-doors-Windows-doors",
        },
        "exterior-shutters-accessories-windows-doors": {
            "name": "Exterior Shutters & Accessories",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/c/Exterior-shutters-accessories-Windows-doors",
        },
        "garage-doors-openers-windows-doors": {
            "name": "Garage Doors & Openers",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/c/Garage-doors-openers-Windows-doors",
        },
        "hurricane-shutter-panels-hardware-windows-doors": {
            "name": "Hurricane Shutter Panels & Hardware",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/pl/Hurricane-shutter-panels-hardware-Windows-doors/4294858024",
        },
        "interior-doors-windows-doors": {
            "name": "Interior Doors",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/c/Interior-doors-Windows-doors",
        },
        "replacement-screens-windows-doors": {
            "name": "Replacement Screens",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/pl/Replacement-screens-Windows-doors/2867482404",
        },
        "screen-frame-connectors-windows-doors": {
            "name": "Screen Frame Connectors",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/pl/Screen-frame-connectors-Windows-doors/2155437395",
        },
        "screen-spline-windows-doors": {
            "name": "Screen Spline",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/pl/Screen-spline-Windows-doors/4294772364",
        },
        "screen-tools-windows-doors": {
            "name": "Screen Tools",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/pl/Screen-tools-Windows-doors/4294772361",
        },
        "screening-systems-windows-doors": {
            "name": "Screening Systems",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/pl/Screening-systems-Windows-doors/555679654",
        },
        "weatherstripping-windows-doors": {
            "name": "Weatherstripping",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/pl/Weatherstripping-Windows-doors/4294929691",
        },
        "windows-windows-doors": {
            "name": "Windows",
            "department": "Windows & Doors",
            "url": "https://www.lowes.com/c/Windows-Windows-doors",
        },
    },
}
