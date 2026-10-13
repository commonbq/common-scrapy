"""Complete Movoto sale-market taxonomy from the first-party sitemap.

Source: ``https://www.movoto.com/sitemap/`` (the rendered "United States
Homes for Sale" directory), captured 2026-10-13. The page lists 149 crawlable
city sale-market links; grouping is by the trailing US state code so leaf names
stay globally unique for the DAG output paths.
"""

MOVOTO_CATEGORIES = {
    "AK": {
        "anchorage-ak": "https://www.movoto.com/anchorage-ak/",
    },
    "AL": {
        "huntsville-al": "https://www.movoto.com/huntsville-al/",
    },
    "AZ": {
        "buckeye-az": "https://www.movoto.com/buckeye-az/",
        "gilbert-az": "https://www.movoto.com/gilbert-az/",
        "mesa-az": "https://www.movoto.com/mesa-az/",
        "phoenix-az": "https://www.movoto.com/phoenix-az/",
        "prescott-az": "https://www.movoto.com/prescott-az/",
        "scottsdale-az": "https://www.movoto.com/scottsdale-az/",
        "surprise-az": "https://www.movoto.com/surprise-az/",
        "tucson-az": "https://www.movoto.com/tucson-az/",
        "yuma-az": "https://www.movoto.com/yuma-az/",
    },
    "CA": {
        "bakersfield-ca": "https://www.movoto.com/bakersfield-ca/",
        "fresno-ca": "https://www.movoto.com/fresno-ca/",
        "lancaster-ca": "https://www.movoto.com/lancaster-ca/",
        "los-angeles-ca": "https://www.movoto.com/los-angeles-ca/",
        "riverside-ca": "https://www.movoto.com/riverside-ca/",
        "sacramento-ca": "https://www.movoto.com/sacramento-ca/",
        "san-diego-ca": "https://www.movoto.com/san-diego-ca/",
        "san-jose-ca": "https://www.movoto.com/san-jose-ca/",
        "stockton-ca": "https://www.movoto.com/stockton-ca/",
    },
    "CO": {
        "aurora-co": "https://www.movoto.com/aurora-co/",
        "colorado-springs-co": "https://www.movoto.com/colorado-springs-co/",
        "denver-co": "https://www.movoto.com/denver-co/",
        "grand-junction-co": "https://www.movoto.com/grand-junction-co/",
    },
    "DC": {
        "washington-dc": "https://www.movoto.com/washington-dc/",
    },
    "FL": {
        "boca-raton-fl": "https://www.movoto.com/boca-raton-fl/",
        "boynton-beach-fl": "https://www.movoto.com/boynton-beach-fl/",
        "bradenton-fl": "https://www.movoto.com/bradenton-fl/",
        "cape-coral-fl": "https://www.movoto.com/cape-coral-fl/",
        "clermont-fl": "https://www.movoto.com/clermont-fl/",
        "davenport-fl": "https://www.movoto.com/davenport-fl/",
        "daytona-beach-fl": "https://www.movoto.com/daytona-beach-fl/",
        "deerfield-beach-fl": "https://www.movoto.com/deerfield-beach-fl/",
        "delray-beach-fl": "https://www.movoto.com/delray-beach-fl/",
        "fort-lauderdale-fl": "https://www.movoto.com/fort-lauderdale-fl/",
        "fort-myers-fl": "https://www.movoto.com/fort-myers-fl/",
        "fort-pierce-fl": "https://www.movoto.com/fort-pierce-fl/",
        "gainesville-fl": "https://www.movoto.com/gainesville-fl/",
        "jacksonville-fl": "https://www.movoto.com/jacksonville-fl/",
        "kissimmee-fl": "https://www.movoto.com/kissimmee-fl/",
        "lakeland-fl": "https://www.movoto.com/lakeland-fl/",
        "lehigh-acres-fl": "https://www.movoto.com/lehigh-acres-fl/",
        "miami-fl": "https://www.movoto.com/miami-fl/",
        "naples-fl": "https://www.movoto.com/naples-fl/",
        "north-port-fl": "https://www.movoto.com/north-port-fl/",
        "ocala-fl": "https://www.movoto.com/ocala-fl/",
        "orlando-fl": "https://www.movoto.com/orlando-fl/",
        "palm-bay-fl": "https://www.movoto.com/palm-bay-fl/",
        "palm-coast-fl": "https://www.movoto.com/palm-coast-fl/",
        "panama-city-beach-fl": "https://www.movoto.com/panama-city-beach-fl/",
        "panama-city-fl": "https://www.movoto.com/panama-city-fl/",
        "pensacola-fl": "https://www.movoto.com/pensacola-fl/",
        "port-charlotte-fl": "https://www.movoto.com/port-charlotte-fl/",
        "port-saint-lucie-fl": "https://www.movoto.com/port-saint-lucie-fl/",
        "punta-gorda-fl": "https://www.movoto.com/punta-gorda-fl/",
        "saint-augustine-fl": "https://www.movoto.com/saint-augustine-fl/",
        "saint-petersburg-fl": "https://www.movoto.com/saint-petersburg-fl/",
        "sarasota-fl": "https://www.movoto.com/sarasota-fl/",
        "spring-hill-fl": "https://www.movoto.com/spring-hill-fl/",
        "tallahassee-fl": "https://www.movoto.com/tallahassee-fl/",
        "tampa-fl": "https://www.movoto.com/tampa-fl/",
        "the-villages-fl": "https://www.movoto.com/the-villages-fl/",
        "vero-beach-fl": "https://www.movoto.com/vero-beach-fl/",
        "west-palm-beach-fl": "https://www.movoto.com/west-palm-beach-fl/",
    },
    "GA": {
        "atlanta-ga": "https://www.movoto.com/atlanta-ga/",
        "macon-ga": "https://www.movoto.com/macon-ga/",
        "marietta-ga": "https://www.movoto.com/marietta-ga/",
        "savannah-ga": "https://www.movoto.com/savannah-ga/",
    },
    "HI": {
        "honolulu-hi": "https://www.movoto.com/honolulu-hi/",
    },
    "ID": {
        "boise-id": "https://www.movoto.com/boise-id/",
    },
    "IL": {
        "chicago-il": "https://www.movoto.com/chicago-il/",
    },
    "IN": {
        "fort-wayne-in": "https://www.movoto.com/fort-wayne-in/",
        "indianapolis-in": "https://www.movoto.com/indianapolis-in/",
    },
    "KS": {
        "wichita-ks": "https://www.movoto.com/wichita-ks/",
    },
    "KY": {
        "lexington-ky": "https://www.movoto.com/lexington-ky/",
        "louisville-ky": "https://www.movoto.com/louisville-ky/",
    },
    "LA": {
        "baton-rouge-la": "https://www.movoto.com/baton-rouge-la/",
        "new-orleans-la": "https://www.movoto.com/new-orleans-la/",
    },
    "MA": {
        "boston-ma": "https://www.movoto.com/boston-ma/",
    },
    "MD": {
        "baltimore-md": "https://www.movoto.com/baltimore-md/",
    },
    "MI": {
        "detroit-mi": "https://www.movoto.com/detroit-mi/",
    },
    "MN": {
        "rochester-mn": "https://www.movoto.com/rochester-mn/",
    },
    "MO": {
        "kansas-city-mo": "https://www.movoto.com/kansas-city-mo/",
        "saint-louis-mo": "https://www.movoto.com/saint-louis-mo/",
    },
    "MT": {
        "billings-mt": "https://www.movoto.com/billings-mt/",
    },
    "NC": {
        "charlotte-nc": "https://www.movoto.com/charlotte-nc/",
        "fayetteville-nc": "https://www.movoto.com/fayetteville-nc/",
        "greensboro-nc": "https://www.movoto.com/greensboro-nc/",
        "raleigh-nc": "https://www.movoto.com/raleigh-nc/",
        "wilmington-nc": "https://www.movoto.com/wilmington-nc/",
        "winston-salem-nc": "https://www.movoto.com/winston-salem-nc/",
    },
    "NE": {
        "lincoln-ne": "https://www.movoto.com/lincoln-ne/",
        "omaha-ne": "https://www.movoto.com/omaha-ne/",
    },
    "NM": {
        "albuquerque-nm": "https://www.movoto.com/albuquerque-nm/",
        "rio-rancho-nm": "https://www.movoto.com/rio-rancho-nm/",
        "santa-fe-nm": "https://www.movoto.com/santa-fe-nm/",
    },
    "NV": {
        "henderson-nv": "https://www.movoto.com/henderson-nv/",
        "las-vegas-nv": "https://www.movoto.com/las-vegas-nv/",
        "pahrump-nv": "https://www.movoto.com/pahrump-nv/",
        "reno-nv": "https://www.movoto.com/reno-nv/",
    },
    "NY": {
        "brooklyn-ny": "https://www.movoto.com/brooklyn-ny/",
        "new-york-ny": "https://www.movoto.com/new-york-ny/",
    },
    "OH": {
        "cincinnati-oh": "https://www.movoto.com/cincinnati-oh/",
        "columbus-oh": "https://www.movoto.com/columbus-oh/",
    },
    "OK": {
        "edmond-ok": "https://www.movoto.com/edmond-ok/",
        "oklahoma-city-ok": "https://www.movoto.com/oklahoma-city-ok/",
        "tulsa-ok": "https://www.movoto.com/tulsa-ok/",
    },
    "OR": {
        "bend-or": "https://www.movoto.com/bend-or/",
        "portland-or": "https://www.movoto.com/portland-or/",
    },
    "PA": {
        "philadelphia-pa": "https://www.movoto.com/philadelphia-pa/",
        "pittsburgh-pa": "https://www.movoto.com/pittsburgh-pa/",
    },
    "SC": {
        "charleston-sc": "https://www.movoto.com/charleston-sc/",
        "columbia-sc": "https://www.movoto.com/columbia-sc/",
        "greenville-sc": "https://www.movoto.com/greenville-sc/",
        "myrtle-beach-sc": "https://www.movoto.com/myrtle-beach-sc/",
        "summerville-sc": "https://www.movoto.com/summerville-sc/",
    },
    "SD": {
        "sioux-falls-sd": "https://www.movoto.com/sioux-falls-sd/",
    },
    "TN": {
        "chattanooga-tn": "https://www.movoto.com/chattanooga-tn/",
        "clarksville-tn": "https://www.movoto.com/clarksville-tn/",
        "knoxville-tn": "https://www.movoto.com/knoxville-tn/",
        "memphis-tn": "https://www.movoto.com/memphis-tn/",
        "murfreesboro-tn": "https://www.movoto.com/murfreesboro-tn/",
        "nashville-tn": "https://www.movoto.com/nashville-tn/",
    },
    "TX": {
        "amarillo-tx": "https://www.movoto.com/amarillo-tx/",
        "arlington-tx": "https://www.movoto.com/arlington-tx/",
        "austin-tx": "https://www.movoto.com/austin-tx/",
        "cleveland-tx": "https://www.movoto.com/cleveland-tx/",
        "conroe-tx": "https://www.movoto.com/conroe-tx/",
        "corpus-christi-tx": "https://www.movoto.com/corpus-christi-tx/",
        "cypress-tx": "https://www.movoto.com/cypress-tx/",
        "dallas-tx": "https://www.movoto.com/dallas-tx/",
        "el-paso-tx": "https://www.movoto.com/el-paso-tx/",
        "fort-worth-tx": "https://www.movoto.com/fort-worth-tx/",
        "frisco-tx": "https://www.movoto.com/frisco-tx/",
        "galveston-tx": "https://www.movoto.com/galveston-tx/",
        "houston-tx": "https://www.movoto.com/houston-tx/",
        "katy-tx": "https://www.movoto.com/katy-tx/",
        "lubbock-tx": "https://www.movoto.com/lubbock-tx/",
        "mckinney-tx": "https://www.movoto.com/mckinney-tx/",
        "montgomery-tx": "https://www.movoto.com/montgomery-tx/",
        "new-braunfels-tx": "https://www.movoto.com/new-braunfels-tx/",
        "richmond-tx": "https://www.movoto.com/richmond-tx/",
        "san-angelo-tx": "https://www.movoto.com/san-angelo-tx/",
        "san-antonio-tx": "https://www.movoto.com/san-antonio-tx/",
        "spring-tx": "https://www.movoto.com/spring-tx/",
    },
    "UT": {
        "salt-lake-city-ut": "https://www.movoto.com/salt-lake-city-ut/",
    },
    "VA": {
        "virginia-beach-va": "https://www.movoto.com/virginia-beach-va/",
    },
    "WA": {
        "seattle-wa": "https://www.movoto.com/seattle-wa/",
        "spokane-wa": "https://www.movoto.com/spokane-wa/",
    },
}
