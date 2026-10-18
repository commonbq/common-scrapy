"""Booking.com city destinations exposed by the live homepage.

Sourced on 2026-10-19 from the homepage ``Popular with travelers from the
United States`` interlinking block: **80 city pages in 38 groups** -- 60 US
leaves across 23 groups (22 states plus the District of Columbia) and 20
non-US leaves across 15 countries.

Every URL was verified live on 2026-10-19 through the configured ScrapeOps US
route: HTTP 200 with a decodable ``lxAccommodations(...)`` Apollo hydration,
which the spider needs to resolve each city's destination ID.

``BOOKING_CATEGORIES`` uses the grouped mapping contract consumed by
``BaseListingSpider``: ``{region: {leaf: url}}``. Leaf keys stay the bare city
slug, so the documented ``-a category=las-vegas`` command is unchanged; the
DAG groups the tasks by region.
"""

BOOKING_CATEGORIES = {
    "Arizona": {
        "phoenix": "https://www.booking.com/city/us/phoenix.html",
        "tucson": "https://www.booking.com/city/us/tucson.html",
    },
    "California": {
        "bakersfield": "https://www.booking.com/city/us/bakersfield.html",
        "los-angeles": "https://www.booking.com/city/us/los-angeles.html",
        "mammoth-lakes": "https://www.booking.com/city/us/mammoth-lakes.html",
        "palm-springs": "https://www.booking.com/city/us/palm-springs.html",
        "riverside": "https://www.booking.com/city/us/riverside.html",
        "san-diego": "https://www.booking.com/city/us/san-diego.html",
        "san-francisco": "https://www.booking.com/city/us/san-francisco.html",
        "san-jose": "https://www.booking.com/city/us/san-jose.html",
        "santa-cruz": "https://www.booking.com/city/us/santa-cruz.html",
        "sorrento": "https://www.booking.com/city/us/sorrento.html",
        "south-lake-tahoe": "https://www.booking.com/city/us/south-lake-tahoe.html",
    },
    "Canada": {
        "montreal": "https://www.booking.com/city/ca/montreal.html",
        "niagara-falls": "https://www.booking.com/city/ca/niagara-falls.html",
        "toronto": "https://www.booking.com/city/ca/toronto.html",
    },
    "Chile": {
        "puerto-natales": "https://www.booking.com/city/cl/puerto-natales.html",
    },
    "Colorado": {
        "breckenridge": "https://www.booking.com/city/us/breckenridge.html",
        "denver": "https://www.booking.com/city/us/denver.html",
    },
    "Croatia": {
        "dubrovnik": "https://www.booking.com/city/hr/dubrovnik.html",
    },
    "District Of Columbia": {
        "washington": "https://www.booking.com/city/us/washington.html",
    },
    "Florida": {
        "cocoa-beach": "https://www.booking.com/city/us/cocoa-beach.html",
        "daytona-beach": "https://www.booking.com/city/us/daytona-beach.html",
        "destin": "https://www.booking.com/city/us/destin.html",
        "fort-lauderdale": "https://www.booking.com/city/us/fort-lauderdale.html",
        "jacksonville": "https://www.booking.com/city/us/jacksonville.html",
        "kissimmee": "https://www.booking.com/city/us/kissimmee.html",
        "miami": "https://www.booking.com/city/us/miami.html",
        "miami-beach": "https://www.booking.com/city/us/miami-beach.html",
        "orlando": "https://www.booking.com/city/us/orlando.html",
        "panama-city-beach": "https://www.booking.com/city/us/panama-city-beach.html",
        "saint-augustine": "https://www.booking.com/city/us/saint-augustine.html",
        "tallahassee": "https://www.booking.com/city/us/tallahassee.html",
        "tampa": "https://www.booking.com/city/us/tampa.html",
    },
    "France": {
        "paris": "https://www.booking.com/city/fr/paris.html",
    },
    "Georgia": {
        "atlanta": "https://www.booking.com/city/us/atlanta.html",
        "savannah": "https://www.booking.com/city/us/savannah.html",
    },
    "Illinois": {
        "chicago": "https://www.booking.com/city/us/chicago.html",
    },
    "Italy": {
        "florence": "https://www.booking.com/city/it/florence.html",
        "rome": "https://www.booking.com/city/it/rome.html",
    },
    "Japan": {
        "kyoto": "https://www.booking.com/city/jp/kyoto.html",
        "tokyo": "https://www.booking.com/city/jp/tokyo.html",
    },
    "Kentucky": {
        "louisville": "https://www.booking.com/city/us/louisville.html",
    },
    "Louisiana": {
        "new-orleans": "https://www.booking.com/city/us/new-orleans.html",
    },
    "Maldives": {
        "male": "https://www.booking.com/city/mv/male.html",
    },
    "Maryland": {
        "ocean-city": "https://www.booking.com/city/us/ocean-city.html",
    },
    "Massachusetts": {
        "boston": "https://www.booking.com/city/us/boston.html",
    },
    "Mexico": {
        "sanya-cn": "https://www.booking.com/city/mx/sanya-cn.html",
    },
    "Michigan": {
        "detroit": "https://www.booking.com/city/us/detroit.html",
    },
    "Missouri": {
        "kansas-city": "https://www.booking.com/city/us/kansas-city.html",
        "saint-louis": "https://www.booking.com/city/us/saint-louis.html",
        "springfield": "https://www.booking.com/city/us/springfield.html",
    },
    "Netherlands": {
        "amsterdam": "https://www.booking.com/city/nl/amsterdam.html",
    },
    "Nevada": {
        "las-vegas": "https://www.booking.com/city/us/las-vegas.html",
        "reno": "https://www.booking.com/city/us/reno.html",
    },
    "New York": {
        "brooklyn": "https://www.booking.com/city/us/brooklyn.html",
        "new-york": "https://www.booking.com/city/us/new-york.html",
    },
    "New Zealand": {
        "hahei": "https://www.booking.com/city/nz/hahei.html",
    },
    "North Carolina": {
        "charlotte": "https://www.booking.com/city/us/charlotte.html",
        "raleigh": "https://www.booking.com/city/us/raleigh.html",
    },
    "Ohio": {
        "columbus": "https://www.booking.com/city/us/columbus.html",
    },
    "Oklahoma": {
        "oklahoma-city": "https://www.booking.com/city/us/oklahoma-city.html",
    },
    "Oregon": {
        "portland": "https://www.booking.com/city/us/portland.html",
    },
    "Peru": {
        "cusco": "https://www.booking.com/city/pe/cusco.html",
    },
    "Puerto Rico": {
        "san-juan": "https://www.booking.com/city/pr/san-juan.html",
    },
    "South Carolina": {
        "myrtle-beach": "https://www.booking.com/city/us/myrtle-beach.html",
    },
    "Spain": {
        "barcelona": "https://www.booking.com/city/es/barcelona.html",
        "granada": "https://www.booking.com/city/es/granada.html",
    },
    "Switzerland": {
        "zermatt": "https://www.booking.com/city/ch/zermatt.html",
    },
    "Tennessee": {
        "gatlinburg": "https://www.booking.com/city/us/gatlinburg.html",
        "nashville": "https://www.booking.com/city/us/nashville.html",
        "pigeon-forge": "https://www.booking.com/city/us/pigeon-forge.html",
    },
    "Texas": {
        "amarillo": "https://www.booking.com/city/us/amarillo.html",
        "austin": "https://www.booking.com/city/us/austin.html",
        "fort-worth": "https://www.booking.com/city/us/fort-worth.html",
        "galveston": "https://www.booking.com/city/us/galveston.html",
        "houston": "https://www.booking.com/city/us/houston.html",
        "san-antonio": "https://www.booking.com/city/us/san-antonio.html",
    },
    "Thailand": {
        "bangkok": "https://www.booking.com/city/th/bangkok.html",
    },
    "Washington": {
        "seattle": "https://www.booking.com/city/us/seattle.html",
    },
}
