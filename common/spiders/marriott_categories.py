"""Marriott destinations from the site's Browse All Destinations catalogue.

Source: https://www.marriott.com/en/destinations.mi (retrieved 2026-10-13).
"""

from __future__ import annotations

_DESTINATION_SLUGS = {
    "United States": (
        "dauphin gulf-shores huntsville mobile montgomery birmingham tuscaloosa point-clear",
        "orange-beach anchorage fairbanks flagstaff page phoenix prescott sedona tucson yuma mesa",
        "tempe scottsdale glendale chandler fayetteville hot-springs little-rock anaheim berkeley",
        "big-bear-lake fresno la-quinta lake-arrowhead lake-tahoe lancaster-california long-beach",
        "los-angeles mammoth-lakes marina-del-rey monterey napa newport-beach oceano ontario",
        "palm-springs paso-robles redding sacramento san-diego san-francisco san-jose-california",
        "san-luis-obispo santa-barbara santa-clarita santa-cruz santa-rosa sea-ranch",
        "sequoia-national-forest sonoma south-lake-tahoe temecula ventura yosemite oakland",
        "westlake-village walnut-creek torrance sunnyvale santa-monica santa-clara san-mateo",
        "redwood-city pasadena palm-desert oceanside mountain-view manhattan-beach la-jolla",
        "irvine hollywood emeryville el-segundo dana-point coronado carlsbad camarillo burbank",
        "bakersfield aspen boulder breckenridge colorado-springs denver durango fort-collins",
        "glenwood-springs grand-junction grand-lake keystone ouray pagosa-springs silverthorne",
        "steamboat-springs telluride vail winter-park aurora avon hartford mystic new-haven",
        "stamford rehoboth-beach wilmington-delaware district-of-columbia amelia-island",
        "cape-coral cape-san-blas clearwater daytona-beach delray-beach destin florida-keys",
        "fort-lauderdale fort-myers fort-walton-beach indian-rocks-beach jacksonville key-largo",
        "key-west kissimmee marco-island melbourne-florida miami miami-beach miramar-beach",
        "naples-florida ocala orlando palm-beach panama-city-florida panama-city-beach pensacola",
        "sanibel santa-rosa-beach sarasota st-augustine tallahassee tampa treasure-island",
        "venice-florida west-palm-beach winter-haven anna-maria port-st-lucie vero-beach",
        "the-villages st-petersburg ponte-vedra-beach pompano-beach lake-buena-vista jupiter",
        "jensen-beach hollywood-florida gainesville coral-gables coconut-grove cocoa-beach",
        "bradenton boca-raton atlanta augusta brunswick-georgia columbus-georgia helen",
        "jekyll-island macon savannah st-simons tybee-island valdosta athens stone-mountain",
        "marietta buckhead alpharetta island-of-hawaii kauai maui oahu honolulu waikiki ko-olina",
        "bear-lake boise coeur-d-alene idaho-falls sun-valley chicago peoria springfield-illinois",
        "oak-brook fort-wayne indianapolis south-bend evansville carmel bloomington davenport",
        "des-moines iowa-city sioux-city cedar-rapids wichita ashland bowling-green lexington",
        "louisville baton-rouge lafayette lake-charles new-orleans shreveport bangor",
        "boothbay-harbor kennebunkport portland-maine boston cape-cod lenox plymouth",
        "springfield-massachusetts baltimore deep-creek-lake ocean-city towson annapolis",
        "ann-arbor detroit grand-rapids kalamazoo lansing marquette traverse-city",
        "holland-michigan novi duluth minneapolis gulfport jackson-mississippi kansas-city",
        "st-louis springfield branson big-sky billings bozeman great-falls helena kalispell",
        "missoula lincoln omaha las-vegas reno winnemucca henderson north-conway manchester",
        "portsmouth atlantic-city mahwah princeton jersey-city cherry-hill newark albuquerque",
        "las-cruces santa-fe gallup albany buffalo ithaca lake-george lake-placid long-island nyc",
        "niagara-falls poughkeepsie rochester saratoga-springs syracuse white-plains brooklyn",
        "hudson-valley asheville boone carolina-beach charlotte cherokee greensboro",
        "greenville-north-carolina outer-banks raleigh sugar-mountain winston-salem pinehurst",
        "durham-north-carolina chapel-hill bismarck fargo grand-forks akron cincinnati cleveland",
        "columbus-ohio dayton toledo-spain sandusky lawton oklahoma-city tulsa bend eugene",
        "klamath-falls lincoln-city medford mount-hood portland-oregon allentown",
        "delaware-water-gap erie gettysburg harrisburg philadelphia pittsburgh wilkes-barre",
        "lancaster-pennsylvania king-of-prussia hershey newport providence beaufort",
        "charleston-south-carolina columbia hilton-head-island myrtle-beach north-myrtle-beach",
        "kiawah-island aberdeen deadwood rapid-city sioux-falls chattanooga gatlinburg",
        "johnson-city knoxville memphis nashville pigeon-forge murfreesboro franklin amarillo",
        "austin corpus-christi dallas el-paso fort-worth galveston houston lubbock marble-falls",
        "midland odessa rockport san-antonio south-padre-island waco the-woodlands plano",
        "new-braunfels katy grapevine college-station arlington-texas moab ogden park-city",
        "salt-lake-city st-george-utah draper burlington charlottesville fredericksburg richmond",
        "roanoke virginia-beach williamsburg winchester tysons-corner norfolk hampton",
        "crystal-city chesapeake arlington bellingham lake-chelan olympia seattle spokane",
        "tri-cities wenatchee yakima tacoma pullman bellevue charleston-west-virginia morgantown",
        "fairmont appleton green-bay la-crosse lake-geneva madison milwaukee cheyenne",
        "jackson-wyoming yellowstone",
    ),
    "Africa": (
        "algiers gaborone accra nairobi blantyre mauritius casablanca fez marrakesh windhoek",
        "port-harcourt lagos-nigeria kigali bloemfontein cape-town durban george johannesburg",
        "kruger-park nelspruit pretoria stellenbosch arusha dar-es-salaam zanzibar sousse tunis",
        "kampala livingstone lusaka",
    ),
    "Asia": (
        "baku dhaka thimphu phnom-penh beijing shanghai macau hong-kong agra ahmedabad amritsar",
        "bengaluru bhopal chandigarh chennai coimbatore dehradun goa gurugram hyderabad indore",
        "jaipur jaisalmer jodhpur kochi kolkata lucknow madurai mahabaleshwar mumbai mussoorie",
        "nagpur nashik navi-mumbai new-delhi pune pushkar siliguri srinagar vadodara",
        "visakhapatnam rajasthan bali bandung batam belitung jakarta medan surabaya yogyakarta",
        "gifu hakodate hiroshima hokkaido ise izu kyoto nagano nagoya nikko okinawa osaka sapporo",
        "sendai shirahama tokyo utsunomiya shizuoka nago-city nara almaty astana bishkek desaru",
        "johor-bahru kota-kinabalu kuala-lumpur kuantan langkawi miri penang maldives kathmandu",
        "islamabad karachi lahore iloilo-city manila cebu-city singapore busan daegu daejeon",
        "incheon jeju-do seoul bangkok chiang-rai hua-hin khao-lak koh-samui krabi pattaya phuket",
        "rayong tashkent da-nang hanoi ho-chi-minh-city nha-trang phu-quoc",
    ),
    "Australia & Pacific Islands": (
        "brisbane canberra melbourne perth sydney goldcoast fiji bora-bora guam auckland",
    ),
    "Canada": (
        "barrie blue-mountains calgary charlottetown edmonton fredericton grande-prairie halifax",
        "hamilton kamloops kelowna canada-kingston=kingston london-canada moncton montreal",
        "mont-tremblant ottawa prince-george quebec red-deer regina revelstoke sarnia saskatoon",
        "sault-ste-marie thunder-bay toronto vancouver victoria whistler winnipeg st-johns-canada",
        "windsor banff",
    ),
    "Caribbean": (
        "aruba bahamas barbados bermuda grand-cayman curacao caribbean-kingston=kingston san-juan",
        "trinidad-and-tobago st-croix st-thomas",
    ),
    "Central America": (
        "san-pedro-town gulf-of-papagayo playa-herradura san-jose panama-city guatemala-city",
        "san-salvador",
    ),
    "Europe": (
        "yerevan dornbirn innsbruck linz salzburg vienna minsk antwerp brussels ghent mostar",
        "sarajevo sofia brac dubrovnik mlini split zagreb cyprus brno prague copenhagen aarhus",
        "tallinn helsinki tampere anglet annecy antibes avignon bayonne beaune biarritz bordeaux",
        "cannes deauville dijon honfleur la-ciotat lille lyon marseille megeve menton montpellier",
        "mougins nice paris reims rouen saint-remy-de-provence saint-tropez strasbourg toulouse",
        "val-d-isere batumi tbilisi baden-baden berlin bremen cologne dresden dusseldorf essen",
        "frankfurt freiburg-im-breisgau hamburg hanover heidelberg leipzig mainz mosel munich",
        "nuremberg stuttgart weimar wolfsburg wurzburg andros corfu costa-navarino crete",
        "ionian-islands kea kythnos mykonos naxos paros rhodes santorini sifnos tinos",
        "athens-greece greek-islands budapest athlone dublin kilkenny amalfi arezzo bologna",
        "bolzano brescia cortina-d-ampezzo ferrara florence genoa grosseto ischia lake-como",
        "lake-garda lake-maggiore lucca milan padova perugia pienza pisa positano praiano rome",
        "salerno siena sorrento turin venice viareggio vicenza pristina kaunas vilnius skopje",
        "malta chisinau monte-carlo amsterdam eindhoven maastricht rotterdam utrecht bergen",
        "gdansk gdynia katowice krakow poznan sopot szczecin warsaw wroclaw albufeira cascais",
        "faro lisbon portimao porto sesimbra setubal sintra viana-do-castelo lagos-portugal",
        "algarve bucharest belgrade novi-sad bratislava ljubljana a-coruna algeciras alicante",
        "badajoz baqueira barcelona benalmadena bilbao burgos calpe cordoba estepona formentera",
        "fuerteventura gijon gran-canaria granada huelva ibiza javea la-rioja lanzarote madrid",
        "malaga mallorca marbella mijas murcia nerja oviedo pamplona ronda salamanca",
        "san-sebastian santiago-de-compostela seville sitges tarragona tenerife toledo valencia",
        "valladolid vigo vitoria-gasteiz palma-de-mallorca balearic-islands andalusia stockholm",
        "ascona basel bern crans flims geneva gstaad interlaken lausanne lucerne montreux sion",
        "st-moritz verbier zermatt zug zurich neuchatel ankara bodrum bursa cesme istanbul izmir",
        "aberdeen-united-kingdom bath belfast bournemouth brighton bristol cambridge cardiff",
        "chester derby durham edinburgh exeter glasgow inverness leeds leicester liverpool london",
        "luton maidstone milton-keynes newcastle northampton oxford perth-united-kingdom",
        "peterborough preston shrewsbury southampton stoke-on-trent stratford-upon-avon swansea",
        "swindon telford whitby york birmingham-united-kingdom manchester-united-kingdom",
        "portsmouth-united-kingdom winchester-united-kingdom windsor-united-kingdom",
    ),
    "Mexico": (
        "cabo-san-lucas campeche cancun chihuahua ciudad-juarez guadalajara holbox la-paz merida",
        "mexico-city monterrey playa-del-carmen puebla puerto-escondido puerto-vallarta",
        "punta-mita riviera-nayarit san-jose-del-cabo san-luis-potosi san-miguel-de-cozumel",
        "sonora tijuana tulum villahermosa los-cabos",
    ),
    "Middle East": (
        "manama alexandria cairo hurghada sharm-el-sheikh red-sea eilat haifa jerusalem tel-aviv",
        "amman aqaba petra kuwait-city beirut muscat doha al-khobar jeddah riyadh abu-dhabi",
        "al-ain al-aqah dubai sharjah",
    ),
    "South America": (
        "buenos-aires mar-del-plata mendoza salta san-carlos-de-bariloche santa-cruz-de-la-sierra",
        "rio-de-janeiro santos sao-paulo santiago vina-del-mar barranquilla bogota cali cartagena",
        "medellin santa-marta cuenca guayaquil quito georgetown asuncion cusco lima paracas",
        "paramaribo colonia-del-sacramento montevideo caracas",
    ),
}

MARRIOTT_CATEGORIES = {
    region: {
        token.partition("=")[0]: {
            "url": (
                "https://www.marriott.com/en/destinations/"
                f"{token.partition('=')[2] or token}.mi"
            )
        }
        for chunk in chunks
        for token in chunk.split()
    }
    for region, chunks in _DESTINATION_SLUGS.items()
}
