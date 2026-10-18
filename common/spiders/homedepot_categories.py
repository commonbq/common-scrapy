"""Home Depot department -> subcategory inventory from the live storefront nav.

Source of truth: the ``SideNavigation`` node of the ``__APOLLO_STATE__`` payload
on each department PLP (https://www.homedepot.com/b/<Department>/N-<id>), which
is the same first-party navigation tree the left rail renders. Captured
2026-10-18 UTC through the repository's configured ScrapeOps US residential
proxy: **26 departments** and **393 leaf category PLPs**.

Grouped ``{department: {leaf: {url, label}}}`` mapping as required by the
``BaseListingSpider`` contract, so the spider and the DAG share one source of
truth and ``_spider_category_groups(..., group_by="department")`` can emit one
TaskGroup per department.

Excluded: ``heading: true`` rail headers and promotional landing pages
(``Tool Savings``, ``Tool Innovation``, ``Shop All Bath Savings`` variants).

Every leaf is globally unique and every URL is distinct. A PLP linked from two
departments is stored once under the department named by its own breadcrumb, so
``-a category=<leaf>`` stays unambiguous; a department hub linked from a sibling
department always stays with its own group. Each department also keeps a leaf
named after its own group key (``tools`` -> the department hub) so the documented
``-a category=tools`` command keeps working. Hub entries sit last in their group:
the DAG factory schedules only the first three leaves per group, so the scheduled
tasks are real subcategory PLPs while the hub stays reachable for a manual run.
"""

from __future__ import annotations

HOMEDEPOT_CATEGORIES: dict[str, dict[str, dict[str, str]]] = {

    "appliances": {
        "appliances-refrigerators": {
            "url": "https://www.homedepot.com/b/Appliances-Refrigerators/N-5yc1vZc3pi",
            "label": "Refrigerators",
        },
        "appliances-ranges": {
            "url": "https://www.homedepot.com/b/Appliances-Ranges/N-5yc1vZc3o9",
            "label": "Ranges",
        },
        "appliances-dishwashers": {
            "url": "https://www.homedepot.com/b/Appliances-Dishwashers/N-5yc1vZc3po",
            "label": "Dishwashers",
        },
        "appliances-microwaves": {
            "url": "https://www.homedepot.com/b/Appliances-Microwaves/N-5yc1vZc3ok",
            "label": "Microwaves",
        },
        "appliances-microwaves-over-the-range-microwaves": {
            "url": "https://www.homedepot.com/b/Appliances-Microwaves-Over-the-Range-Microwaves/N-5yc1vZc3pa",
            "label": "Over-the-Range Microwaves",
        },
        "appliances-range-hoods": {
            "url": "https://www.homedepot.com/b/Appliances-Range-Hoods/N-5yc1vZc3nk",
            "label": "Range Hoods",
        },
        "appliances-freezers": {
            "url": "https://www.homedepot.com/b/Appliances-Freezers/N-5yc1vZc3p2",
            "label": "Freezers",
        },
        "appliances-wall-ovens": {
            "url": "https://www.homedepot.com/b/Appliances-Wall-Ovens/N-5yc1vZc3nq",
            "label": "Wall Ovens",
        },
        "appliances-cooktops": {
            "url": "https://www.homedepot.com/b/Appliances-Cooktops/N-5yc1vZc3oq",
            "label": "Cooktops",
        },
        "appliances-beverage-coolers": {
            "url": "https://www.homedepot.com/b/Appliances-Beverage-Coolers/N-5yc1vZc3o4",
            "label": "Beverage Coolers",
        },
        "appliances-mini-fridges": {
            "url": "https://www.homedepot.com/b/Appliances-Mini-Fridges/N-5yc1vZc4mo",
            "label": "Mini Fridges",
        },
        "appliances-washers-dryers-washer-dryer-sets": {
            "url": "https://www.homedepot.com/b/Appliances-Washers-Dryers-Washer-Dryer-Sets/N-5yc1vZ2fkpgvt",
            "label": "Washer & Dryer Sets",
        },
        "appliances-washers-dryers-washing-machines": {
            "url": "https://www.homedepot.com/b/Appliances-Washers-Dryers-Washing-Machines/N-5yc1vZc3ov",
            "label": "Washers",
        },
        "appliances-washers-dryers-dryers": {
            "url": "https://www.homedepot.com/b/Appliances-Washers-Dryers-Dryers/N-5yc1vZc3p3",
            "label": "Dryers",
        },
        "appliances-washers-dryers": {
            "url": "https://www.homedepot.com/b/Appliances-Washers-Dryers/Stackable/N-5yc1vZc3olZ1z17ic0",
            "label": "Stackable Washers & Dryers",
        },
        "appliances-floor-care-vacuums": {
            "url": "https://www.homedepot.com/b/Appliances-Floor-Care-Vacuums/N-5yc1vZbv1z",
            "label": "Floor Care & Vacuums",
        },
        "appliances-vacuum-cleaners": {
            "url": "https://www.homedepot.com/b/Appliances-Vacuum-Cleaners/N-5yc1vZbv74",
            "label": "Vacuums",
        },
        "appliances": {
            "url": "https://www.homedepot.com/b/Appliances/N-5yc1vZbv1w",
            "label": "Appliances",
        },
    },
    "bath": {
        "bath-bathroom-vanities": {
            "url": "https://www.homedepot.com/b/Bath-Bathroom-Vanities/N-5yc1vZcfv3",
            "label": "Bathroom Vanities",
        },
        "bath-bathroom-faucets": {
            "url": "https://www.homedepot.com/b/Bath-Bathroom-Faucets/N-5yc1vZbreo",
            "label": "Bathroom Faucets",
        },
        "bath-showers": {
            "url": "https://www.homedepot.com/b/Bath-Showers/N-5yc1vZbzcd",
            "label": "Showers & Doors",
        },
        "bath-bathtubs": {
            "url": "https://www.homedepot.com/b/Bath-Bathtubs/N-5yc1vZbzb7",
            "label": "Bathtubs",
        },
        "bath-bathroom-faucets-shower-heads": {
            "url": "https://www.homedepot.com/b/Bath-Bathroom-Faucets-Shower-Heads/N-5yc1vZcjoc",
            "label": "Shower Heads",
        },
        "bath-toilets": {
            "url": "https://www.homedepot.com/b/Bath-Toilets/N-5yc1vZbzbd",
            "label": "Toilets",
        },
        "bath-toilets-toilet-seats": {
            "url": "https://www.homedepot.com/b/Bath-Toilets-Toilet-Seats/N-5yc1vZceq5",
            "label": "Toilet Seats",
        },
        "bath-bidets": {
            "url": "https://www.homedepot.com/b/Bath-Bidets/N-5yc1vZceq2",
            "label": "Bidets",
        },
        "bath-bathroom-sinks": {
            "url": "https://www.homedepot.com/b/Bath-Bathroom-Sinks/N-5yc1vZbzb0",
            "label": "Bathroom Sinks",
        },
        "bath-bathroom-accessories": {
            "url": "https://www.homedepot.com/b/Bath-Bathroom-Accessories/N-5yc1vZcfvt",
            "label": "Bathroom Accessories",
        },
        "bath-bathroom-storage": {
            "url": "https://www.homedepot.com/b/Bath-Bathroom-Storage/N-5yc1vZcfvm",
            "label": "Bathroom Storage",
        },
        "bath-bathroom-storage-bathroom-cabinets": {
            "url": "https://www.homedepot.com/b/Bath-Bathroom-Storage-Bathroom-Cabinets/N-5yc1vZ2fkp9qx",
            "label": "Bathroom Cabinets",
        },
        "bath-bathroom-mirrors": {
            "url": "https://www.homedepot.com/b/Bath-Bathroom-Mirrors/N-5yc1vZbzbo",
            "label": "Bathroom Mirrors",
        },
        "bath-bathroom-exhaust-fans": {
            "url": "https://www.homedepot.com/b/Bath-Bathroom-Exhaust-Fans/N-5yc1vZc4ly",
            "label": "Bathroom Exhaust Fans",
        },
        "bath-bathroom-safety": {
            "url": "https://www.homedepot.com/b/Bath-Bathroom-Safety/N-5yc1vZ1z18i4t",
            "label": "Bathroom Safety",
        },
        "bath-shower-accessories-shower-curtains": {
            "url": "https://www.homedepot.com/b/Bath-Shower-Accessories-Shower-Curtains/N-5yc1vZcfv5",
            "label": "Shower Curtains",
        },
        "bath-bathroom-accessories-bathroom-hardware": {
            "url": "https://www.homedepot.com/b/Bath-Bathroom-Accessories-Bathroom-Hardware/N-5yc1vZcfv8",
            "label": "Bathroom Hardware",
        },
        "bath-bathroom-exhaust-fans-bath-fans": {
            "url": "https://www.homedepot.com/b/Bath-Bathroom-Exhaust-Fans-Bath-Fans/N-5yc1vZc4kq",
            "label": "Bathroom Fans",
        },
        "bath": {
            "url": "https://www.homedepot.com/b/Bath/N-5yc1vZbzb3",
            "label": "Bath",
        },
    },
    "window-treatments": {
        "window-treatments-blinds": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Blinds/N-5yc1vZch24",
            "label": "Blinds",
        },
        "window-treatments-window-shades": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Window-Shades/N-5yc1vZch27",
            "label": "Shades",
        },
        "window-treatments-curtains-drapes": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Curtains-Drapes/N-5yc1vZarfw",
            "label": "Curtains & Drapes",
        },
        "window-treatments-window-shades-cellular-shades": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Window-Shades-Cellular-Shades/N-5yc1vZbt0s",
            "label": "Cellular Shades",
        },
        "window-treatments-blinds-faux-wood-blinds": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Blinds-Faux-Wood-Blinds/N-5yc1vZbc8b",
            "label": "Faux Wood Blinds",
        },
        "window-treatments-window-shades-roller-shades": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Window-Shades-Roller-Shades/N-5yc1vZbt0w",
            "label": "Roller Shades",
        },
        "window-treatments-blinds-mini-blinds": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Blinds-Mini-Blinds/N-5yc1vZapzq",
            "label": "Mini Blinds",
        },
        "window-treatments-blinds-vertical-blinds": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Blinds-Vertical-Blinds/N-5yc1vZbc7c",
            "label": "Vertical Blinds",
        },
        "window-treatments-blinds-wood-blinds": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Blinds-Wood-Blinds/N-5yc1vZbc75",
            "label": "Wood Blinds",
        },
        "window-treatments-window-shades-roman-shades": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Window-Shades-Roman-Shades/N-5yc1vZbt0h",
            "label": "Roman Shades",
        },
        "window-treatments-window-shades-solar-shades": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Window-Shades-Solar-Shades/N-5yc1vZcbb8",
            "label": "Solar Shades",
        },
        "window-treatments-window-shades-pleated-shades": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Window-Shades-Pleated-Shades/N-5yc1vZc9nu",
            "label": "Pleated Shades",
        },
        "window-treatments-window-film": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Window-Film/N-5yc1vZarc3",
            "label": "Window Film",
        },
        "window-treatments-curtains-drapes-curtain-rods": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Curtains-Drapes-Curtain-Rods/N-5yc1vZasco",
            "label": "Curtain Rods",
        },
        "window-treatments-curtains-drapes-curtain-drapery-hardware": {
            "url": "https://www.homedepot.com/b/Window-Treatments-Curtains-Drapes-Curtain-Drapery-Hardware/N-5yc1vZ1z18gsm",
            "label": "Curtain Hardware",
        },
        "window-treatments": {
            "url": "https://www.homedepot.com/b/Window-Treatments/N-5yc1vZar4w",
            "label": "Blinds & Window Treatments",
        },
    },
    "building-materials": {
        "building-materials-concrete-cement-masonry": {
            "url": "https://www.homedepot.com/b/Building-Materials-Concrete-Cement-Masonry/N-5yc1vZarlk",
            "label": "Concrete, Cement & Masonry",
        },
        "building-materials-moulding-millwork": {
            "url": "https://www.homedepot.com/b/Building-Materials-Moulding-Millwork/N-5yc1vZaq4y",
            "label": "Moulding & Millwork",
        },
        "building-materials-insulation": {
            "url": "https://www.homedepot.com/b/Building-Materials-Insulation/N-5yc1vZasbs",
            "label": "Insulation",
        },
        "building-materials-drywall": {
            "url": "https://www.homedepot.com/b/Building-Materials-Drywall/N-5yc1vZar3d",
            "label": "Drywall",
        },
        "building-materials-roofing": {
            "url": "https://www.homedepot.com/b/Building-Materials-Roofing/N-5yc1vZaq7m",
            "label": "Roofing",
        },
        "building-materials-gutter-systems": {
            "url": "https://www.homedepot.com/b/Building-Materials-Gutter-Systems/N-5yc1vZardx",
            "label": "Gutter Systems",
        },
        "building-materials-siding": {
            "url": "https://www.homedepot.com/b/Building-Materials-Siding/N-5yc1vZarip",
            "label": "Siding",
        },
        "building-materials-ladders": {
            "url": "https://www.homedepot.com/b/Building-Materials-Ladders/N-5yc1vZaqnp",
            "label": "Ladders",
        },
        "building-materials-building-hardware": {
            "url": "https://www.homedepot.com/b/Building-Materials-Building-Hardware/N-5yc1vZaqzs",
            "label": "Building Hardware",
        },
        "building-materials-ventilation": {
            "url": "https://www.homedepot.com/b/Building-Materials-Ventilation/N-5yc1vZc4mr",
            "label": "Ventilation",
        },
        "building-materials-ceilings": {
            "url": "https://www.homedepot.com/b/Building-Materials-Ceilings/N-5yc1vZc58i",
            "label": "Ceilings",
        },
        "building-materials-moulding-millwork-moulding-door-window-moulding": {
            "url": "https://www.homedepot.com/b/Building-Materials-Moulding-Millwork-Moulding-Door-Window-Moulding/Jamb-Moulding/N-5yc1vZcbjmZ1z1xu0a",
            "label": "Door Jamb",
        },
        "building-materials": {
            "url": "https://www.homedepot.com/b/Building-Materials/N-5yc1vZaqns",
            "label": "Building Materials",
        },
    },
    "lumber-composites": {
        "lumber-composites-decking": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Decking/N-5yc1vZbqmg",
            "label": "Decking",
        },
        "lumber-composites-fencing": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Fencing/N-5yc1vZbrk7",
            "label": "Fencing",
        },
        "lumber-composites-plywood": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Plywood/N-5yc1vZbqm7",
            "label": "Plywood",
        },
        "lumber-composites-boards-planks-panels": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Boards-Planks-Panels/N-5yc1vZ1z18h41",
            "label": "Boards, Planks & Panels",
        },
        "lumber-composites-dimensional-lumber": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Dimensional-Lumber/N-5yc1vZc3tc",
            "label": "Dimensional Lumber",
        },
        "lumber-composites-plywood-oriented-strand-board-osb": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Plywood-Oriented-Strand-Board-OSB/N-5yc1vZbqpq",
            "label": "OSB",
        },
        "lumber-composites-plywood-sheathing-plywood": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Plywood-Sheathing-Plywood/N-5yc1vZc7q5",
            "label": "Sheathing Plywood",
        },
        "lumber-composites-boards-planks-wood-boards": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Boards-Planks-Wood-Boards/N-5yc1vZbqmc",
            "label": "Wood Boards",
        },
        "lumber-composites-boards-planks-panels-wall-paneling": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Boards-Planks-Panels-Wall-Paneling/N-5yc1vZbqp3",
            "label": "Wall Paneling",
        },
        "lumber-composites-pressure-treated-lumber": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Pressure-Treated-Lumber/N-5yc1vZc3sr",
            "label": "Pressure Treated Lumber",
        },
        "lumber-composites-decking-deck-boards": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Decking-Deck-Boards/N-5yc1vZc5mh",
            "label": "Deck Boards",
        },
        "lumber-composites-decking-deck-boards-wood-decking-boards": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Decking-Deck-Boards-Wood-Decking-Boards/N-5yc1vZc80m",
            "label": "Wood Decking Boards",
        },
        "lumber-composites-decking-deck-railings": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Decking-Deck-Railings/N-5yc1vZc5i7",
            "label": "Deck Railings",
        },
        "lumber-composites-fencing-wood-fencing": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Fencing-Wood-Fencing/N-5yc1vZc3m6",
            "label": "Wood Fencing",
        },
        "lumber-composites-lattice": {
            "url": "https://www.homedepot.com/b/Lumber-Composites-Lattice/N-5yc1vZbqna",
            "label": "Lattice",
        },
        "lumber-composites": {
            "url": "https://www.homedepot.com/b/Lumber-Composites/N-5yc1vZbqpg",
            "label": "Lumber & Composites",
        },
    },
    "moulding-millwork": {
        "moulding-millwork-moulding": {
            "url": "https://www.homedepot.com/b/Moulding-Millwork-Moulding/Pro-Pack/N-5yc1vZara1Z1z1xyta",
            "label": "Pro Packs",
        },
        "moulding-millwork-moulding-ceiling-moulding": {
            "url": "https://www.homedepot.com/b/Moulding-Millwork-Moulding-Ceiling-Moulding/Crown-Moulding/N-5yc1vZ2fkph7wZ1z1rueh",
            "label": "Crown Moulding",
        },
        "moulding-millwork-moulding-general-purpose-moulding": {
            "url": "https://www.homedepot.com/b/Moulding-Millwork-Moulding-General-Purpose-Moulding/N-5yc1vZcbj5",
            "label": "General Purpose",
        },
        "moulding-millwork-moulding-door-window-moulding": {
            "url": "https://www.homedepot.com/b/Moulding-Millwork-Moulding-Door-Window-Moulding/N-5yc1vZcbjm",
            "label": "Door & Window",
        },
        "moulding-millwork-moulding-floor-moulding": {
            "url": "https://www.homedepot.com/b/Moulding-Millwork-Moulding-Floor-Moulding/Shoe-Moulding/N-5yc1vZ2fkph7uZ1z1u6ri",
            "label": "Shoe Moulding",
        },
        "moulding-millwork-columns-accessories": {
            "url": "https://www.homedepot.com/b/Moulding-Millwork-Columns-Accessories/N-5yc1vZaqok",
            "label": "Columns & Accessories",
        },
        "moulding-millwork-dowels": {
            "url": "https://www.homedepot.com/b/Moulding-Millwork-Dowels/N-5yc1vZaqif",
            "label": "Dowels",
        },
        "moulding-millwork-stairs-railings": {
            "url": "https://www.homedepot.com/b/Moulding-Millwork-Stairs-Railings/N-5yc1vZbcro",
            "label": "Interior Stair Parts",
        },
        "moulding-millwork-stairs-railings-stair-railings-handrails": {
            "url": "https://www.homedepot.com/b/Moulding-Millwork-Stairs-Railings-Stair-Railings-Handrails/N-5yc1vZ2fkpaac",
            "label": "Handrails",
        },
        "moulding-millwork": {
            "url": "https://www.homedepot.com/b/Moulding-Millwork/N-5yc1vZaq4y",
            "label": "Moulding & Millwork",
        },
    },
    "cleaning": {
        "cleaning-cleaning-products": {
            "url": "https://www.homedepot.com/b/Cleaning-Cleaning-Products/N-5yc1vZcb33",
            "label": "Shop All Cleaning Products",
        },
        "cleaning-cleaning-tools": {
            "url": "https://www.homedepot.com/b/Cleaning-Cleaning-Tools/N-5yc1vZcb51",
            "label": "Shop All Cleaning Tools",
        },
        "cleaning-cleaning-supplies-all-purpose-cleaners": {
            "url": "https://www.homedepot.com/b/Cleaning-Cleaning-Supplies-All-Purpose-Cleaners/N-5yc1vZcb2p",
            "label": "All-Purpose Cleaners",
        },
        "cleaning-cleaning-supplies-bathroom-cleaners": {
            "url": "https://www.homedepot.com/b/Cleaning-Cleaning-Supplies-Bathroom-Cleaners/N-5yc1vZcb45",
            "label": "Bathroom Cleaners",
        },
        "cleaning-trash-recycling": {
            "url": "https://www.homedepot.com/b/Cleaning-Trash-Recycling/N-5yc1vZcb21",
            "label": "Trash & Recycling",
        },
        "cleaning-cleaning-supplies-floor-cleaners": {
            "url": "https://www.homedepot.com/b/Cleaning-Cleaning-Supplies-Floor-Cleaners/N-5yc1vZcb37",
            "label": "Floor Cleaners",
        },
        "cleaning-household-essentials-room-fresheners": {
            "url": "https://www.homedepot.com/b/Cleaning-Household-Essentials-Room-Fresheners/N-5yc1vZcb47",
            "label": "Room Fresheners",
        },
        "cleaning-cleaning-supplies-kitchen-cleaners": {
            "url": "https://www.homedepot.com/b/Cleaning-Cleaning-Supplies-Kitchen-Cleaners/N-5yc1vZch5o",
            "label": "Kitchen Cleaners",
        },
        "cleaning-cleaning-tools-mops": {
            "url": "https://www.homedepot.com/b/Cleaning-Cleaning-Tools-Mops/N-5yc1vZcb4k",
            "label": "Mops",
        },
        "cleaning-cleaning-tools-brooms": {
            "url": "https://www.homedepot.com/b/Cleaning-Cleaning-Tools-Brooms/N-5yc1vZcb2s",
            "label": "Brooms",
        },
        "cleaning-household-essentials-laundry-supplies": {
            "url": "https://www.homedepot.com/b/Cleaning-Household-Essentials-Laundry-Supplies/N-5yc1vZcb4s",
            "label": "Laundry",
        },
        "cleaning-cleaning-tools-cleaning-brushes": {
            "url": "https://www.homedepot.com/b/Cleaning-Cleaning-Tools-Cleaning-Brushes/N-5yc1vZcb4l",
            "label": "Cleaning Brushes",
        },
        "cleaning-cleaning-tools-power-scrubbers": {
            "url": "https://www.homedepot.com/b/Cleaning-Cleaning-Tools-Power-Scrubbers/N-5yc1vZ2fkpe6x",
            "label": "Power Scrubbers",
        },
        "cleaning-cleaning-tools-cleaning-cloths": {
            "url": "https://www.homedepot.com/b/Cleaning-Cleaning-Tools-Cleaning-Cloths/N-5yc1vZcb3m",
            "label": "Cleaning Cloths",
        },
        "cleaning-household-essentials-toilet-paper": {
            "url": "https://www.homedepot.com/b/Cleaning-Household-Essentials-Toilet-Paper/N-5yc1vZcb2k",
            "label": "Toilet Paper",
        },
        "cleaning-cleaning-supplies-drain-cleaners": {
            "url": "https://www.homedepot.com/b/Cleaning-Cleaning-Supplies-Drain-Cleaners/N-5yc1vZbqlj",
            "label": "Drain Cleaners",
        },
        "cleaning": {
            "url": "https://www.homedepot.com/b/Cleaning/N-5yc1vZbqsi",
            "label": "Cleaning",
        },
    },
    "home-decor": {
        "home-decor-home-accents": {
            "url": "https://www.homedepot.com/b/Home-Decor-Home-Accents/N-5yc1vZar58",
            "label": "Home Accents",
        },
        "home-decor-mirrors": {
            "url": "https://www.homedepot.com/b/Home-Decor-Mirrors/N-5yc1vZbve6",
            "label": "Mirrors",
        },
        "home-decor-wall-decor-wall-art": {
            "url": "https://www.homedepot.com/b/Home-Decor-Wall-Decor-Wall-Art/N-5yc1vZbbzh",
            "label": "Wall Art",
        },
        "home-decor-wallpaper": {
            "url": "https://www.homedepot.com/b/Home-Decor-Wallpaper/N-5yc1vZbc0q",
            "label": "Wallpaper",
        },
        "home-decor-bedding-bath-comforters": {
            "url": "https://www.homedepot.com/b/Home-Decor-Bedding-Bath-Comforters/N-5yc1vZc1jz",
            "label": "Comforters & Comforter Sets",
        },
        "home-decor-artificial-plants": {
            "url": "https://www.homedepot.com/b/Home-Decor-Artificial-Plants/N-5yc1vZbpdg",
            "label": "Artificial Plants",
        },
        "home-decor": {
            "url": "https://www.homedepot.com/b/Home-Decor/N-5yc1vZas6p",
            "label": "Home Décor",
        },
    },
    "lighting": {
        "lighting-light-bulbs": {
            "url": "https://www.homedepot.com/b/Lighting-Light-Bulbs/N-5yc1vZbmbu",
            "label": "Light Bulbs",
        },
        "lighting-flush-mount-ceiling-lights": {
            "url": "https://www.homedepot.com/b/Lighting-Flush-Mount-Ceiling-Lights/N-5yc1vZc7nk",
            "label": "Flush Mount Lights",
        },
        "lighting-chandeliers": {
            "url": "https://www.homedepot.com/b/Lighting-Chandeliers/N-5yc1vZc7o0",
            "label": "Chandeliers",
        },
        "lighting-pendant-lights": {
            "url": "https://www.homedepot.com/b/Lighting-Pendant-Lights/N-5yc1vZc7nu",
            "label": "Pendants",
        },
        "lighting-lamps": {
            "url": "https://www.homedepot.com/b/Lighting-Lamps/N-5yc1vZc7pd",
            "label": "Lamps",
        },
        "lighting-vanity-lighting": {
            "url": "https://www.homedepot.com/b/Lighting-Vanity-Lighting/N-5yc1vZc7pr",
            "label": "Vanity Lights",
        },
        "lighting-recessed-lighting": {
            "url": "https://www.homedepot.com/b/Lighting-Recessed-Lighting/N-5yc1vZc7ni",
            "label": "Recessed Lighting",
        },
        "lighting-wall-sconces": {
            "url": "https://www.homedepot.com/b/Lighting-Wall-Sconces/N-5yc1vZc7pi",
            "label": "Sconces",
        },
        "lighting-ceiling-fans": {
            "url": "https://www.homedepot.com/b/Lighting-Ceiling-Fans/N-5yc1vZbvlq",
            "label": "Ceiling Fans",
        },
        "lighting-commercial-lighting": {
            "url": "https://www.homedepot.com/b/Lighting-Commercial-Lighting/N-5yc1vZc7bu",
            "label": "Commercial Lighting",
        },
        "lighting-ambient-lighting": {
            "url": "https://www.homedepot.com/b/Lighting-Ambient-Lighting/N-5yc1vZ2fkpcyh",
            "label": "Ambient Lighting",
        },
        "lighting-novelty-lighting": {
            "url": "https://www.homedepot.com/b/Lighting-Novelty-Lighting/N-5yc1vZ2fkphlr",
            "label": "Novelty Lighting",
        },
        "lighting-outdoor-lighting": {
            "url": "https://www.homedepot.com/b/Lighting-Outdoor-Lighting/N-5yc1vZc7qv",
            "label": "Outdoor Lighting",
        },
        "lighting-outdoor-lighting-outdoor-wall-lighting": {
            "url": "https://www.homedepot.com/b/Lighting-Outdoor-Lighting-Outdoor-Wall-Lighting/N-5yc1vZc7qq",
            "label": "Wall Lights",
        },
        "lighting-outdoor-lighting-landscape-lighting": {
            "url": "https://www.homedepot.com/b/Lighting-Outdoor-Lighting-Landscape-Lighting/N-5yc1vZc7q6",
            "label": "Landscape Lighting",
        },
        "lighting": {
            "url": "https://www.homedepot.com/b/Lighting/N-5yc1vZbvn5",
            "label": "Lighting",
        },
    },
    "doors-windows": {
        "doors-windows-exterior-doors": {
            "url": "https://www.homedepot.com/b/Doors-Windows-Exterior-Doors/N-5yc1vZas82",
            "label": "Exterior Doors",
        },
        "doors-windows-exterior-doors-front-doors": {
            "url": "https://www.homedepot.com/b/Doors-Windows-Exterior-Doors-Front-Doors/N-5yc1vZar90",
            "label": "Front Doors",
        },
        "doors-windows-exterior-doors-patio-doors": {
            "url": "https://www.homedepot.com/b/Doors-Windows-Exterior-Doors-Patio-Doors/N-5yc1vZarqn",
            "label": "Patio Doors",
        },
        "doors-windows-interior-doors": {
            "url": "https://www.homedepot.com/b/Doors-Windows-Interior-Doors/N-5yc1vZc5io",
            "label": "Interior Doors",
        },
        "doors-windows-interior-doors-prehung-doors": {
            "url": "https://www.homedepot.com/b/Doors-Windows-Interior-Doors-Prehung-Doors/N-5yc1vZc5ij",
            "label": "Prehung Doors",
        },
        "doors-windows-interior-doors-slab-doors": {
            "url": "https://www.homedepot.com/b/Doors-Windows-Interior-Doors-Slab-Doors/N-5yc1vZc5ie",
            "label": "Slab Doors",
        },
        "doors-windows-windows": {
            "url": "https://www.homedepot.com/b/Doors-Windows-Windows/N-5yc1vZaq1w",
            "label": "Windows",
        },
        "doors-windows-windows-double-hung-windows": {
            "url": "https://www.homedepot.com/b/Doors-Windows-Windows-Double-Hung-Windows/N-5yc1vZas47",
            "label": "Double-Hung Windows",
        },
        "doors-windows-windows-single-hung-windows": {
            "url": "https://www.homedepot.com/b/Doors-Windows-Windows-Single-Hung-Windows/N-5yc1vZas73",
            "label": "Single-Hung Windows",
        },
        "doors-windows-garage-doors-and-parts-garage-doors": {
            "url": "https://www.homedepot.com/b/Doors-Windows-Garage-Doors-and-Parts-Garage-Doors/N-5yc1vZ2fkpfuk",
            "label": "Garage Doors",
        },
        "doors-windows-garage-door-openers-and-accessories-garage-door-openers": {
            "url": "https://www.homedepot.com/b/Doors-Windows-Garage-Door-Openers-and-Accessories-Garage-Door-Openers/N-5yc1vZ2fkpfum",
            "label": "Garage Door Openers",
        },
        "doors-windows-exterior-shutters": {
            "url": "https://www.homedepot.com/b/Doors-Windows-Exterior-Shutters/N-5yc1vZarch",
            "label": "Exterior Shutters",
        },
        "doors-windows": {
            "url": "https://www.homedepot.com/b/Doors-Windows/N-5yc1vZaqih",
            "label": "Doors & Windows",
        },
    },
    "electrical": {
        "electrical-electrical-boxes-conduit-fittings-conduit-fittings": {
            "url": "https://www.homedepot.com/b/Electrical-Electrical-Boxes-Conduit-Fittings-Conduit-Fittings/N-5yc1vZbohk",
            "label": "Conduit & Fittings",
        },
        "electrical-electrical-boxes-conduit-fittings-boxes-brackets": {
            "url": "https://www.homedepot.com/b/Electrical-Electrical-Boxes-Conduit-Fittings-Boxes-Brackets/N-5yc1vZbohn",
            "label": "Electrical Boxes & Brackets",
        },
        "electrical-electrical-boxes-conduit-fittings-weatherproof-boxes": {
            "url": "https://www.homedepot.com/b/Electrical-Electrical-Boxes-Conduit-Fittings-Weatherproof-Boxes/N-5yc1vZca29",
            "label": "Weatherproof Boxes",
        },
        "electrical-wiring-devices-light-controls": {
            "url": "https://www.homedepot.com/b/Electrical-Wiring-Devices-Light-Controls/N-5yc1vZc34h",
            "label": "Wiring Devices & Light Controls",
        },
        "electrical-wire": {
            "url": "https://www.homedepot.com/b/Electrical-Wire/N-5yc1vZbm7v",
            "label": "Wire",
        },
        "electrical-wall-plates": {
            "url": "https://www.homedepot.com/b/Electrical-Wall-Plates/N-5yc1vZbm8m",
            "label": "Wall Plates",
        },
        "electrical-electrical-cords": {
            "url": "https://www.homedepot.com/b/Electrical-Electrical-Cords/N-5yc1vZc4mz",
            "label": "Extension Cords & Surge Protectors",
        },
        "electrical-power-distribution-electrical-panels-protective-devices-circuit-breakers": {
            "url": "https://www.homedepot.com/b/Electrical-Power-Distribution-Electrical-Panels-Protective-Devices-Circuit-Breakers/N-5yc1vZbm16",
            "label": "Circuit Breakers",
        },
        "electrical-power-distribution-electrical-panels-protective-devices-breaker-boxes": {
            "url": "https://www.homedepot.com/b/Electrical-Power-Distribution-Electrical-Panels-Protective-Devices-Breaker-Boxes/N-5yc1vZbm2w",
            "label": "Breaker Boxes",
        },
        "electrical-power-distribution-temporary-power-disconnects-safety-switches": {
            "url": "https://www.homedepot.com/b/Electrical-Power-Distribution-Temporary-Power-Disconnects-Safety-Switches/N-5yc1vZbtvq",
            "label": "Safety Switches",
        },
        "electrical-electrical-tools": {
            "url": "https://www.homedepot.com/b/Electrical-Electrical-Tools/N-5yc1vZbmc2",
            "label": "Electrical Tools",
        },
        "electrical-electrical-tools-electrical-testers": {
            "url": "https://www.homedepot.com/b/Electrical-Electrical-Tools-Electrical-Testers/N-5yc1vZboff",
            "label": "Electric Testers",
        },
        "electrical-fire-safety": {
            "url": "https://www.homedepot.com/b/Electrical-Fire-Safety/N-5yc1vZbmgb",
            "label": "Smoke Detectors & Fire Safety",
        },
        "electrical-renewable-energy": {
            "url": "https://www.homedepot.com/b/Electrical-Renewable-Energy/N-5yc1vZbm2y",
            "label": "Renewable Energy",
        },
        "electrical-home-security": {
            "url": "https://www.homedepot.com/b/Electrical-Home-Security/N-5yc1vZc1tg",
            "label": "Home Security",
        },
        "electrical": {
            "url": "https://www.homedepot.com/b/Electrical/N-5yc1vZarcd",
            "label": "Electrical",
        },
    },
    "flooring": {
        "flooring-rugs-area-rugs": {
            "url": "https://www.homedepot.com/b/Flooring-Rugs-Area-Rugs/N-5yc1vZarjg",
            "label": "Rugs",
        },
        "flooring-vinyl-flooring": {
            "url": "https://www.homedepot.com/b/Flooring-Vinyl-Flooring/N-5yc1vZapwr",
            "label": "Vinyl Flooring",
        },
        "flooring-tile": {
            "url": "https://www.homedepot.com/b/Flooring-Tile/N-5yc1vZar0y",
            "label": "Tile",
        },
        "flooring-laminate-flooring": {
            "url": "https://www.homedepot.com/b/Flooring-Laminate-Flooring/N-5yc1vZare1",
            "label": "Laminate Flooring",
        },
        "flooring-hardwood-flooring": {
            "url": "https://www.homedepot.com/b/Flooring-Hardwood-Flooring/N-5yc1vZaq8x",
            "label": "Hardwood Flooring",
        },
        "flooring-hybrid-resilient-flooring": {
            "url": "https://www.homedepot.com/b/Flooring-Hybrid-Resilient-Flooring/N-5yc1vZ2fkpdm6",
            "label": "Hybrid Resilient Flooring",
        },
        "flooring-carpet": {
            "url": "https://www.homedepot.com/b/Flooring-Carpet/N-5yc1vZarl0",
            "label": "Carpet",
        },
        "flooring-gym-flooring": {
            "url": "https://www.homedepot.com/b/Flooring-Gym-Flooring/N-5yc1vZb97i",
            "label": "Gym Flooring",
        },
        "flooring-garage-flooring": {
            "url": "https://www.homedepot.com/b/Flooring-Garage-Flooring/N-5yc1vZb97t",
            "label": "Garage Flooring",
        },
        "flooring-rugs": {
            "url": "https://www.homedepot.com/b/Flooring-Rugs/N-5yc1vZarfm",
            "label": "Rugs",
        },
        "flooring-flooring-supplies": {
            "url": "https://www.homedepot.com/b/Flooring-Flooring-Supplies/N-5yc1vZcdu0",
            "label": "Flooring Supplies",
        },
        "flooring-under-floor-heating": {
            "url": "https://www.homedepot.com/b/Flooring-Under-Floor-Heating/N-5yc1vZapte",
            "label": "Under Floor Heating",
        },
        "flooring": {
            "url": "https://www.homedepot.com/b/Flooring/N-5yc1vZaq7r",
            "label": "Flooring",
        },
    },
    "hardware": {
        "hardware-fasteners": {
            "url": "https://www.homedepot.com/b/Hardware-Fasteners/N-5yc1vZc255",
            "label": "Screws, Nails & Anchors",
        },
        "hardware-door-hardware": {
            "url": "https://www.homedepot.com/b/Hardware-Door-Hardware/N-5yc1vZc213",
            "label": "Door Hardware",
        },
        "hardware-door-hardware-door-locks": {
            "url": "https://www.homedepot.com/b/Hardware-Door-Hardware-Door-Locks/N-5yc1vZc223",
            "label": "Door Locks",
        },
        "hardware-door-hardware-door-handles": {
            "url": "https://www.homedepot.com/b/Hardware-Door-Hardware-Door-Handles/N-5yc1vZc28z",
            "label": "Door Handles",
        },
        "hardware-door-hardware-door-locks-door-lock-combo-packs": {
            "url": "https://www.homedepot.com/b/Hardware-Door-Hardware-Door-Locks-Door-Lock-Combo-Packs/N-5yc1vZc2g4",
            "label": "Door Lock Combo Packs",
        },
        "hardware-cabinet-hardware": {
            "url": "https://www.homedepot.com/b/Hardware-Cabinet-Hardware/N-5yc1vZc29z",
            "label": "Cabinet Hardware",
        },
        "hardware-mailboxes": {
            "url": "https://www.homedepot.com/b/Hardware-Mailboxes/N-5yc1vZc8f5",
            "label": "Mailboxes",
        },
        "hardware-mailboxes-address-signs": {
            "url": "https://www.homedepot.com/b/Hardware-Mailboxes-Address-Signs/N-5yc1vZcfzy",
            "label": "Address Signs",
        },
        "hardware-weather-stripping": {
            "url": "https://www.homedepot.com/b/Hardware-Weather-Stripping/N-5yc1vZc291",
            "label": "Weather Stripping",
        },
        "hardware-metal-stock": {
            "url": "https://www.homedepot.com/b/Hardware-Metal-Stock/N-5yc1vZc2b9",
            "label": "Metal Stock",
        },
        "hardware-chains-ropes": {
            "url": "https://www.homedepot.com/b/Hardware-Chains-Ropes/N-5yc1vZc2cs",
            "label": "Chains & Ropes",
        },
        "hardware-tie-down-straps": {
            "url": "https://www.homedepot.com/b/Hardware-Tie-Down-Straps/N-5yc1vZc2dn",
            "label": "Tie Down Straps",
        },
        "hardware-signage": {
            "url": "https://www.homedepot.com/b/Hardware-Signage/N-5yc1vZc8f1",
            "label": "Signage",
        },
        "hardware-window-hardware": {
            "url": "https://www.homedepot.com/b/Hardware-Window-Hardware/N-5yc1vZc2ab",
            "label": "Window Hardware",
        },
        "hardware-gate-hardware": {
            "url": "https://www.homedepot.com/b/Hardware-Gate-Hardware/N-5yc1vZc2f1",
            "label": "Gate Hardware",
        },
        "hardware-door-hardware-screen-storm-door-hardware": {
            "url": "https://www.homedepot.com/b/Hardware-Door-Hardware-Screen-Storm-Door-Hardware/N-5yc1vZc2e1",
            "label": "Screen & Storm Door Hardware",
        },
        "hardware-garage-door-hardware": {
            "url": "https://www.homedepot.com/b/Hardware-Garage-Door-Hardware/N-5yc1vZc275",
            "label": "Garage Door Hardware",
        },
        "hardware": {
            "url": "https://www.homedepot.com/b/Hardware/N-5yc1vZc21m",
            "label": "Hardware",
        },
    },
    "heating-venting-cooling": {
        "heating-venting-cooling-air-conditioners": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Air-Conditioners/N-5yc1vZc4me",
            "label": "Air Conditioners",
        },
        "heating-venting-cooling-heaters-space-heaters": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Heaters-Space-Heaters/N-5yc1vZc4lh",
            "label": "Space Heaters",
        },
        "heating-venting-cooling-air-conditioners-central-air-conditioners": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Air-Conditioners-Central-Air-Conditioners/N-5yc1vZc4kd",
            "label": "Central Air Conditioners",
        },
        "heating-venting-cooling-air-conditioners-portable-air-conditioners": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Air-Conditioners-Portable-Air-Conditioners/N-5yc1vZc4m4",
            "label": "Portable Air Conditioners",
        },
        "heating-venting-cooling-air-conditioners-window-air-conditioners": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Air-Conditioners-Window-Air-Conditioners/N-5yc1vZc4lu",
            "label": "Window Air Conditioners",
        },
        "heating-venting-cooling-mini-split-air-conditioners": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Mini-Split-Air-Conditioners/N-5yc1vZc4m1",
            "label": "Mini Split Air Conditioners",
        },
        "heating-venting-cooling-air-conditioners-wall-air-conditioners": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Air-Conditioners-Wall-Air-Conditioners/N-5yc1vZc4md",
            "label": "Wall Air Conditioners",
        },
        "heating-venting-cooling-hvac-supplies": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-HVAC-Supplies/N-5yc1vZc4nl",
            "label": "HVAC Parts & Supplies",
        },
        "heating-venting-cooling-fans": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Fans/N-5yc1vZc4lw",
            "label": "Fans",
        },
        "heating-venting-cooling-evaporative-coolers": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Evaporative-Coolers/N-5yc1vZc4lr",
            "label": "Evaporative Coolers",
        },
        "heating-venting-cooling-air-filters": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Air-Filters/N-5yc1vZc4kw",
            "label": "Air Filters",
        },
        "heating-venting-cooling-dehumidifiers": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Dehumidifiers/N-5yc1vZc4l8",
            "label": "Dehumidifiers",
        },
        "heating-venting-cooling-thermostats": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Thermostats/N-5yc1vZc4lf",
            "label": "Thermostats",
        },
        "heating-venting-cooling-heaters": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling-Heaters/N-5yc1vZc4l7",
            "label": "Heaters",
        },
        "heating-venting-cooling": {
            "url": "https://www.homedepot.com/b/Heating-Venting-Cooling/N-5yc1vZc4k8",
            "label": "Heating, Venting & Cooling",
        },
    },
    "kitchen": {
        "kitchen-kitchen-storage-organization": {
            "url": "https://www.homedepot.com/b/Kitchen-Kitchen-Storage-Organization/N-5yc1vZapu6",
            "label": "Kitchen Storage & Organization",
        },
        "kitchen-kitchenware": {
            "url": "https://www.homedepot.com/b/Kitchen-Kitchenware/N-5yc1vZaqzo",
            "label": "Kitchenware",
        },
        "kitchen-kitchen-cabinets": {
            "url": "https://www.homedepot.com/b/Kitchen-Kitchen-Cabinets/N-5yc1vZas87",
            "label": "Kitchen Cabinets",
        },
        "kitchen-countertops": {
            "url": "https://www.homedepot.com/b/Kitchen-Countertops/N-5yc1vZbmf2",
            "label": "Kitchen Countertops",
        },
        "kitchen-kitchen-sinks": {
            "url": "https://www.homedepot.com/b/Kitchen-Kitchen-Sinks/N-5yc1vZarsa",
            "label": "Kitchen Sinks",
        },
        "kitchen-kitchen-faucets": {
            "url": "https://www.homedepot.com/b/Kitchen-Kitchen-Faucets/N-5yc1vZar0k",
            "label": "Kitchen Faucets",
        },
        "kitchen-kitchen-cabinets-kitchen-cabinet-samples": {
            "url": "https://www.homedepot.com/b/Kitchen-Kitchen-Cabinets-Kitchen-Cabinet-Samples/N-5yc1vZc3b4",
            "label": "Cabinet Samples",
        },
        "kitchen": {
            "url": "https://www.homedepot.com/b/Kitchen/N-5yc1vZar4i",
            "label": "Kitchen",
        },
    },
    "outdoors-garden-center": {
        "outdoors-garden-center-artificial-grass": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Artificial-Grass/N-5yc1vZcdgy",
            "label": "Artificial Grass",
        },
        "outdoors-garden-center-outdoor-plants-garden-flowers": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Outdoor-Plants-Garden-Flowers/N-5yc1vZ2fkp97o",
            "label": "Garden Flowers",
        },
        "outdoors-garden-center-indoor-plants": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Indoor-Plants/N-5yc1vZc8rn",
            "label": "Indoor Plants",
        },
        "outdoors-garden-center-outdoor-plants-garden-flowers-perennials": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Outdoor-Plants-Garden-Flowers-Perennials/N-5yc1vZc8ry",
            "label": "Perennials",
        },
        "outdoors-garden-center-outdoor-plants-garden-flowers-annual-flowers": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Outdoor-Plants-Garden-Flowers-Annual-Flowers/N-5yc1vZc8rm",
            "label": "Annuals",
        },
        "outdoors-garden-center-outdoor-plants-trees": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Outdoor-Plants-Trees/Ship-to-Home/N-5yc1vZc8rq",
            "label": "Trees",
        },
        "outdoors-garden-center-outdoor-plants-bushes-hydrangeas": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Outdoor-Plants-Bushes-Hydrangeas/Ship-to-Home/N-5yc1vZ2fkpcyqZbwo60",
            "label": "Hydrangeas ",
        },
        "outdoors-garden-center-succulents": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Succulents/Ship-to-Home/N-5yc1vZc8s2Zbwo60",
            "label": "Succulents",
        },
        "outdoors-garden-center-outdoor-plants-edible-garden": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Outdoor-Plants-Edible-Garden/N-5yc1vZcg6h",
            "label": "Edible Garden",
        },
        "outdoors-garden-center-garden-tools": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Garden-Tools/N-5yc1vZbx6x",
            "label": "Garden Tools",
        },
        "outdoors-garden-center-landscaping-supplies-soils": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Landscaping-Supplies-Soils/N-5yc1vZbx67",
            "label": "Soils",
        },
        "outdoors-garden-center-landscaping-supplies-mulch": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Landscaping-Supplies-Mulch/N-5yc1vZbx4a",
            "label": "Mulch",
        },
        "outdoors-garden-center-lawn-care-grass-seed": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Lawn-Care-Grass-Seed/N-5yc1vZbx62",
            "label": "Grass Seed",
        },
        "outdoors-garden-center-raised-garden-beds": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Raised-Garden-Beds/N-5yc1vZbx7c",
            "label": "Raised Garden Beds",
        },
        "outdoors-garden-center-greenhouses": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Greenhouses/N-5yc1vZcc4v",
            "label": "Greenhouses",
        },
        "outdoors-garden-center-landscaping-supplies-landscape-rocks": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Landscaping-Supplies-Landscape-Rocks/N-5yc1vZbx5d",
            "label": "Landscape Rocks",
        },
        "outdoors-garden-center-hardscapes-pavers": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Hardscapes-Pavers/N-5yc1vZbx4b",
            "label": "Pavers",
        },
        "outdoors-garden-center-planters-plant-stands": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Planters-Plant-Stands/N-5yc1vZbx7z",
            "label": "Plant Stands",
        },
        "outdoors-garden-center-planters": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Planters/N-5yc1vZbx81",
            "label": "Planters",
        },
        "outdoors-garden-center-watering-irrigation-watering-essentials-garden-hoses": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Watering-Irrigation-Watering-Essentials-Garden-Hoses/N-5yc1vZbx4e",
            "label": "Garden Hoses",
        },
        "outdoors-garden-center-pest-control": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center-Pest-Control/N-5yc1vZbx4w",
            "label": "Insect & Pest Control",
        },
        "outdoors-garden-center": {
            "url": "https://www.homedepot.com/b/Outdoors-Garden-Center/N-5yc1vZbx6k",
            "label": "Garden Center",
        },
    },
    "outdoors": {
        "outdoors-outdoor-power-equipment-lawn-mowers": {
            "url": "https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Lawn-Mowers/N-5yc1vZc5ar",
            "label": "Lawn Mowers",
        },
        "outdoors-patio-furniture": {
            "url": "https://www.homedepot.com/b/Outdoors-Patio-Furniture/N-5yc1vZbx4o",
            "label": "Patio Furniture",
        },
        "outdoors-outdoor-cooking": {
            "url": "https://www.homedepot.com/b/Outdoors-Outdoor-Cooking/N-5yc1vZcfb7",
            "label": "Outdoor Cooking & Grills",
        },
        "outdoors-outdoor-power-equipment": {
            "url": "https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/N-5yc1vZbx5c",
            "label": "Outdoor Power Equipment",
        },
        "outdoors-outdoor-power-equipment-pressure-washers": {
            "url": "https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Pressure-Washers/N-5yc1vZbxbe",
            "label": "Pressure Washers",
        },
        "outdoors-outdoor-power-equipment-generators": {
            "url": "https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment-Generators/N-5yc1vZbx8l",
            "label": "Generators",
        },
        "outdoors-shade-structures-gazebos": {
            "url": "https://www.homedepot.com/b/Outdoors-Shade-Structures-Gazebos/N-5yc1vZbtya",
            "label": "Gazebos",
        },
        "outdoors-pools": {
            "url": "https://www.homedepot.com/b/Outdoors-Pools/N-5yc1vZcfyr",
            "label": "Pools",
        },
        "outdoors-patio-furniture-patio-tables-picnic-tables": {
            "url": "https://www.homedepot.com/b/Outdoors-Patio-Furniture-Patio-Tables-Picnic-Tables/N-5yc1vZccg9",
            "label": "Picnic Tables",
        },
        "outdoors-outdoor-heating-fire-pits": {
            "url": "https://www.homedepot.com/b/Outdoors-Outdoor-Heating-Fire-Pits/N-5yc1vZc6na",
            "label": "Fire Pits",
        },
        "outdoors": {
            "url": "https://www.homedepot.com/b/Outdoors/N-5yc1vZbx82",
            "label": "Outdoors",
        },
    },
    "paint": {
        "paint-ideas": {
            "url": "https://www.homedepot.com/b/Paint-Ideas/popular",
            "label": "Paint Color Wall",
        },
        "paint-interior-paint": {
            "url": "https://www.homedepot.com/b/Paint-Interior-Paint/N-5yc1vZbbbp",
            "label": "Interior Paint",
        },
        "paint-exterior-wood-coatings": {
            "url": "https://www.homedepot.com/b/Paint-Exterior-Wood-Coatings/N-5yc1vZbbbr",
            "label": "Exterior Wood Coatings",
        },
        "paint-exterior-paint": {
            "url": "https://www.homedepot.com/b/Paint-Exterior-Paint/N-5yc1vZcg5u",
            "label": "Exterior Paint",
        },
        "paint-concrete-coatings-concrete-sealers": {
            "url": "https://www.homedepot.com/b/Paint-Concrete-Coatings-Concrete-Sealers/N-5yc1vZcj9b",
            "label": "Concrete Sealers",
        },
        "paint-spray-paint": {
            "url": "https://www.homedepot.com/b/Paint-Spray-Paint/N-5yc1vZapz5",
            "label": "Spray Paint",
        },
        "paint-interior-wood-stains": {
            "url": "https://www.homedepot.com/b/Paint-Interior-Wood-Stains/N-5yc1vZbo8p",
            "label": "Interior Wood Stains",
        },
        "paint-primers": {
            "url": "https://www.homedepot.com/b/Paint-Primers/N-5yc1vZbt0t",
            "label": "Primers",
        },
        "paint-paint-colors": {
            "url": "https://www.homedepot.com/b/Paint-Paint-Colors/8-Ounce/N-5yc1vZcaw8Z1z1dqqg",
            "label": "Paint Samples",
        },
        "paint-paint-supplies": {
            "url": "https://www.homedepot.com/b/Paint-Paint-Supplies/N-5yc1vZci1w",
            "label": "Paint Supplies",
        },
        "paint-paint-supplies-paint-applicators": {
            "url": "https://www.homedepot.com/b/Paint-Paint-Supplies-Paint-Applicators/N-5yc1vZ2fkpdmg",
            "label": "Paint Applicators",
        },
        "paint-paint-supplies-adhesives": {
            "url": "https://www.homedepot.com/b/Paint-Paint-Supplies-Adhesives/N-5yc1vZci1s",
            "label": "Adhesives",
        },
        "paint-paint-supplies-tape": {
            "url": "https://www.homedepot.com/b/Paint-Paint-Supplies-Tape/N-5yc1vZc5dk",
            "label": "Tape",
        },
        "paint-paint-supplies-tarps": {
            "url": "https://www.homedepot.com/b/Paint-Paint-Supplies-Tarps/N-5yc1vZci18",
            "label": "Tarps",
        },
        "paint-paint-supplies-caulk-sealants": {
            "url": "https://www.homedepot.com/b/Paint-Paint-Supplies-Caulk-Sealants/N-5yc1vZc5bp",
            "label": "Caulk & Sealants",
        },
        "paint-paint-supplies-sanding-supplies": {
            "url": "https://www.homedepot.com/b/Paint-Paint-Supplies-Sanding-Supplies/N-5yc1vZc5d2",
            "label": "Sanding Supplies",
        },
        "paint-paint-supplies-patching-repair": {
            "url": "https://www.homedepot.com/b/Paint-Paint-Supplies-Patching-Repair/N-5yc1vZ2fkpd23",
            "label": "Patching & Repair",
        },
        "glidden": {
            "url": "https://www.homedepot.com/b/Glidden/N-5yc1vZ30j",
            "label": "Glidden Paint",
        },
        "kilz": {
            "url": "https://www.homedepot.com/b/KILZ/N-5yc1vZ3my",
            "label": "Kilz Primers",
        },
        "paint": {
            "url": "https://www.homedepot.com/b/Paint/N-5yc1vZar2d",
            "label": "Paint",
        },
    },
    "plumbing": {
        "plumbing-pipe-fittings-pipe": {
            "url": "https://www.homedepot.com/b/Plumbing-Pipe-Fittings-Pipe/N-5yc1vZ1z18i34",
            "label": "Pipe",
        },
        "plumbing-pipe-fittings-fittings": {
            "url": "https://www.homedepot.com/b/Plumbing-Pipe-Fittings-Fittings/N-5yc1vZ1z18i3t",
            "label": "Fittings",
        },
        "plumbing-pipe-fittings-pipe-pvc-pipe": {
            "url": "https://www.homedepot.com/b/Plumbing-Pipe-Fittings-Pipe-PVC-Pipe/N-5yc1vZ1z18i41",
            "label": "PVC Pipe",
        },
        "plumbing-drainage": {
            "url": "https://www.homedepot.com/b/Plumbing-Drainage/N-5yc1vZbv0z",
            "label": "Drainage",
        },
        "plumbing-valves": {
            "url": "https://www.homedepot.com/b/Plumbing-Valves/N-5yc1vZbbl6",
            "label": "Valves",
        },
        "plumbing-water-filters": {
            "url": "https://www.homedepot.com/b/Plumbing-Water-Filters/N-5yc1vZarmz",
            "label": "Water Filters",
        },
        "plumbing-water-filters-water-softeners-water-softener-systems": {
            "url": "https://www.homedepot.com/b/Plumbing-Water-Filters-Water-Softeners-Water-Softener-Systems/N-5yc1vZc6sb",
            "label": "Water Softener Systems",
        },
        "plumbing-water-heaters": {
            "url": "https://www.homedepot.com/b/Plumbing-Water-Heaters/N-5yc1vZbqly",
            "label": "Tank Water Heaters",
        },
        "plumbing-water-heaters-tankless-water-heaters": {
            "url": "https://www.homedepot.com/b/Plumbing-Water-Heaters-Tankless-Water-Heaters/N-5yc1vZ2fkoqer",
            "label": "Tankless Water Heaters",
        },
        "plumbing-plumbing-parts-toilet-parts": {
            "url": "https://www.homedepot.com/b/Plumbing-Plumbing-Parts-Toilet-Parts/N-5yc1vZc69l",
            "label": "Toilet Parts",
        },
        "plumbing-plumbing-tools-drain-cleaning-tools-sewer-machines": {
            "url": "https://www.homedepot.com/b/Plumbing-Plumbing-Tools-Drain-Cleaning-Tools-Sewer-Machines/N-5yc1vZ2fkowh2",
            "label": "Sewer Machines",
        },
        "plumbing-plumbing-tools-drain-cleaning-tools-drain-snakes": {
            "url": "https://www.homedepot.com/b/Plumbing-Plumbing-Tools-Drain-Cleaning-Tools-Drain-Snakes/N-5yc1vZbqoe",
            "label": "Drain Snakes",
        },
        "plumbing-plumbing-tools-drain-cleaning-tools-plungers": {
            "url": "https://www.homedepot.com/b/Plumbing-Plumbing-Tools-Drain-Cleaning-Tools-Plungers/N-5yc1vZbqkv",
            "label": "Toilet Plungers",
        },
        "plumbing-water-pumps": {
            "url": "https://www.homedepot.com/b/Plumbing-Water-Pumps/N-5yc1vZbqlb",
            "label": "Water Pumps",
        },
        "plumbing-utility-laundry-sinks": {
            "url": "https://www.homedepot.com/b/Plumbing-Utility-Laundry-Sinks/N-5yc1vZcgeu",
            "label": "Utility Sinks",
        },
        "plumbing": {
            "url": "https://www.homedepot.com/b/Plumbing/N-5yc1vZbqew",
            "label": "Plumbing",
        },
    },
    "holiday-decorations": {
        "holiday-decorations-halloween-decorations": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Halloween-Decorations/N-5yc1vZc2ve",
            "label": "Shop All Halloween Decorations",
        },
        "holiday-decorations-christmas-decorations": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Christmas-Decorations/N-5yc1vZcgxo",
            "label": "Shop All Christmas Decor",
        },
        "holiday-decorations-christmas-decorations-christmas-trees": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Christmas-Decorations-Christmas-Trees/N-5yc1vZc3rz",
            "label": "Christmas Trees",
        },
        "holiday-decorations-christmas-decorations-christmas-greenery": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Christmas-Decorations-Christmas-Greenery/N-5yc1vZc3tk",
            "label": "Christmas Greenery",
        },
        "holiday-decorations-christmas-decorations-christmas-lights": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Christmas-Decorations-Christmas-Lights/N-5yc1vZc3tb",
            "label": "Christmas Lights",
        },
        "holiday-decorations-christmas-decorations-outdoor-christmas-decorations": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Christmas-Decorations-Outdoor-Christmas-Decorations/N-5yc1vZc3sq",
            "label": "Outdoor Christmas Decorations",
        },
        "holiday-decorations-christmas-decorations-indoor-christmas-decorations-christmas-animatronics": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Christmas-Decorations-Indoor-Christmas-Decorations-Christmas-Animatronics/N-5yc1vZ2fkpfb7",
            "label": "Christmas Animatronics",
        },
        "holiday-decorations-christmas-decorations-outdoor-christmas-decorations-christmas-inflatables": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Christmas-Decorations-Outdoor-Christmas-Decorations-Christmas-Inflatables/N-5yc1vZc3rx",
            "label": "Christmas Inflatables",
        },
        "holiday-decorations-christmas-decorations-indoor-christmas-decorations": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Christmas-Decorations-Indoor-Christmas-Decorations/N-5yc1vZc3rv",
            "label": "Indoor Christmas Decorations",
        },
        "holiday-decorations-fall-decorations": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Fall-Decorations/N-5yc1vZc9qn",
            "label": "Shop All Fall Decor",
        },
        "holiday-decorations-fall-decorations-fall-wreaths": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Fall-Decorations-Fall-Wreaths/N-5yc1vZc2w5",
            "label": "Fall Wreaths",
        },
        "holiday-decorations-fall-decorations-fall-garlands": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Fall-Decorations-Fall-Garlands/N-5yc1vZcks2",
            "label": "Fall Garlands",
        },
        "holiday-decorations-hanukkah-decorations": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Hanukkah-Decorations/N-5yc1vZc2xz",
            "label": "Hanukkah",
        },
        "holiday-decorations-seasonal-decorations": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Seasonal-Decorations/N-5yc1vZch29",
            "label": "Shop All Seasonal Decor",
        },
        "holiday-decorations-party-decorations": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations-Party-Decorations/N-5yc1vZch2a",
            "label": "Party Supplies",
        },
        "holiday-decorations": {
            "url": "https://www.homedepot.com/b/Holiday-Decorations/N-5yc1vZbd6e",
            "label": "Holiday Decorations",
        },
    },
    "smart-home": {
        "smart-home-smart-devices": {
            "url": "https://www.homedepot.com/b/Smart-Home-Smart-Devices/Special-Buys/N-5yc1vZ2fkp3e0Z1z11ao3",
            "label": "Smart Home Savings",
        },
        "blink": {
            "url": "https://www.homedepot.com/b/Blink/N-5yc1vZrko",
            "label": "Blink",
        },
        "smart-home-smart-devices-smart-thermostats": {
            "url": "https://www.homedepot.com/b/Smart-Home-Smart-Devices-Smart-Thermostats/N-5yc1vZc7cl",
            "label": "Smart Thermostats",
        },
        "smart-home-smart-devices-smart-home-security-smart-security-cameras": {
            "url": "https://www.homedepot.com/b/Smart-Home-Smart-Devices-Smart-Home-Security-Smart-Security-Cameras/N-5yc1vZc7ce",
            "label": "Smart Cameras",
        },
        "smart-home-smart-devices-smart-home-security-smart-doorbells": {
            "url": "https://www.homedepot.com/b/Smart-Home-Smart-Devices-Smart-Home-Security-Smart-Doorbells/N-5yc1vZccbt",
            "label": "Smart Doorbells",
        },
        "smart-home-smart-devices-smart-home-security-smart-locks": {
            "url": "https://www.homedepot.com/b/Smart-Home-Smart-Devices-Smart-Home-Security-Smart-Locks/N-5yc1vZc7by",
            "label": "Smart Locks",
        },
        "smart-home-smart-lighting": {
            "url": "https://www.homedepot.com/b/Smart-Home-Smart-Lighting/N-5yc1vZc7c8",
            "label": "Smart Lights",
        },
        "smart-home-smart-wiring-devices-smart-light-switches": {
            "url": "https://www.homedepot.com/b/Smart-Home-Smart-Wiring-Devices-Smart-Light-Switches/N-5yc1vZc7cc",
            "label": "Smart Light Switches",
        },
        "smart-home-smart-devices-smart-home-systems-smart-routers": {
            "url": "https://www.homedepot.com/b/Smart-Home-Smart-Devices-Smart-Home-Systems-Smart-Routers/N-5yc1vZc21b",
            "label": "Routers",
        },
        "smart-home": {
            "url": "https://www.homedepot.com/b/Smart-Home/N-5yc1vZc1jw",
            "label": "Smart Home",
        },
    },
    "storage-organization": {
        "storage-organization-outdoor-storage-sheds": {
            "url": "https://www.homedepot.com/b/Storage-Organization-Outdoor-Storage-Sheds/N-5yc1vZbtz2",
            "label": "Sheds",
        },
        "garage-storage-bins": {
            "url": "https://www.homedepot.com/b/Garage-Storage-Bins/N-5yc1vZcl3z",
            "label": "Storage Containers",
        },
        "storage-organization-closet-organizers": {
            "url": "https://www.homedepot.com/b/Storage-Organization-Closet-Organizers/N-5yc1vZc1x1",
            "label": "Closet Organizers",
        },
        "storage-organization-closet-organizers-closet-accessories": {
            "url": "https://www.homedepot.com/b/Storage-Organization-Closet-Organizers-Closet-Accessories/N-5yc1vZc89g",
            "label": "Closet Accessories",
        },
        "storage-organization-moving-supplies": {
            "url": "https://www.homedepot.com/b/Storage-Organization-Moving-Supplies/N-5yc1vZc89r",
            "label": "Moving Boxes & Supplies",
        },
        "storage-organization-outdoor-storage": {
            "url": "https://www.homedepot.com/b/Storage-Organization-Outdoor-Storage/N-5yc1vZbu96",
            "label": "Outdoor Storage",
        },
        "storage-organization-laundry-room-storage": {
            "url": "https://www.homedepot.com/b/Storage-Organization-Laundry-Room-Storage/N-5yc1vZc89h",
            "label": "Laundry Storage",
        },
        "storage-organization-folding-furniture": {
            "url": "https://www.homedepot.com/b/Storage-Organization-Folding-Furniture/N-5yc1vZ2fkpdux",
            "label": "Folding Furniture",
        },
        "garage-tool-storage": {
            "url": "https://www.homedepot.com/b/Garage-Tool-Storage/N-5yc1vZc22e",
            "label": "Tool Storage",
        },
        "garage-garage-storage": {
            "url": "https://www.homedepot.com/b/Garage-Garage-Storage/N-5yc1vZarmi",
            "label": "Garage Storage",
        },
        "garage-garage-storage-garage-wall-organization": {
            "url": "https://www.homedepot.com/b/Garage-Garage-Storage-Garage-Wall-Organization/N-5yc1vZccyo",
            "label": "Garage Wall Organization",
        },
        "storage-organization-garage-storage-garage-cabinets": {
            "url": "https://www.homedepot.com/b/Storage-Organization-Garage-Storage-Garage-Cabinets/N-5yc1vZccv5",
            "label": "Garage Cabinets",
        },
        "garage-garage-storage-garage-storage-systems": {
            "url": "https://www.homedepot.com/b/Garage-Garage-Storage-Garage-Storage-Systems/N-5yc1vZ2fkookg",
            "label": "Garage Storage Systems",
        },
        "garage-garage-storage-garage-shelving": {
            "url": "https://www.homedepot.com/b/Garage-Garage-Storage-Garage-Shelving/N-5yc1vZ2fkoolb",
            "label": "Garage Shelving",
        },
        "garage-garage-storage-overhead-garage-storage": {
            "url": "https://www.homedepot.com/b/Garage-Garage-Storage-Overhead-Garage-Storage/N-5yc1vZ2fkp9in",
            "label": "Overhead Garage Storage",
        },
        "storage-organization": {
            "url": "https://www.homedepot.com/b/Storage-Organization/N-5yc1vZas7e",
            "label": "Storage & Organization",
        },
    },
    "tools": {
        "tools-power-tools": {
            "url": "https://www.homedepot.com/b/Tools-Power-Tools/N-5yc1vZc298",
            "label": "Power Tools",
        },
        "tools-hand-tools": {
            "url": "https://www.homedepot.com/b/Tools-Hand-Tools/N-5yc1vZc1zg",
            "label": "Hand Tools",
        },
        "tools-tool-storage": {
            "url": "https://www.homedepot.com/b/Tools-Tool-Storage/N-5yc1vZc22e",
            "label": "Tool Storage",
        },
        "tools-power-tool-accessories": {
            "url": "https://www.homedepot.com/b/Tools-Power-Tool-Accessories/N-5yc1vZc246",
            "label": "Power Tool Accessories",
        },
        "tools-power-tool-batteries": {
            "url": "https://www.homedepot.com/b/Tools-Power-Tool-Batteries/N-5yc1vZc809",
            "label": "Power Tool Batteries",
        },
        "tools-air-compressor-tools": {
            "url": "https://www.homedepot.com/b/Tools-Air-Compressor-Tools/N-5yc1vZc2fh",
            "label": "Air Compressors & Air Tools",
        },
        "tools-woodworking-tools": {
            "url": "https://www.homedepot.com/b/Tools-Woodworking-Tools/N-5yc1vZc2gv",
            "label": "Woodworking Tools",
        },
        "safety-equipment": {
            "url": "https://www.homedepot.com/b/Safety-Equipment/N-5yc1vZc4ow",
            "label": "Workwear & Safety Equipment",
        },
        "garage-shop-vacuums": {
            "url": "https://www.homedepot.com/b/Garage-Shop-Vacuums/N-5yc1vZc2a7",
            "label": "Wet & Dry Vacuums",
        },
        "tools-welding-soldering": {
            "url": "https://www.homedepot.com/b/Tools-Welding-Soldering/N-5yc1vZc8lp",
            "label": "Welding & Soldering",
        },
        "tools-safety-security-home-safety-child-safety-baby-monitors": {
            "url": "https://www.homedepot.com/b/Tools-Safety-Security-Home-Safety-Child-Safety-Baby-Monitors/N-5yc1vZc24m",
            "label": "Baby Monitors",
        },
        "tools": {
            "url": "https://www.homedepot.com/b/Tools/N-5yc1vZc1xy",
            "label": "Tools",
        },
    },
    "automotive": {
        "garage-automotive-mechanics-tools": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Mechanics-Tools/N-5yc1vZclb1",
            "label": "Mechanics Tools",
        },
        "garage-automotive-shop-equipment": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Shop-Equipment/N-5yc1vZc8mr",
            "label": "Shop Equipment",
        },
        "garage-automotive-shop-equipment-car-jacks": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Shop-Equipment-Car-Jacks/N-5yc1vZc8mp",
            "label": "Car Jacks",
        },
        "garage-automotive-shop-equipment-car-lifts": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Shop-Equipment-Car-Lifts/N-5yc1vZc8mw",
            "label": "Car Lifts",
        },
        "garage-automotive-auto-parts": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Auto-Parts/N-5yc1vZc8ss",
            "label": "Auto Parts",
        },
        "garage-automotive-battery-charging-systems": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Battery-Charging-Systems/N-5yc1vZc8m6",
            "label": "Battery Charging Systems ",
        },
        "garage-automotive-battery-charging-systems-automotive-batteries": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Battery-Charging-Systems-Automotive-Batteries/N-5yc1vZ2fkph6t",
            "label": "Automotive Batteries",
        },
        "garage-automotive-boat-supplies": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Boat-Supplies/N-5yc1vZclrc",
            "label": "Boat Supplies ",
        },
        "garage-automotive-car-cleaning-supplies": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Car-Cleaning-Supplies/N-5yc1vZc8ne",
            "label": "Car Cleaning Supplies ",
        },
        "garage-automotive-car-fluids-chemicals": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Car-Fluids-Chemicals/N-5yc1vZ2fkot4v",
            "label": "Car Fluids & Chemicals ",
        },
        "garage-automotive-cargo-carriers": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Cargo-Carriers/N-5yc1vZc8ly",
            "label": "Cargo Carriers ",
        },
        "garage-automotive-exterior-car-accessories": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Exterior-Car-Accessories/N-5yc1vZc8n1",
            "label": "Exterior Car Accessories ",
        },
        "garage-automotive-interior-car-accessories": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Interior-Car-Accessories/N-5yc1vZclal",
            "label": "Interior Car Accessories",
        },
        "garage-automotive-rv-supplies": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-RV-Supplies/N-5yc1vZclre",
            "label": "RV Supplies ",
        },
        "garage-automotive-tire-accessories": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Tire-Accessories/N-5yc1vZc8sw",
            "label": "Tire Accessories ",
        },
        "garage-automotive-tires": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Tires/N-5yc1vZc8m4",
            "label": "Tires ",
        },
        "garage-automotive-towing-equipment": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Towing-Equipment/N-5yc1vZc8n0",
            "label": "Towing Equipment ",
        },
        "garage-automotive-truck-accessories": {
            "url": "https://www.homedepot.com/b/Garage-Automotive-Truck-Accessories/N-5yc1vZ1z18ier",
            "label": "Truck Accessories ",
        },
        "automotive": {
            "url": "https://www.homedepot.com/b/Automotive/N-5yc1vZc8o1",
            "label": "Automotive",
        },
    },
    "furniture": {
        "furniture-living-room-furniture": {
            "url": "https://www.homedepot.com/b/Furniture-Living-Room-Furniture/N-5yc1vZc7p3",
            "label": "Living Room Furniture",
        },
        "furniture-kitchen-dining-room-furniture": {
            "url": "https://www.homedepot.com/b/Furniture-Kitchen-Dining-Room-Furniture/N-5yc1vZc7ou",
            "label": "Kitchen & Dining Furniture",
        },
        "furniture-bedroom-furniture": {
            "url": "https://www.homedepot.com/b/Furniture-Bedroom-Furniture/N-5yc1vZc7pe",
            "label": "Bedroom Furniture",
        },
        "furniture-home-office-furniture": {
            "url": "https://www.homedepot.com/b/Furniture-Home-Office-Furniture/N-5yc1vZc7np",
            "label": "Home Office Furniture",
        },
        "furniture-entryway-furniture": {
            "url": "https://www.homedepot.com/b/Furniture-Entryway-Furniture/N-5yc1vZc7oz",
            "label": "Entryway Furniture",
        },
        "furniture-bedroom-furniture-mattresses": {
            "url": "https://www.homedepot.com/b/Furniture-Bedroom-Furniture-Mattresses/N-5yc1vZc7oe",
            "label": "Mattresses",
        },
        "furniture-bedroom-furniture-bedroom-sets": {
            "url": "https://www.homedepot.com/b/Furniture-Bedroom-Furniture-Bedroom-Sets/N-5yc1vZc7ow",
            "label": "Bedroom Sets",
        },
        "furniture-bedroom-furniture-beds": {
            "url": "https://www.homedepot.com/b/Furniture-Bedroom-Furniture-Beds/N-5yc1vZc7oh",
            "label": "Beds",
        },
        "furniture-bedroom-furniture-makeup-vanities": {
            "url": "https://www.homedepot.com/b/Furniture-Bedroom-Furniture-Makeup-Vanities/N-5yc1vZc7oc",
            "label": "Makeup Vanities",
        },
        "furniture-kitchen-dining-room-furniture-kitchen-islands": {
            "url": "https://www.homedepot.com/b/Furniture-Kitchen-Dining-Room-Furniture-Kitchen-Islands/N-5yc1vZcf2b",
            "label": "Kitchen Islands",
        },
        "furniture-living-room-furniture-living-room-sets": {
            "url": "https://www.homedepot.com/b/Furniture-Living-Room-Furniture-Living-Room-Sets/N-5yc1vZck6q",
            "label": "Living Room Sets",
        },
        "furniture-living-room-furniture-massage-chairs": {
            "url": "https://www.homedepot.com/b/Furniture-Living-Room-Furniture-Massage-Chairs/N-5yc1vZcf8w",
            "label": "Massage Chairs",
        },
        "furniture-living-room-furniture-tv-stands": {
            "url": "https://www.homedepot.com/b/Furniture-Living-Room-Furniture-TV-Stands/N-5yc1vZcfct",
            "label": "TV Stands",
        },
        "furniture-bar-furniture": {
            "url": "https://www.homedepot.com/b/Furniture-Bar-Furniture/N-5yc1vZ2fkpaag",
            "label": "Bar Furniture",
        },
        "furniture-bar-furniture-bar-stools": {
            "url": "https://www.homedepot.com/b/Furniture-Bar-Furniture-Bar-Stools/N-5yc1vZc7of",
            "label": "Bar Stools",
        },
        "furniture-furniture-accessories-replacement-parts": {
            "url": "https://www.homedepot.com/b/Furniture-Furniture-Accessories-Replacement-Parts/N-5yc1vZc7ns",
            "label": "Furniture Accessories & Replacement Parts",
        },
        "furniture": {
            "url": "https://www.homedepot.com/b/Furniture/N-5yc1vZc7pc",
            "label": "Furniture",
        },
    },
    "baby-kids": {
        "baby-kids-nursery-nursery-baby-furniture": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Nursery-Nursery-Baby-Furniture/N-5yc1vZcevp",
            "label": "Baby Furniture",
        },
        "baby-kids-kids-home-kids-furniture": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Kids-Home-Kids-Furniture/N-5yc1vZc8rc",
            "label": "Kids Furniture",
        },
        "baby-kids-nursery-nursery-baby-furniture-cribs": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Nursery-Nursery-Baby-Furniture-Cribs/N-5yc1vZcevy",
            "label": "Cribs",
        },
        "baby-kids-nursery-nursery-baby-furniture-crib-mattresses": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Nursery-Nursery-Baby-Furniture-Crib-Mattresses/N-5yc1vZ2fkp9n3",
            "label": "Crib Mattresses",
        },
        "baby-kids-nursery-baby-bedding-crib-bedding": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Nursery-Baby-Bedding-Crib-Bedding/N-5yc1vZcfao",
            "label": "Crib Bedding",
        },
        "baby-kids-nursery-nursery-baby-furniture-nursery-dressers": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Nursery-Nursery-Baby-Furniture-Nursery-Dressers/N-5yc1vZcew9",
            "label": "Nursery Dressers",
        },
        "baby-kids-nursery-nursery-baby-furniture-nursery-chairs": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Nursery-Nursery-Baby-Furniture-Nursery-Chairs/N-5yc1vZ2fkpfuo",
            "label": "Nursery Chairs",
        },
        "baby-kids-nursery-nursery-baby-furniture-changing-tables": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Nursery-Nursery-Baby-Furniture-Changing-Tables/N-5yc1vZcevv",
            "label": "Changing Tables",
        },
        "baby-kids-kids-home-kids-furniture-kids-bedroom-furniture-bunk-beds": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Kids-Home-Kids-Furniture-Kids-Bedroom-Furniture-Bunk-Beds/N-5yc1vZcijj",
            "label": "Bunk Beds",
        },
        "baby-kids-kids-home-kids-furniture-kids-bedroom-furniture-loft-beds": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Kids-Home-Kids-Furniture-Kids-Bedroom-Furniture-Loft-Beds/N-5yc1vZ2fkp97d",
            "label": "Loft Beds",
        },
        "baby-kids-kids-home-kids-furniture-kids-bedroom-furniture-kids-beds": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Kids-Home-Kids-Furniture-Kids-Bedroom-Furniture-Kids-Beds/N-5yc1vZcf89",
            "label": "Kids Beds",
        },
        "baby-kids-kids-home-kids-bedding-sets": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Kids-Home-Kids-Bedding-Sets/N-5yc1vZ2fkok7m",
            "label": "Kids Bedding Sets",
        },
        "baby-kids-kids-home-kids-furniture-kids-bedroom-furniture-kids-dressers": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Kids-Home-Kids-Furniture-Kids-Bedroom-Furniture-Kids-Dressers/N-5yc1vZcf7z",
            "label": "Kids Dressers",
        },
        "baby-kids-kids-home-kids-furniture-kids-bedroom-furniture-kids-bookshelves": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Kids-Home-Kids-Furniture-Kids-Bedroom-Furniture-Kids-Bookshelves/N-5yc1vZcf92",
            "label": "Kids Bookshelves",
        },
        "baby-kids-kids-home-kids-furniture-kids-bedroom-furniture-kids-nightstands": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Kids-Home-Kids-Furniture-Kids-Bedroom-Furniture-Kids-Nightstands/N-5yc1vZcf8y",
            "label": "Kids Nightstands",
        },
        "baby-kids-kids-home-kids-furniture-kids-bedroom-furniture-kids-vanities": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Kids-Home-Kids-Furniture-Kids-Bedroom-Furniture-Kids-Vanities/N-5yc1vZ2fkpfuf",
            "label": "Kids Vanities",
        },
        "baby-kids-kids-home-kids-furniture-kids-playroom-kids-chairs": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Kids-Home-Kids-Furniture-Kids-Playroom-Kids-Chairs/N-5yc1vZciir",
            "label": "Kids Chairs",
        },
        "baby-kids-kids-home-kids-storage-toy-boxes": {
            "url": "https://www.homedepot.com/b/Baby-Kids-Kids-Home-Kids-Storage-Toy-Boxes/N-5yc1vZ2fkp97g",
            "label": "Toy Boxes",
        },
        "baby-kids": {
            "url": "https://www.homedepot.com/b/Baby-Kids/N-5yc1vZ2fkpfui",
            "label": "Baby & Kids",
        },
    },
}
