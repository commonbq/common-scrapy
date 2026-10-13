"""Viator's complete Popular Cities inventory from the homepage."""

# Verified against the live homepage's ``Popular Cities`` section on 2026-10-13.
VIATOR_CATEGORIES = {
    "popular-cities": {
        slug: f"https://www.viator.com/{path}"
        for slug, path in (
            ("nashville", "Nashville/d799"),
            ("chicago", "Chicago/d673"),
            ("houston", "Houston/d5186"),
            ("san-diego", "San-Diego/d736"),
            ("atlanta", "Atlanta/d784"),
            ("denver", "Denver/d4837"),
            ("las-vegas", "Las-Vegas/d684"),
            ("miami", "Miami/d662"),
            ("orlando", "Orlando/d663"),
            ("dallas", "Dallas/d918"),
            ("new-orleans", "New-Orleans/d675"),
            ("san-antonio", "San-Antonio/d910"),
            ("san-francisco", "San-Francisco/d651"),
            ("seattle", "Seattle/d704"),
            ("austin", "Austin/d5021"),
            ("boston", "Boston/d678"),
            ("rome", "Rome/d511"),
            ("los-angeles", "Los-Angeles/d645"),
            ("myrtle-beach", "Myrtle-Beach/d5217"),
            ("philadelphia", "Philadelphia/d906"),
            ("paris", "Paris/d479"),
            ("colorado", "Colorado/d273"),
            ("phoenix", "Phoenix/d639"),
            ("london", "London/d737"),
            ("tampa", "Tampa/d666"),
            ("florence", "Florence/d519"),
            ("oahu", "Oahu/d672"),
            ("key-west", "Key-West/d661"),
            ("new-york-city", "New-York-City/d687"),
            ("maui", "Maui/d671"),
            ("arizona", "Arizona/d271"),
            ("barcelona", "Barcelona/d562"),
            ("florida", "Florida/d276"),
            ("lisbon", "Lisbon/d538"),
            ("washington-dc", "Washington-DC/d657"),
        )
    }
}
