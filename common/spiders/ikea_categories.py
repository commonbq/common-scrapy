import json

IKE_A_CATEGORIES = json.loads(r'''
{
  "Storage & organization": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/storage-organization-st001/"
    },
    {
      "name": "Dressers & storage drawers",
      "url": "https://www.ikea.com/us/en/cat/dressers-storage-drawers-st004/"
    },
    {
      "name": "Shelving furniture",
      "url": "https://www.ikea.com/us/en/cat/bookcases-shelving-units-st002/"
    },
    {
      "name": "Storage solution systems",
      "url": "https://www.ikea.com/us/en/cat/storage-solution-systems-46052/"
    },
    {
      "name": "Display & storage cabinets",
      "url": "https://www.ikea.com/us/en/cat/display-storage-cabinets-st003/"
    },
    {
      "name": "Armoires & wardrobes",
      "url": "https://www.ikea.com/us/en/cat/armoires-wardrobes-19053/"
    },
    {
      "name": "TV & media furniture",
      "url": "https://www.ikea.com/us/en/cat/tv-media-furniture-10475/"
    },
    {
      "name": "Living room & entryway tables",
      "url": "https://www.ikea.com/us/en/cat/sideboards-buffets-sofa-tables-30454/"
    },
    {
      "name": "Rolling utility & storage carts",
      "url": "https://www.ikea.com/us/en/cat/utility-storage-carts-fu005/"
    },
    {
      "name": "Garage storage solutions",
      "url": "https://www.ikea.com/us/en/cat/garage-storage-700440/"
    },
    {
      "name": "Outdoor storage: shelves, cabinets & boxes",
      "url": "https://www.ikea.com/us/en/cat/outdoor-organizing-21958/"
    },
    {
      "name": "Room dividers",
      "url": "https://www.ikea.com/us/en/cat/room-dividers-46080/"
    },
    {
      "name": "Hallway furniture sets",
      "url": "https://www.ikea.com/us/en/cat/hallway-furniture-sets-700411/"
    },
    {
      "name": "Filing cabinets",
      "url": "https://www.ikea.com/us/en/cat/storage-cabinets-10385/"
    },
    {
      "name": "Shoe cabinets",
      "url": "https://www.ikea.com/us/en/cat/shoe-cabinets-10456/"
    },
    {
      "name": "Kids storage & organization",
      "url": "https://www.ikea.com/us/en/cat/kids-storage-organization-18706/"
    }
  ],
  "Sofas & armchairs": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/sofas-armchairs-700640/"
    },
    {
      "name": "Sofas & sectionals",
      "url": "https://www.ikea.com/us/en/cat/sofas-sectionals-fu003/"
    },
    {
      "name": "Sleeper sofas & sofa beds",
      "url": "https://www.ikea.com/us/en/cat/sleeper-sofas-10663/"
    },
    {
      "name": "Armchairs & accent chairs",
      "url": "https://www.ikea.com/us/en/cat/armchairs-chaises-fu006/"
    },
    {
      "name": "Ottomans, footstools & poufs",
      "url": "https://www.ikea.com/us/en/cat/ottomans-20926/"
    },
    {
      "name": "Chaise lounges",
      "url": "https://www.ikea.com/us/en/cat/chaise-lounges-57527/"
    },
    {
      "name": "Sofa & armchair cushions & headrests",
      "url": "https://www.ikea.com/us/en/cat/sofa-cushions-57536/"
    },
    {
      "name": "Sofa legs",
      "url": "https://www.ikea.com/us/en/cat/sofa-legs-31785/"
    },
    {
      "name": "Sofa & armchairs covers",
      "url": "https://www.ikea.com/us/en/cat/sofa-covers-10664/"
    },
    {
      "name": "Modular sofas",
      "url": "https://www.ikea.com/us/en/cat/sofa-modules-31786/"
    }
  ],
  "Beds & mattresses": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/beds-mattresses-bm001/"
    },
    {
      "name": "Beds",
      "url": "https://www.ikea.com/us/en/cat/beds-bm003/"
    },
    {
      "name": "Mattresses",
      "url": "https://www.ikea.com/us/en/cat/mattresses-bm002/"
    },
    {
      "name": "Bedding & bedding sets",
      "url": "https://www.ikea.com/us/en/cat/bedding-tl004/"
    },
    {
      "name": "Nightstands",
      "url": "https://www.ikea.com/us/en/cat/nightstands-20656/"
    },
    {
      "name": "Underbed storage bags & bins",
      "url": "https://www.ikea.com/us/en/cat/under-bed-storage-19059/"
    },
    {
      "name": "Bedroom furniture sets",
      "url": "https://www.ikea.com/us/en/cat/bedroom-furniture-sets-54992/"
    },
    {
      "name": "Mattresses with bed frame included",
      "url": "https://www.ikea.com/us/en/cat/beds-with-mattresses-included-700513/"
    },
    {
      "name": "Headboards",
      "url": "https://www.ikea.com/us/en/cat/headboards-19064/"
    },
    {
      "name": "Bed slats",
      "url": "https://www.ikea.com/us/en/cat/bed-slats-24827/"
    },
    {
      "name": "Mattress foundations & bases",
      "url": "https://www.ikea.com/us/en/cat/mattress-bases-24825/"
    },
    {
      "name": "Bed frame & headboard covers",
      "url": "https://www.ikea.com/us/en/cat/bed-headboard-covers-57280/"
    },
    {
      "name": "Bed legs",
      "url": "https://www.ikea.com/us/en/cat/bed-legs-24822/"
    }
  ],
  "Lighting": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/lighting-li001/"
    },
    {
      "name": "Lamps & light fixtures",
      "url": "https://www.ikea.com/us/en/cat/lamps-light-fixtures-li002/"
    },
    {
      "name": "Decorative lighting",
      "url": "https://www.ikea.com/us/en/cat/decorative-lighting-14971/"
    },
    {
      "name": "Smart lighting",
      "url": "https://www.ikea.com/us/en/cat/smart-lighting-36812/"
    },
    {
      "name": "Integrated lighting",
      "url": "https://www.ikea.com/us/en/cat/integrated-lighting-16280/"
    },
    {
      "name": "LED light bulbs",
      "url": "https://www.ikea.com/us/en/cat/led-bulbs-20514/"
    },
    {
      "name": "Bathroom lighting",
      "url": "https://www.ikea.com/us/en/cat/bathroom-lighting-10736/"
    },
    {
      "name": "Outdoor lighting",
      "url": "https://www.ikea.com/us/en/cat/outdoor-lighting-17897/"
    },
    {
      "name": "Ceiling fans",
      "url": "https://www.ikea.com/us/en/cat/ceiling-fans-700600/"
    }
  ],
  "Kitchen, appliances & supplies": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/kitchen-appliances-ka001/"
    },
    {
      "name": "Kitchen systems",
      "url": "https://www.ikea.com/us/en/cat/kitchens-ka003/"
    },
    {
      "name": "Kitchen cabinets",
      "url": "https://www.ikea.com/us/en/cat/kitchen-cabinets-700292/"
    },
    {
      "name": "Kitchen doors & drawer fronts",
      "url": "https://www.ikea.com/us/en/cat/kitchen-doors-drawer-fronts-700293/"
    },
    {
      "name": "Kitchen appliances",
      "url": "https://www.ikea.com/us/en/cat/appliances-ka002/"
    },
    {
      "name": "Kitchen countertops",
      "url": "https://www.ikea.com/us/en/cat/kitchen-countertops-24264/"
    },
    {
      "name": "Kitchen islands & carts",
      "url": "https://www.ikea.com/us/en/cat/kitchen-islands-carts-10471/"
    },
    {
      "name": "Kitchen cabinet & drawer organization",
      "url": "https://www.ikea.com/us/en/cat/interior-fittings-24255/"
    },
    {
      "name": "Kitchen organization & wall storage",
      "url": "https://www.ikea.com/us/en/cat/kitchen-wall-storage-20676/"
    },
    {
      "name": "Pantry shelving",
      "url": "https://www.ikea.com/us/en/cat/kitchen-pantry-storage-16200/"
    },
    {
      "name": "Kitchen faucets",
      "url": "https://www.ikea.com/us/en/cat/kitchen-faucets-10482/"
    },
    {
      "name": "Kitchen sinks",
      "url": "https://www.ikea.com/us/en/cat/kitchen-sinks-24263/"
    },
    {
      "name": "Modular kitchens & kitchenettes",
      "url": "https://www.ikea.com/us/en/cat/modular-kitchens-22957/"
    },
    {
      "name": "Knobs and handles",
      "url": "https://www.ikea.com/us/en/cat/cabinet-knobs-handles-pulls-16298/"
    },
    {
      "name": "Kitchen lighting",
      "url": "https://www.ikea.com/us/en/cat/kitchen-lighting-16282/"
    },
    {
      "name": "SEKTION cabinet shelves & drawers",
      "url": "https://www.ikea.com/us/en/cat/sektion-cabinet-shelves-and-drawers-49117/"
    }
  ],
  "Rugs & home textiles": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/home-textiles-tl001/"
    },
    {
      "name": "Bedding & bedding sets",
      "url": "https://www.ikea.com/us/en/cat/bedding-tl004/"
    },
    {
      "name": "Decorative pillows & couch cushion covers",
      "url": "https://www.ikea.com/us/en/cat/decorative-pillows-cushion-covers-10659/"
    },
    {
      "name": "Rugs",
      "url": "https://www.ikea.com/us/en/cat/rugs-10653/"
    },
    {
      "name": "Table linens",
      "url": "https://www.ikea.com/us/en/cat/table-linen-20538/"
    },
    {
      "name": "Blankets & throws",
      "url": "https://www.ikea.com/us/en/cat/blankets-throws-20528/"
    },
    {
      "name": "Bathroom textiles",
      "url": "https://www.ikea.com/us/en/cat/bathroom-textiles-tl003/"
    },
    {
      "name": "Kitchen linens & textiles",
      "url": "https://www.ikea.com/us/en/cat/kitchen-textiles-18850/"
    },
    {
      "name": "Textiles for kids",
      "url": "https://www.ikea.com/us/en/cat/kids-textiles-18730/"
    },
    {
      "name": "Outdoor cushions",
      "url": "https://www.ikea.com/us/en/cat/outdoor-cushions-17893/"
    },
    {
      "name": "Chair pads & seat cushions",
      "url": "https://www.ikea.com/us/en/cat/chair-pads-20542/"
    },
    {
      "name": "Clothing & accessories",
      "url": "https://www.ikea.com/us/en/cat/clothing-accessories-42925/"
    },
    {
      "name": "Baby textiles",
      "url": "https://www.ikea.com/us/en/cat/baby-textiles-18690/"
    },
    {
      "name": "Fabric & sewing accessories",
      "url": "https://www.ikea.com/us/en/cat/fabrics-sewing-10655/"
    },
    {
      "name": "Lumbar support pillows",
      "url": "https://www.ikea.com/us/en/cat/lumbar-support-700528/"
    }
  ],
  "Tables & chairs": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/tables-chairs-fu002/"
    },
    {
      "name": "Dining furniture",
      "url": "https://www.ikea.com/us/en/cat/dining-furniture-700417/"
    },
    {
      "name": "Tables",
      "url": "https://www.ikea.com/us/en/cat/tables-700675/"
    },
    {
      "name": "Chairs",
      "url": "https://www.ikea.com/us/en/cat/chairs-700676/"
    },
    {
      "name": "Benches",
      "url": "https://www.ikea.com/us/en/cat/benches-700319/"
    },
    {
      "name": "Bar furniture",
      "url": "https://www.ikea.com/us/en/cat/bar-furniture-16244/"
    },
    {
      "name": "Accent tables",
      "url": "https://www.ikea.com/us/en/cat/accent-tables-10705/"
    },
    {
      "name": "Kids tables",
      "url": "https://www.ikea.com/us/en/cat/kids-tables-18768/"
    },
    {
      "name": "High chairs",
      "url": "https://www.ikea.com/us/en/cat/high-chairs-45782/"
    },
    {
      "name": "Stools",
      "url": "https://www.ikea.com/us/en/cat/stools-22659/"
    },
    {
      "name": "Café furniture",
      "url": "https://www.ikea.com/us/en/cat/cafe-furniture-19141/"
    },
    {
      "name": "Step stools & step ladders",
      "url": "https://www.ikea.com/us/en/cat/step-stools-step-ladders-20611/"
    },
    {
      "name": "Vanity chairs",
      "url": "https://www.ikea.com/us/en/cat/dressing-table-chairs-stools-59250/"
    },
    {
      "name": "Children's seating",
      "url": "https://www.ikea.com/us/en/cat/childrens-chairs-bc004/"
    }
  ],
  "Desks & desk chairs": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/workspace-desks-chairs-fu004/"
    },
    {
      "name": "Desks & computer desks",
      "url": "https://www.ikea.com/us/en/cat/desks-computer-desks-20649/"
    },
    {
      "name": "Desk chairs",
      "url": "https://www.ikea.com/us/en/cat/desk-chairs-20652/"
    },
    {
      "name": "Gaming furniture",
      "url": "https://www.ikea.com/us/en/cat/gaming-furniture-55002/"
    },
    {
      "name": "Conference tables",
      "url": "https://www.ikea.com/us/en/cat/mittzon-conference-meeting-tables-54173/"
    },
    {
      "name": "Conference table & chair sets",
      "url": "https://www.ikea.com/us/en/cat/conference-table-chair-sets-700424/"
    },
    {
      "name": "Desk & chair sets",
      "url": "https://www.ikea.com/us/en/cat/desk-chair-sets-53249/"
    },
    {
      "name": "Conference chairs",
      "url": "https://www.ikea.com/us/en/cat/conference-chairs-47068/"
    }
  ],
  "Kitchenware & tableware": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/cookware-tableware-kt001/"
    },
    {
      "name": "Dinnerware",
      "url": "https://www.ikea.com/us/en/cat/dinnerware-18860/"
    },
    {
      "name": "Food storage & organizing",
      "url": "https://www.ikea.com/us/en/cat/food-storage-organizing-15937/"
    },
    {
      "name": "Cookware",
      "url": "https://www.ikea.com/us/en/cat/cookware-kt003/"
    },
    {
      "name": "Serveware",
      "url": "https://www.ikea.com/us/en/cat/serveware-16043/"
    },
    {
      "name": "Drinkware",
      "url": "https://www.ikea.com/us/en/cat/drinkware-18868/"
    },
    {
      "name": "Kitchen & cooking accessories",
      "url": "https://www.ikea.com/us/en/cat/cooking-baking-utensils-kt002/"
    },
    {
      "name": "Flatware & cutlery",
      "url": "https://www.ikea.com/us/en/cat/flatware-18865/"
    },
    {
      "name": "Table linens",
      "url": "https://www.ikea.com/us/en/cat/table-linen-20538/"
    },
    {
      "name": "Bakeware & accessories",
      "url": "https://www.ikea.com/us/en/cat/bakeware-20636/"
    },
    {
      "name": "Dishwashing accessories",
      "url": "https://www.ikea.com/us/en/cat/dishwashing-accessories-15938/"
    },
    {
      "name": "Kitchen linens & textiles",
      "url": "https://www.ikea.com/us/en/cat/kitchen-textiles-18850/"
    },
    {
      "name": "Kids tableware & dinnerware",
      "url": "https://www.ikea.com/us/en/cat/kids-kitchenware-tableware-18714/"
    },
    {
      "name": "Coffee & tea accessories",
      "url": "https://www.ikea.com/us/en/cat/coffee-tea-16044/"
    },
    {
      "name": "Knives & cutting boards",
      "url": "https://www.ikea.com/us/en/cat/knives-chopping-boards-15934/"
    },
    {
      "name": "Napkins & napkin holders",
      "url": "https://www.ikea.com/us/en/cat/napkins-napkin-holders-20560/"
    },
    {
      "name": "Outdoor & picnic supplies",
      "url": "https://www.ikea.com/us/en/cat/picnic-outdoor-recreation-42924/"
    },
    {
      "name": "Nursing, feeding & eating",
      "url": "https://www.ikea.com/us/en/cat/nursing-feeding-eating-31772/"
    }
  ],
  "Home decor & accessories": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/home-decor-de001/"
    },
    {
      "name": "Wall décor",
      "url": "https://www.ikea.com/us/en/cat/wall-decor-10757/"
    },
    {
      "name": "Mirrors",
      "url": "https://www.ikea.com/us/en/cat/mirrors-20489/"
    },
    {
      "name": "Plants and flowers",
      "url": "https://www.ikea.com/us/en/cat/plants-flowers-pp003/"
    },
    {
      "name": "Plant pots & stands",
      "url": "https://www.ikea.com/us/en/cat/flower-pots-stands-pp004/"
    },
    {
      "name": "Home fragrances & scents",
      "url": "https://www.ikea.com/us/en/cat/home-fragrance-42926/"
    },
    {
      "name": "Candle holders & candles",
      "url": "https://www.ikea.com/us/en/cat/candle-holders-candles-10760/"
    },
    {
      "name": "Vases & decorating bowls",
      "url": "https://www.ikea.com/us/en/cat/vases-bowls-10769/"
    },
    {
      "name": "Storage boxes & organization bins",
      "url": "https://www.ikea.com/us/en/cat/storage-boxes-baskets-10550/"
    },
    {
      "name": "Bulletin boards, peg boards, pin boards & more",
      "url": "https://www.ikea.com/us/en/cat/noticeboards-10574/"
    },
    {
      "name": "Clocks",
      "url": "https://www.ikea.com/us/en/cat/clocks-10759/"
    },
    {
      "name": "Holiday decor",
      "url": "https://www.ikea.com/us/en/cat/winter-decoration-49149/"
    },
    {
      "name": "Wrapping paper and bags",
      "url": "https://www.ikea.com/us/en/cat/paper-shop-25227/"
    },
    {
      "name": "Table decor & decorative accessories",
      "url": "https://www.ikea.com/us/en/cat/decorative-accessories-24924/"
    }
  ],
  "Baby & kids": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/baby-kids-bc001/"
    },
    {
      "name": "Baby",
      "url": "https://www.ikea.com/us/en/cat/baby-bc002/"
    },
    {
      "name": "Kids",
      "url": "https://www.ikea.com/us/en/cat/kids-bc003/"
    }
  ],
  "Storage containers, organizers & baskets": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/storage-containers-st007/"
    },
    {
      "name": "Storage boxes & organization bins",
      "url": "https://www.ikea.com/us/en/cat/storage-boxes-baskets-10550/"
    },
    {
      "name": "Clothes organizers",
      "url": "https://www.ikea.com/us/en/cat/clothes-organizers-10452/"
    },
    {
      "name": "Desk accessories",
      "url": "https://www.ikea.com/us/en/cat/desk-accessories-10573/"
    },
    {
      "name": "Food storage & organizing",
      "url": "https://www.ikea.com/us/en/cat/food-storage-organizing-15937/"
    },
    {
      "name": "Bathroom accessories & organizers",
      "url": "https://www.ikea.com/us/en/cat/bathroom-accessories-10555/"
    },
    {
      "name": "Paper & media organizers",
      "url": "https://www.ikea.com/us/en/cat/paper-media-organizers-10551/"
    },
    {
      "name": "Recycling bins",
      "url": "https://www.ikea.com/us/en/cat/recycling-bins-34470/"
    },
    {
      "name": "Cable management & cord organizers",
      "url": "https://www.ikea.com/us/en/cat/cable-management-accessories-16195/"
    },
    {
      "name": "Wall shelves & hooks",
      "url": "https://www.ikea.com/us/en/cat/wall-shelves-hooks-st006/"
    },
    {
      "name": "Bags",
      "url": "https://www.ikea.com/us/en/cat/bags-16248/"
    },
    {
      "name": "Moving supplies",
      "url": "https://www.ikea.com/us/en/cat/moving-supplies-46078/"
    }
  ],
  "Bathroom: furniture, supplies & more": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/bathroom-ba001/"
    },
    {
      "name": "Bathroom vanities",
      "url": "https://www.ikea.com/us/en/cat/bathroom-vanities-20719/"
    },
    {
      "name": "Bathroom systems",
      "url": "https://www.ikea.com/us/en/cat/bathroom-systems-700450/"
    },
    {
      "name": "Bathroom shelving units",
      "url": "https://www.ikea.com/us/en/cat/bathroom-shelving-units-20804/"
    },
    {
      "name": "Bathroom accessories & organizers",
      "url": "https://www.ikea.com/us/en/cat/bathroom-accessories-10555/"
    },
    {
      "name": "Bathroom textiles",
      "url": "https://www.ikea.com/us/en/cat/bathroom-textiles-tl003/"
    },
    {
      "name": "Bathroom wall cabinets",
      "url": "https://www.ikea.com/us/en/cat/bathroom-wall-cabinets-20808/"
    },
    {
      "name": "Bathroom faucets & sink taps",
      "url": "https://www.ikea.com/us/en/cat/bathroom-faucets-20724/"
    },
    {
      "name": "Bathroom mirrors",
      "url": "https://www.ikea.com/us/en/cat/bathroom-mirrors-20490/"
    },
    {
      "name": "Bathroom countertop & drawer organizers",
      "url": "https://www.ikea.com/us/en/cat/bathroom-boxes-baskets-16233/"
    },
    {
      "name": "Bathroom storage carts",
      "url": "https://www.ikea.com/us/en/cat/bathroom-carts-20858/"
    },
    {
      "name": "Bathroom stools & benches",
      "url": "https://www.ikea.com/us/en/cat/bathroom-stools-benches-20859/"
    },
    {
      "name": "Bathroom laundry",
      "url": "https://www.ikea.com/us/en/cat/bathroom-laundry-ba003/"
    },
    {
      "name": "Bathroom lighting",
      "url": "https://www.ikea.com/us/en/cat/bathroom-lighting-10736/"
    },
    {
      "name": "Bathroom sinks",
      "url": "https://www.ikea.com/us/en/cat/bathroom-sinks-20723/"
    },
    {
      "name": "Bathroom shelves",
      "url": "https://www.ikea.com/us/en/cat/bathroom-shelves-20615/"
    },
    {
      "name": "Bathroom countertops",
      "url": "https://www.ikea.com/us/en/cat/bathroom-countertops-30565/"
    },
    {
      "name": "Showers",
      "url": "https://www.ikea.com/us/en/cat/showers-40690/"
    }
  ],
  "Outdoor": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/outdoor-od001/"
    },
    {
      "name": "Outdoor patio furniture",
      "url": "https://www.ikea.com/us/en/cat/outdoor-patio-furniture-od003/"
    },
    {
      "name": "Outdoor storage: shelves, cabinets & boxes",
      "url": "https://www.ikea.com/us/en/cat/outdoor-organizing-21958/"
    },
    {
      "name": "Outdoor tiles & flooring",
      "url": "https://www.ikea.com/us/en/cat/outdoor-flooring-21957/"
    },
    {
      "name": "Outdoor kitchen & accessories",
      "url": "https://www.ikea.com/us/en/cat/outdoor-kitchens-700349/"
    },
    {
      "name": "Outdoor patio accessories",
      "url": "https://www.ikea.com/us/en/cat/outdoor-accessories-34203/"
    },
    {
      "name": "Outdoor umbrellas, canopies, gazebos & more",
      "url": "https://www.ikea.com/us/en/cat/umbrellas-gazebos-17887/"
    },
    {
      "name": "Plant accessories",
      "url": "https://www.ikea.com/us/en/cat/outdoor-pots-plants-31787/"
    },
    {
      "name": "Outdoor lighting",
      "url": "https://www.ikea.com/us/en/cat/outdoor-lighting-17897/"
    },
    {
      "name": "Outdoor rugs",
      "url": "https://www.ikea.com/us/en/cat/outdoor-rugs-34204/"
    }
  ],
  "Window treatments & coverings": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/window-treatments-tl002/"
    },
    {
      "name": "Curtains & drapes",
      "url": "https://www.ikea.com/us/en/cat/curtains-10700/"
    },
    {
      "name": "Window blinds and shades",
      "url": "https://www.ikea.com/us/en/cat/blinds-10701/"
    },
    {
      "name": "Curtain rods, rails & holders",
      "url": "https://www.ikea.com/us/en/cat/curtain-rods-rails-18891/"
    },
    {
      "name": "Sewing supplies & accessories",
      "url": "https://www.ikea.com/us/en/cat/sewing-accessories-14350/"
    },
    {
      "name": "Window accessories",
      "url": "https://www.ikea.com/us/en/cat/window-films-accessories-700628/"
    }
  ],
  "Plants & planters": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/plants-planters-pp001/"
    },
    {
      "name": "Plants and flowers",
      "url": "https://www.ikea.com/us/en/cat/plants-flowers-pp003/"
    },
    {
      "name": "Plant pots & stands",
      "url": "https://www.ikea.com/us/en/cat/flower-pots-stands-pp004/"
    },
    {
      "name": "Plant stands",
      "url": "https://www.ikea.com/us/en/cat/plant-stands-movers-20494/"
    },
    {
      "name": "Plant supplies & accessories",
      "url": "https://www.ikea.com/us/en/cat/plant-supplies-accessories-24887/"
    },
    {
      "name": "Watering cans & plant misters",
      "url": "https://www.ikea.com/us/en/cat/watering-cans-20493/"
    },
    {
      "name": "Spray bottles & misters",
      "url": "https://www.ikea.com/us/en/cat/spray-bottles-misters-700778/"
    }
  ],
  "Laundry & cleaning": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/laundry-cleaning-lc001/"
    },
    {
      "name": "Waste sorting",
      "url": "https://www.ikea.com/us/en/cat/bins-bags-16213/"
    },
    {
      "name": "Dishwashing accessories",
      "url": "https://www.ikea.com/us/en/cat/dishwashing-accessories-15938/"
    },
    {
      "name": "Laundry room cabinets & shelving",
      "url": "https://www.ikea.com/us/en/cat/laundry-cabinets-shelving-48925/"
    },
    {
      "name": "Laundry baskets, hampers & bags",
      "url": "https://www.ikea.com/us/en/cat/laundry-baskets-20601/"
    },
    {
      "name": "Laundry accessories",
      "url": "https://www.ikea.com/us/en/cat/laundry-accessories-55004/"
    },
    {
      "name": "Cleaning tools & essentials",
      "url": "https://www.ikea.com/us/en/cat/cleaning-accessories-20609/"
    },
    {
      "name": "Clothes drying racks",
      "url": "https://www.ikea.com/us/en/cat/drying-racks-20602/"
    },
    {
      "name": "Ironing boards & covers",
      "url": "https://www.ikea.com/us/en/cat/ironing-boards-20608/"
    }
  ],
  "IKEA Food & Swedish restaurant": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/ikea-food-restaurant-fb001/"
    },
    {
      "name": "Holiday food",
      "url": "https://www.ikea.com/us/en/cat/holiday-foods-49227/"
    },
    {
      "name": "Side dishes & sauces",
      "url": "https://www.ikea.com/us/en/cat/side-dishes-sauces-49147/"
    },
    {
      "name": "Snacks & sweets",
      "url": "https://www.ikea.com/us/en/cat/snacks-sweets-46192/"
    },
    {
      "name": "Meat",
      "url": "https://www.ikea.com/us/en/cat/meat-25217/"
    },
    {
      "name": "Fish & seafood",
      "url": "https://www.ikea.com/us/en/cat/fish-seafood-25214/"
    },
    {
      "name": "Bread & dairy",
      "url": "https://www.ikea.com/us/en/cat/bread-dairy-25212/"
    },
    {
      "name": "Pastries, desserts & cookies",
      "url": "https://www.ikea.com/us/en/cat/pastries-desserts-cookies-25215/"
    },
    {
      "name": "Condiments & spreads",
      "url": "https://www.ikea.com/us/en/cat/condiments-cheese-jams-25216/"
    },
    {
      "name": "Vegetarian & plant based",
      "url": "https://www.ikea.com/us/en/cat/vegetarian-plant-based-25213/"
    },
    {
      "name": "Beverages",
      "url": "https://www.ikea.com/us/en/cat/beverages-25211/"
    },
    {
      "name": "Summer food",
      "url": "https://www.ikea.com/us/en/cat/summer-food-53254/"
    }
  ],
  "Home electronics": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/home-electronics-he001/"
    },
    {
      "name": "Wireless & home speakers",
      "url": "https://www.ikea.com/us/en/cat/speakers-40842/"
    },
    {
      "name": "Cell phone, tablet & laptop accessories",
      "url": "https://www.ikea.com/us/en/cat/mobile-tablet-accessories-40843/"
    },
    {
      "name": "Charging accessories & power cords",
      "url": "https://www.ikea.com/us/en/cat/cords-chargers-40845/"
    },
    {
      "name": "Cable management & cord organizers",
      "url": "https://www.ikea.com/us/en/cat/cable-management-accessories-16195/"
    },
    {
      "name": "Smart lighting",
      "url": "https://www.ikea.com/us/en/cat/smart-lighting-36812/"
    },
    {
      "name": "Kitchen appliances",
      "url": "https://www.ikea.com/us/en/cat/appliances-ka002/"
    },
    {
      "name": "Air purifiers & filters",
      "url": "https://www.ikea.com/us/en/cat/air-quality-products-49081/"
    },
    {
      "name": "Smart switches, plugs & sensors",
      "url": "https://www.ikea.com/us/en/cat/smart-light-wireless-switch-36814/"
    }
  ],
  "Home improvement": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/home-improvement-hi001/"
    },
    {
      "name": "SKYTTA sliding door system",
      "url": "https://www.ikea.com/us/en/cat/skytta-sliding-door-system-55984/"
    },
    {
      "name": "Knobs and handles",
      "url": "https://www.ikea.com/us/en/cat/cabinet-knobs-handles-pulls-16298/"
    },
    {
      "name": "Outdoor tiles & flooring",
      "url": "https://www.ikea.com/us/en/cat/outdoor-flooring-21957/"
    },
    {
      "name": "Tools and accessories",
      "url": "https://www.ikea.com/us/en/cat/tools-hardware-16292/"
    },
    {
      "name": "Faucets",
      "url": "https://www.ikea.com/us/en/cat/taps-700718/"
    },
    {
      "name": "Moving supplies",
      "url": "https://www.ikea.com/us/en/cat/moving-supplies-46078/"
    },
    {
      "name": "Wood treatment oils & furniture paint",
      "url": "https://www.ikea.com/us/en/cat/oils-stains-product-care-42948/"
    },
    {
      "name": "Sound absorbing acoustic panels",
      "url": "https://www.ikea.com/us/en/cat/acoustic-panels-46077/"
    },
    {
      "name": "Home safety locks, latches & more",
      "url": "https://www.ikea.com/us/en/cat/safety-products-sp001/"
    }
  ],
  "Pet products": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/pet-accessories-pt001/"
    },
    {
      "name": "Cat furniture & accessories",
      "url": "https://www.ikea.com/us/en/cat/cats-39569/"
    },
    {
      "name": "Dog beds, toys & bowls",
      "url": "https://www.ikea.com/us/en/cat/dogs-39570/"
    }
  ],
  "Smart home": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/smart-home-hs001/"
    },
    {
      "name": "Smart lighting",
      "url": "https://www.ikea.com/us/en/cat/smart-lighting-36812/"
    },
    {
      "name": "Smart switches, plugs & sensors",
      "url": "https://www.ikea.com/us/en/cat/smart-light-wireless-switch-36814/"
    },
    {
      "name": "Smart air purifiers",
      "url": "https://www.ikea.com/us/en/cat/smart-air-purifiers-56472/"
    }
  ],
  "Winter holiday shop": [
    {
      "name": "Shop all",
      "url": "https://www.ikea.com/us/en/cat/winter-holidays-wt001/"
    },
    {
      "name": "Holiday decor",
      "url": "https://www.ikea.com/us/en/cat/winter-decoration-49149/"
    },
    {
      "name": "Christmas lights",
      "url": "https://www.ikea.com/us/en/cat/winter-lights-49150/"
    },
    {
      "name": "Holiday textiles",
      "url": "https://www.ikea.com/us/en/cat/winter-textiles-49152/"
    },
    {
      "name": "Holiday tableware",
      "url": "https://www.ikea.com/us/en/cat/winter-tableware-49153/"
    },
    {
      "name": "Winter plants",
      "url": "https://www.ikea.com/us/en/cat/winter-pots-plants-49151/"
    },
    {
      "name": "Holiday food",
      "url": "https://www.ikea.com/us/en/cat/holiday-foods-49227/"
    },
    {
      "name": "Wrapping paper and bags",
      "url": "https://www.ikea.com/us/en/cat/paper-shop-25227/"
    },
    {
      "name": "Holiday baking tools",
      "url": "https://www.ikea.com/us/en/cat/winter-cooking-baking-49154/"
    }
  ]
}
''')
