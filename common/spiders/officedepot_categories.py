"""Office Depot category inventory from the first-party header menu endpoint.

Source: https://ma.officedepot.com/header-menu-excel/products.json
Snapshot refreshed 2026-10-14. The spider refreshes the same inventory at crawl
time, while Airflow reads the static mapping at DAG parse time.
"""

from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urlsplit

_SLUG_CLEAN_RE = re.compile(r"[^a-z0-9]+")


def _slug(value: str) -> str:
    return _SLUG_CLEAN_RE.sub("-", value.lower()).strip("-")


def category_slug(department: str, sub_category: str, name: str, url: str) -> str:
    """Stable globally unique leaf key accepted by ``-a category=``."""
    category_id = urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]
    return _slug(f"{department}-{sub_category}-{name}-{category_id}")


def parse_categories(payload: str | bytes) -> dict[str, dict[str, dict[str, str]]]:
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8", "replace")
    data = json.loads(payload)
    grouped: dict[str, dict[str, dict[str, str]]] = {}

    def add(department: str, sub_category: str, name: str, url: str) -> None:
        if not url.startswith("/b/"):
            return
        leaf = category_slug(department, sub_category, name, url)
        grouped.setdefault(department, {})[leaf] = {
            "url": url,
            "name": name,
            "sub_category": sub_category,
        }

    def walk(nodes: list[dict[str, Any]], department: str, parent: str) -> None:
        for node in nodes:
            name = (node.get("name") or "").strip()
            url = (node.get("url") or "").strip()
            add(department, parent, name, url)
            walk(node.get("hierarchy") or [], department, name)

    menu = data.get("responseObject", {}).get("menuList", [])
    for department_node in menu:
        department = (department_node.get("name") or "").strip()
        add(department, "", department, (department_node.get("url") or "").strip())
        walk(department_node.get("hierarchy") or [], department, "")
    return grouped


# BEGIN GENERATED CATEGORY SNAPSHOT
OFFICEDEPOT_CATEGORIES = {'Office Supplies': {'office-supplies-office-supplies-n-1676': {'url': '/b/office-supplies/N-1676',
                                                                'name': 'Office Supplies',
                                                                'sub_category': ''},
                     'office-supplies-pens-pencils-markers-n-4367': {'url': '/b/pens-pencils-and-markers/N-4367',
                                                                     'name': 'Pens, Pencils & '
                                                                             'Markers',
                                                                     'sub_category': ''},
                     'office-supplies-pens-pencils-markers-pens-n-4520': {'url': '/b/pens/N-4520',
                                                                          'name': 'Pens',
                                                                          'sub_category': 'Pens, '
                                                                                          'Pencils '
                                                                                          '& '
                                                                                          'Markers'},
                     'office-supplies-pens-pencils-markers-markers-highlighters-n-4467': {'url': '/b/markers-and-highlighters/N-4467',
                                                                                          'name': 'Markers '
                                                                                                  '& '
                                                                                                  'Highlighters',
                                                                                          'sub_category': 'Pens, '
                                                                                                          'Pencils '
                                                                                                          '& '
                                                                                                          'Markers'},
                     'office-supplies-pens-pencils-markers-pencils-n-4504': {'url': '/b/pencils/N-4504',
                                                                             'name': 'Pencils',
                                                                             'sub_category': 'Pens, '
                                                                                             'Pencils '
                                                                                             '& '
                                                                                             'Markers'},
                     'office-supplies-pens-pencils-markers-correction-fluid-tape-n-4404': {'url': '/b/correction-fluid-and-tape/N-4404',
                                                                                           'name': 'Correction '
                                                                                                   'Fluid '
                                                                                                   '& '
                                                                                                   'Tape',
                                                                                           'sub_category': 'Pens, '
                                                                                                           'Pencils '
                                                                                                           '& '
                                                                                                           'Markers'},
                     'office-supplies-filing-folders-n-3469': {'url': '/b/filing-and-folders/N-3469',
                                                               'name': 'Filing & Folders',
                                                               'sub_category': ''},
                     'office-supplies-filing-folders-file-folders-n-3545': {'url': '/b/file-folders/N-3545',
                                                                            'name': 'File Folders',
                                                                            'sub_category': 'Filing '
                                                                                            '& '
                                                                                            'Folders'},
                     'office-supplies-filing-folders-hanging-file-folders-n-3628': {'url': '/b/hanging-file-folders/N-3628',
                                                                                    'name': 'Hanging '
                                                                                            'File '
                                                                                            'Folders',
                                                                                    'sub_category': 'Filing '
                                                                                                    '& '
                                                                                                    'Folders'},
                     'office-supplies-filing-folders-expanding-file-folders-n-3507': {'url': '/b/expanding-file-folders/N-3507',
                                                                                      'name': 'Expanding '
                                                                                              'File '
                                                                                              'Folders',
                                                                                      'sub_category': 'Filing '
                                                                                                      '& '
                                                                                                      'Folders'},
                     'office-supplies-filing-folders-classification-folders-n-1438369': {'url': '/b/classification-folders/N-1438369',
                                                                                         'name': 'Classification '
                                                                                                 'Folders',
                                                                                         'sub_category': 'Filing '
                                                                                                         '& '
                                                                                                         'Folders'},
                     'office-supplies-desk-accessories-n-1170326': {'url': '/b/desk-accessories/N-1170326',
                                                                    'name': 'Desk Accessories',
                                                                    'sub_category': ''},
                     'office-supplies-desk-accessories-desk-organizers-n-1170330': {'url': '/b/desk-organizers/N-1170330',
                                                                                    'name': 'Desk '
                                                                                            'Organizers',
                                                                                    'sub_category': 'Desk '
                                                                                                    'Accessories'},
                     'office-supplies-desk-accessories-desk-trays-n-1170332': {'url': '/b/desk-trays/N-1170332',
                                                                               'name': 'Desk Trays',
                                                                               'sub_category': 'Desk '
                                                                                               'Accessories'},
                     'office-supplies-desk-accessories-file-organizers-n-1170334': {'url': '/b/file-organizers/N-1170334',
                                                                                    'name': 'File '
                                                                                            'Organizers',
                                                                                    'sub_category': 'Desk '
                                                                                                    'Accessories'},
                     'office-supplies-desk-accessories-drawer-organizers-n-1170333': {'url': '/b/drawer-organizers/N-1170333',
                                                                                      'name': 'Drawer '
                                                                                              'Organizers',
                                                                                      'sub_category': 'Desk '
                                                                                                      'Accessories'},
                     'office-supplies-basic-supplies-n-1886': {'url': '/b/basic-supplies/N-1886',
                                                               'name': 'Basic Supplies',
                                                               'sub_category': ''},
                     'office-supplies-basic-supplies-staplers-staples-n-658785': {'url': '/b/staplers-and-staples/N-658785',
                                                                                  'name': 'Staplers '
                                                                                          '& '
                                                                                          'Staples',
                                                                                  'sub_category': 'Basic '
                                                                                                  'Supplies'},
                     'office-supplies-basic-supplies-paper-binder-clips-n-581682': {'url': '/b/paper-clips-binder-clips-and-fasteners/N-581682',
                                                                                    'name': 'Paper '
                                                                                            '& '
                                                                                            'Binder '
                                                                                            'Clips',
                                                                                    'sub_category': 'Basic '
                                                                                                    'Supplies'},
                     'office-supplies-basic-supplies-scissors-n-581693': {'url': '/b/scissors/N-581693',
                                                                          'name': 'Scissors',
                                                                          'sub_category': 'Basic '
                                                                                          'Supplies'},
                     'office-supplies-basic-supplies-paper-punches-cutters-n-658776': {'url': '/b/paper-punches-cutters-and-folding-machines/N-658776',
                                                                                       'name': 'Paper '
                                                                                               'Punches '
                                                                                               '& '
                                                                                               'Cutters',
                                                                                       'sub_category': 'Basic '
                                                                                                       'Supplies'},
                     'office-supplies-binders-accessories-n-2155': {'url': '/b/binders-and-accessories/N-2155',
                                                                    'name': 'Binders & Accessories',
                                                                    'sub_category': ''},
                     'office-supplies-binders-accessories-binders-n-1035691': {'url': '/b/binders/N-1035691',
                                                                               'name': 'Binders',
                                                                               'sub_category': 'Binders '
                                                                                               '& '
                                                                                               'Accessories'},
                     'office-supplies-binders-accessories-dividers-tabs-n-581130': {'url': '/b/dividers-and-tabs/N-581130',
                                                                                    'name': 'Dividers '
                                                                                            '& '
                                                                                            'Tabs',
                                                                                    'sub_category': 'Binders '
                                                                                                    '& '
                                                                                                    'Accessories'},
                     'office-supplies-binders-accessories-report-covers-portfolios-n-567576': {'url': '/b/report-covers-and-portfolios/N-567576',
                                                                                               'name': 'Report '
                                                                                                       'Covers '
                                                                                                       '& '
                                                                                                       'Portfolios',
                                                                                               'sub_category': 'Binders '
                                                                                                               '& '
                                                                                                               'Accessories'},
                     'office-supplies-binders-accessories-sheet-protectors-n-2310': {'url': '/b/sheet-protectors/N-2310',
                                                                                     'name': 'Sheet '
                                                                                             'Protectors',
                                                                                     'sub_category': 'Binders '
                                                                                                     '& '
                                                                                                     'Accessories'},
                     'office-supplies-storage-file-boxes-n-1123257': {'url': '/b/file-boxes/N-1123257',
                                                                      'name': 'File Boxes',
                                                                      'sub_category': 'Storage'},
                     'office-supplies-storage-plastic-storage-containers-n-1123255': {'url': '/b/plastic-storage-containers/N-1123255',
                                                                                      'name': 'Plastic '
                                                                                              'Storage '
                                                                                              'Containers',
                                                                                      'sub_category': 'Storage'},
                     'office-supplies-storage-storage-bins-baskets-n-1123253': {'url': '/b/storage-bins-and-baskets/N-1123253',
                                                                                'name': 'Storage '
                                                                                        'Bins & '
                                                                                        'Baskets',
                                                                                'sub_category': 'Storage'},
                     'office-supplies-storage-storage-drawers-carts-n-1123259': {'url': '/b/storage-drawers-and-carts/N-1123259',
                                                                                 'name': 'Storage '
                                                                                         'Drawers '
                                                                                         '& Carts',
                                                                                 'sub_category': 'Storage'},
                     'office-supplies-mailing-shipping-n-3912': {'url': '/b/mailing-packing-and-shipping/N-3912',
                                                                 'name': 'Mailing & Shipping',
                                                                 'sub_category': ''},
                     'office-supplies-mailing-shipping-envelopes-n-514132': {'url': '/b/envelopes/N-514132',
                                                                             'name': 'Envelopes',
                                                                             'sub_category': 'Mailing '
                                                                                             '& '
                                                                                             'Shipping'},
                     'office-supplies-mailing-shipping-shipping-moving-boxes-n-3913': {'url': '/b/shipping-and-moving-boxes/N-3913',
                                                                                       'name': 'Shipping '
                                                                                               '& '
                                                                                               'Moving '
                                                                                               'Boxes',
                                                                                       'sub_category': 'Mailing '
                                                                                                       '& '
                                                                                                       'Shipping'},
                     'office-supplies-mailing-shipping-mailers-n-530021': {'url': '/b/mailers/N-530021',
                                                                           'name': 'Mailers',
                                                                           'sub_category': 'Mailing '
                                                                                           '& '
                                                                                           'Shipping'},
                     'office-supplies-mailing-shipping-packing-tape-n-4009': {'url': '/b/packing-tape/N-4009',
                                                                              'name': 'Packing '
                                                                                      'Tape',
                                                                              'sub_category': 'Mailing '
                                                                                              '& '
                                                                                              'Shipping'},
                     'office-supplies-mailing-shipping-packing-materials-n-3972': {'url': '/b/packing-materials/N-3972',
                                                                                   'name': 'Packing '
                                                                                           'Materials',
                                                                                   'sub_category': 'Mailing '
                                                                                                   '& '
                                                                                                   'Shipping'},
                     'office-supplies-labels-label-makers-n-1159754': {'url': '/b/labels-and-label-makers/N-1159754',
                                                                       'name': 'Labels & Label '
                                                                               'Makers',
                                                                       'sub_category': ''},
                     'office-supplies-labels-label-makers-standard-labels-n-1159765': {'url': '/b/standard-labels/N-1159765',
                                                                                       'name': 'Standard '
                                                                                               'Labels',
                                                                                       'sub_category': 'Labels '
                                                                                                       '& '
                                                                                                       'Label '
                                                                                                       'Makers'},
                     'office-supplies-labels-label-makers-label-maker-tapes-n-1159761': {'url': '/b/label-maker-tapes/N-1159761',
                                                                                         'name': 'Label '
                                                                                                 'Maker '
                                                                                                 'Tapes',
                                                                                         'sub_category': 'Labels '
                                                                                                         '& '
                                                                                                         'Label '
                                                                                                         'Makers'},
                     'office-supplies-labels-label-makers-address-labels-n-1159755': {'url': '/b/address-labels/N-1159755',
                                                                                      'name': 'Address '
                                                                                              'Labels',
                                                                                      'sub_category': 'Labels '
                                                                                                      '& '
                                                                                                      'Label '
                                                                                                      'Makers'},
                     'office-supplies-labels-label-makers-label-makers-n-1159762': {'url': '/b/label-makers/N-1159762',
                                                                                    'name': 'Label '
                                                                                            'Makers',
                                                                                    'sub_category': 'Labels '
                                                                                                    '& '
                                                                                                    'Label '
                                                                                                    'Makers'},
                     'office-supplies-labels-label-makers-name-badges-holders-n-1159763': {'url': '/b/name-badges-and-holders/N-1159763',
                                                                                           'name': 'Name '
                                                                                                   'Badges '
                                                                                                   '& '
                                                                                                   'Holders',
                                                                                           'sub_category': 'Labels '
                                                                                                           '& '
                                                                                                           'Label '
                                                                                                           'Makers'},
                     'office-supplies-more-ways-to-shop-backpacks-n-535201': {'url': '/b/backpacks/N-535201',
                                                                              'name': 'Backpacks',
                                                                              'sub_category': 'More '
                                                                                              'Ways '
                                                                                              'to '
                                                                                              'Shop'},
                     'office-supplies-more-ways-to-shop-post-it-sticky-notes-n-549832': {'url': '/b/sticky-notes-and-flags/N-549832',
                                                                                         'name': 'Post-It '
                                                                                                 '& '
                                                                                                 'Sticky '
                                                                                                 'Notes',
                                                                                         'sub_category': 'More '
                                                                                                         'Ways '
                                                                                                         'to '
                                                                                                         'Shop'},
                     'office-supplies-more-ways-to-shop-tape-adhesives-n-371557': {'url': '/b/tape-and-adhesives/N-371557',
                                                                                   'name': 'Tape & '
                                                                                           'Adhesives',
                                                                                   'sub_category': 'More '
                                                                                                   'Ways '
                                                                                                   'to '
                                                                                                   'Shop'},
                     'office-supplies-more-ways-to-shop-presentation-boards-n-1677': {'url': '/b/presentation-boards/N-1677',
                                                                                      'name': 'Presentation '
                                                                                              'Boards',
                                                                                      'sub_category': 'More '
                                                                                                      'Ways '
                                                                                                      'to '
                                                                                                      'Shop'}},
 'Furniture': {'furniture-furniture-n-917': {'url': '/b/furniture/N-917',
                                             'name': 'Furniture',
                                             'sub_category': ''},
               'furniture-chairs-seating-n-593061': {'url': '/b/chairs-and-seating/N-593061',
                                                     'name': 'Chairs & Seating',
                                                     'sub_category': ''},
               'furniture-chairs-seating-office-chairs-n-593067': {'url': '/b/office-chairs/N-593067',
                                                                   'name': 'Office Chairs',
                                                                   'sub_category': 'Chairs & '
                                                                                   'Seating'},
               'furniture-chairs-seating-ergonomic-office-chairs-n-593065': {'url': '/b/ergonomic-office-chairs/N-593065',
                                                                             'name': 'Ergonomic '
                                                                                     'Office '
                                                                                     'Chairs',
                                                                             'sub_category': 'Chairs '
                                                                                             '& '
                                                                                             'Seating'},
               'furniture-chairs-seating-task-chairs-n-593071': {'url': '/b/task-chairs/N-593071',
                                                                 'name': 'Task Chairs',
                                                                 'sub_category': 'Chairs & '
                                                                                 'Seating'},
               'furniture-chairs-seating-big-tall-chairs-n-593062': {'url': '/b/big-and-tall-chairs/N-593062',
                                                                     'name': 'Big & Tall Chairs',
                                                                     'sub_category': 'Chairs & '
                                                                                     'Seating'},
               'furniture-chairs-seating-gaming-chairs-n-1302556': {'url': '/b/gaming-chairs/N-1302556',
                                                                    'name': 'Gaming Chairs',
                                                                    'sub_category': 'Chairs & '
                                                                                    'Seating'},
               'furniture-chairs-seating-chair-mats-n-1211740': {'url': '/b/chair-mats-and-floor-mats/N-1211740',
                                                                 'name': 'Chair Mats',
                                                                 'sub_category': 'Chairs & '
                                                                                 'Seating'},
               'furniture-desks-n-501545': {'url': '/b/desks/N-501545',
                                            'name': 'Desks',
                                            'sub_category': ''},
               'furniture-desks-corner-desks-n-553865': {'url': '/b/corner-and-l-shaped-desks/N-553865',
                                                         'name': 'Corner Desks',
                                                         'sub_category': 'Desks'},
               'furniture-desks-computer-desks-n-579905': {'url': '/b/computer-desks/N-579905',
                                                           'name': 'Computer Desks',
                                                           'sub_category': 'Desks'},
               'furniture-desks-executive-desks-n-579907': {'url': '/b/executive-desks/N-579907',
                                                            'name': 'Executive Desks',
                                                            'sub_category': 'Desks'},
               'furniture-desks-standing-desks-n-715982': {'url': '/b/standing-desks/N-715982',
                                                           'name': 'Standing Desks',
                                                           'sub_category': 'Desks'},
               'furniture-desks-commercial-desks-n-501546': {'url': '/b/commercial-grade-desks/N-501546',
                                                             'name': 'Commercial Desks',
                                                             'sub_category': 'Desks'},
               'furniture-desks-student-desks-n-1186187': {'url': '/b/student-desks/N-1186187',
                                                           'name': 'Student Desks',
                                                           'sub_category': 'Desks'},
               'furniture-storage-solutions-file-cabinets-n-1141176': {'url': '/b/file-cabinets/N-1141176',
                                                                       'name': 'File Cabinets',
                                                                       'sub_category': 'Storage '
                                                                                       'Solutions'},
               'furniture-storage-solutions-cabinets-shelving-units-n-533590': {'url': '/b/storage-cabinets-and-shelving-units/N-533590',
                                                                                'name': 'Cabinets '
                                                                                        '& '
                                                                                        'Shelving '
                                                                                        'Units',
                                                                                'sub_category': 'Storage '
                                                                                                'Solutions'},
               'furniture-storage-solutions-bookcases-n-654600': {'url': '/b/bookcases/N-654600',
                                                                  'name': 'Bookcases',
                                                                  'sub_category': 'Storage '
                                                                                  'Solutions'},
               'furniture-storage-solutions-lockers-n-533600': {'url': '/b/lockers/N-533600',
                                                                'name': 'Lockers',
                                                                'sub_category': 'Storage '
                                                                                'Solutions'},
               'furniture-office-decor-n-504392': {'url': '/b/office-decor/N-504392',
                                                   'name': 'Office Decor',
                                                   'sub_category': ''},
               'furniture-lamps-lighting-n-1256962': {'url': '/b/lamps-and-lighting/N-1256962',
                                                      'name': 'Lamps & Lighting',
                                                      'sub_category': ''},
               'furniture-tables-n-501910': {'url': '/b/tables/N-501910',
                                             'name': 'Tables',
                                             'sub_category': ''},
               'furniture-carts-stands-n-501476': {'url': '/b/carts-and-stands/N-501476',
                                                   'name': 'Carts & Stands',
                                                   'sub_category': ''},
               'furniture-furniture-by-work-style-mobile-office-n-579913': {'url': '/b/portable-desks/N-579913',
                                                                            'name': 'Mobile Office',
                                                                            'sub_category': 'Furniture '
                                                                                            'by '
                                                                                            'Work '
                                                                                            'Style'},
               'furniture-furniture-deals-n-917': {'url': '/b/furniture/Featured_Items--On_Sale/N-917',
                                                   'name': 'Furniture Deals',
                                                   'sub_category': ''}},
 'Cleaning': {'cleaning-cleaning-n-530552': {'url': '/b/cleaning/N-530552',
                                             'name': 'Cleaning',
                                             'sub_category': ''},
              'cleaning-cleaning-supplies-n-1477628': {'url': '/b/cleaning-supplies/N-1477628',
                                                       'name': 'Cleaning Supplies',
                                                       'sub_category': ''},
              'cleaning-cleaning-supplies-cleaning-wipes-n-1477632': {'url': '/b/cleaning-wipes/N-1477632',
                                                                      'name': 'Cleaning Wipes',
                                                                      'sub_category': 'Cleaning '
                                                                                      'Supplies'},
              'cleaning-cleaning-supplies-all-purpose-cleaners-n-1477629': {'url': '/b/all-purpose-cleaners/N-1477629',
                                                                            'name': 'All-Purpose '
                                                                                    'Cleaners',
                                                                            'sub_category': 'Cleaning '
                                                                                            'Supplies'},
              'cleaning-cleaning-supplies-dish-detergents-n-1477633': {'url': '/b/dish-detergents/N-1477633',
                                                                       'name': 'Dish Detergents',
                                                                       'sub_category': 'Cleaning '
                                                                                       'Supplies'},
              'cleaning-cleaning-supplies-bathroom-cleaners-n-1477630': {'url': '/b/bathroom-cleaners/N-1477630',
                                                                         'name': 'Bathroom '
                                                                                 'Cleaners',
                                                                         'sub_category': 'Cleaning '
                                                                                         'Supplies'},
              'cleaning-cleaning-supplies-glass-cleaners-n-1477636': {'url': '/b/glass-cleaners/N-1477636',
                                                                      'name': 'Glass Cleaners',
                                                                      'sub_category': 'Cleaning '
                                                                                      'Supplies'},
              'cleaning-paper-products-toilet-paper-n-1170289': {'url': '/b/toilet-paper/N-1170289',
                                                                 'name': 'Toilet Paper',
                                                                 'sub_category': 'Paper Products'},
              'cleaning-paper-products-paper-towel-rolls-n-1170288': {'url': '/b/paper-towels/Item_Type--Paper_Towel_Roll/N-1170288',
                                                                      'name': 'Paper Towel Rolls',
                                                                      'sub_category': 'Paper '
                                                                                      'Products'},
              'cleaning-paper-products-c-fold-towels-n-1170288': {'url': '/b/paper-towels/Fold_Type--C_Fold/N-1170288',
                                                                  'name': 'C-Fold Towels',
                                                                  'sub_category': 'Paper Products'},
              'cleaning-paper-products-multifold-towels-n-1170288': {'url': '/b/paper-towels/Fold_Type--Multi_Fold/N-1170288',
                                                                     'name': 'Multifold Towels',
                                                                     'sub_category': 'Paper '
                                                                                     'Products'},
              'cleaning-paper-products-facial-tissues-n-1170285': {'url': '/b/facial-tissues/N-1170285',
                                                                   'name': 'Facial Tissues',
                                                                   'sub_category': 'Paper '
                                                                                   'Products'},
              'cleaning-cleaning-tools-n-1176181': {'url': '/b/cleaning-tools/N-1176181',
                                                    'name': 'Cleaning Tools',
                                                    'sub_category': ''},
              'cleaning-cleaning-tools-floor-care-n-1176186': {'url': '/b/floor-care/N-1176186',
                                                               'name': 'Floor Care',
                                                               'sub_category': 'Cleaning Tools'},
              'cleaning-cleaning-tools-dusters-n-1176185': {'url': '/b/dusters/N-1176185',
                                                            'name': 'Dusters',
                                                            'sub_category': 'Cleaning Tools'},
              'cleaning-cleaning-tools-sponges-n-1176188': {'url': '/b/sponges/N-1176188',
                                                            'name': 'Sponges',
                                                            'sub_category': 'Cleaning Tools'},
              'cleaning-cleaning-tools-cloths-n-1176184': {'url': '/b/cloths/N-1176184',
                                                           'name': 'Cloths',
                                                           'sub_category': 'Cleaning Tools'},
              'cleaning-trash-cans-bags-n-1170290': {'url': '/b/trash-cans-and-bags/N-1170290',
                                                     'name': 'Trash Cans & Bags',
                                                     'sub_category': ''},
              'cleaning-trash-cans-bags-trash-cans-n-1170293': {'url': '/b/trash-cans/N-1170293',
                                                                'name': 'Trash Cans',
                                                                'sub_category': 'Trash Cans & '
                                                                                'Bags'},
              'cleaning-trash-cans-bags-trash-bags-n-1170292': {'url': '/b/trash-bags/N-1170292',
                                                                'name': 'Trash Bags',
                                                                'sub_category': 'Trash Cans & '
                                                                                'Bags'},
              'cleaning-trash-cans-bags-recycle-bins-n-1170291': {'url': '/b/recycle-bins/N-1170291',
                                                                  'name': 'Recycle Bins',
                                                                  'sub_category': 'Trash Cans & '
                                                                                  'Bags'},
              'cleaning-soaps-sanitizers-hand-soap-n-1170287': {'url': '/b/hand-soap/N-1170287',
                                                                'name': 'Hand Soap',
                                                                'sub_category': 'Soaps & '
                                                                                'Sanitizers'},
              'cleaning-soaps-sanitizers-hand-soap-refills-n-1170287': {'url': '/b/hand-soap/Product_Type--Soap_Dispenser_Refill/N-1170287',
                                                                        'name': 'Hand Soap Refills',
                                                                        'sub_category': 'Soaps & '
                                                                                        'Sanitizers'},
              'cleaning-soaps-sanitizers-soap-dispensers-n-1170287': {'url': '/b/hand-soap/Type--Counter_Dispenser/Type--Mountable_Dispenser/Type--Touchless_Soap_Dispenser/N-1170287',
                                                                      'name': 'Soap Dispensers',
                                                                      'sub_category': 'Soaps & '
                                                                                      'Sanitizers'},
              'cleaning-soaps-sanitizers-hand-sanitizer-n-1170286': {'url': '/b/hand-sanitizers/N-1170286',
                                                                     'name': 'Hand Sanitizer',
                                                                     'sub_category': 'Soaps & '
                                                                                     'Sanitizers'},
              'cleaning-air-fresheners-n-1176180': {'url': '/b/air-fresheners/N-1176180',
                                                    'name': 'Air Fresheners',
                                                    'sub_category': ''},
              'cleaning-air-fresheners-air-freshener-spray-n-1176180': {'url': '/b/air-fresheners/Product_Type--Air_Freshener_Spray/N-1176180',
                                                                        'name': 'Air Freshener '
                                                                                'Spray',
                                                                        'sub_category': 'Air '
                                                                                        'Fresheners'},
              'cleaning-air-fresheners-freshener-refills-n-1176180': {'url': '/b/air-fresheners/Product_Type--Air_Freshener_Dispenser_Refill/N-1176180',
                                                                      'name': 'Freshener Refills',
                                                                      'sub_category': 'Air '
                                                                                      'Fresheners'},
              'cleaning-medical-supplies-n-654427': {'url': '/b/medical-supplies/N-654427',
                                                     'name': 'Medical Supplies',
                                                     'sub_category': ''},
              'cleaning-medical-supplies-measuring-devices-n-1181082': {'url': '/b/diagnostic/N-1181082',
                                                                        'name': 'Measuring Devices',
                                                                        'sub_category': 'Medical '
                                                                                        'Supplies'},
              'cleaning-medical-supplies-infection-control-n-1181095': {'url': '/b/infection-control/N-1181095',
                                                                        'name': 'Infection Control',
                                                                        'sub_category': 'Medical '
                                                                                        'Supplies'},
              'cleaning-medical-supplies-medical-wear-n-1181107': {'url': '/b/medical-wear/N-1181107',
                                                                   'name': 'Medical Wear',
                                                                   'sub_category': 'Medical '
                                                                                   'Supplies'},
              'cleaning-medical-supplies-patient-care-n-1181126': {'url': '/b/patient-care/N-1181126',
                                                                   'name': 'Patient Care',
                                                                   'sub_category': 'Medical '
                                                                                   'Supplies'},
              'cleaning-medical-supplies-wound-care-n-1181163': {'url': '/b/wound-care/N-1181163',
                                                                 'name': 'Wound Care',
                                                                 'sub_category': 'Medical '
                                                                                 'Supplies'},
              'cleaning-safety-security-n-654510': {'url': '/b/safety-and-security/N-654510',
                                                    'name': 'Safety & Security',
                                                    'sub_category': ''},
              'cleaning-safety-security-eye-protection-n-654523': {'url': '/b/eye-protection/N-654523',
                                                                   'name': 'Eye Protection',
                                                                   'sub_category': 'Safety & '
                                                                                   'Security'},
              'cleaning-safety-security-gloves-hand-protection-n-654548': {'url': '/b/gloves-and-hand-protection/N-654548',
                                                                           'name': 'Gloves & Hand '
                                                                                   'Protection',
                                                                           'sub_category': 'Safety '
                                                                                           '& '
                                                                                           'Security'},
              'cleaning-safety-security-head-face-protection-n-654551': {'url': '/b/head-and-face-protection/N-654551',
                                                                         'name': 'Head & Face '
                                                                                 'Protection',
                                                                         'sub_category': 'Safety & '
                                                                                         'Security'},
              'cleaning-safety-security-respiratory-protection-n-654565': {'url': '/b/respiratory-protection/N-654565',
                                                                           'name': 'Respiratory '
                                                                                   'Protection',
                                                                           'sub_category': 'Safety '
                                                                                           '& '
                                                                                           'Security'}},
 'Breakroom': {'breakroom-breakroom-n-530419': {'url': '/b/breakroom/N-530419',
                                                'name': 'Breakroom',
                                                'sub_category': ''},
               'breakroom-coffee-coffee-supplies-n-1154872': {'url': '/b/coffee-and-coffee-supplies/N-1154872',
                                                              'name': 'Coffee & Coffee Supplies',
                                                              'sub_category': ''},
               'breakroom-coffee-coffee-supplies-coffee-n-1154874': {'url': '/b/coffee/N-1154874',
                                                                     'name': 'Coffee',
                                                                     'sub_category': 'Coffee & '
                                                                                     'Coffee '
                                                                                     'Supplies'},
               'breakroom-coffee-coffee-supplies-coffee-makers-n-1176154': {'url': '/b/coffee-makers/N-1176154',
                                                                            'name': 'Coffee Makers',
                                                                            'sub_category': 'Coffee '
                                                                                            '& '
                                                                                            'Coffee '
                                                                                            'Supplies'},
               'breakroom-coffee-coffee-supplies-creamers-n-1154878': {'url': '/b/creamers/N-1154878',
                                                                       'name': 'Creamers',
                                                                       'sub_category': 'Coffee & '
                                                                                       'Coffee '
                                                                                       'Supplies'},
               'breakroom-coffee-coffee-supplies-sugar-sweeteners-n-1154881': {'url': '/b/sugar-and-sweeteners/N-1154881',
                                                                               'name': 'Sugar & '
                                                                                       'Sweeteners',
                                                                               'sub_category': 'Coffee '
                                                                                               '& '
                                                                                               'Coffee '
                                                                                               'Supplies'},
               'breakroom-coffee-coffee-supplies-hot-cups-lids-n-1154879': {'url': '/b/hot-cups-and-lids/N-1154879',
                                                                            'name': 'Hot Cups & '
                                                                                    'Lids',
                                                                            'sub_category': 'Coffee '
                                                                                            '& '
                                                                                            'Coffee '
                                                                                            'Supplies'},
               'breakroom-fresh-frozen-food-n-1418020': {'url': '/b/fresh-and-frozen-foods/N-1418020',
                                                         'name': 'Fresh & Frozen Food',
                                                         'sub_category': ''},
               'breakroom-fresh-frozen-food-bakery-breads-n-1418021': {'url': '/b/bakery-and-breads/N-1418021',
                                                                       'name': 'Bakery & Breads',
                                                                       'sub_category': 'Fresh & '
                                                                                       'Frozen '
                                                                                       'Food'},
               'breakroom-fresh-frozen-food-breakfast-cereal-n-1418022': {'url': '/b/breakfast-and-cereal/N-1418022',
                                                                          'name': 'Breakfast & '
                                                                                  'Cereal',
                                                                          'sub_category': 'Fresh & '
                                                                                          'Frozen '
                                                                                          'Food'},
               'breakroom-fresh-frozen-food-dairy-n-1418023': {'url': '/b/dairy/N-1418023',
                                                               'name': 'Dairy',
                                                               'sub_category': 'Fresh & Frozen '
                                                                               'Food'},
               'breakroom-fresh-frozen-food-frozen-meals-snacks-n-1418024': {'url': '/b/frozen-meals-and-snacks/N-1418024',
                                                                             'name': 'Frozen Meals '
                                                                                     '& Snacks',
                                                                             'sub_category': 'Fresh '
                                                                                             '& '
                                                                                             'Frozen '
                                                                                             'Food'},
               'breakroom-fresh-frozen-food-fruits-vegetables-n-1418025': {'url': '/b/fruits-and-vegetables/N-1418025',
                                                                           'name': 'Fruits & '
                                                                                   'Vegetables',
                                                                           'sub_category': 'Fresh '
                                                                                           '& '
                                                                                           'Frozen '
                                                                                           'Food'},
               'breakroom-candy-snacks-n-1418009': {'url': '/b/candy-and-snacks/N-1418009',
                                                    'name': 'Candy & Snacks',
                                                    'sub_category': ''},
               'breakroom-candy-snacks-chips-pretzels-n-1418010': {'url': '/b/chips-and-pretzels/N-1418010',
                                                                   'name': 'Chips & Pretzels',
                                                                   'sub_category': 'Candy & '
                                                                                   'Snacks'},
               'breakroom-candy-snacks-chocolate-caramels-n-1418011': {'url': '/b/chocolate-and-caramels/N-1418011',
                                                                       'name': 'Chocolate & '
                                                                               'Caramels',
                                                                       'sub_category': 'Candy & '
                                                                                       'Snacks'},
               'breakroom-candy-snacks-cookies-n-1418012': {'url': '/b/cookies/N-1418012',
                                                            'name': 'Cookies',
                                                            'sub_category': 'Candy & Snacks'},
               'breakroom-candy-snacks-crackers-n-1418013': {'url': '/b/crackers/N-1418013',
                                                             'name': 'Crackers',
                                                             'sub_category': 'Candy & Snacks'},
               'breakroom-candy-snacks-gum-mints-n-1418015': {'url': '/b/gum-and-mints/N-1418015',
                                                              'name': 'Gum & Mints',
                                                              'sub_category': 'Candy & Snacks'},
               'breakroom-cups-plates-cutlery-n-1176169': {'url': '/b/cups-plates-and-cutlery/N-1176169',
                                                           'name': 'Cups, Plates & Cutlery',
                                                           'sub_category': ''},
               'breakroom-cups-plates-cutlery-cups-n-1176172': {'url': '/b/cups/N-1176172',
                                                                'name': 'Cups',
                                                                'sub_category': 'Cups, Plates & '
                                                                                'Cutlery'},
               'breakroom-cups-plates-cutlery-plates-n-1176177': {'url': '/b/plates/N-1176177',
                                                                  'name': 'Plates',
                                                                  'sub_category': 'Cups, Plates & '
                                                                                  'Cutlery'},
               'breakroom-cups-plates-cutlery-cutlery-n-1176173': {'url': '/b/cutlery/N-1176173',
                                                                   'name': 'Cutlery',
                                                                   'sub_category': 'Cups, Plates & '
                                                                                   'Cutlery'},
               'breakroom-cups-plates-cutlery-cooking-utensils-n-1176171': {'url': '/b/cooking-utensils/N-1176171',
                                                                            'name': 'Cooking '
                                                                                    'Utensils',
                                                                            'sub_category': 'Cups, '
                                                                                            'Plates '
                                                                                            '& '
                                                                                            'Cutlery'},
               'breakroom-cups-plates-cutlery-bowls-n-1176170': {'url': '/b/bowls/N-1176170',
                                                                 'name': 'Bowls',
                                                                 'sub_category': 'Cups, Plates & '
                                                                                 'Cutlery'},
               'breakroom-beverages-n-1154865': {'url': '/b/beverages/N-1154865',
                                                 'name': 'Beverages',
                                                 'sub_category': ''},
               'breakroom-beverages-water-n-1154871': {'url': '/b/water/N-1154871',
                                                       'name': 'Water',
                                                       'sub_category': 'Beverages'},
               'breakroom-beverages-soda-n-1154869': {'url': '/b/soda/N-1154869',
                                                      'name': 'Soda',
                                                      'sub_category': 'Beverages'},
               'breakroom-beverages-juice-n-1154868': {'url': '/b/juice/N-1154868',
                                                       'name': 'Juice',
                                                       'sub_category': 'Beverages'},
               'breakroom-beverages-tea-n-1154870': {'url': '/b/tea/N-1154870',
                                                     'name': 'Tea',
                                                     'sub_category': 'Beverages'},
               'breakroom-beverages-energy-nutrition-drinks-n-1154866': {'url': '/b/energy-and-nutrition-drinks/N-1154866',
                                                                         'name': 'Energy & '
                                                                                 'Nutrition Drinks',
                                                                         'sub_category': 'Beverages'},
               'breakroom-appliances-n-530420': {'url': '/b/appliances/N-530420',
                                                 'name': 'Appliances',
                                                 'sub_category': ''},
               'breakroom-appliances-heating-cooling-n-1176144': {'url': '/b/heating-and-cooling/N-1176144',
                                                                  'name': 'Heating & Cooling',
                                                                  'sub_category': 'Appliances'},
               'breakroom-appliances-kitchen-n-1176150': {'url': '/b/kitchen/N-1176150',
                                                          'name': 'Kitchen',
                                                          'sub_category': 'Appliances'},
               'breakroom-appliances-laundry-n-1176164': {'url': '/b/laundry/N-1176164',
                                                          'name': 'Laundry',
                                                          'sub_category': 'Appliances'}},
 'Computers & Accessories': {'computers-accessories-computers-accessories-n-1461888': {'url': '/b/computers-and-accessories/N-1461888',
                                                                                       'name': 'Computers '
                                                                                               '& '
                                                                                               'Accessories',
                                                                                       'sub_category': ''},
                             'computers-accessories-computers-laptop-computers-n-1462020': {'url': '/b/laptop-computers/N-1462020',
                                                                                            'name': 'Laptop '
                                                                                                    'Computers',
                                                                                            'sub_category': 'Computers'},
                             'computers-accessories-computers-desktop-computers-n-1461989': {'url': '/b/desktop-computers/N-1461989',
                                                                                             'name': 'Desktop '
                                                                                                     'Computers',
                                                                                             'sub_category': 'Computers'},
                             'computers-accessories-computers-all-in-one-computers-n-1461990': {'url': '/b/all-in-one-computers/N-1461990',
                                                                                                'name': 'All-in-One '
                                                                                                        'Computers',
                                                                                                'sub_category': 'Computers'},
                             'computers-accessories-computers-business-desktops-n-1461993': {'url': '/b/business-desktops/N-1461993',
                                                                                             'name': 'Business '
                                                                                                     'Desktops',
                                                                                             'sub_category': 'Computers'},
                             'computers-accessories-computers-monitors-accessories-n-1462029': {'url': '/b/monitors-and-accessories/N-1462029',
                                                                                                'name': 'Monitors '
                                                                                                        '& '
                                                                                                        'Accessories',
                                                                                                'sub_category': 'Computers'},
                             'computers-accessories-computer-accessories-n-1461889': {'url': '/b/computer-accessories/N-1461889',
                                                                                      'name': 'Computer '
                                                                                              'Accessories',
                                                                                      'sub_category': ''},
                             'computers-accessories-computer-accessories-mice-keyboards-n-1461905': {'url': '/b/mice-and-keyboards/N-1461905',
                                                                                                     'name': 'Mice '
                                                                                                             '& '
                                                                                                             'Keyboards',
                                                                                                     'sub_category': 'Computer '
                                                                                                                     'Accessories'},
                             'computers-accessories-computer-accessories-mousepads-wrist-rests-n-1461910': {'url': '/b/mousepads-and-wrist-rests/N-1461910',
                                                                                                            'name': 'Mousepads '
                                                                                                                    '& '
                                                                                                                    'Wrist '
                                                                                                                    'Rests',
                                                                                                            'sub_category': 'Computer '
                                                                                                                            'Accessories'},
                             'computers-accessories-computer-accessories-computer-speakers-headsets-n-1461893': {'url': '/b/computer-speakers-and-headsets/N-1461893',
                                                                                                                 'name': 'Computer '
                                                                                                                         'Speakers '
                                                                                                                         '& '
                                                                                                                         'Headsets',
                                                                                                                 'sub_category': 'Computer '
                                                                                                                                 'Accessories'},
                             'computers-accessories-computer-accessories-compressed-air-dusters-n-1504673': {'url': '/b/compressed-air-dusters/N-1504673',
                                                                                                             'name': 'Compressed '
                                                                                                                     'Air '
                                                                                                                     'Dusters',
                                                                                                             'sub_category': 'Computer '
                                                                                                                             'Accessories'},
                             'computers-accessories-computer-accessories-laptop-accessories-n-1461898': {'url': '/b/laptop-accessories/N-1461898',
                                                                                                         'name': 'Laptop '
                                                                                                                 'Accessories',
                                                                                                         'sub_category': 'Computer '
                                                                                                                         'Accessories'},
                             'computers-accessories-software-n-1462054': {'url': '/b/software/N-1462054',
                                                                          'name': 'Software',
                                                                          'sub_category': ''},
                             'computers-accessories-software-business-software-n-1462062': {'url': '/b/business-software/N-1462062',
                                                                                            'name': 'Business '
                                                                                                    'Software',
                                                                                            'sub_category': 'Software'},
                             'computers-accessories-software-finance-legal-software-n-1462079': {'url': '/b/finance-and-legal-software/N-1462079',
                                                                                                 'name': 'Finance '
                                                                                                         '& '
                                                                                                         'Legal '
                                                                                                         'Software',
                                                                                                 'sub_category': 'Software'},
                             'computers-accessories-software-antivirus-utilities-software-n-1462055': {'url': '/b/antivirus-security-and-utilities-software/N-1462055',
                                                                                                       'name': 'Antivirus '
                                                                                                               '& '
                                                                                                               'Utilities '
                                                                                                               'Software',
                                                                                                       'sub_category': 'Software'},
                             'computers-accessories-software-education-software-n-1462075': {'url': '/b/education-software/N-1462075',
                                                                                             'name': 'Education '
                                                                                                     'Software',
                                                                                             'sub_category': 'Software'},
                             'computers-accessories-software-editing-software-n-1462071': {'url': '/b/editing-software/N-1462071',
                                                                                           'name': 'Editing '
                                                                                                   'Software',
                                                                                           'sub_category': 'Software'},
                             'computers-accessories-printers-accessories-n-1462036': {'url': '/b/printers-and-accessories/N-1462036',
                                                                                      'name': 'Printers '
                                                                                              '& '
                                                                                              'Accessories',
                                                                                      'sub_category': ''},
                             'computers-accessories-printers-accessories-laser-printers-n-1462042': {'url': '/b/laser-printers/N-1462042',
                                                                                                     'name': 'Laser '
                                                                                                             'Printers',
                                                                                                     'sub_category': 'Printers '
                                                                                                                     '& '
                                                                                                                     'Accessories'},
                             'computers-accessories-printers-accessories-inkjet-printers-n-1462040': {'url': '/b/inkjet-printers/N-1462040',
                                                                                                      'name': 'Inkjet '
                                                                                                              'Printers',
                                                                                                      'sub_category': 'Printers '
                                                                                                                      '& '
                                                                                                                      'Accessories'},
                             'computers-accessories-printers-accessories-all-in-one-printers-n-1462038': {'url': '/b/all-in-one-printers/N-1462038',
                                                                                                          'name': 'All-in-One '
                                                                                                                  'Printers',
                                                                                                          'sub_category': 'Printers '
                                                                                                                          '& '
                                                                                                                          'Accessories'},
                             'computers-accessories-printers-accessories-supertank-printers-n-1462045': {'url': '/b/supertank-printers/N-1462045',
                                                                                                         'name': 'Supertank '
                                                                                                                 'Printers',
                                                                                                         'sub_category': 'Printers '
                                                                                                                         '& '
                                                                                                                         'Accessories'},
                             'computers-accessories-computer-components-n-1461921': {'url': '/b/computer-cards-and-components/N-1461921',
                                                                                     'name': 'Computer '
                                                                                             'Components',
                                                                                     'sub_category': ''},
                             'computers-accessories-computer-components-graphic-sound-cards-n-1461933': {'url': '/b/graphic-and-sound-cards/N-1461933',
                                                                                                         'name': 'Graphic '
                                                                                                                 '& '
                                                                                                                 'Sound '
                                                                                                                 'Cards',
                                                                                                         'sub_category': 'Computer '
                                                                                                                         'Components'},
                             'computers-accessories-computer-components-motherboards-n-1461943': {'url': '/b/motherboards/N-1461943',
                                                                                                  'name': 'Motherboards',
                                                                                                  'sub_category': 'Computer '
                                                                                                                  'Components'},
                             'computers-accessories-computer-components-memory-n-1461936': {'url': '/b/memory/N-1461936',
                                                                                            'name': 'Memory',
                                                                                            'sub_category': 'Computer '
                                                                                                            'Components'},
                             'computers-accessories-computer-components-computer-cooling-n-1461924': {'url': '/b/computer-cooling/N-1461924',
                                                                                                      'name': 'Computer '
                                                                                                              'Cooling',
                                                                                                      'sub_category': 'Computer '
                                                                                                                      'Components'},
                             'computers-accessories-computer-components-computer-power-supplies-n-1461927': {'url': '/b/computer-power-supplies/N-1461927',
                                                                                                             'name': 'Computer '
                                                                                                                     'Power '
                                                                                                                     'Supplies',
                                                                                                             'sub_category': 'Computer '
                                                                                                                             'Components'},
                             'computers-accessories-data-storage-media-n-1461951': {'url': '/b/data-storage-and-media/N-1461951',
                                                                                    'name': 'Data '
                                                                                            'Storage '
                                                                                            '& '
                                                                                            'Media',
                                                                                    'sub_category': ''},
                             'computers-accessories-data-storage-media-usb-flash-drives-n-1461987': {'url': '/b/usb-flash-drives/N-1461987',
                                                                                                     'name': 'USB '
                                                                                                             'Flash '
                                                                                                             'Drives',
                                                                                                     'sub_category': 'Data '
                                                                                                                     'Storage '
                                                                                                                     '& '
                                                                                                                     'Media'},
                             'computers-accessories-data-storage-media-external-hard-drives-n-1461964': {'url': '/b/external-hard-drives/N-1461964',
                                                                                                         'name': 'External '
                                                                                                                 'Hard '
                                                                                                                 'Drives',
                                                                                                         'sub_category': 'Data '
                                                                                                                         'Storage '
                                                                                                                         '& '
                                                                                                                         'Media'},
                             'computers-accessories-data-storage-media-internal-hard-drives-n-1461965': {'url': '/b/internal-hard-drives/N-1461965',
                                                                                                         'name': 'Internal '
                                                                                                                 'Hard '
                                                                                                                 'Drives',
                                                                                                         'sub_category': 'Data '
                                                                                                                         'Storage '
                                                                                                                         '& '
                                                                                                                         'Media'},
                             'computers-accessories-data-storage-media-solid-state-drives-n-1461967': {'url': '/b/solid-state-drives/N-1461967',
                                                                                                       'name': 'Solid '
                                                                                                               'State '
                                                                                                               'Drives',
                                                                                                       'sub_category': 'Data '
                                                                                                                       'Storage '
                                                                                                                       '& '
                                                                                                                       'Media'},
                             'computers-accessories-data-storage-media-discs-cartridges-n-1461968': {'url': '/b/media/N-1461968',
                                                                                                     'name': 'Discs '
                                                                                                             '& '
                                                                                                             'Cartridges',
                                                                                                     'sub_category': 'Data '
                                                                                                                     'Storage '
                                                                                                                     '& '
                                                                                                                     'Media'}},
 'Printers & Scanners': {'printers-scanners-printers-scanners-n-1462036': {'url': '/b/printers-and-accessories/N-1462036',
                                                                           'name': 'Printers & '
                                                                                   'Scanners',
                                                                           'sub_category': ''},
                         'printers-scanners-shop-by-use-commercial-printers-n-1462036': {'url': '/b/printers-and-accessories/Printer_Use--Commercial/N-1462036',
                                                                                         'name': 'Commercial '
                                                                                                 'Printers',
                                                                                         'sub_category': 'Shop '
                                                                                                         'By '
                                                                                                         'Use'},
                         'printers-scanners-shop-by-use-home-printers-n-1462036': {'url': '/b/printers-and-accessories/Printer_Use--Home_Office/N-1462036',
                                                                                   'name': 'Home '
                                                                                           'Printers',
                                                                                   'sub_category': 'Shop '
                                                                                                   'By '
                                                                                                   'Use'},
                         'printers-scanners-shop-by-use-office-printers-n-1462036': {'url': '/b/printers-and-accessories/Printer_Use--Medium_Business/Printer_Use--Small_Business/N-1462036',
                                                                                     'name': 'Office '
                                                                                             'Printers',
                                                                                     'sub_category': 'Shop '
                                                                                                     'By '
                                                                                                     'Use'},
                         'printers-scanners-shop-by-use-all-printer-deals-n-1462036': {'url': '/b/printers-and-accessories/Featured_Items--On_Sale/N-1462036',
                                                                                       'name': 'All '
                                                                                               'Printer '
                                                                                               'Deals',
                                                                                       'sub_category': 'Shop '
                                                                                                       'By '
                                                                                                       'Use'},
                         'printers-scanners-shop-by-functionality-black-white-printers-n-1462036': {'url': '/b/printers-and-accessories/Print_Color--Black_XaX_White/N-1462036',
                                                                                                    'name': 'Black '
                                                                                                            '& '
                                                                                                            'White '
                                                                                                            'Printers',
                                                                                                    'sub_category': 'Shop '
                                                                                                                    'By '
                                                                                                                    'Functionality'},
                         'printers-scanners-shop-by-functionality-color-printers-n-1462036': {'url': '/b/printers-and-accessories/Print_Color--Color/N-1462036',
                                                                                              'name': 'Color '
                                                                                                      'Printers',
                                                                                              'sub_category': 'Shop '
                                                                                                              'By '
                                                                                                              'Functionality'},
                         'printers-scanners-shop-by-functionality-duplex-printers-n-1462036': {'url': '/b/printers-and-accessories/Duplex_Printing--Automatic/Duplex_Printing--Manual/N-1462036',
                                                                                               'name': 'Duplex '
                                                                                                       'Printers',
                                                                                               'sub_category': 'Shop '
                                                                                                               'By '
                                                                                                               'Functionality'},
                         'printers-scanners-shop-by-functionality-photo-printers-n-1462380': {'url': '/b/photo-printers/N-1462380',
                                                                                              'name': 'Photo '
                                                                                                      'Printers',
                                                                                              'sub_category': 'Shop '
                                                                                                              'By '
                                                                                                              'Functionality'},
                         'printers-scanners-shop-by-functionality-portable-printers-n-1462036': {'url': '/b/printers-and-accessories/Features--Portable/N-1462036',
                                                                                                 'name': 'Portable '
                                                                                                         'Printers',
                                                                                                 'sub_category': 'Shop '
                                                                                                                 'By '
                                                                                                                 'Functionality'},
                         'printers-scanners-shop-by-functionality-supertank-printers-n-1462045': {'url': '/b/supertank-printers/N-1462045',
                                                                                                  'name': 'Supertank '
                                                                                                          'Printers',
                                                                                                  'sub_category': 'Shop '
                                                                                                                  'By '
                                                                                                                  'Functionality'},
                         'printers-scanners-shop-by-functionality-wide-format-printers-n-1462036': {'url': '/b/printers-and-accessories/Maximum_Sheet_Size--LedgerXsXTabloid_XoX11XdX_x_17XdXXcX/Maximum_Sheet_Size--Nonstandard/Maximum_Sheet_Size--13XdX_x_19XdX/N-1462036',
                                                                                                    'name': 'Wide '
                                                                                                            'Format '
                                                                                                            'Printers',
                                                                                                    'sub_category': 'Shop '
                                                                                                                    'By '
                                                                                                                    'Functionality'},
                         'printers-scanners-shop-by-functionality-wireless-printers-n-1462036': {'url': '/b/printers-and-accessories/Features--Wireless/N-1462036',
                                                                                                 'name': 'Wireless '
                                                                                                         'Printers',
                                                                                                 'sub_category': 'Shop '
                                                                                                                 'By '
                                                                                                                 'Functionality'},
                         'printers-scanners-shop-by-type-all-in-one-printers-n-1462038': {'url': '/b/all-in-one-printers/N-1462038',
                                                                                          'name': 'All-In-One '
                                                                                                  'Printers',
                                                                                          'sub_category': 'Shop '
                                                                                                          'By '
                                                                                                          'Type'},
                         'printers-scanners-shop-by-type-dot-matrix-printers-n-1462039': {'url': '/b/dot-matrix-printers/N-1462039',
                                                                                          'name': 'Dot '
                                                                                                  'Matrix '
                                                                                                  'Printers',
                                                                                          'sub_category': 'Shop '
                                                                                                          'By '
                                                                                                          'Type'},
                         'printers-scanners-shop-by-type-inkjet-printers-n-1462040': {'url': '/b/inkjet-printers/N-1462040',
                                                                                      'name': 'Inkjet '
                                                                                              'Printers',
                                                                                      'sub_category': 'Shop '
                                                                                                      'By '
                                                                                                      'Type'},
                         'printers-scanners-shop-by-type-large-format-printers-n-1462041': {'url': '/b/large-format-printers/N-1462041',
                                                                                            'name': 'Large '
                                                                                                    'Format '
                                                                                                    'Printers',
                                                                                            'sub_category': 'Shop '
                                                                                                            'By '
                                                                                                            'Type'},
                         'printers-scanners-shop-by-type-laser-printers-n-1462042': {'url': '/b/laser-printers/N-1462042',
                                                                                     'name': 'Laser '
                                                                                             'Printers',
                                                                                     'sub_category': 'Shop '
                                                                                                     'By '
                                                                                                     'Type'},
                         'printers-scanners-shop-by-type-led-printers-n-1462043': {'url': '/b/led-printers/N-1462043',
                                                                                   'name': 'LED '
                                                                                           'Printers',
                                                                                   'sub_category': 'Shop '
                                                                                                   'By '
                                                                                                   'Type'},
                         'printers-scanners-shop-by-type-thermal-printers-n-1462046': {'url': '/b/thermal-printers/N-1462046',
                                                                                       'name': 'Thermal '
                                                                                               'Printers',
                                                                                       'sub_category': 'Shop '
                                                                                                       'By '
                                                                                                       'Type'},
                         'printers-scanners-shop-by-type-shop-all-printers-n-1462036': {'url': '/b/printers-and-accessories/N-1462036',
                                                                                        'name': 'Shop '
                                                                                                'All '
                                                                                                'Printers',
                                                                                        'sub_category': 'Shop '
                                                                                                        'By '
                                                                                                        'Type'},
                         'printers-scanners-printers-by-brand-brother-printers-n-1462036': {'url': '/b/printers-and-accessories/Brand--Brother/N-1462036',
                                                                                            'name': 'Brother '
                                                                                                    'Printers',
                                                                                            'sub_category': 'Printers '
                                                                                                            'By '
                                                                                                            'Brand'},
                         'printers-scanners-printers-by-brand-canon-printers-n-1462036': {'url': '/b/printers-and-accessories/Brand--Canon/N-1462036',
                                                                                          'name': 'Canon '
                                                                                                  'Printers',
                                                                                          'sub_category': 'Printers '
                                                                                                          'By '
                                                                                                          'Brand'},
                         'printers-scanners-printers-by-brand-epson-printers-n-1462036': {'url': '/b/printers-and-accessories/Brand--Epson/N-1462036',
                                                                                          'name': 'Epson '
                                                                                                  'Printers',
                                                                                          'sub_category': 'Printers '
                                                                                                          'By '
                                                                                                          'Brand'},
                         'printers-scanners-printers-by-brand-hp-printers-n-1462036': {'url': '/b/printers-and-accessories/Brand--HP/N-1462036',
                                                                                       'name': 'HP '
                                                                                               'Printers',
                                                                                       'sub_category': 'Printers '
                                                                                                       'By '
                                                                                                       'Brand'},
                         'printers-scanners-printers-by-brand-lexmark-printers-n-1462036': {'url': '/b/printers-and-accessories/Brand--Lexmark/N-1462036',
                                                                                            'name': 'Lexmark '
                                                                                                    'Printers',
                                                                                            'sub_category': 'Printers '
                                                                                                            'By '
                                                                                                            'Brand'},
                         'printers-scanners-printers-by-brand-xerox-printers-n-1462036': {'url': '/b/printers-and-accessories/Brand--Xerox/N-1462036',
                                                                                          'name': 'Xerox '
                                                                                                  'Printers',
                                                                                          'sub_category': 'Printers '
                                                                                                          'By '
                                                                                                          'Brand'},
                         'printers-scanners-ink-toner-by-brand-brother-ink-toner-n-1462019': {'url': '/b/ink-and-toner/Brand--Brother/N-1462019',
                                                                                              'name': 'Brother '
                                                                                                      'Ink '
                                                                                                      '& '
                                                                                                      'Toner',
                                                                                              'sub_category': 'Ink '
                                                                                                              '& '
                                                                                                              'Toner '
                                                                                                              'By '
                                                                                                              'Brand'},
                         'printers-scanners-ink-toner-by-brand-canon-ink-toner-n-1462019': {'url': '/b/ink-and-toner/Brand--Canon/N-1462019',
                                                                                            'name': 'Canon '
                                                                                                    'Ink '
                                                                                                    '& '
                                                                                                    'Toner',
                                                                                            'sub_category': 'Ink '
                                                                                                            '& '
                                                                                                            'Toner '
                                                                                                            'By '
                                                                                                            'Brand'},
                         'printers-scanners-ink-toner-by-brand-epson-ink-toner-n-1462019': {'url': '/b/ink-and-toner/Brand--Epson/N-1462019',
                                                                                            'name': 'Epson '
                                                                                                    'Ink '
                                                                                                    '& '
                                                                                                    'Toner',
                                                                                            'sub_category': 'Ink '
                                                                                                            '& '
                                                                                                            'Toner '
                                                                                                            'By '
                                                                                                            'Brand'},
                         'printers-scanners-ink-toner-by-brand-hp-ink-toner-n-1462019': {'url': '/b/ink-and-toner/Brand--HP/N-1462019',
                                                                                         'name': 'HP '
                                                                                                 'Ink '
                                                                                                 '& '
                                                                                                 'Toner',
                                                                                         'sub_category': 'Ink '
                                                                                                         '& '
                                                                                                         'Toner '
                                                                                                         'By '
                                                                                                         'Brand'},
                         'printers-scanners-ink-toner-by-brand-lexmark-ink-toner-n-1462019': {'url': '/b/ink-and-toner/Brand--Lexmark/N-1462019',
                                                                                              'name': 'Lexmark '
                                                                                                      'Ink '
                                                                                                      '& '
                                                                                                      'Toner',
                                                                                              'sub_category': 'Ink '
                                                                                                              '& '
                                                                                                              'Toner '
                                                                                                              'By '
                                                                                                              'Brand'},
                         'printers-scanners-ink-toner-by-brand-xerox-ink-toner-n-1462019': {'url': '/b/ink-and-toner/Brand--Xerox/N-1462019',
                                                                                            'name': 'Xerox '
                                                                                                    'Ink '
                                                                                                    '& '
                                                                                                    'Toner',
                                                                                            'sub_category': 'Ink '
                                                                                                            '& '
                                                                                                            'Toner '
                                                                                                            'By '
                                                                                                            'Brand'},
                         'printers-scanners-printer-accessories-printer-cables-n-1462044': {'url': '/b/printer-accessories/Product_Type--Data_Cable/N-1462044',
                                                                                            'name': 'Printer '
                                                                                                    'Cables',
                                                                                            'sub_category': 'Printer '
                                                                                                            'Accessories'},
                         'printers-scanners-printer-accessories-printer-paper-n-530730': {'url': '/b/copy-and-multipurpose-paper/N-530730/',
                                                                                          'name': 'Printer '
                                                                                                  'Paper',
                                                                                          'sub_category': 'Printer '
                                                                                                          'Accessories'},
                         'printers-scanners-scanners-n-1040464': {'url': '/b/scanners/N-1040464/',
                                                                  'name': 'Scanners',
                                                                  'sub_category': ''},
                         'printers-scanners-scanners-document-scanners-n-1040464': {'url': '/b/scanners/Scanner_Type--Document/N-1040464',
                                                                                    'name': 'Document '
                                                                                            'Scanners',
                                                                                    'sub_category': 'Scanners'},
                         'printers-scanners-scanners-photo-scanners-n-1040464': {'url': '/b/scanners/Scanner_Type--Photo/N-1040464',
                                                                                 'name': 'Photo '
                                                                                         'Scanners',
                                                                                 'sub_category': 'Scanners'},
                         'printers-scanners-scanners-receipt-scanners-n-1040464': {'url': '/b/scanners/Scanner_Type--Receipt/N-1040464',
                                                                                   'name': 'Receipt '
                                                                                           'Scanners',
                                                                                   'sub_category': 'Scanners'}},
 'Electronics': {'electronics-electronics-n-9021': {'url': '/b/electronics/N-9021',
                                                    'name': 'Electronics',
                                                    'sub_category': ''},
                 'electronics-office-equipment-n-509740': {'url': '/b/office-equipment/N-509740',
                                                           'name': 'Office Equipment',
                                                           'sub_category': ''},
                 'electronics-office-equipment-scanners-n-1040464': {'url': '/b/scanners/N-1040464',
                                                                     'name': 'Scanners',
                                                                     'sub_category': 'Office '
                                                                                     'Equipment'},
                 'electronics-office-equipment-shredders-n-509777': {'url': '/b/shredders/N-509777',
                                                                     'name': 'Shredders',
                                                                     'sub_category': 'Office '
                                                                                     'Equipment'},
                 'electronics-office-equipment-calculators-n-509745': {'url': '/b/calculators/N-509745',
                                                                       'name': 'Calculators',
                                                                       'sub_category': 'Office '
                                                                                       'Equipment'},
                 'electronics-office-equipment-projectors-n-1123281': {'url': '/b/projectors/N-1123281',
                                                                       'name': 'Projectors',
                                                                       'sub_category': 'Office '
                                                                                       'Equipment'},
                 'electronics-office-equipment-time-clocks-n-509784': {'url': '/b/time-clocks/N-509784',
                                                                       'name': 'Time Clocks',
                                                                       'sub_category': 'Office '
                                                                                       'Equipment'},
                 'electronics-tvs-home-theater-n-509401': {'url': '/b/tvs-and-home-theater/N-509401',
                                                           'name': 'TVs & Home Theater',
                                                           'sub_category': ''},
                 'electronics-tvs-home-theater-media-streaming-devices-n-510911': {'url': '/b/media-streaming-devices/N-510911',
                                                                                   'name': 'Media '
                                                                                           'Streaming '
                                                                                           'Devices',
                                                                                   'sub_category': 'TVs '
                                                                                                   '& '
                                                                                                   'Home '
                                                                                                   'Theater'},
                 'electronics-tvs-home-theater-tvs-n-509465': {'url': '/b/tvs/N-509465',
                                                               'name': 'TVs',
                                                               'sub_category': 'TVs & Home '
                                                                               'Theater'},
                 'electronics-tvs-home-theater-tv-home-theater-accessories-n-509458': {'url': '/b/tv-and-home-theater-accessories/N-509458',
                                                                                       'name': 'TV '
                                                                                               '& '
                                                                                               'Home '
                                                                                               'Theater '
                                                                                               'Accessories',
                                                                                       'sub_category': 'TVs '
                                                                                                       '& '
                                                                                                       'Home '
                                                                                                       'Theater'},
                 'electronics-tvs-home-theater-video-equipment-n-509470': {'url': '/b/video-equipment/N-509470',
                                                                           'name': 'Video '
                                                                                   'Equipment',
                                                                           'sub_category': 'TVs & '
                                                                                           'Home '
                                                                                           'Theater'},
                 'electronics-tvs-home-theater-audio-devices-n-651017': {'url': '/b/audio-devices/N-651017',
                                                                         'name': 'Audio Devices',
                                                                         'sub_category': 'TVs & '
                                                                                         'Home '
                                                                                         'Theater'},
                 'electronics-batteries-power-protection-n-509475': {'url': '/b/batteries-and-power-protection/N-509475',
                                                                     'name': 'Batteries & Power '
                                                                             'Protection',
                                                                     'sub_category': ''},
                 'electronics-batteries-power-protection-alkaline-batteries-n-509485': {'url': '/b/alkaline-batteries/N-509485',
                                                                                        'name': 'Alkaline '
                                                                                                'Batteries',
                                                                                        'sub_category': 'Batteries '
                                                                                                        '& '
                                                                                                        'Power '
                                                                                                        'Protection'},
                 'electronics-batteries-power-protection-lithium-batteries-n-509496': {'url': '/b/lithium-batteries/N-509496',
                                                                                       'name': 'Lithium '
                                                                                               'Batteries',
                                                                                       'sub_category': 'Batteries '
                                                                                                       '& '
                                                                                                       'Power '
                                                                                                       'Protection'},
                 'electronics-batteries-power-protection-ups-battery-backup-n-509510': {'url': '/b/ups-battery-backup/N-509510',
                                                                                        'name': 'UPS '
                                                                                                'Battery '
                                                                                                'Backup',
                                                                                        'sub_category': 'Batteries '
                                                                                                        '& '
                                                                                                        'Power '
                                                                                                        'Protection'},
                 'electronics-batteries-power-protection-chargers-adapters-n-509492': {'url': '/b/chargers-and-adapters/N-509492',
                                                                                       'name': 'Chargers '
                                                                                               '& '
                                                                                               'Adapters',
                                                                                       'sub_category': 'Batteries '
                                                                                                       '& '
                                                                                                       'Power '
                                                                                                       'Protection'},
                 'electronics-batteries-power-protection-rechargeable-batteries-n-509504': {'url': '/b/rechargeable-batteries/N-509504',
                                                                                            'name': 'Rechargeable '
                                                                                                    'Batteries',
                                                                                            'sub_category': 'Batteries '
                                                                                                            '& '
                                                                                                            'Power '
                                                                                                            'Protection'},
                 'electronics-phones-accessories-n-509793': {'url': '/b/phones-and-accessories/N-509793',
                                                             'name': 'Phones & Accessories',
                                                             'sub_category': ''},
                 'electronics-phones-accessories-multi-line-phones-n-509810': {'url': '/b/multi-line-phones/N-509810',
                                                                               'name': 'Multi-Line '
                                                                                       'Phones',
                                                                               'sub_category': 'Phones '
                                                                                               '& '
                                                                                               'Accessories'},
                 'electronics-phones-accessories-teleconferencing-n-509806': {'url': '/b/teleconferencing/N-509806',
                                                                              'name': 'Teleconferencing',
                                                                              'sub_category': 'Phones '
                                                                                              '& '
                                                                                              'Accessories'},
                 'electronics-phones-accessories-cell-phone-accessories-n-509794': {'url': '/b/cell-phone-accessories/N-509794',
                                                                                    'name': 'Cell '
                                                                                            'Phone '
                                                                                            'Accessories',
                                                                                    'sub_category': 'Phones '
                                                                                                    '& '
                                                                                                    'Accessories'},
                 'electronics-phones-accessories-single-line-phones-n-509829': {'url': '/b/single-line-phones/N-509829',
                                                                                'name': 'Single-Line '
                                                                                        'Phones',
                                                                                'sub_category': 'Phones '
                                                                                                '& '
                                                                                                'Accessories'},
                 'electronics-phones-accessories-voip-phones-systems-n-509807': {'url': '/b/voip/N-509807',
                                                                                 'name': 'VoIP '
                                                                                         'Phones & '
                                                                                         'Systems',
                                                                                 'sub_category': 'Phones '
                                                                                                 '& '
                                                                                                 'Accessories'},
                 'electronics-networking-cables-n-509688': {'url': '/b/networking-and-cables/N-509688',
                                                            'name': 'Networking & Cables',
                                                            'sub_category': ''},
                 'electronics-networking-cables-wireless-networking-n-509733': {'url': '/b/wireless-networking/N-509733',
                                                                                'name': 'Wireless '
                                                                                        'Networking',
                                                                                'sub_category': 'Networking '
                                                                                                '& '
                                                                                                'Cables'},
                 'electronics-networking-cables-network-switches-hubs-n-509719': {'url': '/b/network-switches-and-hubs/N-509719',
                                                                                  'name': 'Network '
                                                                                          'Switches '
                                                                                          '& Hubs',
                                                                                  'sub_category': 'Networking '
                                                                                                  '& '
                                                                                                  'Cables'},
                 'electronics-networking-cables-cables-n-509689': {'url': '/b/cables/N-509689',
                                                                   'name': 'Cables',
                                                                   'sub_category': 'Networking & '
                                                                                   'Cables'},
                 'electronics-networking-cables-cable-management-n-509693': {'url': '/b/cable-management/N-509693',
                                                                             'name': 'Cable '
                                                                                     'Management',
                                                                             'sub_category': 'Networking '
                                                                                             '& '
                                                                                             'Cables'},
                 'electronics-networking-cables-usb-hubs-adapters-n-509728': {'url': '/b/usb-hubs-adapters-and-switches/N-509728',
                                                                              'name': 'USB Hubs & '
                                                                                      'Adapters',
                                                                              'sub_category': 'Networking '
                                                                                              '& '
                                                                                              'Cables'},
                 'electronics-audio-n-552805': {'url': '/b/audio/N-552805',
                                                'name': 'Audio',
                                                'sub_category': ''},
                 'electronics-audio-headphones-n-552818': {'url': '/b/headphones/N-552818',
                                                           'name': 'Headphones',
                                                           'sub_category': 'Audio'},
                 'electronics-audio-home-audio-n-633847': {'url': '/b/home-audio/N-633847',
                                                           'name': 'Home Audio',
                                                           'sub_category': 'Audio'},
                 'electronics-audio-wireless-speakers-n-696204': {'url': '/b/wireless-and-bluetooth-speakers/N-696204',
                                                                  'name': 'Wireless Speakers',
                                                                  'sub_category': 'Audio'},
                 'electronics-audio-audio-accessories-n-552815': {'url': '/b/audio-accessories/N-552815',
                                                                  'name': 'Audio Accessories',
                                                                  'sub_category': 'Audio'},
                 'electronics-audio-docks-radios-n-633852': {'url': '/b/docks-and-radios/N-633852',
                                                             'name': 'Docks & Radios',
                                                             'sub_category': 'Audio'},
                 'electronics-more-ways-to-shop-smart-home-n-734014': {'url': '/b/smart-home/N-734014',
                                                                       'name': 'Smart Home',
                                                                       'sub_category': 'More Ways '
                                                                                       'to Shop'},
                 'electronics-more-ways-to-shop-cameras-camcorders-n-509515': {'url': '/b/cameras-and-camcorders/N-509515',
                                                                               'name': 'Cameras & '
                                                                                       'Camcorders',
                                                                               'sub_category': 'More '
                                                                                               'Ways '
                                                                                               'to '
                                                                                               'Shop'},
                 'electronics-more-ways-to-shop-wearable-technology-n-573033': {'url': '/b/wearable-technology/N-573033',
                                                                                'name': 'Wearable '
                                                                                        'Technology',
                                                                                'sub_category': 'More '
                                                                                                'Ways '
                                                                                                'to '
                                                                                                'Shop'}},
 'Paper': {'paper-paper-n-530715': {'url': '/b/paper/N-530715',
                                    'name': 'Paper',
                                    'sub_category': ''},
           'paper-copy-printer-paper-n-530728': {'url': '/b/copy-and-printer-paper/N-530728',
                                                 'name': 'Copy & Printer Paper',
                                                 'sub_category': ''},
           'paper-copy-printer-paper-copy-multipurpose-paper-n-530730': {'url': '/b/copy-and-multipurpose-paper/N-530730',
                                                                         'name': 'Copy & '
                                                                                 'Multipurpose '
                                                                                 'Paper',
                                                                         'sub_category': 'Copy & '
                                                                                         'Printer '
                                                                                         'Paper'},
           'paper-copy-printer-paper-inkjet-printer-paper-n-530731': {'url': '/b/inkjet-printer-paper/N-530731',
                                                                      'name': 'Inkjet Printer '
                                                                              'Paper',
                                                                      'sub_category': 'Copy & '
                                                                                      'Printer '
                                                                                      'Paper'},
           'paper-copy-printer-paper-colored-paper-n-530729': {'url': '/b/colored-paper/N-530729',
                                                               'name': 'Colored Paper',
                                                               'sub_category': 'Copy & Printer '
                                                                               'Paper'},
           'paper-copy-printer-paper-laser-printer-paper-n-530732': {'url': '/b/laser-printer-paper/N-530732',
                                                                     'name': 'Laser Printer Paper',
                                                                     'sub_category': 'Copy & '
                                                                                     'Printer '
                                                                                     'Paper'},
           'paper-notebooks-pads-n-530741': {'url': '/b/notebooks-and-pads/N-530741',
                                             'name': 'Notebooks & Pads',
                                             'sub_category': ''},
           'paper-notebooks-pads-writing-pads-n-549829': {'url': '/b/writing-pads/N-549829',
                                                          'name': 'Writing Pads',
                                                          'sub_category': 'Notebooks & Pads'},
           'paper-notebooks-pads-spiral-notebooks-n-530745': {'url': '/b/spiral-and-wireless-notebooks/N-530745',
                                                              'name': 'Spiral Notebooks',
                                                              'sub_category': 'Notebooks & Pads'},
           'paper-notebooks-pads-journals-diaries-n-606538': {'url': '/b/journals-and-diaries/N-606538',
                                                              'name': 'Journals & Diaries',
                                                              'sub_category': 'Notebooks & Pads'},
           'paper-notebooks-pads-composition-books-n-530742': {'url': '/b/composition-books/N-530742',
                                                               'name': 'Composition Books',
                                                               'sub_category': 'Notebooks & Pads'},
           'paper-notebooks-pads-discbound-notebooks-n-1012166': {'url': '/b/discbound-note-taking-systems/N-1012166',
                                                                  'name': 'Discbound Notebooks',
                                                                  'sub_category': 'Notebooks & '
                                                                                  'Pads'},
           'paper-featured-brands-office-depot-n-530715': {'url': '/b/paper/Brand--Office_Depot/N-530715',
                                                           'name': 'Office Depot',
                                                           'sub_category': 'Featured Brands'},
           'paper-featured-brands-hp-n-530715': {'url': '/b/paper/Brand--HP/N-530715',
                                                 'name': 'HP',
                                                 'sub_category': 'Featured Brands'},
           'paper-photo-presentation-n-530747': {'url': '/b/photo-and-presentation-paper/N-530747',
                                                 'name': 'Photo & Presentation',
                                                 'sub_category': ''},
           'paper-photo-presentation-photo-printer-paper-n-530749': {'url': '/b/photo-printer-paper/N-530749',
                                                                     'name': 'Photo Printer Paper',
                                                                     'sub_category': 'Photo & '
                                                                                     'Presentation'},
           'paper-photo-presentation-brochure-paper-n-530748': {'url': '/b/brochure-and-presentation-paper/N-530748',
                                                                'name': 'Brochure Paper',
                                                                'sub_category': 'Photo & '
                                                                                'Presentation'},
           'paper-photo-presentation-commercial-printing-paper-n-1251127': {'url': '/b/commercial-printing-paper/N-1251127',
                                                                            'name': 'Commercial '
                                                                                    'Printing '
                                                                                    'Paper',
                                                                            'sub_category': 'Photo '
                                                                                            '& '
                                                                                            'Presentation'},
           'paper-photo-presentation-stationery-resume-paper-n-549831': {'url': '/b/stationery-and-resume-paper/N-549831',
                                                                         'name': 'Stationery & '
                                                                                 'Resume Paper',
                                                                         'sub_category': 'Photo & '
                                                                                         'Presentation'},
           'paper-photo-presentation-wide-format-paper-n-530751': {'url': '/b/wide-format-paper/N-530751',
                                                                   'name': 'Wide Format Paper',
                                                                   'sub_category': 'Photo & '
                                                                                   'Presentation'},
           'paper-post-it-sticky-notepads-n-1563983': {'url': '/b/sticky-notes-and-flags/N-1563983',
                                                       'name': 'Post-It & Sticky Notepads',
                                                       'sub_category': ''},
           'paper-post-it-sticky-notepads-sticky-notes-n-1563986': {'url': '/b/sticky-notes/N-1563986',
                                                                    'name': 'Sticky Notes',
                                                                    'sub_category': 'Post-It & '
                                                                                    'Sticky '
                                                                                    'Notepads'},
           'paper-post-it-sticky-notepads-sticky-flags-n-1563985': {'url': '/b/sticky-flags/N-1563985',
                                                                    'name': 'Sticky Flags',
                                                                    'sub_category': 'Post-It & '
                                                                                    'Sticky '
                                                                                    'Notepads'},
           'paper-post-it-sticky-notepads-sticky-tabs-n-1563987': {'url': '/b/sticky-tabs/N-1563987',
                                                                   'name': 'Sticky Tabs',
                                                                   'sub_category': 'Post-It & '
                                                                                   'Sticky '
                                                                                   'Notepads'},
           'paper-post-it-sticky-notepads-sticky-note-dispensers-n-1563984': {'url': '/b/note-dispensers/N-1563984',
                                                                              'name': 'Sticky Note '
                                                                                      'Dispensers',
                                                                              'sub_category': 'Post-It '
                                                                                              '& '
                                                                                              'Sticky '
                                                                                              'Notepads'},
           'paper-filler-graph-paper-n-549821': {'url': '/b/filler-and-graph-paper/N-549821',
                                                 'name': 'Filler & Graph Paper',
                                                 'sub_category': ''},
           'paper-filler-graph-paper-filler-paper-n-549823': {'url': '/b/filler-paper/N-549823',
                                                              'name': 'Filler Paper',
                                                              'sub_category': 'Filler & Graph '
                                                                              'Paper'},
           'paper-filler-graph-paper-graph-paper-n-549824': {'url': '/b/graph-paper/N-549824',
                                                             'name': 'Graph Paper',
                                                             'sub_category': 'Filler & Graph '
                                                                             'Paper'},
           'paper-filler-graph-paper-data-pads-n-549822': {'url': '/b/data-pads/N-549822',
                                                           'name': 'Data Pads',
                                                           'sub_category': 'Filler & Graph Paper'},
           'paper-register-thermal-paper-rolls-n-530723': {'url': '/b/cash-register-and-thermal-rolls/N-530723',
                                                           'name': 'Register & Thermal Paper Rolls',
                                                           'sub_category': ''},
           'paper-register-thermal-paper-rolls-register-paper-rolls-n-530724': {'url': '/b/cash-register-and-thermal-paper-rolls/N-530724',
                                                                                'name': 'Register '
                                                                                        'Paper '
                                                                                        'Rolls',
                                                                                'sub_category': 'Register '
                                                                                                '& '
                                                                                                'Thermal '
                                                                                                'Paper '
                                                                                                'Rolls'},
           'paper-register-thermal-paper-rolls-calculator-paper-rolls-n-549817': {'url': '/b/calculator-paper-rolls/N-549817',
                                                                                  'name': 'Calculator '
                                                                                          'Paper '
                                                                                          'Rolls',
                                                                                  'sub_category': 'Register '
                                                                                                  '& '
                                                                                                  'Thermal '
                                                                                                  'Paper '
                                                                                                  'Rolls'},
           'paper-register-thermal-paper-rolls-fax-paper-n-530726': {'url': '/b/fax-paper/N-530726',
                                                                     'name': 'Fax Paper',
                                                                     'sub_category': 'Register & '
                                                                                     'Thermal '
                                                                                     'Paper Rolls'},
           'paper-art-craft-paper-n-530716': {'url': '/b/art-and-craft-paper/N-530716',
                                              'name': 'Art & Craft Paper',
                                              'sub_category': ''},
           'paper-art-craft-paper-construction-paper-n-530717': {'url': '/b/construction-paper/N-530717',
                                                                 'name': 'Construction Paper',
                                                                 'sub_category': 'Art & Craft '
                                                                                 'Paper'},
           'paper-art-craft-paper-drawing-paper-pads-n-530720': {'url': '/b/drawing-paper-and-pads/N-530720',
                                                                 'name': 'Drawing Paper & Pads',
                                                                 'sub_category': 'Art & Craft '
                                                                                 'Paper'},
           'paper-art-craft-paper-craft-tissue-paper-n-530719': {'url': '/b/craft-and-tissue-paper/N-530719',
                                                                 'name': 'Craft & Tissue Paper',
                                                                 'sub_category': 'Art & Craft '
                                                                                 'Paper'},
           'paper-art-craft-paper-iron-on-transfers-n-530721': {'url': '/b/iron-on-transfers/N-530721',
                                                                'name': 'Iron-on Transfers',
                                                                'sub_category': 'Art & Craft '
                                                                                'Paper'}},
 'School Supplies': {'school-supplies-arts-crafts-n-1155033': {'url': '/b/arts-and-crafts/N-1155033',
                                                               'name': 'Arts & Crafts',
                                                               'sub_category': ''},
                     'school-supplies-arts-crafts-colored-pencils-n-872379': {'url': '/b/colored-pencils/N-872379',
                                                                              'name': 'Colored '
                                                                                      'Pencils',
                                                                              'sub_category': 'Arts '
                                                                                              '& '
                                                                                              'Crafts'},
                     'school-supplies-arts-crafts-markers-n-4467': {'url': '/b/markers-and-highlighters/N-4467',
                                                                    'name': 'Markers',
                                                                    'sub_category': 'Arts & '
                                                                                    'Crafts'},
                     'school-supplies-arts-crafts-crayons-n-639153': {'url': '/b/crayons/N-639153',
                                                                      'name': 'Crayons',
                                                                      'sub_category': 'Arts & '
                                                                                      'Crafts'},
                     'school-supplies-arts-crafts-glue-n-371558': {'url': '/b/glue-and-adhesives/N-371558',
                                                                   'name': 'Glue',
                                                                   'sub_category': 'Arts & Crafts'},
                     'school-supplies-arts-crafts-construction-paper-n-530717': {'url': '/b/construction-paper/N-530717',
                                                                                 'name': 'Construction '
                                                                                         'Paper',
                                                                                 'sub_category': 'Arts '
                                                                                                 '& '
                                                                                                 'Crafts'},
                     'school-supplies-school-backpacks-lunch-bags-n-1155042': {'url': '/b/backpacks-and-lunch-bags/N-1155042',
                                                                               'name': 'School '
                                                                                       'Backpacks '
                                                                                       '& Lunch '
                                                                                       'Bags',
                                                                               'sub_category': ''},
                     'school-supplies-school-backpacks-lunch-bags-school-backpacks-n-1155043': {'url': '/b/backpacks/N-1155043',
                                                                                                'name': 'School '
                                                                                                        'Backpacks',
                                                                                                'sub_category': 'School '
                                                                                                                'Backpacks '
                                                                                                                '& '
                                                                                                                'Lunch '
                                                                                                                'Bags'},
                     'school-supplies-school-backpacks-lunch-bags-lunch-bags-n-1155044': {'url': '/b/lunch-bags/N-1155044',
                                                                                          'name': 'Lunch '
                                                                                                  'Bags',
                                                                                          'sub_category': 'School '
                                                                                                          'Backpacks '
                                                                                                          '& '
                                                                                                          'Lunch '
                                                                                                          'Bags'},
                     'school-supplies-school-backpacks-lunch-bags-water-bottles-cups-n-1211738': {'url': '/b/water-bottles/N-1211738',
                                                                                                  'name': 'Water '
                                                                                                          'Bottles '
                                                                                                          '& '
                                                                                                          'Cups',
                                                                                                  'sub_category': 'School '
                                                                                                                  'Backpacks '
                                                                                                                  '& '
                                                                                                                  'Lunch '
                                                                                                                  'Bags'},
                     'school-supplies-basic-school-supplies-n-1155045': {'url': '/b/basic-school-supplies/N-1155045',
                                                                         'name': 'Basic School '
                                                                                 'Supplies',
                                                                         'sub_category': ''},
                     'school-supplies-basic-school-supplies-scissors-n-581693': {'url': '/b/scissors/N-581693',
                                                                                 'name': 'Scissors',
                                                                                 'sub_category': 'Basic '
                                                                                                 'School '
                                                                                                 'Supplies'},
                     'school-supplies-basic-school-supplies-pencil-cases-n-1156638': {'url': '/b/pencil-cases/N-1156638',
                                                                                      'name': 'Pencil '
                                                                                              'Cases',
                                                                                      'sub_category': 'Basic '
                                                                                                      'School '
                                                                                                      'Supplies'},
                     'school-supplies-basic-school-supplies-tape-n-371573': {'url': '/b/office-tape/N-371573',
                                                                             'name': 'Tape',
                                                                             'sub_category': 'Basic '
                                                                                             'School '
                                                                                             'Supplies'},
                     'school-supplies-basic-school-supplies-rulers-n-581690': {'url': '/b/rulers/N-581690',
                                                                               'name': 'Rulers',
                                                                               'sub_category': 'Basic '
                                                                                               'School '
                                                                                               'Supplies'},
                     'school-supplies-basic-school-supplies-protractors-n-590395': {'url': '/b/protractors/N-590395',
                                                                                    'name': 'Protractors',
                                                                                    'sub_category': 'Basic '
                                                                                                    'School '
                                                                                                    'Supplies'},
                     'school-supplies-basic-school-supplies-staples-staplers-n-658785': {'url': '/b/staplers-and-staples/N-658785',
                                                                                         'name': 'Staples '
                                                                                                 '& '
                                                                                                 'Staplers',
                                                                                         'sub_category': 'Basic '
                                                                                                         'School '
                                                                                                         'Supplies'},
                     'school-supplies-school-electronics-calculators-n-509745': {'url': '/b/calculators/N-509745',
                                                                                 'name': 'Calculators',
                                                                                 'sub_category': 'School '
                                                                                                 'Electronics'},
                     'school-supplies-school-electronics-earbuds-headphones-n-552818': {'url': '/b/headphones/N-552818',
                                                                                        'name': 'Earbuds '
                                                                                                '& '
                                                                                                'Headphones',
                                                                                        'sub_category': 'School '
                                                                                                        'Electronics'},
                     'school-supplies-school-electronics-hard-drives-n-1461964': {'url': '/b/external-hard-drives/N-1461964',
                                                                                  'name': 'Hard '
                                                                                          'Drives',
                                                                                  'sub_category': 'School '
                                                                                                  'Electronics'},
                     'school-supplies-school-electronics-flash-drives-n-1461987': {'url': '/b/usb-flash-drives/N-1461987',
                                                                                   'name': 'Flash '
                                                                                           'Drives',
                                                                                   'sub_category': 'School '
                                                                                                   'Electronics'},
                     'school-supplies-folders-binders-n-1155061': {'url': '/b/folders-and-binders/N-1155061',
                                                                   'name': 'Folders & Binders',
                                                                   'sub_category': ''},
                     'school-supplies-folders-binders-pocket-folders-n-1155065': {'url': '/b/pocket-folders/N-1155065',
                                                                                  'name': 'Pocket '
                                                                                          'Folders',
                                                                                  'sub_category': 'Folders '
                                                                                                  '& '
                                                                                                  'Binders'},
                     'school-supplies-folders-binders-binders-n-1035691': {'url': '/b/binders/N-1035691',
                                                                           'name': 'Binders',
                                                                           'sub_category': 'Folders '
                                                                                           '& '
                                                                                           'Binders'},
                     'school-supplies-folders-binders-file-folders-n-3545': {'url': '/b/file-folders/N-3545',
                                                                             'name': 'File Folders',
                                                                             'sub_category': 'Folders '
                                                                                             '& '
                                                                                             'Binders'},
                     'school-supplies-folders-binders-dividers-n-581131': {'url': '/b/dividers/N-581131',
                                                                           'name': 'Dividers',
                                                                           'sub_category': 'Folders '
                                                                                           '& '
                                                                                           'Binders'},
                     'school-supplies-folders-binders-sheet-protectors-n-1461717': {'url': '/b/sheet-protectors/N-1461717',
                                                                                    'name': 'Sheet '
                                                                                            'Protectors',
                                                                                    'sub_category': 'Folders '
                                                                                                    '& '
                                                                                                    'Binders'},
                     'school-supplies-notebooks-paper-n-1155070': {'url': '/b/notebooks-and-paper/N-1155070',
                                                                   'name': 'Notebooks & Paper',
                                                                   'sub_category': ''},
                     'school-supplies-notebooks-paper-notebooks-n-530745': {'url': '/b/spiral-and-wireless-notebooks/N-530745',
                                                                            'name': 'Notebooks',
                                                                            'sub_category': 'Notebooks '
                                                                                            '& '
                                                                                            'Paper'},
                     'school-supplies-notebooks-paper-composition-books-n-530742': {'url': '/b/composition-books/N-530742',
                                                                                    'name': 'Composition '
                                                                                            'Books',
                                                                                    'sub_category': 'Notebooks '
                                                                                                    '& '
                                                                                                    'Paper'},
                     'school-supplies-notebooks-paper-loose-leaf-paper-n-1155076': {'url': '/b/loose-leaf-paper/N-1155076',
                                                                                    'name': 'Loose '
                                                                                            'Leaf '
                                                                                            'Paper',
                                                                                    'sub_category': 'Notebooks '
                                                                                                    '& '
                                                                                                    'Paper'},
                     'school-supplies-notebooks-paper-index-cards-n-1123261': {'url': '/b/index-cards/N-1123261',
                                                                               'name': 'Index '
                                                                                       'Cards',
                                                                               'sub_category': 'Notebooks '
                                                                                               '& '
                                                                                               'Paper'},
                     'school-supplies-notebooks-paper-graph-paper-n-549824': {'url': '/b/graph-paper/N-549824',
                                                                              'name': 'Graph Paper',
                                                                              'sub_category': 'Notebooks '
                                                                                              '& '
                                                                                              'Paper'},
                     'school-supplies-writing-n-4367': {'url': '/b/pens-pencils-and-markers/N-4367',
                                                        'name': 'Writing',
                                                        'sub_category': ''},
                     'school-supplies-writing-pens-n-4520': {'url': '/b/pens/N-4520',
                                                             'name': 'Pens',
                                                             'sub_category': 'Writing'},
                     'school-supplies-writing-pencils-n-4504': {'url': '/b/pencils/N-4504',
                                                                'name': 'Pencils',
                                                                'sub_category': 'Writing'},
                     'school-supplies-writing-highlighters-markers-n-4467': {'url': '/b/markers-and-highlighters/N-4467',
                                                                             'name': 'Highlighters '
                                                                                     '& Markers',
                                                                             'sub_category': 'Writing'},
                     'school-supplies-writing-correction-fluid-n-4405': {'url': '/b/correction-fluid/N-4405',
                                                                         'name': 'Correction Fluid',
                                                                         'sub_category': 'Writing'},
                     'school-supplies-writing-erasers-n-4420': {'url': '/b/erasers/N-4420',
                                                                'name': 'Erasers',
                                                                'sub_category': 'Writing'},
                     'school-supplies-shop-by-grade-k-5-n-502600': {'url': '/b/school-supplies/Grades--K-5/N-502600',
                                                                    'name': 'K-5',
                                                                    'sub_category': 'Shop By '
                                                                                    'Grade'},
                     'school-supplies-shop-by-grade-6-8-n-502600': {'url': '/b/school-supplies/Grades--6-8/N-502600',
                                                                    'name': '6-8',
                                                                    'sub_category': 'Shop By '
                                                                                    'Grade'},
                     'school-supplies-shop-by-grade-9-12-n-502600': {'url': '/b/school-supplies/Grades--9-12/N-502600',
                                                                     'name': '9-12',
                                                                     'sub_category': 'Shop By '
                                                                                     'Grade'},
                     'school-supplies-teacher-supplies-n-1186205': {'url': '/b/teacher-supplies/N-1186205',
                                                                    'name': 'Teacher Supplies',
                                                                    'sub_category': ''}},
 'Mailing & Shipping': {'mailing-shipping-mailing-shipping-n-3912': {'url': '/b/mailing-packing-and-shipping/N-3912',
                                                                     'name': 'Mailing & Shipping',
                                                                     'sub_category': ''},
                        'mailing-shipping-envelopes-n-514132': {'url': '/b/envelopes/N-514132',
                                                                'name': 'Envelopes',
                                                                'sub_category': ''},
                        'mailing-shipping-envelopes-business-envelopes-n-514133': {'url': '/b/business-envelopes/N-514133',
                                                                                   'name': 'Business '
                                                                                           'Envelopes',
                                                                                   'sub_category': 'Envelopes'},
                        'mailing-shipping-envelopes-catalog-envelopes-n-514135': {'url': '/b/catalog-envelopes/N-514135',
                                                                                  'name': 'Catalog '
                                                                                          'Envelopes',
                                                                                  'sub_category': 'Envelopes'},
                        'mailing-shipping-envelopes-tax-envelopes-n-1013810': {'url': '/b/tax-envelopes/N-1013810',
                                                                               'name': 'Tax '
                                                                                       'Envelopes',
                                                                               'sub_category': 'Envelopes'},
                        'mailing-shipping-envelopes-invitation-envelopes-n-887332': {'url': '/b/invitation-envelopes/N-887332',
                                                                                     'name': 'Invitation '
                                                                                             'Envelopes',
                                                                                     'sub_category': 'Envelopes'},
                        'mailing-shipping-envelopes-booklet-envelopes-n-887330': {'url': '/b/booklet-envelopes/N-887330',
                                                                                  'name': 'Booklet '
                                                                                          'Envelopes',
                                                                                  'sub_category': 'Envelopes'},
                        'mailing-shipping-envelopes-window-envelopes-n-887333': {'url': '/b/window-envelopes/N-887333',
                                                                                 'name': 'Window '
                                                                                         'Envelopes',
                                                                                 'sub_category': 'Envelopes'},
                        'mailing-shipping-envelopes-coin-envelopes-n-887331': {'url': '/b/coin-envelopes/N-887331',
                                                                               'name': 'Coin '
                                                                                       'Envelopes',
                                                                               'sub_category': 'Envelopes'},
                        'mailing-shipping-shipping-moving-boxes-n-3913': {'url': '/b/shipping-and-moving-boxes/N-3913',
                                                                          'name': 'Shipping & '
                                                                                  'Moving Boxes',
                                                                          'sub_category': ''},
                        'mailing-shipping-shipping-moving-boxes-shipping-boxes-n-3914': {'url': '/b/shipping-boxes/N-3914',
                                                                                         'name': 'Shipping '
                                                                                                 'Boxes',
                                                                                         'sub_category': 'Shipping '
                                                                                                         '& '
                                                                                                         'Moving '
                                                                                                         'Boxes'},
                        'mailing-shipping-shipping-moving-boxes-moving-boxes-n-530206': {'url': '/b/moving-boxes/N-530206',
                                                                                         'name': 'Moving '
                                                                                                 'Boxes',
                                                                                         'sub_category': 'Shipping '
                                                                                                         '& '
                                                                                                         'Moving '
                                                                                                         'Boxes'},
                        'mailing-shipping-shipping-moving-boxes-storage-boxes-n-3913': {'url': '/b/shipping-and-moving-boxes/Usage--Storage/N-3913',
                                                                                        'name': 'Storage '
                                                                                                'Boxes',
                                                                                        'sub_category': 'Shipping '
                                                                                                        '& '
                                                                                                        'Moving '
                                                                                                        'Boxes'},
                        'mailing-shipping-postage-stamps-n-543624': {'url': '/b/postage-stamps/N-543624',
                                                                     'name': 'Postage Stamps',
                                                                     'sub_category': ''},
                        'mailing-shipping-mailers-n-530021': {'url': '/b/mailers/N-530021',
                                                              'name': 'Mailers',
                                                              'sub_category': ''},
                        'mailing-shipping-mailers-bubble-mailers-n-1012421': {'url': '/b/bubble-mailers/N-1012421',
                                                                              'name': 'Bubble '
                                                                                      'Mailers',
                                                                              'sub_category': 'Mailers'},
                        'mailing-shipping-mailers-flat-mailers-n-1012422': {'url': '/b/flat-mailers/N-1012422',
                                                                            'name': 'Flat Mailers',
                                                                            'sub_category': 'Mailers'},
                        'mailing-shipping-mailers-mailing-tubes-n-530025': {'url': '/b/mailing-tubes/N-530025',
                                                                            'name': 'Mailing Tubes',
                                                                            'sub_category': 'Mailers'},
                        'mailing-shipping-mailers-corrugated-mailers-n-530023': {'url': '/b/corrugated-mailers/N-530023',
                                                                                 'name': 'Corrugated '
                                                                                         'Mailers',
                                                                                 'sub_category': 'Mailers'},
                        'mailing-shipping-mailers-padded-mailers-n-1012423': {'url': '/b/padded-mailers/N-1012423',
                                                                              'name': 'Padded '
                                                                                      'Mailers',
                                                                              'sub_category': 'Mailers'},
                        'mailing-shipping-mailers-poly-mailers-n-1199130': {'url': '/b/poly-mailers/N-1199130',
                                                                            'name': 'Poly Mailers',
                                                                            'sub_category': 'Mailers'},
                        'mailing-shipping-packing-tape-n-4009': {'url': '/b/packing-tape/N-4009',
                                                                 'name': 'Packing Tape',
                                                                 'sub_category': ''},
                        'mailing-shipping-packing-tape-shipping-tape-n-4009': {'url': '/b/packing-tape/Usage--Shipping/N-4009',
                                                                               'name': 'Shipping '
                                                                                       'Tape',
                                                                               'sub_category': 'Packing '
                                                                                               'Tape'},
                        'mailing-shipping-packing-tape-moving-tape-n-4009': {'url': '/b/packing-tape/Usage--Moving/N-4009',
                                                                             'name': 'Moving Tape',
                                                                             'sub_category': 'Packing '
                                                                                             'Tape'},
                        'mailing-shipping-packing-tape-storage-tape-n-4009': {'url': '/b/packing-tape/Usage--Storage/N-4009',
                                                                              'name': 'Storage '
                                                                                      'Tape',
                                                                              'sub_category': 'Packing '
                                                                                              'Tape'},
                        'mailing-shipping-packing-tape-tape-dispensers-n-4009': {'url': '/b/packing-tape/Product_Type--Industrial_Tape_Dispenser/N-4009',
                                                                                 'name': 'Tape '
                                                                                         'Dispensers',
                                                                                 'sub_category': 'Packing '
                                                                                                 'Tape'},
                        'mailing-shipping-mailroom-equipment-n-530211': {'url': '/b/mailroom-equipment/N-530211',
                                                                         'name': 'Mailroom '
                                                                                 'Equipment',
                                                                         'sub_category': ''},
                        'mailing-shipping-mailroom-equipment-postal-scales-n-1012428': {'url': '/b/postal-scales/N-1012428',
                                                                                        'name': 'Postal '
                                                                                                'Scales',
                                                                                        'sub_category': 'Mailroom '
                                                                                                        'Equipment'},
                        'mailing-shipping-mailroom-equipment-mail-sorters-n-1012426': {'url': '/b/mail-sorters/N-1012426',
                                                                                       'name': 'Mail '
                                                                                               'Sorters',
                                                                                       'sub_category': 'Mailroom '
                                                                                                       'Equipment'},
                        'mailing-shipping-labels-n-3950': {'url': '/b/labels-and-tags/N-3950',
                                                           'name': 'Labels',
                                                           'sub_category': ''},
                        'mailing-shipping-labels-address-labels-n-3951': {'url': '/b/address-labels/N-3951',
                                                                          'name': 'Address Labels',
                                                                          'sub_category': 'Labels'},
                        'mailing-shipping-labels-shipping-labels-n-1159764': {'url': '/b/shipping-labels/N-1159764',
                                                                              'name': 'Shipping '
                                                                                      'Labels',
                                                                              'sub_category': 'Labels'},
                        'mailing-shipping-labels-packing-list-envelopes-n-1012420': {'url': '/b/packing-list-envelopes/N-1012420',
                                                                                     'name': 'Packing '
                                                                                             'List '
                                                                                             'Envelopes',
                                                                                     'sub_category': 'Labels'},
                        'mailing-shipping-packing-materials-n-3972': {'url': '/b/packing-materials/N-3972',
                                                                      'name': 'Packing Materials',
                                                                      'sub_category': ''},
                        'mailing-shipping-packing-materials-bubble-rolls-wrap-n-3973': {'url': '/b/bubble-rolls-and-wrap/N-3973',
                                                                                        'name': 'Bubble '
                                                                                                'Rolls '
                                                                                                '& '
                                                                                                'Wrap',
                                                                                        'sub_category': 'Packing '
                                                                                                        'Materials'},
                        'mailing-shipping-packing-materials-packing-peanuts-n-530215': {'url': '/b/packing-peanuts/N-530215',
                                                                                        'name': 'Packing '
                                                                                                'Peanuts',
                                                                                        'sub_category': 'Packing '
                                                                                                        'Materials'},
                        'mailing-shipping-packing-materials-packing-papers-n-3988': {'url': '/b/packing-papers/N-3988',
                                                                                     'name': 'Packing '
                                                                                             'Papers',
                                                                                     'sub_category': 'Packing '
                                                                                                     'Materials'},
                        'mailing-shipping-packing-materials-corrugated-sheets-rolls-n-1012430': {'url': '/b/corrugated-sheets-and-rolls/N-1012430',
                                                                                                 'name': 'Corrugated '
                                                                                                         'Sheets '
                                                                                                         '& '
                                                                                                         'Rolls',
                                                                                                 'sub_category': 'Packing '
                                                                                                                 'Materials'},
                        'mailing-shipping-industrial-shipping-supplies-n-1012408': {'url': '/b/industrial-shipping-supplies/N-1012408',
                                                                                    'name': 'Industrial '
                                                                                            'Shipping '
                                                                                            'Supplies',
                                                                                    'sub_category': ''},
                        'mailing-shipping-industrial-shipping-supplies-industrial-tape-n-1012438': {'url': '/b/industrial-tape/N-1012438',
                                                                                                    'name': 'Industrial '
                                                                                                            'Tape',
                                                                                                    'sub_category': 'Industrial '
                                                                                                                    'Shipping '
                                                                                                                    'Supplies'},
                        'mailing-shipping-industrial-shipping-supplies-shrink-wrap-n-1012416': {'url': '/b/shrink-wrap/N-1012416',
                                                                                                'name': 'Shrink-Wrap',
                                                                                                'sub_category': 'Industrial '
                                                                                                                'Shipping '
                                                                                                                'Supplies'},
                        'mailing-shipping-industrial-shipping-supplies-inspection-shipping-tags-n-1012412': {'url': '/b/inspection-and-shipping-tags/N-1012412',
                                                                                                             'name': 'Inspection '
                                                                                                                     '& '
                                                                                                                     'Shipping '
                                                                                                                     'Tags',
                                                                                                             'sub_category': 'Industrial '
                                                                                                                             'Shipping '
                                                                                                                             'Supplies'},
                        'mailing-shipping-industrial-shipping-supplies-hand-trucks-dollies-n-1012410': {'url': '/b/hand-trucks-and-dollies/N-1012410',
                                                                                                        'name': 'Hand '
                                                                                                                'Trucks '
                                                                                                                '& '
                                                                                                                'Dollies',
                                                                                                        'sub_category': 'Industrial '
                                                                                                                        'Shipping '
                                                                                                                        'Supplies'},
                        'mailing-shipping-industrial-shipping-supplies-utility-knives-cutters-blades-n-1012418': {'url': '/b/utility-knives-cutters-and-blades/N-1012418',
                                                                                                                  'name': 'Utility '
                                                                                                                          'Knives, '
                                                                                                                          'Cutters '
                                                                                                                          '& '
                                                                                                                          'Blades',
                                                                                                                  'sub_category': 'Industrial '
                                                                                                                                  'Shipping '
                                                                                                                                  'Supplies'},
                        'mailing-shipping-industrial-shipping-supplies-shipping-straps-n-1012417': {'url': '/b/strapping-materials-and-twine/N-1012417',
                                                                                                    'name': 'Shipping '
                                                                                                            'Straps',
                                                                                                    'sub_category': 'Industrial '
                                                                                                                    'Shipping '
                                                                                                                    'Supplies'},
                        'mailing-shipping-poly-bags-n-4045': {'url': '/b/poly-bags/N-4045',
                                                              'name': 'Poly Bags',
                                                              'sub_category': ''},
                        'mailing-shipping-custom-mailing-labels-n-1212303': {'url': '/b/custom-mailing-labels/N-1212303',
                                                                             'name': 'Custom '
                                                                                     'Mailing '
                                                                                     'Labels',
                                                                             'sub_category': ''}},
 'Calendars & Planners': {'calendars-planners-calendars-planners-n-1131206': {'url': '/b/calendars-and-planners/N-1131206',
                                                                              'name': 'Calendars & '
                                                                                      'Planners',
                                                                              'sub_category': ''}}}
# END GENERATED CATEGORY SNAPSHOT
