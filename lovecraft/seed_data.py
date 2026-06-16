"""Curated seed content for the Lovecraft bestiary.

Sizes and weights are deliberately rough and often ``None`` — many cosmic
entities have no canonical dimensions ("a mountain walked", "coextensive with
all reality"). ``size_note`` captures the prose qualifier in those cases.

Extend these two lists to grow the encyclopedia; ``database.ensure_database``
rebuilds the tables from them.
"""

# (name, classification, description, height_m, weight_kg, size_note)
ENTITIES = [
    (
        "Cthulhu",
        "Great Old One",
        "A vast octopoid-dragon hybrid priest of the Old Ones, lying dead-but-dreaming "
        "in the sunken city of R'lyeh until the stars are right.",
        150.0,
        None,
        "Mountainous — 'a mountain walked or stumbled'.",
    ),
    (
        "Azathoth",
        "Outer God",
        "The blind idiot god and 'daemon sultan' at the center of infinity, around whom "
        "lesser gods dance to the piping of mad flutes.",
        None,
        None,
        "Cosmic and boundless; not a physical body in any human sense.",
    ),
    (
        "Nyarlathotep",
        "Outer God",
        "The Crawling Chaos, messenger and soul of the Outer Gods, who walks among humans "
        "in a thousand guises to spread madness.",
        None,
        None,
        "Shapeshifting; manifests in myriad forms, often humanoid.",
    ),
    (
        "Yog-Sothoth",
        "Outer God",
        "A being coterminous with all space and time, perceived as a congeries of "
        "iridescent globes; the key and gate to other dimensions.",
        None,
        None,
        "Coextensive with all reality.",
    ),
    (
        "Shub-Niggurath",
        "Outer God",
        "The Black Goat of the Woods with a Thousand Young, a fertility deity of monstrous "
        "and ever-spawning brood.",
        None,
        None,
        "Vast, cloud-like mass spawning endless young.",
    ),
    (
        "Dagon",
        "Great Old One",
        "A colossal, scaly humanoid worshipped by the Deep Ones, glimpsed rising from the "
        "depths of the ocean.",
        30.0,
        None,
        "Vast Polyphemus-like sea-dweller.",
    ),
    (
        "Shoggoth",
        "Engineered servitor",
        "A protoplasmic mass of black slime bubbling with temporary eyes and limbs, bred "
        "as slaves by the Elder Things before rebelling.",
        4.6,
        None,
        "Shapeless protoplasm, roughly 15 feet across, able to grow far larger.",
    ),
    (
        "Deep One",
        "Lesser race",
        "An immortal fish-frog humanoid dwelling in undersea cities, interbreeding with "
        "coastal humans at Innsmouth.",
        2.0,
        120.0,
        "Humanoid; never stops growing, so elders are larger.",
    ),
    (
        "Nightgaunt",
        "Lesser race",
        "A lean, black, rubbery winged creature with no face, which carries off travellers "
        "in silence through the Dreamlands.",
        2.0,
        70.0,
        "Faceless, horned, leathery flier.",
    ),
    (
        "Mi-go",
        "Alien race",
        "A fungoid, crustacean-like winged species from Yuggoth that mines Earth and "
        "extracts human brains into metal cylinders.",
        1.5,
        50.0,
        "Pinkish fungoid body roughly the size of a person.",
    ),
    (
        "Elder Thing",
        "Alien race",
        "A barrel-torsoed, star-headed, winged being — among the first intelligent life on "
        "Earth — that built cities in Antarctica.",
        2.4,
        None,
        "Barrel torso about six feet tall, plus wings and tentacles.",
    ),
    (
        "Great Race of Yith",
        "Alien race",
        "A species of rugose, cone-shaped beings that projects its minds across time, "
        "swapping bodies with creatures of other eras.",
        3.0,
        None,
        "Iridescent cone roughly ten feet tall.",
    ),
    (
        "Hound of Tindalos",
        "Extra-dimensional predator",
        "A lean, hungry entity that dwells in the angles of time and hunts those who travel "
        "into the distant past.",
        None,
        None,
        "Manifests through sharp angles; no stable physical size.",
    ),
    (
        "The Colour Out of Space",
        "Alien entity",
        "An indescribable colour beyond the visible spectrum, arriving in a meteorite and "
        "draining the life and sanity from everything around it.",
        None,
        None,
        "Intangible radiance; a hue with no earthly analogue.",
    ),
    (
        "Gug",
        "Lesser race",
        "A towering, black-furred giant of the Dreamlands underworld with a vertical mouth "
        "splitting its face and forepaws on its arms.",
        6.0,
        None,
        "Towering, roughly twenty feet tall.",
    ),
    (
        "Moon-beast",
        "Lesser race",
        "A greyish-white, toad-like slaver of the Dreamlands that trades in human souls and "
        "serves Nyarlathotep.",
        2.5,
        200.0,
        "Bloated, pinkish-grey, toad-like bulk.",
    ),
    (
        "Ghast",
        "Lesser race",
        "A kangaroo-like, hoofed dweller of the lightless Vaults of Zin that preys on the "
        "blind and the lost.",
        1.8,
        90.0,
        "Loping, hoofed, roughly man-sized.",
    ),
    (
        "Star-spawn of Cthulhu",
        "Great Old One",
        "The smaller kin and priesthood of Cthulhu, who came down from the stars to build "
        "R'lyeh and rule the early Earth.",
        30.0,
        None,
        "Like Cthulhu in form, on a smaller scale.",
    ),
    (
        "Wilbur Whateley",
        "Human hybrid",
        "The half-human son of Yog-Sothoth, born in Dunwich, who grew at monstrous speed "
        "and hid a non-human body beneath his clothes.",
        2.7,
        None,
        "Abnormally tall; near nine feet by adolescence.",
    ),
    (
        "The Dunwich Horror",
        "Hybrid monstrosity",
        "The invisible, barn-sized twin brother of Wilbur Whateley, another spawn of "
        "Yog-Sothoth, revealed only by its footprints and stench.",
        None,
        None,
        "House-sized and invisible to the naked eye.",
    ),
    (
        "Yig",
        "Great Old One",
        "The Father of Serpents, a snake-god who takes terrible vengeance on those who harm "
        "his children.",
        None,
        None,
        "Serpentine deity of variable form.",
    ),
    (
        "Tsathoggua",
        "Great Old One",
        "A squat, furred, toad-and-sloth-like god slumbering in the black gulf of N'kai "
        "beneath the earth.",
        2.0,
        None,
        "Squat and bloated, the size of a large man.",
    ),
]

# (entity_name, work_title, work_type, year)
APPEARANCES = [
    ("Cthulhu", "The Call of Cthulhu", "short story", 1928),
    ("Cthulhu", "The Whisperer in Darkness", "novella", 1931),
    ("Azathoth", "The Dream-Quest of Unknown Kadath", "novella", 1943),
    ("Azathoth", "The Whisperer in Darkness", "novella", 1931),
    ("Nyarlathotep", "Nyarlathotep", "prose poem", 1920),
    ("Nyarlathotep", "The Dream-Quest of Unknown Kadath", "novella", 1943),
    ("Nyarlathotep", "The Whisperer in Darkness", "novella", 1931),
    ("Yog-Sothoth", "The Dunwich Horror", "novella", 1929),
    ("Yog-Sothoth", "The Case of Charles Dexter Ward", "novel", 1941),
    ("Yog-Sothoth", "Through the Gates of the Silver Key", "novella", 1934),
    ("Shub-Niggurath", "The Whisperer in Darkness", "novella", 1931),
    ("Shub-Niggurath", "The Dunwich Horror", "novella", 1929),
    ("Dagon", "Dagon", "short story", 1919),
    ("Dagon", "The Shadow over Innsmouth", "novella", 1936),
    ("Shoggoth", "At the Mountains of Madness", "novella", 1936),
    ("Shoggoth", "The Shadow over Innsmouth", "novella", 1936),
    ("Deep One", "The Shadow over Innsmouth", "novella", 1936),
    ("Nightgaunt", "The Dream-Quest of Unknown Kadath", "novella", 1943),
    ("Nightgaunt", "Fungi from Yuggoth", "sonnet cycle", 1943),
    ("Mi-go", "The Whisperer in Darkness", "novella", 1931),
    ("Elder Thing", "At the Mountains of Madness", "novella", 1936),
    ("Great Race of Yith", "The Shadow Out of Time", "novella", 1936),
    ("Hound of Tindalos", "The Hounds of Tindalos", "short story", 1929),
    ("The Colour Out of Space", "The Colour Out of Space", "short story", 1927),
    ("Gug", "The Dream-Quest of Unknown Kadath", "novella", 1943),
    ("Moon-beast", "The Dream-Quest of Unknown Kadath", "novella", 1943),
    ("Ghast", "The Dream-Quest of Unknown Kadath", "novella", 1943),
    ("Star-spawn of Cthulhu", "At the Mountains of Madness", "novella", 1936),
    ("Star-spawn of Cthulhu", "The Call of Cthulhu", "short story", 1928),
    ("Wilbur Whateley", "The Dunwich Horror", "novella", 1929),
    ("The Dunwich Horror", "The Dunwich Horror", "novella", 1929),
    ("Yig", "The Curse of Yig", "short story", 1929),
    ("Tsathoggua", "The Whisperer in Darkness", "novella", 1931),
    ("Tsathoggua", "The Mound", "novella", 1940),
]
