"""AutoZone product-category inventory from the live top navigation.

Source of truth: the ``topNavProductData`` React Query payload embedded in
``__NEXT_DATA__`` on https://www.autozone.com/ -- the same first-party
navigation tree the header renders, read back from the server-rendered
bootstrap state rather than scraped out of the DOM.

Captured 2026-10-18 UTC through the repository's configured ScrapeOps US
proxy: **23 departments** and **971 leaf categories**, all with unique
``seoUrl`` paths and unique trailing slugs, so a leaf slug is globally
addressable and ``-a category=<leaf-slug>`` needs no department prefix.

Each department's ``childCategories`` entry is kept as a rich leaf with its
display name, so the DAG and the spider share one source of truth:
``BaseListingSpider`` normalises ``{department: {leaf: {url, name}}}`` and
``_spider_category_groups`` groups the leaves by their enclosing department.
AutoZone's own taxonomy path (``taxonomyPath``) diverges from the storefront
URL for some leaves, so the crawlable ``seoUrl`` is what is stored.
"""

from __future__ import annotations

AUTOZONE_SITE_BASE = "https://www.autozone.com"

AUTOZONE_CATEGORIES: dict[str, dict[str, dict[str, str]]] = {
    "batteries-starting-and-charging": {  # Batteries & Chargers
        "batteries-battery-cables": {
            "url": "https://www.autozone.com/batteries-starting-and-charging/batteries-battery-cables",
            "name": "Batteries & Battery Cables",
        },
        "battery-acid-battery-cleaning-installation": {
            "url": "https://www.autozone.com/batteries-starting-and-charging/battery-acid-battery-cleaning-installation",
            "name": "Battery Acid, Battery Cleaning & Installation",
        },
        "battery-chargers-accessories": {
            "url": "https://www.autozone.com/batteries-starting-and-charging/battery-chargers-accessories",
            "name": "Battery Chargers & Accessories",
        },
        "battery-fuses-power-distribution": {
            "url": "https://www.autozone.com/batteries-starting-and-charging/battery-fuses-power-distribution",
            "name": "Battery Fuses & Power Distribution",
        },
        "battery-switches": {
            "url": "https://www.autozone.com/batteries-starting-and-charging/battery-switches",
            "name": "Battery Switches",
        },
        "hybrid-electric-battery-pack-charging-equipment": {
            "url": "https://www.autozone.com/batteries-starting-and-charging/hybrid-electric-battery-pack-charging-equipment",
            "name": "Hybrid & Electric Battery Pack & Charging Equipment",
        },
    },
    "brakes-and-traction-control": {  # Brakes
        "abs-traction-control": {
            "url": "https://www.autozone.com/brakes-and-traction-control/abs-traction-control",
            "name": "ABS & Traction Control",
        },
        "air-brake-system": {
            "url": "https://www.autozone.com/brakes-and-traction-control/air-brake-system",
            "name": "Air Brake System",
        },
        "backing-plates-dust-shields": {
            "url": "https://www.autozone.com/brakes-and-traction-control/backing-plates-dust-shields",
            "name": "Backing Plates & Dust Shields",
        },
        "brake-bleeder-screws": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-bleeder-screws",
            "name": "Brake Bleeder Screws",
        },
        "brake-calipers-brackets": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-calipers-brackets",
            "name": "Brake Calipers & Brackets",
        },
        "brake-disc-drum-hardware": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-disc-drum-hardware",
            "name": "Brake Disc & Drum Hardware",
        },
        "brake-shoes": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-shoes",
            "name": "Brake Drums & Shoes",
        },
        "brake-hoses-brake-lines-brake-banjo-bolts": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-hoses-brake-lines-brake-banjo-bolts",
            "name": "Brake Hoses, Brake Lines & Brake Banjo Bolts",
        },
        "brake-kits-and-upgrades": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-kits-and-upgrades",
            "name": "Brake Kits & Upgrades",
        },
        "brake-master-cylinders-and-power-boosters": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-master-cylinders-and-power-boosters",
            "name": "Brake Master Cylinders & Power Boosters",
        },
        "brake-pads-and-wear-indicator-sensors": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-pads-and-wear-indicator-sensors",
            "name": "Brake Pads & Wear Indicator Sensors",
        },
        "brake-proportioning-valves": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-proportioning-valves",
            "name": "Brake Proportioning Valves",
        },
        "brake-rotors": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-rotors",
            "name": "Brake Rotors",
        },
        "brake-sensors-switches": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-sensors-switches",
            "name": "Brake Sensors & Switches",
        },
        "brake-system-fuses": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-system-fuses",
            "name": "Brake System Fuses",
        },
        "brake-system-modules": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-system-modules",
            "name": "Brake System Modules",
        },
        "brake-system-relays": {
            "url": "https://www.autozone.com/brakes-and-traction-control/brake-system-relays",
            "name": "Brake System Relays",
        },
        "engine-brakes": {
            "url": "https://www.autozone.com/brakes-and-traction-control/engine-brakes",
            "name": "Engine Brakes",
        },
        "exhaust-brake-actuators": {
            "url": "https://www.autozone.com/brakes-and-traction-control/exhaust-brake-actuators",
            "name": "Exhaust Brake Actuators",
        },
        "parking-brake-release": {
            "url": "https://www.autozone.com/brakes-and-traction-control/parking-brake-release",
            "name": "Parking Brake Release",
        },
        "wheel-cylinders": {
            "url": "https://www.autozone.com/brakes-and-traction-control/wheel-cylinders",
            "name": "Wheel Cylinders",
        },
    },
    "electrical-and-lighting": {  # Lighting & Electrical
        "accent-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/accent-lights",
            "name": "Accent Lights",
        },
        "adaptive-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/adaptive-lights",
            "name": "Adaptive Lights",
        },
        "ambient-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/ambient-lights",
            "name": "Ambient Lights",
        },
        "ashtray-light": {
            "url": "https://www.autozone.com/electrical-and-lighting/ashtray-light",
            "name": "Ashtray Light",
        },
        "auxiliary-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/auxiliary-lights",
            "name": "Auxiliary Lights",
        },
        "back-up-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/back-up-lights",
            "name": "Back Up Lights",
        },
        "beacon-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/beacon-lights",
            "name": "Beacon  Lights",
        },
        "brake-lights-3rd-brake-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/brake-lights-3rd-brake-lights",
            "name": "Brake Lights",
        },
        "cargo-area-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/cargo-area-lights",
            "name": "Cargo Area Lights",
        },
        "chassis-frame-wiring-harnesses": {
            "url": "https://www.autozone.com/electrical-and-lighting/chassis-frame-wiring-harnesses",
            "name": "Chassis & Frame Wiring",
        },
        "clearance-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/clearance-lights",
            "name": "Clearance Lights",
        },
        "clock-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/clock-lights",
            "name": "Clock Lights",
        },
        "combination-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/combination-lights",
            "name": "Combination Lights",
        },
        "cornering-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/cornering-lights",
            "name": "Cornering Lights",
        },
        "courtesy-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/courtesy-lights",
            "name": "Courtesy Lights",
        },
        "daytime-running-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/daytime-running-lights",
            "name": "Daytime Running Lights",
        },
        "dimmer-light-switches": {
            "url": "https://www.autozone.com/electrical-and-lighting/dimmer-light-switches",
            "name": "Dimmer Light Switches",
        },
        "dome-map-reading-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/dome-map-reading-lights",
            "name": "Dome, Map & Reading Lights",
        },
        "door-ajar-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/door-ajar-lights",
            "name": "Door Ajar Lights",
        },
        "door-mirror-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/door-mirror-lights",
            "name": "Door Mirror Lights",
        },
        "driving-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/driving-lights",
            "name": "Driving Lights",
        },
        "electrical-bulkhead-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/electrical-bulkhead-connector",
            "name": "Electrical Bulkhead Connector",
        },
        "electrical-connector-housing": {
            "url": "https://www.autozone.com/electrical-and-lighting/electrical-connector-housing",
            "name": "Electrical Connector Housing",
        },
        "electrical-wiring-fuses-switches": {
            "url": "https://www.autozone.com/electrical-and-lighting/electrical-wiring-fuses-switches",
            "name": "Electrical Wiring, Fuses & Switches",
        },
        "emergency-vehicle-light-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/emergency-vehicle-light-connector",
            "name": "Emergency Vehicle Light Connector",
        },
        "emergency-vehicle-light-switch-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/emergency-vehicle-light-switch-connector",
            "name": "Emergency Vehicle Light Switch Connector",
        },
        "emergency-warning-light": {
            "url": "https://www.autozone.com/electrical-and-lighting/emergency-warning-light",
            "name": "Emergency Warning Light",
        },
        "exterior-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/exterior-lights",
            "name": "Exterior Lights",
        },
        "flood-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/flood-lights",
            "name": "Flood Lights",
        },
        "floor-console-compartment-light-bulb": {
            "url": "https://www.autozone.com/electrical-and-lighting/floor-console-compartment-light-bulb",
            "name": "Floor Console Compartment Light Bulb",
        },
        "fog-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/fog-lights",
            "name": "Fog & Cornering Lights",
        },
        "footwell-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/footwell-lights",
            "name": "Footwell Lights",
        },
        "forward-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/forward-lights",
            "name": "Forward Lights",
        },
        "glove-box-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/glove-box-lights",
            "name": "Glove Box Lights",
        },
        "hazard-warning-turn-signal-flashers-relays": {
            "url": "https://www.autozone.com/electrical-and-lighting/hazard-warning-turn-signal-flashers-relays",
            "name": "Hazard Warning, Turn Signal Flashers & Relays",
        },
        "headlights-halo-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/headlights-halo-lights",
            "name": "Headlights & Halo Lights",
        },
        "heated-steering-wheel-module-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/heated-steering-wheel-module-connector",
            "name": "Heated Steering Wheel Module Connector",
        },
        "identification-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/identification-lights",
            "name": "Identification Lights",
        },
        "illuminated-entry-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/illuminated-entry-lights",
            "name": "Illuminated Entry Lights",
        },
        "illuminated-entry-switch-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/illuminated-entry-switch-connector",
            "name": "Illuminated Entry Switch Connector",
        },
        "illumination-relay-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/illumination-relay-connector",
            "name": "Illumination Relay Connector",
        },
        "information-display-module-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/information-display-module-connector",
            "name": "Information Display Module Connector",
        },
        "inline-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/inline-connector",
            "name": "Inline Connector",
        },
        "instrument-panel-indicator-warning-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/instrument-panel-indicator-warning-lights",
            "name": "Instrument Panel, Indicator & Warning Lights",
        },
        "interior-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/interior-lights",
            "name": "Interior Lights",
        },
        "license-plate-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/license-plate-lights",
            "name": "License Plate Lights",
        },
        "cornering-turn-signal-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/cornering-turn-signal-lights",
            "name": "Light Bars",
        },
        "light-wiring-kit": {
            "url": "https://www.autozone.com/miscellaneous-non-automotive/light-wiring-kit",
            "name": "Light Wiring Kit",
        },
        "luggage-compartment-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/luggage-compartment-lights",
            "name": "Luggage Compartment Lights",
        },
        "main-relay": {
            "url": "https://www.autozone.com/electrical-and-lighting/main-relay",
            "name": "Main Relay",
        },
        "marine-all-around-light": {
            "url": "https://www.autozone.com/lighting-electrical/marine-all-around-light",
            "name": "Marine All-Around Light",
        },
        "marine-bow-light": {
            "url": "https://www.autozone.com/electrical-and-lighting/marine-bow-light",
            "name": "Marine Bow Light",
        },
        "micro-plug-relay": {
            "url": "https://www.autozone.com/electrical-and-lighting/micro-plug-relay",
            "name": "Micro Plug Relay",
        },
        "micro-plug-relay-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/micro-plug-relay-connector",
            "name": "Micro Plug Relay Connector",
        },
        "multi-purpose-actuator": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-actuator",
            "name": "Multi-Purpose Actuator",
        },
        "multi-purpose-alarm-module-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-alarm-module-connector",
            "name": "Multi-Purpose Alarm Module Connector",
        },
        "diode": {
            "url": "https://www.autozone.com/batteries-starting-and-charging/diode",
            "name": "Multi-Purpose Diode",
        },
        "multi-purpose-insulator": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-insulator",
            "name": "Multi-Purpose Insulator",
        },
        "multi-purpose-jumper": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-jumper",
            "name": "Multi-Purpose Jumper",
        },
        "interior-exterior-light": {
            "url": "https://www.autozone.com/electrical-and-lighting/interior-exterior-light",
            "name": "Multi-Purpose Light Bulb",
        },
        "multi-purpose-light-bulb-kit": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-light-bulb-kit",
            "name": "Multi-Purpose Light Bulb Kit",
        },
        "multi-purpose-light-bulb-socket": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-light-bulb-socket",
            "name": "Multi-Purpose Light Bulb Socket",
        },
        "multi-purpose-module": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-module",
            "name": "Multi-Purpose Module",
        },
        "multi-purpose-relay": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-relay",
            "name": "Multi-Purpose Relay",
        },
        "multi-purpose-relay-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-relay-connector",
            "name": "Multi-Purpose Relay Connector",
        },
        "multi-purpose-relay-kit": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-relay-kit",
            "name": "Multi-Purpose Relay Kit",
        },
        "multi-purpose-sensor": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-sensor",
            "name": "Multi-Purpose Sensor",
        },
        "multi-purpose-temperature-sensor": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-temperature-sensor",
            "name": "Multi-Purpose Temperature Sensor",
        },
        "multi-purpose-light": {
            "url": "https://www.autozone.com/exterior-lighting/multi-purpose-light",
            "name": "Multi-Purpose Warning Light",
        },
        "multi-purpose-wiring-connector-seal": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-wiring-connector-seal",
            "name": "Multi-Purpose Wiring Connector Seal",
        },
        "multi-purpose-wiring-harness": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-wiring-harness",
            "name": "Multi-Purpose Wiring Harness",
        },
        "multi-purpose-wiring-harness-connector-plug": {
            "url": "https://www.autozone.com/electrical-and-lighting/multi-purpose-wiring-harness-connector-plug",
            "name": "Multi-Purpose Wiring Harness Connector Plug",
        },
        "off-road-light-wiring-harness-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/off-road-light-wiring-harness-connector",
            "name": "Off-Road Light Wiring Harness Connector",
        },
        "opera-light-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/opera-light-connector",
            "name": "Opera Light Connector",
        },
        "opera-light-socket": {
            "url": "https://www.autozone.com/electrical-and-lighting/opera-light-socket",
            "name": "Opera Light Socket",
        },
        "optic-sensor-kit": {
            "url": "https://www.autozone.com/electrical-and-lighting/optic-sensor-kit",
            "name": "Optic Sensor Kit",
        },
        "overdrive-cancel-switch-connector": {
            "url": "https://www.autozone.com/drivetrain/overdrive-cancel-switch-connector",
            "name": "Overdrive Cancel Switch Connector",
        },
        "overdrive-relay-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/overdrive-relay-connector",
            "name": "Overdrive Relay Connector",
        },
        "overhead-console-harness-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/overhead-console-harness-connector",
            "name": "Overhead Console Wiring Harness Connector",
        },
        "parking-clearance-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/parking-clearance-lights",
            "name": "Parking & Clearance Lights",
        },
        "parking-cornering-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/parking-cornering-lights",
            "name": "Parking & Cornering Lights",
        },
        "parking-daytime-running-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/parking-daytime-running-lights",
            "name": "Parking & Daytime Running Lights",
        },
        "parking-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/parking-lights",
            "name": "Parking Lights",
        },
        "passive-restraints-relay-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/passive-restraints-relay-connector",
            "name": "Passive Restraints Relay Connector",
        },
        "polarity-surge-protection": {
            "url": "https://www.autozone.com/electrical-and-lighting/polarity-surge-protection",
            "name": "Polarity & Surge Protection",
        },
        "power-feed-harness-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/power-feed-harness-connector",
            "name": "Power Feed Harness Connector",
        },
        "power-supply-module": {
            "url": "https://www.autozone.com/electrical-and-lighting/power-supply-module",
            "name": "Power Supply Module",
        },
        "power-supply-module-fuse": {
            "url": "https://www.autozone.com/lighting-electrical/power-supply-module-fuse",
            "name": "Power Supply Module Fuse",
        },
        "power-supply-module-nut": {
            "url": "https://www.autozone.com/lighting-electrical/power-supply-module-nut",
            "name": "Power Supply Module Nut",
        },
        "power-supply-module-relay": {
            "url": "https://www.autozone.com/lighting-electrical/power-supply-module-relay",
            "name": "Power Supply Module Relay",
        },
        "marine-lighting": {
            "url": "https://www.autozone.com/miscellaneous-non-automotive/marine-lighting",
            "name": "Puddle Light",
        },
        "puddle-light-bulb": {
            "url": "https://www.autozone.com/electrical-and-lighting/puddle-light-bulb",
            "name": "Puddle Light Bulb",
        },
        "reading-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/reading-lights",
            "name": "Reading Light",
        },
        "rear-heater-coolant-shut-off-solenoid-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/rear-heater-coolant-shut-off-solenoid-connector",
            "name": "Rear Heater Coolant Shut-Off Solenoid Connector",
        },
        "rear-lamp-harness-connector": {
            "url": "https://www.autozone.com/exterior-lighting/rear-lamp-harness-connector",
            "name": "Rear Light Harness Connector",
        },
        "reflectors": {
            "url": "https://www.autozone.com/electrical-and-lighting/reflectors",
            "name": "Reflectors",
        },
        "relay-box": {
            "url": "https://www.autozone.com/electrical-and-lighting/relay-box",
            "name": "Relay Box",
        },
        "relay-box-temperature-switch": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/relay-box-temperature-switch",
            "name": "Relay Box Temperature Switch",
        },
        "relay-box-temperature-switch-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/relay-box-temperature-switch-connector",
            "name": "Relay Box Temperature Switch Connector",
        },
        "relay-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/relay-connector",
            "name": "Relay Connector",
        },
        "relay-control-module": {
            "url": "https://www.autozone.com/electrical-and-lighting/relay-control-module",
            "name": "Relay Control Module",
        },
        "relay-control-module-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/relay-control-module-connector",
            "name": "Relay Control Module Connector",
        },
        "roof-marker-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/roof-marker-lights",
            "name": "Roof Marker Lights",
        },
        "running-board-light-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/running-board-light-connector",
            "name": "Running Board Light Connector",
        },
        "running-board-light-socket": {
            "url": "https://www.autozone.com/electrical-and-lighting/running-board-light-socket",
            "name": "Running Board Light Socket",
        },
        "serial-data-gateway-module": {
            "url": "https://www.autozone.com/electrical-and-lighting/serial-data-gateway-module",
            "name": "Serial Data Gateway Module",
        },
        "serial-data-gateway-module-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/serial-data-gateway-module-connector",
            "name": "Serial Data Gateway Module Connector",
        },
        "engine-shutdown-switch-harness-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/engine-shutdown-switch-harness-connector",
            "name": "Shutdown Switch Harness Connector",
        },
        "side-marker-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/side-marker-lights",
            "name": "Side Marker Lights",
        },
        "side-mirror-signal-light-bulb": {
            "url": "https://www.autozone.com/electrical-and-lighting/side-mirror-signal-light-bulb",
            "name": "Side Mirror Signal Light Bulb",
        },
        "side-repeater-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/side-repeater-lights",
            "name": "Side Repeater Lights",
        },
        "siren-relay-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/siren-relay-connector",
            "name": "Siren Relay Connector",
        },
        "stepwell-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/stepwell-lights",
            "name": "Stepwell Lights",
        },
        "strobe-underbody-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/strobe-underbody-lights",
            "name": "Strobe & Underbody Lights",
        },
        "sun-load-temperature-sensor": {
            "url": "https://www.autozone.com/electrical-and-lighting/sun-load-temperature-sensor",
            "name": "Sun Load Temperature Sensor",
        },
        "sun-load-temperature-sensor-bezel": {
            "url": "https://www.autozone.com/electrical-and-lighting/sun-load-temperature-sensor-bezel",
            "name": "Sun Load Temperature Sensor Bezel",
        },
        "sun-load-temp-sensor-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/sun-load-temp-sensor-connector",
            "name": "Sun Load Temperature Sensor Connector",
        },
        "sun-visor-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/sun-visor-lights",
            "name": "Sun Visor Lights",
        },
        "switch-mounting-bracket": {
            "url": "https://www.autozone.com/electrical-and-lighting/switch-mounting-bracket",
            "name": "Switch Mounting Bracket",
        },
        "switch-mounting-panel": {
            "url": "https://www.autozone.com/ignition/switch-mounting-panel",
            "name": "Switch Mounting Panel",
        },
        "switch-panel-and-wiring-harness": {
            "url": "https://www.autozone.com/electrical-and-lighting/switch-panel-and-wiring-harness",
            "name": "Switch Panel & Wiring Harness",
        },
        "switch-plug": {
            "url": "https://www.autozone.com/electrical-and-lighting/switch-plug",
            "name": "Switch Plug",
        },
        "tail-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/tail-lights",
            "name": "Tail Lights",
        },
        "tailgate-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/tailgate-lights",
            "name": "Tailgate Lights",
        },
        "tilt-cab-pump-wiring-harness": {
            "url": "https://www.autozone.com/electrical-and-lighting/tilt-cab-pump-wiring-harness",
            "name": "Tilt Cab Pump Wiring Harness",
        },
        "time-delay-relay-accessory-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/time-delay-relay-accessory-connector",
            "name": "Time Delay Relay Accessory Connector",
        },
        "trunk-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/trunk-lights",
            "name": "Trunk Lights",
        },
        "turn-signal-multi-function-switches": {
            "url": "https://www.autozone.com/electrical-and-lighting/turn-signal-multi-function-switches",
            "name": "Turn Signal & Multi-Function Switches",
        },
        "turn-signal-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/turn-signal-lights",
            "name": "Turn Signal Lights",
        },
        "twilight-sentinel-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/twilight-sentinel-lights",
            "name": "Twilight Sentinel Lights",
        },
        "underhood-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/underhood-lights",
            "name": "Under Hood Lights",
        },
        "vehicle-mounted-work-light": {
            "url": "https://www.autozone.com/electrical-and-lighting/vehicle-mounted-work-light",
            "name": "Vehicle-Mounted Work Light",
        },
        "vehicle-mounted-work-light-mounting-bracket": {
            "url": "https://www.autozone.com/electrical-and-lighting/vehicle-mounted-work-light-mounting-bracket",
            "name": "Vehicle-Mounted Work Light Mounting Bracket",
        },
        "warning-buzzer-relay-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/warning-buzzer-relay-connector",
            "name": "Warning Buzzer Relay Connector",
        },
        "warning-lights": {
            "url": "https://www.autozone.com/electrical-and-lighting/warning-lights",
            "name": "Warning Lights",
        },
        "wheel-accent-light": {
            "url": "https://www.autozone.com/electrical-and-lighting/wheel-accent-light",
            "name": "Wheel Accent Light",
        },
        "window-defroster-control-module-connector": {
            "url": "https://www.autozone.com/electrical-and-lighting/window-defroster-control-module-connector",
            "name": "Window Defroster Control Module Connector",
        },
        "window-defroster-relays": {
            "url": "https://www.autozone.com/electrical-and-lighting/window-defroster-relays",
            "name": "Window Defroster Relays",
        },
        "window-defroster-switches-and-knobs": {
            "url": "https://www.autozone.com/electrical-and-lighting/window-defroster-switches-and-knobs",
            "name": "Window Defroster Switches & Knobs",
        },
        "wiring-harness-adapter": {
            "url": "https://www.autozone.com/electrical-and-lighting/wiring-harness-adapter",
            "name": "Wiring Harness Adapter",
        },
        "engine-wiring-harness-diode": {
            "url": "https://www.autozone.com/electrical-and-lighting/engine-wiring-harness-diode",
            "name": "Wiring Harness Diode",
        },
        "wiring-relays": {
            "url": "https://www.autozone.com/electrical-and-lighting/wiring-relays",
            "name": "Wiring Relays",
        },
        "x-contact-relays": {
            "url": "https://www.autozone.com/electrical-and-lighting/x-contact-relays",
            "name": "X-Contact Relays",
        },
    },
    "ignition-tune-up-and-routine-maintenance": {  # Wipers & Components
        "wiper-blades-wiper-arms": {
            "url": "https://www.autozone.com/ignition-tune-up-and-routine-maintenance/wiper-blades-wiper-arms",
            "name": "Wiper Blades & Wiper Arms",
        },
        "wiper-motors-washer-pumps-washer-reservoirs": {
            "url": "https://www.autozone.com/ignition-tune-up-and-routine-maintenance/wiper-motors-washer-pumps-washer-reservoirs",
            "name": "Wiper Motors, Washer Pumps & Washer Reservoirs",
        },
    },
    "wash-and-wax": {  # Wash & Wax
        "buffers-polishers-pads": {
            "url": "https://www.autozone.com/wash-and-wax/buffers-polishers-pads",
            "name": "Buffers, Polishers, Pads",
        },
        "carpet-floor-mat-cleaners": {
            "url": "https://www.autozone.com/wash-and-wax/carpet-floor-mat-cleaners",
            "name": "Carpet & Floor Mat Cleaners",
        },
        "chamois-and-detailing-wipes": {
            "url": "https://www.autozone.com/wash-and-wax/chamois-and-detailing-wipes",
            "name": "Chamois, Detailing Wipes & Drying Towels",
        },
        "clay-bar-detailer": {
            "url": "https://www.autozone.com/wash-and-wax/clay-bar-detailer",
            "name": "Clay Bar Detailer",
        },
        "cleaning-brushes": {
            "url": "https://www.autozone.com/wash-and-wax/cleaning-brushes",
            "name": "Cleaning Brushes",
        },
        "convertible-top-conditioner": {
            "url": "https://www.autozone.com/wash-and-wax/convertible-top-conditioner",
            "name": "Convertible Top Conditioner",
        },
        "dusters": {
            "url": "https://www.autozone.com/wash-and-wax/dusters",
            "name": "Dusters",
        },
        "glass-cleaner-and-treatment": {
            "url": "https://www.autozone.com/wash-and-wax/glass-cleaner-and-treatment",
            "name": "Glass Cleaner & Treatment",
        },
        "hand-wipes": {
            "url": "https://www.autozone.com/wash-and-wax/hand-wipes",
            "name": "Hand Wipes",
        },
        "headlight-restoration": {
            "url": "https://www.autozone.com/wash-and-wax/headlight-restoration",
            "name": "Headlight Restoration",
        },
        "polish": {
            "url": "https://www.autozone.com/wash-and-wax/polish",
            "name": "Polish",
        },
        "protectants": {
            "url": "https://www.autozone.com/wash-and-wax/protectants",
            "name": "Protectants",
        },
        "rubbing-compounds": {
            "url": "https://www.autozone.com/wash-and-wax/rubbing-compounds",
            "name": "Rubbing Compounds",
        },
        "spray-bottles-sponges-and-squeegee": {
            "url": "https://www.autozone.com/wash-and-wax/spray-bottles-sponges-and-squeegee",
            "name": "Spray Bottles, Sponges & Squeegee",
        },
        "tire-wheel-cleaner": {
            "url": "https://www.autozone.com/wash-and-wax/tire-wheel-cleaner",
            "name": "Tire & Wheel Cleaner",
        },
        "wash": {
            "url": "https://www.autozone.com/wash-and-wax/wash",
            "name": "Wash",
        },
        "water-hoses-nozzles": {
            "url": "https://www.autozone.com/wash-and-wax/water-hoses-nozzles",
            "name": "Water Hoses & Nozzles",
        },
        "wax": {
            "url": "https://www.autozone.com/wash-and-wax/wax",
            "name": "Wax",
        },
        "wax-remover": {
            "url": "https://www.autozone.com/wash-and-wax/wax-remover",
            "name": "Wax Remover",
        },
    },
    "fluids-and-chemicals": {  # Oil, Fluids & Chemicals
        "ac-system-servicing": {
            "url": "https://www.autozone.com/fluids-and-chemicals/ac-system-servicing",
            "name": "AC System Servicing",
        },
        "antiseize-graphite": {
            "url": "https://www.autozone.com/fluids-and-chemicals/antiseize-graphite",
            "name": "AntiSeize & Graphite",
        },
        "antifreeze-additives": {
            "url": "https://www.autozone.com/fluids-and-chemicals/antifreeze-additives",
            "name": "Antifreeze & Additives",
        },
        "belt-conditioner-stop-squeak": {
            "url": "https://www.autozone.com/fluids-and-chemicals/belt-conditioner-stop-squeak",
            "name": "Belt Conditioner Stop Squeak",
        },
        "brake-cleaner-brake-lubricant": {
            "url": "https://www.autozone.com/fluids-and-chemicals/brake-cleaner-brake-lubricant",
            "name": "Brake Cleaner & Brake Lubricant",
        },
        "brake-fluid-brake-fluid-testers": {
            "url": "https://www.autozone.com/fluids-and-chemicals/brake-fluid-brake-fluid-testers",
            "name": "Brake Fluid & Brake Fluid Testers",
        },
        "cv-axle-joint-grease": {
            "url": "https://www.autozone.com/fluids-and-chemicals/cv-axle-joint-grease",
            "name": "CV Axle Joint Grease",
        },
        "carburetor-choke-tbi-cleaner": {
            "url": "https://www.autozone.com/fluids-and-chemicals/carburetor-choke-tbi-cleaner",
            "name": "Carburetor, Choke & TBI Cleaner",
        },
        "chain-case-oils": {
            "url": "https://www.autozone.com/fluids-and-chemicals/chain-case-oils",
            "name": "Chain Case Oil",
        },
        "chain-lubricants": {
            "url": "https://www.autozone.com/fluids-and-chemicals/chain-lubricants",
            "name": "Chain Lubricant",
        },
        "concrete-floor-cleaner": {
            "url": "https://www.autozone.com/fluids-and-chemicals/concrete-floor-cleaner",
            "name": "Concrete & Floor Cleaner",
        },
        "convertible-top-hydraulic-fluid": {
            "url": "https://www.autozone.com/fluids-and-chemicals/convertible-top-hydraulic-fluid",
            "name": "Convertible Top Hydraulic Fluid",
        },
        "def-fluid": {
            "url": "https://www.autozone.com/fluids-and-chemicals/def-fluid",
            "name": "DEF Fluid",
        },
        "de-icer-starting-fluids": {
            "url": "https://www.autozone.com/fluids-and-chemicals/de-icer-starting-fluids",
            "name": "De-Icer & Starting Fluids",
        },
        "degreasers-stain-removal": {
            "url": "https://www.autozone.com/fluids-and-chemicals/degreasers-stain-removal",
            "name": "Degreasers & Stain Removal",
        },
        "dielectric-grease-electrical-cleaner": {
            "url": "https://www.autozone.com/fluids-and-chemicals/dielectric-grease-electrical-cleaner",
            "name": "Dielectric Grease & Electrical Cleaner",
        },
        "diesel-dpf-cleaner": {
            "url": "https://www.autozone.com/fluids-and-chemicals/diesel-dpf-cleaner",
            "name": "Diesel DPF Cleaner",
        },
        "electronic-screen-cleaner": {
            "url": "https://www.autozone.com/fluids-and-chemicals/electronic-screen-cleaner",
            "name": "Electronic Screen Cleaner",
        },
        "engine-assembly-lubricant": {
            "url": "https://www.autozone.com/fluids-and-chemicals/engine-assembly-lubricant",
            "name": "Engine Assembly Lubricant",
        },
        "engine-flushes": {
            "url": "https://www.autozone.com/fluids-and-chemicals/engine-flushes",
            "name": "Engine Flush",
        },
        "engine-oil-additives": {
            "url": "https://www.autozone.com/fluids-and-chemicals/engine-oil-additives",
            "name": "Engine Oil & Additives",
        },
        "fuel-additives-stabilizers": {
            "url": "https://www.autozone.com/fluids-and-chemicals/fuel-additives-stabilizers",
            "name": "Fuel Additives & Stabilizers",
        },
        "gear-oil-additives": {
            "url": "https://www.autozone.com/fluids-and-chemicals/gear-oil-additives",
            "name": "Gear Oil & Additives",
        },
        "grease-cartridges": {
            "url": "https://www.autozone.com/fluids-and-chemicals/grease-cartridges",
            "name": "Grease & Cartridges",
        },
        "hydraulic-fluids-jack-oil": {
            "url": "https://www.autozone.com/fluids-and-chemicals/hydraulic-fluids-jack-oil",
            "name": "Hydraulic Fluids & Jack Oil",
        },
        "mass-air-flow-cleaner": {
            "url": "https://www.autozone.com/fluids-and-chemicals/mass-air-flow-cleaner",
            "name": "Mass Air Flow Cleaner",
        },
        "multi-purpose-cleaner": {
            "url": "https://www.autozone.com/fluids-and-chemicals/multi-purpose-cleaner",
            "name": "Multi-Purpose Cleaner",
        },
        "multi-purpose-cleaner-and-disinfectant": {
            "url": "https://www.autozone.com/fluids-and-chemicals/multi-purpose-cleaner-and-disinfectant",
            "name": "Multi-Purpose Cleaner & Disinfectant",
        },
        "multi-purpose-lubricant": {
            "url": "https://www.autozone.com/fluids-and-chemicals/multi-purpose-lubricant",
            "name": "Multi-Purpose Lubricant",
        },
        "multi-purpose-oil": {
            "url": "https://www.autozone.com/fluids-and-chemicals/multi-purpose-oil",
            "name": "Multi-Purpose Oil",
        },
        "penetrating-oils": {
            "url": "https://www.autozone.com/fluids-and-chemicals/penetrating-oils",
            "name": "Penetrating Oils",
        },
        "plastic-cleaner": {
            "url": "https://www.autozone.com/fluids-and-chemicals/plastic-cleaner",
            "name": "Plastic Cleaner",
        },
        "power-steering-fluids-additives": {
            "url": "https://www.autozone.com/fluids-and-chemicals/power-steering-fluids-additives",
            "name": "Power Steering Fluids & Additives",
        },
        "rubber-lubricant": {
            "url": "https://www.autozone.com/fluids-and-chemicals/rubber-lubricant",
            "name": "Rubber Lubricant",
        },
        "rust-remover": {
            "url": "https://www.autozone.com/fluids-and-chemicals/rust-remover",
            "name": "Rust Remover",
        },
        "transmission-fluid-additives": {
            "url": "https://www.autozone.com/fluids-and-chemicals/transmission-fluid-additives",
            "name": "Transmission Fluid & Additives",
        },
        "transmission-flush": {
            "url": "https://www.autozone.com/fluids-and-chemicals/transmission-flush",
            "name": "Transmission Flush",
        },
        "washer-fluid": {
            "url": "https://www.autozone.com/fluids-and-chemicals/washer-fluid",
            "name": "Washer Fluid",
        },
    },
    "alternators-and-charging-system": {  # Alternators & Starters
        "alternator-fuses-starter-fuses": {
            "url": "https://www.autozone.com/alternators-and-charging-system/alternator-fuses-starter-fuses",
            "name": "Alternator & Charging Fuses",
        },
        "alternator-relays-charging-relays": {
            "url": "https://www.autozone.com/alternators-and-charging-system/alternator-relays-charging-relays",
            "name": "Alternator Relays & Charging Relays",
        },
        "alternators-pulleys": {
            "url": "https://www.autozone.com/alternators-and-charging-system/alternators-pulleys",
            "name": "Alternators & Pulleys",
        },
        "generators-serviceable-parts": {
            "url": "https://www.autozone.com/alternators-and-charging-system/generators-serviceable-parts",
            "name": "Generators & Serviceable Parts",
        },
        "neutral-safety-switches": {
            "url": "https://www.autozone.com/alternators-and-charging-system/neutral-safety-switches",
            "name": "Neutral Safety Switches",
        },
        "alternator-starter-fuses": {
            "url": "https://www.autozone.com/alternators-and-charging-system/alternator-starter-fuses",
            "name": "Starter Fuses",
        },
        "starters-starter-solenoids": {
            "url": "https://www.autozone.com/alternators-and-charging-system/starters-starter-solenoids",
            "name": "Starters & Starter Solenoids",
        },
        "voltage-regulators": {
            "url": "https://www.autozone.com/alternators-and-charging-system/voltage-regulators",
            "name": "Voltage Regulators",
        },
    },
    "truck-and-towing": {  # Towing & Trailer
        "fifth-wheel-gooseneck": {
            "url": "https://www.autozone.com/truck-and-towing/fifth-wheel-gooseneck",
            "name": "Fifth Wheel & Gooseneck",
        },
        "tail-light-converters": {
            "url": "https://www.autozone.com/truck-and-towing/tail-light-converters",
            "name": "Tail Light Converters",
        },
        "towing-mirrors": {
            "url": "https://www.autozone.com/truck-and-towing/towing-mirrors",
            "name": "Towing Mirrors",
        },
        "trailer-accessories-specialty": {
            "url": "https://www.autozone.com/truck-and-towing/trailer-accessories-specialty",
            "name": "Trailer Accessories & Specialty",
        },
        "trailer-balls-trailer-hitches-couplers-receivers": {
            "url": "https://www.autozone.com/truck-and-towing/trailer-balls-trailer-hitches-couplers-receivers",
            "name": "Trailer Balls, Trailer Hitches, Couplers & Receivers",
        },
        "trailer-brake-components": {
            "url": "https://www.autozone.com/truck-and-towing/trailer-brake-components",
            "name": "Trailer Bearings & Brakes",
        },
        "trailer-bunk-trailer-carpet-trailer-cargo": {
            "url": "https://www.autozone.com/truck-and-towing/trailer-bunk-trailer-carpet-trailer-cargo",
            "name": "Trailer Bunk, Trailer Carpet, & Trailer Cargo",
        },
        "trailer-jacks-jack-accessories": {
            "url": "https://www.autozone.com/truck-and-towing/trailer-jacks-jack-accessories",
            "name": "Trailer Jacks & Jack Accessories",
        },
        "trailer-lights": {
            "url": "https://www.autozone.com/truck-and-towing/trailer-lights",
            "name": "Trailer Lights",
        },
        "trailer-relays": {
            "url": "https://www.autozone.com/truck-and-towing/trailer-relays",
            "name": "Trailer Relays",
        },
        "trailer-sway-control-weight-distribution": {
            "url": "https://www.autozone.com/truck-and-towing/trailer-sway-control-weight-distribution",
            "name": "Trailer Sway Control & Weight Distribution",
        },
        "trailer-tire-pressure-monitoring-system-tpms-control-module": {
            "url": "https://www.autozone.com/towing-trailer/trailer-tire-pressure-monitoring-system-tpms-control-module",
            "name": "Trailer Tire Pressure Monitoring System (TPMS) Control Module",
        },
        "trailer-turn-signal-relays": {
            "url": "https://www.autozone.com/truck-and-towing/trailer-turn-signal-relays",
            "name": "Trailer Turn Signal Relays",
        },
        "trailer-wiring-adapters-connectors-harnesses": {
            "url": "https://www.autozone.com/truck-and-towing/trailer-wiring-adapters-connectors-harnesses",
            "name": "Trailer Wiring Adapters, Connectors & Harnesses",
        },
        "winches-cables-hooks": {
            "url": "https://www.autozone.com/truck-and-towing/winches-cables-hooks",
            "name": "Winches, Cables & Hooks",
        },
    },
    "interior-accessories": {  # Interior Accessories
        "accessory-power-outlets-cigarette-lighters": {
            "url": "https://www.autozone.com/interior-accessories/accessory-power-outlets-cigarette-lighters",
            "name": "Accessory Power Outlets & Cigarette Lighters",
        },
        "accessory-relays": {
            "url": "https://www.autozone.com/interior-accessories/accessory-relays",
            "name": "Accessory Relays",
        },
        "air-fresheners": {
            "url": "https://www.autozone.com/interior-accessories/air-fresheners",
            "name": "Air Fresheners",
        },
        "alarm-theft": {
            "url": "https://www.autozone.com/interior-accessories/alarm-theft",
            "name": "Alarm & Theft",
        },
        "antenna-dvd-gps-stereos-amps-speakers": {
            "url": "https://www.autozone.com/interior-accessories/antenna-dvd-gps-stereos-amps-speakers",
            "name": "Antenna, DVD, GPS, Stereos, Amps, & Speakers",
        },
        "ash-trays": {
            "url": "https://www.autozone.com/interior-accessories/ash-trays",
            "name": "Ash Trays",
        },
        "cell-phone-accessories": {
            "url": "https://www.autozone.com/interior-accessories/cell-phone-accessories",
            "name": "Cell Phone Accessories",
        },
        "clocks-accessories": {
            "url": "https://www.autozone.com/interior-accessories/clocks-accessories",
            "name": "Clocks & Accessories",
        },
        "combination-and-multi-function-switches": {
            "url": "https://www.autozone.com/interior-accessories/combination-and-multi-function-switches",
            "name": "Combination Switches",
        },
        "consoles-accessories": {
            "url": "https://www.autozone.com/interior-accessories/consoles-accessories",
            "name": "Consoles & Accessories",
        },
        "courtesy-mat": {
            "url": "https://www.autozone.com/interior-accessories/courtesy-mat",
            "name": "Courtesy Mat",
        },
        "cruise-control": {
            "url": "https://www.autozone.com/interior-accessories/cruise-control",
            "name": "Cruise Control",
        },
        "cups-cup-holders": {
            "url": "https://www.autozone.com/exterior-accessories/cups-cup-holders",
            "name": "Cups & Cup Holders",
        },
        "dashboard-accessories": {
            "url": "https://www.autozone.com/interior-accessories/dashboard-accessories",
            "name": "Dashboard Accessories",
        },
        "dashboard-wiring-harnesses": {
            "url": "https://www.autozone.com/interior-accessories/dashboard-wiring-harnesses",
            "name": "Dashboard Wiring Harness",
        },
        "floor-carpet-floor-liners-floor-mats": {
            "url": "https://www.autozone.com/interior-accessories/floor-carpet-floor-liners-floor-mats",
            "name": "Floor Carpet, Floor Liners & Floor Mats",
        },
        "glove-boxes": {
            "url": "https://www.autozone.com/interior-accessories/glove-boxes",
            "name": "Glove Boxes",
        },
        "heated-windshields": {
            "url": "https://www.autozone.com/interior-accessories/heated-windshields",
            "name": "Heated Windshields",
        },
        "horns-buttons-contacts-fuses-relays": {
            "url": "https://www.autozone.com/interior-accessories/horns-buttons-contacts-fuses-relays",
            "name": "Horns, Buttons, Contacts, Fuses & Relays",
        },
        "instrument-clusters-instrument-panels-gauges-bezels": {
            "url": "https://www.autozone.com/interior-accessories/instrument-clusters-instrument-panels-gauges-bezels",
            "name": "Instrument Clusters, Instrument Panels, Gauges & Bezels",
        },
        "interior-mirrors": {
            "url": "https://www.autozone.com/exterior-accessories/interior-mirrors",
            "name": "Interior Mirrors",
        },
        "keyless-entry-key-fobs-remote-start": {
            "url": "https://www.autozone.com/interior-accessories/keyless-entry-key-fobs-remote-start",
            "name": "Keyless Entry, Key Fobs & Remote Start",
        },
        "parking-cameras-backup-alarm-system": {
            "url": "https://www.autozone.com/interior-accessories/parking-cameras-backup-alarm-system",
            "name": "Parking Cameras & Backup Alarm System",
        },
        "pedals-pads": {
            "url": "https://www.autozone.com/interior-accessories/pedals-pads",
            "name": "Pedals & Pads",
        },
        "personal-protection": {
            "url": "https://www.autozone.com/tools-and-equipment/personal-protection",
            "name": "Personal Protection",
        },
        "pet-accessories": {
            "url": "https://www.autozone.com/interior-accessories/pet-accessories",
            "name": "Pet Accessories",
        },
        "portable-fans-cab-heaters": {
            "url": "https://www.autozone.com/interior-accessories/portable-fans-cab-heaters",
            "name": "Portable Fans & Cab Heaters",
        },
        "seats-headrests": {
            "url": "https://www.autozone.com/interior-accessories/seats-headrests",
            "name": "Seats, Seat Belts & Headrests",
        },
        "steering-wheels": {
            "url": "https://www.autozone.com/interior-accessories/steering-wheels",
            "name": "Steering Wheels",
        },
        "storage-management": {
            "url": "https://www.autozone.com/interior-accessories/storage-management",
            "name": "Storage Management",
        },
        "sun-visors-accessories": {
            "url": "https://www.autozone.com/interior-accessories/sun-visors-accessories",
            "name": "Sun Visors & Accessories",
        },
        "sunshades-sunvisors-windshield-screens": {
            "url": "https://www.autozone.com/interior-accessories/sunshades-sunvisors-windshield-screens",
            "name": "Sunshades, Sunvisors & Windshield Screens",
        },
        "tailgates-truck-beds": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/tailgates-truck-beds",
            "name": "Tailgates & Truck Beds",
        },
        "toys": {
            "url": "https://www.autozone.com/interior-accessories/toys",
            "name": "Toys",
        },
        "window-cranks-handles": {
            "url": "https://www.autozone.com/interior-accessories/window-cranks-handles",
            "name": "Window Cranks & Handles",
        },
    },
    "cooling-heating-and-climate-control": {  # Air Conditioning & Heating
        "ac-accumulators-driers-expansion-valves-and-orifices": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-accumulators-driers-expansion-valves-and-orifices",
            "name": "AC Accumulators, Driers, Expansion Valves & Orifices",
        },
        "ac-charging-adapters-valve-caps-and-cores": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-charging-adapters-valve-caps-and-cores",
            "name": "AC Charging Adapters, Valve Caps & Cores",
        },
        "ac-compressor-ac-clutch": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-compressor-ac-clutch",
            "name": "AC Compressor & AC Clutch",
        },
        "ac-condenser-components": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-condenser-components",
            "name": "AC Condenser & Components",
        },
        "ac-control-panel-modules-blower-fan-switches": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-control-panel-modules-blower-fan-switches",
            "name": "AC Control Panel Modules & Blower Fan Switches",
        },
        "ac-evaporator-core-components": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-evaporator-core-components",
            "name": "AC Evaporator Core & Components",
        },
        "ac-heater-blower-fan-motors-and-wheels": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-heater-blower-fan-motors-and-wheels",
            "name": "AC Heater Blower Fan Motors & Wheels",
        },
        "ac-heater-fuses": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-heater-fuses",
            "name": "AC Heater Fuses",
        },
        "ac-heater-mode-actuators-doors": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-heater-mode-actuators-doors",
            "name": "AC Heater Mode Actuators & Doors",
        },
        "ac-heater-relays": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-heater-relays",
            "name": "AC Heater Relays",
        },
        "ac-heater-resistors": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-heater-resistors",
            "name": "AC Heater Resistors",
        },
        "ac-heater-wiring-harnesses": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-heater-wiring-harnesses",
            "name": "AC Heater Wiring Harnesses",
        },
        "ac-hoses-gaskets-o-rings-seals": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-hoses-gaskets-o-rings-seals",
            "name": "AC Hoses, Gaskets, O-Rings & Seals",
        },
        "ac-poa-valves-power-servos": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-poa-valves-power-servos",
            "name": "AC POA Valves & Power Servos",
        },
        "ac-sensors-ac-switches": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/ac-sensors-ac-switches",
            "name": "AC Sensors & AC Switches",
        },
        "cabin-air-filters": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/cabin-air-filters",
            "name": "Cabin Air Filters",
        },
        "heater-cores-heater-control-valves": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/heater-cores-heater-control-valves",
            "name": "Heater Cores & Heater Control Valves",
        },
        "vacuum-reservoirs-vacuum-power-elements": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/vacuum-reservoirs-vacuum-power-elements",
            "name": "Vacuum Reservoirs & Vacuum Power Elements",
        },
    },
    "apparel-clothing-hats": {  # Apparel, Clothing & Hats
        "apparel-accessories": {
            "url": "https://www.autozone.com/apparel-clothing-hats/apparel-accessories",
            "name": "Apparel Accessories",
        },
        "clothing": {
            "url": "https://www.autozone.com/apparel-clothing-hats/clothing",
            "name": "Clothing",
        },
        "helmets-hats": {
            "url": "https://www.autozone.com/apparel-clothing-hats/helmets-hats",
            "name": "Helmets & Hats",
        },
        "racing-gear": {
            "url": "https://www.autozone.com/apparel-clothing-hats/racing-gear",
            "name": "Racing Gear",
        },
        "safety-gear": {
            "url": "https://www.autozone.com/apparel-clothing-hats/safety-gear",
            "name": "Safety Gear",
        },
    },
    "belts-and-hoses": {  # Belts & Hoses
        "engine-belts-belt-tensioners-and-idler-pulleys": {
            "url": "https://www.autozone.com/belts-and-hoses/engine-belts-belt-tensioners-and-idler-pulleys",
            "name": "Engine Belts, Belt Tensioners & Idler Pulleys",
        },
        "engine-coolant-hoses-and-coolant-pipes-flanges-and-gaskets": {
            "url": "https://www.autozone.com/belts-and-hoses/engine-coolant-hoses-and-coolant-pipes-flanges-and-gaskets",
            "name": "Engine Coolant Hoses, Coolant Pipes, Flanges & Gaskets",
        },
        "engine-heater-hoses-heater-coolant-pipes-gaskets-seals": {
            "url": "https://www.autozone.com/belts-and-hoses/engine-heater-hoses-heater-coolant-pipes-gaskets-seals",
            "name": "Engine Heater Hoses, Heater Coolant Pipes & Gaskets",
        },
    },
    "collision-body-parts-and-hardware": {  # Body & Collision
        "air-bag-impact-sensor-components": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/air-bag-impact-sensor-components",
            "name": "Air Bag, Clock Spring & Impact Sensors",
        },
        "back-glass": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/back-glass",
            "name": "Back Glass",
        },
        "body-a-body-b-body-c-body-d-pillars": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/body-a-body-b-body-c-body-d-pillars",
            "name": "Body A, Body B, Body C & Body D Pillars",
        },
        "body-control-modules": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/body-control-modules",
            "name": "Body Control Modules",
        },
        "body-header-panels": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/body-header-panels",
            "name": "Body Header Panels",
        },
        "body-molding-panel-trim-clips-fasteners": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/body-molding-panel-trim-clips-fasteners",
            "name": "Body Molding & Panel Trim Clips & Fasteners",
        },
        "body-molding-seal-kits": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/body-molding-seal-kits",
            "name": "Body Molding & Seal Kits",
        },
        "body-mounts-body-and-suspension-subframe-mounts": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/body-mounts-body-and-suspension-subframe-mounts",
            "name": "Body Mounts, Crossmembers & Subframe Mounts",
        },
        "body-wiring-harnesses": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/body-wiring-harnesses",
            "name": "Body Wiring Harnesses",
        },
        "body-work": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/body-work",
            "name": "Body Work",
        },
        "bumpers-grilles-valance-panels-air-dams": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/bumpers-grilles-valance-panels-air-dams",
            "name": "Bumpers, Grilles, Valance Panels & Air Dams",
        },
        "bus-door-motor": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/bus-door-motor",
            "name": "Bus Door Motor",
        },
        "channels-for-windshields": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/channels-for-windshields",
            "name": "Chassis & Components",
        },
        "chassis-fairing-handle-extension": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/chassis-fairing-handle-extension",
            "name": "Chassis Fairing Handle Extension",
        },
        "chassis-fairing-handle-kit": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/chassis-fairing-handle-kit",
            "name": "Chassis Fairing Handle Kit",
        },
        "convertible-tops": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/convertible-tops",
            "name": "Convertible Tops",
        },
        "cowls-components": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/cowls-components",
            "name": "Cowls & Components",
        },
        "crane-chassis": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/crane-chassis",
            "name": "Crane Chassis",
        },
        "cross-body-frame-relays-wiring-harness": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/cross-body-frame-relays-wiring-harness",
            "name": "Cross Body Frame Relays & Wiring Harness",
        },
        "deck-lids": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/deck-lids",
            "name": "Deck Lids",
        },
        "door-channels-door-trim-hardware": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/door-channels-door-trim-hardware",
            "name": "Door Channels, Door Trim & Hardware",
        },
        "door-handle-link": {
            "url": "https://www.autozone.com/interior/door-handle-link",
            "name": "Door Handle Link",
        },
        "doors": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/doors",
            "name": "Doors",
        },
        "entry-step-trim-panel": {
            "url": "https://www.autozone.com/body-collision/entry-step-trim-panel",
            "name": "Entry Step Trim Panel",
        },
        "fender-clips-retainers": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/fender-clips-retainers",
            "name": "Fender Clips & Retainers",
        },
        "fenders": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/fenders",
            "name": "Fenders",
        },
        "fenderwells-wheel-housings": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/fenderwells-wheel-housings",
            "name": "Fenderwells & Wheel Housings",
        },
        "firewall-grommets": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/firewall-grommets",
            "name": "Firewall Grommets",
        },
        "floor-truck-bed-supports": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/floor-truck-bed-supports",
            "name": "Floor & Truck Bed Supports",
        },
        "floor-pan-brace": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/floor-pan-brace",
            "name": "Floor Pan Brace",
        },
        "floor-pan-patch-panel": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/floor-pan-patch-panel",
            "name": "Floor Pan Patch Panel",
        },
        "floor-pans": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/floor-pans",
            "name": "Floor Pans",
        },
        "fuel-filler-doors-hinges-relays-release-cables": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/fuel-filler-doors-hinges-relays-release-cables",
            "name": "Fuel Filler Doors, Hinges, Relays & Release Cables",
        },
        "ground-cables": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/ground-cables",
            "name": "Ground Cables",
        },
        "hard-tops": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/hard-tops",
            "name": "Hard Tops",
        },
        "hatches": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/hatches",
            "name": "Hatches",
        },
        "headliners": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/headliners",
            "name": "Headliners",
        },
        "hoods": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/hoods",
            "name": "Hoods",
        },
        "lift-supports": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/lift-supports",
            "name": "Lift Supports",
        },
        "liftgates": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/liftgates",
            "name": "Liftgates",
        },
        "lifting-sling": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/lifting-sling",
            "name": "Lifting Sling",
        },
        "molding-clip": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/molding-clip",
            "name": "Molding Clip",
        },
        "molding-clip-set": {
            "url": "https://www.autozone.com/body-collision/molding-clip-set",
            "name": "Molding Clip Set",
        },
        "multi-purpose-cap": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/multi-purpose-cap",
            "name": "Multi-Purpose Cap",
        },
        "multi-purpose-clip": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/multi-purpose-clip",
            "name": "Multi-Purpose Clip",
        },
        "universal-control-cables": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/universal-control-cables",
            "name": "Multi-Purpose Control Cable",
        },
        "multi-purpose-fitting": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/multi-purpose-fitting",
            "name": "Multi-Purpose Fitting",
        },
        "multi-purpose-grommet": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/multi-purpose-grommet",
            "name": "Multi-Purpose Grommet",
        },
        "universal-utility-knob": {
            "url": "https://www.autozone.com/interior/universal-utility-knob",
            "name": "Multi-Purpose Knob",
        },
        "multi-purpose-lift-support-bracket": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/multi-purpose-lift-support-bracket",
            "name": "Multi-Purpose Lift Support Bracket",
        },
        "multi-purpose-lift-support-clamp-set": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/multi-purpose-lift-support-clamp-set",
            "name": "Multi-Purpose Lift Support Clamp Set",
        },
        "multi-purpose-lift-support-stud": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/multi-purpose-lift-support-stud",
            "name": "Multi-Purpose Lift Support Stud",
        },
        "retainer-clamp": {
            "url": "https://www.autozone.com/plumbing-hosing/retainer-clamp",
            "name": "Multi-Purpose Retainer",
        },
        "multi-purpose-spring-clip": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/multi-purpose-spring-clip",
            "name": "Multi-Purpose Spring Clip",
        },
        "multi-purpose-stop-bumper": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/multi-purpose-stop-bumper",
            "name": "Multi-Purpose Stop Bumper",
        },
        "multi-purpose-switch-bezel": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/multi-purpose-switch-bezel",
            "name": "Multi-Purpose Switch Bezel",
        },
        "multi-purpose-switch-panel-kit": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/multi-purpose-switch-panel-kit",
            "name": "Multi-Purpose Switch Panel Kit",
        },
        "protective-shroud": {
            "url": "https://www.autozone.com/chrome-and-dress-up/protective-shroud",
            "name": "Protective Shroud",
        },
        "quarter-windows": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/quarter-windows",
            "name": "Quarter Panels & Windows",
        },
        "rear-panel-applique": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/rear-panel-applique",
            "name": "Rear Panel Applique",
        },
        "rear-windows": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/rear-windows",
            "name": "Rear Windows",
        },
        "retainer-clips": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/retainer-clips",
            "name": "Retainer Clips",
        },
        "rocker-panels": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/rocker-panels",
            "name": "Rocker Panels",
        },
        "roof-drip-molding-clip": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/roof-drip-molding-clip",
            "name": "Roof Drip Molding Clip",
        },
        "roof-header-panel-seal": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/roof-header-panel-seal",
            "name": "Roof Header Panel Seal",
        },
        "roof-molding": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/roof-molding",
            "name": "Roof Molding",
        },
        "roof-molding-clip": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/roof-molding-clip",
            "name": "Roof Molding Clip",
        },
        "roof-panel-reveal-molding-clip": {
            "url": "https://www.autozone.com/screws-pins-and-clips/roof-panel-reveal-molding-clip",
            "name": "Roof Panel Reveal Molding Clip",
        },
        "roof-panel-seal": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/roof-panel-seal",
            "name": "Roof Panel Seal",
        },
        "roof-side-rail-air-bag-module-connector": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/roof-side-rail-air-bag-module-connector",
            "name": "Roof Side Rail Air Bag Module Connector",
        },
        "roof-side-rail-gasket": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/roof-side-rail-gasket",
            "name": "Roof Side Rail Gasket",
        },
        "roof-vent-cover": {
            "url": "https://www.autozone.com/body-collision/roof-vent-cover",
            "name": "Roof Vent Cover",
        },
        "roof-vent-insulator": {
            "url": "https://www.autozone.com/body-collision/roof-vent-insulator",
            "name": "Roof Vent Insulator",
        },
        "roof-vent-lid": {
            "url": "https://www.autozone.com/body-collision/roof-vent-lid",
            "name": "Roof Vent Lid",
        },
        "rubber-stop-bumper-assortment": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/rubber-stop-bumper-assortment",
            "name": "Rubber Stop Bumper Assortment",
        },
        "side-body-panel-molding": {
            "url": "https://www.autozone.com/exterior-dress-up/side-body-panel-molding",
            "name": "Side Body Panel Molding",
        },
        "side-body-panel-molding-clip": {
            "url": "https://www.autozone.com/screws-pins-and-clips/side-body-panel-molding-clip",
            "name": "Side Body Panel Molding Clip",
        },
        "side-body-trim-nameplate-clip": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/side-body-trim-nameplate-clip",
            "name": "Side Body Trim Nameplate Clip",
        },
        "side-body-trim-protector-clip": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/side-body-trim-protector-clip",
            "name": "Side Body Trim Protector Clip",
        },
        "side-windows": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/side-windows",
            "name": "Side Windows",
        },
        "skid-plates": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/skid-plates",
            "name": "Skid Plates",
        },
        "sliding-doors-components": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/sliding-doors-components",
            "name": "Sliding Doors & Components",
        },
        "sliding-windows-components": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/sliding-windows-components",
            "name": "Sliding Windows & Components",
        },
        "soft-tops": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/soft-tops",
            "name": "Soft Tops",
        },
        "sunroofs": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/sunroofs",
            "name": "Sunroofs",
        },
        "t-tops": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/t-tops",
            "name": "T-Tops",
        },
        "tailgates": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/tailgates",
            "name": "Tailgates",
        },
        "targa-top-latch-handle": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/targa-top-latch-handle",
            "name": "Targa Top Latch Handle",
        },
        "targa-top-seal-weatherstrip": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/targa-top-seal-weatherstrip",
            "name": "Targa Top Seal",
        },
        "trunks": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/trunks",
            "name": "Trunks",
        },
        "undercar-engine-splash-shields-hardware": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/undercar-engine-splash-shields-hardware",
            "name": "Undercar & Engine Splash Shields - Hardware",
        },
        "universal-body-plug": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/universal-body-plug",
            "name": "Universal Body Plug",
        },
        "vent-windows": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/vent-windows",
            "name": "Vent Windows",
        },
        "weatherstripping-door-channels-hardware": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/weatherstripping-door-channels-hardware",
            "name": "Weatherstripping, Door Channels & Hardware",
        },
        "window-vent-window-latches": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/window-vent-window-latches",
            "name": "Window & Vent Window Latches",
        },
        "window-channels": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/window-channels",
            "name": "Window Channels",
        },
        "window-fuses": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/window-fuses",
            "name": "Window Fuses",
        },
        "window-glass-lift-plate": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/window-glass-lift-plate",
            "name": "Window Glass Lift Plate",
        },
        "window-guides": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/window-guides",
            "name": "Window Guides",
        },
        "window-handles": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/window-handles",
            "name": "Window Handles",
        },
        "window-motors-window-regulators": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/window-motors-window-regulators",
            "name": "Window Motors & Regulators",
        },
        "window-relays": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/window-relays",
            "name": "Window Relays",
        },
        "window-switches": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/window-switches",
            "name": "Window Switches",
        },
        "windshield-molding": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/windshield-molding",
            "name": "Windshields",
        },
    },
    "external-engine": {  # Engines
        "cold-air-intake-systems": {
            "url": "https://www.autozone.com/external-engine/cold-air-intake-systems",
            "name": "Cold Air Intake Systems",
        },
        "engine-auxiliary-balance-intermediate-shafts": {
            "url": "https://www.autozone.com/external-engine/engine-auxiliary-balance-intermediate-shafts",
            "name": "Engine Auxiliary, Balance & Intermediate Shafts",
        },
        "engine-camshafts-bearings-valve-lifters": {
            "url": "https://www.autozone.com/external-engine/engine-camshafts-bearings-valve-lifters",
            "name": "Engine Camshafts, Bearings & Valve Lifters",
        },
        "engine-coolant-sensors-and-sending-units": {
            "url": "https://www.autozone.com/external-engine/engine-coolant-sensors-and-sending-units",
            "name": "Engine Coolant Sensors & Sending Units",
        },
        "engine-covers": {
            "url": "https://www.autozone.com/external-engine/engine-covers",
            "name": "Engine Covers",
        },
        "engine-cradles": {
            "url": "https://www.autozone.com/external-engine/engine-cradles",
            "name": "Engine Cradles",
        },
        "engine-crankshafts-connecting-rods-pistons": {
            "url": "https://www.autozone.com/external-engine/engine-crankshafts-connecting-rods-pistons",
            "name": "Engine Crankshafts, Connecting Rods & Pistons",
        },
        "engine-cylinder-heads-valves-springs-pushrods-and-rockers": {
            "url": "https://www.autozone.com/external-engine/engine-cylinder-heads-valves-springs-pushrods-and-rockers",
            "name": "Engine Cylinder Heads, Valves, Springs, Pushrods & Rockers",
        },
        "engine-dress-up-kits-and-top-end-kits": {
            "url": "https://www.autozone.com/external-engine/engine-dress-up-kits-and-top-end-kits",
            "name": "Engine Dress Up Kits & Top End Kits",
        },
        "engine-gaskets-and-expansion-plugs": {
            "url": "https://www.autozone.com/external-engine/engine-gaskets-and-expansion-plugs",
            "name": "Engine Gaskets & Expansion Plugs",
        },
        "engine-harmonic-balancers-pulleys-repair-sleeves": {
            "url": "https://www.autozone.com/external-engine/engine-harmonic-balancers-pulleys-repair-sleeves",
            "name": "Engine Harmonic Balancers, Pulleys & Repair Sleeves",
        },
        "engine-heaters": {
            "url": "https://www.autozone.com/external-engine/engine-heaters",
            "name": "Engine Heaters",
        },
        "engine-intake-exhaust-valves": {
            "url": "https://www.autozone.com/external-engine/engine-intake-exhaust-valves",
            "name": "Engine Intake & Exhaust Valves",
        },
        "engine-intake-manifold-intake-plenum": {
            "url": "https://www.autozone.com/external-engine/engine-intake-manifold-intake-plenum",
            "name": "Engine Intake Manifold & Intake Plenum",
        },
        "engine-mounts-torque-struts": {
            "url": "https://www.autozone.com/external-engine/engine-mounts-torque-struts",
            "name": "Engine Mounts & Torque Struts",
        },
        "engine-oil-coolers-cooler-lines-hoses-and-connectors": {
            "url": "https://www.autozone.com/external-engine/engine-oil-coolers-cooler-lines-hoses-and-connectors",
            "name": "Engine Oil Coolers, Cooler Lines, Hoses & Connectors",
        },
        "engine-oil-dipstick-tube": {
            "url": "https://www.autozone.com/external-engine/engine-oil-dipstick-tube",
            "name": "Engine Oil Dipstick & Tube",
        },
        "engine-oil-drain-plugs-gasket-seals": {
            "url": "https://www.autozone.com/external-engine/engine-oil-drain-plugs-gasket-seals",
            "name": "Engine Oil Drain Plugs & Gasket Seals",
        },
        "engine-oil-feed-lines": {
            "url": "https://www.autozone.com/external-engine/engine-oil-feed-lines",
            "name": "Engine Oil Feed Lines",
        },
        "engine-oil-filler-tubes-oil-filler-caps": {
            "url": "https://www.autozone.com/external-engine/engine-oil-filler-tubes-oil-filler-caps",
            "name": "Engine Oil Filler Tubes & Oil Filler Caps",
        },
        "engine-oil-filter-housings-gaskets": {
            "url": "https://www.autozone.com/external-engine/engine-oil-filter-housings-gaskets",
            "name": "Engine Oil Filter Housings & Gaskets",
        },
        "engine-oil-level-and-oil-pressure-sensors-and-sending-units": {
            "url": "https://www.autozone.com/external-engine/engine-oil-level-and-oil-pressure-sensors-and-sending-units",
            "name": "Engine Oil Level & Oil Pressure Sensors & Sending Units",
        },
        "engine-oil-pans-oil-sumps-and-oil-separators": {
            "url": "https://www.autozone.com/external-engine/engine-oil-pans-oil-sumps-and-oil-separators",
            "name": "Engine Oil Pans & Oil Sumps",
        },
        "engine-oil-pumps-pickup-tubes-screens": {
            "url": "https://www.autozone.com/external-engine/engine-oil-pumps-pickup-tubes-screens",
            "name": "Engine Oil Pumps, Pickup Tubes & Screens",
        },
        "engine-oil-stand-pipes-tubes": {
            "url": "https://www.autozone.com/external-engine/engine-oil-stand-pipes-tubes",
            "name": "Engine Oil Stand Pipes & Tubes",
        },
        "engine-timing-belts-components": {
            "url": "https://www.autozone.com/external-engine/engine-timing-belts-components",
            "name": "Engine Timing Belts & Components",
        },
        "engine-timing-covers": {
            "url": "https://www.autozone.com/external-engine/engine-timing-covers",
            "name": "Engine Timing Covers",
        },
        "engine-timing-gears-timing-chains-tensioners": {
            "url": "https://www.autozone.com/external-engine/engine-timing-gears-timing-chains-tensioners",
            "name": "Engine Timing Gears, Timing Chains & Tensioners",
        },
        "engine-cylinder-air-deflectors-and-ground-straps": {
            "url": "https://www.autozone.com/external-engine/engine-cylinder-air-deflectors-and-ground-straps",
            "name": "Engine Vacuum Pumps",
        },
        "engine-valve-covers-components": {
            "url": "https://www.autozone.com/external-engine/engine-valve-covers-components",
            "name": "Engine Valve Covers & Components",
        },
        "engine-variable-valve-timing-components": {
            "url": "https://www.autozone.com/external-engine/engine-variable-valve-timing-components",
            "name": "Engine Variable Valve Timing Components",
        },
        "engines-engine-kits": {
            "url": "https://www.autozone.com/external-engine/engines-engine-kits",
            "name": "Engines & Engine Kits",
        },
        "fan-clutches-fan-blades": {
            "url": "https://www.autozone.com/external-engine/fan-clutches-fan-blades",
            "name": "Fan Clutches",
        },
        "fuel-pump-camshaft-followers-and-pushrods": {
            "url": "https://www.autozone.com/external-engine/fuel-pump-camshaft-followers-and-pushrods",
            "name": "Fuel Pump Camshaft Followers & Pushrods",
        },
        "multi-purpose-gasket": {
            "url": "https://www.autozone.com/engines/multi-purpose-gasket",
            "name": "Multi-Purpose Gasket",
        },
        "multi-purpose-o-ring": {
            "url": "https://www.autozone.com/heating-and-cooling/multi-purpose-o-ring",
            "name": "Multi-Purpose O-Ring",
        },
        "multi-purpose-seal": {
            "url": "https://www.autozone.com/external-engine/multi-purpose-seal",
            "name": "Multi-Purpose Seal",
        },
        "multi-purpose-seal-kit": {
            "url": "https://www.autozone.com/external-engine/multi-purpose-seal-kit",
            "name": "Multi-Purpose Seal Kit",
        },
        "multi-purpose-seal-ring": {
            "url": "https://www.autozone.com/external-engine/multi-purpose-seal-ring",
            "name": "Multi-Purpose Seal Ring",
        },
        "performance-parts": {
            "url": "https://www.autozone.com/external-engine/performance-parts",
            "name": "Performance Parts",
        },
        "radiator-cooling-fan-fuses": {
            "url": "https://www.autozone.com/external-engine/radiator-cooling-fan-fuses",
            "name": "Radiator Cooling Fan Fuses",
        },
        "radiator-cooling-fan-sensors-switches": {
            "url": "https://www.autozone.com/external-engine/radiator-cooling-fan-sensors-switches",
            "name": "Radiator Cooling Fan Sensors & Switches",
        },
        "radiator-cooling-fans-modules-relays-resistors": {
            "url": "https://www.autozone.com/external-engine/radiator-cooling-fans-modules-relays-resistors",
            "name": "Radiator Cooling Fans, Modules, Relays & Resistors",
        },
        "radiator-drain-plugs": {
            "url": "https://www.autozone.com/external-engine/radiator-drain-plugs",
            "name": "Radiator Drain Plugs",
        },
        "radiators-caps-coolant-reservoirs": {
            "url": "https://www.autozone.com/external-engine/radiators-caps-coolant-reservoirs",
            "name": "Radiators, Caps, & Coolant Reservoirs",
        },
        "thermostats-and-housings-water-outlets-and-gaskets": {
            "url": "https://www.autozone.com/external-engine/thermostats-and-housings-water-outlets-and-gaskets",
            "name": "Thermostats & Housings, Water Outlets & Gaskets",
        },
        "timing-tape-timing-pointers": {
            "url": "https://www.autozone.com/external-engine/timing-tape-timing-pointers",
            "name": "Timing Mark Tab & Pointer",
        },
        "water-pump-fuses-relays": {
            "url": "https://www.autozone.com/external-engine/water-pump-fuses-relays",
            "name": "Water Pump Fuses & Relays",
        },
        "water-pumps-gaskets-pulleys": {
            "url": "https://www.autozone.com/external-engine/water-pumps-gaskets-pulleys",
            "name": "Water Pumps, Gaskets & Pulleys",
        },
    },
    "emission-control-and-exhaust": {  # Exhaust & Emission Control
        "air-pumps-air-injection": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/air-pumps-air-injection",
            "name": "Air Pumps & AIR Injection",
        },
        "atomization-module-air-drier-filter-mount-kit": {
            "url": "https://www.autozone.com/exhaust-emission-control/atomization-module-air-drier-filter-mount-kit",
            "name": "Atomization Module Air Drier Filter Mount Kit",
        },
        "catalytic-convertors-exhaust-manifolds-manifold-gaskets": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/catalytic-convertors-exhaust-manifolds-manifold-gaskets",
            "name": "Catalytic Convertors, Exhaust Manifolds & Manifold Gaskets",
        },
        "diesel-dpf-particulate-filter-sensors-relays": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/diesel-dpf-particulate-filter-sensors-relays",
            "name": "Diesel DPF Particulate Filter Sensors & Relays",
        },
        "diesel-oxidation-catalyst": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/diesel-oxidation-catalyst",
            "name": "Diesel Oxidation Catalyst",
        },
        "egr-control-relays-solenoids-switches": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/egr-control-relays-solenoids-switches",
            "name": "EGR Control Relays, Solenoids & Switches",
        },
        "egr-cooler-gaskets-hoses-pipes": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/egr-cooler-gaskets-hoses-pipes",
            "name": "EGR Cooler Gaskets, Hoses & Pipes",
        },
        "egr-coolers-installation-kits": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/egr-coolers-installation-kits",
            "name": "EGR Coolers & Sensors",
        },
        "egr-valves-gaskets-feed-pipes": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/egr-valves-gaskets-feed-pipes",
            "name": "EGR Valves, Gaskets & Feed Pipes",
        },
        "emission-check-valve-insulator": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/emission-check-valve-insulator",
            "name": "Emission Check Valve Insulator",
        },
        "exhaust-air-supply-gasket": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/exhaust-air-supply-gasket",
            "name": "Exhaust Air Supply Gasket",
        },
        "exhaust-ammonia-sensor": {
            "url": "https://www.autozone.com/electrical-and-lighting/exhaust-ammonia-sensor",
            "name": "Exhaust Ammonia Sensor",
        },
        "exhaust-ammonia-sensor-control-module": {
            "url": "https://www.autozone.com/electrical-and-lighting/exhaust-ammonia-sensor-control-module",
            "name": "Exhaust Ammonia Sensor Control Module",
        },
        "exhaust-bolts-manifold-bolts-flanges-nuts-studs-and-gaskets": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-bolts-manifold-bolts-flanges-nuts-studs-and-gaskets",
            "name": "Exhaust Bolts, Manifold Bolts, Flanges, Nuts, Studs & Gaskets",
        },
        "exhaust-headers": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-headers",
            "name": "Exhaust Headers",
        },
        "exhaust-hose": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-hose",
            "name": "Exhaust Hose",
        },
        "exhaust-insert-muffler": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-insert-muffler",
            "name": "Exhaust Insert Muffler",
        },
        "exhaust-mufflers-exhaust-pipes-and-tips": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-mufflers-exhaust-pipes-and-tips",
            "name": "Exhaust Mufflers, Exhaust Pipes & Tips",
        },
        "exhaust-pipe-adapters-connectors-reducers": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-pipe-adapters-connectors-reducers",
            "name": "Exhaust Pipe Adapters, Connectors & Reducers",
        },
        "exhaust-silencer-insert": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-silencer-insert",
            "name": "Exhaust Silencer Insert",
        },
        "exhaust-sleeve": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-sleeve",
            "name": "Exhaust Sleeve",
        },
        "exhaust-stack-pipe": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-stack-pipe",
            "name": "Exhaust Stack Pipe",
        },
        "exhaust-stack-pipe-mounting-kit": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-stack-pipe-mounting-kit",
            "name": "Exhaust Stack Pipe Mounting Kit",
        },
        "exhaust-system-suspension-kit": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-system-suspension-kit",
            "name": "Exhaust System - Suspension Kit",
        },
        "exhaust-brackets-clamps-hangers-and-heat-shields": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-brackets-clamps-hangers-and-heat-shields",
            "name": "Exhaust System Mounting Hardware",
        },
        "exhaust-system-wrap": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-system-wrap",
            "name": "Exhaust System Wrap",
        },
        "exhaust-system-wrap-coating": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-system-wrap-coating",
            "name": "Exhaust System Wrap Coating",
        },
        "exhaust-system-wrap-kit": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/exhaust-system-wrap-kit",
            "name": "Exhaust System Wrap Kit",
        },
        "heat-shield-insulator-kit": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/heat-shield-insulator-kit",
            "name": "Heat Shield Insulator Kit",
        },
        "hydrocarbon-injector": {
            "url": "https://www.autozone.com/fuel-delivery/hydrocarbon-injector",
            "name": "Hydrocarbon Injector",
        },
        "solenoid-heat-shield": {
            "url": "https://www.autozone.com/batteries-starting-and-charging/solenoid-heat-shield",
            "name": "Multi-Purpose Heat Shield",
        },
        "vacuum-check-valve": {
            "url": "https://www.autozone.com/engine-management/vacuum-check-valve",
            "name": "Vacuum Check Valve",
        },
    },
    "exterior-accessories": {  # Exterior Accessories
        "atv-soft-sided-bag": {
            "url": "https://www.autozone.com/exterior-accessories/atv-soft-sided-bag",
            "name": "ATV Soft Sided Bag",
        },
        "atv-tool-box": {
            "url": "https://www.autozone.com/exterior-accessories/atv-tool-box",
            "name": "ATV Tool Box",
        },
        "bow-eye": {
            "url": "https://www.autozone.com/exterior-accessories/bow-eye",
            "name": "Bow Eye",
        },
        "power-roofs-circuit-breakers-and-relays": {
            "url": "https://www.autozone.com/exterior-accessories/power-roofs-circuit-breakers-and-relays",
            "name": "Bull Bars & Bumper Guards",
        },
        "camping-travel-vacation": {
            "url": "https://www.autozone.com/exterior-accessories/camping-travel-vacation",
            "name": "Camping, Travel & Vacation",
        },
        "cargo-management": {
            "url": "https://www.autozone.com/exterior-accessories/cargo-management",
            "name": "Cargo Management",
        },
        "decals-emblem-kits": {
            "url": "https://www.autozone.com/exterior-accessories/decals-emblem-kits",
            "name": "Decals & Emblem Kits",
        },
        "exterior-mirrors": {
            "url": "https://www.autozone.com/exterior-accessories/exterior-mirrors",
            "name": "Exterior Mirrors",
        },
        "fuel-storage": {
            "url": "https://www.autozone.com/exterior-accessories/fuel-storage",
            "name": "Fuel Can & Utility Can",
        },
        "garage-door-openers": {
            "url": "https://www.autozone.com/exterior-accessories/garage-door-openers",
            "name": "Garage Door Openers",
        },
        "handle-walk-plate-spring-release": {
            "url": "https://www.autozone.com/truck-bed-accessories/handle-walk-plate-spring-release",
            "name": "Handle Walk Plate Spring Release",
        },
        "hood-appearance": {
            "url": "https://www.autozone.com/front-end-covers-and-hood-products/hood-appearance",
            "name": "Hood Appearance Set",
        },
        "hood-deflectors-bug-guards": {
            "url": "https://www.autozone.com/exterior-accessories/hood-deflectors-bug-guards",
            "name": "Hood Deflectors & Bug Guards",
        },
        "kayak-storage-mount": {
            "url": "https://www.autozone.com/exterior-accessories/kayak-storage-mount",
            "name": "Kayak Storage Mount",
        },
        "license-plates-frames": {
            "url": "https://www.autozone.com/exterior-accessories/license-plates-frames",
            "name": "License Plates & Frames",
        },
        "liquid-transfer-tanks": {
            "url": "https://www.autozone.com/exterior-accessories/liquid-transfer-tanks",
            "name": "Liquid Transfer Tanks",
        },
        "mud-flaps-fender-guards": {
            "url": "https://www.autozone.com/exterior-accessories/mud-flaps-fender-guards",
            "name": "Mud Flaps & Fender Guards",
        },
        "rv-accessories": {
            "url": "https://www.autozone.com/exterior-accessories/rv-accessories",
            "name": "RV Accessories",
        },
        "rain-sensors": {
            "url": "https://www.autozone.com/exterior-accessories/rain-sensors",
            "name": "Rain Sensors",
        },
        "roll-bar-accessories": {
            "url": "https://www.autozone.com/tie-down-and-cargo-management/roll-bar-accessories",
            "name": "Roll Bar",
        },
        "roll-bar-carrier-bracket": {
            "url": "https://www.autozone.com/engine-and-vehicle-lift/roll-bar-carrier-bracket",
            "name": "Roll Bar Carrier Bracket",
        },
        "roll-bar-cover": {
            "url": "https://www.autozone.com/exterior-accessories/roll-bar-cover",
            "name": "Roll Bar Cover",
        },
        "roll-bar-padding": {
            "url": "https://www.autozone.com/tie-down-and-cargo-management/roll-bar-padding",
            "name": "Roll Bar Padding",
        },
        "roof-racks-ladders": {
            "url": "https://www.autozone.com/exterior-accessories/roof-racks-ladders",
            "name": "Roof Racks & Ladders",
        },
        "rope": {
            "url": "https://www.autozone.com/tie-downs-and-tow-straps/rope",
            "name": "Rope",
        },
        "signs": {
            "url": "https://www.autozone.com/exterior-accessories/signs",
            "name": "Signs",
        },
        "step-bars": {
            "url": "https://www.autozone.com/exterior-accessories/step-bars",
            "name": "Step Bars",
        },
        "tarps-vehicle-covers": {
            "url": "https://www.autozone.com/exterior-accessories/tarps-vehicle-covers",
            "name": "Tarps & Vehicle Covers",
        },
        "tire-snow-chains": {
            "url": "https://www.autozone.com/exterior-accessories/tire-snow-chains",
            "name": "Tire & Snow Chains",
        },
        "tonneau-truck-beds": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/tonneau-truck-beds",
            "name": "Tonneau & Truck Beds",
        },
        "truck-cab-accessories": {
            "url": "https://www.autozone.com/exterior-accessories/truck-cab-accessories",
            "name": "Truck Cab Accessories",
        },
        "truck-fairing-latches": {
            "url": "https://www.autozone.com/exterior-accessories/truck-fairing-latches",
            "name": "Truck Fairing Latches",
        },
        "truck-tool-boxes-accessories": {
            "url": "https://www.autozone.com/exterior-accessories/truck-tool-boxes-accessories",
            "name": "Truck Tool Boxes & Accessories",
        },
        "watersport-carrier": {
            "url": "https://www.autozone.com/tie-down-and-cargo-management/watersport-carrier",
            "name": "Watersport Carrier",
        },
        "whip-light": {
            "url": "https://www.autozone.com/exterior-accessories/whip-light",
            "name": "Whip Light",
        },
        "window-guard": {
            "url": "https://www.autozone.com/exterior-accessories/window-guard",
            "name": "Window Guard",
        },
        "window-net": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/window-net",
            "name": "Window Net",
        },
        "window-net-mount": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/window-net-mount",
            "name": "Window Net Mount",
        },
        "windshield-banner": {
            "url": "https://www.autozone.com/exterior-accessories/windshield-banner",
            "name": "Windshield Banner",
        },
    },
    "filters-and-pcv": {  # Filters & PCV
        "air-filters": {
            "url": "https://www.autozone.com/filters-and-pcv/air-filters",
            "name": "Air Filters",
        },
        "diesel-dpf-particulate-filters": {
            "url": "https://www.autozone.com/emission-control-and-exhaust/diesel-dpf-particulate-filters",
            "name": "Diesel DPF Particulate Filters",
        },
        "engine-oil-filters": {
            "url": "https://www.autozone.com/filters-and-pcv/engine-oil-filters",
            "name": "Engine Oil Filters",
        },
        "hydraulic-filter": {
            "url": "https://www.autozone.com/cooling-heating-and-climate-control/hydraulic-filter",
            "name": "Hydraulic Filter",
        },
        "pcv-valves-and-crankcase-ventilation": {
            "url": "https://www.autozone.com/filters-and-pcv/pcv-valves-and-crankcase-ventilation",
            "name": "PCV Valves & Crankcase Ventilation",
        },
    },
    "fuel-and-air-delivery": {  # Fuel & Air Delivery
        "accelerator-cable-throttle-linkage": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/accelerator-cable-throttle-linkage",
            "name": "Accelerator Cable & Throttle Linkage",
        },
        "pedal-position-sensors-and-connectors": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/pedal-position-sensors-and-connectors",
            "name": "Accelerator Pedal Sensors",
        },
        "air-and-fuel-delivery-sensors-solenoids-and-switches": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/air-and-fuel-delivery-sensors-solenoids-and-switches",
            "name": "Air & Fuel Delivery Sensors, Solenoids & Switches",
        },
        "air-cleaner-housings-cases": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/air-cleaner-housings-cases",
            "name": "Air Cleaner Housings & Cases",
        },
        "air-intakes-housings": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/air-intakes-housings",
            "name": "Air Intakes & Housings",
        },
        "carburetors-chokes": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/carburetors-chokes",
            "name": "Carburetors & Chokes",
        },
        "choke-relays": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/choke-relays",
            "name": "Choke Relays",
        },
        "cold-start-injectors-relays": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/cold-start-injectors-relays",
            "name": "Cold Start Injectors & Relays",
        },
        "def-system-components": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/def-system-components",
            "name": "DEF System Components",
        },
        "diesel-fuel-heating-elements": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/diesel-fuel-heating-elements",
            "name": "Diesel Fuel Heating Elements",
        },
        "diesel-fuel-injection-system": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/diesel-fuel-injection-system",
            "name": "Diesel Fuel Injection System",
        },
        "engine-shut-down-relays-switches": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/engine-shut-down-relays-switches",
            "name": "Engine Shut Down Relays & Switches",
        },
        "fuel-caps-fuel-cap-tethers": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/fuel-caps-fuel-cap-tethers",
            "name": "Fuel Caps & Fuel Cap Tethers",
        },
        "fuel-filters-fuel-filter-caps-fuel-filter-housings": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/fuel-filters-fuel-filter-caps-fuel-filter-housings",
            "name": "Fuel Filters, Fuel Filter Caps & Fuel Filter Housings",
        },
        "fuel-heater-relays": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/fuel-heater-relays",
            "name": "Fuel Heater Relays",
        },
        "fuel-heaters": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/fuel-heaters",
            "name": "Fuel Heaters",
        },
        "fuel-hoses-fuel-lines": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/fuel-hoses-fuel-lines",
            "name": "Fuel Hoses & Fuel Lines",
        },
        "fuel-injectors-o-ring-seals-fuel-rails": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/fuel-injectors-o-ring-seals-fuel-rails",
            "name": "Fuel Injectors, O-Ring Seals & Fuel Rails",
        },
        "fuel-pressure-sensors-regulators-dampers": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/fuel-pressure-sensors-regulators-dampers",
            "name": "Fuel Pressure Sensors, Regulators & Dampers",
        },
        "fuel-pump-inertia-switch-auto-shut-down": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/fuel-pump-inertia-switch-auto-shut-down",
            "name": "Fuel Pump Inertia Switch & Auto Shut Down",
        },
        "fuel-pumps-strainers-sending-units-fuel-tanks-and-filler-hoses": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/fuel-pumps-strainers-sending-units-fuel-tanks-and-filler-hoses",
            "name": "Fuel Pumps, Strainers, Sending Units, Fuel Tanks & Filler Hoses",
        },
        "fuel-system-control-relays": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/fuel-system-control-relays",
            "name": "Fuel System Control Relays",
        },
        "idle-speed-control": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/idle-speed-control",
            "name": "Idle Speed Control",
        },
        "liquid-propane-gas-lpg-fuel-feed-hose": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/liquid-propane-gas-lpg-fuel-feed-hose",
            "name": "Liquid Propane Gas (LPG) Fuel Feed Hose",
        },
        "liquid-propane-gas-lpg-fuel-feed-hose-kit": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/liquid-propane-gas-lpg-fuel-feed-hose-kit",
            "name": "Liquid Propane Gas (LPG) Fuel Feed Hose Kit",
        },
        "liquid-propane-gas-lpg-fuel-filler-hose": {
            "url": "https://www.autozone.com/fuel-air-delivery/liquid-propane-gas-lpg-fuel-filler-hose",
            "name": "Liquid Propane Gas (LPG) Fuel Filler Hose",
        },
        "liquid-propane-gas-lpg-fuel-tank": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/liquid-propane-gas-lpg-fuel-tank",
            "name": "Liquid Propane Gas (LPG) Fuel Tank",
        },
        "liquid-propane-gas-lpg-fuel-tank-bracket": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/liquid-propane-gas-lpg-fuel-tank-bracket",
            "name": "Liquid Propane Gas (LPG) Fuel Tank Bracket",
        },
        "liquid-propane-gas-lpg-fuel-tank-drain-valve": {
            "url": "https://www.autozone.com/fuel-air-delivery/liquid-propane-gas-lpg-fuel-tank-drain-valve",
            "name": "Liquid Propane Gas (LPG) Fuel Tank Drain Valve",
        },
        "liquid-propane-gas-lpg-low-pressure-regulator": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/liquid-propane-gas-lpg-low-pressure-regulator",
            "name": "Liquid Propane Gas (LPG) Low Pressure Regulator",
        },
        "liquid-propane-gas-lpg-tank-filler-cap": {
            "url": "https://www.autozone.com/fuel-air-delivery/liquid-propane-gas-lpg-tank-filler-cap",
            "name": "Liquid Propane Gas (LPG) Tank Filler Cap",
        },
        "liquid-propane-gas-tank-filler-hose-fitting": {
            "url": "https://www.autozone.com/fittings-and-hose-line-connectors/liquid-propane-gas-tank-filler-hose-fitting",
            "name": "Liquid Propane Gas (LPG) Tank Filler Hose Fitting",
        },
        "shut-off-valve": {
            "url": "https://www.autozone.com/fuel-systems/shut-off-valve",
            "name": "Shut-Off Valve",
        },
        "throttle-body-throttle-actuators": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/throttle-body-throttle-actuators",
            "name": "Throttle Body & Throttle Actuators",
        },
        "throttle-plates": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/throttle-plates",
            "name": "Throttle Plates",
        },
        "wide-open-throttle-relays-switches": {
            "url": "https://www.autozone.com/fuel-and-air-delivery/wide-open-throttle-relays-switches",
            "name": "Wide Open Throttle Relays & Switches",
        },
    },
    "paint-and-body": {  # Paint & Adhesive
        "adhesives": {
            "url": "https://www.autozone.com/paint-and-body/adhesives",
            "name": "Adhesives",
        },
        "epoxy-sealants-tape": {
            "url": "https://www.autozone.com/paint-and-body/epoxy-sealants-tape",
            "name": "Epoxy, Sealants & Tape",
        },
        "paint-primer-tack-cloth": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/paint-primer-tack-cloth",
            "name": "Paint, Primer & Tack Cloth",
        },
        "truck-bed-coating": {
            "url": "https://www.autozone.com/paint-and-body/truck-bed-coating",
            "name": "Truck Bed Coating",
        },
    },
    "powertrain": {  # Power Train & Drive Train
        "axles-cv-axles-wheel-bearings-and-seals": {
            "url": "https://www.autozone.com/powertrain/axles-cv-axles-wheel-bearings-and-seals",
            "name": "Axles, CV Axles, Wheel Bearings & Seals",
        },
        "clutch-flywheel": {
            "url": "https://www.autozone.com/powertrain/clutch-flywheel",
            "name": "Clutch & Flywheel",
        },
        "differentials-carriers-bearings": {
            "url": "https://www.autozone.com/powertrain/differentials-carriers-bearings",
            "name": "Differentials, Carriers & Bearings",
        },
        "driveshafts-and-universal-joints": {
            "url": "https://www.autozone.com/powertrain/driveshafts-and-universal-joints",
            "name": "Driveshafts & Universal Joints",
        },
        "engine-management-obd-ii": {
            "url": "https://www.autozone.com/powertrain/engine-management-obd-ii",
            "name": "Engine Management OBD II",
        },
        "hybrid-electric-vehicles": {
            "url": "https://www.autozone.com/batteries-starting-and-charging/hybrid-electric-vehicles",
            "name": "Hybrid & Electric Vehicles",
        },
        "ignition-system": {
            "url": "https://www.autozone.com/powertrain/ignition-system",
            "name": "Ignition System",
        },
        "multi-purpose-bearing": {
            "url": "https://www.autozone.com/power-train-drive-train/multi-purpose-bearing",
            "name": "Multi-Purpose Bearing",
        },
        "multi-purpose-bearing-race-set": {
            "url": "https://www.autozone.com/power-train-drive-train/multi-purpose-bearing-race-set",
            "name": "Multi-Purpose Bearing & Race Set",
        },
        "multi-purpose-bushing": {
            "url": "https://www.autozone.com/power-train-drive-train/multi-purpose-bushing",
            "name": "Multi-Purpose Bushing",
        },
        "multi-purpose-race": {
            "url": "https://www.autozone.com/power-train-drive-train/multi-purpose-race",
            "name": "Multi-Purpose Race",
        },
        "pto-power-take-off": {
            "url": "https://www.autozone.com/powertrain/pto-power-take-off",
            "name": "PTO Power Take Off",
        },
        "taper-bearing-cone": {
            "url": "https://www.autozone.com/power-train-drive-train/taper-bearing-cone",
            "name": "Taper Bearing Cone",
        },
        "taper-bearing-outer-race": {
            "url": "https://www.autozone.com/power-train-drive-train/taper-bearing-outer-race",
            "name": "Taper Bearing Outer Race",
        },
        "transfer-case-4wd-awd": {
            "url": "https://www.autozone.com/powertrain/transfer-case-4wd-awd",
            "name": "Transfer Case 4WD & AWD",
        },
        "transmissions": {
            "url": "https://www.autozone.com/powertrain/transmissions",
            "name": "Transmissions",
        },
        "wheel-locking-collar": {
            "url": "https://www.autozone.com/power-train-drive-train/wheel-locking-collar",
            "name": "Wheel Locking Collar",
        },
    },
    "suspension-steering-tire-and-wheel": {  # Steering & Suspension
        "axle-beams": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/axle-beams",
            "name": "Axle Beams",
        },
        "ball-joints-control-arms": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/ball-joints-control-arms",
            "name": "Ball Joints & Control Arms",
        },
        "bump-stop-jounce-bumper": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/bump-stop-jounce-bumper",
            "name": "Bump Stop & Jounce Bumper",
        },
        "centerlinks-idler-arms-pitman-arms-tie-rods": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/centerlinks-idler-arms-pitman-arms-tie-rods",
            "name": "Centerlinks, Idler Arms, Pitman Arms & Tie Rods",
        },
        "coil-springs-leaf-springs-torsion-bars": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/coil-springs-leaf-springs-torsion-bars",
            "name": "Coil Springs, Leaf Springs & Torsion Bars",
        },
        "king-pin-bushing-kits": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/king-pin-bushing-kits",
            "name": "King Pin & Bushing Kits",
        },
        "power-steering-assist-motors": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/power-steering-assist-motors",
            "name": "Power Steering Assist Motors",
        },
        "power-steering-control-modules": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/power-steering-control-modules",
            "name": "Power Steering Control Modules",
        },
        "power-steering-coolers": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/power-steering-coolers",
            "name": "Power Steering Coolers",
        },
        "power-steering-hoses-lines": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/power-steering-hoses-lines",
            "name": "Power Steering Hoses & Lines",
        },
        "power-steering-pumps-pulleys-reservoirs": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/power-steering-pumps-pulleys-reservoirs",
            "name": "Power Steering Pumps, Pulleys & Reservoirs",
        },
        "power-steering-relays": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/power-steering-relays",
            "name": "Power Steering Relays",
        },
        "power-steering-sensors-and-switches": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/power-steering-sensors-and-switches",
            "name": "Power Steering Sensors & Switches",
        },
        "rack-pinions": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/rack-pinions",
            "name": "Rack & Pinions",
        },
        "radius-arms-bushings": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/radius-arms-bushings",
            "name": "Radius Arms & Bushings",
        },
        "rod-end": {
            "url": "https://www.autozone.com/external-engine/rod-end",
            "name": "Rod End",
        },
        "shocks-struts-air-ride-suspension": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/shocks-struts-air-ride-suspension",
            "name": "Shocks, Struts & Air Ride Suspension",
        },
        "stability-suspension-relays-sensors": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/stability-suspension-relays-sensors",
            "name": "Stability & Suspension Relays & Sensors",
        },
        "stabilizer-bars-stabilizer-links-steering-dampers": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/stabilizer-bars-stabilizer-links-steering-dampers",
            "name": "Stabilizer Bars, Stabilizer Links & Steering Dampers",
        },
        "steering-suspension-fuses": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/steering-suspension-fuses",
            "name": "Steering & Suspension Fuses",
        },
        "steering-and-suspension-knuckles-spindles-and-spindle-lock-nuts": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/steering-and-suspension-knuckles-spindles-and-spindle-lock-nuts",
            "name": "Steering & Suspension Knuckles, Spindles & Lock Nuts",
        },
        "steering-columns-intermediate-steering-shafts": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/steering-columns-intermediate-steering-shafts",
            "name": "Steering Columns & Intermediate Steering Shafts",
        },
        "steering-gear-boxes-repair-kits": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/steering-gear-boxes-repair-kits",
            "name": "Steering Gear Boxes & Repair Kits",
        },
        "subframe-components": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/subframe-components",
            "name": "Subframe Components",
        },
        "suspension-guide-rods-integral-links": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/suspension-guide-rods-integral-links",
            "name": "Suspension Guide Rods & Integral Links",
        },
        "suspension-kits": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/suspension-kits",
            "name": "Suspension Kits",
        },
        "track-bars-traction-bars": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/track-bars-traction-bars",
            "name": "Track Bars & Traction Bars",
        },
        "lateral-arms-trailing-arms": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/lateral-arms-trailing-arms",
            "name": "Trailing Arms",
        },
        "trunnion": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/trunnion",
            "name": "Trunnion",
        },
        "trunnion-bushing": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/trunnion-bushing",
            "name": "Trunnion Bushing",
        },
        "watts-links-bushings": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/watts-links-bushings",
            "name": "Watts Links & Bushings",
        },
        "wheel-alignment-specialty-parts": {
            "url": "https://www.autozone.com/suspension-steering-tire-and-wheel/wheel-alignment-specialty-parts",
            "name": "Wheel Alignment Specialty Parts",
        },
    },
    "tire-repair-and-tire-wheel": {  # Tire & Wheel
        "lug-nuts-lugs-studs-lug-wheel-locks": {
            "url": "https://www.autozone.com/tire-repair-and-tire-wheel/lug-nuts-lugs-studs-lug-wheel-locks",
            "name": "Lug Nuts, Lugs Studs, Lug Wheel Locks",
        },
        "lug-wrenches": {
            "url": "https://www.autozone.com/tire-repair-and-tire-wheel/lug-wrenches",
            "name": "Lug Wrenches",
        },
        "spare-jack-equipment-spare-tires": {
            "url": "https://www.autozone.com/tire-repair-and-tire-wheel/spare-jack-equipment-spare-tires",
            "name": "Spare Jack Equipment & Spare Tires",
        },
        "tpms-tire-valve-stems-caps-cores": {
            "url": "https://www.autozone.com/tire-repair-and-tire-wheel/tpms-tire-valve-stems-caps-cores",
            "name": "TPMS, Tire Valve Stems, Caps & Cores",
        },
        "tire-repair": {
            "url": "https://www.autozone.com/tire-repair-and-tire-wheel/tire-repair",
            "name": "Tire Repair",
        },
        "wheel-caps-wheel-covers": {
            "url": "https://www.autozone.com/tire-repair-and-tire-wheel/wheel-caps-wheel-covers",
            "name": "Wheel Caps & Wheel Covers",
        },
        "wheel-rim-guard-wheel-trim-rings": {
            "url": "https://www.autozone.com/tire-repair-and-tire-wheel/wheel-rim-guard-wheel-trim-rings",
            "name": "Wheel Rim Guard & Wheel Trim Rings",
        },
        "wheel-skin": {
            "url": "https://www.autozone.com/tire-repair-and-tire-wheel/wheel-skin",
            "name": "Wheel Skin",
        },
        "wheels-wheel-dust-shields-spacers-installation-kits": {
            "url": "https://www.autozone.com/tire-repair-and-tire-wheel/wheels-wheel-dust-shields-spacers-installation-kits",
            "name": "Wheels, Dust Shields, Wheel Adapters, Spacers & Kits",
        },
    },
    "tools-and-equipment": {  # Tools & Garage Equipment
        "ac-repair-service": {
            "url": "https://www.autozone.com/tools-and-equipment/ac-repair-service",
            "name": "AC Repair & Service",
        },
        "an-fittings": {
            "url": "https://www.autozone.com/tools-and-equipment/an-fittings",
            "name": "AN Fittings",
        },
        "air-and-power-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/air-and-power-tools",
            "name": "Air Compressors & Air Tools",
        },
        "air-line-junction-block": {
            "url": "https://www.autozone.com/tools-and-equipment/air-line-junction-block",
            "name": "Air Line Junction Block",
        },
        "air-pressure-gauge": {
            "url": "https://www.autozone.com/tools-and-equipment/air-pressure-gauge",
            "name": "Air Pressure Gauge",
        },
        "alternator-battery-testing-repair": {
            "url": "https://www.autozone.com/tools-and-equipment/alternator-battery-testing-repair",
            "name": "Alternator, Battery Testing & Repair",
        },
        "battery-service-repair": {
            "url": "https://www.autozone.com/tools-and-equipment/battery-service-repair",
            "name": "Battery Service & Repair",
        },
        "bearing-grease-packers": {
            "url": "https://www.autozone.com/tools-and-equipment/bearing-grease-packers",
            "name": "Bearing Grease Packers",
        },
        "belt-tensioner-tools-and-tension-gauges": {
            "url": "https://www.autozone.com/tools-and-equipment/belt-tensioner-tools-and-tension-gauges",
            "name": "Belt Tensioner Tools & Tension Gauges",
        },
        "bench-grinders-accessories": {
            "url": "https://www.autozone.com/tools-and-equipment/bench-grinders-accessories",
            "name": "Bench Grinders & Accessories",
        },
        "bit-drivers-driver-bits": {
            "url": "https://www.autozone.com/tools-and-equipment/bit-drivers-driver-bits",
            "name": "Bit Drivers & Driver Bits",
        },
        "body-work-painting": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/body-work-painting",
            "name": "Body Work & Painting",
        },
        "bolt-cutters": {
            "url": "https://www.autozone.com/tools-and-equipment/bolt-cutters",
            "name": "Bolt Cutters",
        },
        "bolts-nuts-washers": {
            "url": "https://www.autozone.com/tools-and-equipment/bolts-nuts-washers",
            "name": "Bolts, Nuts & Washers",
        },
        "borescopes": {
            "url": "https://www.autozone.com/tools-and-equipment/borescopes",
            "name": "Borescopes",
        },
        "braided-hose-spreader": {
            "url": "https://www.autozone.com/tools-and-equipment/braided-hose-spreader",
            "name": "Braided Hose Spreader",
        },
        "brake-bleeding": {
            "url": "https://www.autozone.com/tools-and-equipment/brake-bleeding",
            "name": "Brake Bleeding",
        },
        "brake-lathes-equipment": {
            "url": "https://www.autozone.com/tools-and-equipment/brake-lathes-equipment",
            "name": "Brake Lathes & Equipment",
        },
        "brakes-wheel-bearing-repair": {
            "url": "https://www.autozone.com/tools-and-equipment/brakes-wheel-bearing-repair",
            "name": "Brakes & Wheel Bearing Repair",
        },
        "breaker-bars-ratchets-sockets-extensions": {
            "url": "https://www.autozone.com/tools-and-equipment/breaker-bars-ratchets-sockets-extensions",
            "name": "Breaker Bars, Ratchets, Sockets & Extensions",
        },
        "brooms-brushes": {
            "url": "https://www.autozone.com/tools-and-equipment/brooms-brushes",
            "name": "Brooms & Brushes",
        },
        "buckets-containers": {
            "url": "https://www.autozone.com/tools-and-equipment/buckets-containers",
            "name": "Buckets & Containers",
        },
        "bulk-fluid-metering-device": {
            "url": "https://www.autozone.com/tools-and-equipment/bulk-fluid-metering-device",
            "name": "Bulk Fluid Metering Device",
        },
        "bulk-hose": {
            "url": "https://www.autozone.com/tools-and-equipment/bulk-hose",
            "name": "Bulk Hose",
        },
        "carabiner-set": {
            "url": "https://www.autozone.com/tools-and-equipment/carabiner-set",
            "name": "Carabiner Set",
        },
        "caulk-guns": {
            "url": "https://www.autozone.com/tools-and-equipment/caulk-guns",
            "name": "Caulk Guns",
        },
        "chain-quick-link": {
            "url": "https://www.autozone.com/tools-and-equipment/chain-quick-link",
            "name": "Chain Quick Link",
        },
        "clamp-on-hose-fitting": {
            "url": "https://www.autozone.com/tools-and-equipment/clamp-on-hose-fitting",
            "name": "Clamp-On Hose Fitting",
        },
        "clamps": {
            "url": "https://www.autozone.com/tools-and-equipment/clamps",
            "name": "Clamps",
        },
        "clevis-hook": {
            "url": "https://www.autozone.com/tools-and-equipment/clevis-hook",
            "name": "Clevis Hook",
        },
        "clevis-pin": {
            "url": "https://www.autozone.com/tools-and-equipment/clevis-pin",
            "name": "Clevis Pin",
        },
        "clips-fasteners-retainers-snap-rings": {
            "url": "https://www.autozone.com/tools-and-equipment/clips-fasteners-retainers-snap-rings",
            "name": "Clips, Fasteners, Retainers & Snap Rings",
        },
        "clutch-flywheel-tools": {
            "url": "https://www.autozone.com/powertrain/clutch-flywheel-tools",
            "name": "Clutch & Flywheel Tools",
        },
        "code-readers-scanners": {
            "url": "https://www.autozone.com/tools-and-equipment/code-readers-scanners",
            "name": "Code Readers & Scanners",
        },
        "compression-flare-fittings": {
            "url": "https://www.autozone.com/tools-and-equipment/compression-flare-fittings",
            "name": "Compression & Flare Fittings",
        },
        "cooling-system-service": {
            "url": "https://www.autozone.com/tools-and-equipment/cooling-system-service",
            "name": "Cooling System Service",
        },
        "cotter-pins-assortments": {
            "url": "https://www.autozone.com/tools-and-equipment/cotter-pins-assortments",
            "name": "Cotter Pins & Assortments",
        },
        "joint-router": {
            "url": "https://www.autozone.com/tools-and-equipment/joint-router",
            "name": "Crack-Joint Router",
        },
        "crimping-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/crimping-tools",
            "name": "Crimping Tools",
        },
        "deburring-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/deburring-tools",
            "name": "Deburring Tools",
        },
        "deck-plate-key-and-tool": {
            "url": "https://www.autozone.com/tools-and-equipment/deck-plate-key-and-tool",
            "name": "Deck Plate Key & Tool",
        },
        "diaphragm-pump": {
            "url": "https://www.autozone.com/tools-and-equipment/diaphragm-pump",
            "name": "Diaphragm Pump",
        },
        "diesel-exhaust-fluid-def-storage-drum-transfer-cart": {
            "url": "https://www.autozone.com/shop-presses-equipment/diesel-exhaust-fluid-def-storage-drum-transfer-cart",
            "name": "Diesel Exhaust Fluid (DEF) Storage Drum Transfer Cart",
        },
        "differential-fluid-exchangers": {
            "url": "https://www.autozone.com/tools-and-equipment/differential-fluid-exchangers",
            "name": "Differential Fluid Exchangers",
        },
        "drain-pans": {
            "url": "https://www.autozone.com/tools-and-equipment/drain-pans",
            "name": "Drain Pans",
        },
        "drain-plug-assortments": {
            "url": "https://www.autozone.com/tools-and-equipment/drain-plug-assortments",
            "name": "Drain Plug Assortments",
        },
        "drills-drill-bits": {
            "url": "https://www.autozone.com/tools-and-equipment/drills-drill-bits",
            "name": "Drills & Drill Bits",
        },
        "drip-pan": {
            "url": "https://www.autozone.com/tools-and-equipment/drip-pan",
            "name": "Drip Pan",
        },
        "drip-rail-molding": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/drip-rail-molding",
            "name": "Drip Rail Molding",
        },
        "drum-pumps": {
            "url": "https://www.autozone.com/tools-and-equipment/drum-pumps",
            "name": "Drum Pumps",
        },
        "electrical-testing-tools-and-soldering": {
            "url": "https://www.autozone.com/tools-and-equipment/electrical-testing-tools-and-soldering",
            "name": "Electrical Testing Tools & Soldering",
        },
        "engine-inspection-testing": {
            "url": "https://www.autozone.com/tools-and-equipment/engine-inspection-testing",
            "name": "Engine Inspection & Testing",
        },
        "engine-repair-replacement": {
            "url": "https://www.autozone.com/tools-and-equipment/engine-repair-replacement",
            "name": "Engine Repair & Replacement",
        },
        "engraving-machine": {
            "url": "https://www.autozone.com/tools-and-equipment/engraving-machine",
            "name": "Engraving Machine",
        },
        "exhaust-system-service-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/exhaust-system-service-tools",
            "name": "Exhaust System Service Tools",
        },
        "extension-cords": {
            "url": "https://www.autozone.com/tools-and-equipment/extension-cords",
            "name": "Extension Cords",
        },
        "extension-spring": {
            "url": "https://www.autozone.com/tools-and-equipment/extension-spring",
            "name": "Extension Spring",
        },
        "external-retaining-ring-assortment": {
            "url": "https://www.autozone.com/tools-and-equipment/external-retaining-ring-assortment",
            "name": "External Retaining Ring Assortment",
        },
        "fastener-removers": {
            "url": "https://www.autozone.com/tools-and-equipment/fastener-removers",
            "name": "Fastener Removers",
        },
        "fender-covers": {
            "url": "https://www.autozone.com/tools-and-equipment/fender-covers",
            "name": "Fender Covers",
        },
        "files": {
            "url": "https://www.autozone.com/tools-and-equipment/files",
            "name": "Files",
        },
        "flaring-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/flaring-tools",
            "name": "Flaring Tools",
        },
        "flashlights-shop-lights": {
            "url": "https://www.autozone.com/tools-and-equipment/flashlights-shop-lights",
            "name": "Flashlights & Shop Lights",
        },
        "floor-plug": {
            "url": "https://www.autozone.com/engine/floor-plug",
            "name": "Floor Plug",
        },
        "fluid-cooler-tube": {
            "url": "https://www.autozone.com/tools-and-equipment/fluid-cooler-tube",
            "name": "Fluid Cooler Tube",
        },
        "fluid-hand-pump-adapter": {
            "url": "https://www.autozone.com/tools-and-equipment/fluid-hand-pump-adapter",
            "name": "Fluid Hand Pump Adapter",
        },
        "foot-rest": {
            "url": "https://www.autozone.com/tools-and-equipment/foot-rest",
            "name": "Foot Rest",
        },
        "foot-stool": {
            "url": "https://www.autozone.com/tools-and-equipment/foot-stool",
            "name": "Foot Stool",
        },
        "fuel-injector-testing-repair": {
            "url": "https://www.autozone.com/tools-and-equipment/fuel-injector-testing-repair",
            "name": "Fuel Injector Testing & Repair",
        },
        "fuel-line-bending-fuel-line-repair": {
            "url": "https://www.autozone.com/tools-and-equipment/fuel-line-bending-fuel-line-repair",
            "name": "Fuel Line Bending & Fuel Line Repair",
        },
        "fuel-pressure-testers-carburetor-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/fuel-pressure-testers-carburetor-tools",
            "name": "Fuel Pressure Testers & Carburetor Tools",
        },
        "fuel-pump-installation-removal-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/fuel-pump-installation-removal-tools",
            "name": "Fuel Pump Replacement Tools",
        },
        "fuel-tester": {
            "url": "https://www.autozone.com/test-scan-and-specialty-tools/fuel-tester",
            "name": "Fuel Tester",
        },
        "fuel-transfer-hose": {
            "url": "https://www.autozone.com/tools-garage-equipment/fuel-transfer-hose",
            "name": "Fuel Transfer Hose",
        },
        "fuel-transfer-hose-nozzle": {
            "url": "https://www.autozone.com/tools-and-equipment/fuel-transfer-hose-nozzle",
            "name": "Fuel Transfer Hose Nozzle",
        },
        "fuel-transfer-pump": {
            "url": "https://www.autozone.com/tools-and-equipment/fuel-transfer-pump",
            "name": "Fuel Transfer Pump",
        },
        "fuel-transfer-tank-filter": {
            "url": "https://www.autozone.com/tools-garage-equipment/fuel-transfer-tank-filter",
            "name": "Fuel Transfer Tank Filter",
        },
        "fuel-transfer-tank-kit": {
            "url": "https://www.autozone.com/tools-garage-equipment/fuel-transfer-tank-kit",
            "name": "Fuel Transfer Tank Kit",
        },
        "fuel-transfer-unit-tube": {
            "url": "https://www.autozone.com/tools-garage-equipment/fuel-transfer-unit-tube",
            "name": "Fuel Transfer Unit Tube",
        },
        "funnels": {
            "url": "https://www.autozone.com/tools-and-equipment/funnels",
            "name": "Funnels",
        },
        "garage-shop": {
            "url": "https://www.autozone.com/tools-and-equipment/garage-shop",
            "name": "Garage & Shop",
        },
        "garage-door-opener-switch": {
            "url": "https://www.autozone.com/tools-and-equipment/garage-door-opener-switch",
            "name": "Garage Door Opener Switch",
        },
        "garage-door-opener-transmitter": {
            "url": "https://www.autozone.com/tools-and-equipment/garage-door-opener-transmitter",
            "name": "Garage Door Opener Transmitter",
        },
        "garage-door-transmitter": {
            "url": "https://www.autozone.com/tools-and-equipment/garage-door-transmitter",
            "name": "Garage Door Transmitter",
        },
        "garage-door-transmitter-control-module": {
            "url": "https://www.autozone.com/tools-and-equipment/garage-door-transmitter-control-module",
            "name": "Garage Door Transmitter Control Module",
        },
        "garage-door-transmitter-control-module-bracket": {
            "url": "https://www.autozone.com/tools-and-equipment/garage-door-transmitter-control-module-bracket",
            "name": "Garage Door Transmitter Control Module Bracket",
        },
        "garage-floor-protection-mat": {
            "url": "https://www.autozone.com/tools-and-equipment/garage-floor-protection-mat",
            "name": "Garage Floor Protection Mat",
        },
        "garage-screen": {
            "url": "https://www.autozone.com/tools-and-equipment/garage-screen",
            "name": "Garage Screen",
        },
        "garage-wall-protector": {
            "url": "https://www.autozone.com/tools-and-equipment/garage-wall-protector",
            "name": "Garage Wall Protector",
        },
        "general-maintenance-hardware-assortment": {
            "url": "https://www.autozone.com/tools-and-equipment/general-maintenance-hardware-assortment",
            "name": "General Maintenance Hardware Assortment",
        },
        "gloves-shop-towels": {
            "url": "https://www.autozone.com/tools-and-equipment/gloves-shop-towels",
            "name": "Gloves & Shop Towels",
        },
        "grease-guns-accessories": {
            "url": "https://www.autozone.com/tools-and-equipment/grease-guns-accessories",
            "name": "Grease Guns & Accessories",
        },
        "grinders": {
            "url": "https://www.autozone.com/tools-and-equipment/grinders",
            "name": "Grinders",
        },
        "grommet-assortments": {
            "url": "https://www.autozone.com/tools-and-equipment/grommet-assortments",
            "name": "Grommet Assortments",
        },
        "hammers-slide-hammers": {
            "url": "https://www.autozone.com/tools-and-equipment/hammers-slide-hammers",
            "name": "Hammers & Slide Hammers",
        },
        "hand-cleaners": {
            "url": "https://www.autozone.com/tools-and-equipment/hand-cleaners",
            "name": "Hand Cleaners",
        },
        "hand-held-oiler": {
            "url": "https://www.autozone.com/tools-and-equipment/hand-held-oiler",
            "name": "Hand Held Oiler",
        },
        "hand-hoist": {
            "url": "https://www.autozone.com/tools-and-equipment/hand-hoist",
            "name": "Hand Hoist",
        },
        "head-mounted-work-light": {
            "url": "https://www.autozone.com/tools-and-equipment/head-mounted-work-light",
            "name": "Head-Mounted Work Light",
        },
        "heat-guns": {
            "url": "https://www.autozone.com/tools-and-equipment/heat-guns",
            "name": "Heat Guns",
        },
        "hex-star-keys": {
            "url": "https://www.autozone.com/tools-and-equipment/hex-star-keys",
            "name": "Hex & Star Keys",
        },
        "hones": {
            "url": "https://www.autozone.com/tools-and-equipment/hones",
            "name": "Hones",
        },
        "hook-and-loop-strap": {
            "url": "https://www.autozone.com/tools-and-equipment/hook-and-loop-strap",
            "name": "Hook & Loop Strap",
        },
        "hook-picks": {
            "url": "https://www.autozone.com/tools-and-equipment/hook-picks",
            "name": "Hook & Picks",
        },
        "hose-clamps": {
            "url": "https://www.autozone.com/tools-and-equipment/hose-clamps",
            "name": "Hose Clamps",
        },
        "hose-end-wrench": {
            "url": "https://www.autozone.com/tools-and-equipment/hose-end-wrench",
            "name": "Hose End Wrench",
        },
        "hose-expander-kit": {
            "url": "https://www.autozone.com/tools-and-equipment/hose-expander-kit",
            "name": "Hose Expander Kit",
        },
        "hose-installation-tool": {
            "url": "https://www.autozone.com/tools-and-equipment/hose-installation-tool",
            "name": "Hose Installation Tool",
        },
        "hose-merchandiser": {
            "url": "https://www.autozone.com/tools-and-equipment/hose-merchandiser",
            "name": "Hose Merchandiser",
        },
        "hose-reducer": {
            "url": "https://www.autozone.com/tools-and-equipment/hose-reducer",
            "name": "Hose Reducer",
        },
        "hydraulic-coupling-adapter": {
            "url": "https://www.autozone.com/tools-and-equipment/hydraulic-coupling-adapter",
            "name": "Hydraulic Coupling - Adapter",
        },
        "hydraulic-pump": {
            "url": "https://www.autozone.com/tools-and-equipment/hydraulic-pump",
            "name": "Hydraulic Pump",
        },
        "hydrometer": {
            "url": "https://www.autozone.com/tools-and-equipment/hydrometer",
            "name": "Hydrometer",
        },
        "ignition-system-and-obd-ii": {
            "url": "https://www.autozone.com/tools-and-equipment/ignition-system-and-obd-ii",
            "name": "Ignition System &  OBD II",
        },
        "infrared-thermometer": {
            "url": "https://www.autozone.com/tools-and-equipment/infrared-thermometer",
            "name": "Infrared Thermometer",
        },
        "instructional-video-cd-dvd": {
            "url": "https://www.autozone.com/tools-and-equipment/instructional-video-cd-dvd",
            "name": "Instructional Video - CD - DVD",
        },
        "interior-upholstery-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/interior-upholstery-tools",
            "name": "Interior & Upholstery Tools",
        },
        "jacks-jack-stands": {
            "url": "https://www.autozone.com/tools-and-equipment/jacks-jack-stands",
            "name": "Jacks & Jack Stands",
        },
        "key-cutting": {
            "url": "https://www.autozone.com/tools-and-equipment/key-cutting",
            "name": "Key Cutting",
        },
        "kitchen-scissors": {
            "url": "https://www.autozone.com/tools-and-equipment/kitchen-scissors",
            "name": "Kitchen Scissors",
        },
        "knee-pad-set": {
            "url": "https://www.autozone.com/tools-and-equipment/knee-pad-set",
            "name": "Knee Pad Set",
        },
        "knives-scrapers-snips-scissors": {
            "url": "https://www.autozone.com/tools-and-equipment/knives-scrapers-snips-scissors",
            "name": "Knives, Scrapers, Snips, & Scissors",
        },
        "lanyard": {
            "url": "https://www.autozone.com/tools-and-equipment/lanyard",
            "name": "Lanyard",
        },
        "lateral-accelerometer-gauge": {
            "url": "https://www.autozone.com/tools-and-equipment/lateral-accelerometer-gauge",
            "name": "Lateral Accelerometer Gauge",
        },
        "lawn-garden": {
            "url": "https://www.autozone.com/tools-and-equipment/lawn-garden",
            "name": "Lawn & Garden",
        },
        "levels": {
            "url": "https://www.autozone.com/tools-and-equipment/levels",
            "name": "Levels",
        },
        "lift-table": {
            "url": "https://www.autozone.com/tools-garage-equipment/lift-table",
            "name": "Lift Table",
        },
        "lifts": {
            "url": "https://www.autozone.com/tools-and-equipment/lifts",
            "name": "Lifts",
        },
        "liquid-transfer-tank-tool-box-unit": {
            "url": "https://www.autozone.com/truck-boxes-and-liquid-storage-tanks/liquid-transfer-tank-tool-box-unit",
            "name": "Liquid Transfer Tank - Tool Box Unit",
        },
        "liquid-transfer-tank-connector-kit": {
            "url": "https://www.autozone.com/tools-and-equipment/liquid-transfer-tank-connector-kit",
            "name": "Liquid Transfer Tank Connector Kit",
        },
        "trash-can-litter-container": {
            "url": "https://www.autozone.com/interior-organization-and-cargo-management/trash-can-litter-container",
            "name": "Litter Basket",
        },
        "loading-ramp": {
            "url": "https://www.autozone.com/tools-and-equipment/loading-ramp",
            "name": "Loading Ramp",
        },
        "lock-box": {
            "url": "https://www.autozone.com/tools-garage-equipment/lock-box",
            "name": "Lock Box",
        },
        "lockout-tool-set": {
            "url": "https://www.autozone.com/tools-and-equipment/lockout-tool-set",
            "name": "Lockout Tool Set",
        },
        "lopper": {
            "url": "https://www.autozone.com/tools-and-equipment/lopper",
            "name": "Lopper",
        },
        "lube-bucket": {
            "url": "https://www.autozone.com/tools-and-equipment/lube-bucket",
            "name": "Lube Bucket",
        },
        "luggage-compartment-cover-clip": {
            "url": "https://www.autozone.com/screws-pins-and-clips/luggage-compartment-cover-clip",
            "name": "Luggage Compartment Cover Clip",
        },
        "magnetic-tool-holder": {
            "url": "https://www.autozone.com/tools-boxes-storage-and-organization/magnetic-tool-holder",
            "name": "Magnetic Heater",
        },
        "magnetic-key-holder": {
            "url": "https://www.autozone.com/tools-and-equipment/magnetic-key-holder",
            "name": "Magnetic Key Holder",
        },
        "magnetic-pickup-tools-magnifying-glass": {
            "url": "https://www.autozone.com/tools-and-equipment/magnetic-pickup-tools-magnifying-glass",
            "name": "Magnetic Pickup Tools & Magnifying Glass",
        },
        "maintenance-lift": {
            "url": "https://www.autozone.com/tools-and-equipment/maintenance-lift",
            "name": "Maintenance Lift",
        },
        "marine-anchor-control": {
            "url": "https://www.autozone.com/tools-garage-equipment/marine-anchor-control",
            "name": "Marine Anchor Control",
        },
        "marine-cover": {
            "url": "https://www.autozone.com/tools-and-equipment/marine-cover",
            "name": "Marine Cover",
        },
        "marine-plumbing": {
            "url": "https://www.autozone.com/miscellaneous-non-automotive/marine-plumbing",
            "name": "Marine Drain Tube",
        },
        "marine-mirror": {
            "url": "https://www.autozone.com/miscellaneous-non-automotive/marine-mirror",
            "name": "Marine Rear View Mirror",
        },
        "marine-trim-and-tilt-fluid": {
            "url": "https://www.autozone.com/tools-and-equipment/marine-trim-and-tilt-fluid",
            "name": "Marine Trim & Tilt Fluid",
        },
        "marine-trim-level-gauge": {
            "url": "https://www.autozone.com/tools-and-equipment/marine-trim-level-gauge",
            "name": "Marine Trim Level Gauge",
        },
        "measuring-square-set": {
            "url": "https://www.autozone.com/clamps-and-measuring-tools/measuring-square-set",
            "name": "Measuring Square Set",
        },
        "measuring-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/measuring-tools",
            "name": "Measuring Tools",
        },
        "mechanics-utility-wire": {
            "url": "https://www.autozone.com/tools-and-equipment/mechanics-utility-wire",
            "name": "Mechanics Utility Wire",
        },
        "metal-seal-ring-washer-assortment": {
            "url": "https://www.autozone.com/tools-and-equipment/metal-seal-ring-washer-assortment",
            "name": "Metal Seal Ring - Washer Assortment",
        },
        "metal-shears": {
            "url": "https://www.autozone.com/tools-and-equipment/metal-shears",
            "name": "Metal Shears",
        },
        "strapping-kit": {
            "url": "https://www.autozone.com/gaskets-and-miscellaneous-fasteners/strapping-kit",
            "name": "Metal Strapping Kit",
        },
        "metal-tubing": {
            "url": "https://www.autozone.com/tools-and-equipment/metal-tubing",
            "name": "Metal Tubing",
        },
        "molding-release-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/molding-release-tools",
            "name": "Molding Release Tools",
        },
        "multi-function-air-compressor-pressure-switch": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-function-air-compressor-pressure-switch",
            "name": "Multi-Function Air Compressor Pressure Switch",
        },
        "multi-purpose-band-clamp": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-band-clamp",
            "name": "Multi-Purpose Band Clamp",
        },
        "multi-purpose-can-storage-tray": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-can-storage-tray",
            "name": "Multi-Purpose Can Storage Tray",
        },
        "safety-chain": {
            "url": "https://www.autozone.com/trailer-hitch-hitch-balls-and-towing-accessories/safety-chain",
            "name": "Multi-Purpose Chain",
        },
        "multi-purpose-check-valve": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-check-valve",
            "name": "Multi-Purpose Check Valve",
        },
        "multi-purpose-clamp": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-clamp",
            "name": "Multi-Purpose Clamp",
        },
        "multi-purpose-cover": {
            "url": "https://www.autozone.com/miscellaneous-non-automotive/multi-purpose-cover",
            "name": "Multi-Purpose Cover",
        },
        "multi-purpose-fluid-transfer-pump": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-fluid-transfer-pump",
            "name": "Multi-Purpose Fluid Transfer Pump",
        },
        "multi-purpose-hardware": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-hardware",
            "name": "Multi-Purpose Hardware",
        },
        "multi-purpose-lock": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-lock",
            "name": "Multi-Purpose Lock",
        },
        "multi-purpose-magnet": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-magnet",
            "name": "Multi-Purpose Magnet",
        },
        "multi-purpose-material-spreader": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-material-spreader",
            "name": "Multi-Purpose Material Spreader",
        },
        "vernier-caliper": {
            "url": "https://www.autozone.com/clamps-and-measuring-tools/vernier-caliper",
            "name": "Multi-Purpose Measuring Caliper",
        },
        "multi-purpose-micrometer": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-micrometer",
            "name": "Multi-Purpose Micrometer",
        },
        "multi-purpose-mirror": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/multi-purpose-mirror",
            "name": "Multi-Purpose Mirror",
        },
        "multi-purpose-pin": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-pin",
            "name": "Multi-Purpose Pin",
        },
        "multi-purpose-pressure-gauge": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-pressure-gauge",
            "name": "Multi-Purpose Pressure Gauge",
        },
        "multi-purpose-repair-sleeve": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-repair-sleeve",
            "name": "Multi-Purpose Repair Sleeve",
        },
        "multi-purpose-shackle": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-shackle",
            "name": "Multi-Purpose Shackle",
        },
        "multi-purpose-shelf": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-shelf",
            "name": "Multi-Purpose Shelf",
        },
        "multi-purpose-spill-kit": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-spill-kit",
            "name": "Multi-Purpose Spill Kit",
        },
        "multi-purpose-spout": {
            "url": "https://www.autozone.com/tools-garage-equipment/multi-purpose-spout",
            "name": "Multi-Purpose Spout",
        },
        "multi-purpose-spring-assortment": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-spring-assortment",
            "name": "Multi-Purpose Spring Assortment",
        },
        "multi-purpose-storage-case": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-storage-case",
            "name": "Multi-Purpose Storage Case",
        },
        "multi-purpose-threaded-plug": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-threaded-plug",
            "name": "Multi-Purpose Threaded Plug",
        },
        "multi-purpose-tool-storage-case": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-tool-storage-case",
            "name": "Multi-Purpose Tool Storage Case",
        },
        "multi-purpose-transfer-pump": {
            "url": "https://www.autozone.com/tools-and-equipment/multi-purpose-transfer-pump",
            "name": "Multi-Purpose Transfer Pump",
        },
        "oil-absorbent": {
            "url": "https://www.autozone.com/tools-and-equipment/oil-absorbent",
            "name": "Oil Absorbent",
        },
        "oil-catch-can": {
            "url": "https://www.autozone.com/tools-and-equipment/oil-catch-can",
            "name": "Oil Catch Can",
        },
        "oil-change-service": {
            "url": "https://www.autozone.com/tools-and-equipment/oil-change-service",
            "name": "Oil Change & Service",
        },
        "engine-oil-drain-hose": {
            "url": "https://www.autozone.com/external-engine/engine-oil-drain-hose",
            "name": "Oil Drain Hose",
        },
        "fluid-pump": {
            "url": "https://www.autozone.com/test-scan-and-specialty-tools/fluid-pump",
            "name": "Oil Drain Pump",
        },
        "engine-oil-extraction-pump": {
            "url": "https://www.autozone.com/tools-and-equipment/engine-oil-extraction-pump",
            "name": "Oil Extraction Pump",
        },
        "oil-filter-wrenches": {
            "url": "https://www.autozone.com/tools-and-equipment/oil-filter-wrenches",
            "name": "Oil Filter Wrenches",
        },
        "engine-oil-level-information-label": {
            "url": "https://www.autozone.com/tools-and-equipment/engine-oil-level-information-label",
            "name": "Oil Level Information Label",
        },
        "owners-manual": {
            "url": "https://www.autozone.com/tools-and-equipment/owners-manual",
            "name": "Owners Manual",
        },
        "package-tray-retainer": {
            "url": "https://www.autozone.com/collision-body-parts-and-hardware/package-tray-retainer",
            "name": "Package Tray Retainer",
        },
        "package-tray-trim-clip": {
            "url": "https://www.autozone.com/tools-and-equipment/package-tray-trim-clip",
            "name": "Package Tray Trim Clip",
        },
        "padlock": {
            "url": "https://www.autozone.com/tools-and-equipment/padlock",
            "name": "Padlock",
        },
        "pain-and-fever-relief-medicine": {
            "url": "https://www.autozone.com/tools-and-equipment/pain-and-fever-relief-medicine",
            "name": "Pain & Fever Relief Medicine",
        },
        "paper-towels": {
            "url": "https://www.autozone.com/tools-and-equipment/paper-towels",
            "name": "Paper Towels",
        },
        "parts-bag": {
            "url": "https://www.autozone.com/tools-and-equipment/parts-bag",
            "name": "Parts Bag",
        },
        "parts-cleaning": {
            "url": "https://www.autozone.com/tools-and-equipment/parts-cleaning",
            "name": "Parts Cleaning",
        },
        "parts-trays": {
            "url": "https://www.autozone.com/tools-and-equipment/parts-trays",
            "name": "Parts Trays",
        },
        "permanent-marker": {
            "url": "https://www.autozone.com/miscellaneous-non-automotive/permanent-marker",
            "name": "Permanent Marker",
        },
        "pinch-bolt": {
            "url": "https://www.autozone.com/tools-and-equipment/pinch-bolt",
            "name": "Pinch Bolt",
        },
        "pintle-hook-mounting-plate": {
            "url": "https://www.autozone.com/tools-and-equipment/pintle-hook-mounting-plate",
            "name": "Pintle Hook Mounting Plate",
        },
        "pipe-plug-removal-tool": {
            "url": "https://www.autozone.com/tools-and-equipment/pipe-plug-removal-tool",
            "name": "Pipe Plug Removal Tool",
        },
        "pipe-plugs-pipe-fittings": {
            "url": "https://www.autozone.com/tools-and-equipment/pipe-plugs-pipe-fittings",
            "name": "Pipe Plugs & Pipe Fittings",
        },
        "pipe-to-compression-fitting": {
            "url": "https://www.autozone.com/tools-and-equipment/pipe-to-compression-fitting",
            "name": "Pipe to Compression Fitting",
        },
        "pliers": {
            "url": "https://www.autozone.com/tools-and-equipment/pliers",
            "name": "Pliers",
        },
        "universal-plug-button-assortment": {
            "url": "https://www.autozone.com/gaskets-and-miscellaneous-fasteners/universal-plug-button-assortment",
            "name": "Plug Button",
        },
        "point-of-purchase-display": {
            "url": "https://www.autozone.com/tools-and-equipment/point-of-purchase-display",
            "name": "Point of Purchase Display",
        },
        "portable-generator": {
            "url": "https://www.autozone.com/shop-and-garage-tools/portable-generator",
            "name": "Portable Generator",
        },
        "portable-generator-parallel-kit": {
            "url": "https://www.autozone.com/tools-garage-equipment/portable-generator-parallel-kit",
            "name": "Portable Generator Parallel Kit",
        },
        "portable-power-station": {
            "url": "https://www.autozone.com/tools-garage-equipment/portable-power-station",
            "name": "Portable Power Station",
        },
        "portable-spotlight": {
            "url": "https://www.autozone.com/tools-and-equipment/portable-spotlight",
            "name": "Portable Spotlight",
        },
        "position-light": {
            "url": "https://www.autozone.com/tools-and-equipment/position-light",
            "name": "Position Light",
        },
        "power-cord-plug": {
            "url": "https://www.autozone.com/tools-and-equipment/power-cord-plug",
            "name": "Power Cord Plug",
        },
        "power-drive-adapter-set": {
            "url": "https://www.autozone.com/tools-and-equipment/power-drive-adapter-set",
            "name": "Power Drive Adapter Set",
        },
        "power-flap-wheel": {
            "url": "https://www.autozone.com/tools-and-equipment/power-flap-wheel",
            "name": "Power Flap Wheel",
        },
        "power-outlet-adapter": {
            "url": "https://www.autozone.com/tools-and-equipment/power-outlet-adapter",
            "name": "Power Outlet Adapter",
        },
        "power-outlet-strip": {
            "url": "https://www.autozone.com/tools-garage-equipment/power-outlet-strip",
            "name": "Power Outlet Strip",
        },
        "power-supply-cord": {
            "url": "https://www.autozone.com/tools-and-equipment/power-supply-cord",
            "name": "Power Supply Cord",
        },
        "power-tool-battery-pack": {
            "url": "https://www.autozone.com/tools-garage-equipment/power-tool-battery-pack",
            "name": "Power Tool Battery Pack",
        },
        "power-tool-charger": {
            "url": "https://www.autozone.com/tools-and-equipment/power-tool-charger",
            "name": "Power Tool Charger",
        },
        "pressure-washer": {
            "url": "https://www.autozone.com/tools-garage-equipment/pressure-washer",
            "name": "Pressure Washer",
        },
        "pressure-washer-connector": {
            "url": "https://www.autozone.com/tools-garage-equipment/pressure-washer-connector",
            "name": "Pressure Washer Connector",
        },
        "pressure-washer-spray-nozzle": {
            "url": "https://www.autozone.com/tools-garage-equipment/pressure-washer-spray-nozzle",
            "name": "Pressure Washer Spray Nozzle",
        },
        "primary-drive-gasket": {
            "url": "https://www.autozone.com/external-engine/primary-drive-gasket",
            "name": "Primary Drive Gasket",
        },
        "primers": {
            "url": "https://www.autozone.com/tools-and-equipment/primers",
            "name": "Primers",
        },
        "printer-plotter": {
            "url": "https://www.autozone.com/tools-and-equipment/printer-plotter",
            "name": "Printer - Plotter",
        },
        "printer-label": {
            "url": "https://www.autozone.com/tools-and-equipment/printer-label",
            "name": "Printer Label",
        },
        "printer-paper": {
            "url": "https://www.autozone.com/tools-and-equipment/printer-paper",
            "name": "Printer Paper",
        },
        "probe-thermometer": {
            "url": "https://www.autozone.com/tools-and-equipment/probe-thermometer",
            "name": "Probe Thermometer",
        },
        "product-identification-label": {
            "url": "https://www.autozone.com/tools-and-equipment/product-identification-label",
            "name": "Product Identification Label",
        },
        "propeller-lock": {
            "url": "https://www.autozone.com/tools-and-equipment/propeller-lock",
            "name": "Propeller Lock",
        },
        "pry-bars": {
            "url": "https://www.autozone.com/tools-and-equipment/pry-bars",
            "name": "Pry Bars",
        },
        "pull-claw": {
            "url": "https://www.autozone.com/tools-and-equipment/pull-claw",
            "name": "Pull Claw",
        },
        "pullers-presses-separators": {
            "url": "https://www.autozone.com/tools-and-equipment/pullers-presses-separators",
            "name": "Pullers, Presses & Separators",
        },
        "pump-sprayer": {
            "url": "https://www.autozone.com/tools-and-equipment/pump-sprayer",
            "name": "Pump Sprayer",
        },
        "punches": {
            "url": "https://www.autozone.com/tools-and-equipment/punches",
            "name": "Punches",
        },
        "push-nuts": {
            "url": "https://www.autozone.com/tools-and-equipment/push-nuts",
            "name": "Push Nuts",
        },
        "pyrometer": {
            "url": "https://www.autozone.com/tools-and-equipment/pyrometer",
            "name": "Pyrometer",
        },
        "pyrometer-kit": {
            "url": "https://www.autozone.com/exhaust/pyrometer-kit",
            "name": "Pyrometer Kit",
        },
        "pyrometer-module": {
            "url": "https://www.autozone.com/tools-and-equipment/pyrometer-module",
            "name": "Pyrometer Module",
        },
        "pyrometer-sensor": {
            "url": "https://www.autozone.com/tools-and-equipment/pyrometer-sensor",
            "name": "Pyrometer Sensor",
        },
        "quick-disconnect-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/quick-disconnect-tools",
            "name": "Quick Disconnect Tools",
        },
        "ramp-lip-kit": {
            "url": "https://www.autozone.com/tools-and-equipment/ramp-lip-kit",
            "name": "Ramp Lip Kit",
        },
        "recovery-rope": {
            "url": "https://www.autozone.com/tools-and-equipment/recovery-rope",
            "name": "Recovery Rope",
        },
        "refrigerator-power-cord": {
            "url": "https://www.autozone.com/tools-and-equipment/refrigerator-power-cord",
            "name": "Refrigerator Power Cord",
        },
        "refrigerator-wiring-kit": {
            "url": "https://www.autozone.com/tools-and-equipment/refrigerator-wiring-kit",
            "name": "Refrigerator Wiring Kit",
        },
        "repair-manuals-software": {
            "url": "https://www.autozone.com/tools-and-equipment/repair-manuals-software",
            "name": "Repair Manuals & Software",
        },
        "rivets-accessories": {
            "url": "https://www.autozone.com/tools-and-equipment/rivets-accessories",
            "name": "Rivets & Accessories",
        },
        "rope-hoist": {
            "url": "https://www.autozone.com/tools-and-equipment/rope-hoist",
            "name": "Rope Hoist",
        },
        "rotary-tool-bit": {
            "url": "https://www.autozone.com/tools-and-equipment/rotary-tool-bit",
            "name": "Rotary Tool Bit",
        },
        "rotary-tools-grinders": {
            "url": "https://www.autozone.com/tools-and-equipment/rotary-tools-grinders",
            "name": "Rotary Tools",
        },
        "ruler": {
            "url": "https://www.autozone.com/tools-and-equipment/ruler",
            "name": "Ruler",
        },
        "safety-equipment-ear-face-protection": {
            "url": "https://www.autozone.com/tools-and-equipment/safety-equipment-ear-face-protection",
            "name": "Safety Equipment, Ear & Face Protection",
        },
        "safety-tool-clamp": {
            "url": "https://www.autozone.com/tools-and-equipment/safety-tool-clamp",
            "name": "Safety Tool Clamp",
        },
        "marine-whistle": {
            "url": "https://www.autozone.com/miscellaneous-non-automotive/marine-whistle",
            "name": "Safety Whistle",
        },
        "saws-saw-blades": {
            "url": "https://www.autozone.com/tools-and-equipment/saws-saw-blades",
            "name": "Saws & Saw Blades",
        },
        "float-weight-scale": {
            "url": "https://www.autozone.com/clamps-and-measuring-tools/float-weight-scale",
            "name": "Scale",
        },
        "scan-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/scan-tools",
            "name": "Scan Tools",
        },
        "screw-pin-shackle": {
            "url": "https://www.autozone.com/tools-and-equipment/screw-pin-shackle",
            "name": "Screw Pin Shackle",
        },
        "screwdrivers-nutdrivers": {
            "url": "https://www.autozone.com/tools-and-equipment/screwdrivers-nutdrivers",
            "name": "Screwdrivers & Nutdrivers",
        },
        "screws": {
            "url": "https://www.autozone.com/tools-and-equipment/screws",
            "name": "Screws",
        },
        "seal-ring-washer": {
            "url": "https://www.autozone.com/tools-and-equipment/seal-ring-washer",
            "name": "Seal Ring - Washer",
        },
        "seam-sealer": {
            "url": "https://www.autozone.com/tools-and-equipment/seam-sealer",
            "name": "Seam Sealer",
        },
        "shaft-repair-sleeve": {
            "url": "https://www.autozone.com/tools-and-equipment/shaft-repair-sleeve",
            "name": "Shaft Repair Sleeve",
        },
        "sheet-metal-bead-roller": {
            "url": "https://www.autozone.com/tools-and-equipment/sheet-metal-bead-roller",
            "name": "Sheet Metal Bead Roller",
        },
        "shoe-cover": {
            "url": "https://www.autozone.com/tools-and-equipment/shoe-cover",
            "name": "Shoe Cover",
        },
        "shop-presses-equipment": {
            "url": "https://www.autozone.com/tools-and-equipment/shop-presses-equipment",
            "name": "Shop Presses & Equipment",
        },
        "snatch-block": {
            "url": "https://www.autozone.com/tools-and-equipment/snatch-block",
            "name": "Snatch Block",
        },
        "snow-plow-blade": {
            "url": "https://www.autozone.com/tools-and-equipment/snow-plow-blade",
            "name": "Snow Plow Blade",
        },
        "snow-plow-bracket": {
            "url": "https://www.autozone.com/tools-and-equipment/snow-plow-bracket",
            "name": "Snow Plow Bracket",
        },
        "snow-plow-cable-assembly": {
            "url": "https://www.autozone.com/tools-and-equipment/snow-plow-cable-assembly",
            "name": "Snow Plow Cable Assembly",
        },
        "snow-plow-cutting-edge": {
            "url": "https://www.autozone.com/tools-and-equipment/snow-plow-cutting-edge",
            "name": "Snow Plow Cutting Edge",
        },
        "snow-plow-frame": {
            "url": "https://www.autozone.com/tools-and-equipment/snow-plow-frame",
            "name": "Snow Plow Frame",
        },
        "snow-plow-hardware": {
            "url": "https://www.autozone.com/miscellaneous-non-automotive/snow-plow-hardware",
            "name": "Snow Plow Hardware",
        },
        "snow-plow-hinge-pin": {
            "url": "https://www.autozone.com/tools-and-equipment/snow-plow-hinge-pin",
            "name": "Snow Plow Hinge Pin",
        },
        "snow-plow-hydraulic-lift-cylinder": {
            "url": "https://www.autozone.com/tools-and-equipment/snow-plow-hydraulic-lift-cylinder",
            "name": "Snow Plow Hydraulic Lift Cylinder",
        },
        "snow-plow-light": {
            "url": "https://www.autozone.com/tools-and-equipment/snow-plow-light",
            "name": "Snow Plow Light",
        },
        "snow-plow-shoe-assembly": {
            "url": "https://www.autozone.com/tools-and-equipment/snow-plow-shoe-assembly",
            "name": "Snow Plow Shoe Assembly",
        },
        "software-license": {
            "url": "https://www.autozone.com/tools-and-equipment/software-license",
            "name": "Software License",
        },
        "solar-panel": {
            "url": "https://www.autozone.com/tools-and-equipment/solar-panel",
            "name": "Solar Panel",
        },
        "specialty-clamps": {
            "url": "https://www.autozone.com/tools-and-equipment/specialty-clamps",
            "name": "Specialty Clamps",
        },
        "specialty-sockets-wrenches": {
            "url": "https://www.autozone.com/tools-and-equipment/specialty-sockets-wrenches",
            "name": "Specialty Sockets & Wrenches",
        },
        "spray-bottle-nozzle": {
            "url": "https://www.autozone.com/tools-and-equipment/spray-bottle-nozzle",
            "name": "Spray Bottle Nozzle",
        },
        "spray-gun-cup": {
            "url": "https://www.autozone.com/tools-and-equipment/spray-gun-cup",
            "name": "Spray Gun Cup",
        },
        "spray-gun-cup-lid": {
            "url": "https://www.autozone.com/tools-and-equipment/spray-gun-cup-lid",
            "name": "Spray Gun Cup Lid",
        },
        "spray-gun-nozzle": {
            "url": "https://www.autozone.com/tools-and-equipment/spray-gun-nozzle",
            "name": "Spray Gun Nozzle",
        },
        "spray-gun-nozzle-tip": {
            "url": "https://www.autozone.com/tools-and-equipment/spray-gun-nozzle-tip",
            "name": "Spray Gun Nozzle Tip",
        },
        "spray-gun-repair-kit": {
            "url": "https://www.autozone.com/tools-and-equipment/spray-gun-repair-kit",
            "name": "Spray Gun Repair Kit",
        },
        "spray-paint-can-trigger": {
            "url": "https://www.autozone.com/tools-and-equipment/spray-paint-can-trigger",
            "name": "Spray Paint Can Trigger",
        },
        "spring-washer": {
            "url": "https://www.autozone.com/tools-and-equipment/spring-washer",
            "name": "Spring Washer",
        },
        "stainless-steel-hardware-assortment": {
            "url": "https://www.autozone.com/tools-and-equipment/stainless-steel-hardware-assortment",
            "name": "Stainless Steel Hardware Assortment",
        },
        "steering-suspension-service-repair": {
            "url": "https://www.autozone.com/tools-and-equipment/steering-suspension-service-repair",
            "name": "Steering & Suspension Service & Repair",
        },
        "steering-wheel-air-bag-service": {
            "url": "https://www.autozone.com/tools-and-equipment/steering-wheel-air-bag-service",
            "name": "Steering Wheel & Air Bag Service",
        },
        "storage-container": {
            "url": "https://www.autozone.com/tools-and-equipment/storage-container",
            "name": "Storage Container",
        },
        "storage-drum-pump": {
            "url": "https://www.autozone.com/tools-and-equipment/storage-drum-pump",
            "name": "Storage Drum Pump",
        },
        "storage-pouch": {
            "url": "https://www.autozone.com/tools-and-equipment/storage-pouch",
            "name": "Storage Pouch",
        },
        "suction-gun": {
            "url": "https://www.autozone.com/tools-and-equipment/suction-gun",
            "name": "Suction Gun",
        },
        "swab": {
            "url": "https://www.autozone.com/tools-and-equipment/swab",
            "name": "Swab",
        },
        "swivel-eye-hasp": {
            "url": "https://www.autozone.com/tools-and-equipment/swivel-eye-hasp",
            "name": "Swivel Eye Hasp",
        },
        "tacky-mat": {
            "url": "https://www.autozone.com/tools-and-equipment/tacky-mat",
            "name": "Tacky Mat",
        },
        "taps-dies-extractors-thread-repair": {
            "url": "https://www.autozone.com/tools-and-equipment/taps-dies-extractors-thread-repair",
            "name": "Taps, Dies, Extractors & Thread Repair",
        },
        "thermal-protection-hose-wrap": {
            "url": "https://www.autozone.com/tools-and-equipment/thermal-protection-hose-wrap",
            "name": "Thermal Protection Hose Wrap",
        },
        "thermal-protection-mat": {
            "url": "https://www.autozone.com/tools-and-equipment/thermal-protection-mat",
            "name": "Thermal Protection Mat",
        },
        "thermal-protection-tubing": {
            "url": "https://www.autozone.com/tools-and-equipment/thermal-protection-tubing",
            "name": "Thermal Protection Tubing",
        },
        "thermometers": {
            "url": "https://www.autozone.com/tools-and-equipment/thermometers",
            "name": "Thermometers",
        },
        "thru-hull-connector": {
            "url": "https://www.autozone.com/tools-and-equipment/thru-hull-connector",
            "name": "Thru-Hull Connector",
        },
        "tire-balancing-wheel-alignment": {
            "url": "https://www.autozone.com/tools-and-equipment/tire-balancing-wheel-alignment",
            "name": "Tire Balancing & Wheel Alignment",
        },
        "tire-change-wheel-lug-stud-repair": {
            "url": "https://www.autozone.com/tire-repair-and-tire-wheel/tire-change-wheel-lug-stud-repair",
            "name": "Tire Change & Repair, Wheel Lug & Stud Repair",
        },
        "tire-inflators-tire-gauges": {
            "url": "https://www.autozone.com/tools-and-equipment/tire-inflators-tire-gauges",
            "name": "Tire Inflators & Tire Gauges",
        },
        "tool-board": {
            "url": "https://www.autozone.com/tools-garage-equipment/tool-board",
            "name": "Tool Board",
        },
        "tool-sets-tool-accessories": {
            "url": "https://www.autozone.com/tools-and-equipment/tool-sets-tool-accessories",
            "name": "Tool Sets & Tool Accessories",
        },
        "torque-wrenches": {
            "url": "https://www.autozone.com/tools-and-equipment/torque-wrenches",
            "name": "Torque Wrenches",
        },
        "touch-up-bottle": {
            "url": "https://www.autozone.com/tools-and-equipment/touch-up-bottle",
            "name": "Touch-Up Bottle",
        },
        "track-hook": {
            "url": "https://www.autozone.com/tools-and-equipment/track-hook",
            "name": "Track Hook",
        },
        "transfer-utility-pump": {
            "url": "https://www.autozone.com/tools-and-equipment/transfer-utility-pump",
            "name": "Transfer Utility Pump",
        },
        "transfer-utility-pump-hose": {
            "url": "https://www.autozone.com/tools-garage-equipment/transfer-utility-pump-hose",
            "name": "Transfer Utility Pump Hose",
        },
        "transmission-repair-and-service": {
            "url": "https://www.autozone.com/tools-and-equipment/transmission-repair-and-service",
            "name": "Transmission Repair & Service",
        },
        "transom-seal-kit": {
            "url": "https://www.autozone.com/tools-and-equipment/transom-seal-kit",
            "name": "Transom Seal Kit",
        },
        "tube-bending-flaring": {
            "url": "https://www.autozone.com/tools-and-equipment/tube-bending-flaring",
            "name": "Tube Bending & Flaring",
        },
        "tweezers": {
            "url": "https://www.autozone.com/tools-and-equipment/tweezers",
            "name": "Tweezers",
        },
        "u-joints-center-supports-and-driveshafts": {
            "url": "https://www.autozone.com/tools-and-equipment/u-joints-center-supports-and-driveshafts",
            "name": "U-Joints, Center Supports & Driveshafts",
        },
        "vacuum-cleaners": {
            "url": "https://www.autozone.com/tools-and-equipment/vacuum-cleaners",
            "name": "Vacuum Cleaners",
        },
        "vacuum-hose-connectors": {
            "url": "https://www.autozone.com/tools-and-equipment/vacuum-hose-connectors",
            "name": "Vacuum Hose & Connectors",
        },
        "vehicle-lifts-dollys": {
            "url": "https://www.autozone.com/tools-and-equipment/vehicle-lifts-dollys",
            "name": "Vehicle Lifts & Dollys",
        },
        "vehicle-scales": {
            "url": "https://www.autozone.com/tools-and-equipment/vehicle-scales",
            "name": "Vehicle Scale",
        },
        "vises": {
            "url": "https://www.autozone.com/tools-and-equipment/vises",
            "name": "Vises",
        },
        "welding-and-torches": {
            "url": "https://www.autozone.com/tools-and-equipment/welding-and-torches",
            "name": "Welding & Torches",
        },
        "window-handle-removal-": {
            "url": "https://www.autozone.com/tools-and-equipment/window-handle-removal-",
            "name": "Window Handle Removal",
        },
        "wiper-arm-removal-tools": {
            "url": "https://www.autozone.com/tools-and-equipment/wiper-arm-removal-tools",
            "name": "Wiper Arm Removal Tools",
        },
        "wrenches-wrench-sets": {
            "url": "https://www.autozone.com/tools-and-equipment/wrenches-wrench-sets",
            "name": "Wrenches & Wrench Sets",
        },
    },
}

