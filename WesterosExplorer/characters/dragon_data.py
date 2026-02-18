"""
Complete dragon data for Targaryen characters
"""
DRAGON_DATA = {
    # Conquest era
    'Aegon I Targaryen': 'Balerion (The Black Dread)',
    'Rhaenys Targaryen': 'Meraxes',
    'Visenya Targaryen': 'Vhagar',
    
    # Early Targaryens
    'Aenys I Targaryen': 'Quicksilver',
    'Maegor I Targaryen': 'Balerion',
    'Jaehaerys I Targaryen': 'Vermithrax',
    'Alysanne Targaryen': 'Silverwing',
    
    # Dance of the Dragons era
    'Viserys I Targaryen': 'Balerion (last rider)',
    'Rhaenyra Targaryen': 'Syrax',
    'Daemon Targaryen': 'Caraxes (The Blood Wyrm)',
    'Aegon II Targaryen': 'Sunfyre (The Golden)',
    'Helaena Targaryen': 'Dreamfyre',
    'Aemond Targaryen': 'Vhagar',
    'Daeron Targaryen': 'Tessarion (The Blue Queen)',
    'Jacaerys Velaryon': 'Vermax',
    'Lucerys Velaryon': 'Arrax',
    'Joffrey Velaryon': 'Tyraxes',
    'Aegon III Targaryen': 'Stormcloud (later none - Dragonbane)',
    'Viserys II Targaryen': 'None (last dragon died young)',
    
    # Later Targaryens
    'Daeron I Targaryen': 'None (dragons extinct)',
    'Baelor I Targaryen': 'None (dragons extinct)',
    'Aerys I Targaryen': 'None (dragons extinct)',
    'Maekar I Targaryen': 'None (dragons extinct)',
    'Aegon V Targaryen': 'None (dragons extinct)',
    'Duncan Targaryen': 'None (dragons extinct)',
    'Daeron Targaryen': 'None (dragons extinct)',
    'Aerys II Targaryen': 'None (dragons extinct)',
    'Rhaella Targaryen': 'None (dragons extinct)',
    'Rhaegar Targaryen': 'None (dragons extinct)',
    'Viserys Targaryen': 'None (dragons extinct)',
    'Daenerys Targaryen': 'Drogon, Rhaegal, Viserion (The Last Dragonrider)',
    
    # Other dragon riders
    'Corlys Velaryon': 'Seasmoke',
    'Laenor Velaryon': 'Seasmoke',
    'Laena Velaryon': 'Vhagar',
    'Rhaenys Targaryen (The Queen Who Never Was)': 'Meleys (The Red Queen)',
    'Hugh Hammer': 'Vermithor (The Bronze Fury)',
    'Ulf White': 'Silverwing',
    'Nettles': 'Sheepstealer',
    'Addam Velaryon': 'Seasmoke',
    'Alyn Velaryon': 'Morning',
    
    # Show characters
    'Jon Snow': 'Rhaegal (briefly)',
}

def get_dragon_info(character_name):
    """Get dragon info for a character"""
    # Check exact match
    if character_name in DRAGON_DATA:
        return DRAGON_DATA[character_name]
    
    # Check partial match
    for name, dragon in DRAGON_DATA.items():
        if name.lower() in character_name.lower() or character_name.lower() in name.lower():
            return dragon
    
    return None

def is_dragon_rider(character):
    """Check if character is a dragon rider"""
    if not character:
        return False
    
    # Check if they have dragon in their data
    if character.dragon and character.dragon not in ['None', '']:
        return True
    
    # Check dragon data
    dragon = get_dragon_info(character.name)
    if dragon and dragon != 'None' and 'extinct' not in dragon.lower():
        return True
    
    # Targaryens before the dance
    if character.house and character.house.name == 'Targaryen':
        # Parse birth year to determine era
        if character.born:
            if 'BC' in character.born or ('AC' in character.born and int(str(character.born).split()[0]) < 150):
                return True
    
    return False