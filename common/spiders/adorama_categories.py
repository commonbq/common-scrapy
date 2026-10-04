from __future__ import annotations

import re

"""Adorama category inventory.

Adorama publishes its live taxonomy as an XML sitemap:

    GET https://www.adorama.com/UnifySiteMaps/Category.xml

That sitemap was normalized into ``ADORAMA_CATEGORY_INVENTORY`` below: 11
top-level departments and 1,090 ``/l/`` URLs (depths 1-5).

Two page kinds live under ``/l/``:

* **Depth-1 department landings** (``/l/Photography``, ``/l/Audio``) render
  ``pageInfo.pageType == "bcmsSitePage"``. They are CMS landing content with no
  product grid, so they are *not* crawlable listings and are excluded from
  ``ADORAMA_CATEGORIES``.
* **Depth-2+ category pages** (``/l/Photography/Cameras``) render
  ``pageInfo.pageType == "listPage"`` with 24 SSR products per page. These are
  the 1,079 crawlable URLs exposed by ``ADORAMA_CATEGORIES``.

To refresh the inventory, re-derive the nested dictionary from
``/UnifySiteMaps/Category.xml`` and keep this schema: department label ->
``{"url": ..., "subcategories": {label: node}}``.
"""

ADORAMA_BASE_URL = "https://www.adorama.com"

ADORAMA_CATEGORY_INVENTORY = {
    'Audio': {"url": '/l/Audio', "subcategories": {
        'Audio-Bags-and-Cases': {"url": '/l/Audio/Audio-Bags-and-Cases', "subcategories": {
            'Audio-Organizer-Bags': {"url": '/l/Audio/Audio-Bags-and-Cases/Audio-Organizer-Bags'},
            'DJ-Equipment-Cases': {"url": '/l/Audio/Audio-Bags-and-Cases/DJ-Equipment-Cases'},
            'Microphone-Cases': {"url": '/l/Audio/Audio-Bags-and-Cases/Microphone-Cases'},
            'Mixer-Cases': {"url": '/l/Audio/Audio-Bags-and-Cases/Mixer-Cases'},
            'PA-System-Cases': {"url": '/l/Audio/Audio-Bags-and-Cases/PA-System-Cases'},
            'Stand-Bags-and-Cases': {"url": '/l/Audio/Audio-Bags-and-Cases/Stand-Bags-and-Cases'}
        }},
        'Audio-Visual-Presentation': {"url": '/l/Audio/Audio-Visual-Presentation', "subcategories": {
            'AV-Projector-Screens': {"url": '/l/Audio/Audio-Visual-Presentation/AV-Projector-Screens'},
            'Audio-Solutions': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Solutions', "subcategories": {
                'Assistive-Listening': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Solutions/Assistive-Listening'},
                'Audio-Conferencing-Systems': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Solutions/Audio-Conferencing-Systems'},
                'Commercial-Speakers': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Solutions/Commercial-Speakers'},
                'Commercial-Subwoofers': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Solutions/Commercial-Subwoofers'},
                'Horn-Loudspeakers': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Solutions/Horn-Loudspeakers'},
                'Lecterns-and-Podiums': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Solutions/Lecterns-and-Podiums'}
            }},
            'Audio-Visual-Presentation-Accessories': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories', "subcategories": {
                'Audio-Conferencing-Accessories': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories/Audio-Conferencing-Accessories'},
                'Audio-Snakes-and-Stage-Boxes': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories/Audio-Snakes-and-Stage-Boxes'},
                'Commercial-Display-Accessories': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories/Commercial-Display-Accessories'},
                'Display-Adapters': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories/Display-Adapters'},
                'Display-Mounts-and-Stands': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories/Display-Mounts-and-Stands'},
                'Display-Splitters': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories/Display-Splitters'},
                'DisplayPort-Cables': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories/DisplayPort-Cables'},
                'Panel-Jacks-and-Adapters': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories/Panel-Jacks-and-Adapters'},
                'Projector-Lamps': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories/Projector-Lamps'},
                'Projector-Mounts': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories/Projector-Mounts'},
                'VGA-Cables': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories/VGA-Cables'},
                'Wireless-Presenters': {"url": '/l/Audio/Audio-Visual-Presentation/Audio-Visual-Presentation-Accessories/Wireless-Presenters'}
            }},
            'Production-Carts': {"url": '/l/Audio/Audio-Visual-Presentation/Production-Carts'},
            'Projection-and-Display': {"url": '/l/Audio/Audio-Visual-Presentation/Projection-and-Display', "subcategories": {
                'Business-Professional-Projectors': {"url": '/l/Audio/Audio-Visual-Presentation/Projection-and-Display/Business-Professional-Projectors'},
                'Commercial-Monitors-and-Displays': {"url": '/l/Audio/Audio-Visual-Presentation/Projection-and-Display/Commercial-Monitors-and-Displays'},
                'Overheads-and-Visualizers': {"url": '/l/Audio/Audio-Visual-Presentation/Projection-and-Display/Overheads-and-Visualizers'},
                'Portable-Projectors': {"url": '/l/Audio/Audio-Visual-Presentation/Projection-and-Display/Portable-Projectors'},
                'Video-Conferencing': {"url": '/l/Audio/Audio-Visual-Presentation/Projection-and-Display/Video-Conferencing'},
                'Whiteboards-comma-Easels-and-Displays': {"url": '/l/Audio/Audio-Visual-Presentation/Projection-and-Display/Whiteboards-comma-Easels-and-Displays'}
            }}
        }},
        'Audio-for-Video': {"url": '/l/Audio/Audio-for-Video', "subcategories": {
            'Audio-Recorders': {"url": '/l/Audio/Audio-for-Video/Audio-Recorders', "subcategories": {
                'Digital-Field-Recorders': {"url": '/l/Audio/Audio-for-Video/Audio-Recorders/Digital-Field-Recorders'},
                'Recorder-Accessories': {"url": '/l/Audio/Audio-for-Video/Audio-Recorders/Recorder-Accessories'}
            }},
            'Audio-Visual-Accessories': {"url": '/l/Audio/Audio-for-Video/Audio-Visual-Accessories'},
            'Lavalier-Microphones': {"url": '/l/Audio/Audio-for-Video/Lavalier-Microphones'}
        }},
        'Bluetooth-and-Wireless-Speakers': {"url": '/l/Audio/Bluetooth-and-Wireless-Speakers'},
        'Cables-and-Adapters': {"url": '/l/Audio/Cables-and-Adapters', "subcategories": {
            'Audio-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables', "subcategories": {
                'Bantam-lrbr-TT-rrbr-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables/Bantam-lrbr-TT-rrbr-Cables'},
                'Mini-to-Mini-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables/Mini-to-Mini-Cables'},
                'Mini-to-Phone-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables/Mini-to-Phone-Cables'},
                'Phone-to-RCA-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables/Phone-to-RCA-Cables'},
                'Phono-to-Phono-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables/Phono-to-Phono-Cables'},
                'Phono-to-XLR-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables/Phono-to-XLR-Cables'},
                'RCA-to-RCA-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables/RCA-to-RCA-Cables'},
                'RCA-to-XLR-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables/RCA-to-XLR-Cables'},
                'Speaker-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables/Speaker-Cables'},
                'Stereo-Phone-to-Stereo-Phone-lrbr-TRS-rrbr-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables/Stereo-Phone-to-Stereo-Phone-lrbr-TRS-rrbr-Cables'},
                'TRS-to-XLR-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables/TRS-to-XLR-Cables'},
                'Y-and-Insert-Cables': {"url": '/l/Audio/Cables-and-Adapters/Audio-Cables/Y-and-Insert-Cables'}
            }},
            'Digital-and-Data-Cables': {"url": '/l/Audio/Cables-and-Adapters/Digital-and-Data-Cables', "subcategories": {
                'AES-and-EBU-Cables': {"url": '/l/Audio/Cables-and-Adapters/Digital-and-Data-Cables/AES-and-EBU-Cables'},
                'Coaxial-Cables': {"url": '/l/Audio/Cables-and-Adapters/Digital-and-Data-Cables/Coaxial-Cables'},
                'MIDI-Cables': {"url": '/l/Audio/Cables-and-Adapters/Digital-and-Data-Cables/MIDI-Cables'},
                'Optical-lrbr-Toslink-rrbr-Cables': {"url": '/l/Audio/Cables-and-Adapters/Digital-and-Data-Cables/Optical-lrbr-Toslink-rrbr-Cables'}
            }},
            'In-hyphen-Line-Solutions': {"url": '/l/Audio/Cables-and-Adapters/In-hyphen-Line-Solutions', "subcategories": {
                'Couplers-and-Combiners': {"url": '/l/Audio/Cables-and-Adapters/In-hyphen-Line-Solutions/Couplers-and-Combiners'},
                'Pads': {"url": '/l/Audio/Cables-and-Adapters/In-hyphen-Line-Solutions/Pads'},
                'Splitters': {"url": '/l/Audio/Cables-and-Adapters/In-hyphen-Line-Solutions/Splitters'},
                'Transformers': {"url": '/l/Audio/Cables-and-Adapters/In-hyphen-Line-Solutions/Transformers'}
            }},
            'Snakes-and-Adapters': {"url": '/l/Audio/Cables-and-Adapters/Snakes-and-Adapters', "subcategories": {
                'Audio-Connectors': {"url": '/l/Audio/Cables-and-Adapters/Snakes-and-Adapters/Audio-Connectors'},
                'Bulk-Audio-Cable': {"url": '/l/Audio/Cables-and-Adapters/Snakes-and-Adapters/Bulk-Audio-Cable'}
            }}
        }},
        'DJ-Equipment': {"url": '/l/Audio/DJ-Equipment', "subcategories": {
            'DJ-Controllers': {"url": '/l/Audio/DJ-Equipment/DJ-Controllers'},
            'DJ-Equipment-Cases': {"url": '/l/Audio/DJ-Equipment/DJ-Equipment-Cases'},
            'DJ-Headphones': {"url": '/l/Audio/DJ-Equipment/DJ-Headphones'},
            'DJ-Lighting-and-Effects': {"url": '/l/Audio/DJ-Equipment/DJ-Lighting-and-Effects', "subcategories": {
                'Color-and-Wash-Lights': {"url": '/l/Audio/DJ-Equipment/DJ-Lighting-and-Effects/Color-and-Wash-Lights'},
                'DJ-and-Effect-Lights': {"url": '/l/Audio/DJ-Equipment/DJ-Lighting-and-Effects/DJ-and-Effect-Lights'},
                'Fog-and-Bubble-Machines': {"url": '/l/Audio/DJ-Equipment/DJ-Lighting-and-Effects/Fog-and-Bubble-Machines'},
                'Lighting-Cables-and-Accessories': {"url": '/l/Audio/DJ-Equipment/DJ-Lighting-and-Effects/Lighting-Cables-and-Accessories'},
                'Lighting-Controllers-and-Interfaces': {"url": '/l/Audio/DJ-Equipment/DJ-Lighting-and-Effects/Lighting-Controllers-and-Interfaces'},
                'Par-Cans': {"url": '/l/Audio/DJ-Equipment/DJ-Lighting-and-Effects/Par-Cans'},
                'Spotlights': {"url": '/l/Audio/DJ-Equipment/DJ-Lighting-and-Effects/Spotlights'}
            }},
            'DJ-Mixers': {"url": '/l/Audio/DJ-Equipment/DJ-Mixers'},
            'DJ-Stands-and-Racks': {"url": '/l/Audio/DJ-Equipment/DJ-Stands-and-Racks'},
            'DJ-Turntables-and-Accessories': {"url": '/l/Audio/DJ-Equipment/DJ-Turntables-and-Accessories', "subcategories": {
                'DJ-Turntable-Accessories': {"url": '/l/Audio/DJ-Equipment/DJ-Turntables-and-Accessories/DJ-Turntable-Accessories'},
                'Phono-Preamps': {"url": '/l/Audio/DJ-Equipment/DJ-Turntables-and-Accessories/Phono-Preamps'},
                'Professional-Turntables': {"url": '/l/Audio/DJ-Equipment/DJ-Turntables-and-Accessories/Professional-Turntables'},
                'Turntables-and-Record-Players': {"url": '/l/Audio/DJ-Equipment/DJ-Turntables-and-Accessories/Turntables-and-Record-Players'}
            }}
        }},
        'Headphones-and-Earphones': {"url": '/l/Audio/Headphones-and-Earphones', "subcategories": {
            'Computer-Headsets': {"url": '/l/Audio/Headphones-and-Earphones/Computer-Headsets'},
            'DJ-and-Studio-Headphones': {"url": '/l/Audio/Headphones-and-Earphones/DJ-and-Studio-Headphones'},
            'Earphones-and-Earbuds': {"url": '/l/Audio/Headphones-and-Earphones/Earphones-and-Earbuds'},
            'Headphone-Accessories': {"url": '/l/Audio/Headphones-and-Earphones/Headphone-Accessories'},
            'Intercom-and-Broadcast-Headsets': {"url": '/l/Audio/Headphones-and-Earphones/Intercom-and-Broadcast-Headsets'},
            'Performance-Hearing-Protection': {"url": '/l/Audio/Headphones-and-Earphones/Performance-Hearing-Protection'},
            'Telephone-Headsets': {"url": '/l/Audio/Headphones-and-Earphones/Telephone-Headsets'},
            'Wired-Headphones': {"url": '/l/Audio/Headphones-and-Earphones/Wired-Headphones'},
            'Wireless-Headphones': {"url": '/l/Audio/Headphones-and-Earphones/Wireless-Headphones'}
        }},
        'Microphone-Accessories': {"url": '/l/Audio/Microphone-Accessories', "subcategories": {
            'Antennas-and-Accessories': {"url": '/l/Audio/Microphone-Accessories/Antennas-and-Accessories'},
            'Desktop-Microphone-Stands': {"url": '/l/Audio/Microphone-Accessories/Desktop-Microphone-Stands'},
            'Microphone-Boom-Poles': {"url": '/l/Audio/Microphone-Accessories/Microphone-Boom-Poles'},
            'Microphone-Cables-and-Adapters': {"url": '/l/Audio/Microphone-Accessories/Microphone-Cables-and-Adapters'},
            'Microphone-Cases': {"url": '/l/Audio/Microphone-Accessories/Microphone-Cases'},
            'Microphone-Mounts': {"url": '/l/Audio/Microphone-Accessories/Microphone-Mounts'},
            'Microphone-Parts-and-Components': {"url": '/l/Audio/Microphone-Accessories/Microphone-Parts-and-Components'},
            'Microphone-Power-Supplies': {"url": '/l/Audio/Microphone-Accessories/Microphone-Power-Supplies'},
            'Microphone-Stands': {"url": '/l/Audio/Microphone-Accessories/Microphone-Stands'},
            'Shockmounts': {"url": '/l/Audio/Microphone-Accessories/Shockmounts'},
            'Windscreens-and-Pop-Filters': {"url": '/l/Audio/Microphone-Accessories/Windscreens-and-Pop-Filters'}
        }},
        'Microphones': {"url": '/l/Audio/Microphones', "subcategories": {
            'Boundary-Microphones': {"url": '/l/Audio/Microphones/Boundary-Microphones'},
            'Condenser-Microphones': {"url": '/l/Audio/Microphones/Condenser-Microphones'},
            'Dynamic-Microphones': {"url": '/l/Audio/Microphones/Dynamic-Microphones'},
            'Gooseneck-and-Paging-Microphones': {"url": '/l/Audio/Microphones/Gooseneck-and-Paging-Microphones'},
            'Handheld-Microphones': {"url": '/l/Audio/Microphones/Handheld-Microphones'},
            'Headset-and-Earset-Microphones': {"url": '/l/Audio/Microphones/Headset-and-Earset-Microphones'},
            'Instrument-Microphones': {"url": '/l/Audio/Microphones/Instrument-Microphones'},
            'Lavalier-Microphones': {"url": '/l/Audio/Microphones/Lavalier-Microphones'},
            'Ribbon-Microphones': {"url": '/l/Audio/Microphones/Ribbon-Microphones'},
            'Shotgun-Microphones': {"url": '/l/Audio/Microphones/Shotgun-Microphones'},
            'Smartphone-Microphones': {"url": '/l/Audio/Microphones/Smartphone-Microphones'},
            'USB-Microphones': {"url": '/l/Audio/Microphones/USB-Microphones'},
            'Wireless-Microphones': {"url": '/l/Audio/Microphones/Wireless-Microphones', "subcategories": {
                'Handheld-Wireless-Microphone-Systems': {"url": '/l/Audio/Microphones/Wireless-Microphones/Handheld-Wireless-Microphone-Systems'},
                'Headset-Wireless-Microphone-Systems': {"url": '/l/Audio/Microphones/Wireless-Microphones/Headset-Wireless-Microphone-Systems'},
                'In-hyphen-Ear-Monitors': {"url": '/l/Audio/Microphones/Wireless-Microphones/In-hyphen-Ear-Monitors'},
                'Lavalier-Wireless-Microphone-Systems': {"url": '/l/Audio/Microphones/Wireless-Microphones/Lavalier-Wireless-Microphone-Systems'},
                'Wireless-Camera-Microphones': {"url": '/l/Audio/Microphones/Wireless-Microphones/Wireless-Camera-Microphones'},
                'Wireless-Instrument-Microphone-System': {"url": '/l/Audio/Microphones/Wireless-Microphones/Wireless-Instrument-Microphone-System'},
                'Wireless-Transmitters-and-Receivers': {"url": '/l/Audio/Microphones/Wireless-Microphones/Wireless-Transmitters-and-Receivers'}
            }}
        }},
        'PA-and-Live-Sound': {"url": '/l/Audio/PA-and-Live-Sound', "subcategories": {
            'Amplifiers': {"url": '/l/Audio/PA-and-Live-Sound/Amplifiers', "subcategories": {
                'Amplifiers-with-Mixers': {"url": '/l/Audio/PA-and-Live-Sound/Amplifiers/Amplifiers-with-Mixers'},
                'Headphone-and-Distribution': {"url": '/l/Audio/PA-and-Live-Sound/Amplifiers/Headphone-and-Distribution'},
                'Power-Amplifiers': {"url": '/l/Audio/PA-and-Live-Sound/Amplifiers/Power-Amplifiers'},
                'Vacuum-Tubes': {"url": '/l/Audio/PA-and-Live-Sound/Amplifiers/Vacuum-Tubes'}
            }},
            'Audio-Snakes-and-Stage-Boxes': {"url": '/l/Audio/PA-and-Live-Sound/Audio-Snakes-and-Stage-Boxes'},
            'Intercom-Systems': {"url": '/l/Audio/PA-and-Live-Sound/Intercom-Systems'},
            'Mixers': {"url": '/l/Audio/PA-and-Live-Sound/Mixers', "subcategories": {
                'Mixer-Accessories': {"url": '/l/Audio/PA-and-Live-Sound/Mixers/Mixer-Accessories'},
                'Mixer-Cases': {"url": '/l/Audio/PA-and-Live-Sound/Mixers/Mixer-Cases'},
                'Recording-Mixers': {"url": '/l/Audio/PA-and-Live-Sound/Mixers/Recording-Mixers'}
            }},
            'PA-Systems-and-Speakers': {"url": '/l/Audio/PA-and-Live-Sound/PA-Systems-and-Speakers', "subcategories": {
                'PA-Power-and-Presentation-Accessories': {"url": '/l/Audio/PA-and-Live-Sound/PA-Systems-and-Speakers/PA-Power-and-Presentation-Accessories'},
                'PA-Speakers': {"url": '/l/Audio/PA-and-Live-Sound/PA-Systems-and-Speakers/PA-Speakers'},
                'PA-System-Cases': {"url": '/l/Audio/PA-and-Live-Sound/PA-Systems-and-Speakers/PA-System-Cases'},
                'PA-Systems': {"url": '/l/Audio/PA-and-Live-Sound/PA-Systems-and-Speakers/PA-Systems'}
            }},
            'Performance-Hearing-Protection': {"url": '/l/Audio/PA-and-Live-Sound/Performance-Hearing-Protection'},
            'Sound-Meters-and-Reference-Mics': {"url": '/l/Audio/PA-and-Live-Sound/Sound-Meters-and-Reference-Mics'}
        }},
        'Studio-and-Recording': {"url": '/l/Audio/Studio-and-Recording', "subcategories": {
            'Acoustic-Treatments': {"url": '/l/Audio/Studio-and-Recording/Acoustic-Treatments', "subcategories": {
                'Acoustic-Panels-and-Kits': {"url": '/l/Audio/Studio-and-Recording/Acoustic-Treatments/Acoustic-Panels-and-Kits'},
                'Acoustic-Treatment-Accessories': {"url": '/l/Audio/Studio-and-Recording/Acoustic-Treatments/Acoustic-Treatment-Accessories'},
                'Bass-Traps': {"url": '/l/Audio/Studio-and-Recording/Acoustic-Treatments/Bass-Traps'}
            }},
            'Audio-Recorders-and-Players': {"url": '/l/Audio/Studio-and-Recording/Audio-Recorders-and-Players', "subcategories": {
                'CD-and-DVD-Recorders-and-Players': {"url": '/l/Audio/Studio-and-Recording/Audio-Recorders-and-Players/CD-and-DVD-Recorders-and-Players'},
                'Digital-Multitrack-Recorders-and-Players': {"url": '/l/Audio/Studio-and-Recording/Audio-Recorders-and-Players/Digital-Multitrack-Recorders-and-Players'}
            }},
            'Channel-Strips-and-Preamps': {"url": '/l/Audio/Studio-and-Recording/Channel-Strips-and-Preamps', "subcategories": {
                'Direct-Boxes': {"url": '/l/Audio/Studio-and-Recording/Channel-Strips-and-Preamps/Direct-Boxes'},
                'Microphone-Preamplifiers': {"url": '/l/Audio/Studio-and-Recording/Channel-Strips-and-Preamps/Microphone-Preamplifiers'}
            }},
            'Computer-Audio-for-Video': {"url": '/l/Audio/Studio-and-Recording/Computer-Audio-for-Video', "subcategories": {
                'Audio-Editing-Software': {"url": '/l/Audio/Studio-and-Recording/Computer-Audio-for-Video/Audio-Editing-Software'},
                'Digital-Audio-Interfaces': {"url": '/l/Audio/Studio-and-Recording/Computer-Audio-for-Video/Digital-Audio-Interfaces'},
                'Royalty-Free-Sound-EFX': {"url": '/l/Audio/Studio-and-Recording/Computer-Audio-for-Video/Royalty-Free-Sound-EFX'}
            }},
            'Professional-Audio-Speakers': {"url": '/l/Audio/Studio-and-Recording/Professional-Audio-Speakers', "subcategories": {
                'Installed-Amplifiers': {"url": '/l/Audio/Studio-and-Recording/Professional-Audio-Speakers/Installed-Amplifiers'},
                'Studio-Monitor-Parts-and-Accessories': {"url": '/l/Audio/Studio-and-Recording/Professional-Audio-Speakers/Studio-Monitor-Parts-and-Accessories'},
                'Studio-Monitors': {"url": '/l/Audio/Studio-and-Recording/Professional-Audio-Speakers/Studio-Monitors'},
                'Studio-Subwoofers': {"url": '/l/Audio/Studio-and-Recording/Professional-Audio-Speakers/Studio-Subwoofers'}
            }},
            'Recording-Studio-Equipment': {"url": '/l/Audio/Studio-and-Recording/Recording-Studio-Equipment'},
            'Signal-Processing': {"url": '/l/Audio/Studio-and-Recording/Signal-Processing', "subcategories": {
                'Dynamic-Processors': {"url": '/l/Audio/Studio-and-Recording/Signal-Processing/Dynamic-Processors'},
                'Equalizers': {"url": '/l/Audio/Studio-and-Recording/Signal-Processing/Equalizers'},
                'Signal-and-Effects-Processors': {"url": '/l/Audio/Studio-and-Recording/Signal-Processing/Signal-and-Effects-Processors'}
            }}
        }}
    }},
    'Computers': {"url": '/l/Computers', "subcategories": {
        'Computer-Accessories': {"url": '/l/Computers/Computer-Accessories', "subcategories": {
            'Computer-Bags-and-Cases': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases', "subcategories": {
                'Backpacks': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Backpacks'},
                'Computer-Monitor-Cases': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Computer-Monitor-Cases'},
                'Laptop-Bags-and-Cases': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Laptop-Bags-and-Cases', "subcategories": {
                    'Laptop-Backpacks': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Laptop-Bags-and-Cases/Laptop-Backpacks'},
                    'Laptop-Folio-Cases-comma-Sleeves-comma-and-Skins': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Laptop-Bags-and-Cases/Laptop-Folio-Cases-comma-Sleeves-comma-and-Skins'},
                    'Laptop-Shoulder-Bags': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Laptop-Bags-and-Cases/Laptop-Shoulder-Bags'},
                    'Rolling-Laptop-Cases': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Laptop-Bags-and-Cases/Rolling-Laptop-Cases'}
                }},
                'Memory-and-Media-Cases': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Memory-and-Media-Cases', "subcategories": {
                    'Disc-Cases-and-Sleeves': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Memory-and-Media-Cases/Disc-Cases-and-Sleeves'},
                    'Hard-Drive-Cases': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Memory-and-Media-Cases/Hard-Drive-Cases'},
                    'Memory-Card-Cases': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Memory-and-Media-Cases/Memory-Card-Cases'},
                    'USB-Flash-Drive-Cases': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Memory-and-Media-Cases/USB-Flash-Drive-Cases'}
                }},
                'Shoulder-and-Messenger-Bags': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Shoulder-and-Messenger-Bags'},
                'Wallets': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/Wallets'},
                'iPad-and-Tablet-Cases': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/iPad-and-Tablet-Cases', "subcategories": {
                    'Folio-Cases-comma-Sleeves-and-Wraps': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/iPad-and-Tablet-Cases/Folio-Cases-comma-Sleeves-and-Wraps'},
                    'Shoulder-Bags': {"url": '/l/Computers/Computer-Accessories/Computer-Bags-and-Cases/iPad-and-Tablet-Cases/Shoulder-Bags'}
                }}
            }},
            'Computer-Cables-and-Adapters': {"url": '/l/Computers/Computer-Accessories/Computer-Cables-and-Adapters', "subcategories": {
                'Cable-Management': {"url": '/l/Computers/Computer-Accessories/Computer-Cables-and-Adapters/Cable-Management'},
                'Ethernet-Cables-and-Connectors': {"url": '/l/Computers/Computer-Accessories/Computer-Cables-and-Adapters/Ethernet-Cables-and-Connectors'},
                'KVM-Cables-and-Switches': {"url": '/l/Computers/Computer-Accessories/Computer-Cables-and-Adapters/KVM-Cables-and-Switches'},
                'Laptop-and-Notebook-Accessories': {"url": '/l/Computers/Computer-Accessories/Computer-Cables-and-Adapters/Laptop-and-Notebook-Accessories'},
                'Thunderbolt-Cables-and-Adapters': {"url": '/l/Computers/Computer-Accessories/Computer-Cables-and-Adapters/Thunderbolt-Cables-and-Adapters'},
                'USB-Cables-and-Adapters': {"url": '/l/Computers/Computer-Accessories/Computer-Cables-and-Adapters/USB-Cables-and-Adapters'}
            }},
            'Computer-Headsets': {"url": '/l/Computers/Computer-Accessories/Computer-Headsets'},
            'Computer-Keyboards-and-Mice': {"url": '/l/Computers/Computer-Accessories/Computer-Keyboards-and-Mice', "subcategories": {
                'Keyboard-Accessories': {"url": '/l/Computers/Computer-Accessories/Computer-Keyboards-and-Mice/Keyboard-Accessories'},
                'Mice': {"url": '/l/Computers/Computer-Accessories/Computer-Keyboards-and-Mice/Mice'},
                'Standard-Layout-Keyboards': {"url": '/l/Computers/Computer-Accessories/Computer-Keyboards-and-Mice/Standard-Layout-Keyboards'},
                'Video-Editing-Keyboards': {"url": '/l/Computers/Computer-Accessories/Computer-Keyboards-and-Mice/Video-Editing-Keyboards'},
                'iPad-and-Tablet-Keyboards': {"url": '/l/Computers/Computer-Accessories/Computer-Keyboards-and-Mice/iPad-and-Tablet-Keyboards'}
            }},
            'Computer-Microphones-and-Webcams': {"url": '/l/Computers/Computer-Accessories/Computer-Microphones-and-Webcams'},
            'Computer-Speakers': {"url": '/l/Computers/Computer-Accessories/Computer-Speakers'},
            'Docking-Stations-and-Hubs': {"url": '/l/Computers/Computer-Accessories/Docking-Stations-and-Hubs'},
            'Routers-and-Modems': {"url": '/l/Computers/Computer-Accessories/Routers-and-Modems'}
        }},
        'Computer-Components': {"url": '/l/Computers/Computer-Components', "subcategories": {
            'Add-hyphen-On-Cards': {"url": '/l/Computers/Computer-Components/Add-hyphen-On-Cards'},
            'Computer-Memory-lrbr-RAM-rrbr': {"url": '/l/Computers/Computer-Components/Computer-Memory-lrbr-RAM-rrbr'},
            'Desktop-Power-Supplies': {"url": '/l/Computers/Computer-Components/Desktop-Power-Supplies'},
            'Fans-and-PC-Cooling': {"url": '/l/Computers/Computer-Components/Fans-and-PC-Cooling'},
            'Hard-Drives-and-Storage': {"url": '/l/Computers/Computer-Components/Hard-Drives-and-Storage'},
            'Motherboard-Interfaces': {"url": '/l/Computers/Computer-Components/Motherboard-Interfaces'},
            'PCI-and-PCIe-Cards': {"url": '/l/Computers/Computer-Components/PCI-and-PCIe-Cards'},
            'Video-and-Graphics-Cards': {"url": '/l/Computers/Computer-Components/Video-and-Graphics-Cards'}
        }},
        'Computer-Monitors-and-Mounts': {"url": '/l/Computers/Computer-Monitors-and-Mounts', "subcategories": {
            'Computer-Monitor-Accessories': {"url": '/l/Computers/Computer-Monitors-and-Mounts/Computer-Monitor-Accessories'},
            'Computer-Monitor-Mounts-and-Stands': {"url": '/l/Computers/Computer-Monitors-and-Mounts/Computer-Monitor-Mounts-and-Stands'},
            'Computer-Monitors': {"url": '/l/Computers/Computer-Monitors-and-Mounts/Computer-Monitors'},
            'Gaming-Monitors': {"url": '/l/Computers/Computer-Monitors-and-Mounts/Gaming-Monitors'},
            'Monitor-Color-Calibration': {"url": '/l/Computers/Computer-Monitors-and-Mounts/Monitor-Color-Calibration'}
        }},
        'Computer-Software': {"url": '/l/Computers/Computer-Software', "subcategories": {
            'Office-and-Organization-Software': {"url": '/l/Computers/Computer-Software/Office-and-Organization-Software'},
            'Operating-Systems': {"url": '/l/Computers/Computer-Software/Operating-Systems'},
            'Photo-Editing-Software': {"url": '/l/Computers/Computer-Software/Photo-Editing-Software'},
            'Security-and-Anti-hyphen-Virus-Software': {"url": '/l/Computers/Computer-Software/Security-and-Anti-hyphen-Virus-Software'}
        }},
        'Computer-Tower-Cases': {"url": '/l/Computers/Computer-Tower-Cases'},
        'Computer-Warranties': {"url": '/l/Computers/Computer-Warranties'},
        'Desktop-Computers': {"url": '/l/Computers/Desktop-Computers', "subcategories": {
            'All-in-One-PCs': {"url": '/l/Computers/Desktop-Computers/All-in-One-PCs'},
            'Apple-Desktops': {"url": '/l/Computers/Desktop-Computers/Apple-Desktops'},
            'Barebone-and-Mini-PCs': {"url": '/l/Computers/Desktop-Computers/Barebone-and-Mini-PCs'},
            'Desktops': {"url": '/l/Computers/Desktop-Computers/Desktops'},
            'Gaming-PCs': {"url": '/l/Computers/Desktop-Computers/Gaming-PCs'}
        }},
        'Digital-Storage-and-Duplication': {"url": '/l/Computers/Digital-Storage-and-Duplication', "subcategories": {
            'Blank-Media': {"url": '/l/Computers/Digital-Storage-and-Duplication/Blank-Media'},
            'Computer-Sticks': {"url": '/l/Computers/Digital-Storage-and-Duplication/Computer-Sticks'},
            'Disc-Printers-and-Labeling': {"url": '/l/Computers/Digital-Storage-and-Duplication/Disc-Printers-and-Labeling'},
            'Memory-Card-Readers-and-Writers': {"url": '/l/Computers/Digital-Storage-and-Duplication/Memory-Card-Readers-and-Writers'},
            'Memory-Cards': {"url": '/l/Computers/Digital-Storage-and-Duplication/Memory-Cards'},
            'Optical-Drives': {"url": '/l/Computers/Digital-Storage-and-Duplication/Optical-Drives'},
            'Storage-Media-Duplicators-and-Accessories': {"url": '/l/Computers/Digital-Storage-and-Duplication/Storage-Media-Duplicators-and-Accessories'},
            'USB-Flash-Drives-and-Thumb-Drives': {"url": '/l/Computers/Digital-Storage-and-Duplication/USB-Flash-Drives-and-Thumb-Drives'}
        }},
        'Drives-comma-SSD-and-Storage': {"url": '/l/Computers/Drives-comma-SSD-and-Storage', "subcategories": {
            'External-Desktop-Drives': {"url": '/l/Computers/Drives-comma-SSD-and-Storage/External-Desktop-Drives'},
            'External-Portable-Drives': {"url": '/l/Computers/Drives-comma-SSD-and-Storage/External-Portable-Drives'},
            'External-Solid-State-Drives-lrbr-SSD-rrbr': {"url": '/l/Computers/Drives-comma-SSD-and-Storage/External-Solid-State-Drives-lrbr-SSD-rrbr'},
            'Hard-Disk-Drives': {"url": '/l/Computers/Drives-comma-SSD-and-Storage/Hard-Disk-Drives'},
            'Hard-Drive-Arrays-and-RAID': {"url": '/l/Computers/Drives-comma-SSD-and-Storage/Hard-Drive-Arrays-and-RAID'},
            'Hard-Drive-Enclosures-and-Accessories': {"url": '/l/Computers/Drives-comma-SSD-and-Storage/Hard-Drive-Enclosures-and-Accessories'},
            'Internal-SSD-Drives': {"url": '/l/Computers/Drives-comma-SSD-and-Storage/Internal-SSD-Drives'},
            'Memory-Card-Backup-Devices': {"url": '/l/Computers/Drives-comma-SSD-and-Storage/Memory-Card-Backup-Devices'},
            'NAS-and-Server-Accessories': {"url": '/l/Computers/Drives-comma-SSD-and-Storage/NAS-and-Server-Accessories'},
            'NAS-and-Servers': {"url": '/l/Computers/Drives-comma-SSD-and-Storage/NAS-and-Servers'}
        }},
        'Inks-and-Toners': {"url": '/l/Computers/Inks-and-Toners'},
        'Laptops': {"url": '/l/Computers/Laptops', "subcategories": {
            'Chromebooks': {"url": '/l/Computers/Laptops/Chromebooks'},
            'Gaming-Laptops': {"url": '/l/Computers/Laptops/Gaming-Laptops'},
            'Laptops-and-Notebooks': {"url": '/l/Computers/Laptops/Laptops-and-Notebooks'},
            'MacBooks': {"url": '/l/Computers/Laptops/MacBooks'}
        }},
        'Networking': {"url": '/l/Computers/Networking', "subcategories": {
            'Antennas-and-Range-Extenders': {"url": '/l/Computers/Networking/Antennas-and-Range-Extenders'},
            'Ethernet-Bridges-and-Adapters': {"url": '/l/Computers/Networking/Ethernet-Bridges-and-Adapters'},
            'NAS-and-Server-Accessories': {"url": '/l/Computers/Networking/NAS-and-Server-Accessories'},
            'NAS-and-Servers': {"url": '/l/Computers/Networking/NAS-and-Servers'},
            'Network-Cards': {"url": '/l/Computers/Networking/Network-Cards'},
            'Networking-Switches': {"url": '/l/Computers/Networking/Networking-Switches'},
            'Routers-and-Modems': {"url": '/l/Computers/Networking/Routers-and-Modems'},
            'Wireless-Access-Points': {"url": '/l/Computers/Networking/Wireless-Access-Points'},
            'Wireless-Adapters-and-Cards': {"url": '/l/Computers/Networking/Wireless-Adapters-and-Cards'}
        }},
        'Printers': {"url": '/l/Computers/Printers'},
        'iPads-and-Tablets': {"url": '/l/Computers/iPads-and-Tablets', "subcategories": {
            'Drawing-Tablets-and-Electronic-Notepads': {"url": '/l/Computers/iPads-and-Tablets/Drawing-Tablets-and-Electronic-Notepads'},
            'Electronic-Pens-and-Styli': {"url": '/l/Computers/iPads-and-Tablets/Electronic-Pens-and-Styli'},
            'Tablets': {"url": '/l/Computers/iPads-and-Tablets/Tablets'},
            'iPad-and-Tablet-Accessories': {"url": '/l/Computers/iPads-and-Tablets/iPad-and-Tablet-Accessories'},
            'iPads': {"url": '/l/Computers/iPads-and-Tablets/iPads'}
        }}
    }},
    'Drones-and-Accessories': {"url": '/l/Drones-and-Accessories', "subcategories": {
        'Drone-Accessories': {"url": '/l/Drones-and-Accessories/Drone-Accessories'},
        'Drone-Bags-and-Cases': {"url": '/l/Drones-and-Accessories/Drone-Bags-and-Cases'},
        'Drone-Batteries-and-Chargers': {"url": '/l/Drones-and-Accessories/Drone-Batteries-and-Chargers'},
        'Drone-Cameras': {"url": '/l/Drones-and-Accessories/Drone-Cameras'},
        'Drone-Remote-Controls-and-Accessories': {"url": '/l/Drones-and-Accessories/Drone-Remote-Controls-and-Accessories'},
        'Drone-Software': {"url": '/l/Drones-and-Accessories/Drone-Software'},
        'Drone-Training-Courses': {"url": '/l/Drones-and-Accessories/Drone-Training-Courses'},
        'Drone-Warranties': {"url": '/l/Drones-and-Accessories/Drone-Warranties'},
        'Drones': {"url": '/l/Drones-and-Accessories/Drones'}
    }},
    'Gaming': {"url": '/l/Gaming', "subcategories": {
        'Console-Gaming': {"url": '/l/Gaming/Console-Gaming'},
        'Game-Downloads': {"url": '/l/Gaming/Game-Downloads'},
        'Gaming-Projectors': {"url": '/l/Gaming/Gaming-Projectors'},
        'PC-Gaming': {"url": '/l/Gaming/PC-Gaming', "subcategories": {
            'Computer-Tower-Cases': {"url": '/l/Gaming/PC-Gaming/Computer-Tower-Cases'},
            'Gaming-Desktops': {"url": '/l/Gaming/PC-Gaming/Gaming-Desktops'},
            'Gaming-Laptops': {"url": '/l/Gaming/PC-Gaming/Gaming-Laptops'},
            'Gaming-Monitors': {"url": '/l/Gaming/PC-Gaming/Gaming-Monitors'},
            'PC-Gaming-Accessories': {"url": '/l/Gaming/PC-Gaming/PC-Gaming-Accessories', "subcategories": {
                'Gaming-Controllers': {"url": '/l/Gaming/PC-Gaming/PC-Gaming-Accessories/Gaming-Controllers'},
                'Gaming-Furniture': {"url": '/l/Gaming/PC-Gaming/PC-Gaming-Accessories/Gaming-Furniture'},
                'Gaming-Headsets': {"url": '/l/Gaming/PC-Gaming/PC-Gaming-Accessories/Gaming-Headsets'},
                'Gaming-Keyboards': {"url": '/l/Gaming/PC-Gaming/PC-Gaming-Accessories/Gaming-Keyboards'},
                'Gaming-Mice': {"url": '/l/Gaming/PC-Gaming/PC-Gaming-Accessories/Gaming-Mice'}
            }}
        }},
        'VR-Headsets-and-Accessories': {"url": '/l/Gaming/VR-Headsets-and-Accessories'}
    }},
    'Home-Electronics': {"url": '/l/Home-Electronics', "subcategories": {
        'Auto-and-Marine': {"url": '/l/Home-Electronics/Auto-and-Marine', "subcategories": {
            'Antennas-and-FM-Transmitters': {"url": '/l/Home-Electronics/Auto-and-Marine/Antennas-and-FM-Transmitters'},
            'Area-and-Task-Lights': {"url": '/l/Home-Electronics/Auto-and-Marine/Area-and-Task-Lights'},
            'Automotive-Accessories': {"url": '/l/Home-Electronics/Auto-and-Marine/Automotive-Accessories'},
            'Car-Chargers-and-Power-Adapters': {"url": '/l/Home-Electronics/Auto-and-Marine/Car-Chargers-and-Power-Adapters'},
            'Car-Dash-Cameras-and-Mounts': {"url": '/l/Home-Electronics/Auto-and-Marine/Car-Dash-Cameras-and-Mounts'},
            'GPS-and-Navigation': {"url": '/l/Home-Electronics/Auto-and-Marine/GPS-and-Navigation'},
            'Jump-Starters-and-Air-Compressors': {"url": '/l/Home-Electronics/Auto-and-Marine/Jump-Starters-and-Air-Compressors'},
            'Megaphones-and-Car-Units': {"url": '/l/Home-Electronics/Auto-and-Marine/Megaphones-and-Car-Units'},
            'Two-hyphen-Way-Radios': {"url": '/l/Home-Electronics/Auto-and-Marine/Two-hyphen-Way-Radios'}
        }},
        'Batteries-and-Power-Supply': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply', "subcategories": {
            'Household-Batteries-and-Accessories': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply/Household-Batteries-and-Accessories', "subcategories": {
                'Household-Batteries': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply/Household-Batteries-and-Accessories/Household-Batteries'},
                'Household-Battery-Accessories': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply/Household-Batteries-and-Accessories/Household-Battery-Accessories'},
                'Household-Battery-Chargers': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply/Household-Batteries-and-Accessories/Household-Battery-Chargers'}
            }},
            'Portable-Chargers': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply/Portable-Chargers'},
            'Power-Supplies': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply/Power-Supplies', "subcategories": {
                'Electrical-Tools-and-Testers': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply/Power-Supplies/Electrical-Tools-and-Testers'},
                'Extension-Cords': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply/Power-Supplies/Extension-Cords'},
                'Outlet-Strips-and-Surge-Protectors': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply/Power-Supplies/Outlet-Strips-and-Surge-Protectors'},
                'Solar-Power': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply/Power-Supplies/Solar-Power'},
                'UPS-Backup-and-Accessories': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply/Power-Supplies/UPS-Backup-and-Accessories'},
                'Wall-and-Floor-Unit-Accessories': {"url": '/l/Home-Electronics/Batteries-and-Power-Supply/Power-Supplies/Wall-and-Floor-Unit-Accessories'}
            }}
        }},
        'Cell-Phone-Cases': {"url": '/l/Home-Electronics/Cell-Phone-Cases'},
        'Home-Audio': {"url": '/l/Home-Electronics/Home-Audio', "subcategories": {
            'Home-Audio-Accessories': {"url": '/l/Home-Electronics/Home-Audio/Home-Audio-Accessories'},
            'Karaoke-Equipment': {"url": '/l/Home-Electronics/Home-Audio/Karaoke-Equipment'},
            'Media-Players-and-Sound-Docks': {"url": '/l/Home-Electronics/Home-Audio/Media-Players-and-Sound-Docks'},
            'Turntables-and-Record-Players': {"url": '/l/Home-Electronics/Home-Audio/Turntables-and-Record-Players'}
        }},
        'Home-Office': {"url": '/l/Home-Electronics/Home-Office', "subcategories": {
            'Cubicle-and-Office-Furniture': {"url": '/l/Home-Electronics/Home-Office/Cubicle-and-Office-Furniture'},
            'Die-Cutting-Supplies': {"url": '/l/Home-Electronics/Home-Office/Die-Cutting-Supplies'},
            'Electronics-Warranties': {"url": '/l/Home-Electronics/Home-Office/Electronics-Warranties'},
            'Inks-and-Toners': {"url": '/l/Home-Electronics/Home-Office/Inks-and-Toners', "subcategories": {
                'Dye-Sub-and-Thermal-Ribbons': {"url": '/l/Home-Electronics/Home-Office/Inks-and-Toners/Dye-Sub-and-Thermal-Ribbons'},
                'Inkjet-Cartridges': {"url": '/l/Home-Electronics/Home-Office/Inks-and-Toners/Inkjet-Cartridges'},
                'Toner-Cartridges': {"url": '/l/Home-Electronics/Home-Office/Inks-and-Toners/Toner-Cartridges'},
                'Wide-Format-Cartridges': {"url": '/l/Home-Electronics/Home-Office/Inks-and-Toners/Wide-Format-Cartridges'}
            }},
            'Labeling-and-Shipping': {"url": '/l/Home-Electronics/Home-Office/Labeling-and-Shipping', "subcategories": {
                'Barcode-Scanners': {"url": '/l/Home-Electronics/Home-Office/Labeling-and-Shipping/Barcode-Scanners'},
                'Labeling-Accessories': {"url": '/l/Home-Electronics/Home-Office/Labeling-and-Shipping/Labeling-Accessories'},
                'Labeling-Ink-and-Toner': {"url": '/l/Home-Electronics/Home-Office/Labeling-and-Shipping/Labeling-Ink-and-Toner'},
                'Labeling-Machines': {"url": '/l/Home-Electronics/Home-Office/Labeling-and-Shipping/Labeling-Machines'},
                'Labeling-Tape': {"url": '/l/Home-Electronics/Home-Office/Labeling-and-Shipping/Labeling-Tape'}
            }},
            'Office-Machines': {"url": '/l/Home-Electronics/Home-Office/Office-Machines', "subcategories": {
                'Air-Conditioners-comma-Purifiers-and-Fans': {"url": '/l/Home-Electronics/Home-Office/Office-Machines/Air-Conditioners-comma-Purifiers-and-Fans'},
                'Calculators': {"url": '/l/Home-Electronics/Home-Office/Office-Machines/Calculators'},
                'Cash-Management-Machines': {"url": '/l/Home-Electronics/Home-Office/Office-Machines/Cash-Management-Machines'},
                'Phones': {"url": '/l/Home-Electronics/Home-Office/Office-Machines/Phones'},
                'Shredders': {"url": '/l/Home-Electronics/Home-Office/Office-Machines/Shredders'},
                'Voice-Recorders': {"url": '/l/Home-Electronics/Home-Office/Office-Machines/Voice-Recorders'}
            }},
            'Printer-Accessories': {"url": '/l/Home-Electronics/Home-Office/Printer-Accessories'},
            'Printer-Paper-and-Media': {"url": '/l/Home-Electronics/Home-Office/Printer-Paper-and-Media', "subcategories": {
                'Image-Protective-Coating': {"url": '/l/Home-Electronics/Home-Office/Printer-Paper-and-Media/Image-Protective-Coating'},
                'Printer-Paper': {"url": '/l/Home-Electronics/Home-Office/Printer-Paper-and-Media/Printer-Paper'},
                'Specialty-Paper-and-Media': {"url": '/l/Home-Electronics/Home-Office/Printer-Paper-and-Media/Specialty-Paper-and-Media'},
                'Wide-Format-Paper': {"url": '/l/Home-Electronics/Home-Office/Printer-Paper-and-Media/Wide-Format-Paper'}
            }},
            'Printers': {"url": '/l/Home-Electronics/Home-Office/Printers', "subcategories": {
                '3D-Printers-and-Accessories': {"url": '/l/Home-Electronics/Home-Office/Printers/3D-Printers-and-Accessories'},
                'All-hyphen-in-hyphen-One-Printers': {"url": '/l/Home-Electronics/Home-Office/Printers/All-hyphen-in-hyphen-One-Printers'},
                'Dot-Matrix-Printers': {"url": '/l/Home-Electronics/Home-Office/Printers/Dot-Matrix-Printers'},
                'Dye-Sub-and-Thermal-Printers': {"url": '/l/Home-Electronics/Home-Office/Printers/Dye-Sub-and-Thermal-Printers'},
                'Inkjet-Printers': {"url": '/l/Home-Electronics/Home-Office/Printers/Inkjet-Printers'},
                'Laser-Printers': {"url": '/l/Home-Electronics/Home-Office/Printers/Laser-Printers'},
                'Printer-Warranties': {"url": '/l/Home-Electronics/Home-Office/Printers/Printer-Warranties'},
                'Wide-Format-Printers': {"url": '/l/Home-Electronics/Home-Office/Printers/Wide-Format-Printers'}
            }},
            'Rack-Mounts-and-Workstations': {"url": '/l/Home-Electronics/Home-Office/Rack-Mounts-and-Workstations', "subcategories": {
                'Charging-Carts': {"url": '/l/Home-Electronics/Home-Office/Rack-Mounts-and-Workstations/Charging-Carts'},
                'Rack-Accessories': {"url": '/l/Home-Electronics/Home-Office/Rack-Mounts-and-Workstations/Rack-Accessories'},
                'Rack-Cases': {"url": '/l/Home-Electronics/Home-Office/Rack-Mounts-and-Workstations/Rack-Cases'},
                'Rack-Enclosures-and-Cabinets': {"url": '/l/Home-Electronics/Home-Office/Rack-Mounts-and-Workstations/Rack-Enclosures-and-Cabinets'},
                'Workstations-and-Desks': {"url": '/l/Home-Electronics/Home-Office/Rack-Mounts-and-Workstations/Workstations-and-Desks'}
            }},
            'Scanner-Accessories': {"url": '/l/Home-Electronics/Home-Office/Scanner-Accessories'},
            'Scanners': {"url": '/l/Home-Electronics/Home-Office/Scanners', "subcategories": {
                'Film-Scanners': {"url": '/l/Home-Electronics/Home-Office/Scanners/Film-Scanners'},
                'Flatbed-Scanners': {"url": '/l/Home-Electronics/Home-Office/Scanners/Flatbed-Scanners'},
                'Photo-Scanners': {"url": '/l/Home-Electronics/Home-Office/Scanners/Photo-Scanners'},
                'Portable-Scanners': {"url": '/l/Home-Electronics/Home-Office/Scanners/Portable-Scanners'},
                'Sheetfed-Scanners': {"url": '/l/Home-Electronics/Home-Office/Scanners/Sheetfed-Scanners'}
            }},
            'Wide-Format-Printer-Accessories': {"url": '/l/Home-Electronics/Home-Office/Wide-Format-Printer-Accessories'}
        }},
        'Home-Security-and-Surveillance-Systems': {"url": '/l/Home-Electronics/Home-Security-and-Surveillance-Systems', "subcategories": {
            'Home-Smart-Locks': {"url": '/l/Home-Electronics/Home-Security-and-Surveillance-Systems/Home-Smart-Locks'},
            'Motion-Sensors-and-Detectors': {"url": '/l/Home-Electronics/Home-Security-and-Surveillance-Systems/Motion-Sensors-and-Detectors'},
            'Security-Cameras': {"url": '/l/Home-Electronics/Home-Security-and-Surveillance-Systems/Security-Cameras'},
            'Surveillance-Lenses-and-Accessories': {"url": '/l/Home-Electronics/Home-Security-and-Surveillance-Systems/Surveillance-Lenses-and-Accessories'},
            'Wireless-Doorbell-Cameras': {"url": '/l/Home-Electronics/Home-Security-and-Surveillance-Systems/Wireless-Doorbell-Cameras'}
        }},
        'Home-Theater': {"url": '/l/Home-Electronics/Home-Theater', "subcategories": {
            'Home-Theater-Accessories': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Accessories', "subcategories": {
                'Cleaning-Accessories': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Accessories/Cleaning-Accessories'},
                'HDMI-and-DVI-Cables': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Accessories/HDMI-and-DVI-Cables'},
                'Home-Theater-Remotes-and-Switches': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Accessories/Home-Theater-Remotes-and-Switches'},
                'Speaker-Stands-and-Mounts': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Accessories/Speaker-Stands-and-Mounts'},
                'Streaming-Media-Players': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Accessories/Streaming-Media-Players'}
            }},
            'Home-Theater-Furniture': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Furniture'},
            'Home-Theater-Speakers': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Speakers', "subcategories": {
                'Bluetooth-and-Wireless-Speakers': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Speakers/Bluetooth-and-Wireless-Speakers'},
                'Bookshelf-Speakers': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Speakers/Bookshelf-Speakers'},
                'Center-Channel-Speakers': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Speakers/Center-Channel-Speakers'},
                'Floor-Standing-Speakers': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Speakers/Floor-Standing-Speakers'},
                'Home-Theater-Systems': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Speakers/Home-Theater-Systems'},
                'In-hyphen-Wall-and-In-hyphen-Ceiling-Speakers': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Speakers/In-hyphen-Wall-and-In-hyphen-Ceiling-Speakers'},
                'Outdoor-Speakers': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Speakers/Outdoor-Speakers'},
                'Soundbars': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Speakers/Soundbars'},
                'Subwoofers': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Speakers/Subwoofers'},
                'Surround-Sound-Speakers': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Speakers/Surround-Sound-Speakers'}
            }},
            'Home-Theater-Systems': {"url": '/l/Home-Electronics/Home-Theater/Home-Theater-Systems'},
            'Projector-Screens-and-Accessories': {"url": '/l/Home-Electronics/Home-Theater/Projector-Screens-and-Accessories', "subcategories": {
                'Projector-Accessories': {"url": '/l/Home-Electronics/Home-Theater/Projector-Screens-and-Accessories/Projector-Accessories'},
                'Projector-Screen-Accessories': {"url": '/l/Home-Electronics/Home-Theater/Projector-Screens-and-Accessories/Projector-Screen-Accessories'},
                'Projector-Screens': {"url": '/l/Home-Electronics/Home-Theater/Projector-Screens-and-Accessories/Projector-Screens'}
            }},
            'Projectors': {"url": '/l/Home-Electronics/Home-Theater/Projectors', "subcategories": {
                'Business-Professional-Projectors': {"url": '/l/Home-Electronics/Home-Theater/Projectors/Business-Professional-Projectors'},
                'Gaming-Projectors': {"url": '/l/Home-Electronics/Home-Theater/Projectors/Gaming-Projectors'},
                'Home-Entertainment-Projectors': {"url": '/l/Home-Electronics/Home-Theater/Projectors/Home-Entertainment-Projectors'},
                'Portable-Projectors': {"url": '/l/Home-Electronics/Home-Theater/Projectors/Portable-Projectors'},
                'Projector-Accessories': {"url": '/l/Home-Electronics/Home-Theater/Projectors/Projector-Accessories'}
            }},
            'Receivers-and-Amplifiers': {"url": '/l/Home-Electronics/Home-Theater/Receivers-and-Amplifiers'},
            'Televisions': {"url": '/l/Home-Electronics/Home-Theater/Televisions'}
        }},
        'Mobile-Phone-Accessories': {"url": '/l/Home-Electronics/Mobile-Phone-Accessories', "subcategories": {
            'Cell-Phone-Cases': {"url": '/l/Home-Electronics/Mobile-Phone-Accessories/Cell-Phone-Cases'},
            'Device-Charging-and-Sync-Cables': {"url": '/l/Home-Electronics/Mobile-Phone-Accessories/Device-Charging-and-Sync-Cables'},
            'Device-Mounts-and-Stands': {"url": '/l/Home-Electronics/Mobile-Phone-Accessories/Device-Mounts-and-Stands'},
            'Mobile-Phone-Printers': {"url": '/l/Home-Electronics/Mobile-Phone-Accessories/Mobile-Phone-Printers'},
            'Phone-Screen-Protection': {"url": '/l/Home-Electronics/Mobile-Phone-Accessories/Phone-Screen-Protection'},
            'Portable-Chargers': {"url": '/l/Home-Electronics/Mobile-Phone-Accessories/Portable-Chargers'}
        }},
        'Novelty-and-Gifts': {"url": '/l/Home-Electronics/Novelty-and-Gifts'},
        'Smart-Home': {"url": '/l/Home-Electronics/Smart-Home', "subcategories": {
            'Bluetooth-Trackers': {"url": '/l/Home-Electronics/Smart-Home/Bluetooth-Trackers'},
            'Smart-Doorbells': {"url": '/l/Home-Electronics/Smart-Home/Smart-Doorbells'},
            'Smart-Home-Locks': {"url": '/l/Home-Electronics/Smart-Home/Smart-Home-Locks'},
            'Smart-Lighting': {"url": '/l/Home-Electronics/Smart-Home/Smart-Lighting'},
            'Smart-Speakers-and-Voice-Assistants': {"url": '/l/Home-Electronics/Smart-Home/Smart-Speakers-and-Voice-Assistants'}
        }},
        'Surveillance-and-Security-Accessories': {"url": '/l/Home-Electronics/Surveillance-and-Security-Accessories', "subcategories": {
            'Security-Camera-Mounting': {"url": '/l/Home-Electronics/Surveillance-and-Security-Accessories/Security-Camera-Mounting'},
            'Security-Video-Recorders': {"url": '/l/Home-Electronics/Surveillance-and-Security-Accessories/Security-Video-Recorders'},
            'Surveillance-Cables-and-Accessories': {"url": '/l/Home-Electronics/Surveillance-and-Security-Accessories/Surveillance-Cables-and-Accessories'},
            'Surveillance-Monitors': {"url": '/l/Home-Electronics/Surveillance-and-Security-Accessories/Surveillance-Monitors'}
        }},
        'Toys-and-STEM-Education': {"url": '/l/Home-Electronics/Toys-and-STEM-Education'},
        'Unlocked-Cell-Phones': {"url": '/l/Home-Electronics/Unlocked-Cell-Phones'},
        'Wearable-Tech': {"url": '/l/Home-Electronics/Wearable-Tech', "subcategories": {
            'Exercise-and-Sleep-Monitors': {"url": '/l/Home-Electronics/Wearable-Tech/Exercise-and-Sleep-Monitors'},
            'Smart-Watches': {"url": '/l/Home-Electronics/Wearable-Tech/Smart-Watches'},
            'Virtual-Reality': {"url": '/l/Home-Electronics/Wearable-Tech/Virtual-Reality'},
            'Wearable-Tech-Accessories': {"url": '/l/Home-Electronics/Wearable-Tech/Wearable-Tech-Accessories'}
        }},
        'Wireless-and-Bluetooth-Headphones': {"url": '/l/Home-Electronics/Wireless-and-Bluetooth-Headphones'}
    }},
    'Miscellaneous': {"url": '/l/Miscellaneous', "subcategories": {
        'New-Products-at-Adorama': {"url": '/l/Miscellaneous/New-Products-at-Adorama'}
    }},
    'Musical-Instruments': {"url": '/l/Musical-Instruments', "subcategories": {
        'DJ-Equipment': {"url": '/l/Musical-Instruments/DJ-Equipment', "subcategories": {
            'DJ-Controllers': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Controllers'},
            'DJ-Equipment-Cases': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Equipment-Cases'},
            'DJ-Headphones': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Headphones'},
            'DJ-Lighting-and-Effects': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Lighting-and-Effects', "subcategories": {
                'Color-and-Wash-Lights': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Lighting-and-Effects/Color-and-Wash-Lights'},
                'DJ-and-Effect-Lights': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Lighting-and-Effects/DJ-and-Effect-Lights'},
                'Fog-and-Bubble-Machines': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Lighting-and-Effects/Fog-and-Bubble-Machines'},
                'Lighting-Cables-and-Accessories': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Lighting-and-Effects/Lighting-Cables-and-Accessories'},
                'Lighting-Controllers-and-Interfaces': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Lighting-and-Effects/Lighting-Controllers-and-Interfaces'},
                'Par-Cans': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Lighting-and-Effects/Par-Cans'},
                'Spotlights': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Lighting-and-Effects/Spotlights'}
            }},
            'DJ-Mixers': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Mixers'},
            'DJ-Stands-and-Racks': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Stands-and-Racks'},
            'DJ-Turntables-and-Accessories': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Turntables-and-Accessories', "subcategories": {
                'DJ-Turntable-Accessories': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Turntables-and-Accessories/DJ-Turntable-Accessories'},
                'Phono-Preamps': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Turntables-and-Accessories/Phono-Preamps'},
                'Professional-Turntables': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Turntables-and-Accessories/Professional-Turntables'},
                'Turntables-and-Record-Players': {"url": '/l/Musical-Instruments/DJ-Equipment/DJ-Turntables-and-Accessories/Turntables-and-Record-Players'}
            }}
        }},
        'Drums-and-Percussion': {"url": '/l/Musical-Instruments/Drums-and-Percussion', "subcategories": {
            'Acoustic-Drums': {"url": '/l/Musical-Instruments/Drums-and-Percussion/Acoustic-Drums'},
            'Cymbals-and-Gongs': {"url": '/l/Musical-Instruments/Drums-and-Percussion/Cymbals-and-Gongs'},
            'Drum-Hardware-and-Seating': {"url": '/l/Musical-Instruments/Drums-and-Percussion/Drum-Hardware-and-Seating'},
            'Drum-Pedals-and-Accessories': {"url": '/l/Musical-Instruments/Drums-and-Percussion/Drum-Pedals-and-Accessories'},
            'Electronic-Drums': {"url": '/l/Musical-Instruments/Drums-and-Percussion/Electronic-Drums'}
        }},
        'Effects': {"url": '/l/Musical-Instruments/Effects', "subcategories": {
            'Effects-Pedal-Accessories': {"url": '/l/Musical-Instruments/Effects/Effects-Pedal-Accessories'},
            'Effects-Pedals': {"url": '/l/Musical-Instruments/Effects/Effects-Pedals'}
        }},
        'Folk-Instruments': {"url": '/l/Musical-Instruments/Folk-Instruments', "subcategories": {
            'Banjos': {"url": '/l/Musical-Instruments/Folk-Instruments/Banjos'},
            'Harmonicas': {"url": '/l/Musical-Instruments/Folk-Instruments/Harmonicas'},
            'Mandolins': {"url": '/l/Musical-Instruments/Folk-Instruments/Mandolins'},
            'Ukuleles': {"url": '/l/Musical-Instruments/Folk-Instruments/Ukuleles'}
        }},
        'Guitars': {"url": '/l/Musical-Instruments/Guitars', "subcategories": {
            'Acoustic-Electric-Guitars': {"url": '/l/Musical-Instruments/Guitars/Acoustic-Electric-Guitars'},
            'Acoustic-Guitars': {"url": '/l/Musical-Instruments/Guitars/Acoustic-Guitars'},
            'Bass-Guitars': {"url": '/l/Musical-Instruments/Guitars/Bass-Guitars'},
            'Electric-Guitars': {"url": '/l/Musical-Instruments/Guitars/Electric-Guitars'},
            'Guitar-Accessories': {"url": '/l/Musical-Instruments/Guitars/Guitar-Accessories'}
        }},
        'In-hyphen-Ear-Monitors': {"url": '/l/Musical-Instruments/In-hyphen-Ear-Monitors'},
        'Instrument-Accessories': {"url": '/l/Musical-Instruments/Instrument-Accessories', "subcategories": {
            'Clothing-and-Collectibles': {"url": '/l/Musical-Instruments/Instrument-Accessories/Clothing-and-Collectibles'},
            'Guitar-Accessories': {"url": '/l/Musical-Instruments/Instrument-Accessories/Guitar-Accessories', "subcategories": {
                'Parts-and-Tools': {"url": '/l/Musical-Instruments/Instrument-Accessories/Guitar-Accessories/Parts-and-Tools'},
                'Straps': {"url": '/l/Musical-Instruments/Instrument-Accessories/Guitar-Accessories/Straps'},
                'Strings': {"url": '/l/Musical-Instruments/Instrument-Accessories/Guitar-Accessories/Strings'}
            }},
            'Instrument-Bags-and-Cases': {"url": '/l/Musical-Instruments/Instrument-Accessories/Instrument-Bags-and-Cases'},
            'Instrument-Cables': {"url": '/l/Musical-Instruments/Instrument-Accessories/Instrument-Cables'},
            'Instrument-Trainers-and-Tuners': {"url": '/l/Musical-Instruments/Instrument-Accessories/Instrument-Trainers-and-Tuners'},
            'Stands-and-Seating': {"url": '/l/Musical-Instruments/Instrument-Accessories/Stands-and-Seating'},
            'String-Instrument-Accessories': {"url": '/l/Musical-Instruments/Instrument-Accessories/String-Instrument-Accessories'}
        }},
        'Instrument-Amplifiers': {"url": '/l/Musical-Instruments/Instrument-Amplifiers', "subcategories": {
            'Amplifier-Accessories': {"url": '/l/Musical-Instruments/Instrument-Amplifiers/Amplifier-Accessories'},
            'Bass-Amp-Cabinets': {"url": '/l/Musical-Instruments/Instrument-Amplifiers/Bass-Amp-Cabinets'},
            'Bass-Amp-Heads': {"url": '/l/Musical-Instruments/Instrument-Amplifiers/Bass-Amp-Heads'},
            'Bass-Combo-Amps-and-Kits': {"url": '/l/Musical-Instruments/Instrument-Amplifiers/Bass-Combo-Amps-and-Kits'},
            'Guitar-Amp-Cabinets': {"url": '/l/Musical-Instruments/Instrument-Amplifiers/Guitar-Amp-Cabinets'},
            'Guitar-Amp-Heads': {"url": '/l/Musical-Instruments/Instrument-Amplifiers/Guitar-Amp-Heads'},
            'Guitar-Combo-Amps-and-Kits': {"url": '/l/Musical-Instruments/Instrument-Amplifiers/Guitar-Combo-Amps-and-Kits'},
            'Keyboard-Amps': {"url": '/l/Musical-Instruments/Instrument-Amplifiers/Keyboard-Amps'}
        }},
        'Keyboards-and-MIDI': {"url": '/l/Musical-Instruments/Keyboards-and-MIDI', "subcategories": {
            'Keyboard-and-MIDI-Accessories': {"url": '/l/Musical-Instruments/Keyboards-and-MIDI/Keyboard-and-MIDI-Accessories'},
            'Keyboards-and-Pianos': {"url": '/l/Musical-Instruments/Keyboards-and-MIDI/Keyboards-and-Pianos'},
            'Modular-Synths-and-Sequencers': {"url": '/l/Musical-Instruments/Keyboards-and-MIDI/Modular-Synths-and-Sequencers'},
            'Synthesizers-and-Euroracks': {"url": '/l/Musical-Instruments/Keyboards-and-MIDI/Synthesizers-and-Euroracks'}
        }},
        'Microphone-Accessories': {"url": '/l/Musical-Instruments/Microphone-Accessories'},
        'Microphones': {"url": '/l/Musical-Instruments/Microphones'},
        'PA-and-Live-Sound': {"url": '/l/Musical-Instruments/PA-and-Live-Sound'},
        'Studio-and-Recording': {"url": '/l/Musical-Instruments/Studio-and-Recording'}
    }},
    'Optics-and-Binoculars': {"url": '/l/Optics-and-Binoculars', "subcategories": {
        'Binoculars-and-Accessories': {"url": '/l/Optics-and-Binoculars/Binoculars-and-Accessories', "subcategories": {
            'Astronomy-Binoculars': {"url": '/l/Optics-and-Binoculars/Binoculars-and-Accessories/Astronomy-Binoculars'},
            'Binocular-Accessories': {"url": '/l/Optics-and-Binoculars/Binoculars-and-Accessories/Binocular-Accessories'},
            'Binocular-Cases': {"url": '/l/Optics-and-Binoculars/Binoculars-and-Accessories/Binocular-Cases'},
            'Binoculars': {"url": '/l/Optics-and-Binoculars/Binoculars-and-Accessories/Binoculars'},
            'Opera-Glasses': {"url": '/l/Optics-and-Binoculars/Binoculars-and-Accessories/Opera-Glasses'},
            'Solar-Binoculars-and-Eclipse-Viewers': {"url": '/l/Optics-and-Binoculars/Binoculars-and-Accessories/Solar-Binoculars-and-Eclipse-Viewers'}
        }},
        'Field-Accessories': {"url": '/l/Optics-and-Binoculars/Field-Accessories', "subcategories": {
            'Area-and-Task-Lights': {"url": '/l/Optics-and-Binoculars/Field-Accessories/Area-and-Task-Lights'},
            'Camping-Coolers-and-Ice-Chests': {"url": '/l/Optics-and-Binoculars/Field-Accessories/Camping-Coolers-and-Ice-Chests'},
            'Flashlight-and-Weapon-Light-Accessories': {"url": '/l/Optics-and-Binoculars/Field-Accessories/Flashlight-and-Weapon-Light-Accessories'},
            'Flashlights': {"url": '/l/Optics-and-Binoculars/Field-Accessories/Flashlights'},
            'Headlamps': {"url": '/l/Optics-and-Binoculars/Field-Accessories/Headlamps'},
            'Metal-Detectors-and-Accessories': {"url": '/l/Optics-and-Binoculars/Field-Accessories/Metal-Detectors-and-Accessories'},
            'Portable-Radios': {"url": '/l/Optics-and-Binoculars/Field-Accessories/Portable-Radios'},
            'Survival-Essentials': {"url": '/l/Optics-and-Binoculars/Field-Accessories/Survival-Essentials'},
            'Trail-Cameras': {"url": '/l/Optics-and-Binoculars/Field-Accessories/Trail-Cameras'},
            'Weapon-Lights': {"url": '/l/Optics-and-Binoculars/Field-Accessories/Weapon-Lights'}
        }},
        'Laser-Rangefinders-and-Accessories': {"url": '/l/Optics-and-Binoculars/Laser-Rangefinders-and-Accessories'},
        'Microscopes-and-Accessories': {"url": '/l/Optics-and-Binoculars/Microscopes-and-Accessories', "subcategories": {
            'Digital-Microscopes': {"url": '/l/Optics-and-Binoculars/Microscopes-and-Accessories/Digital-Microscopes'},
            'Microscope-Accessories': {"url": '/l/Optics-and-Binoculars/Microscopes-and-Accessories/Microscope-Accessories'},
            'Microscopes': {"url": '/l/Optics-and-Binoculars/Microscopes-and-Accessories/Microscopes'}
        }},
        'Monoculars': {"url": '/l/Optics-and-Binoculars/Monoculars'},
        'Nightvision-and-Thermal-Imaging': {"url": '/l/Optics-and-Binoculars/Nightvision-and-Thermal-Imaging', "subcategories": {
            'Night-Vision': {"url": '/l/Optics-and-Binoculars/Nightvision-and-Thermal-Imaging/Night-Vision'},
            'Night-Vision-Thermal-Accessories': {"url": '/l/Optics-and-Binoculars/Nightvision-and-Thermal-Imaging/Night-Vision-Thermal-Accessories'},
            'Thermal-Imaging': {"url": '/l/Optics-and-Binoculars/Nightvision-and-Thermal-Imaging/Thermal-Imaging'}
        }},
        'Rifle-Scopes-and-Shooting-Gear': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear', "subcategories": {
            'Airgun-Scopes-and-Sights': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Airgun-Scopes-and-Sights'},
            'Archery-Scopes-and-Sights': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Archery-Scopes-and-Sights'},
            'Handgun-Scopes-and-Mounts': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Handgun-Scopes-and-Mounts'},
            'Rifle-Scope-Accessories': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scope-Accessories', "subcategories": {
                'Filters-and-Anti-hyphen-Reflection-Devices': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scope-Accessories/Filters-and-Anti-hyphen-Reflection-Devices'},
                'Laser-Accessories': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scope-Accessories/Laser-Accessories'},
                'Mounting-Adapters': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scope-Accessories/Mounting-Adapters'},
                'Optics-Caps-and-Sun-Shades': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scope-Accessories/Optics-Caps-and-Sun-Shades'},
                'Red-Dot-and-Holo-Sight-Add-hyphen-Ons': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scope-Accessories/Red-Dot-and-Holo-Sight-Add-hyphen-Ons'},
                'Riflescope-Add-hyphen-Ons': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scope-Accessories/Riflescope-Add-hyphen-Ons'},
                'Riflescope-Mounts': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scope-Accessories/Riflescope-Mounts'},
                'Riflescope-Rails-and-Bases': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scope-Accessories/Riflescope-Rails-and-Bases'},
                'Ring-and-Mount-Add-hyphen-Ons': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scope-Accessories/Ring-and-Mount-Add-hyphen-Ons'},
                'Rings': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scope-Accessories/Rings'},
                'Sporting-Optics-Cleaning-Gear': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scope-Accessories/Sporting-Optics-Cleaning-Gear'}
            }},
            'Rifle-Scopes': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Rifle-Scopes'},
            'Shooting-Gear': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Shooting-Gear', "subcategories": {
                'Archery-Accessories': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Shooting-Gear/Archery-Accessories'},
                'Carry-and-Storage': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Shooting-Gear/Carry-and-Storage'},
                'Eye-and-Ear-Protection': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Shooting-Gear/Eye-and-Ear-Protection'},
                'Gun-Cleaning-and-Maintenance': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Shooting-Gear/Gun-Cleaning-and-Maintenance'},
                'Gun-Parts-and-Shooting-Extras': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Shooting-Gear/Gun-Parts-and-Shooting-Extras'},
                'Holsters': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Shooting-Gear/Holsters'},
                'Knives-and-Multi-hyphen-Tools': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Shooting-Gear/Knives-and-Multi-hyphen-Tools'},
                'Reloading-Supplies': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Shooting-Gear/Reloading-Supplies'},
                'Shooting-Accessories': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Shooting-Gear/Shooting-Accessories'},
                'Shooting-Apparel': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Shooting-Gear/Shooting-Apparel'}
            }},
            'Sights-and-Accessories': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Sights-and-Accessories', "subcategories": {
                'Laser-Sights': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Sights-and-Accessories/Laser-Sights'},
                'Laser-Trainer-and-Bore-Sighter': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Sights-and-Accessories/Laser-Trainer-and-Bore-Sighter'},
                'Red-Dot-and-Holo-Sights': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Sights-and-Accessories/Red-Dot-and-Holo-Sights'},
                'Replacement-Sights': {"url": '/l/Optics-and-Binoculars/Rifle-Scopes-and-Shooting-Gear/Sights-and-Accessories/Replacement-Sights'}
            }}
        }},
        'Spotting-Scopes-and-Accessories': {"url": '/l/Optics-and-Binoculars/Spotting-Scopes-and-Accessories', "subcategories": {
            'Digiscoping': {"url": '/l/Optics-and-Binoculars/Spotting-Scopes-and-Accessories/Digiscoping'},
            'Spotting-Scope-Accessories': {"url": '/l/Optics-and-Binoculars/Spotting-Scopes-and-Accessories/Spotting-Scope-Accessories'},
            'Spotting-Scope-Cases': {"url": '/l/Optics-and-Binoculars/Spotting-Scopes-and-Accessories/Spotting-Scope-Cases'},
            'Spotting-Scope-Eyepieces': {"url": '/l/Optics-and-Binoculars/Spotting-Scopes-and-Accessories/Spotting-Scope-Eyepieces'},
            'Spotting-Scopes': {"url": '/l/Optics-and-Binoculars/Spotting-Scopes-and-Accessories/Spotting-Scopes'},
            'T-Mounts-for-Digiscoping': {"url": '/l/Optics-and-Binoculars/Spotting-Scopes-and-Accessories/T-Mounts-for-Digiscoping'}
        }},
        'Telescopes-and-Astronomy': {"url": '/l/Optics-and-Binoculars/Telescopes-and-Astronomy', "subcategories": {
            'Astrophotography': {"url": '/l/Optics-and-Binoculars/Telescopes-and-Astronomy/Astrophotography'},
            'Skywatching-Binoculars': {"url": '/l/Optics-and-Binoculars/Telescopes-and-Astronomy/Skywatching-Binoculars'},
            'Smart-Telescopes': {"url": '/l/Optics-and-Binoculars/Telescopes-and-Astronomy/Smart-Telescopes'},
            'Solar-Binoculars-and-Eclipse-Viewers': {"url": '/l/Optics-and-Binoculars/Telescopes-and-Astronomy/Solar-Binoculars-and-Eclipse-Viewers'},
            'Telescope-Accessories': {"url": '/l/Optics-and-Binoculars/Telescopes-and-Astronomy/Telescope-Accessories'},
            'Telescope-Eyepieces': {"url": '/l/Optics-and-Binoculars/Telescopes-and-Astronomy/Telescope-Eyepieces'},
            'Telescope-Filters': {"url": '/l/Optics-and-Binoculars/Telescopes-and-Astronomy/Telescope-Filters'},
            'Telescope-Tripods': {"url": '/l/Optics-and-Binoculars/Telescopes-and-Astronomy/Telescope-Tripods'},
            'Telescope-Tripods-and-Mounts': {"url": '/l/Optics-and-Binoculars/Telescopes-and-Astronomy/Telescope-Tripods-and-Mounts'},
            'Telescopes': {"url": '/l/Optics-and-Binoculars/Telescopes-and-Astronomy/Telescopes'}
        }}
    }},
    'Photography': {"url": '/l/Photography', "subcategories": {
        'Camera-Accessories': {"url": '/l/Photography/Camera-Accessories', "subcategories": {
            'Battery-Grips': {"url": '/l/Photography/Camera-Accessories/Battery-Grips'},
            'Bellows-and-Focusing-Rails': {"url": '/l/Photography/Camera-Accessories/Bellows-and-Focusing-Rails'},
            'Body-Caps': {"url": '/l/Photography/Camera-Accessories/Body-Caps'},
            'Camera-Bags-and-Cases': {"url": '/l/Photography/Camera-Accessories/Camera-Bags-and-Cases'},
            'Camera-Batteries': {"url": '/l/Photography/Camera-Accessories/Camera-Batteries'},
            'Camera-Battery-Chargers': {"url": '/l/Photography/Camera-Accessories/Camera-Battery-Chargers'},
            'Camera-Cables-and-Accessories': {"url": '/l/Photography/Camera-Accessories/Camera-Cables-and-Accessories'},
            'Camera-Cleaning': {"url": '/l/Photography/Camera-Accessories/Camera-Cleaning'},
            'Camera-Grips': {"url": '/l/Photography/Camera-Accessories/Camera-Grips'},
            'Camera-Microphones': {"url": '/l/Photography/Camera-Accessories/Camera-Microphones'},
            'Camera-Supports': {"url": '/l/Photography/Camera-Accessories/Camera-Supports'},
            'Diopters': {"url": '/l/Photography/Camera-Accessories/Diopters'},
            'Film': {"url": '/l/Photography/Camera-Accessories/Film'},
            'Gimbals': {"url": '/l/Photography/Camera-Accessories/Gimbals'},
            'Gloves': {"url": '/l/Photography/Camera-Accessories/Gloves'},
            'Light-Meters': {"url": '/l/Photography/Camera-Accessories/Light-Meters'},
            'Memory-Cards': {"url": '/l/Photography/Camera-Accessories/Memory-Cards'},
            'Remote-Controls': {"url": '/l/Photography/Camera-Accessories/Remote-Controls'},
            'Screen-Protectors': {"url": '/l/Photography/Camera-Accessories/Screen-Protectors'},
            'Specialty-Camera-Accessories': {"url": '/l/Photography/Camera-Accessories/Specialty-Camera-Accessories'},
            'Tripods-and-Supports': {"url": '/l/Photography/Camera-Accessories/Tripods-and-Supports'},
            'Vests': {"url": '/l/Photography/Camera-Accessories/Vests'},
            'Viewfinders-and-Eyepieces': {"url": '/l/Photography/Camera-Accessories/Viewfinders-and-Eyepieces'},
            'White-Balance-and-Color-Calibration': {"url": '/l/Photography/Camera-Accessories/White-Balance-and-Color-Calibration'}
        }},
        'Cameras': {"url": '/l/Photography/Cameras', "subcategories": {
            'Digital-Point-and-Shoot-Cameras': {"url": '/l/Photography/Cameras/Digital-Point-and-Shoot-Cameras'},
            'Digital-SLR-Cameras': {"url": '/l/Photography/Cameras/Digital-SLR-Cameras'},
            'Film-Cameras': {"url": '/l/Photography/Cameras/Film-Cameras'},
            'Instant-Cameras': {"url": '/l/Photography/Cameras/Instant-Cameras'},
            'Medium-Format-Cameras': {"url": '/l/Photography/Cameras/Medium-Format-Cameras'},
            'Mirrorless-Cameras': {"url": '/l/Photography/Cameras/Mirrorless-Cameras'}
        }},
        'Film-and-Darkroom-Equipment': {"url": '/l/Photography/Film-and-Darkroom-Equipment', "subcategories": {
            'Darkroom-Chemicals': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Darkroom-Chemicals', "subcategories": {
                'Black-and-White-Chemicals': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Darkroom-Chemicals/Black-and-White-Chemicals'},
                'Color-Chemicals': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Darkroom-Chemicals/Color-Chemicals'},
                'Toners': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Darkroom-Chemicals/Toners'}
            }},
            'Darkroom-Setup': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Darkroom-Setup'},
            'Developing-and-Processing': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Developing-and-Processing', "subcategories": {
                'Chemical-Storage': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Developing-and-Processing/Chemical-Storage'},
                'Developing-Tanks-and-Reels': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Developing-and-Processing/Developing-Tanks-and-Reels'},
                'Developing-Trays': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Developing-and-Processing/Developing-Trays'},
                'Loupes-and-Magnifiers': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Developing-and-Processing/Loupes-and-Magnifiers'},
                'Retouching': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Developing-and-Processing/Retouching'},
                'Washing-and-Drying-Aids': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Developing-and-Processing/Washing-and-Drying-Aids'}
            }},
            'Enlarger-Accessories': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Enlarger-Accessories'},
            'Enlargers': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Enlargers'},
            'Enlarging-Paper': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Enlarging-Paper', "subcategories": {
                'Black-and-White-Paper': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Enlarging-Paper/Black-and-White-Paper'},
                'Color-Paper': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Enlarging-Paper/Color-Paper'}
            }},
            'Film': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Film', "subcategories": {
                '120-Film': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Film/120-Film'},
                '35mm-Film': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Film/35mm-Film'},
                'Film-Accessories': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Film/Film-Accessories'},
                'Instant-Film': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Film/Instant-Film'},
                'Motion-Picture-Film': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Film/Motion-Picture-Film'},
                'Sheet-Film': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Film/Sheet-Film'}
            }},
            'Lightboxes-and-Accessories': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Lightboxes-and-Accessories', "subcategories": {
                'Lightbox-Accessories': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Lightboxes-and-Accessories/Lightbox-Accessories'},
                'Lightboxes': {"url": '/l/Photography/Film-and-Darkroom-Equipment/Lightboxes-and-Accessories/Lightboxes'}
            }}
        }},
        'Lens-Accessories': {"url": '/l/Photography/Lens-Accessories', "subcategories": {
            'Conversion-Lenses': {"url": '/l/Photography/Lens-Accessories/Conversion-Lenses'},
            'Extension-Tubes': {"url": '/l/Photography/Lens-Accessories/Extension-Tubes'},
            'Lens-Bumpers': {"url": '/l/Photography/Lens-Accessories/Lens-Bumpers'},
            'Lens-Caps': {"url": '/l/Photography/Lens-Accessories/Lens-Caps'},
            'Lens-Covers': {"url": '/l/Photography/Lens-Accessories/Lens-Covers'},
            'Lens-Hoods': {"url": '/l/Photography/Lens-Accessories/Lens-Hoods'},
            'Lens-Supports': {"url": '/l/Photography/Lens-Accessories/Lens-Supports'},
            'Point-and-Shoot-Add-hyphen-On-Lenses': {"url": '/l/Photography/Lens-Accessories/Point-and-Shoot-Add-hyphen-On-Lenses'},
            'Reversing-Rings': {"url": '/l/Photography/Lens-Accessories/Reversing-Rings'},
            'Teleconverters': {"url": '/l/Photography/Lens-Accessories/Teleconverters'}
        }},
        'Lens-Filters': {"url": '/l/Photography/Lens-Filters', "subcategories": {
            'Black-and-White-Contrast-Filters': {"url": '/l/Photography/Lens-Filters/Black-and-White-Contrast-Filters'},
            'Close-Up-Lens-Filters': {"url": '/l/Photography/Lens-Filters/Close-Up-Lens-Filters'},
            'Color-Compensating-Filters': {"url": '/l/Photography/Lens-Filters/Color-Compensating-Filters'},
            'Color-Conversion-Filters': {"url": '/l/Photography/Lens-Filters/Color-Conversion-Filters'},
            'Filter-Accessories': {"url": '/l/Photography/Lens-Filters/Filter-Accessories', "subcategories": {
                'Filter-Adapters': {"url": '/l/Photography/Lens-Filters/Filter-Accessories/Filter-Adapters'},
                'Filter-Caps': {"url": '/l/Photography/Lens-Filters/Filter-Accessories/Filter-Caps'},
                'Filter-Holders': {"url": '/l/Photography/Lens-Filters/Filter-Accessories/Filter-Holders'},
                'Step-Down-Rings': {"url": '/l/Photography/Lens-Filters/Filter-Accessories/Step-Down-Rings'},
                'Step-Up-Rings': {"url": '/l/Photography/Lens-Filters/Filter-Accessories/Step-Up-Rings'}
            }},
            'Filter-Kits': {"url": '/l/Photography/Lens-Filters/Filter-Kits'},
            'Image-Softening-Filters': {"url": '/l/Photography/Lens-Filters/Image-Softening-Filters'},
            'Infrared-Filters': {"url": '/l/Photography/Lens-Filters/Infrared-Filters'},
            'Neutral-Density-Filters': {"url": '/l/Photography/Lens-Filters/Neutral-Density-Filters'},
            'Polarizing-Filters': {"url": '/l/Photography/Lens-Filters/Polarizing-Filters'},
            'Protective-Filters-hyphen-UV-and-Clear': {"url": '/l/Photography/Lens-Filters/Protective-Filters-hyphen-UV-and-Clear'},
            'Special-Effect-Filters': {"url": '/l/Photography/Lens-Filters/Special-Effect-Filters'},
            'Underwater-Filters': {"url": '/l/Photography/Lens-Filters/Underwater-Filters'},
            'Viewing-Filters': {"url": '/l/Photography/Lens-Filters/Viewing-Filters'}
        }},
        'Lenses': {"url": '/l/Photography/Lenses', "subcategories": {
            'Lens-Mount-Adapters': {"url": '/l/Photography/Lenses/Lens-Mount-Adapters'},
            'Lens-Warranties': {"url": '/l/Photography/Lenses/Lens-Warranties'},
            'Medium-Format-Lenses': {"url": '/l/Photography/Lenses/Medium-Format-Lenses'},
            'Mirrorless-Lenses': {"url": '/l/Photography/Lenses/Mirrorless-Lenses'},
            'Rangefinder-Lenses': {"url": '/l/Photography/Lenses/Rangefinder-Lenses'},
            'SLR-Lenses': {"url": '/l/Photography/Lenses/SLR-Lenses'},
            'Specialty-Lenses': {"url": '/l/Photography/Lenses/Specialty-Lenses'}
        }},
        'Lighting-and-Studio': {"url": '/l/Photography/Lighting-and-Studio', "subcategories": {
            'Backgrounds-and-Supports': {"url": '/l/Photography/Lighting-and-Studio/Backgrounds-and-Supports', "subcategories": {
                'Background-Supports-and-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Backgrounds-and-Supports/Background-Supports-and-Accessories', "subcategories": {
                    'Background-Support': {"url": '/l/Photography/Lighting-and-Studio/Backgrounds-and-Supports/Background-Supports-and-Accessories/Background-Support'},
                    'Background-Support-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Backgrounds-and-Supports/Background-Supports-and-Accessories/Background-Support-Accessories'}
                }},
                'Chroma-Key-Backgrounds': {"url": '/l/Photography/Lighting-and-Studio/Backgrounds-and-Supports/Chroma-Key-Backgrounds'},
                'Collapsible-Backgrounds': {"url": '/l/Photography/Lighting-and-Studio/Backgrounds-and-Supports/Collapsible-Backgrounds'},
                'Fabric-Backgrounds': {"url": '/l/Photography/Lighting-and-Studio/Backgrounds-and-Supports/Fabric-Backgrounds'},
                'Floor-Drops': {"url": '/l/Photography/Lighting-and-Studio/Backgrounds-and-Supports/Floor-Drops'},
                'Seamless-Paper-Backgrounds': {"url": '/l/Photography/Lighting-and-Studio/Backgrounds-and-Supports/Seamless-Paper-Backgrounds'},
                'Vinyl-Backgrounds': {"url": '/l/Photography/Lighting-and-Studio/Backgrounds-and-Supports/Vinyl-Backgrounds'}
            }},
            'Continuous-Lighting': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting', "subcategories": {
                'Fluorescent-Lighting': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting/Fluorescent-Lighting'},
                'LED-Lighting': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting/LED-Lighting', "subcategories": {
                    'Fresnels': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting/LED-Lighting/Fresnels'},
                    'Light-Panels': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting/LED-Lighting/Light-Panels'},
                    'Light-Wands-and-Tubes': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting/LED-Lighting/Light-Wands-and-Tubes'},
                    'Monolight-Style': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting/LED-Lighting/Monolight-Style'},
                    'Ring-Lights': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting/LED-Lighting/Ring-Lights'},
                    'Special-Application-Lighting': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting/LED-Lighting/Special-Application-Lighting'},
                    'Strip-Lights': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting/LED-Lighting/Strip-Lights'}
                }},
                'PAR-Lights': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting/PAR-Lights'},
                'Spotlights': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting/Spotlights'},
                'Tungsten-Lighting': {"url": '/l/Photography/Lighting-and-Studio/Continuous-Lighting/Tungsten-Lighting'}
            }},
            'Flashes-and-On-hyphen-Camera-Lighting': {"url": '/l/Photography/Lighting-and-Studio/Flashes-and-On-hyphen-Camera-Lighting', "subcategories": {
                'Flash-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Flashes-and-On-hyphen-Camera-Lighting/Flash-Accessories', "subcategories": {
                    'Barebulb-Flash-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Flashes-and-On-hyphen-Camera-Lighting/Flash-Accessories/Barebulb-Flash-Accessories'},
                    'Camera-Flash-Brackets': {"url": '/l/Photography/Lighting-and-Studio/Flashes-and-On-hyphen-Camera-Lighting/Flash-Accessories/Camera-Flash-Brackets'},
                    'Flash-Batteries': {"url": '/l/Photography/Lighting-and-Studio/Flashes-and-On-hyphen-Camera-Lighting/Flash-Accessories/Flash-Batteries'},
                    'Flash-Battery-Chargers': {"url": '/l/Photography/Lighting-and-Studio/Flashes-and-On-hyphen-Camera-Lighting/Flash-Accessories/Flash-Battery-Chargers'},
                    'Flash-Bounce-and-Diffusers': {"url": '/l/Photography/Lighting-and-Studio/Flashes-and-On-hyphen-Camera-Lighting/Flash-Accessories/Flash-Bounce-and-Diffusers'},
                    'Flash-Cables-and-Adapters': {"url": '/l/Photography/Lighting-and-Studio/Flashes-and-On-hyphen-Camera-Lighting/Flash-Accessories/Flash-Cables-and-Adapters'},
                    'Flash-Tube-Covers': {"url": '/l/Photography/Lighting-and-Studio/Flashes-and-On-hyphen-Camera-Lighting/Flash-Accessories/Flash-Tube-Covers'},
                    'PC-Sync-Cords': {"url": '/l/Photography/Lighting-and-Studio/Flashes-and-On-hyphen-Camera-Lighting/Flash-Accessories/PC-Sync-Cords'}
                }},
                'Macro-Flashes-and-Ringlights': {"url": '/l/Photography/Lighting-and-Studio/Flashes-and-On-hyphen-Camera-Lighting/Macro-Flashes-and-Ringlights'},
                'On-Camera-Flashes': {"url": '/l/Photography/Lighting-and-Studio/Flashes-and-On-hyphen-Camera-Lighting/On-Camera-Flashes'}
            }},
            'Flashtubes-and-Lamps': {"url": '/l/Photography/Lighting-and-Studio/Flashtubes-and-Lamps', "subcategories": {
                'Flashtubes': {"url": '/l/Photography/Lighting-and-Studio/Flashtubes-and-Lamps/Flashtubes'},
                'Lamps': {"url": '/l/Photography/Lighting-and-Studio/Flashtubes-and-Lamps/Lamps'}
            }},
            'Light-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Light-Accessories', "subcategories": {
                'Remotes-and-Light-Controllers': {"url": '/l/Photography/Lighting-and-Studio/Light-Accessories/Remotes-and-Light-Controllers'},
                'Safety-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Light-Accessories/Safety-Accessories'},
                'Socket-and-Cord-Sets': {"url": '/l/Photography/Lighting-and-Studio/Light-Accessories/Socket-and-Cord-Sets'}
            }},
            'Light-Modifiers-and-Reflectors': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors', "subcategories": {
                'Butterflies-and-Panels': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Butterflies-and-Panels', "subcategories": {
                    'Butterfly-and-Panel-Reflector-Fabrics': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Butterflies-and-Panels/Butterfly-and-Panel-Reflector-Fabrics'},
                    'Butterfly-and-Panel-Reflector-Kits': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Butterflies-and-Panels/Butterfly-and-Panel-Reflector-Kits'},
                    'Collapsible-Reflectors': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Butterflies-and-Panels/Collapsible-Reflectors'},
                    'Reflector-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Butterflies-and-Panels/Reflector-Accessories'},
                    'Reflector-Boards': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Butterflies-and-Panels/Reflector-Boards'}
                }},
                'Cucoloris-comma-Fingers-and-Dots': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Cucoloris-comma-Fingers-and-Dots'},
                'Fabric-Scrims': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Fabric-Scrims'},
                'Lenses-and-Gobos': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Lenses-and-Gobos'},
                'Light-Control-Flags-and-Cutters': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Light-Control-Flags-and-Cutters'},
                'Lighting-Gels-and-Diffusion': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Lighting-Gels-and-Diffusion', "subcategories": {
                    'Color-Correction-Filters-and-Gels': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Lighting-Gels-and-Diffusion/Color-Correction-Filters-and-Gels'},
                    'Color-Effects-Filters-and-Gels': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Lighting-Gels-and-Diffusion/Color-Effects-Filters-and-Gels'},
                    'Diffusers-and-Diffusion-Material': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Lighting-Gels-and-Diffusion/Diffusers-and-Diffusion-Material'},
                    'Frames-and-Holders': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Lighting-Gels-and-Diffusion/Frames-and-Holders'}
                }},
                'Reflectors-and-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Reflectors-and-Accessories', "subcategories": {
                    'Barndoors': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Reflectors-and-Accessories/Barndoors'},
                    'Honeycomb-and-Grids': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Reflectors-and-Accessories/Honeycomb-and-Grids'},
                    'Reflectors': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Reflectors-and-Accessories/Reflectors'},
                    'Snoots': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Reflectors-and-Accessories/Snoots'}
                }},
                'Softboxes-and-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Softboxes-and-Accessories', "subcategories": {
                    'Softbox-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Softboxes-and-Accessories/Softbox-Accessories'},
                    'Softboxes': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Softboxes-and-Accessories/Softboxes'}
                }},
                'Speed-Rings-and-Adapters': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Speed-Rings-and-Adapters'},
                'Umbrellas-and-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Umbrellas-and-Accessories', "subcategories": {
                    'Umbrella-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Umbrellas-and-Accessories/Umbrella-Accessories'},
                    'Umbrella-Mounts': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Umbrellas-and-Accessories/Umbrella-Mounts'},
                    'Umbrellas': {"url": '/l/Photography/Lighting-and-Studio/Light-Modifiers-and-Reflectors/Umbrellas-and-Accessories/Umbrellas'}
                }}
            }},
            'Light-Stands-and-Mounting': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting', "subcategories": {
                'Grips-comma-Clamps-and-Arms': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Grips-comma-Clamps-and-Arms', "subcategories": {
                    'Arms': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Grips-comma-Clamps-and-Arms/Arms'},
                    'Clamps': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Grips-comma-Clamps-and-Arms/Clamps'},
                    'Grips-Heads': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Grips-comma-Clamps-and-Arms/Grips-Heads'}
                }},
                'Light-Booms-and-Stands': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Light-Booms-and-Stands'},
                'Light-Stand-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Light-Stand-Accessories', "subcategories": {
                    'Adapters': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Light-Stand-Accessories/Adapters'},
                    'Casters-and-Wheels': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Light-Stand-Accessories/Casters-and-Wheels'},
                    'Columns-and-Risers': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Light-Stand-Accessories/Columns-and-Risers'},
                    'Light-Stand-Bases': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Light-Stand-Accessories/Light-Stand-Bases'},
                    'Light-Stand-Extensions': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Light-Stand-Accessories/Light-Stand-Extensions'},
                    'Special-Accessory': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Light-Stand-Accessories/Special-Accessory'},
                    'Weight-Bags': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Light-Stand-Accessories/Weight-Bags'}
                }},
                'Mounting-Hardware': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Mounting-Hardware'},
                'Railing-Systems-and-Components': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Railing-Systems-and-Components'},
                'Trussing-Equipment': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Trussing-Equipment'},
                'Umbrella-Mounts': {"url": '/l/Photography/Lighting-and-Studio/Light-Stands-and-Mounting/Umbrella-Mounts'}
            }},
            'Lighting-Power-and-Cables': {"url": '/l/Photography/Lighting-and-Studio/Lighting-Power-and-Cables', "subcategories": {
                'AC-Power-Supplies': {"url": '/l/Photography/Lighting-and-Studio/Lighting-Power-and-Cables/AC-Power-Supplies'},
                'Battery-Adapter-Plates': {"url": '/l/Photography/Lighting-and-Studio/Lighting-Power-and-Cables/Battery-Adapter-Plates'},
                'Cables': {"url": '/l/Photography/Lighting-and-Studio/Lighting-Power-and-Cables/Cables'},
                'DC-Power-Supplies': {"url": '/l/Photography/Lighting-and-Studio/Lighting-Power-and-Cables/DC-Power-Supplies'},
                'Lighting-Batteries': {"url": '/l/Photography/Lighting-and-Studio/Lighting-Power-and-Cables/Lighting-Batteries'},
                'Lighting-Chargers': {"url": '/l/Photography/Lighting-and-Studio/Lighting-Power-and-Cables/Lighting-Chargers'},
                'Power-Adapters': {"url": '/l/Photography/Lighting-and-Studio/Lighting-Power-and-Cables/Power-Adapters'},
                'Power-Inverters': {"url": '/l/Photography/Lighting-and-Studio/Lighting-Power-and-Cables/Power-Inverters'},
                'Power-Pack-Strobes': {"url": '/l/Photography/Lighting-and-Studio/Lighting-Power-and-Cables/Power-Pack-Strobes'}
            }},
            'Monolights-and-Strobes': {"url": '/l/Photography/Lighting-and-Studio/Monolights-and-Strobes', "subcategories": {
                'Camera-and-Flash-Triggers': {"url": '/l/Photography/Lighting-and-Studio/Monolights-and-Strobes/Camera-and-Flash-Triggers'},
                'Monolight-Batteries': {"url": '/l/Photography/Lighting-and-Studio/Monolights-and-Strobes/Monolight-Batteries'},
                'Monolights': {"url": '/l/Photography/Lighting-and-Studio/Monolights-and-Strobes/Monolights'},
                'Power-Pack-Strobes': {"url": '/l/Photography/Lighting-and-Studio/Monolights-and-Strobes/Power-Pack-Strobes'},
                'Replacement-Parts-and-Fuses': {"url": '/l/Photography/Lighting-and-Studio/Monolights-and-Strobes/Replacement-Parts-and-Fuses'}
            }},
            'Optical-Triggers': {"url": '/l/Photography/Lighting-and-Studio/Optical-Triggers', "subcategories": {
                'Camera-and-Flash-Trigger-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Optical-Triggers/Camera-and-Flash-Trigger-Accessories'},
                'Camera-and-Flash-Triggers': {"url": '/l/Photography/Lighting-and-Studio/Optical-Triggers/Camera-and-Flash-Triggers'},
                'Light-Meters': {"url": '/l/Photography/Lighting-and-Studio/Optical-Triggers/Light-Meters'}
            }},
            'Studio-Equipment': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment', "subcategories": {
                'Apple-Boxes': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment/Apple-Boxes'},
                'Gaffer-Tape': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment/Gaffer-Tape'},
                'Paints-and-Scenic-Treatments': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment/Paints-and-Scenic-Treatments'},
                'Posing-Equipment': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment/Posing-Equipment'},
                'Props-and-Special-Effects': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment/Props-and-Special-Effects'},
                'Tabletop-Shooting': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment/Tabletop-Shooting', "subcategories": {
                    'Copy-Stands-and-Lights': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment/Tabletop-Shooting/Copy-Stands-and-Lights'},
                    'Product-Turntables': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment/Tabletop-Shooting/Product-Turntables'},
                    'Shooting-Tables': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment/Tabletop-Shooting/Shooting-Tables'},
                    'Shooting-Tents': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment/Tabletop-Shooting/Shooting-Tents'},
                    'Table-and-Tent-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment/Tabletop-Shooting/Table-and-Tent-Accessories'},
                    'Turntable-Accessories': {"url": '/l/Photography/Lighting-and-Studio/Studio-Equipment/Tabletop-Shooting/Turntable-Accessories'}
                }}
            }}
        }},
        'Mobile-Photography': {"url": '/l/Photography/Mobile-Photography', "subcategories": {
            'Mobile-Photography-Lenses-and-Adapters': {"url": '/l/Photography/Mobile-Photography/Mobile-Photography-Lenses-and-Adapters'},
            'Mobile-Photography-Lighting': {"url": '/l/Photography/Mobile-Photography/Mobile-Photography-Lighting'},
            'Mobile-Photography-Support': {"url": '/l/Photography/Mobile-Photography/Mobile-Photography-Support'},
            'Smartphone-Microphones': {"url": '/l/Photography/Mobile-Photography/Smartphone-Microphones'}
        }},
        'Photo-Albums-comma-Frames-and-Storage': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage', "subcategories": {
            'Archival-Storage': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Archival-Storage', "subcategories": {
                'Archival-Storage-Accessories': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Archival-Storage/Archival-Storage-Accessories'},
                'Archival-Tissue-Paper': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Archival-Storage/Archival-Tissue-Paper'},
                'Disc-Cases-comma-Sleeves-and-Storage': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Archival-Storage/Disc-Cases-comma-Sleeves-and-Storage'},
                'Print-and-Document-Storage-Boxes': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Archival-Storage/Print-and-Document-Storage-Boxes'},
                'Safe-and-Lock-Boxes': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Archival-Storage/Safe-and-Lock-Boxes'},
                'Slide-and-Negatives-Storage': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Archival-Storage/Slide-and-Negatives-Storage'},
                'Storage-Boxes': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Archival-Storage/Storage-Boxes'},
                'Storage-Envelopes-and-Protectors': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Archival-Storage/Storage-Envelopes-and-Protectors'}
            }},
            'Custom-Photo-Products': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Custom-Photo-Products', "subcategories": {
                'Custom-Photo-Books-and-Albums': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Custom-Photo-Products/Custom-Photo-Books-and-Albums'},
                'Custom-Photo-Prints': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Custom-Photo-Products/Custom-Photo-Prints'}
            }},
            'Cutting-comma-Mounting-comma-and-Laminating': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Cutting-comma-Mounting-comma-and-Laminating', "subcategories": {
                'Cutters-and-Trimmers': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Cutting-comma-Mounting-comma-and-Laminating/Cutters-and-Trimmers', "subcategories": {
                    'Blades-and-Accessories': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Cutting-comma-Mounting-comma-and-Laminating/Cutters-and-Trimmers/Blades-and-Accessories'},
                    'Cutters': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Cutting-comma-Mounting-comma-and-Laminating/Cutters-and-Trimmers/Cutters'},
                    'Handheld-Knives': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Cutting-comma-Mounting-comma-and-Laminating/Cutters-and-Trimmers/Handheld-Knives'}
                }},
                'Laminating': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Cutting-comma-Mounting-comma-and-Laminating/Laminating', "subcategories": {
                    'Laminating-Accessories': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Cutting-comma-Mounting-comma-and-Laminating/Laminating/Laminating-Accessories'},
                    'Laminating-Machines': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Cutting-comma-Mounting-comma-and-Laminating/Laminating/Laminating-Machines'}
                }},
                'Picture-Mounting': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Cutting-comma-Mounting-comma-and-Laminating/Picture-Mounting', "subcategories": {
                    'Mat-Boards': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Cutting-comma-Mounting-comma-and-Laminating/Picture-Mounting/Mat-Boards'},
                    'Mounting-Tape': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Cutting-comma-Mounting-comma-and-Laminating/Picture-Mounting/Mounting-Tape'},
                    'Mounting-Tissue': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Cutting-comma-Mounting-comma-and-Laminating/Picture-Mounting/Mounting-Tissue'}
                }}
            }},
            'Frames': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Frames', "subcategories": {
                'Digital-Picture-Frames': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Frames/Digital-Picture-Frames'},
                'Framing-Accessories': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Frames/Framing-Accessories'},
                'Picture-Frames': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Frames/Picture-Frames'}
            }},
            'Photo-Albums-and-Album-Accessories': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Photo-Albums-and-Album-Accessories', "subcategories": {
                'Photo-Album-Accessories': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Photo-Albums-and-Album-Accessories/Photo-Album-Accessories'},
                'Photo-Albums': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Photo-Albums-and-Album-Accessories/Photo-Albums'},
                'Scrapbook-Accessories': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Photo-Albums-and-Album-Accessories/Scrapbook-Accessories'},
                'Scrapbooks': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Photo-Albums-and-Album-Accessories/Scrapbooks'}
            }},
            'Portfolios-and-Binders': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Portfolios-and-Binders', "subcategories": {
                'Folios-and-Folders': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Portfolios-and-Binders/Folios-and-Folders'},
                'Portfolio-Binder-Accessories': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Portfolios-and-Binders/Portfolio-Binder-Accessories'},
                'Presentation-Binders-and-Cases': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Portfolios-and-Binders/Presentation-Binders-and-Cases'},
                'Presentation-Books-and-Binders': {"url": '/l/Photography/Photo-Albums-comma-Frames-and-Storage/Portfolios-and-Binders/Presentation-Books-and-Binders'}
            }}
        }},
        'Photography-Bags-and-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases', "subcategories": {
            'Bag-and-Case-Accessories': {"url": '/l/Photography/Photography-Bags-and-Cases/Bag-and-Case-Accessories', "subcategories": {
                'Clips-and-Connectors': {"url": '/l/Photography/Photography-Bags-and-Cases/Bag-and-Case-Accessories/Clips-and-Connectors'},
                'Dividers': {"url": '/l/Photography/Photography-Bags-and-Cases/Bag-and-Case-Accessories/Dividers'},
                'Foam': {"url": '/l/Photography/Photography-Bags-and-Cases/Bag-and-Case-Accessories/Foam'},
                'Hard-Case-Accessories-and-Parts': {"url": '/l/Photography/Photography-Bags-and-Cases/Bag-and-Case-Accessories/Hard-Case-Accessories-and-Parts'},
                'Inserts': {"url": '/l/Photography/Photography-Bags-and-Cases/Bag-and-Case-Accessories/Inserts'},
                'Luggage-and-Case-Locks': {"url": '/l/Photography/Photography-Bags-and-Cases/Bag-and-Case-Accessories/Luggage-and-Case-Locks'},
                'Organizers': {"url": '/l/Photography/Photography-Bags-and-Cases/Bag-and-Case-Accessories/Organizers'},
                'Photography-Belts-and-Harnesses': {"url": '/l/Photography/Photography-Bags-and-Cases/Bag-and-Case-Accessories/Photography-Belts-and-Harnesses'},
                'Pockets': {"url": '/l/Photography/Photography-Bags-and-Cases/Bag-and-Case-Accessories/Pockets'}
            }},
            'Belt-Pouches': {"url": '/l/Photography/Photography-Bags-and-Cases/Belt-Pouches'},
            'Camera-Bags-and-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Camera-Bags-and-Cases', "subcategories": {
                'Camera-Backpacks': {"url": '/l/Photography/Photography-Bags-and-Cases/Camera-Bags-and-Cases/Camera-Backpacks'},
                'Camera-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Camera-Bags-and-Cases/Camera-Cases'},
                'Camera-Insert-Bags': {"url": '/l/Photography/Photography-Bags-and-Cases/Camera-Bags-and-Cases/Camera-Insert-Bags'},
                'Camera-Shoulder-Bags': {"url": '/l/Photography/Photography-Bags-and-Cases/Camera-Bags-and-Cases/Camera-Shoulder-Bags'},
                'Camera-Sling-Bags': {"url": '/l/Photography/Photography-Bags-and-Cases/Camera-Bags-and-Cases/Camera-Sling-Bags'},
                'Camera-Waist-Packs': {"url": '/l/Photography/Photography-Bags-and-Cases/Camera-Bags-and-Cases/Camera-Waist-Packs'},
                'Rolling-Camera-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Camera-Bags-and-Cases/Rolling-Camera-Cases'}
            }},
            'Camera-Rain-Covers': {"url": '/l/Photography/Photography-Bags-and-Cases/Camera-Rain-Covers'},
            'Duffel-Bags': {"url": '/l/Photography/Photography-Bags-and-Cases/Duffel-Bags'},
            'Hard-Shell-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Hard-Shell-Cases'},
            'Lens-and-Filter-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Lens-and-Filter-Cases', "subcategories": {
                'Filter-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Lens-and-Filter-Cases/Filter-Cases'},
                'Lens-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Lens-and-Filter-Cases/Lens-Cases'}
            }},
            'Lighting-Bags-and-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Lighting-Bags-and-Cases', "subcategories": {
                'Flash-Bags-and-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Lighting-Bags-and-Cases/Flash-Bags-and-Cases'},
                'Light-Stand-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Lighting-Bags-and-Cases/Light-Stand-Cases'},
                'Lighting-Accessory-Bags-and-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Lighting-Bags-and-Cases/Lighting-Accessory-Bags-and-Cases'},
                'Lighting-System-Bags-and-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Lighting-Bags-and-Cases/Lighting-System-Bags-and-Cases'}
            }},
            'Luggage': {"url": '/l/Photography/Photography-Bags-and-Cases/Luggage'},
            'Protective-Wraps': {"url": '/l/Photography/Photography-Bags-and-Cases/Protective-Wraps'},
            'Straps-and-Slings': {"url": '/l/Photography/Photography-Bags-and-Cases/Straps-and-Slings', "subcategories": {
                'Bag-and-Case-Straps': {"url": '/l/Photography/Photography-Bags-and-Cases/Straps-and-Slings/Bag-and-Case-Straps'},
                'Camera-Straps': {"url": '/l/Photography/Photography-Bags-and-Cases/Straps-and-Slings/Camera-Straps'},
                'Strap-Accessories': {"url": '/l/Photography/Photography-Bags-and-Cases/Straps-and-Slings/Strap-Accessories'},
                'Strap-and-Sling-Pads': {"url": '/l/Photography/Photography-Bags-and-Cases/Straps-and-Slings/Strap-and-Sling-Pads'},
                'Tripod-Straps': {"url": '/l/Photography/Photography-Bags-and-Cases/Straps-and-Slings/Tripod-Straps'}
            }},
            'Tripod-Cases': {"url": '/l/Photography/Photography-Bags-and-Cases/Tripod-Cases'}
        }},
        'Photography-Guides-and-Tutorials': {"url": '/l/Photography/Photography-Guides-and-Tutorials'},
        'Tripods-and-Supports': {"url": '/l/Photography/Tripods-and-Supports', "subcategories": {
            'Monopods-and-Accessories': {"url": '/l/Photography/Tripods-and-Supports/Monopods-and-Accessories', "subcategories": {
                'Monopod-Accessories': {"url": '/l/Photography/Tripods-and-Supports/Monopods-and-Accessories/Monopod-Accessories'},
                'Monopods': {"url": '/l/Photography/Tripods-and-Supports/Monopods-and-Accessories/Monopods'}
            }},
            'Mounts-and-Supports': {"url": '/l/Photography/Tripods-and-Supports/Mounts-and-Supports', "subcategories": {
                'Car-Mounts': {"url": '/l/Photography/Tripods-and-Supports/Mounts-and-Supports/Car-Mounts'},
                'Clamp-and-Screw-Mounts': {"url": '/l/Photography/Tripods-and-Supports/Mounts-and-Supports/Clamp-and-Screw-Mounts'},
                'Hi-Hat-Mounts': {"url": '/l/Photography/Tripods-and-Supports/Mounts-and-Supports/Hi-Hat-Mounts'},
                'Magnetic-Mounts': {"url": '/l/Photography/Tripods-and-Supports/Mounts-and-Supports/Magnetic-Mounts'},
                'Suction-Mounts': {"url": '/l/Photography/Tripods-and-Supports/Mounts-and-Supports/Suction-Mounts'}
            }},
            'Quick-Release': {"url": '/l/Photography/Tripods-and-Supports/Quick-Release', "subcategories": {
                'L-hyphen-Brackets': {"url": '/l/Photography/Tripods-and-Supports/Quick-Release/L-hyphen-Brackets'},
                'Quick-Release-Accessories': {"url": '/l/Photography/Tripods-and-Supports/Quick-Release/Quick-Release-Accessories'},
                'Quick-Release-Clamps': {"url": '/l/Photography/Tripods-and-Supports/Quick-Release/Quick-Release-Clamps'},
                'Quick-Release-Plates': {"url": '/l/Photography/Tripods-and-Supports/Quick-Release/Quick-Release-Plates'},
                'Quick-Release-Systems': {"url": '/l/Photography/Tripods-and-Supports/Quick-Release/Quick-Release-Systems'}
            }},
            'Tripod-Cases': {"url": '/l/Photography/Tripods-and-Supports/Tripod-Cases'},
            'Tripod-Heads': {"url": '/l/Photography/Tripods-and-Supports/Tripod-Heads', "subcategories": {
                'Ball-Heads': {"url": '/l/Photography/Tripods-and-Supports/Tripod-Heads/Ball-Heads'},
                'Gimbal-Heads': {"url": '/l/Photography/Tripods-and-Supports/Tripod-Heads/Gimbal-Heads'},
                'Pan-and-Tilt-Heads': {"url": '/l/Photography/Tripods-and-Supports/Tripod-Heads/Pan-and-Tilt-Heads'},
                'Panoramic-and-Rotator-Heads': {"url": '/l/Photography/Tripods-and-Supports/Tripod-Heads/Panoramic-and-Rotator-Heads'},
                'Pistol-Grip-Heads': {"url": '/l/Photography/Tripods-and-Supports/Tripod-Heads/Pistol-Grip-Heads'},
                'Tripod-Head-Accessories': {"url": '/l/Photography/Tripods-and-Supports/Tripod-Heads/Tripod-Head-Accessories'},
                'Video-Heads': {"url": '/l/Photography/Tripods-and-Supports/Tripod-Heads/Video-Heads'}
            }},
            'Tripods': {"url": '/l/Photography/Tripods-and-Supports/Tripods', "subcategories": {
                'Photo-Tripods': {"url": '/l/Photography/Tripods-and-Supports/Tripods/Photo-Tripods'},
                'Tripod-Accessories': {"url": '/l/Photography/Tripods-and-Supports/Tripods/Tripod-Accessories'},
                'Tripod-Legs': {"url": '/l/Photography/Tripods-and-Supports/Tripods/Tripod-Legs'},
                'Video-Tripods': {"url": '/l/Photography/Tripods-and-Supports/Tripods/Video-Tripods'}
            }}
        }},
        'Underwater-Photography': {"url": '/l/Photography/Underwater-Photography', "subcategories": {
            'Underwater-Arms-comma-Brackets-and-Handles': {"url": '/l/Photography/Underwater-Photography/Underwater-Arms-comma-Brackets-and-Handles'},
            'Underwater-Camera-Housings': {"url": '/l/Photography/Underwater-Photography/Underwater-Camera-Housings', "subcategories": {
                'Camera-Housings': {"url": '/l/Photography/Underwater-Photography/Underwater-Camera-Housings/Camera-Housings'}
            }},
            'Underwater-Cameras': {"url": '/l/Photography/Underwater-Photography/Underwater-Cameras'},
            'Underwater-Lenses-and-Accessories': {"url": '/l/Photography/Underwater-Photography/Underwater-Lenses-and-Accessories', "subcategories": {
                'Underwater-Lens-Ports': {"url": '/l/Photography/Underwater-Photography/Underwater-Lenses-and-Accessories/Underwater-Lens-Ports'},
                'Underwater-Lens-and-Lens-Port-Accessories': {"url": '/l/Photography/Underwater-Photography/Underwater-Lenses-and-Accessories/Underwater-Lens-and-Lens-Port-Accessories'}
            }},
            'Underwater-Lighting-and-Strobes': {"url": '/l/Photography/Underwater-Photography/Underwater-Lighting-and-Strobes', "subcategories": {
                'Dive-Lights': {"url": '/l/Photography/Underwater-Photography/Underwater-Lighting-and-Strobes/Dive-Lights'},
                'Underwater-Lighting-Accessories': {"url": '/l/Photography/Underwater-Photography/Underwater-Lighting-and-Strobes/Underwater-Lighting-Accessories'}
            }},
            'Underwater-Photography-Accessories': {"url": '/l/Photography/Underwater-Photography/Underwater-Photography-Accessories', "subcategories": {
                'Buoyancy-Weights': {"url": '/l/Photography/Underwater-Photography/Underwater-Photography-Accessories/Buoyancy-Weights'},
                'Connecting-Cords': {"url": '/l/Photography/Underwater-Photography/Underwater-Photography-Accessories/Connecting-Cords'},
                'Replacement-Parts': {"url": '/l/Photography/Underwater-Photography/Underwater-Photography-Accessories/Replacement-Parts'},
                'Screen-Protection-and-Covers': {"url": '/l/Photography/Underwater-Photography/Underwater-Photography-Accessories/Screen-Protection-and-Covers'},
                'Trays-and-Handles': {"url": '/l/Photography/Underwater-Photography/Underwater-Photography-Accessories/Trays-and-Handles'},
                'Underwater-Batteries-and-Power-Supply': {"url": '/l/Photography/Underwater-Photography/Underwater-Photography-Accessories/Underwater-Batteries-and-Power-Supply'},
                'Underwater-Straps-and-Slings': {"url": '/l/Photography/Underwater-Photography/Underwater-Photography-Accessories/Underwater-Straps-and-Slings'}
            }}
        }}
    }},
    'Public-Safety': {"url": '/l/Public-Safety', "subcategories": {
        'Forensics': {"url": '/l/Public-Safety/Forensics', "subcategories": {
            'Analysis-and-Testing-Supplies': {"url": '/l/Public-Safety/Forensics/Analysis-and-Testing-Supplies', "subcategories": {
                'Blood-and-Urine-Analysis': {"url": '/l/Public-Safety/Forensics/Analysis-and-Testing-Supplies/Blood-and-Urine-Analysis'},
                'Firearm-and-Explosive-Analysis': {"url": '/l/Public-Safety/Forensics/Analysis-and-Testing-Supplies/Firearm-and-Explosive-Analysis'}
            }},
            'Crime-Scene-Marking': {"url": '/l/Public-Safety/Forensics/Crime-Scene-Marking'},
            'Crime-Scene-Optics': {"url": '/l/Public-Safety/Forensics/Crime-Scene-Optics'},
            'Digital-Forensic-Supplies': {"url": '/l/Public-Safety/Forensics/Digital-Forensic-Supplies'},
            'Evidence-Collection-Tools': {"url": '/l/Public-Safety/Forensics/Evidence-Collection-Tools', "subcategories": {
                'Biological-Collection-Tools': {"url": '/l/Public-Safety/Forensics/Evidence-Collection-Tools/Biological-Collection-Tools'},
                'Casting-Supplies': {"url": '/l/Public-Safety/Forensics/Evidence-Collection-Tools/Casting-Supplies'},
                'Knives-and-Scribers': {"url": '/l/Public-Safety/Forensics/Evidence-Collection-Tools/Knives-and-Scribers'},
                'Rulers-and-Reference-Scales': {"url": '/l/Public-Safety/Forensics/Evidence-Collection-Tools/Rulers-and-Reference-Scales'}
            }},
            'Evidence-Packaging-and-Labeling': {"url": '/l/Public-Safety/Forensics/Evidence-Packaging-and-Labeling'},
            'Fingerprint-Supplies': {"url": '/l/Public-Safety/Forensics/Fingerprint-Supplies', "subcategories": {
                'Fingerprinting': {"url": '/l/Public-Safety/Forensics/Fingerprint-Supplies/Fingerprinting'},
                'Latent-Print-Supplies': {"url": '/l/Public-Safety/Forensics/Fingerprint-Supplies/Latent-Print-Supplies'}
            }},
            'Forensic-Lighting': {"url": '/l/Public-Safety/Forensics/Forensic-Lighting'},
            'Forensic-Photography': {"url": '/l/Public-Safety/Forensics/Forensic-Photography'},
            'Forensic-Workstations-and-Equipment': {"url": '/l/Public-Safety/Forensics/Forensic-Workstations-and-Equipment'},
            'Protective-Equipment': {"url": '/l/Public-Safety/Forensics/Protective-Equipment'}
        }},
        'Law-Enforcement-and-EMS-Accessories': {"url": '/l/Public-Safety/Law-Enforcement-and-EMS-Accessories'},
        'Security': {"url": '/l/Public-Safety/Security'}
    }},
    'Video': {"url": '/l/Video', "subcategories": {
        'AV-Presentation': {"url": '/l/Video/AV-Presentation'},
        'Post-Production-Equipment': {"url": '/l/Video/Post-Production-Equipment', "subcategories": {
            'Disc-Publishers-and-Duplicators': {"url": '/l/Video/Post-Production-Equipment/Disc-Publishers-and-Duplicators'},
            'Video-Editing-Controllers': {"url": '/l/Video/Post-Production-Equipment/Video-Editing-Controllers'},
            'Video-Editing-Software': {"url": '/l/Video/Post-Production-Equipment/Video-Editing-Software'}
        }},
        'Teleprompters-and-Accessories': {"url": '/l/Video/Teleprompters-and-Accessories', "subcategories": {
            'Teleprompter-Controllers': {"url": '/l/Video/Teleprompters-and-Accessories/Teleprompter-Controllers'},
            'Teleprompters': {"url": '/l/Video/Teleprompters-and-Accessories/Teleprompters'},
            'Teleprompting-Software-and-Accessories': {"url": '/l/Video/Teleprompters-and-Accessories/Teleprompting-Software-and-Accessories'}
        }},
        'Video-Accessories': {"url": '/l/Video/Video-Accessories', "subcategories": {
            '360-Camera-Accessories': {"url": '/l/Video/Video-Accessories/360-Camera-Accessories'},
            '360-Camera-Mounts': {"url": '/l/Video/Video-Accessories/360-Camera-Mounts'},
            'Action-Camera-Accessories': {"url": '/l/Video/Video-Accessories/Action-Camera-Accessories'},
            'Action-Camera-Mounts': {"url": '/l/Video/Video-Accessories/Action-Camera-Mounts'},
            'Battery-Adapters-and-Mounts': {"url": '/l/Video/Video-Accessories/Battery-Adapters-and-Mounts'},
            'Camcorder-Batteries': {"url": '/l/Video/Video-Accessories/Camcorder-Batteries'},
            'Microphone-Shoe-Mounts': {"url": '/l/Video/Video-Accessories/Microphone-Shoe-Mounts'},
            'PTZ-Camera-Accessories': {"url": '/l/Video/Video-Accessories/PTZ-Camera-Accessories'},
            'PTZ-Camera-Controllers': {"url": '/l/Video/Video-Accessories/PTZ-Camera-Controllers'},
            'Portable-Video-Recording': {"url": '/l/Video/Video-Accessories/Portable-Video-Recording'},
            'Production-Accessories': {"url": '/l/Video/Video-Accessories/Production-Accessories'},
            'Production-Carts': {"url": '/l/Video/Video-Accessories/Production-Carts'},
            'Replacement-Video-Power-Supplies': {"url": '/l/Video/Video-Accessories/Replacement-Video-Power-Supplies'},
            'Video-Battery-Packs-and-Belts': {"url": '/l/Video/Video-Accessories/Video-Battery-Packs-and-Belts'},
            'Video-Battery-and-Camcorder-Chargers': {"url": '/l/Video/Video-Accessories/Video-Battery-and-Camcorder-Chargers'},
            'Video-Cables-and-Adapters': {"url": '/l/Video/Video-Accessories/Video-Cables-and-Adapters'},
            'Video-Shoe-Adapters': {"url": '/l/Video/Video-Accessories/Video-Shoe-Adapters'},
            'Video-Test-Charts': {"url": '/l/Video/Video-Accessories/Video-Test-Charts'},
            'Video-Viewfinders': {"url": '/l/Video/Video-Accessories/Video-Viewfinders'}
        }},
        'Video-Bags-and-Cases': {"url": '/l/Video/Video-Bags-and-Cases', "subcategories": {
            'Camcorder-Cases': {"url": '/l/Video/Video-Bags-and-Cases/Camcorder-Cases'},
            'Video-Backpacks': {"url": '/l/Video/Video-Bags-and-Cases/Video-Backpacks'},
            'Video-Camera-Rain-Covers': {"url": '/l/Video/Video-Bags-and-Cases/Video-Camera-Rain-Covers'},
            'Video-System-Cases': {"url": '/l/Video/Video-Bags-and-Cases/Video-System-Cases'},
            'Video-Waist-Packs': {"url": '/l/Video/Video-Bags-and-Cases/Video-Waist-Packs'}
        }},
        'Video-Cameras': {"url": '/l/Video/Video-Cameras', "subcategories": {
            'Action-Cameras': {"url": '/l/Video/Video-Cameras/Action-Cameras'},
            'Consumer-Camcorders': {"url": '/l/Video/Video-Cameras/Consumer-Camcorders'},
            'Digital-Cinema-Bodies': {"url": '/l/Video/Video-Cameras/Digital-Cinema-Bodies'},
            'PTZ-Cameras': {"url": '/l/Video/Video-Cameras/PTZ-Cameras'},
            'Professional-360-Cameras': {"url": '/l/Video/Video-Cameras/Professional-360-Cameras'},
            'Professional-Camcorders': {"url": '/l/Video/Video-Cameras/Professional-Camcorders'},
            'Studio-and-ENG-Cameras': {"url": '/l/Video/Video-Cameras/Studio-and-ENG-Cameras'}
        }},
        'Video-Lens-Accessories': {"url": '/l/Video/Video-Lens-Accessories', "subcategories": {
            'Action-Camera-Lens-Filters': {"url": '/l/Video/Video-Lens-Accessories/Action-Camera-Lens-Filters'},
            'Follow-Focus-and-Lens-Support': {"url": '/l/Video/Video-Lens-Accessories/Follow-Focus-and-Lens-Support', "subcategories": {
                'Focus-Drive-Gears': {"url": '/l/Video/Video-Lens-Accessories/Follow-Focus-and-Lens-Support/Focus-Drive-Gears'},
                'Focus-Gear-Rings': {"url": '/l/Video/Video-Lens-Accessories/Follow-Focus-and-Lens-Support/Focus-Gear-Rings'},
                'Follow-Focus-Accessories': {"url": '/l/Video/Video-Lens-Accessories/Follow-Focus-and-Lens-Support/Follow-Focus-Accessories'},
                'Follow-Focus-Systems': {"url": '/l/Video/Video-Lens-Accessories/Follow-Focus-and-Lens-Support/Follow-Focus-Systems'},
                'Video-Lens-Support': {"url": '/l/Video/Video-Lens-Accessories/Follow-Focus-and-Lens-Support/Video-Lens-Support'}
            }},
            'Lens-Attachments-and-Adapters': {"url": '/l/Video/Video-Lens-Accessories/Lens-Attachments-and-Adapters'},
            'Matte-Boxes-and-Accessories': {"url": '/l/Video/Video-Lens-Accessories/Matte-Boxes-and-Accessories', "subcategories": {
                'Matte-Box-Adapters': {"url": '/l/Video/Video-Lens-Accessories/Matte-Boxes-and-Accessories/Matte-Box-Adapters'},
                'Matte-Box-Filter-Holders': {"url": '/l/Video/Video-Lens-Accessories/Matte-Boxes-and-Accessories/Matte-Box-Filter-Holders'},
                'Matte-Box-Flags-and-Mattes': {"url": '/l/Video/Video-Lens-Accessories/Matte-Boxes-and-Accessories/Matte-Box-Flags-and-Mattes'},
                'Matte-Box-Support': {"url": '/l/Video/Video-Lens-Accessories/Matte-Boxes-and-Accessories/Matte-Box-Support'},
                'Matte-Boxes': {"url": '/l/Video/Video-Lens-Accessories/Matte-Boxes-and-Accessories/Matte-Boxes'}
            }},
            'Video-Controls-and-Accessories': {"url": '/l/Video/Video-Lens-Accessories/Video-Controls-and-Accessories'}
        }},
        'Video-Lenses': {"url": '/l/Video/Video-Lenses', "subcategories": {
            'Digital-Cinema-Lenses': {"url": '/l/Video/Video-Lenses/Digital-Cinema-Lenses'},
            'Professional-Lenses': {"url": '/l/Video/Video-Lenses/Professional-Lenses'}
        }},
        'Video-Monitors': {"url": '/l/Video/Video-Monitors', "subcategories": {
            'Monitor-Color-Calibration': {"url": '/l/Video/Video-Monitors/Monitor-Color-Calibration'},
            'Monitor-Controls-and-Cables': {"url": '/l/Video/Video-Monitors/Monitor-Controls-and-Cables'},
            'Monitor-Hoods': {"url": '/l/Video/Video-Monitors/Monitor-Hoods'},
            'Monitor-Screen-Protection': {"url": '/l/Video/Video-Monitors/Monitor-Screen-Protection'},
            'Monitor-and-Viewfinder-Mounting': {"url": '/l/Video/Video-Monitors/Monitor-and-Viewfinder-Mounting'},
            'On-hyphen-Camera-Video-Monitors': {"url": '/l/Video/Video-Monitors/On-hyphen-Camera-Video-Monitors'},
            'Production-Monitors': {"url": '/l/Video/Video-Monitors/Production-Monitors'},
            'Video-Monitor-Power': {"url": '/l/Video/Video-Monitors/Video-Monitor-Power'}
        }},
        'Video-Stabilizers-and-Supports': {"url": '/l/Video/Video-Stabilizers-and-Supports', "subcategories": {
            'Camera-Stands-and-Pedestals': {"url": '/l/Video/Video-Stabilizers-and-Supports/Camera-Stands-and-Pedestals'},
            'Cranes-and-Jib-Accessories': {"url": '/l/Video/Video-Stabilizers-and-Supports/Cranes-and-Jib-Accessories'},
            'Cranes-and-Jibs': {"url": '/l/Video/Video-Stabilizers-and-Supports/Cranes-and-Jibs'},
            'Dolly-comma-Stand-and-Pedestal-Accessories': {"url": '/l/Video/Video-Stabilizers-and-Supports/Dolly-comma-Stand-and-Pedestal-Accessories'},
            'Handheld-Gimbal-Stabilizer-Accessories': {"url": '/l/Video/Video-Stabilizers-and-Supports/Handheld-Gimbal-Stabilizer-Accessories'},
            'Handheld-Gimbal-Stabilizers': {"url": '/l/Video/Video-Stabilizers-and-Supports/Handheld-Gimbal-Stabilizers'},
            'Rod-Support-Systems': {"url": '/l/Video/Video-Stabilizers-and-Supports/Rod-Support-Systems'},
            'Support-Rig-Accessories': {"url": '/l/Video/Video-Stabilizers-and-Supports/Support-Rig-Accessories'},
            'Supports-and-Rigs': {"url": '/l/Video/Video-Stabilizers-and-Supports/Supports-and-Rigs'},
            'Video-Camera-Dollies-and-Sliders': {"url": '/l/Video/Video-Stabilizers-and-Supports/Video-Camera-Dollies-and-Sliders'},
            'Video-Tripods': {"url": '/l/Video/Video-Stabilizers-and-Supports/Video-Tripods'}
        }},
        'Video-Warranties': {"url": '/l/Video/Video-Warranties'},
        'Wireless-and-Live-Streaming': {"url": '/l/Video/Wireless-and-Live-Streaming', "subcategories": {
            'Video-Capture-and-Converters': {"url": '/l/Video/Wireless-and-Live-Streaming/Video-Capture-and-Converters', "subcategories": {
                'Pro-Video-Players-and-Recorders': {"url": '/l/Video/Wireless-and-Live-Streaming/Video-Capture-and-Converters/Pro-Video-Players-and-Recorders'},
                'Video-Capture': {"url": '/l/Video/Wireless-and-Live-Streaming/Video-Capture-and-Converters/Video-Capture'},
                'Video-Format-Converters': {"url": '/l/Video/Wireless-and-Live-Streaming/Video-Capture-and-Converters/Video-Format-Converters'}
            }},
            'Video-Switching-and-Distribution': {"url": '/l/Video/Wireless-and-Live-Streaming/Video-Switching-and-Distribution', "subcategories": {
                'Multimedia-Mixers-and-Live-Production': {"url": '/l/Video/Wireless-and-Live-Streaming/Video-Switching-and-Distribution/Multimedia-Mixers-and-Live-Production'},
                'Video-Distribution-Amplifiers-and-Accessories': {"url": '/l/Video/Wireless-and-Live-Streaming/Video-Switching-and-Distribution/Video-Distribution-Amplifiers-and-Accessories'},
                'Video-Switchers-and-Components': {"url": '/l/Video/Wireless-and-Live-Streaming/Video-Switching-and-Distribution/Video-Switchers-and-Components'}
            }},
            'Wireless-and-Broadcast-Equipment': {"url": '/l/Video/Wireless-and-Live-Streaming/Wireless-and-Broadcast-Equipment', "subcategories": {
                'Encoders-and-Controls': {"url": '/l/Video/Wireless-and-Live-Streaming/Wireless-and-Broadcast-Equipment/Encoders-and-Controls'},
                'Sync-and-Signal-Generation': {"url": '/l/Video/Wireless-and-Live-Streaming/Wireless-and-Broadcast-Equipment/Sync-and-Signal-Generation'},
                'Wireless-Video-Transmission-Accessories': {"url": '/l/Video/Wireless-and-Live-Streaming/Wireless-and-Broadcast-Equipment/Wireless-Video-Transmission-Accessories'},
                'Wireless-Video-Transmitters-and-Receivers': {"url": '/l/Video/Wireless-and-Live-Streaming/Wireless-and-Broadcast-Equipment/Wireless-Video-Transmitters-and-Receivers'}
            }}
        }}
    }}
}



def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _walk(node: dict, depth: int = 1, name: str | None = None):
    """Yield ``(depth, label, node)`` for ``node`` and every descendant."""
    yield depth, name, node
    for child_name, child in (node.get("subcategories") or {}).items():
        yield from _walk(child, depth + 1, child_name)


def _flatten_categories() -> list[dict[str, str]]:
    """Flatten depth-2+ inventory nodes into ``BaseListingSpider`` categories.

    Depth-1 department landings are skipped: they render ``bcmsSitePage`` CMS
    content with no product grid. Category slugs are disambiguated with the
    department when the same label appears under multiple departments.
    """
    categories: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    used_names: set[str] = set()
    for department, root in ADORAMA_CATEGORY_INVENTORY.items():
        for depth, name, node in _walk(root):
            if depth < 2 or not name:
                continue
            path = node.get("url") or ""
            if not path or path in seen_urls:
                continue
            seen_urls.add(path)
            slug = _slug(name)
            category = slug
            if category in used_names:
                category = f"{_slug(department)}-{slug}"
            suffix = 2
            while category in used_names:
                category = f"{_slug(department)}-{slug}-{suffix}"
                suffix += 1
            used_names.add(category)
            categories.append({
                "category": category,
                "department": department,
                "subcategory": name,
                "path": path,
                "url": f"{ADORAMA_BASE_URL}{path}",
            })
    return categories


ADORAMA_CATEGORIES = _flatten_categories()
