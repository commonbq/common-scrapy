"""Blick Art Materials (dickblick.com) category taxonomy (issue #227).

Captured 2026-10-05 from the Next.js hydration of the global category index:

    https://www.dickblick.com/categories/
        -> <script id="__NEXT_DATA__">
             -> props.pageProps.data[] = {"id", "contentType", "name", "url"}

``pageProps.data`` holds 2,697 records: the same 899 nodes repeated under three
``contentType`` values (``department``, ``categoriesLandingPages``,
``subCategoriesLandingPages``). Only the records that carry both ``name`` and
``url`` are kept, which collapses the 2,697 rows to **899 unique
``/categories/.../`` URLs under 17 top-level departments**.

The tree is rebuilt from URL path segments (``/categories/<dept>/[<group>/]
<leaf>/``) so the parent/child relationship is deterministic rather than
dependent on the order the CMS emits the nodes in. Display names come from the
hydration records.

Shape of every node::

    {"name": "Acrylic Paint", "url": "https://www.dickblick.com/categories/...", "children": {...}}

``children`` is omitted for leaf nodes. The 899 crawlable URLs sit at three
levels: 16 department landing pages, 204 direct children, 679 grandchildren.
Nine further group nodes are path-derived containers with ``url=None`` (e.g.
``/categories/painting/acrylics/`` exists only as a path segment of its
children and is absent from the CMS index itself); the spider skips those.
Flattening therefore yields 908 rows, of which ``crawlable_categories()``
returns 899.

Note: the marketing homepage's smaller ``browseDepartments`` array is **not**
used -- it is a curated subset and would miss hundreds of leaf categories.

One department, ``/categories/macpherson-overstock-liquidation-sale/``, has no
landing page of its own; its name is derived from the URL segment and its
children are kept as the first level.

About 95 URLs are cross-listed by the CMS under two display names (e.g.
"Primers" and "Primers and Gessoes" both point at ``/categories/canvas/primers/``).
The lexicographically smallest name wins so the tree does not depend on the
order the CMS emits records in.
"""

from __future__ import annotations

BLICK_SITE_BASE = "https://www.dickblick.com"

# Counts asserted against the live /categories/ hydration on the capture date.
BLICK_CATEGORY_COUNTS = {
    "hydration_records": 2697,
    "departments": 17,
    "category_urls": 899,
    "structural_group_nodes": 9,
    "captured": "2026-10-05",
}

BLICK_CATEGORY_TREE: dict[str, dict] = {
    "art-canvases-and-painting-surfaces": {
        "name": "Art Canvases and Painting Surfaces",
        "url": "https://www.dickblick.com/categories/canvas/",
        "children": {
            "canvas-boards-and-panels": {
                "name": "Canvas Boards and Panels",
                "url": "https://www.dickblick.com/categories/canvas/panels/"
            },
            "canvas-rolls": {
                "name": "Canvas Rolls",
                "url": "https://www.dickblick.com/categories/canvas/canvas-rolls/"
            },
            "canvas-stretching-tools": {
                "name": "Canvas Stretching Tools",
                "url": "https://www.dickblick.com/categories/canvas/stretching-tools/"
            },
            "hardboard-and-wood-painting-panels": {
                "name": "Hardboard and Wood Painting Panels",
                "url": "https://www.dickblick.com/categories/canvas/wood-painting-panels/"
            },
            "primers-and-gessoes": {
                "name": "Primers and Gessoes",
                "url": "https://www.dickblick.com/categories/canvas/primers/",
                "children": {
                    "acrylic-gessoes-and-primers": {
                        "name": "Acrylic Gessoes and Primers",
                        "url": "https://www.dickblick.com/categories/canvas/primers/acrylic-gessoes/"
                    },
                    "oil-priming-materials": {
                        "name": "Oil Priming Materials",
                        "url": "https://www.dickblick.com/categories/canvas/primers/oil-priming-materials/"
                    },
                    "rabbit-skin-glue": {
                        "name": "Rabbit Skin Glue",
                        "url": "https://www.dickblick.com/categories/canvas/primers/rabbit-skin-glue/"
                    },
                    "sign-painting-primers-and-sealers": {
                        "name": "Sign Painting Primers and Sealers",
                        "url": "https://www.dickblick.com/categories/canvas/primers/sign-painting/"
                    },
                    "specialty-gessoes": {
                        "name": "Specialty Gessoes",
                        "url": "https://www.dickblick.com/categories/canvas/primers/specialty-gessoes/"
                    }
                }
            },
            "stretched-canvas": {
                "name": "Stretched Canvas",
                "url": "https://www.dickblick.com/categories/canvas/stretched-canvas/"
            },
            "stretched-canvas-by-popular-sizes": {
                "name": "Stretched Canvas by Popular Sizes",
                "url": "https://www.dickblick.com/categories/canvas/stretched-canvas-by-size/",
                "children": {
                    "11-x-14-stretched-canvas": {
                        "name": "11\" x 14\" Stretched Canvas ",
                        "url": "https://www.dickblick.com/categories/canvas/stretched-canvas-by-size/11x14/"
                    },
                    "12-x-12-stretched-canvas": {
                        "name": "12\" x 12\" Stretched Canvas",
                        "url": "https://www.dickblick.com/categories/canvas/stretched-canvas-by-size/12x12/"
                    },
                    "16-x-20-stretched-canvas": {
                        "name": "16\" x 20\" Stretched Canvas",
                        "url": "https://www.dickblick.com/categories/canvas/stretched-canvas-by-size/16x20/"
                    },
                    "18-x-24-stretched-canvas": {
                        "name": "18\" x 24\" Stretched Canvas ",
                        "url": "https://www.dickblick.com/categories/canvas/stretched-canvas-by-size/18x24/"
                    },
                    "24-x-36-stretched-canvas": {
                        "name": "24\" x 36\" Stretched Canvas ",
                        "url": "https://www.dickblick.com/categories/canvas/stretched-canvas-by-size/24x36/"
                    },
                    "30-x-40-stretched-canvas": {
                        "name": "30\" x 40\" Stretched Canvas ",
                        "url": "https://www.dickblick.com/categories/canvas/stretched-canvas-by-size/30x40/"
                    },
                    "36-x-48-stretched-canvas": {
                        "name": "36\" x 48\" Stretched Canvas",
                        "url": "https://www.dickblick.com/categories/canvas/stretched-canvas-by-size/36x48/"
                    },
                    "8-x-10-stretched-canvas": {
                        "name": "8\" x 10\" Stretched Canvas",
                        "url": "https://www.dickblick.com/categories/canvas/stretched-canvas-by-size/8x10/"
                    },
                    "extra-large-stretched-canvas": {
                        "name": "Extra Large Stretched Canvas",
                        "url": "https://www.dickblick.com/categories/canvas/stretched-canvas-by-size/extra-large-canvas/"
                    }
                }
            },
            "stretcher-bars-and-braces": {
                "name": "Stretcher Bars and Braces",
                "url": "https://www.dickblick.com/categories/canvas/stretcher-bars/"
            }
        }
    },
    "art-easels": {
        "name": "Art Easels",
        "url": "https://www.dickblick.com/categories/easels/",
        "children": {
            "a-frame-easels": {
                "name": "A-Frame Easels",
                "url": "https://www.dickblick.com/categories/easels/a-frame/"
            },
            "art-display-easels": {
                "name": "Art Display Easels",
                "url": "https://www.dickblick.com/categories/easels/display/"
            },
            "classroom-easels": {
                "name": "Classroom Easels",
                "url": "https://www.dickblick.com/categories/easels/classroom/"
            },
            "easel-lights": {
                "name": "Easel Lights",
                "url": "https://www.dickblick.com/categories/easels/lights/"
            },
            "french-and-plein-air-easels": {
                "name": "French and Plein Air Easels",
                "url": "https://www.dickblick.com/categories/easels/french-plein-air/"
            },
            "h-frame-easels": {
                "name": "H-Frame Easels",
                "url": "https://www.dickblick.com/categories/easels/h-frame/"
            },
            "kids-easels": {
                "name": "Kids' Easels",
                "url": "https://www.dickblick.com/categories/easels/kids/"
            },
            "metal-and-aluminum-easels": {
                "name": "Metal and Aluminum Easels",
                "url": "https://www.dickblick.com/categories/easels/metal-aluminum/"
            },
            "studio-easels": {
                "name": "Studio Easels",
                "url": "https://www.dickblick.com/categories/easels/studio/"
            },
            "tabletop-easels": {
                "name": "Tabletop Easels",
                "url": "https://www.dickblick.com/categories/easels/tabletop/"
            },
            "wooden-easels": {
                "name": "Wooden Easels",
                "url": "https://www.dickblick.com/categories/easels/wooden/"
            }
        }
    },
    "art-paper-and-boards": {
        "name": "Art Paper and Boards",
        "url": "https://www.dickblick.com/categories/paper/",
        "children": {
            "boards": {
                "name": "Boards",
                "url": "https://www.dickblick.com/categories/paper/boards/",
                "children": {
                    "chipboard": {
                        "name": "Chipboard",
                        "url": "https://www.dickblick.com/categories/paper/boards/chipboard/"
                    },
                    "foam-board": {
                        "name": "Foam Board",
                        "url": "https://www.dickblick.com/categories/paper/boards/foam-board/"
                    },
                    "poster-board": {
                        "name": "Poster Board",
                        "url": "https://www.dickblick.com/categories/paper/boards/poster-board/"
                    },
                    "project-display-boards": {
                        "name": "Project Display Boards",
                        "url": "https://www.dickblick.com/categories/paper/boards/display-boards/"
                    },
                    "sculpture-board": {
                        "name": "Sculpture Board",
                        "url": "https://www.dickblick.com/categories/paper/boards/sculpture-board/"
                    }
                }
            },
            "colored-and-decorative-paper": {
                "name": "Colored and Decorative Paper",
                "url": "https://www.dickblick.com/categories/paper/colored-decorative/",
                "children": {
                    "cardstock": {
                        "name": "Cardstock",
                        "url": "https://www.dickblick.com/categories/paper/colored-decorative/cardstock/"
                    },
                    "colored-paper": {
                        "name": "Colored Paper",
                        "url": "https://www.dickblick.com/categories/paper/colored-decorative/colored/"
                    },
                    "construction-paper": {
                        "name": "Construction Paper",
                        "url": "https://www.dickblick.com/categories/paper/colored-decorative/construction/"
                    },
                    "corrugated-paper-and-boards": {
                        "name": "Corrugated Paper and Boards",
                        "url": "https://www.dickblick.com/categories/paper/colored-decorative/corrugated/"
                    },
                    "decorative-and-handmade-paper": {
                        "name": "Decorative and Handmade Paper",
                        "url": "https://www.dickblick.com/categories/paper/colored-decorative/decorative/"
                    },
                    "metallic-paper": {
                        "name": "Metallic Paper",
                        "url": "https://www.dickblick.com/categories/paper/colored-decorative/metallic/"
                    },
                    "scrapbook-paper": {
                        "name": "Scrapbook Paper",
                        "url": "https://www.dickblick.com/categories/paper/colored-decorative/scrapbook/"
                    },
                    "sticky-notes-and-pads": {
                        "name": "Sticky Notes and Pads",
                        "url": "https://www.dickblick.com/categories/paper/colored-decorative/sticky-notes/"
                    },
                    "tissue-paper-and-crepe-paper": {
                        "name": "Tissue Paper and Crepe Paper",
                        "url": "https://www.dickblick.com/categories/paper/colored-decorative/tissue-crepe/"
                    }
                }
            },
            "cutting-tools": {
                "name": "Cutting Tools",
                "url": None,
                "children": {
                    "die-cutting-and-digital-cutting-machines": {
                        "name": "Die Cutting and Digital Cutting Machines",
                        "url": "https://www.dickblick.com/categories/paper/cutting-tools/die-cut/"
                    }
                }
            },
            "films-and-barrier-paper": {
                "name": "Films and Barrier Paper",
                "url": "https://www.dickblick.com/categories/paper/films/",
                "children": {
                    "acetate-film": {
                        "name": "Acetate Film",
                        "url": "https://www.dickblick.com/categories/paper/films/acetate/"
                    },
                    "glassine-paper-and-barrier-paper": {
                        "name": "Glassine Paper and Barrier Paper",
                        "url": "https://www.dickblick.com/categories/paper/films/glassine-barrier/"
                    },
                    "stencil-paper-and-films": {
                        "name": "Stencil Paper and Films",
                        "url": "https://www.dickblick.com/categories/paper/films/stencil-paper/"
                    }
                }
            },
            "japanese-paper": {
                "name": "Japanese Paper",
                "url": "https://www.dickblick.com/categories/paper/japanese/"
            },
            "kids-paper": {
                "name": "Kids' Paper",
                "url": "https://www.dickblick.com/categories/paper/kids/",
                "children": {
                    "kids-canvas": {
                        "name": "Kids' Canvas",
                        "url": "https://www.dickblick.com/categories/paper/kids/canvas/"
                    },
                    "kids-painting-paper": {
                        "name": "Kids' Painting Paper",
                        "url": "https://www.dickblick.com/categories/paper/kids/painting-paper/"
                    }
                }
            },
            "painting-papers-and-pads": {
                "name": "Painting Papers and Pads",
                "url": "https://www.dickblick.com/categories/paper/painting/",
                "children": {
                    "acrylic-painting-paper-and-pads": {
                        "name": "Acrylic Painting Paper and Pads",
                        "url": "https://www.dickblick.com/categories/paper/painting/acrylic-paper/"
                    },
                    "canvas-pads": {
                        "name": "Canvas Pads",
                        "url": "https://www.dickblick.com/categories/paper/painting/canvas-pads/"
                    },
                    "mixed-media-art-boards": {
                        "name": "Mixed Media Art Boards",
                        "url": "https://www.dickblick.com/categories/paper/painting/mixed-media-board/"
                    },
                    "oil-painting-paper-and-pads": {
                        "name": "Oil Painting Paper and Pads",
                        "url": "https://www.dickblick.com/categories/paper/painting/oil-paper/"
                    }
                }
            },
            "paper-crafts": {
                "name": "Paper Crafts",
                "url": "https://www.dickblick.com/categories/paper/crafts/",
                "children": {
                    "bookmaking-and-bookbinding-supplies": {
                        "name": "Bookmaking and Bookbinding Supplies",
                        "url": "https://www.dickblick.com/categories/paper/crafts/bookmaking/"
                    },
                    "marbling-supplies": {
                        "name": "Marbling Supplies",
                        "url": "https://www.dickblick.com/categories/paper/crafts/marbling/"
                    },
                    "origami-paper": {
                        "name": "Origami Paper",
                        "url": "https://www.dickblick.com/categories/paper/crafts/origami/"
                    },
                    "paper-craft-kits-and-sets": {
                        "name": "Paper Craft Kits and Sets",
                        "url": "https://www.dickblick.com/categories/paper/crafts/kits/"
                    },
                    "paper-craft-tools": {
                        "name": "Paper Craft Tools",
                        "url": "https://www.dickblick.com/categories/paper/crafts/tools/"
                    },
                    "paper-embossing": {
                        "name": "Paper Embossing",
                        "url": "https://www.dickblick.com/categories/paper/crafts/embossing/"
                    },
                    "paper-soaking-trays-and-tubs": {
                        "name": "Paper Soaking Trays and Tubs",
                        "url": "https://www.dickblick.com/categories/paper/crafts/soaking-trays/"
                    },
                    "papermaking": {
                        "name": "Papermaking",
                        "url": "https://www.dickblick.com/categories/paper/crafts/papermaking/"
                    },
                    "quilling": {
                        "name": "Quilling",
                        "url": "https://www.dickblick.com/categories/paper/crafts/quilling/"
                    },
                    "rubber-stamping": {
                        "name": "Rubber Stamping",
                        "url": "https://www.dickblick.com/categories/paper/crafts/rubber-stamping/"
                    },
                    "shrink-film": {
                        "name": "Shrink Film",
                        "url": "https://www.dickblick.com/categories/paper/crafts/shrink-film/"
                    }
                }
            },
            "paper-rolls": {
                "name": "Paper Rolls",
                "url": "https://www.dickblick.com/categories/paper/rolls/",
                "children": {
                    "banner-and-background-paper-rolls": {
                        "name": "Banner and Background Paper Rolls",
                        "url": "https://www.dickblick.com/categories/paper/rolls/banner/"
                    },
                    "colored-paper-rolls": {
                        "name": "Colored Paper Rolls",
                        "url": "https://www.dickblick.com/categories/paper/rolls/colored/"
                    },
                    "tracing-paper-rolls": {
                        "name": "Tracing Paper Rolls",
                        "url": "https://www.dickblick.com/categories/paper/rolls/tracing/"
                    },
                    "utility-and-kraft-paper-rolls": {
                        "name": "Utility and Kraft Paper Rolls",
                        "url": "https://www.dickblick.com/categories/paper/rolls/kraft-paper/"
                    }
                }
            },
            "watercolor-paper-and-pads": {
                "name": "Watercolor Paper and Pads",
                "url": "https://www.dickblick.com/categories/paper/watercolor-paper/",
                "children": {
                    "100-cotton-watercolor-paper": {
                        "name": "100% Cotton Watercolor Paper",
                        "url": "https://www.dickblick.com/categories/paper/watercolor-paper/cotton/"
                    },
                    "cold-press-watercolor-paper": {
                        "name": "Cold Press Watercolor Paper",
                        "url": "https://www.dickblick.com/categories/paper/watercolor-paper/cold-press/"
                    },
                    "hot-press-watercolor-paper": {
                        "name": "Hot Press Watercolor Paper",
                        "url": "https://www.dickblick.com/categories/paper/watercolor-paper/hot-press/"
                    },
                    "synthetic-paper-and-pads": {
                        "name": "Synthetic Paper and Pads",
                        "url": "https://www.dickblick.com/categories/paper/watercolor-paper/synthetic/"
                    },
                    "watercolor-blocks": {
                        "name": "Watercolor Blocks ",
                        "url": "https://www.dickblick.com/categories/paper/watercolor-paper/blocks/"
                    },
                    "watercolor-cards-and-envelopes": {
                        "name": "Watercolor Cards and Envelopes",
                        "url": "https://www.dickblick.com/categories/paper/watercolor-paper/cards/"
                    },
                    "watercolor-pads": {
                        "name": "Watercolor Pads",
                        "url": "https://www.dickblick.com/categories/paper/watercolor-paper/pads/"
                    },
                    "watercolor-panels-and-boards": {
                        "name": "Watercolor Panels and Boards",
                        "url": "https://www.dickblick.com/categories/paper/watercolor-paper/panels/"
                    },
                    "watercolor-paper-stretching": {
                        "name": "Watercolor Paper Stretching",
                        "url": "https://www.dickblick.com/categories/paper/watercolor-paper/boards/"
                    },
                    "watercolor-sketchbooks-and-journals": {
                        "name": "Watercolor Sketchbooks and Journals ",
                        "url": "https://www.dickblick.com/categories/paper/watercolor-paper/sketchbooks/"
                    }
                }
            }
        }
    },
    "books-for-artists": {
        "name": "Books for Artists",
        "url": "https://www.dickblick.com/categories/books/",
        "children": {
            "art-education-books-and-resources": {
                "name": "Art Education Books and Resources",
                "url": "https://www.dickblick.com/categories/books/art-education/",
                "children": {
                    "art-education-and-instruction-books": {
                        "name": "Art Education and Instruction Books",
                        "url": "https://www.dickblick.com/categories/books/art-education/instruction/"
                    },
                    "art-history-books": {
                        "name": "Art History Books",
                        "url": "https://www.dickblick.com/categories/books/art-education/art-history/"
                    },
                    "art-instructional-materials": {
                        "name": "Art Instructional Materials",
                        "url": "https://www.dickblick.com/categories/books/art-education/instructional-materials/"
                    }
                }
            },
            "artist-books-by-subject": {
                "name": "Artist Books by Subject",
                "url": "https://www.dickblick.com/categories/books/subject/",
                "children": {
                    "animal-and-wildlife-books": {
                        "name": "Animal and Wildlife Books",
                        "url": "https://www.dickblick.com/categories/books/subject/animals/"
                    },
                    "fantasy-and-cosplay-books": {
                        "name": "Fantasy and Cosplay Books",
                        "url": "https://www.dickblick.com/categories/books/subject/fantasy/"
                    },
                    "landscape-and-nature-books": {
                        "name": "Landscape and Nature Books",
                        "url": "https://www.dickblick.com/categories/books/subject/landscapes/"
                    }
                }
            },
            "ceramics-and-sculpture-books": {
                "name": "Ceramics and Sculpture Books",
                "url": "https://www.dickblick.com/categories/books/ceramics-sculpture/",
                "children": {
                    "ceramics-and-pottery-books": {
                        "name": "Ceramics and Pottery Books",
                        "url": "https://www.dickblick.com/categories/books/ceramics-sculpture/ceramics/"
                    },
                    "paper-sculpture-books": {
                        "name": "Paper Sculpture Books",
                        "url": "https://www.dickblick.com/categories/books/ceramics-sculpture/paper-sculpture/"
                    },
                    "sculpture-books": {
                        "name": "Sculpture Books",
                        "url": "https://www.dickblick.com/categories/books/ceramics-sculpture/sculpture/"
                    }
                }
            },
            "coffee-table-art-books": {
                "name": "Coffee Table Art Books",
                "url": "https://www.dickblick.com/categories/books/coffee-table/"
            },
            "coloring-books-and-activity-books": {
                "name": "Coloring Books and Activity Books",
                "url": "https://www.dickblick.com/categories/books/coloring/",
                "children": {
                    "adult-coloring-books": {
                        "name": "Adult Coloring Books",
                        "url": "https://www.dickblick.com/categories/books/coloring/adult/"
                    }
                }
            },
            "craft-books": {
                "name": "Craft Books",
                "url": "https://www.dickblick.com/categories/books/crafts/"
            },
            "drawing-books": {
                "name": "Drawing Books",
                "url": "https://www.dickblick.com/categories/books/drawing/",
                "children": {
                    "cartooning-and-manga-books": {
                        "name": "Cartooning and Manga Books",
                        "url": "https://www.dickblick.com/categories/books/drawing/cartooning/"
                    },
                    "lettering-and-calligraphy-books": {
                        "name": "Lettering and Calligraphy Books",
                        "url": "https://www.dickblick.com/categories/books/drawing/lettering/"
                    },
                    "marker-and-pen-and-ink-books": {
                        "name": "Marker and Pen-and-Ink Books",
                        "url": "https://www.dickblick.com/categories/books/drawing/markers-pens/"
                    },
                    "pastel-books": {
                        "name": "Pastel Books",
                        "url": "https://www.dickblick.com/categories/books/drawing/pastels/"
                    },
                    "pencil-and-colored-pencil-books": {
                        "name": "Pencil and Colored Pencil Books",
                        "url": "https://www.dickblick.com/categories/books/drawing/pencils/"
                    },
                    "perspective-and-proportion-books": {
                        "name": "Perspective and Proportion Books",
                        "url": "https://www.dickblick.com/categories/books/drawing/perspective/"
                    },
                    "portraiture-and-figure-drawing-books": {
                        "name": "Portraiture and Figure Drawing Books",
                        "url": "https://www.dickblick.com/categories/books/drawing/portraiture/"
                    }
                }
            },
            "kids-books": {
                "name": "Kids' Books",
                "url": "https://www.dickblick.com/categories/books/kids/",
                "children": {
                    "activity-books-and-coloring-books-for-kids": {
                        "name": "Activity Books and Coloring Books for Kids",
                        "url": "https://www.dickblick.com/categories/books/kids/coloring/"
                    },
                    "art-appreciation-books-for-kids": {
                        "name": "Art Appreciation Books for Kids",
                        "url": "https://www.dickblick.com/categories/books/kids/art-appreciation/"
                    },
                    "art-storybooks-for-kids": {
                        "name": "Art Storybooks for Kids",
                        "url": "https://www.dickblick.com/categories/books/kids/storybooks/"
                    },
                    "drawing-books-for-kids": {
                        "name": "Drawing Books for Kids",
                        "url": "https://www.dickblick.com/categories/books/kids/drawing/"
                    }
                }
            },
            "painting-books": {
                "name": "Painting Books",
                "url": "https://www.dickblick.com/categories/books/painting/",
                "children": {
                    "acrylic-painting-books": {
                        "name": "Acrylic Painting Books",
                        "url": "https://www.dickblick.com/categories/books/painting/acrylic/"
                    },
                    "color-theory-books": {
                        "name": "Color Theory Books",
                        "url": "https://www.dickblick.com/categories/books/painting/color-theory/"
                    },
                    "mixed-media-books": {
                        "name": "Mixed Media Books",
                        "url": "https://www.dickblick.com/categories/books/painting/encaustic/"
                    },
                    "oil-painting-books": {
                        "name": "Oil Painting Books",
                        "url": "https://www.dickblick.com/categories/books/painting/oil/"
                    },
                    "sumi-painting-books": {
                        "name": "Sumi Painting Books",
                        "url": "https://www.dickblick.com/categories/books/painting/sumi/"
                    },
                    "watercolor-books": {
                        "name": "Watercolor Books",
                        "url": "https://www.dickblick.com/categories/books/painting/watercolor/"
                    }
                }
            },
            "printmaking-books": {
                "name": "Printmaking Books ",
                "url": "https://www.dickblick.com/categories/books/printmaking/"
            },
            "textile-and-jewelry-making-books": {
                "name": "Textile and Jewelry Making Books",
                "url": "https://www.dickblick.com/categories/books/textile-jewelry/"
            }
        }
    },
    "brushes-and-painting-tools": {
        "name": "Brushes and Painting Tools",
        "url": "https://www.dickblick.com/categories/brushes/",
        "children": {
            "acrylic-brushes": {
                "name": "Acrylic Brushes",
                "url": "https://www.dickblick.com/categories/brushes/acrylic/",
                "children": {
                    "acrylic-paint-brush-sets": {
                        "name": "Acrylic Paint Brush Sets",
                        "url": "https://www.dickblick.com/categories/brushes/acrylic/sets/"
                    },
                    "kids-acrylic-and-tempera-brushes": {
                        "name": "Kids' Acrylic and Tempera Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/acrylic/classroom/"
                    },
                    "natural-hair-acrylic-brushes": {
                        "name": "Natural Hair Acrylic Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/acrylic/natural/"
                    },
                    "synthetic-acrylic-paint-brushes": {
                        "name": "Synthetic Acrylic Paint Brushes ",
                        "url": "https://www.dickblick.com/categories/brushes/acrylic/synthetic/"
                    }
                }
            },
            "brush-sets-and-packs": {
                "name": "Brush Sets and Packs",
                "url": "https://www.dickblick.com/categories/brushes/sets/",
                "children": {
                    "kids-brush-sets-and-canisters": {
                        "name": "Kids' Brush Sets and Canisters",
                        "url": "https://www.dickblick.com/categories/brushes/sets/classroom/"
                    }
                }
            },
            "brushes-by-shape": {
                "name": "Brushes by Shape",
                "url": "https://www.dickblick.com/categories/brushes/shapes/",
                "children": {
                    "angular-brushes": {
                        "name": "Angular Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/angular/"
                    },
                    "bright-brushes": {
                        "name": "Bright Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/bright/"
                    },
                    "fan-brushes": {
                        "name": "Fan Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/fan/"
                    },
                    "filbert-paint-brushes": {
                        "name": "Filbert Paint Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/filbert/"
                    },
                    "flat-brushes": {
                        "name": "Flat Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/flat/"
                    },
                    "hake-brushes": {
                        "name": "Hake Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/hake/"
                    },
                    "liner-paint-brushes": {
                        "name": "Liner Paint Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/liner/"
                    },
                    "mop-paint-brushes": {
                        "name": "Mop Paint Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/mop/"
                    },
                    "mottler-brushes": {
                        "name": "Mottler Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/mottler/"
                    },
                    "one-stroke-brushes": {
                        "name": "One Stroke Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/one-stroke/"
                    },
                    "oval-wash-brushes": {
                        "name": "Oval Wash Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/oval-wash/"
                    },
                    "paddle-brushes": {
                        "name": "Paddle Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/paddle/"
                    },
                    "quill-brushes": {
                        "name": "Quill Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/quill/"
                    },
                    "rigger-brushes": {
                        "name": "Rigger Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/rigger/"
                    },
                    "round-paint-brushes": {
                        "name": "Round Paint Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/round/"
                    },
                    "wash-brushes": {
                        "name": "Wash Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/shapes/wash/"
                    }
                }
            },
            "craft-and-specialty-brushes": {
                "name": "Craft and Specialty Brushes",
                "url": "https://www.dickblick.com/categories/brushes/specialty/",
                "children": {
                    "ceramic-and-glazing-brushes": {
                        "name": "Ceramic and Glazing Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/ceramic-glazing/"
                    },
                    "decorative-and-tole-brushes": {
                        "name": "Decorative and Tole Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/decorative/"
                    },
                    "encaustic-brushes": {
                        "name": "Encaustic Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/encaustic/"
                    },
                    "faux-finish-brushes-and-tools": {
                        "name": "Faux Finish Brushes and Tools",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/faux-finish/"
                    },
                    "foam-and-sponge-brushes": {
                        "name": "Foam and Sponge Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/foam-sponge/"
                    },
                    "lettering-brushes": {
                        "name": "Lettering Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/lettering/"
                    },
                    "makeup-brushes-and-accessories": {
                        "name": "Makeup Brushes and Accessories",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/makeup/"
                    },
                    "miniature-brushes": {
                        "name": "Miniature Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/miniature/"
                    },
                    "mixed-media-brushes": {
                        "name": "Mixed Media Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/mixed-media/"
                    },
                    "mural-and-large-scale-paint-brushes": {
                        "name": "Mural and Large Scale Paint Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/mural-oversize/"
                    },
                    "pinstriping-brushes-and-tools": {
                        "name": "Pinstriping Brushes and Tools",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/pinstriping/"
                    },
                    "stencil-brushes": {
                        "name": "Stencil Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/stencil/"
                    },
                    "travel-and-pocket-paint-brushes": {
                        "name": "Travel and Pocket Paint Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/travel/"
                    },
                    "varnish-and-gesso-brushes": {
                        "name": "Varnish and Gesso Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/specialty/varnish-gesso/"
                    }
                }
            },
            "kids-brushes": {
                "name": "Kids' Brushes",
                "url": "https://www.dickblick.com/categories/brushes/kids/"
            },
            "natural-hair-brushes": {
                "name": "Natural Hair Brushes",
                "url": "https://www.dickblick.com/categories/brushes/natural/",
                "children": {
                    "badger-brushes": {
                        "name": "Badger Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/natural/badger/"
                    },
                    "bristle-paint-brushes": {
                        "name": "Bristle Paint Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/natural/bristle/"
                    },
                    "goat-and-ox-brushes": {
                        "name": "Goat and Ox Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/natural/goat-ox/"
                    },
                    "kolinsky-and-sable-brushes": {
                        "name": "Kolinsky and Sable Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/natural/sable/"
                    },
                    "natural-brushes-by-shape": {
                        "name": "Natural Brushes by Shape",
                        "url": "https://www.dickblick.com/categories/brushes/natural/shape/"
                    },
                    "squirrel-paint-brushes": {
                        "name": "Squirrel Paint Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/natural/squirrel/"
                    }
                }
            },
            "oil-paint-brushes": {
                "name": "Oil Paint Brushes",
                "url": "https://www.dickblick.com/categories/brushes/oil/",
                "children": {
                    "natural-hair-oil-brushes": {
                        "name": "Natural Hair Oil Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/oil/natural/"
                    },
                    "oil-brush-sets": {
                        "name": "Oil Brush Sets",
                        "url": "https://www.dickblick.com/categories/brushes/oil/sets/"
                    },
                    "synthetic-oil-brushes": {
                        "name": "Synthetic Oil Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/oil/synthetic/"
                    }
                }
            },
            "paint-brush-cleaners-and-washers": {
                "name": "Paint Brush Cleaners and Washers",
                "url": "https://www.dickblick.com/categories/brushes/cleaners/"
            },
            "paint-brush-holders-and-organizers": {
                "name": "Paint Brush Holders and Organizers",
                "url": "https://www.dickblick.com/categories/brushes/holders/"
            },
            "synthetic-brushes": {
                "name": "Synthetic Brushes",
                "url": "https://www.dickblick.com/categories/brushes/synthetic/",
                "children": {
                    "synthetic-brushes-by-shape": {
                        "name": "Synthetic Brushes by Shape",
                        "url": "https://www.dickblick.com/categories/brushes/synthetic/shape/"
                    }
                }
            },
            "watercolor-brushes": {
                "name": "Watercolor Brushes",
                "url": "https://www.dickblick.com/categories/brushes/watercolor/",
                "children": {
                    "kids-watercolor-brushes": {
                        "name": "Kids' Watercolor Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/watercolor/classroom/"
                    },
                    "natural-watercolor-brushes": {
                        "name": "Natural Watercolor Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/watercolor/natural/"
                    },
                    "synthetic-watercolor-brushes": {
                        "name": "Synthetic Watercolor Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/watercolor/synthetic/"
                    },
                    "water-brushes": {
                        "name": "Water Brushes",
                        "url": "https://www.dickblick.com/categories/brushes/watercolor/water-brushes/"
                    },
                    "watercolor-paint-brush-sets": {
                        "name": "Watercolor Paint Brush Sets",
                        "url": "https://www.dickblick.com/categories/brushes/watercolor/sets/"
                    }
                }
            }
        }
    },
    "ceramics-and-sculpture": {
        "name": "Ceramics and Sculpture",
        "url": "https://www.dickblick.com/categories/ceramics-sculpture/",
        "children": {
            "carving": {
                "name": "Carving",
                "url": "https://www.dickblick.com/categories/ceramics-sculpture/carving/",
                "children": {
                    "carving-materials": {
                        "name": "Carving Materials",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/carving/materials/"
                    },
                    "sculpture-and-carving-tools": {
                        "name": "Sculpture and Carving Tools",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/carving/tools/"
                    }
                }
            },
            "ceramic-bisque": {
                "name": "Ceramic Bisque",
                "url": "https://www.dickblick.com/categories/ceramics-sculpture/bisque/"
            },
            "ceramic-and-pottery-glazes": {
                "name": "Ceramic and Pottery Glazes",
                "url": "https://www.dickblick.com/categories/ceramics-sculpture/glazes/",
                "children": {
                    "ceramic-glaze-tools": {
                        "name": "Ceramic Glaze Tools",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/glazes/tools/"
                    },
                    "ceramic-transfers-and-decals": {
                        "name": "Ceramic Transfers and Decals",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/glazes/transfers-decals/"
                    },
                    "ceramic-underglazes": {
                        "name": "Ceramic Underglazes",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/glazes/underglazes/"
                    },
                    "glaze-additives-and-resist": {
                        "name": "Glaze Additives and Resist",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/glazes/additives/"
                    },
                    "low-fire-glazes-and-effects": {
                        "name": "Low-Fire Glazes and Effects",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/glazes/low-fire/"
                    },
                    "mid-to-high-fire-glazes-and-effects": {
                        "name": "Mid to High-Fire Glazes and Effects",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/glazes/mid-high-fire/"
                    }
                }
            },
            "clay-and-modeling-materials": {
                "name": "Clay and Modeling Materials",
                "url": "https://www.dickblick.com/categories/ceramics-sculpture/clay/",
                "children": {
                    "air-dry-clay": {
                        "name": "Air Dry Clay",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/clay/air-dry/"
                    },
                    "modeling-clay": {
                        "name": "Modeling Clay",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/clay/modeling/"
                    },
                    "modeling-dough": {
                        "name": "Modeling Dough",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/clay/modeling-dough/"
                    },
                    "other-sculpting-materials": {
                        "name": "Other Sculpting Materials",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/clay/sculpting-materials/"
                    },
                    "polymer-clay-and-oven-bake-clay": {
                        "name": "Polymer Clay and Oven Bake Clay",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/clay/polymer/"
                    },
                    "pottery-clay": {
                        "name": "Pottery Clay",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/clay/firing/"
                    }
                }
            },
            "glass-art": {
                "name": "Glass Art",
                "url": "https://www.dickblick.com/categories/ceramics-sculpture/glass-art/",
                "children": {
                    "glass-cutters-and-grinders": {
                        "name": "Glass Cutters and Grinders",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/glass-art/glass-cutters/"
                    },
                    "glass-etching": {
                        "name": "Glass Etching",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/glass-art/glass-etching/"
                    },
                    "glass-fusing-and-casting": {
                        "name": "Glass Fusing and Casting",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/glass-art/glass-fusing-casting/"
                    },
                    "glass-and-porcelain-paint": {
                        "name": "Glass and Porcelain Paint",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/glass-art/porcelain-paints/"
                    },
                    "stained-glass-supplies": {
                        "name": "Stained Glass Supplies",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/glass-art/stained-glass/"
                    }
                }
            },
            "kilns-and-firing-accessories": {
                "name": "Kilns and Firing Accessories",
                "url": "https://www.dickblick.com/categories/ceramics-sculpture/kilns/",
                "children": {
                    "enameling-and-glass-kilns": {
                        "name": "Enameling and Glass Kilns",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/kilns/glass-kilns/"
                    },
                    "kiln-cleaning-and-maintenance": {
                        "name": "Kiln Cleaning and Maintenance",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/kilns/cleaning/"
                    },
                    "kiln-safety-and-ventilation": {
                        "name": "Kiln Safety and Ventilation",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/kilns/safety/"
                    },
                    "kiln-shelves-and-parts": {
                        "name": "Kiln Shelves and Parts",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/kilns/parts/"
                    },
                    "pottery-and-ceramic-kilns": {
                        "name": "Pottery & Ceramic Kilns",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/kilns/ceramic-kilns/"
                    },
                    "pyrometric-cones-and-bars": {
                        "name": "Pyrometric Cones and Bars",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/kilns/pyrometric-cones/"
                    }
                }
            },
            "modeling-and-pottery-tools": {
                "name": "Modeling and Pottery Tools",
                "url": "https://www.dickblick.com/categories/ceramics-sculpture/tools/",
                "children": {
                    "calipers": {
                        "name": "Calipers",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/tools/calipers/"
                    },
                    "clay-cutters": {
                        "name": "Clay Cutters",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/tools/clay-cutters/"
                    },
                    "clay-modeling-tools": {
                        "name": "Clay Modeling Tools",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/tools/clay-modeling-tools/"
                    },
                    "clay-molds-and-texture-tools": {
                        "name": "Clay Molds and Texture Tools",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/tools/clay-molds-texture/"
                    },
                    "clay-slab-rollers-and-rolling-pins": {
                        "name": "Clay Slab Rollers and Rolling Pins",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/tools/slab-rollers/"
                    },
                    "clay-and-color-shapers": {
                        "name": "Clay and Color Shapers",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/tools/color-shapers/"
                    },
                    "needle-and-sgraffito-tools": {
                        "name": "Needle and Sgraffito Tools",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/tools/needle-sgraffito/"
                    },
                    "pottery-ribs-and-scrapers": {
                        "name": "Pottery Ribs and Scrapers",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/tools/pottery-ribs/"
                    },
                    "pottery-trimming-tools": {
                        "name": "Pottery Trimming Tools",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/tools/loop-ribbon/"
                    },
                    "sponges": {
                        "name": "Sponges",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/tools/sponges/"
                    },
                    "tongs-and-lifting-tools": {
                        "name": "Tongs and Lifting Tools",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/tools/tongs/"
                    }
                }
            },
            "mold-making-and-casting": {
                "name": "Mold Making and Casting",
                "url": "https://www.dickblick.com/categories/ceramics-sculpture/mold-making-casting/",
                "children": {
                    "casting-materials": {
                        "name": "Casting Materials",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/mold-making-casting/casting/"
                    },
                    "mold-making-materials": {
                        "name": "Mold Making Materials",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/mold-making-casting/mold-making/"
                    },
                    "pre-made-molds": {
                        "name": "Pre-Made Molds",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/mold-making-casting/pre-made-molds/"
                    },
                    "resin-art-supplies": {
                        "name": "Resin Art Supplies",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/mold-making-casting/resin/"
                    },
                    "silicone-and-rubber": {
                        "name": "Silicone and Rubber",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/mold-making-casting/silicone-rubber/"
                    }
                }
            },
            "pottery-wheels-and-equipment": {
                "name": "Pottery Wheels and Equipment",
                "url": "https://www.dickblick.com/categories/ceramics-sculpture/equipment/",
                "children": {
                    "banding-wheels-and-modeling-stands": {
                        "name": "Banding Wheels and Modeling Stands",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/equipment/banding-wheels/"
                    },
                    "clay-extruders": {
                        "name": "Clay Extruders",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/equipment/clay-extruders/"
                    },
                    "containers-for-storing-and-mixing-clay": {
                        "name": "Containers for Storing and Mixing Clay",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/equipment/clay-containers/"
                    },
                    "damp-and-dry-storage-cabinets": {
                        "name": "Damp and Dry Storage Cabinets",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/equipment/damp-dry-storage/"
                    },
                    "pottery-bats-and-wheel-accessories": {
                        "name": "Pottery Bats and Wheel Accessories",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/equipment/pottery-bats/"
                    },
                    "pottery-wheels": {
                        "name": "Pottery Wheels",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/equipment/pottery-wheels/"
                    },
                    "pug-mills": {
                        "name": "Pug Mills",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/equipment/pug-mills/"
                    },
                    "wedging-tables-and-boards": {
                        "name": "Wedging Tables and Boards",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/equipment/wedging-boards/"
                    }
                }
            },
            "wire-sculpture-supplies": {
                "name": "Wire Sculpture Supplies",
                "url": "https://www.dickblick.com/categories/ceramics-sculpture/metal-sculpture/",
                "children": {
                    "armature-wire-and-wire-form": {
                        "name": "Armature Wire and Wire Form",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/metal-sculpture/armature-wire/"
                    },
                    "craft-wire": {
                        "name": "Craft Wire",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/metal-sculpture/jewelry-wire/"
                    },
                    "jewelry-and-wire-tools": {
                        "name": "Jewelry and Wire Tools",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/metal-sculpture/jewelry-wire-tools/"
                    },
                    "metal-sheets-and-rods": {
                        "name": "Metal Sheets and Rods",
                        "url": "https://www.dickblick.com/categories/ceramics-sculpture/metal-sculpture/metal-sheets-rods/"
                    }
                }
            }
        }
    },
    "crafts-and-textiles": {
        "name": "Crafts & Textiles",
        "url": "https://www.dickblick.com/categories/crafts/",
        "children": {
            "art-stencils-and-stenciling-supplies": {
                "name": "Art Stencils and Stenciling Supplies",
                "url": "https://www.dickblick.com/categories/crafts/stencils/",
                "children": {
                    "decorative-and-craft-stencils": {
                        "name": "Decorative and Craft Stencils",
                        "url": "https://www.dickblick.com/categories/crafts/stencils/decorative/"
                    },
                    "stencil-cutters-and-burners": {
                        "name": "Stencil Cutters and Burners",
                        "url": "https://www.dickblick.com/categories/crafts/stencils/cutters/"
                    }
                }
            },
            "beads-and-jewelry-making": {
                "name": "Beads and Jewelry Making",
                "url": "https://www.dickblick.com/categories/crafts/jewelry-making/",
                "children": {
                    "bead-and-jewelry-storage": {
                        "name": "Bead and Jewelry Storage",
                        "url": "https://www.dickblick.com/categories/crafts/jewelry-making/storage/"
                    },
                    "jewelry-beads": {
                        "name": "Jewelry Beads",
                        "url": "https://www.dickblick.com/categories/crafts/jewelry-making/beads/"
                    },
                    "jewelry-cord-and-thread": {
                        "name": "Jewelry Cord and Thread",
                        "url": "https://www.dickblick.com/categories/crafts/jewelry-making/cord/"
                    },
                    "jewelry-findings": {
                        "name": "Jewelry Findings",
                        "url": "https://www.dickblick.com/categories/crafts/jewelry-making/findings/"
                    },
                    "jewelry-glue-and-adhesives": {
                        "name": "Jewelry Glue and Adhesives",
                        "url": "https://www.dickblick.com/categories/crafts/jewelry-making/glue/"
                    },
                    "metal-jewelry-making": {
                        "name": "Metal Jewelry Making",
                        "url": "https://www.dickblick.com/categories/crafts/jewelry-making/metal/"
                    },
                    "resin-jewelry": {
                        "name": "Resin Jewelry",
                        "url": "https://www.dickblick.com/categories/crafts/jewelry-making/resin/"
                    },
                    "soldering-tools-and-materials": {
                        "name": "Soldering Tools and Materials",
                        "url": "https://www.dickblick.com/categories/crafts/jewelry-making/soldering/"
                    }
                }
            },
            "candle-making-and-candles": {
                "name": "Candle Making and Candles",
                "url": "https://www.dickblick.com/categories/crafts/candle-making/"
            },
            "collage-and-scrapbooking": {
                "name": "Collage and Scrapbooking",
                "url": "https://www.dickblick.com/categories/crafts/collage/",
                "children": {
                    "collage-glue-and-adhesives": {
                        "name": "Collage Glue and Adhesives",
                        "url": "https://www.dickblick.com/categories/crafts/collage/adhesives/"
                    },
                    "collage-materials": {
                        "name": "Collage Materials",
                        "url": "https://www.dickblick.com/categories/crafts/collage/materials/"
                    }
                }
            },
            "cosplay-supplies": {
                "name": "Cosplay Supplies",
                "url": "https://www.dickblick.com/categories/crafts/cosplay/",
                "children": {
                    "cosplay-embellishments": {
                        "name": "Cosplay Embellishments",
                        "url": "https://www.dickblick.com/categories/crafts/cosplay/embellishments/"
                    },
                    "cosplay-foam": {
                        "name": "Cosplay Foam",
                        "url": "https://www.dickblick.com/categories/crafts/cosplay/foam/"
                    },
                    "cosplay-thermoplastics": {
                        "name": "Cosplay Thermoplastics",
                        "url": "https://www.dickblick.com/categories/crafts/cosplay/thermoplastics/"
                    },
                    "cosplay-and-costume-fabric": {
                        "name": "Cosplay and Costume Fabric",
                        "url": "https://www.dickblick.com/categories/crafts/cosplay/fabric/"
                    }
                }
            },
            "craft-basics": {
                "name": "Craft Basics",
                "url": "https://www.dickblick.com/categories/crafts/basics/",
                "children": {
                    "buttons-and-pins": {
                        "name": "Buttons and Pins",
                        "url": "https://www.dickblick.com/categories/crafts/basics/buttons-pins/"
                    },
                    "colored-sand": {
                        "name": "Colored Sand",
                        "url": "https://www.dickblick.com/categories/crafts/basics/colored-sand/"
                    },
                    "cork": {
                        "name": "Cork",
                        "url": "https://www.dickblick.com/categories/crafts/basics/cork/"
                    },
                    "craft-assortment-kits": {
                        "name": "Craft Assortment Kits",
                        "url": "https://www.dickblick.com/categories/crafts/basics/craft-kits/"
                    },
                    "craft-canvas": {
                        "name": "Craft Canvas",
                        "url": "https://www.dickblick.com/categories/crafts/basics/craft-canvas/"
                    },
                    "craft-foam-and-carving-foam": {
                        "name": "Craft Foam and Carving Foam",
                        "url": "https://www.dickblick.com/categories/crafts/basics/craft-foam/"
                    },
                    "craft-paper-bags": {
                        "name": "Craft Paper Bags",
                        "url": "https://www.dickblick.com/categories/crafts/craft-basics/paper-bags/"
                    },
                    "craft-sticks": {
                        "name": "Craft Sticks",
                        "url": "https://www.dickblick.com/categories/crafts/basics/craft-sticks/"
                    },
                    "feathers": {
                        "name": "Feathers",
                        "url": "https://www.dickblick.com/categories/crafts/basics/feathers/"
                    },
                    "felt-sheets-and-shapes": {
                        "name": "Felt Sheets and Shapes",
                        "url": "https://www.dickblick.com/categories/crafts/basics/felt/"
                    },
                    "glitter-and-sequins": {
                        "name": "Glitter and Sequins",
                        "url": "https://www.dickblick.com/categories/crafts/basics/glitter-sequins/"
                    },
                    "googly-eyes": {
                        "name": "Googly Eyes",
                        "url": "https://www.dickblick.com/categories/crafts/basics/googly-eyes/"
                    },
                    "lanyard-and-plastic-lacing": {
                        "name": "Lanyard and Plastic Lacing",
                        "url": "https://www.dickblick.com/categories/crafts/basics/plastic-lacing-lanyards/"
                    },
                    "pom-poms": {
                        "name": "Pom Poms",
                        "url": "https://www.dickblick.com/categories/crafts/basics/pom-poms/"
                    },
                    "stems-and-pipe-cleaners": {
                        "name": "Stems and Pipe Cleaners",
                        "url": "https://www.dickblick.com/categories/crafts/basics/pipe-cleaners/"
                    },
                    "stickers-and-sticker-activities": {
                        "name": "Stickers and Sticker Activities",
                        "url": "https://www.dickblick.com/categories/crafts/basics/stickers/"
                    }
                }
            },
            "craft-glue-and-adhesives": {
                "name": "Craft Glue and Adhesives",
                "url": "https://www.dickblick.com/categories/crafts/adhesives/",
                "children": {
                    "fabric-glue-and-adhesives": {
                        "name": "Fabric Glue and Adhesives",
                        "url": "https://www.dickblick.com/categories/crafts/adhesives/fabric-glue/"
                    }
                }
            },
            "craft-kits": {
                "name": "Craft Kits",
                "url": "https://www.dickblick.com/categories/crafts/kits/",
                "children": {
                    "model-building-kits": {
                        "name": "Model Building Kits",
                        "url": "https://www.dickblick.com/categories/crafts/kits/model-building/"
                    },
                    "textile-and-jewelry-kits": {
                        "name": "Textile and Jewelry Kits",
                        "url": "https://www.dickblick.com/categories/crafts/kits/textile-jewelry/"
                    }
                }
            },
            "craft-machines": {
                "name": "Craft Machines ",
                "url": "https://www.dickblick.com/categories/crafts/machines/",
                "children": {
                    "heat-presses": {
                        "name": "Heat Presses",
                        "url": "https://www.dickblick.com/categories/crafts/machines/heat-press/"
                    },
                    "vinyl-transfer-sheets-and-die-cutting-materials": {
                        "name": "Vinyl, Transfer Sheets & Die Cutting Materials",
                        "url": "https://www.dickblick.com/categories/crafts/machines/materials/"
                    }
                }
            },
            "craft-paint": {
                "name": "Craft Paint ",
                "url": "https://www.dickblick.com/categories/crafts/paint/",
                "children": {
                    "acrylic-craft-paint": {
                        "name": "Acrylic Craft Paint",
                        "url": "https://www.dickblick.com/categories/crafts/paint/acrylic-craft-paint/"
                    },
                    "faux-finishes": {
                        "name": "Faux Finishes",
                        "url": "https://www.dickblick.com/categories/crafts/paint/faux-finishes/"
                    },
                    "glow-paints": {
                        "name": "Glow Paints",
                        "url": "https://www.dickblick.com/categories/crafts/paint/glow/"
                    },
                    "leather-paint-and-dyes": {
                        "name": "Leather Paint and Dyes",
                        "url": "https://www.dickblick.com/categories/crafts/paint/leather/"
                    },
                    "metallic-and-glitter-paint": {
                        "name": "Metallic and Glitter Paint",
                        "url": "https://www.dickblick.com/categories/crafts/paint/metallic-glitter/"
                    },
                    "model-paint-primers-and-mediums": {
                        "name": "Model Paint Primers and Mediums",
                        "url": "https://www.dickblick.com/categories/crafts/paint/model-primers/"
                    },
                    "model-and-miniature-paint": {
                        "name": "Model and Miniature Paint",
                        "url": "https://www.dickblick.com/categories/crafts/paint/model-paint/"
                    },
                    "window-paint": {
                        "name": "Window Paint",
                        "url": "https://www.dickblick.com/categories/crafts/paint/window/"
                    }
                }
            },
            "fiber-and-textile-arts": {
                "name": "Fiber and Textile Arts",
                "url": "https://www.dickblick.com/categories/crafts/textile-arts/",
                "children": {
                    "basket-weaving": {
                        "name": "Basket Weaving",
                        "url": "https://www.dickblick.com/categories/crafts/textile-arts/basket-weaving/"
                    },
                    "cross-stitch": {
                        "name": "Cross Stitch",
                        "url": "https://www.dickblick.com/categories/crafts/textile-arts/cross-stitch/"
                    },
                    "embroidery": {
                        "name": "Embroidery",
                        "url": "https://www.dickblick.com/categories/crafts/textile-arts/embroidery/"
                    },
                    "fabric-scissors-and-rotary-cutters": {
                        "name": "Fabric Scissors and Rotary Cutters",
                        "url": "https://www.dickblick.com/categories/crafts/textile-arts/fabric-scissors/"
                    },
                    "knitting-and-crochet": {
                        "name": "Knitting and Crochet",
                        "url": "https://www.dickblick.com/categories/crafts/textile-arts/knitting-crochet/"
                    },
                    "looms": {
                        "name": "Looms",
                        "url": "https://www.dickblick.com/categories/crafts/textile-arts/looms/"
                    },
                    "macramé": {
                        "name": "Macramé",
                        "url": "https://www.dickblick.com/categories/crafts/textile-arts/macrame/"
                    },
                    "needle-felting": {
                        "name": "Needle Felting",
                        "url": "https://www.dickblick.com/categories/crafts/textile-arts/needle-felting/"
                    },
                    "needlepoint": {
                        "name": "Needlepoint",
                        "url": "https://www.dickblick.com/categories/crafts/textile-arts/needlepoint/"
                    },
                    "weaving": {
                        "name": "Weaving",
                        "url": "https://www.dickblick.com/categories/crafts/textile-arts/weaving/"
                    },
                    "yarn": {
                        "name": "Yarn",
                        "url": "https://www.dickblick.com/categories/crafts/textile-arts/yarn/"
                    }
                }
            },
            "home-decor": {
                "name": "Home Decor",
                "url": None,
                "children": {
                    "art-prints-and-posters": {
                        "name": "Art Prints and Posters",
                        "url": "https://www.dickblick.com/categories/crafts/home-decor/prints/"
                    },
                    "home-accents": {
                        "name": "Home Accents",
                        "url": "https://www.dickblick.com/categories/crafts/home-decor/accents/"
                    },
                    "jars-and-vases": {
                        "name": "Jars and Vases",
                        "url": "https://www.dickblick.com/categories/crafts/home-decor/jars-vases/"
                    },
                    "office-decor": {
                        "name": "Office Decor",
                        "url": "https://www.dickblick.com/categories/crafts/home-decor/office-decor/"
                    },
                    "seasonal-decor-and-crafts": {
                        "name": "Seasonal Decor and Crafts",
                        "url": "https://www.dickblick.com/categories/crafts/home-decor/seasonal/"
                    },
                    "unfinished-surfaces-to-decorate": {
                        "name": "Unfinished Surfaces to Decorate",
                        "url": "https://www.dickblick.com/categories/crafts/home-decor/unfinished-surfaces/"
                    },
                    "wall-decor": {
                        "name": "Wall Decor",
                        "url": "https://www.dickblick.com/categories/crafts/home-decor/wall-decor/"
                    }
                }
            },
            "kids-crafts": {
                "name": "Kids' Crafts",
                "url": "https://www.dickblick.com/categories/crafts/kids/",
                "children": {
                    "craft-beads": {
                        "name": "Craft Beads",
                        "url": "https://www.dickblick.com/categories/crafts/kids/craft-beads/"
                    },
                    "kids-craft-kits": {
                        "name": "Kids' Craft Kits",
                        "url": "https://www.dickblick.com/categories/crafts/kids/kits/"
                    },
                    "kids-scissors": {
                        "name": "Kids' Scissors",
                        "url": "https://www.dickblick.com/categories/crafts/kids/scissors/"
                    },
                    "kids-stickers": {
                        "name": "Kids' Stickers",
                        "url": "https://www.dickblick.com/categories/crafts/kids/stickers/"
                    },
                    "kids-unfinished-wood-shapes": {
                        "name": "Kids' Unfinished Wood Shapes",
                        "url": "https://www.dickblick.com/categories/crafts/kids/wood-shapes/"
                    },
                    "mask-making-supplies": {
                        "name": "Mask Making Supplies",
                        "url": "https://www.dickblick.com/categories/crafts/kids/mask-making/"
                    },
                    "slime-supplies": {
                        "name": "Slime Supplies",
                        "url": "https://www.dickblick.com/categories/crafts/kids/slime/"
                    }
                }
            },
            "leather-crafts": {
                "name": "Leather Crafts",
                "url": "https://www.dickblick.com/categories/crafts/leather-crafts/",
                "children": {
                    "leather": {
                        "name": "Leather",
                        "url": "https://www.dickblick.com/categories/crafts/leather-crafts/leather/"
                    },
                    "leather-care": {
                        "name": "Leather Care",
                        "url": "https://www.dickblick.com/categories/crafts/leather-crafts/leather-care/"
                    },
                    "leather-craft-tools": {
                        "name": "Leather Craft Tools",
                        "url": "https://www.dickblick.com/categories/crafts/leather-crafts/tools/"
                    },
                    "leather-jewelry-making": {
                        "name": "Leather Jewelry Making",
                        "url": "https://www.dickblick.com/categories/crafts/leather-crafts/jewelry-making/"
                    }
                }
            },
            "metal-crafts": {
                "name": "Metal Crafts",
                "url": "https://www.dickblick.com/categories/crafts/metal/",
                "children": {
                    "enameling": {
                        "name": "Enameling",
                        "url": "https://www.dickblick.com/categories/crafts/metal/enameling/"
                    },
                    "metal-punch-tools-and-kits": {
                        "name": "Metal Punch Tools and Kits",
                        "url": "https://www.dickblick.com/categories/crafts/metal/punch-tools/"
                    },
                    "metal-tooling-foil-and-embossing-tools": {
                        "name": "Metal Tooling Foil and Embossing Tools",
                        "url": "https://www.dickblick.com/categories/crafts/metal/embossing/"
                    }
                }
            },
            "model-and-miniature-supplies": {
                "name": "Model and Miniature Supplies",
                "url": "https://www.dickblick.com/categories/crafts/model-miniature/",
                "children": {
                    "scale-model-and-model-figures": {
                        "name": "Scale Model and Model Figures",
                        "url": "https://www.dickblick.com/categories/crafts/model-miniature/figures/"
                    }
                }
            },
            "mosaics": {
                "name": "Mosaics",
                "url": "https://www.dickblick.com/categories/crafts/mosaics/",
                "children": {
                    "mosaic-grout-and-cement": {
                        "name": "Mosaic Grout and Cement",
                        "url": "https://www.dickblick.com/categories/crafts/mosaics/grout/"
                    },
                    "mosaic-kits": {
                        "name": "Mosaic Kits",
                        "url": "https://www.dickblick.com/categories/crafts/mosaics/kits/"
                    },
                    "mosaic-tiles-and-stones": {
                        "name": "Mosaic Tiles and Stones",
                        "url": "https://www.dickblick.com/categories/crafts/mosaics/tiles/"
                    },
                    "mosaic-tools-and-accessories": {
                        "name": "Mosaic Tools and Accessories",
                        "url": "https://www.dickblick.com/categories/crafts/mosaics/tools/"
                    }
                }
            },
            "paper": {
                "name": "Paper",
                "url": None,
                "children": {
                    "paper-mache": {
                        "name": "Paper Mache",
                        "url": "https://www.dickblick.com/categories/crafts/paper/paper-mache/"
                    }
                }
            },
            "party-supplies": {
                "name": "Party Supplies",
                "url": "https://www.dickblick.com/categories/crafts/party-supplies/",
                "children": {
                    "gift-bags-and-gift-tags": {
                        "name": "Gift Bags and Gift Tags",
                        "url": "https://www.dickblick.com/categories/crafts/party-supplies/gift-bags/"
                    },
                    "party-decor": {
                        "name": "Party Decor",
                        "url": "https://www.dickblick.com/categories/crafts/party-supplies/paper-decor/"
                    }
                }
            },
            "sewing-supplies": {
                "name": "Sewing Supplies",
                "url": "https://www.dickblick.com/categories/crafts/sewing/",
                "children": {
                    "craft-and-textile-needles": {
                        "name": "Craft & Textile Needles",
                        "url": "https://www.dickblick.com/categories/crafts/sewing/needles/"
                    },
                    "sewing-kits": {
                        "name": "Sewing Kits",
                        "url": "https://www.dickblick.com/categories/crafts/sewing/kits/"
                    },
                    "sewing-machines-and-accessories": {
                        "name": "Sewing Machines and Accessories",
                        "url": "https://www.dickblick.com/categories/crafts/sewing/sewing-machines/"
                    },
                    "sewing-notions": {
                        "name": "Sewing Notions",
                        "url": "https://www.dickblick.com/categories/crafts/sewing/notions/"
                    },
                    "textile-measuring-tools": {
                        "name": "Textile Measuring Tools",
                        "url": "https://www.dickblick.com/categories/crafts/sewing/textile-tools/"
                    },
                    "thread-and-embroidery-floss": {
                        "name": "Thread and Embroidery Floss",
                        "url": "https://www.dickblick.com/categories/crafts/sewing/thread/"
                    }
                }
            },
            "sign-making": {
                "name": "Sign Making",
                "url": "https://www.dickblick.com/categories/crafts/sign-making/",
                "children": {
                    "banners-and-signs": {
                        "name": "Banners and Signs",
                        "url": "https://www.dickblick.com/categories/crafts/sign-making/banner/"
                    },
                    "easel-backs-and-sign-holders": {
                        "name": "Easel Backs and Sign Holders",
                        "url": "https://www.dickblick.com/categories/crafts/sign-making/easel-backs/"
                    },
                    "letter-stickers": {
                        "name": "Letter Stickers",
                        "url": "https://www.dickblick.com/categories/crafts/sign-making/letter-stickers/"
                    },
                    "plastic-sheets-and-panels": {
                        "name": "Plastic Sheets and Panels",
                        "url": "https://www.dickblick.com/categories/crafts/sign-making/plastic-sheets/"
                    }
                }
            },
            "soap-making": {
                "name": "Soap Making",
                "url": "https://www.dickblick.com/categories/crafts/soap-making/"
            },
            "wood-craft-supplies": {
                "name": "Wood Craft Supplies",
                "url": "https://www.dickblick.com/categories/crafts/wood/",
                "children": {
                    "clockmaking": {
                        "name": "Clockmaking",
                        "url": "https://www.dickblick.com/categories/crafts/wood/clockmaking/"
                    },
                    "sanders-and-sandpaper": {
                        "name": "Sanders and Sandpaper",
                        "url": "https://www.dickblick.com/categories/crafts/wood/sandpaper/"
                    },
                    "unfinished-wood-shapes": {
                        "name": "Unfinished Wood Shapes",
                        "url": "https://www.dickblick.com/categories/crafts/wood/shapes/"
                    },
                    "wood-blocks-and-boxes": {
                        "name": "Wood Blocks and Boxes",
                        "url": "https://www.dickblick.com/categories/crafts/wood/boxes/"
                    },
                    "wood-burning-tools-and-pens": {
                        "name": "Wood Burning Tools and Pens",
                        "url": "https://www.dickblick.com/categories/crafts/wood/wood-burning-tools/"
                    },
                    "wood-glue": {
                        "name": "Wood Glue",
                        "url": "https://www.dickblick.com/categories/crafts/wood/glue/"
                    },
                    "wood-planks-and-surfaces": {
                        "name": "Wood Planks and Surfaces",
                        "url": "https://www.dickblick.com/categories/crafts/wood/planks/"
                    },
                    "wood-project-kits": {
                        "name": "Wood Project Kits",
                        "url": "https://www.dickblick.com/categories/crafts/wood/kits/"
                    }
                }
            }
        }
    },
    "easels-and-art-furniture": {
        "name": "Easels and Art Furniture",
        "url": "https://www.dickblick.com/categories/furniture/",
        "children": {
            "art-display-furniture": {
                "name": "Art Display Furniture",
                "url": "https://www.dickblick.com/categories/furniture/display/",
                "children": {
                    "art-display-panels": {
                        "name": "Art Display Panels",
                        "url": "https://www.dickblick.com/categories/furniture/display/panels/"
                    },
                    "craft-show-display": {
                        "name": "Craft Show Display",
                        "url": "https://www.dickblick.com/categories/furniture/display/craft/"
                    },
                    "display-cases": {
                        "name": "Display Cases",
                        "url": "https://www.dickblick.com/categories/furniture/display/display-cases/"
                    },
                    "display-pedestals": {
                        "name": "Display Pedestals",
                        "url": "https://www.dickblick.com/categories/furniture/display/pedestals/"
                    },
                    "display-rails": {
                        "name": "Display Rails",
                        "url": "https://www.dickblick.com/categories/furniture/display/rails/"
                    }
                }
            },
            "art-studio-furniture": {
                "name": "Art Studio Furniture",
                "url": "https://www.dickblick.com/categories/furniture/art-studio/",
                "children": {
                    "art-storage-cabinets": {
                        "name": "Art Storage Cabinets",
                        "url": "https://www.dickblick.com/categories/furniture/art-studio/storage-cabinets/"
                    },
                    "art-tables-and-desks": {
                        "name": "Art Tables and Desks",
                        "url": "https://www.dickblick.com/categories/furniture/art-studio/tables/"
                    },
                    "artist-chairs-and-stools": {
                        "name": "Artist Chairs and Stools",
                        "url": "https://www.dickblick.com/categories/furniture/art-studio/chairs/"
                    },
                    "flat-files-and-vertical-files": {
                        "name": "Flat Files and Vertical Files",
                        "url": "https://www.dickblick.com/categories/furniture/art-studio/flat-files/"
                    },
                    "paper-drying-racks-and-storage": {
                        "name": "Paper Drying Racks and Storage",
                        "url": "https://www.dickblick.com/categories/furniture/art-studio/drying-racks/"
                    },
                    "print-racks": {
                        "name": "Print Racks",
                        "url": "https://www.dickblick.com/categories/furniture/art-studio/print-racks/"
                    },
                    "rolling-and-utility-carts": {
                        "name": "Rolling and Utility Carts",
                        "url": "https://www.dickblick.com/categories/furniture/art-studio/rolling-utility-carts/"
                    },
                    "room-dividers": {
                        "name": "Room Dividers",
                        "url": "https://www.dickblick.com/categories/furniture/art-studio/room-dividers/"
                    },
                    "taborets": {
                        "name": "Taborets",
                        "url": "https://www.dickblick.com/categories/furniture/art-studio/taborets/"
                    }
                }
            },
            "art-studio-lighting-and-lamps": {
                "name": "Art Studio Lighting and Lamps",
                "url": "https://www.dickblick.com/categories/furniture/lighting/",
                "children": {
                    "artist-lamps": {
                        "name": "Artist Lamps",
                        "url": "https://www.dickblick.com/categories/furniture/lighting/artist-lamps/"
                    },
                    "light-tables-and-light-boxes": {
                        "name": "Light Tables and Light Boxes",
                        "url": "https://www.dickblick.com/categories/furniture/lighting/light-tables/"
                    }
                }
            },
            "classroom-furniture": {
                "name": "Classroom Furniture",
                "url": "https://www.dickblick.com/categories/furniture/classroom/",
                "children": {
                    "chalkboards-and-dry-erase-boards": {
                        "name": "Chalkboards and Dry Erase Boards",
                        "url": "https://www.dickblick.com/categories/furniture/classroom/chalkboard-whiteboard/"
                    },
                    "classroom-chairs-and-stools": {
                        "name": "Classroom Chairs and  Stools",
                        "url": "https://www.dickblick.com/categories/furniture/classroom/chairs/"
                    },
                    "classroom-storage": {
                        "name": "Classroom Storage",
                        "url": "https://www.dickblick.com/categories/furniture/classroom/storage/"
                    },
                    "classroom-tables-and-desks": {
                        "name": "Classroom Tables and Desks",
                        "url": "https://www.dickblick.com/categories/furniture/classroom/tables/"
                    },
                    "display-and-bulletin-boards": {
                        "name": "Display and Bulletin Boards",
                        "url": "https://www.dickblick.com/categories/furniture/classroom/bulletin-boards/"
                    },
                    "early-childhood-furniture": {
                        "name": "Early Childhood Furniture",
                        "url": "https://www.dickblick.com/categories/furniture/classroom/early-childhood/"
                    },
                    "portable-hand-washing-stations": {
                        "name": "Portable Hand Washing Stations",
                        "url": "https://www.dickblick.com/categories/furniture/classroom/portable-hand-washing/"
                    }
                }
            },
            "furniture-accessories": {
                "name": "Furniture Accessories",
                "url": "https://www.dickblick.com/categories/furniture/accessories/"
            },
            "home-and-office-furniture": {
                "name": "Home and Office Furniture",
                "url": "https://www.dickblick.com/categories/furniture/home/",
                "children": {
                    "accent-furniture": {
                        "name": "Accent Furniture",
                        "url": "https://www.dickblick.com/categories/furniture/home/accent-furniture/"
                    },
                    "bookcases-and-shelving": {
                        "name": "Bookcases and Shelving",
                        "url": "https://www.dickblick.com/categories/furniture/home/bookcases/"
                    },
                    "home-and-office-storage-cabinets": {
                        "name": "Home and Office Storage Cabinets",
                        "url": "https://www.dickblick.com/categories/furniture/home/storage-cabinets/"
                    }
                }
            },
            "kids-easels-and-furniture": {
                "name": "Kids' Easels and Furniture",
                "url": "https://www.dickblick.com/categories/furniture/kids/",
                "children": {
                    "kids-furniture": {
                        "name": "Kids' Furniture",
                        "url": "https://www.dickblick.com/categories/furniture/kids/furniture/"
                    },
                    "kids-storage": {
                        "name": "Kids' Storage",
                        "url": "https://www.dickblick.com/categories/furniture/kids/storage/"
                    }
                }
            },
            "outdoor-studio-and-plein-air": {
                "name": "Outdoor Studio and Plein Air",
                "url": "https://www.dickblick.com/categories/furniture/outdoor-studio/",
                "children": {
                    "canopies-and-umbrellas": {
                        "name": "Canopies and Umbrellas",
                        "url": "https://www.dickblick.com/categories/furniture/outdoor-studio/canopies/"
                    },
                    "plein-air-accessories": {
                        "name": "Plein Air Accessories",
                        "url": "https://www.dickblick.com/categories/furniture/outdoor-studio/accessories/"
                    },
                    "plein-air-boards": {
                        "name": "Plein Air Boards",
                        "url": "https://www.dickblick.com/categories/furniture/outdoor-studio/plein-air-boards/"
                    }
                }
            },
            "projectors-and-accessories": {
                "name": "Projectors and Accessories",
                "url": "https://www.dickblick.com/categories/furniture/projectors/"
            },
            "retail-displays-and-fixtures": {
                "name": "Retail Displays and Fixtures",
                "url": "https://www.dickblick.com/categories/furniture/retail/"
            },
            "storage-carts-and-cabinets": {
                "name": "Storage Carts and Cabinets ",
                "url": "https://www.dickblick.com/categories/furniture/storage-carts-cabinets/"
            }
        }
    },
    "frames-and-framing-supplies": {
        "name": "Frames and Framing Supplies",
        "url": "https://www.dickblick.com/categories/framing/",
        "children": {
            "art-frames-by-popular-sizes": {
                "name": "Art Frames by Popular Sizes",
                "url": "https://www.dickblick.com/categories/framing/frames-by-size/",
                "children": {
                    "11-x-14-frames": {
                        "name": "11\" x 14\" Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-size/11x14-frames/"
                    },
                    "12-x-16-frames": {
                        "name": "12\" x 16\" Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-size/12x16-frames/"
                    },
                    "16-x-20-frames": {
                        "name": "16\" x 20\" Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-size/16x20-frames/"
                    },
                    "18-x-24-frames": {
                        "name": "18\" x 24\" Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-size/18x24-frames/"
                    },
                    "24-x-36-frames": {
                        "name": "24\" x 36\" Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-size/24x36-frames/"
                    },
                    "5-x-7-frames": {
                        "name": "5\" x 7\" Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-size/5x7-frames/"
                    },
                    "8-x-10-frames": {
                        "name": "8\" x 10\" Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-size/8x10-frames/"
                    },
                    "8-1-2-x-11-frames": {
                        "name": "8-1/2\" x 11\" Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-size/8-12x11-frames/"
                    },
                    "9-x-12-frames": {
                        "name": "9\" x 12\" Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-size/9x12-frames/"
                    },
                    "square-frames": {
                        "name": "Square Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-size/square-frames/"
                    }
                }
            },
            "art-frames-by-style": {
                "name": "Art Frames by Style",
                "url": "https://www.dickblick.com/categories/framing/frames-by-style/",
                "children": {
                    "modern-frames": {
                        "name": "Modern Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-style/modern-frames/"
                    },
                    "plein-air-frames": {
                        "name": "Plein Air Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-style/plein-air-frames/"
                    },
                    "rustic-frames": {
                        "name": "Rustic Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-style/rustic-frames/"
                    },
                    "traditional-frames": {
                        "name": "Traditional Frames",
                        "url": "https://www.dickblick.com/categories/framing/frames-by-style/traditional-frames/"
                    }
                }
            },
            "canvas-frames-and-floater-frames": {
                "name": "Canvas Frames and Floater Frames",
                "url": "https://www.dickblick.com/categories/framing/canvas-frames/"
            },
            "framing-tools-and-accessories": {
                "name": "Framing Tools and Accessories",
                "url": "https://www.dickblick.com/categories/framing/tools/",
                "children": {
                    "clamps-and-joiners": {
                        "name": "Clamps and Joiners",
                        "url": "https://www.dickblick.com/categories/framing/tools/clamps-joiners/"
                    },
                    "frame-glazing-materials-and-tools": {
                        "name": "Frame Glazing Materials and Tools",
                        "url": "https://www.dickblick.com/categories/framing/tools/glazing-materials/"
                    },
                    "framing-glue-and-adhesives": {
                        "name": "Framing Glue and Adhesives",
                        "url": "https://www.dickblick.com/categories/framing/tools/glue/"
                    },
                    "gold-leaf-and-metal-leaf": {
                        "name": "Gold Leaf and Metal Leaf",
                        "url": "https://www.dickblick.com/categories/framing/tools/gold-leaf/"
                    },
                    "mat-cutters": {
                        "name": "Mat Cutters",
                        "url": "https://www.dickblick.com/categories/framing/tools/mat-cutters/"
                    },
                    "mitre-boxes-and-mitre-saws": {
                        "name": "Mitre Boxes and Mitre Saws",
                        "url": "https://www.dickblick.com/categories/framing/tools/mitre-boxes/"
                    },
                    "picture-frame-backing": {
                        "name": "Picture Frame Backing",
                        "url": "https://www.dickblick.com/categories/framing/tools/picture-frame-backing/"
                    },
                    "point-drivers-and-framing-points": {
                        "name": "Point Drivers and Framing Points",
                        "url": "https://www.dickblick.com/categories/framing/tools/point-drivers/"
                    },
                    "wood-and-frame-touch-up": {
                        "name": "Wood and Frame Touch Up",
                        "url": "https://www.dickblick.com/categories/framing/tools/frame-touch-up/"
                    }
                }
            },
            "gallery-frames": {
                "name": "Gallery Frames",
                "url": "https://www.dickblick.com/categories/framing/gallery-frames/"
            },
            "matboard-and-mounting-board": {
                "name": "Matboard and Mounting Board",
                "url": "https://www.dickblick.com/categories/framing/boards/",
                "children": {
                    "matboard": {
                        "name": "Matboard",
                        "url": "https://www.dickblick.com/categories/framing/boards/matboard/"
                    },
                    "mounting-board": {
                        "name": "Mounting Board",
                        "url": "https://www.dickblick.com/categories/framing/boards/mounting-board/"
                    },
                    "mounting-systems": {
                        "name": "Mounting Systems",
                        "url": "https://www.dickblick.com/categories/framing/boards/mounting-systems/"
                    },
                    "pre-cut-mats": {
                        "name": "Pre-Cut Mats",
                        "url": "https://www.dickblick.com/categories/framing/boards/pre-cut-mats/"
                    }
                }
            },
            "metal-frames": {
                "name": "Metal Frames",
                "url": "https://www.dickblick.com/categories/framing/metal-frames/"
            },
            "picture-hanging-hardware": {
                "name": "Picture Hanging Hardware",
                "url": "https://www.dickblick.com/categories/framing/picture-hanging-supplies/"
            },
            "poster-frames": {
                "name": "Poster Frames",
                "url": "https://www.dickblick.com/categories/framing/poster-frames/"
            },
            "sectional-frame-kits": {
                "name": "Sectional Frame Kits",
                "url": "https://www.dickblick.com/categories/framing/sectional-kits/"
            },
            "shadow-boxes": {
                "name": "Shadow Boxes",
                "url": "https://www.dickblick.com/categories/framing/shadow-boxes/"
            },
            "tabletop-frames": {
                "name": "Tabletop Frames",
                "url": "https://www.dickblick.com/categories/framing/tabletop-frames/"
            },
            "wood-frames": {
                "name": "Wood Frames",
                "url": "https://www.dickblick.com/categories/framing/wood-frames/"
            }
        }
    },
    "gifts-for-artists": {
        "name": "Gifts for Artists",
        "url": "https://www.dickblick.com/categories/gifts/",
        "children": {
            "art-gifts-25-50": {
                "name": "Art Gifts $25-$50",
                "url": "https://www.dickblick.com/categories/gifts/25-50/"
            },
            "art-gifts-50-100": {
                "name": "Art Gifts $50-$100",
                "url": "https://www.dickblick.com/categories/gifts/50-100/"
            },
            "art-gifts-over-100": {
                "name": "Art Gifts Over $100",
                "url": "https://www.dickblick.com/categories/gifts/over-100/"
            },
            "art-gifts-under-25": {
                "name": "Art Gifts Under $25",
                "url": "https://www.dickblick.com/categories/gifts/under-25/"
            },
            "art-gifts-for-kids": {
                "name": "Art Gifts for Kids",
                "url": "https://www.dickblick.com/categories/gifts/kids/",
                "children": {
                    "kids-easels-and-furniture-gifts": {
                        "name": "Kids' Easels and Furniture Gifts",
                        "url": "https://www.dickblick.com/categories/gifts/kids/furniture/"
                    },
                    "kids-play-gifts": {
                        "name": "Kids' Play Gifts",
                        "url": "https://www.dickblick.com/categories/gifts/kids/play/"
                    }
                }
            },
            "classic-and-retro-gifts": {
                "name": "Classic and Retro Gifts",
                "url": "https://www.dickblick.com/categories/gifts/retro/"
            },
            "cute-and-kawaii-gifts": {
                "name": "Cute and Kawaii Gifts",
                "url": "https://www.dickblick.com/categories/gifts/kawaii/"
            },
            "drawing-gifts": {
                "name": "Drawing Gifts",
                "url": "https://www.dickblick.com/categories/gifts/drawing/"
            },
            "easel-and-studio-gifts": {
                "name": "Easel and Studio Gifts",
                "url": "https://www.dickblick.com/categories/gifts/furniture/"
            },
            "gift-wrapping-supplies": {
                "name": "Gift Wrapping Supplies",
                "url": "https://www.dickblick.com/categories/gifts/wrap/",
                "children": {
                    "decorative-ribbon-and-cord": {
                        "name": "Decorative Ribbon and Cord",
                        "url": "https://www.dickblick.com/categories/gifts/wrap/ribbon-tape/"
                    },
                    "decorative-scissors-and-punches": {
                        "name": "Decorative Scissors and Punches ",
                        "url": "https://www.dickblick.com/categories/gifts/wrap/scissors-punches/"
                    },
                    "gift-bag-and-basket-filler": {
                        "name": "Gift Bag and Basket Filler ",
                        "url": "https://www.dickblick.com/categories/gifts/wrap/bag-filler/"
                    },
                    "wrapping-paper": {
                        "name": "Wrapping Paper",
                        "url": "https://www.dickblick.com/categories/gifts/wrap/wrapping-paper/"
                    }
                }
            },
            "gifts-by-interests": {
                "name": "Gifts by Interests",
                "url": "https://www.dickblick.com/categories/gifts/interests/"
            },
            "gifts-for-animal-lovers": {
                "name": "Gifts for Animal Lovers",
                "url": "https://www.dickblick.com/categories/gifts/animals/"
            },
            "gifts-for-art-lovers": {
                "name": "Gifts for Art Lovers",
                "url": "https://www.dickblick.com/categories/gifts/famous-artists/"
            },
            "gifts-for-crafters": {
                "name": "Gifts for Crafters",
                "url": "https://www.dickblick.com/categories/gifts/crafts/",
                "children": {
                    "card-making": {
                        "name": "Card Making",
                        "url": "https://www.dickblick.com/categories/gifts/crafts/card-making/"
                    },
                    "craft-kit-gifts": {
                        "name": "Craft Kit Gifts",
                        "url": "https://www.dickblick.com/categories/gifts/crafts/kits/"
                    }
                }
            },
            "gifts-for-nature-lovers": {
                "name": "Gifts for Nature Lovers",
                "url": "https://www.dickblick.com/categories/gifts/plants-nature/"
            },
            "gifts-for-painters": {
                "name": "Gifts for Painters",
                "url": "https://www.dickblick.com/categories/gifts/painting/"
            },
            "gifts-for-potters": {
                "name": "Gifts for Potters",
                "url": "https://www.dickblick.com/categories/gifts/potters/"
            },
            "gifts-for-travelers": {
                "name": "Gifts for Travelers",
                "url": "https://www.dickblick.com/categories/gifts/travel/"
            },
            "printmaking-gifts": {
                "name": "Printmaking Gifts",
                "url": "https://www.dickblick.com/categories/gifts/printmaking/"
            },
            "self-care-gifts": {
                "name": "Self Care Gifts",
                "url": "https://www.dickblick.com/categories/gifts/wellness/"
            },
            "small-creative-gifts": {
                "name": "Small Creative Gifts",
                "url": "https://www.dickblick.com/categories/gifts/stocking-stuffers/"
            },
            "supernatural-and-space-gifts": {
                "name": "Supernatural and Space Gifts",
                "url": "https://www.dickblick.com/categories/gifts/celestial-space/"
            },
            "textile-art-gifts": {
                "name": "Textile Art Gifts",
                "url": "https://www.dickblick.com/categories/gifts/textile-art/"
            }
        }
    },
    "illustration-and-drawing-supplies": {
        "name": "Illustration and Drawing Supplies",
        "url": "https://www.dickblick.com/categories/drawing/",
        "children": {
            "art-markers": {
                "name": "Art Markers",
                "url": "https://www.dickblick.com/categories/drawing/markers/",
                "children": {
                    "alcohol-markers": {
                        "name": "Alcohol Markers",
                        "url": "https://www.dickblick.com/categories/drawing/markers/alcohol/"
                    },
                    "archival-markers-and-pens": {
                        "name": "Archival Markers and Pens",
                        "url": "https://www.dickblick.com/categories/drawing/markers/archival/"
                    },
                    "brush-markers-and-pens": {
                        "name": "Brush Markers and Pens",
                        "url": "https://www.dickblick.com/categories/drawing/markers/brush/"
                    },
                    "drawing-and-illustration-markers": {
                        "name": "Drawing and Illustration Markers",
                        "url": "https://www.dickblick.com/categories/drawing/markers/illustration/"
                    },
                    "dry-erase-markers": {
                        "name": "Dry-Erase Markers",
                        "url": "https://www.dickblick.com/categories/drawing/markers/whiteboard/"
                    },
                    "empty-markers-and-refills": {
                        "name": "Empty Markers and Refills",
                        "url": "https://www.dickblick.com/categories/drawing/markers/empty-refills/"
                    },
                    "fabric-markers": {
                        "name": "Fabric Markers",
                        "url": "https://www.dickblick.com/categories/drawing/markers/fabric/"
                    },
                    "highlighters": {
                        "name": "Highlighters",
                        "url": "https://www.dickblick.com/categories/drawing/markers/highlighters/"
                    },
                    "marker-organizers-and-storage": {
                        "name": "Marker Organizers and Storage",
                        "url": "https://www.dickblick.com/categories/drawing/markers/cases/"
                    },
                    "metallic-markers": {
                        "name": "Metallic Markers",
                        "url": "https://www.dickblick.com/categories/drawing/markers/metallic/"
                    },
                    "paint-pens-and-markers": {
                        "name": "Paint Pens and Markers",
                        "url": "https://www.dickblick.com/categories/drawing/markers/paint/"
                    },
                    "permanent-markers": {
                        "name": "Permanent Markers",
                        "url": "https://www.dickblick.com/categories/drawing/markers/permanent/"
                    },
                    "water-based-markers": {
                        "name": "Water-Based Markers",
                        "url": "https://www.dickblick.com/categories/drawing/markers/water-based/"
                    }
                }
            },
            "artist-inks": {
                "name": "Artist Inks",
                "url": "https://www.dickblick.com/categories/drawing/inks/",
                "children": {
                    "alcohol-inks-and-surfaces": {
                        "name": "Alcohol Inks and Surfaces",
                        "url": "https://www.dickblick.com/categories/drawing/inks/alcohol/"
                    },
                    "drawing-inks": {
                        "name": "Drawing Inks",
                        "url": "https://www.dickblick.com/categories/drawing/inks/drawing/"
                    },
                    "stamp-ink-and-pads": {
                        "name": "Stamp Ink and Pads",
                        "url": "https://www.dickblick.com/categories/drawing/inks/stamp-pads/"
                    }
                }
            },
            "calligraphy": {
                "name": "Calligraphy",
                "url": "https://www.dickblick.com/categories/drawing/calligraphy/",
                "children": {
                    "calligraphy-inks": {
                        "name": "Calligraphy Inks",
                        "url": "https://www.dickblick.com/categories/drawing/calligraphy/inks/"
                    },
                    "calligraphy-kits": {
                        "name": "Calligraphy Kits",
                        "url": "https://www.dickblick.com/categories/drawing/calligraphy/kits/"
                    },
                    "calligraphy-markers": {
                        "name": "Calligraphy Markers",
                        "url": "https://www.dickblick.com/categories/drawing/calligraphy/markers/"
                    },
                    "calligraphy-papers": {
                        "name": "Calligraphy Papers",
                        "url": "https://www.dickblick.com/categories/drawing/calligraphy/papers/"
                    },
                    "calligraphy-pens-and-refills": {
                        "name": "Calligraphy Pens and Refills",
                        "url": "https://www.dickblick.com/categories/drawing/calligraphy/pens/"
                    }
                }
            },
            "chalk": {
                "name": "Chalk",
                "url": "https://www.dickblick.com/categories/drawing/chalk/",
                "children": {
                    "chalk-markers-and-sprays": {
                        "name": "Chalk Markers and Sprays",
                        "url": "https://www.dickblick.com/categories/drawing/chalk/markers/"
                    },
                    "chalk-and-whiteboard-erasers": {
                        "name": "Chalk and Whiteboard Erasers",
                        "url": "https://www.dickblick.com/categories/drawing/chalk/erasers/"
                    },
                    "chalkboard-chalk": {
                        "name": "Chalkboard Chalk",
                        "url": "https://www.dickblick.com/categories/drawing/chalk/chalkboard/"
                    },
                    "drawing-and-sidewalk-chalk": {
                        "name": "Drawing and Sidewalk Chalk",
                        "url": "https://www.dickblick.com/categories/drawing/chalk/drawing/"
                    },
                    "pastel-chalk": {
                        "name": "Pastel Chalk",
                        "url": "https://www.dickblick.com/categories/drawing/chalk/pastel/"
                    }
                }
            },
            "colored-pencils": {
                "name": "Colored Pencils",
                "url": "https://www.dickblick.com/categories/drawing/colored-pencils/"
            },
            "crayons": {
                "name": "Crayons",
                "url": "https://www.dickblick.com/categories/drawing/crayons/",
                "children": {
                    "crayon-accessories": {
                        "name": "Crayon Accessories",
                        "url": "https://www.dickblick.com/categories/drawing/crayons/accessories/"
                    },
                    "water-soluble-crayons": {
                        "name": "Water Soluble Crayons",
                        "url": "https://www.dickblick.com/categories/drawing/crayons/water-soluble/"
                    },
                    "wax-based-crayons": {
                        "name": "Wax Based Crayons",
                        "url": "https://www.dickblick.com/categories/drawing/crayons/wax/"
                    }
                }
            },
            "digital-art": {
                "name": "Digital Art",
                "url": "https://www.dickblick.com/categories/drawing/digital-art/",
                "children": {
                    "digital-3d-printing": {
                        "name": "Digital 3D Printing",
                        "url": "https://www.dickblick.com/categories/drawing/digital-art/3d-printing/"
                    },
                    "graphics-tablets-and-styluses": {
                        "name": "Graphics Tablets and Styluses",
                        "url": "https://www.dickblick.com/categories/drawing/digital-art/tablets/"
                    },
                    "inkjet-paper-and-film": {
                        "name": "Inkjet Paper and Film",
                        "url": "https://www.dickblick.com/categories/drawing/digital-art/papers/"
                    }
                }
            },
            "drafting-supplies": {
                "name": "Drafting Supplies",
                "url": "https://www.dickblick.com/categories/drawing/drafting/",
                "children": {
                    "architectural-templates": {
                        "name": "Architectural Templates",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/templates/"
                    },
                    "artist-tape-and-drafting-tape": {
                        "name": "Artist Tape and Drafting Tape",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/tape/"
                    },
                    "color-guides": {
                        "name": "Color Guides  ",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/color-guides/"
                    },
                    "curves": {
                        "name": "Curves",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/curves/"
                    },
                    "drafting-paper-and-layout-paper": {
                        "name": "Drafting Paper and Layout Paper",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/papers/"
                    },
                    "drafting-scales": {
                        "name": "Drafting Scales",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/scales/"
                    },
                    "drawing-boards": {
                        "name": "Drawing Boards",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/boards/"
                    },
                    "drawing-compasses-and-dividers": {
                        "name": "Drawing Compasses and Dividers",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/compasses/"
                    },
                    "magnifiers": {
                        "name": "Magnifiers ",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/magnifiers/"
                    },
                    "parallel-rules-and-straightedges": {
                        "name": "Parallel Rules and Straightedges ",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/straightedges/"
                    },
                    "protractors-and-triangles": {
                        "name": "Protractors and Triangles",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/protractors/"
                    },
                    "rulers": {
                        "name": "Rulers",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/rulers/"
                    },
                    "scale-model-building-supplies": {
                        "name": "Scale Model Building Supplies",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/scale-model/"
                    },
                    "scale-model-scenery": {
                        "name": "Scale Model Scenery",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/scale-model-scenery/"
                    },
                    "t-squares-and-l-squares": {
                        "name": "T-Squares and L-Squares",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/t-squares/"
                    },
                    "technical-pens": {
                        "name": "Technical Pens",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/technical-pens/"
                    },
                    "tracing-paper": {
                        "name": "Tracing Paper",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/tracing-papers/"
                    },
                    "transfer-paper-and-films": {
                        "name": "Transfer Paper and Films",
                        "url": "https://www.dickblick.com/categories/drawing/drafting/transfer-papers/"
                    }
                }
            },
            "drawing-charcoal-and-graphite": {
                "name": "Drawing Charcoal and Graphite",
                "url": "https://www.dickblick.com/categories/drawing/charcoal/",
                "children": {
                    "charcoal-and-graphite-tools": {
                        "name": "Charcoal and Graphite Tools",
                        "url": "https://www.dickblick.com/categories/drawing/charcoal/tools/"
                    },
                    "compressed-charcoal": {
                        "name": "Compressed Charcoal",
                        "url": "https://www.dickblick.com/categories/drawing/charcoal/compressed/"
                    },
                    "graphite-sticks": {
                        "name": "Graphite Sticks",
                        "url": "https://www.dickblick.com/categories/drawing/charcoal/graphite-sticks/"
                    },
                    "graphite-and-charcoal-powder": {
                        "name": "Graphite and Charcoal Powder",
                        "url": "https://www.dickblick.com/categories/drawing/charcoal/powder/"
                    },
                    "vine-and-willow-charcoal": {
                        "name": "Vine and Willow Charcoal",
                        "url": "https://www.dickblick.com/categories/drawing/charcoal/vine/"
                    },
                    "watercolor-charcoal-and-graphite": {
                        "name": "Watercolor Charcoal and Graphite",
                        "url": "https://www.dickblick.com/categories/drawing/charcoal/watercolor/"
                    }
                }
            },
            "drawing-paper-and-boards": {
                "name": "Drawing Paper and Boards",
                "url": "https://www.dickblick.com/categories/drawing/paper/",
                "children": {
                    "art-and-illustration-boards": {
                        "name": "Art and Illustration Boards",
                        "url": "https://www.dickblick.com/categories/drawing/paper/art-boards/"
                    },
                    "bristol-paper-and-boards": {
                        "name": "Bristol Paper and Boards",
                        "url": "https://www.dickblick.com/categories/drawing/paper/bristol-boards/"
                    },
                    "cards-and-stationery": {
                        "name": "Cards and Stationery",
                        "url": "https://www.dickblick.com/categories/drawing/paper/cards/"
                    },
                    "charcoal-papers-and-pads": {
                        "name": "Charcoal Papers and Pads",
                        "url": "https://www.dickblick.com/categories/drawing/paper/charcoal-papers/"
                    },
                    "drawing-pads-and-sketch-pads": {
                        "name": "Drawing Pads and Sketch Pads",
                        "url": "https://www.dickblick.com/categories/drawing/paper/sketch-pads/"
                    },
                    "drawing-and-sketching-paper-rolls": {
                        "name": "Drawing and Sketching Paper Rolls",
                        "url": "https://www.dickblick.com/categories/drawing/paper/paper-rolls/"
                    },
                    "drawing-and-sketching-sheets": {
                        "name": "Drawing and Sketching Sheets",
                        "url": "https://www.dickblick.com/categories/drawing/paper/sketching-sheets/"
                    },
                    "journals-and-notebooks": {
                        "name": "Journals and Notebooks",
                        "url": "https://www.dickblick.com/categories/drawing/paper/journals/"
                    },
                    "mixed-media-paper-and-pads": {
                        "name": "Mixed Media Paper and Pads",
                        "url": "https://www.dickblick.com/categories/drawing/paper/mixed-media-papers/"
                    },
                    "newsprint-paper": {
                        "name": "Newsprint Paper",
                        "url": "https://www.dickblick.com/categories/drawing/paper/newsprint/"
                    },
                    "pastel-paper-and-boards": {
                        "name": "Pastel Paper and Boards",
                        "url": "https://www.dickblick.com/categories/drawing/paper/pastel-papers/"
                    },
                    "pen-and-marker-paper": {
                        "name": "Pen and Marker Paper",
                        "url": "https://www.dickblick.com/categories/drawing/paper/pen-marker-pads/"
                    },
                    "sketchbooks": {
                        "name": "Sketchbooks",
                        "url": "https://www.dickblick.com/categories/drawing/paper/sketchbooks/"
                    }
                }
            },
            "drawing-tools-and-accessories": {
                "name": "Drawing Tools and Accessories",
                "url": "https://www.dickblick.com/categories/drawing/tools/",
                "children": {
                    "art-manikins-and-anatomical-models": {
                        "name": "Art Manikins and Anatomical Models",
                        "url": "https://www.dickblick.com/categories/drawing/tools/manikins/"
                    },
                    "artist-s-hand-rests": {
                        "name": "Artist's Hand Rests",
                        "url": "https://www.dickblick.com/categories/drawing/tools/hand-rests/"
                    },
                    "drawing-fixatives": {
                        "name": "Drawing Fixatives",
                        "url": "https://www.dickblick.com/categories/drawing/tools/fixatives/"
                    },
                    "drawing-and-painting-reference-tools": {
                        "name": "Drawing and Painting Reference Tools",
                        "url": "https://www.dickblick.com/categories/drawing/tools/reference/"
                    },
                    "lettering-stencils-and-guides": {
                        "name": "Lettering Stencils and Guides",
                        "url": "https://www.dickblick.com/categories/drawing/tools/lettering-stencils/"
                    },
                    "stumps-and-tortillons": {
                        "name": "Stumps and Tortillons",
                        "url": "https://www.dickblick.com/categories/drawing/tools/stumps/"
                    }
                }
            },
            "erasers": {
                "name": "Erasers",
                "url": "https://www.dickblick.com/categories/drawing/erasers/",
                "children": {
                    "charcoal-and-pastel-erasers": {
                        "name": "Charcoal and Pastel Erasers",
                        "url": "https://www.dickblick.com/categories/drawing/erasers/charcoal/"
                    },
                    "pen-and-ink-erasers": {
                        "name": "Pen and Ink Erasers",
                        "url": "https://www.dickblick.com/categories/drawing/erasers/pen-ink/"
                    },
                    "pencil-and-graphite-erasers": {
                        "name": "Pencil and Graphite Erasers",
                        "url": "https://www.dickblick.com/categories/drawing/erasers/graphite/"
                    }
                }
            },
            "fine-writing-supplies": {
                "name": "Fine Writing Supplies",
                "url": "https://www.dickblick.com/categories/drawing/fine-writing/",
                "children": {
                    "fine-writing-ink-and-refills": {
                        "name": "Fine Writing Ink and Refills",
                        "url": "https://www.dickblick.com/categories/drawing/fine-writing/inks/"
                    },
                    "fine-writing-notebooks-and-planners": {
                        "name": "Fine Writing Notebooks and Planners",
                        "url": "https://www.dickblick.com/categories/drawing/fine-writing/notebooks/"
                    },
                    "fine-writing-pen-and-ink-accessories": {
                        "name": "Fine Writing Pen and Ink Accessories",
                        "url": "https://www.dickblick.com/categories/drawing/fine-writing/pen-ink-accessories/"
                    },
                    "fine-writing-pencils": {
                        "name": "Fine Writing Pencils",
                        "url": "https://www.dickblick.com/categories/drawing/fine-writing/pencils/"
                    },
                    "fine-writing-and-luxury-pens": {
                        "name": "Fine Writing and Luxury Pens",
                        "url": "https://www.dickblick.com/categories/drawing/fine-writing/pens/"
                    }
                }
            },
            "furniture": {
                "name": "Furniture",
                "url": None,
                "children": {
                    "drafting-tables": {
                        "name": "Drafting Tables",
                        "url": "https://www.dickblick.com/categories/drawing/furniture/drafting-tables/"
                    }
                }
            },
            "kids-drawing": {
                "name": "Kids' Drawing",
                "url": "https://www.dickblick.com/categories/drawing/kids/",
                "children": {
                    "kids-chalk": {
                        "name": "Kids' Chalk",
                        "url": "https://www.dickblick.com/categories/drawing/kids/chalk/"
                    },
                    "kids-colored-pencils": {
                        "name": "Kids' Colored Pencils",
                        "url": "https://www.dickblick.com/categories/drawing/kids/colored-pencils/"
                    },
                    "kids-crayons": {
                        "name": "Kids' Crayons ",
                        "url": "https://www.dickblick.com/categories/drawing/kids/crayons/"
                    },
                    "kids-drawing-and-sketch-pads": {
                        "name": "Kids' Drawing and Sketch Pads",
                        "url": "https://www.dickblick.com/categories/drawing/kids/sketch-pads/"
                    },
                    "kids-markers": {
                        "name": "Kids' Markers",
                        "url": "https://www.dickblick.com/categories/drawing/kids/markers/"
                    },
                    "kids-pencils": {
                        "name": "Kids' Pencils ",
                        "url": "https://www.dickblick.com/categories/drawing/kids/pencils/"
                    },
                    "kids-stencils-and-rubbing-plates": {
                        "name": "Kids' Stencils and Rubbing Plates",
                        "url": "https://www.dickblick.com/categories/drawing/kids/stencils/"
                    },
                    "kids-oil-pastels": {
                        "name": "Kids’ Oil Pastels",
                        "url": "https://www.dickblick.com/categories/drawing/kids/pastels/"
                    }
                }
            },
            "pastels": {
                "name": "Pastels",
                "url": "https://www.dickblick.com/categories/drawing/pastels/",
                "children": {
                    "medium-and-hard-pastels": {
                        "name": "Medium and Hard Pastels",
                        "url": "https://www.dickblick.com/categories/drawing/pastels/medium-hard/"
                    },
                    "oil-pastels": {
                        "name": "Oil Pastels",
                        "url": "https://www.dickblick.com/categories/drawing/pastels/oil/"
                    },
                    "pastel-primers-and-grounds": {
                        "name": "Pastel Primers and Grounds",
                        "url": "https://www.dickblick.com/categories/drawing/pastels/primers/"
                    },
                    "pastel-storage-boxes": {
                        "name": "Pastel Storage Boxes",
                        "url": "https://www.dickblick.com/categories/drawing/pastels/storage/"
                    },
                    "pastel-tools": {
                        "name": "Pastel Tools",
                        "url": "https://www.dickblick.com/categories/drawing/pastels/tools/"
                    },
                    "soft-pastels": {
                        "name": "Soft Pastels",
                        "url": "https://www.dickblick.com/categories/drawing/pastels/soft/"
                    }
                }
            },
            "pencils": {
                "name": "Pencils  ",
                "url": "https://www.dickblick.com/categories/drawing/pencils/",
                "children": {
                    "charcoal-pencils": {
                        "name": "Charcoal Pencils",
                        "url": "https://www.dickblick.com/categories/drawing/pencils/charcoal/"
                    },
                    "drawing-and-sketching-pencils": {
                        "name": "Drawing and Sketching Pencils",
                        "url": "https://www.dickblick.com/categories/drawing/pencils/sketching/"
                    },
                    "graphite-writing-pencils": {
                        "name": "Graphite Writing Pencils",
                        "url": "https://www.dickblick.com/categories/drawing/pencils/graphite/"
                    },
                    "graphite-and-charcoal-colored-pencils": {
                        "name": "Graphite and Charcoal Colored Pencils",
                        "url": "https://www.dickblick.com/categories/drawing/pencils/colored-graphite-charcoal/"
                    },
                    "mechanical-pencils-and-accessories": {
                        "name": "Mechanical Pencils and Accessories",
                        "url": "https://www.dickblick.com/categories/drawing/pencils/mechanical/"
                    },
                    "pastel-pencils": {
                        "name": "Pastel Pencils",
                        "url": "https://www.dickblick.com/categories/drawing/pencils/pastel/"
                    },
                    "pencil-holders": {
                        "name": "Pencil Holders",
                        "url": "https://www.dickblick.com/categories/drawing/pencils/holders/"
                    },
                    "pencil-sharpeners": {
                        "name": "Pencil Sharpeners",
                        "url": "https://www.dickblick.com/categories/drawing/pencils/sharpeners/"
                    },
                    "pencil-and-pen-cases": {
                        "name": "Pencil and Pen Cases",
                        "url": "https://www.dickblick.com/categories/drawing/pencils/cases/"
                    },
                    "photo-coloring": {
                        "name": "Photo Coloring ",
                        "url": "https://www.dickblick.com/categories/drawing/pencils/photo-coloring/"
                    },
                    "water-soluble-graphite-pencils": {
                        "name": "Water Soluble Graphite Pencils",
                        "url": "https://www.dickblick.com/categories/drawing/pencils/water-soluble/"
                    },
                    "watercolor-pencils": {
                        "name": "Watercolor Pencils",
                        "url": "https://www.dickblick.com/categories/drawing/pencils/watercolor/"
                    }
                }
            },
            "pens": {
                "name": "Pens",
                "url": "https://www.dickblick.com/categories/drawing/pens/",
                "children": {
                    "ballpoint-pens-and-refills": {
                        "name": "Ballpoint Pens and Refills",
                        "url": "https://www.dickblick.com/categories/drawing/pens/ballpoint/"
                    },
                    "dip-pens-and-nib-holders": {
                        "name": "Dip Pens and Nib Holders",
                        "url": "https://www.dickblick.com/categories/drawing/pens/dip-pens/"
                    },
                    "fiber-tip-and-flair-pens": {
                        "name": "Fiber Tip and Flair Pens",
                        "url": "https://www.dickblick.com/categories/drawing/pens/fiber-tip/"
                    },
                    "fineliner-pens": {
                        "name": "Fineliner Pens",
                        "url": "https://www.dickblick.com/categories/drawing/pens/fineliner/"
                    },
                    "fountain-pens": {
                        "name": "Fountain Pens",
                        "url": "https://www.dickblick.com/categories/drawing/pens/fountain-pens/"
                    },
                    "gel-pens-and-refills": {
                        "name": "Gel Pens and Refills",
                        "url": "https://www.dickblick.com/categories/drawing/pens/gel/"
                    },
                    "pen-cleaners": {
                        "name": "Pen Cleaners",
                        "url": "https://www.dickblick.com/categories/drawing/pens/cleaners/"
                    },
                    "rollerball-pens-and-refills": {
                        "name": "Rollerball Pens and Refills",
                        "url": "https://www.dickblick.com/categories/drawing/pens/rollerball/"
                    }
                }
            },
            "scratchboard-art": {
                "name": "Scratchboard Art",
                "url": "https://www.dickblick.com/categories/drawing/scratchboard/"
            },
            "sumi-e-painting": {
                "name": "Sumi-e Painting",
                "url": "https://www.dickblick.com/categories/drawing/sumi-painting/",
                "children": {
                    "calligraphy-and-sumi-brushes": {
                        "name": "Calligraphy and Sumi Brushes",
                        "url": "https://www.dickblick.com/categories/drawing/sumi-painting/brushes/"
                    },
                    "sumi-inks-and-accessories": {
                        "name": "Sumi Inks and Accessories",
                        "url": "https://www.dickblick.com/categories/drawing/sumi-painting/inks/"
                    },
                    "sumi-e-painting-paper": {
                        "name": "Sumi-e Painting Paper",
                        "url": "https://www.dickblick.com/categories/drawing/sumi-painting/papers/"
                    }
                }
            }
        }
    },
    "kids-art-supplies-and-more": {
        "name": "Kids’ Art Supplies and More",
        "url": "https://www.dickblick.com/categories/kids/",
        "children": {
            "at-home-learning-supplies": {
                "name": "At-Home Learning Supplies",
                "url": "https://www.dickblick.com/categories/kids/home-learning/",
                "children": {
                    "headphones-and-graphic-tablets": {
                        "name": "Headphones and Graphic Tablets",
                        "url": "https://www.dickblick.com/categories/kids/home-learning/tablets-headphones/"
                    }
                }
            },
            "classroom-packs": {
                "name": "Classroom Packs",
                "url": "https://www.dickblick.com/categories/kids/classroom-packs/",
                "children": {
                    "canvas-classroom-packs": {
                        "name": "Canvas Classroom Packs",
                        "url": "https://www.dickblick.com/categories/kids/classroom-packs/canvas/"
                    },
                    "ceramics-and-sculpture-classroom-packs": {
                        "name": "Ceramics and Sculpture Classroom Packs",
                        "url": "https://www.dickblick.com/categories/kids/classroom-packs/ceramics-sculpture/"
                    },
                    "classroom-craft-kits": {
                        "name": "Classroom Craft Kits",
                        "url": "https://www.dickblick.com/categories/kids/classroom-packs/craft-kits/"
                    },
                    "drawing-classroom-packs": {
                        "name": "Drawing Classroom Packs",
                        "url": "https://www.dickblick.com/categories/kids/classroom-packs/drawing/"
                    },
                    "glue-and-scissors-classroom-packs": {
                        "name": "Glue and Scissors Classroom Packs",
                        "url": "https://www.dickblick.com/categories/kids/classroom-packs/glue-scissors/"
                    },
                    "paint-brushes-and-painting-tools-classroom-packs": {
                        "name": "Paint Brushes and Painting Tools Classroom Packs",
                        "url": "https://www.dickblick.com/categories/kids/classroom-packs/paint-brushes/"
                    },
                    "paint-classroom-packs": {
                        "name": "Paint Classroom Packs",
                        "url": "https://www.dickblick.com/categories/kids/classroom-packs/paint/"
                    },
                    "paper-and-boards-classroom-packs": {
                        "name": "Paper and Boards Classroom Packs",
                        "url": "https://www.dickblick.com/categories/kids/classroom-packs/paper/"
                    }
                }
            },
            "kids-activity-kits": {
                "name": "Kids' Activity Kits",
                "url": "https://www.dickblick.com/categories/kids/kits/",
                "children": {
                    "kids-art-sets-and-kits": {
                        "name": "Kids' Art Sets and Kits",
                        "url": "https://www.dickblick.com/categories/kids/kits/art-sets/"
                    },
                    "kids-creative-learning-and-science-kits": {
                        "name": "Kids' Creative Learning and Science Kits",
                        "url": "https://www.dickblick.com/categories/kids/kits/creative-learning/"
                    }
                }
            },
            "kids-aprons-and-smocks": {
                "name": "Kids' Aprons and Smocks",
                "url": "https://www.dickblick.com/categories/kids/aprons/"
            },
            "kids-clay": {
                "name": "Kids' Clay",
                "url": "https://www.dickblick.com/categories/kids/clay/"
            },
            "kids-play": {
                "name": "Kids' Play",
                "url": "https://www.dickblick.com/categories/kids/play/",
                "children": {
                    "creative-toys": {
                        "name": "Creative Toys",
                        "url": "https://www.dickblick.com/categories/kids/play/toys/"
                    },
                    "games": {
                        "name": "Games",
                        "url": "https://www.dickblick.com/categories/kids/play/games/"
                    },
                    "outdoor-play": {
                        "name": "Outdoor Play",
                        "url": "https://www.dickblick.com/categories/kids/play/outdoor/"
                    },
                    "puzzles": {
                        "name": "Puzzles",
                        "url": "https://www.dickblick.com/categories/kids/play/puzzles/"
                    },
                    "tabletop-gaming-accessories": {
                        "name": "Tabletop Gaming Accessories",
                        "url": "https://www.dickblick.com/categories/kids/play/gaming-accessories/"
                    }
                }
            }
        }
    },
    "macpherson-overstock-liquidation-sale": {
        "name": "Macpherson Overstock Liquidation Sale",
        "url": None,
        "children": {
            "paints-liquidation": {
                "name": "Paints Liquidation",
                "url": None,
                "children": {
                    "painting-accessories-liquidation": {
                        "name": "Painting Accessories Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/paints-liquidation/painting-accessories-liquidation/"
                    }
                }
            },
            "popular-brands-liquidation": {
                "name": "Popular Brands Liquidation",
                "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/",
                "children": {
                    "art-alternatives-liquidation": {
                        "name": "Art Alternatives Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/art-alternatives-liquidation/"
                    },
                    "copic-liquidation": {
                        "name": "Copic Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/copic-liquidation/"
                    },
                    "cretacolor-liquidation": {
                        "name": "Cretacolor Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/cretacolor-liquidation/"
                    },
                    "derwent-liquidation": {
                        "name": "Derwent Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/derwent-liquidation/"
                    },
                    "fabriano-liquidation": {
                        "name": "Fabriano Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/fabriano-liquidation/"
                    },
                    "grumbacher-liquidation": {
                        "name": "Grumbacher Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/grumbacher-liquidation/"
                    },
                    "mabef-liquidation": {
                        "name": "Mabef Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/mabef-liquidation/"
                    },
                    "micador-liquidation": {
                        "name": "Micador Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/micador-liquidation/"
                    },
                    "montana-liquidation": {
                        "name": "Montana Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/montana-liquidation/"
                    },
                    "posca-liquidation": {
                        "name": "Posca Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/posca-liquidation/"
                    },
                    "sennelier-liquidation": {
                        "name": "Sennelier Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/sennelier-liquidation/"
                    },
                    "stabilo-liquidation": {
                        "name": "Stabilo Liquidation",
                        "url": "https://www.dickblick.com/categories/macpherson-overstock-liquidation-sale/popular-brands-liquidation/stabilo-liquidation/"
                    }
                }
            }
        }
    },
    "paint-and-mediums": {
        "name": "Paint and Mediums",
        "url": "https://www.dickblick.com/categories/painting/",
        "children": {
            "acrylic-paint": {
                "name": "Acrylic Paint",
                "url": "https://www.dickblick.com/categories/painting/acrylic-paint/"
            },
            "acrylics": {
                "name": "Acrylics",
                "url": None,
                "children": {
                    "acrylic-paint-sets": {
                        "name": "Acrylic Paint Sets",
                        "url": "https://www.dickblick.com/categories/painting/acrylics/paint-sets/"
                    }
                }
            },
            "airbrush-supplies": {
                "name": "Airbrush Supplies",
                "url": "https://www.dickblick.com/categories/painting/airbrushing/",
                "children": {
                    "airbrush-cleaning-and-maintenance": {
                        "name": "Airbrush Cleaning and Maintenance",
                        "url": "https://www.dickblick.com/categories/painting/airbrushing/cleaning/"
                    },
                    "airbrush-compressors-and-accessories": {
                        "name": "Airbrush Compressors and Accessories ",
                        "url": "https://www.dickblick.com/categories/painting/airbrushing/compressors/"
                    },
                    "airbrush-paint": {
                        "name": "Airbrush Paint",
                        "url": "https://www.dickblick.com/categories/painting/airbrushing/paint/"
                    },
                    "airbrush-paint-sets": {
                        "name": "Airbrush Paint Sets",
                        "url": "https://www.dickblick.com/categories/painting/airbrushing/sets/"
                    },
                    "airbrush-stencils-and-templates": {
                        "name": "Airbrush Stencils and Templates",
                        "url": "https://www.dickblick.com/categories/painting/airbrushing/stencils/"
                    },
                    "airbrushes-and-replacement-parts": {
                        "name": "Airbrushes and Replacement Parts",
                        "url": "https://www.dickblick.com/categories/painting/airbrushing/airbrushes/"
                    },
                    "frisket-film": {
                        "name": "Frisket Film",
                        "url": "https://www.dickblick.com/categories/painting/airbrushing/frisket-film/"
                    }
                }
            },
            "body-paint-and-makeup": {
                "name": "Body Paint and Makeup",
                "url": "https://www.dickblick.com/categories/painting/face-body/",
                "children": {
                    "face-paint-and-body-paint": {
                        "name": "Face Paint and Body Paint                                                          ",
                        "url": "https://www.dickblick.com/categories/painting/face-body/paint/"
                    },
                    "makeup": {
                        "name": "Makeup",
                        "url": "https://www.dickblick.com/categories/painting/face-body/makeup/"
                    }
                }
            },
            "cadmium-free-paints": {
                "name": "Cadmium Free Paints",
                "url": "https://www.dickblick.com/categories/painting/cadmium-free/"
            },
            "caseins-and-egg-tempera": {
                "name": "Caseins and Egg Tempera",
                "url": "https://www.dickblick.com/categories/painting/caseins/"
            },
            "encaustic-painting": {
                "name": "Encaustic Painting",
                "url": "https://www.dickblick.com/categories/painting/encaustic/",
                "children": {
                    "encaustic-paint": {
                        "name": "Encaustic Paint",
                        "url": "https://www.dickblick.com/categories/painting/encaustic/paint/"
                    },
                    "encaustic-paint-sets": {
                        "name": "Encaustic Paint Sets",
                        "url": "https://www.dickblick.com/categories/painting/encaustic/sets/"
                    },
                    "encaustic-painting-tools": {
                        "name": "Encaustic Painting Tools",
                        "url": "https://www.dickblick.com/categories/painting/encaustic/tools/"
                    }
                }
            },
            "fabric-painting-and-decorating": {
                "name": "Fabric Painting and Decorating",
                "url": "https://www.dickblick.com/categories/painting/fabric/",
                "children": {
                    "batik-supplies": {
                        "name": "Batik Supplies",
                        "url": "https://www.dickblick.com/categories/painting/fabric/batik/"
                    },
                    "blank-apparel-and-fabric-bases": {
                        "name": "Blank Apparel and Fabric Bases",
                        "url": "https://www.dickblick.com/categories/painting/fabric/blanks/"
                    },
                    "fabric-decorating-tools": {
                        "name": "Fabric Decorating Tools",
                        "url": "https://www.dickblick.com/categories/painting/fabric/tools/"
                    },
                    "fabric-dye-and-tie-dye-supplies": {
                        "name": "Fabric Dye and Tie-Dye Supplies",
                        "url": "https://www.dickblick.com/categories/painting/fabric/dye/"
                    },
                    "fabric-paint": {
                        "name": "Fabric Paint",
                        "url": "https://www.dickblick.com/categories/painting/fabric/paint/"
                    },
                    "fabrics-and-materials": {
                        "name": "Fabrics and Materials",
                        "url": "https://www.dickblick.com/categories/painting/fabric/materials/"
                    },
                    "iron-on-transfer-sheets-and-vinyl": {
                        "name": "Iron-On Transfer Sheets and Vinyl",
                        "url": "https://www.dickblick.com/categories/painting/fabric/iron-on-transfers/"
                    },
                    "silk-painting": {
                        "name": "Silk Painting",
                        "url": "https://www.dickblick.com/categories/painting/fabric/silk/"
                    }
                }
            },
            "gouache-paint-and-sets": {
                "name": "Gouache Paint and Sets",
                "url": "https://www.dickblick.com/categories/painting/gouache/",
                "children": {
                    "vinyl-paint": {
                        "name": "Vinyl Paint",
                        "url": "https://www.dickblick.com/categories/painting/gouache/vinyl-paint/"
                    }
                }
            },
            "home-decor-paint": {
                "name": "Home Decor Paint",
                "url": "https://www.dickblick.com/categories/painting/home-decor-paint/"
            },
            "kids-painting": {
                "name": "Kids' Painting",
                "url": "https://www.dickblick.com/categories/painting/kids/",
                "children": {
                    "finger-paint": {
                        "name": "Finger Paint",
                        "url": "https://www.dickblick.com/categories/painting/kids/finger-paint/"
                    },
                    "kids-acrylic-paint": {
                        "name": "Kids' Acrylic Paint",
                        "url": "https://www.dickblick.com/categories/painting/kids/acrylic-paint/"
                    },
                    "kids-face-paint": {
                        "name": "Kids' Face Paint",
                        "url": "https://www.dickblick.com/categories/painting/kids/face-paint/"
                    },
                    "kids-paint-sets": {
                        "name": "Kids' Paint Sets",
                        "url": "https://www.dickblick.com/categories/painting/kids/sets/"
                    },
                    "kids-watercolor-paint": {
                        "name": "Kids' Watercolor Paint",
                        "url": "https://www.dickblick.com/categories/painting/kids/watercolor/"
                    },
                    "kids-window-paint-and-markers": {
                        "name": "Kids' Window Paint and Markers",
                        "url": "https://www.dickblick.com/categories/painting/kids/window-paint/"
                    },
                    "kids-fabric-painting-and-decorating": {
                        "name": "Kids’ Fabric Painting and Decorating",
                        "url": "https://www.dickblick.com/categories/painting/kids/fabric-paint/"
                    }
                }
            },
            "mural-and-street-art-supplies": {
                "name": "Mural & Street Art Supplies ",
                "url": "https://www.dickblick.com/categories/painting/street-art/",
                "children": {
                    "mural-paint-and-supplies": {
                        "name": "Mural Paint and Supplies",
                        "url": "https://www.dickblick.com/categories/painting/street-art/mural-supplies/"
                    }
                }
            },
            "oil": {
                "name": "Oil",
                "url": None,
                "children": {
                    "oil-paint-sets": {
                        "name": "Oil Paint Sets",
                        "url": "https://www.dickblick.com/categories/painting/oil/paint-sets/"
                    }
                }
            },
            "oil-paint": {
                "name": "Oil Paint",
                "url": "https://www.dickblick.com/categories/painting/oil-paint/"
            },
            "paint-mediums-and-varnishes": {
                "name": "Paint Mediums and Varnishes",
                "url": "https://www.dickblick.com/categories/painting/mediums/",
                "children": {
                    "acrylic-mediums": {
                        "name": "Acrylic Mediums",
                        "url": "https://www.dickblick.com/categories/painting/mediums/acrylic/"
                    },
                    "airbrush-additives-and-mediums": {
                        "name": "Airbrush Additives and Mediums",
                        "url": "https://www.dickblick.com/categories/painting/mediums/airbrush/"
                    },
                    "dry-pigments": {
                        "name": "Dry Pigments",
                        "url": "https://www.dickblick.com/categories/painting/mediums/pigments/"
                    },
                    "encaustic-mediums": {
                        "name": "Encaustic Mediums",
                        "url": "https://www.dickblick.com/categories/painting/mediums/encaustic/"
                    },
                    "fabric-mediums": {
                        "name": "Fabric Mediums",
                        "url": "https://www.dickblick.com/categories/painting/mediums/fabric/"
                    },
                    "fluid-acrylics-and-pouring-mediums": {
                        "name": "Fluid Acrylics and Pouring Mediums",
                        "url": "https://www.dickblick.com/categories/painting/mediums/acrylic-pouring/"
                    },
                    "oil-painting-mediums": {
                        "name": "Oil Painting Mediums",
                        "url": "https://www.dickblick.com/categories/painting/mediums/oil/"
                    },
                    "oil-painting-solvents": {
                        "name": "Oil Painting Solvents",
                        "url": "https://www.dickblick.com/categories/painting/mediums/oil-solvents/"
                    },
                    "paint-varnishes": {
                        "name": "Paint Varnishes",
                        "url": "https://www.dickblick.com/categories/painting/mediums/varnish/"
                    },
                    "watercolor-mediums": {
                        "name": "Watercolor Mediums",
                        "url": "https://www.dickblick.com/categories/painting/mediums/watercolor/"
                    }
                }
            },
            "paint-palettes": {
                "name": "Paint Palettes",
                "url": "https://www.dickblick.com/categories/painting/palettes/"
            },
            "paint-sets": {
                "name": "Paint Sets",
                "url": "https://www.dickblick.com/categories/painting/sets/",
                "children": {
                    "paint-by-number-kits": {
                        "name": "Paint by Number Kits",
                        "url": "https://www.dickblick.com/categories/painting/sets/paint-by-number/"
                    }
                }
            },
            "painting-tools-and-accessories": {
                "name": "Painting Tools and Accessories",
                "url": "https://www.dickblick.com/categories/painting/tools/",
                "children": {
                    "applicator-bottles-and-dispensers": {
                        "name": "Applicator Bottles and Dispensers",
                        "url": "https://www.dickblick.com/categories/painting/tools/applicator-bottle/"
                    },
                    "color-wheels-and-swatch-tools": {
                        "name": "Color Wheels and Swatch Tools",
                        "url": "https://www.dickblick.com/categories/painting/tools/color-wheels/"
                    },
                    "drop-cloths-and-table-covers": {
                        "name": "Drop Cloths and Table Covers",
                        "url": "https://www.dickblick.com/categories/painting/tools/drop-cloth/"
                    },
                    "glass-ink-bottles-and-droppers": {
                        "name": "Glass Ink Bottles and Droppers",
                        "url": "https://www.dickblick.com/categories/painting/tools/glass-ink-bottles/"
                    },
                    "heat-guns": {
                        "name": "Heat Guns",
                        "url": "https://www.dickblick.com/categories/painting/tools/heat-guns/"
                    },
                    "kids-painting-tools": {
                        "name": "Kids' Painting Tools",
                        "url": "https://www.dickblick.com/categories/painting/tools/kids/"
                    },
                    "paint-containers-and-storage": {
                        "name": "Paint Containers and Storage",
                        "url": "https://www.dickblick.com/categories/painting/tools/paint-storage/"
                    },
                    "paint-making-tools": {
                        "name": "Paint Making Tools",
                        "url": "https://www.dickblick.com/categories/painting/tools/paint-making/"
                    },
                    "paint-pouring-and-resin-tools": {
                        "name": "Paint Pouring and Resin Tools ",
                        "url": "https://www.dickblick.com/categories/painting/tools/paint-pouring/"
                    },
                    "paint-rollers": {
                        "name": "Paint Rollers",
                        "url": "https://www.dickblick.com/categories/painting/tools/paint-rollers/"
                    },
                    "painting-and-palette-knives": {
                        "name": "Painting and Palette Knives",
                        "url": "https://www.dickblick.com/categories/painting/tools/palette-knives/"
                    },
                    "palette-cups-and-containers": {
                        "name": "Palette Cups and Containers",
                        "url": "https://www.dickblick.com/categories/painting/tools/palette-cups/"
                    },
                    "spray-booths-and-ventilation-systems": {
                        "name": "Spray Booths and Ventilation Systems",
                        "url": "https://www.dickblick.com/categories/painting/tools/spray-booths/"
                    },
                    "spray-bottles-and-atomizers": {
                        "name": "Spray Bottles and Atomizers",
                        "url": "https://www.dickblick.com/categories/painting/tools/spray-bottles/"
                    },
                    "tube-wringers": {
                        "name": "Tube Wringers",
                        "url": "https://www.dickblick.com/categories/painting/tools/tube-wringers/"
                    }
                }
            },
            "sign-painting-supplies": {
                "name": "Sign Painting Supplies",
                "url": "https://www.dickblick.com/categories/painting/sign-painting/",
                "children": {
                    "enamel-paints-and-mediums": {
                        "name": "Enamel Paints and Mediums",
                        "url": "https://www.dickblick.com/categories/painting/sign-painting/enamel-paint/"
                    },
                    "paint-thinners-and-reducers": {
                        "name": "Paint Thinners and Reducers",
                        "url": "https://www.dickblick.com/categories/painting/sign-painting/paint-thinners/"
                    },
                    "sign-painting-coatings-and-varnishes": {
                        "name": "Sign Painting Coatings and Varnishes",
                        "url": "https://www.dickblick.com/categories/painting/sign-painting/varnish/"
                    }
                }
            },
            "spray-paint-supplies": {
                "name": "Spray Paint Supplies",
                "url": "https://www.dickblick.com/categories/painting/spray-painting/",
                "children": {
                    "spray-paint": {
                        "name": "Spray Paint",
                        "url": "https://www.dickblick.com/categories/painting/spray-painting/paint/"
                    },
                    "spray-paint-cleaners-and-spray-caps": {
                        "name": "Spray Paint Cleaners and Spray Caps",
                        "url": "https://www.dickblick.com/categories/painting/spray-painting/tools/"
                    }
                }
            },
            "tempera-paint": {
                "name": "Tempera Paint",
                "url": "https://www.dickblick.com/categories/painting/tempera-paint/"
            },
            "watercolor": {
                "name": "Watercolor",
                "url": None,
                "children": {
                    "masking-fluids-and-liquid-friskets": {
                        "name": "Masking Fluids and Liquid Friskets",
                        "url": "https://www.dickblick.com/categories/painting/watercolor/masking-fluid/"
                    },
                    "watercolor-paint-sets": {
                        "name": "Watercolor Paint Sets",
                        "url": "https://www.dickblick.com/categories/painting/watercolor/paint-sets/"
                    }
                }
            },
            "watercolor-paint": {
                "name": "Watercolor Paint",
                "url": "https://www.dickblick.com/categories/painting/watercolor-paint/"
            }
        }
    },
    "printmaking-supplies": {
        "name": "Printmaking Supplies",
        "url": "https://www.dickblick.com/categories/printmaking/",
        "children": {
            "block-printing": {
                "name": "Block Printing",
                "url": "https://www.dickblick.com/categories/printmaking/block-printing/",
                "children": {
                    "block-printing-inks": {
                        "name": "Block Printing Inks",
                        "url": "https://www.dickblick.com/categories/printmaking/block-printing/inks/"
                    },
                    "block-printing-kits": {
                        "name": "Block Printing Kits",
                        "url": "https://www.dickblick.com/categories/printmaking/block-printing/kits/"
                    },
                    "block-printing-paper": {
                        "name": "Block Printing Paper",
                        "url": "https://www.dickblick.com/categories/printmaking/block-printing/paper/"
                    },
                    "block-printing-presses": {
                        "name": "Block Printing Presses",
                        "url": "https://www.dickblick.com/categories/printmaking/block-printing/presses/"
                    },
                    "brayers-and-barens": {
                        "name": "Brayers and Barens",
                        "url": "https://www.dickblick.com/categories/printmaking/block-printing/brayers/"
                    },
                    "inking-plates": {
                        "name": "Inking Plates",
                        "url": "https://www.dickblick.com/categories/printmaking/block-printing/plates/"
                    },
                    "linoleum-and-printing-blocks": {
                        "name": "Linoleum and Printing Blocks",
                        "url": "https://www.dickblick.com/categories/printmaking/block-printing/blocks/"
                    }
                }
            },
            "etching-and-intaglio": {
                "name": "Etching and Intaglio",
                "url": "https://www.dickblick.com/categories/printmaking/etching-intaglio/",
                "children": {
                    "etching-inks-and-intaglio-inks": {
                        "name": "Etching Inks and Intaglio Inks",
                        "url": "https://www.dickblick.com/categories/printmaking/etching-intaglio/inks/"
                    },
                    "etching-plates": {
                        "name": "Etching Plates",
                        "url": "https://www.dickblick.com/categories/printmaking/etching-intaglio/plates/"
                    },
                    "etching-presses-and-accessories": {
                        "name": "Etching Presses and Accessories",
                        "url": "https://www.dickblick.com/categories/printmaking/etching-intaglio/presses/"
                    },
                    "etching-and-intaglio-tools": {
                        "name": "Etching and Intaglio Tools",
                        "url": "https://www.dickblick.com/categories/printmaking/etching-intaglio/tools/"
                    }
                }
            },
            "lithography-supplies": {
                "name": "Lithography Supplies",
                "url": "https://www.dickblick.com/categories/printmaking/lithography/"
            },
            "monotype": {
                "name": "Monotype",
                "url": "https://www.dickblick.com/categories/printmaking/monotype/"
            },
            "printing-plates": {
                "name": "Printing Plates",
                "url": "https://www.dickblick.com/categories/printmaking/plates/",
                "children": {
                    "gel-printing-plates": {
                        "name": "Gel Printing Plates",
                        "url": "https://www.dickblick.com/categories/printmaking/plates/gel-printing/"
                    }
                }
            },
            "printing-presses": {
                "name": "Printing Presses",
                "url": "https://www.dickblick.com/categories/printmaking/presses/"
            },
            "printmaking-inks": {
                "name": "Printmaking Inks",
                "url": "https://www.dickblick.com/categories/printmaking/inks/",
                "children": {
                    "lithography-and-monotype-inks": {
                        "name": "Lithography and Monotype Inks",
                        "url": "https://www.dickblick.com/categories/printmaking/inks/lithography-monotype/"
                    }
                }
            },
            "printmaking-paper": {
                "name": "Printmaking Paper",
                "url": "https://www.dickblick.com/categories/printmaking/paper/",
                "children": {
                    "japanese-printmaking-paper": {
                        "name": "Japanese Printmaking Paper",
                        "url": "https://www.dickblick.com/categories/printmaking/paper/japanese/"
                    },
                    "professional-printmaking-paper": {
                        "name": "Professional Printmaking Paper",
                        "url": "https://www.dickblick.com/categories/printmaking/paper/professional/"
                    },
                    "student-printmaking-paper": {
                        "name": "Student Printmaking Paper",
                        "url": "https://www.dickblick.com/categories/printmaking/paper/student/"
                    }
                }
            },
            "printmaking-tools": {
                "name": "Printmaking Tools",
                "url": "https://www.dickblick.com/categories/printmaking/tools/",
                "children": {
                    "spatulas": {
                        "name": "Spatulas",
                        "url": "https://www.dickblick.com/categories/printmaking/tools/spatulas/"
                    },
                    "squeegees": {
                        "name": "Squeegees",
                        "url": "https://www.dickblick.com/categories/printmaking/tools/squeegees/"
                    }
                }
            },
            "screen-printing-supplies": {
                "name": "Screen Printing Supplies",
                "url": "https://www.dickblick.com/categories/printmaking/screen-printing/",
                "children": {
                    "screen-printing-chemicals": {
                        "name": "Screen Printing Chemicals",
                        "url": "https://www.dickblick.com/categories/printmaking/screen-printing/chemicals/"
                    },
                    "screen-printing-inks": {
                        "name": "Screen Printing Inks",
                        "url": "https://www.dickblick.com/categories/printmaking/screen-printing/inks/"
                    },
                    "screen-printing-kits": {
                        "name": "Screen Printing Kits",
                        "url": "https://www.dickblick.com/categories/printmaking/screen-printing/kits/"
                    },
                    "screen-printing-machines-and-equipment": {
                        "name": "Screen Printing Machines and Equipment ",
                        "url": "https://www.dickblick.com/categories/printmaking/screen-printing/machines/"
                    },
                    "screen-printing-screens-and-frames": {
                        "name": "Screen Printing Screens and Frames",
                        "url": "https://www.dickblick.com/categories/printmaking/screen-printing/frames-screens/"
                    },
                    "screen-printing-tools-and-accessories": {
                        "name": "Screen Printing Tools and Accessories",
                        "url": "https://www.dickblick.com/categories/printmaking/screen-printing/tools/"
                    }
                }
            },
            "sublimation-and-heat-printing": {
                "name": "Sublimation and Heat Printing",
                "url": "https://www.dickblick.com/categories/printmaking/sublimation/"
            },
            "sun-printing-and-cyanotype": {
                "name": "Sun Printing and Cyanotype",
                "url": "https://www.dickblick.com/categories/printmaking/cyanotype/"
            }
        }
    },
    "studio-and-office-supplies": {
        "name": "Studio and Office Supplies",
        "url": "https://www.dickblick.com/categories/studio/",
        "children": {
            "adaptive-art-supplies": {
                "name": "Adaptive Art Supplies",
                "url": "https://www.dickblick.com/categories/studio/adaptive-art-supplies/",
                "children": {
                    "adaptive-and-easy-grip-brushes": {
                        "name": "Adaptive and Easy-Grip Brushes",
                        "url": "https://www.dickblick.com/categories/studio/adaptive-art-supplies/brushes/"
                    },
                    "adaptive-and-easy-grip-drawing-tools": {
                        "name": "Adaptive and Easy-Grip Drawing Tools",
                        "url": "https://www.dickblick.com/categories/studio/adaptive-art-supplies/drawing/"
                    },
                    "art-furniture-for-wheelchair-access": {
                        "name": "Art Furniture for Wheelchair Access",
                        "url": "https://www.dickblick.com/categories/studio/adaptive-art-supplies/furniture/"
                    }
                }
            },
            "archival-supplies": {
                "name": "Archival Supplies",
                "url": "https://www.dickblick.com/categories/studio/archival/",
                "children": {
                    "archival-boxes": {
                        "name": "Archival Boxes",
                        "url": "https://www.dickblick.com/categories/studio/archival/storage-boxes/"
                    },
                    "plastic-sleeves-and-print-protectors": {
                        "name": "Plastic Sleeves and Print Protectors",
                        "url": "https://www.dickblick.com/categories/studio/archival/print-protectors/"
                    },
                    "shrink-wrap-and-film": {
                        "name": "Shrink Wrap and Film",
                        "url": "https://www.dickblick.com/categories/studio/archival/shrink-wrap/"
                    }
                }
            },
            "art-safety-supplies-and-protective-gear": {
                "name": "Art Safety Supplies and Protective Gear",
                "url": "https://www.dickblick.com/categories/studio/safety/",
                "children": {
                    "air-purifiers": {
                        "name": "Air Purifiers",
                        "url": "https://www.dickblick.com/categories/studio/safety/air-purifiers/"
                    },
                    "face-masks-and-respirators": {
                        "name": "Face Masks and Respirators",
                        "url": "https://www.dickblick.com/categories/studio/safety/respirators/"
                    },
                    "flammable-cabinets-and-safety-cans": {
                        "name": "Flammable Cabinets and Safety Cans",
                        "url": "https://www.dickblick.com/categories/studio/safety/cabinets-cans/"
                    },
                    "heat-resistant-gloves": {
                        "name": "Heat Resistant Gloves",
                        "url": "https://www.dickblick.com/categories/studio/safety/gloves/"
                    }
                }
            },
            "art-storage-and-organization": {
                "name": "Art Storage and Organization",
                "url": "https://www.dickblick.com/categories/studio/art-storage/",
                "children": {
                    "art-portfolios": {
                        "name": "Art Portfolios",
                        "url": "https://www.dickblick.com/categories/studio/art-storage/portfolios/"
                    },
                    "desk-organizers-and-accessories": {
                        "name": "Desk Organizers and Accessories",
                        "url": "https://www.dickblick.com/categories/studio/art-storage/desk-organizers/"
                    },
                    "paper-racks-and-dispensers": {
                        "name": "Paper Racks and Dispensers",
                        "url": "https://www.dickblick.com/categories/studio/art-storage/paper-dispensers/"
                    },
                    "presentation-books-and-portfolio-binders": {
                        "name": "Presentation Books and Portfolio Binders",
                        "url": "https://www.dickblick.com/categories/studio/art-storage/binders/"
                    },
                    "storage-bins-and-trays": {
                        "name": "Storage Bins and Trays",
                        "url": "https://www.dickblick.com/categories/studio/art-storage/bins/"
                    },
                    "storage-boxes-and-containers": {
                        "name": "Storage Boxes and Containers",
                        "url": "https://www.dickblick.com/categories/studio/art-storage/boxes/"
                    }
                }
            },
            "cleaning-supplies-and-materials": {
                "name": "Cleaning Supplies and Materials",
                "url": "https://www.dickblick.com/categories/studio/cleaning/",
                "children": {
                    "adhesive-removers": {
                        "name": "Adhesive Removers",
                        "url": "https://www.dickblick.com/categories/studio/cleaning/adhesive-removers/"
                    },
                    "art-aprons-and-smocks": {
                        "name": "Art Aprons and Smocks",
                        "url": "https://www.dickblick.com/categories/studio/cleaning/aprons-smocks/"
                    },
                    "cleaning-solvents-and-stain-removers": {
                        "name": "Cleaning Solvents and Stain Removers",
                        "url": "https://www.dickblick.com/categories/studio/cleaning/stain-removers/"
                    },
                    "disposable-gloves-and-barrier-cream": {
                        "name": "Disposable Gloves and Barrier Cream",
                        "url": "https://www.dickblick.com/categories/studio/cleaning/gloves/"
                    },
                    "surface-cleaning-supplies": {
                        "name": "Surface Cleaning Supplies",
                        "url": "https://www.dickblick.com/categories/studio/cleaning/surface-cleaners/"
                    }
                }
            },
            "cutting-tools": {
                "name": "Cutting Tools",
                "url": "https://www.dickblick.com/categories/studio/cutting-tools/",
                "children": {
                    "art-knives-and-blades": {
                        "name": "Art Knives and Blades",
                        "url": "https://www.dickblick.com/categories/studio/cutting-tools/art-knives/"
                    },
                    "cutting-mats": {
                        "name": "Cutting Mats",
                        "url": "https://www.dickblick.com/categories/studio/cutting-tools/cutting-mats/"
                    },
                    "engraving-tools": {
                        "name": "Engraving Tools",
                        "url": "https://www.dickblick.com/categories/studio/cutting-tools/engraving/"
                    },
                    "foam-cutters": {
                        "name": "Foam Cutters",
                        "url": "https://www.dickblick.com/categories/studio/cutting-tools/foam-board/"
                    },
                    "linoleum-cutters-and-accessories": {
                        "name": "Linoleum Cutters and Accessories",
                        "url": "https://www.dickblick.com/categories/studio/cutting-tools/linoleum-cutters/"
                    },
                    "paper-cutters-and-trimmers": {
                        "name": "Paper Cutters and Trimmers ",
                        "url": "https://www.dickblick.com/categories/studio/cutting-tools/paper-cutters/"
                    },
                    "paper-punches-and-awls": {
                        "name": "Paper Punches and Awls",
                        "url": "https://www.dickblick.com/categories/studio/cutting-tools/paper-punches/"
                    },
                    "scissors-and-shears": {
                        "name": "Scissors and Shears",
                        "url": "https://www.dickblick.com/categories/studio/cutting-tools/scissors/"
                    },
                    "sharpening-tools": {
                        "name": "Sharpening Tools",
                        "url": "https://www.dickblick.com/categories/studio/cutting-tools/sharpening-tools/"
                    },
                    "utility-cutters": {
                        "name": "Utility Cutters",
                        "url": "https://www.dickblick.com/categories/studio/cutting-tools/utility-cutters/"
                    }
                }
            },
            "glue": {
                "name": "Glue",
                "url": "https://www.dickblick.com/categories/studio/glue/",
                "children": {
                    "adhesive-spray": {
                        "name": "Adhesive Spray",
                        "url": "https://www.dickblick.com/categories/studio/glue/adhesive-spray/"
                    },
                    "art-paste-and-wheat-paste": {
                        "name": "Art Paste and Wheat Paste",
                        "url": "https://www.dickblick.com/categories/studio/glue/wheat-paste/"
                    },
                    "epoxy-glue": {
                        "name": "Epoxy Glue",
                        "url": "https://www.dickblick.com/categories/studio/glue/epoxy/"
                    },
                    "glue-guns-and-hot-glue-sticks": {
                        "name": "Glue Guns and Hot Glue Sticks",
                        "url": "https://www.dickblick.com/categories/studio/glue/glue-guns/"
                    },
                    "glue-pens-and-applicators": {
                        "name": "Glue Pens and Applicators",
                        "url": "https://www.dickblick.com/categories/studio/glue/pens/"
                    },
                    "glue-sticks": {
                        "name": "Glue Sticks",
                        "url": "https://www.dickblick.com/categories/studio/glue/sticks/"
                    },
                    "heavy-duty-glue-and-multi-surface-glue": {
                        "name": "Heavy-Duty Glue and Multi-Surface Glue",
                        "url": "https://www.dickblick.com/categories/studio/glue/heavy-duty/"
                    },
                    "kids-glue": {
                        "name": "Kids' Glue",
                        "url": "https://www.dickblick.com/categories/studio/glue/kids/"
                    },
                    "model-and-miniature-glue": {
                        "name": "Model and Miniature Glue",
                        "url": "https://www.dickblick.com/categories/studio/glue/model-miniature/"
                    },
                    "pva-glue": {
                        "name": "PVA Glue",
                        "url": "https://www.dickblick.com/categories/studio/glue/pva/"
                    },
                    "plastic-and-rubber-cement": {
                        "name": "Plastic and Rubber Cement",
                        "url": "https://www.dickblick.com/categories/studio/glue/rubber-cement/"
                    },
                    "super-glue": {
                        "name": "Super Glue",
                        "url": "https://www.dickblick.com/categories/studio/glue/super/"
                    },
                    "tacky-glue": {
                        "name": "Tacky Glue",
                        "url": "https://www.dickblick.com/categories/studio/glue/tacky/"
                    },
                    "white-glue": {
                        "name": "White Glue",
                        "url": "https://www.dickblick.com/categories/studio/glue/white/"
                    }
                }
            },
            "hardware": {
                "name": "Hardware",
                "url": "https://www.dickblick.com/categories/studio/hardware/",
                "children": {
                    "fasteners-and-fastening-tools": {
                        "name": "Fasteners and Fastening Tools",
                        "url": "https://www.dickblick.com/categories/studio/hardware/fasteners/"
                    },
                    "hand-tools": {
                        "name": "Hand Tools",
                        "url": "https://www.dickblick.com/categories/studio/hardware/hand-tools/"
                    },
                    "heavy-duty-cutting-tools": {
                        "name": "Heavy Duty Cutting Tools",
                        "url": "https://www.dickblick.com/categories/studio/hardware/heavy-duty-cutters/"
                    },
                    "power-tools": {
                        "name": "Power Tools",
                        "url": "https://www.dickblick.com/categories/studio/hardware/power-tools/"
                    },
                    "safety-gear-and-first-aid": {
                        "name": "Safety Gear and First Aid",
                        "url": "https://www.dickblick.com/categories/studio/hardware/safety-gear/"
                    },
                    "wood-working-tools": {
                        "name": "Wood Working Tools",
                        "url": "https://www.dickblick.com/categories/studio/hardware/wood-working-tools/"
                    }
                }
            },
            "office-supplies": {
                "name": "Office Supplies",
                "url": "https://www.dickblick.com/categories/studio/office-supplies/",
                "children": {
                    "clips-and-binder-rings": {
                        "name": "Clips and Binder Rings",
                        "url": "https://www.dickblick.com/categories/studio/office-supplies/clips/"
                    },
                    "hook-and-loop-fasteners": {
                        "name": "Hook and Loop Fasteners",
                        "url": "https://www.dickblick.com/categories/studio/office-supplies/hook-loop-fasteners/"
                    },
                    "labels-and-label-makers": {
                        "name": "Labels and Label Makers",
                        "url": "https://www.dickblick.com/categories/studio/office-supplies/label-makers/"
                    },
                    "laminators-and-films": {
                        "name": "Laminators and Films",
                        "url": "https://www.dickblick.com/categories/studio/office-supplies/laminators/"
                    },
                    "magnets-and-magnetic-sheets": {
                        "name": "Magnets and Magnetic Sheets",
                        "url": "https://www.dickblick.com/categories/studio/office-supplies/magnets/"
                    },
                    "packing-and-shipping-supplies": {
                        "name": "Packing and Shipping Supplies ",
                        "url": "https://www.dickblick.com/categories/studio/office-supplies/packing-shipping/"
                    },
                    "planners-and-calendars": {
                        "name": "Planners and Calendars",
                        "url": "https://www.dickblick.com/categories/studio/office-supplies/planners-calendars/"
                    },
                    "rubber-bands-and-elastic": {
                        "name": "Rubber Bands and Elastic",
                        "url": "https://www.dickblick.com/categories/studio/office-supplies/rubber-bands/"
                    },
                    "staplers-and-staple-guns": {
                        "name": "Staplers and Staple Guns",
                        "url": "https://www.dickblick.com/categories/studio/office-supplies/staplers/"
                    },
                    "thumb-tacks-and-pushpins": {
                        "name": "Thumb Tacks and Pushpins",
                        "url": "https://www.dickblick.com/categories/studio/office-supplies/pins/"
                    }
                }
            },
            "photography": {
                "name": "Photography",
                "url": "https://www.dickblick.com/categories/studio/photography/",
                "children": {
                    "photo-albums-and-scrapbook-albums": {
                        "name": "Photo Albums and Scrapbook Albums",
                        "url": "https://www.dickblick.com/categories/studio/photography/photo-albums/"
                    },
                    "photography-backdrops": {
                        "name": "Photography Backdrops",
                        "url": "https://www.dickblick.com/categories/studio/photography/backdrops/"
                    },
                    "photography-studio-lighting-and-equipment": {
                        "name": "Photography Studio Lighting and Equipment",
                        "url": "https://www.dickblick.com/categories/studio/photography/lighting-equipment/"
                    }
                }
            },
            "tape": {
                "name": "Tape",
                "url": "https://www.dickblick.com/categories/studio/tape/",
                "children": {
                    "adhesive-sheets": {
                        "name": "Adhesive Sheets",
                        "url": "https://www.dickblick.com/categories/studio/tape/adhesive-sheets/"
                    },
                    "archival-tape-and-adhesives": {
                        "name": "Archival Tape and Adhesives",
                        "url": "https://www.dickblick.com/categories/studio/tape/archival/"
                    },
                    "bookbinding-tape-and-book-repair-tape": {
                        "name": "Bookbinding Tape and Book Repair Tape",
                        "url": "https://www.dickblick.com/categories/studio/tape/bookbinding/"
                    },
                    "clear-tape": {
                        "name": "Clear Tape",
                        "url": "https://www.dickblick.com/categories/studio/tape/clear/"
                    },
                    "craft-and-decorative-tape": {
                        "name": "Craft and Decorative Tape",
                        "url": "https://www.dickblick.com/categories/studio/tape/decorative/"
                    },
                    "double-sided-tape": {
                        "name": "Double-Sided Tape",
                        "url": "https://www.dickblick.com/categories/studio/tape/double-sided/"
                    },
                    "gummed-tape": {
                        "name": "Gummed Tape",
                        "url": "https://www.dickblick.com/categories/studio/tape/gummed/"
                    },
                    "heavy-duty-tape": {
                        "name": "Heavy-Duty Tape",
                        "url": "https://www.dickblick.com/categories/studio/tape/heavy-duty/"
                    },
                    "masking-tape": {
                        "name": "Masking Tape",
                        "url": "https://www.dickblick.com/categories/studio/tape/masking-tape/"
                    },
                    "mounting-squares-and-adhesive-dots": {
                        "name": "Mounting Squares and Adhesive Dots",
                        "url": "https://www.dickblick.com/categories/studio/tape/mounting-squares/"
                    },
                    "screen-printing-tape": {
                        "name": "Screen Printing Tape",
                        "url": "https://www.dickblick.com/categories/studio/tape/screen-printing/"
                    },
                    "tape-dispensers": {
                        "name": "Tape Dispensers",
                        "url": "https://www.dickblick.com/categories/studio/tape/dispensers/"
                    },
                    "watercolor-tape": {
                        "name": "Watercolor Tape",
                        "url": "https://www.dickblick.com/categories/studio/tape/watercolor-tape/"
                    }
                }
            },
            "transporting-and-carrying-art-supplies": {
                "name": "Transporting and Carrying Art Supplies",
                "url": "https://www.dickblick.com/categories/studio/art-transport/",
                "children": {
                    "art-and-poster-tubes": {
                        "name": "Art and Poster Tubes",
                        "url": "https://www.dickblick.com/categories/studio/art-transport/poster-tubes/"
                    },
                    "bags-and-carrying-cases": {
                        "name": "Bags and Carrying Cases",
                        "url": "https://www.dickblick.com/categories/studio/art-transport/totes/"
                    }
                }
            }
        }
    },
    "tattoo-supplies": {
        "name": "Tattoo Supplies",
        "url": "https://www.dickblick.com/categories/tattoo/",
        "children": {
            "tattoo-furniture": {
                "name": "Tattoo Furniture",
                "url": "https://www.dickblick.com/categories/tattoo/furniture/"
            },
            "tattoo-inks-and-accessories": {
                "name": "Tattoo Inks and Accessories",
                "url": "https://www.dickblick.com/categories/tattoo/inks/"
            },
            "tattoo-machines-and-accessories": {
                "name": "Tattoo Machines and Accessories",
                "url": "https://www.dickblick.com/categories/tattoo/machines/"
            },
            "tattoo-medical-supplies": {
                "name": "Tattoo Medical Supplies",
                "url": "https://www.dickblick.com/categories/tattoo/medical/"
            },
            "tattoo-needle-cartridges": {
                "name": "Tattoo Needle Cartridges",
                "url": "https://www.dickblick.com/categories/tattoo/needles/"
            },
            "tattoo-stencil-and-studio-tools": {
                "name": "Tattoo Stencil and Studio Tools ",
                "url": "https://www.dickblick.com/categories/tattoo/stencil-studio/"
            }
        }
    }
}


def _iter_nodes(node: dict):
    """Yield every node in the tree, depth-first."""
    yield node
    for child in (node.get("children") or {}).values():
        yield from _iter_nodes(child)


def _slugify(value: str) -> str:
    out = []
    for ch in value.lower().replace("’", "").replace("&", " and "):
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-")


def flatten_categories(tree: dict[str, dict] | None = None) -> list[dict]:
    """Flatten the tree into deterministic ``{category, name, url, path, depth}`` rows.

    ``category`` is a slug-safe ``department/group/leaf`` path, so ``-a
    category=`` stays unambiguous even when two leaves under different parents
    share a display name. ``path`` keeps the human-readable names.

    Group nodes with ``url=None`` are path-derived containers rather than
    crawlable landing pages; the spider skips them.
    """
    tree = tree if tree is not None else BLICK_CATEGORY_TREE
    rows: list[dict] = []

    def _walk(node: dict, slugs: list[str], names: list[str], depth: int):
        name = (node.get("name") or "").strip()
        rows.append(
            {
                "category": "/".join(slugs + ([_slugify(name)] if name else [])),
                "name": name,
                "url": node.get("url"),
                "path": " > ".join(names + [name] if name else names),
                "depth": depth,
            }
        )
        for child in (node.get("children") or {}).values():
            _walk(
                child,
                slugs + ([_slugify(name)] if name else []),
                names + [name],
                depth + 1,
            )

    for key in sorted(tree):
        _walk(tree[key], [], [], 1)
    return rows


def crawlable_categories(tree: dict[str, dict] | None = None) -> list[dict]:
    """Return only the rows that map to a crawlable category landing page."""
    return [row for row in flatten_categories(tree) if row["url"]]
