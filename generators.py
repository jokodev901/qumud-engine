import random
import math

from entity import Entity
from markov import MarkovNameGenerator


# Markov corpus sets
FIRST_CORPUS = ['Liam','Noah','Olivia','Emma','Oliver','Charlotte','Amelia','Ava','Elijah','Sophia','James','William','Benjamin','Lucas','Henry','Isabella','Mia','Theodore','Jack','Levi','Evelyn','Alexander','Jackson','Mateo','Daniel','Michael','Mason','Sebastian','Ethan','Logan','Owen','Samuel','Jacob','Harper','Asher','Aiden','Luna','John','Joseph','Camila','Wyatt','David','Leo','Luke','Julian','Hudson','Grayson','Gianna','Matthew','Ezra','Gabriel','Elizabeth','Carter','Eleanor','Ella','Abigail','Sofia','Isaac','Jayden','Luca','Avery','Anthony','Dylan','Lincoln','Thomas','Scarlett','Maverick','Emily','Aria','Penelope','Chloe','Elias','Layla','Mila','Nora','Josiah','Hazel','Charles','Madison','Caleb','Ellie','Christopher','Ezekiel','Miles','Jaxon','Isaiah','Lily','Andrew','Nova','Isla','Grace','Violet','Joshua','Aurora','Nathan','Nolan','Riley','Zoey','Willow','Adrian','Cameron','Santiago','Eli','Emilia','Aaron','Stella','Ryan','Zoe','Victoria','Cooper','Angel','Waylon','Easton','Kai','Christian','Landon','Hannah','Colton','Roman','Axel','Addison','Lucy','Leah','Brooks','Eliana','Jonathan','Robert','Ivy','Everly','Lillian','Jameson','Ian','Paisley','Elena','Naomi','Everett','Greyson','Wesley','Jeremiah','Hunter','Leonardo','Maya','Natalie','Jordan','Jose','Bennett','Kinsley','Silas','Nicholas','Parker','Beau','Weston','Connor','Austin','Carson','Delilah','Dominic','Xavier','Claire','Jaxson']
LAST_CORPUS = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez','Hernandez','Lopez','Gonzalez','Wilson','Anderson','Thomas','Taylor','Moore','Jackson','Martin','Lee','Perez','Thompson','White','Harris','Sanchez','Clark','Ramirez','Lewis','Robinson','Walker','Young','Allen','King','Wright','Scott','Torres','Nguyen','Hill','Flores','Green','Adams','Nelson','Baker','Hall','Rivera','Campbell','Mitchell','Carter','Roberts','Gomez','Phillips','Evans','Turner','Diaz','Parker','Cruz','Edwards','Collins','Reyes','Stewart','Morris','Morales','Murphy','Cook','Rogers','Gutierrez','Ortiz','Morgan','Cooper','Peterson','Bailey','Reed','Kelly','Howard','Ramos','Kim','Cox','Ward','Richardson','Watson','Brooks','Chavez','Wood','James','Bennett','Gray','Mendoza','Ruiz','Hughes','Price','Alvarez','Castillo','Sanders','Patel','Myers','Long','Ross','Foster','Jimenez','Powell','Jenkins','Perry','Russell','Sullivan','Bell','Coleman','Butler','Henderson','Barnes','Gonzales','Fisher','Vasquez','Simmons','Romero','Jordan','Patterson','Alexander','Hamilton','Graham','Reynolds','Griffin','Wallace','Moreno','West','Cole','Hayes','Bryant','Herrera','Gibson','Ellis','Tran','Medina','Aguilar','Stevens','Murray','Ford','Castro','Marshall','Owens','Harrison','Fernandez','Mcdonald','Woods','Washington','Kennedy','Wells','Vargas','Henry','Chen','Freeman','Webb','Tucker','Guzman','Burns','Crawford','Olson','Simpson','Porter','Hunter']
CITY_CORPUS = ['London','Birmingham','Leeds','Glasgow','Sheffield','Bradford','Liverpool','Edinburgh','Manchester','Bristol','Kirklees','Fife','Wirral','North Lanarkshire','Wakefield','Cardiff','Dudley','Wigan','East Riding','South Lanarkshire','Coventry','Belfast','Leicester','Sunderland','Sandwell','Doncaster','Stockport','Sefton','Nottingham','Newcastle-upon-Tyne','Kingston-upon-Hull','Bolton','Walsall','Plymouth','Rotherham','Stoke-on-Trent','Wolverhampton','Rhondda, Cynon, Taff','South Gloucestershire','Derby','Swansea','Salford','Aberdeenshire','Barnsley','Tameside','Oldham','Trafford','Aberdeen','Southampton','Highland','Rochdale','Solihull','Gateshead','Milton Keynes','North Tyneside','Calderdale','Northampton','Portsmouth','Warrington','North Somerset','Bury','Luton','St Helens','Stockton-on-Tees','Renfrewshire','York','Thamesdown','Southend-on-Sea','New Forest','Caerphilly','Carmarthenshire','Bath & North East Somerset','Wycombe','Basildon','Bournemouth','Peterborough','North East Lincolnshire','Chelmsford','Brighton','South Tyneside','Charnwood','Aylesbury Vale','Colchester','Knowsley','North Lincolnshire','Huntingdonshire','Macclesfield','Blackpool','West Lothian','South Somerset','Dundee','Basingstoke & Deane','Harrogate','Dumfries & Galloway','Middlesbrough','Flintshire','Rochester-upon-Medway','The Wrekin','Newbury','Falkirk','Reading','Wokingham','Windsor & Maidenhead','Maidstone','Redcar & Cleveland','North Ayrshire','Blackburn','Neath Port Talbot','Poole','Wealden','Arun','Bedford','Oxford','Lancaster','Newport','Canterbury','Preston','Dacorum','Cherwell','Perth & Kinross','Thurrock','Tendring','Kings Lynn & West Norfolk','St Albans','Bridgend','South Cambridgeshire','Braintree','Norwich','Thanet','Isle of Wight','Mid Sussex','South Oxfordshire','Guildford','Elmbridge','Stafford','Powys','East Hertfordshire','Torbay','Wrexham Maelor','East Devon','East Lindsey','Halton','Warwick','East Ayrshire','Newcastle-under-Lyme','North Wiltshire','South Kesteven','Epping Forest','Vale of Glamorgan','Reigate & Banstead','Chester','Mid Bedfordshire','Suffolk Coastal','Horsham','Nuneaton & Bedworth','Gwynedd','Swale','Havant & Waterloo','Teignbridge','Cambridge','Vale Royal','Amber Valley','North Hertfordshire','South Ayrshire','Waverley','Broadland','Crewe & Nantwich','Breckland','Ipswich','Pembrokeshire','Vale of White Horse','Salisbury','Gedling','Eastleigh','Broxtowe','Stratford-on-Avon','South Bedfordshire','Angus','East Hampshire','East Dunbartonshire','Conway','Sevenoaks','Slough','Bracknell Forest','West Lancashire','West Wiltshire','Ashfield','Lisburn','Scarborough','Stroud','Wychavon','Waveney','Exeter','Dover','Test Valley','Gloucester','Erewash','Cheltenham','Bassetlaw','Scottish Borders']
MONSTERS_CORPUS = ['Ancient Red Dragon', 'Ancalagon the Black', 'Beholder', 'Glaurung', 'Wyvern', 'Linnorm', 'Smaug', 'Tiamat', 'Bahamut', 'Dracolich', 'Hydra', 'Great Ice Worm', 'Balrog', 'Mind Flayer', 'Aboleth', 'Nazgûl', 'Lich', 'Grell', 'Demogorgon', 'Gibbering Mouther', 'Displacer Beast', 'Rakshasa', 'Gelatinous Cube', 'Rust Monster', 'Nalfeshnee', 'Vrock', 'Ent', 'Owlbear', 'Chimera', 'Manticore', 'Great Eagle', 'Griffon', 'Hippogriff', 'Peryton', 'Dryad', 'Shambling Mound', 'Warg', 'Blink Dog', 'Treant', 'Satyr', 'Unicorn', 'Hill Giant', 'Frost Giant', 'Fire Giant', 'Cloud Giant', 'Storm Giant', 'Troll', 'Ogre', 'Cyclops', 'Ettin', 'Fomorian', 'Clay Golem', 'Iron Golem', 'Stone Golem', 'Flesh Golem', 'Xorn', 'Bulette', 'Barrow-wight', 'Ghoul', 'Wraith', 'Banshee', 'Death Knight', 'Vampire Lord', 'Mummy Lord', 'Specter', 'Bodak', 'Flameskull', 'Uruk-hai', 'Gnoll', 'Bugbear', 'Hobgoblin', 'Kobold', 'Lizardfolk', 'Minotaur', 'Medusa', 'Yuan-ti', 'Sahuagin', 'Kuo-toa', 'Bullywug', 'Harpy', 'Astral Dreadnought', 'Couatl', 'Nightmare', 'Hell Hound', 'Salamander', 'Marid', 'Efreeti', 'Slaad', 'Modron', 'Sphinx', 'Ungoliant', 'Shelob', 'Kraken', 'Tarrasque', 'Mimic', 'Roc', 'Basilisk', 'Cockatrice', 'Hook Horror', 'Remorhaz', 'Flumph']
DUNGEON_CORPUS = ['Widows Mine', 'Drake Mouth Cavern', 'Ancient Shipwreck', 'Cyclops Den', 'Ruins of Orvo', 'The Whispering Crypt', 'Blighted Grotto', 'Shattered Sanctum', 'Ironfang Keep', 'Dreadmarrow Catacombs', 'Shadowed Sepulcher', 'The Howling Pit', 'Sunken Temple of Aethel', 'Gilded Necropolis', 'Wraith-Haunted Burrow', 'Obsidian Vault', 'The Crimson Oubliette', 'Frozen Bastion', 'Cursed Ossuary', 'The Weeping Mines', 'Spider-Silk Hollow', 'Forsaken Citadel', 'The Maw of Despair', 'Emerald Labyrinth', 'Ancient Archives', 'The Bone Orchard', 'Scourge-Fire Peak', 'Ghost-Light Caverns', 'Lost Aqueducts of Orix', 'The Ashen Laboratory', 'Sunless Grove', 'Twisted Spire', 'Blackwood Thicket', 'The Iron Grave', 'Sirens Cove', 'The Underhall', 'Bleakwood Manor', 'Rune-Scarred Halls', 'Vile Ichor Basin', 'The Silent Bastille', 'Wyrm-Hide Den', 'Misty Chasm', 'The Shattered Spire', 'Deadmans Reach', 'Cinder-Stone Cellars', 'The Hidden Reliquary', 'Fallen Star Crater', 'The Marrow-Pick Mine', 'Glaring Eye Outpost', 'Serpents Coil Tunnel', 'The Void-Touched Rift', 'Desolate Foundry', 'Wailing Woodshed', 'The Marble Mausoleum', 'Grim-Water Lock', 'The Salt-Crusted Tomb', 'Eldritch Excavation', 'The Gloom-Weavers Nest', 'Blood-Drenched Pit', 'The Scaled Bastion', 'Forgotten Armory', 'The Lunar Shrine', 'Brimstone Crevasse', 'The Hollowed Mountain', 'Verdant Overgrowth', 'The Ruined Cloister', 'Sulfur-Stained Caves', 'The Clockwork Maze', 'Drowned Treasury','The Shifting Sands', 'Obsidian Obelisk', 'The Frost-Bitten Hold', 'Amber Web Hive', 'The Petrified Forest', 'Sun-Scorched Ruins', 'The Shadow-Step Alley', 'Basalt Fortress', 'The Murmuring Abyss', 'Lich-Fire Spire', 'The Broken Gatehouse', 'Withered Heart Grove', 'The Stone-Singers Vault', 'Cobalt Quarry', 'The Plague-Ridden Sewers', 'Thunder-Clap Gorge', 'The Eternal Prison', 'Vanguard Outpost', 'The Mossy Warren', 'Raven-Flight Tower', 'The Deep-Core Sinkhole', 'Spectral Citadel', 'The Jagged Crest', 'Whispering Willow Glen', 'The Molten Forge', 'Sable-Stone Hold', 'The Dragon-Tail Bend', 'Mirror-Glass Palace', 'The Ancient Aviary', 'Rotting Root Catacombs', 'The Final Resting Place']


def generate_entity(name: str, seed: object, level: int) -> Entity:
    '''
    (name='', attackrate=1, damage=1, health=15, range=2, speed=1, max_targets=2, stance='skirmish', initiative=5),
    
    a level 1 basic creature should be in the ballpark of:
    
    health: 3-6
    range: 1-3
    speed: 1-3
    damage: 1
    max_targets: 1
    initiative: 0-5
    stance: 'skirmish'
    '''

    random.seed(name + str(seed))

    health = math.floor(random.randrange(3, 6) * (1 + (level * 0.25)))
    range = math.floor(random.randrange(1, 2) * (1 + (level * 0.1)))
    speed = math.floor(random.randrange(1, 2) * (1 + (level * 0.1)))
    damage = math.floor(1 * (1 + (level * 0.25)))
    max_targets = 1
    initiative = random.randint(0, 5)
    stance = random.choice(['skirmish', 'assassin'])

    return Entity(name=name, attackrate=1, damage=damage, health=health, range=range, speed=speed,
                  max_targets=max_targets, initiative=initiative, stance=stance)


def generate_npcs(count: int, seed: object, level: int) -> list[Entity]:
    genfirst = MarkovNameGenerator(order=3, seed=seed, normalize_case=True)
    genlast = MarkovNameGenerator(order=3, seed=seed, normalize_case=True)

    genfirst.fit(FIRST_CORPUS)
    genlast.fit(LAST_CORPUS)

    firstnames = genfirst.generate_many(k=count, max_len=12, min_len=3, avoid_training=True)
    lastnames = genlast.generate_many(k=count, max_len=12, min_len=4, avoid_training=True)

    entities = []
    i = 0

    while i < len(firstnames):
        name = f'{(firstnames[i]).strip().title()} {lastnames[i].strip().title()}'
        entities.append(generate_entity(name, seed, level))
        i += 1

    return entities


def generate_monsters(count: int, seed: object, level: int) -> list[Entity]:
    genmonsters = MarkovNameGenerator(order=3, seed=seed, normalize_case=True)
    genmonsters.fit(MONSTERS_CORPUS)
    names = genmonsters.generate_many(k=count, max_len=12, min_len=3, avoid_training=True)

    entities = []

    for name in names:
        name = name.strip().title()
        entities.append(generate_entity(name, seed, level))

    return entities
