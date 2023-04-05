import numpy as np

castle_heroes = ['Adelaide', 'adelaida', 'adelidea', 'Orrin', 'orin', 
                 'Valeska', 'valesca', 'valaska', 'valiska', 'walizka', 'valissa', 'valiza',  
                 'Edric', 'Sylvia', 'Beatrice', 'beatka', 'Lord Haart', 'lord hart', 'haart', 'lord harrt', 
                 'Sorsha', 'Christian', 'Tyris', 'tyris', 'tytis', 'babeczka z taktyka', 'Rion', 
                 'Adela', 'adele', 'Cuthbert', 'cuttbert', 'Ingham', 
                 'Sanya', 'Loynis', 'Caitlin', 'catlin', 'caitlyn', 'Katarzyna', 'Roland']

rampart_heroes = ['Mephala', 'mefcia', 'mepha', 'Ufretin', 'Jenova', 'yenova', 'jenowa', 'Ryland', 
                  'Giselle', 'gisela', 'gizele', 'Ivor', 'ivar', 'Clancy', 'Thorgrim', 'Kyrre', 'kyre', 
                  'Coronius', 'coronious', 'Uland', 'Elleshar', 'eleshar', 'Gem', 'Malcom', 'Melodia', 
                  'Alagar', 'a la gar', 'Aeris']

tower_heroes = ['Piquedram', 'Thane', 'Josephine', 'josephina', 'ta od golemów', 'Neela', 'Torosar', 'Fafner', 'Rissa', 
                'Iona', 'ilona', 'Astral', 'kasral', 'Halon', 'Serena', 
                'Daremyth', 'deirmith', 'demeryth', 'demetyth', 'daremtyh', 'leokadia', 'deremyth',
                'Theodorus', 'Solmyr', 'solmyr', 'solmir', 'somyr', 'Cyra', 'Aine', 'eine', 'Dracon']

inferno_heroes = ['Fiona', 'Rashka', 'Ten ze scolarem i książką', 'Marius', 'Ignatius', 'ignaś', 
                  'Octavia', 'octawia', 'octabia', 'Calh', 'cahl', 'call', 'clah', 
                  'Pyre', 'Nymus', 'Ayden', 'aiden', 
                  'Xyron', 'Axsis', 'Olema', 'Calid', 'Ash', 'Zydar', 'Xarfax']

necropolis_heroes = ['Straker', 'Vokial', 'Moandor', 'Charna', 'charana','Tamika', 'Isra', 'Clavius', 'Ranloo', 
                     'Septienna', 'septienna', 'septiene', 'septiena', 'sopthiene', 'septhienna', 'septiene',  
                     'Aislinn', 'aislynn', 'aislin', 'Sandro', 'Nimbus', 'Thant', 'Xsi', 'Vidomina', 'vido', 'Nagash',
                    'Haart Lich', 'hart lich', 
                     'Galthran', 'galtek', 'galthan', 'gaithan', 'galtran', 'galtranix', 'galthan', 
                     'Jurek']

dungeon_heroes = ['Lorelei', 'lorelai', 'lorlei', 'lorei', 'Arlach', 'arlach', 'arlah', 'Dace', 'Ajit', 'ajt', 
                  'Damacon', 'damaboss', 'damabo$$', 'Gunnar', 'gunar', 
                  'Synca', 'Shakti', 'shatki', 'szakti', 'shakty', 'shakhti', 'shahty', 'shahti', 
                  'Alamar', 'Jaegar', 'jagar', 'Malekith', 'Jeddite', 'jeddit', 
                  'Deemer', 'dimer', 'deemeer', 'Geon', 'Sephinroth', 'sephi', 'Darkstorn', 'darkstorm',
                 'Mutare Drake', 'Mutare']

stronghold_heroes = ['Yog', 'Gurnisson', 'Jabarkas', 'Crag Hack', 'crag', 'craghack', 'Shiva', 
                     'Gretchin', 'grethin', 'Krellion', 
                     'Tyraxor', 'tyrraxor', 'tyraxxor', 'tyranuxus', 't - rexor','tyra', 
                     'Gird', 'Vey', 'Dessa', 'Terek', 
                     'Zubin', 'Gundula', 'Oris', 'Saurug', 'Boragus', 'baragus']

fortress_heroes = ['Bron', 'Drakon', 'frakon', 'Wystan', 'vystan', 'Tazar', 'szef', 
                   'Alkin', 'smiec', 'śmieć', 'alkim', 'alikn',  
                   'Korbac', 'Gerwulf', 'Broghild', 'Mirlanda', 'miranda', 'Rosic', 'Voy', 
                   'Verdish', 'Kinkeria', 'Merist', 'Styg', 'Andra', 'Tiva', 'Adrienne']

conflux_heroes = ['Pasis', 'passis', 'Thunar', 'Ignissa', 'Lacus', 'Kalt', 'Fiur', 'Erdamon', 'Monere', 'monare', 
                  'Luna', 'lunka', 'Inteus', 'Grindan', 'Labetha', 'Ciele', 'Gelare', 'gelar', 'geleare', 
                  'Aenain', 'aenian', 'Brissa', 'Anakin Skywalker']

cove_heroes = ['Cassiopeia', 'casaiopea', 'casio', 'cassio', 'Derek', 'derrek', 
               'Anabel', 'anabell', 'annabele', 'szefowa', 'annabel', 'Bidley',
               'Illor', 'ilor', 'ilior','Tark', 
               'Corkes', 'corkess', 'korkes', 'Jeremy', 'jeremek', 'jeremi', 'jeremiasz', 'Miriam', 'Elmore', 
               'Leena', 'Eovacius', 'eov', 'evo', 'eovacek', 'eovacius','Astra', 'Andal', 'Manfred', 
               'Casmetra', 'Zilare', 'Spint', 'Dargem']

heroes = {'castle': castle_heroes, 'rampart': rampart_heroes, 'tower': tower_heroes, 'inferno': inferno_heroes, 
          'necropolis': necropolis_heroes, 'dungeon': dungeon_heroes, 'stronghold': stronghold_heroes,
         'fortress': fortress_heroes, 'conflux': conflux_heroes, 'cove': cove_heroes}
         
simplification_dict = {'casio': 'cassiopeia', 'tyra': 'tyraxor', 'sephi': 'sephinroth', 'darkstorm': 'darkstorn',
                      'valesca': 'valeska', 'eov': 'eovacius', 'eovacek': 'eovacius', 'aislin': 'aislinn',
                      'adelaida': 'adelaide', 'eleshar': 'elleshar', 'valaska': 'valeska', 'ilor': 'illor',
                      'jeddit': 'jeddite', 'adelidea': 'adelaide', 'charana': 'charna', 'szefowa': 'anabel',
                      'haart': 'lord haart', 'damaboss': 'damacon', 'corkess': 'corkes', 'crag': 'crag hack',
                      'caitlyn': 'caitlin', 'baragus': 'boragus', 'alkim': 'alkin', 'anabell': 'anabel',
                      'leokadia': 'daremyth', 'cuttbert': 'cuthbert', 'korkes': 'corkes', 'lord harrt': 'lord haart',
                      'arlah': 'arlach', 'octawia': 'octavia', 'jagar': 'jaegar', 'mepha': 'mephala', 'aiden': 'ayden',
                      'galtek': 'galthran', 'shatki': 'shakti', 'cassio': 'cassiopeia', 'evo': 'eovacius', 'cahl': 'calh',
                      'aenian': 'aenain', 'josephina': 'josephine', 'demeryth': 'daremyth', 'mefcia': 'mephala',
                      'gisela': 'giselle', 'shakty': 'shakti', 'ilior': 'illor', 'orin': 'orrin', 'gaithan': 'galthran',
                      'monare': 'monere', 'gunar': 'gunnar', 'lunka': 'luna', 'lord hart': 'lord haart', 
                       'gizele': 'giselle', 'szakti': 'shakti', 'eine': 'aine', 'tyrraxor': 'tyraxor', 
                       'grethin': 'gretchin', 'yenova': 'jenova', 'kyre': 'kyrre', 'lorelai': 'lorelei', 
                       'geleare': 'gelare', 'shahti': 'shakti', 'dimer': 'deemer', 'demetyth': 'daremyth',
                      'gelar': 'gelare', 'galeare': 'gelare', 'galtran': 'galthran', 'alikn': 'alkin', 'somyr': 'solmyr',
                       'annabele': 'anabel', 'jenowa': 'jenova', 'septiena': 'septienna', 'shakhti': 'shakti', 
                       'passis': 'pasis', 'catlin': 'caitlin', 'septiene': 'septienna', 'sopthiene': 'septienna', 
                       'deirmith': 'daremyth', 'miranda': 'mirlanda', 'damabo$$': 'damacon', 'vido': 'vidomina', 
                      'derrek': 'derek', 'adele': 'adela', 'coronious': 'coronius', 'septiena': 'septienna',
                       'anakin skywalker': 'aenain', 'jurek': 'clavius', 'ajt': 'ajit', 'daremtyh': 'daremyth',
                      'craghack': 'crag hack', 'tyraxxor': 'tyraxor', 'tyranuxus': 'tyraxor', 'szef': 'tazar', 
                      'smiec': 'alkin', 'śmieć': 'alkin', 'vystan': 'wystan', 'hart lich': 'haart lich', 
                       'a la gar': 'alagar', 'call': 'calh', 'ignaś': 'ignatius', 'ten ze scolarem i książką': 'rashka',
                      'babeczka z taktyka': 'tyris', 'valiska': 'valeska', 'walizka': 'valeska', 'octabia': 'octavia',
                      'ivar': 'ivor', 'ilona': 'iona', 'jeremek': 'jeremy', 'beatka': 'beatrice', 'lorlei': 'lorelei',
                      'septhienna': 'septienna', 'kasral': 'astral', 'casaiopea': 'cassiopeia', 'galtranix': 'galthran',
                      'deremyth': 'daremyth', 'annabel': 'anabel', 'lorei': 'lorelei', 'slolmyr': 'solmyr', 
                       'tytis': 'tyris', 'aislynn': 'aislinn', 'deemeer': 'deemer', 'galthan': 'galthran', 
                       'valissa': 'valeska', 'jeremiasz': 'jeremy', 'clah': 'calh', 'frakon': 'drakon', 
                       't - rexor': 'tyraxor', 'jeremi': 'jeremy', 'valiza': 'valeska', 'solmir': 'solmyr',
                      'septienne': 'septienna', 'ta od golemów': 'josephine'}
                      
                      
def merging_templates(template: str):
    '''Combines instances like h3dm1 and h3dm3 and h3dm3.2'''
    
    if template is np.nan:
        return 'w/o'
    
    elif 'h3dm' in template:
        return 'h3dm1/3'
    
    elif any(name in template for name in ['mt_firewalk', 'mt_fw', 'mt_FW', 'mt_Firewalk', 'mt_FireWalk']):
        return 'mt_Firewalk'
    
    elif 'ostalgia' in template:
        return 'Nostalgia/TP'
    
    elif '6lm' in template:
        return '6lm10a/tp'
        
    elif any(name in template for name in ['ndromeda', 'ebula']):
        return 'mt_Andromeda'
    
    elif 'mt_mp' in template:
        return 'mt_MP'
    
    elif 'mini' in template:
        return 'Mini-nostalgia'
    
    elif 'spider' in template:
        return 'Spider'
    
    elif 'mt_antares' in template:
        return 'mt_Antares'
    
    elif 'rally' in template:
        return 'Rally'
    
    elif 'mt_wrzosy' in template:
        return 'mt_Wrzosy'
        
    elif 'kubaryt' in template:
        return 'Kubaryt'
    
    else:
        return template
    
    
def binning_templates(template: str):
    if any(name in template for name in ['mt_', 'h3dm']):
        return 'Mirror'
    elif any(name in template for name in ['Jebus', 'jebus']):
        return 'Jebus'
    elif any(name in template for name in ['6lm', 'Nosta', 'Rally', 'Spider', '8mm6a', '8xm12a', 'Kubaryt']):
        return 'XL+U'
    elif template == 'Duel':
        return 'Duel'
    elif template == 'w/o':
        return 'w/o'
    else:
        return 'Other'
        
        
def determining_colour(text: str):
    '''from player_n_setup, determine the colour the player played with'''
    
    if any(name in text for name in ['red', 'Red', 'RED', 'cz', 'Cz', 'CZ']):
        return 'red'
    else:
        return 'blue'
    
    
def determining_town(text: str):
    '''from player_n_setup, determine the starting town the player played with
    Since the user can put whatever, this gets painful. I need to account for case sensitivity, language etc.'''
    
    if any(name in text for name in ['castle', 'zamek', 'Castle', 'Zamek', 'CASTLE', 'ZAMEK']):
        return 'castle'
    
    if any(name in text for name in ['ramp', 'Ramp', 'RAMP', 'bastion', 'Bastion', 'BASTION']):
        return 'rampart'
    
    if any(name in text for name in ['tower', 'Tower', 'TOWER', 'forteca', 'Forteca', 
                                     'FORTECA', 'śnieg', 'Śnieg', 'ŚNIEG']):
        return 'tower'
    
    if any(name in text for name in ['ferno', 'Ferno', 'FERNO']):
        return 'inferno'
    
    if any(name in text for name in ['necro', 'Necro', 'NECRO', 'nekr', 'Nekr', 'NEKR']):
        return 'necropolis'
    
    if any(name in text for name in ['dung', 'Dung', 'DUNG', 'loch', 'Loch', 'LOCH']):
        return 'dungeon'
    
    if any(name in text for name in ['strong', 'Strong', 'STRONG', 'twierdza', 'Twierdza', 'TWIERDZA']):
        return 'stronghold'
    
    if any(name in text for name in ['fortress', 'Fortress', 'FORTRESS', 'cyta', 'Cyta', 'CYTA',
                                    'cytka', 'Cytka', 'CYTKA', 'cytadela', 'Cytadela', 'CYTADELA',
                                    'bagno', 'Bagno', 'BAGNO']):
        return 'fortress'
    
    if any(name in text for name in ['flux', 'Flux', 'FLUX', 'wrota', 'Wrota', 'WROTA']):
        return 'conflux'
    
    if any(name in text for name in ['cove', 'Cove', 'COVE', 'przyst', 'Przyst', 'PRZYST']):
        return 'cove'