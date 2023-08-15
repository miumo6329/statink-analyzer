import json
from enums import Season


weapon_release_season_dict = {
    '52gal': Season.drizzle_2022,
    '96gal': Season.drizzle_2022,
    '96gal_deco': Season.fresh_2023,
    'bold': Season.drizzle_2022,
    'bold_neo': Season.fresh_2023,
    'bottlegeyser': Season.drizzle_2022,
    'heroshooter_replica': Season.drizzle_2022,
    'jetsweeper': Season.drizzle_2022,
    'jetsweeper_custom': Season.fresh_2023,
    'momiji': Season.chill_2022,
    'nzap85': Season.drizzle_2022,
    'nzap89': Season.fresh_2023,
    'prime': Season.drizzle_2022,
    'prime_collabo': Season.chill_2022,
    'promodeler_mg': Season.drizzle_2022,
    'promodeler_rg': Season.chill_2022,
    'sharp': Season.drizzle_2022,
    'sharp_neo': Season.fresh_2023,
    'spaceshooter': Season.chill_2022,
    'spaceshooter_collabo': Season.sizzle_2023,
    'sshooter': Season.drizzle_2022,
    'sshooter_collabo': Season.chill_2022,
    'wakaba': Season.drizzle_2022,
    'clashblaster': Season.drizzle_2022,
    'clashblaster_neo': Season.fresh_2023,
    'hotblaster': Season.drizzle_2022,
    'longblaster': Season.drizzle_2022,
    'nova': Season.drizzle_2022,
    'nova_neo': Season.chill_2022,
    'rapid': Season.drizzle_2022,
    'rapid_deco': Season.fresh_2023,
    'rapid_elite': Season.drizzle_2022,
    'rapid_elite_deco': Season.sizzle_2023,
    'sblast92': Season.sizzle_2023,
    'h3reelgun': Season.drizzle_2022,
    'h3reelgun_d': Season.sizzle_2023,
    'l3reelgun': Season.drizzle_2022,
    'l3reelgun_d': Season.fresh_2023,
    'dualsweeper': Season.drizzle_2022,
    'dualsweeper_custom': Season.sizzle_2023,
    'kelvin525': Season.drizzle_2022,
    'maneuver': Season.drizzle_2022,
    'quadhopper_black': Season.drizzle_2022,
    'quadhopper_white': Season.sizzle_2023,
    'sputtery': Season.drizzle_2022,
    'sputtery_hue': Season.chill_2022,
    'carbon': Season.drizzle_2022,
    'carbon_deco': Season.chill_2022,
    'dynamo': Season.drizzle_2022,
    'splatroller': Season.drizzle_2022,
    'splatroller_collabo': Season.fresh_2023,
    'variableroller': Season.drizzle_2022,
    'wideroller': Season.chill_2022,
    'wideroller_collabo': Season.sizzle_2023,
    'fincent': Season.sizzle_2023,
    'hokusai': Season.drizzle_2022,
    'pablo': Season.drizzle_2022,
    'pablo_hue': Season.chill_2022,
    'drivewiper': Season.drizzle_2022,
    'drivewiper_deco': Season.sizzle_2023,
    'jimuwiper': Season.drizzle_2022,
    'bamboo14mk1': Season.drizzle_2022,
    'liter4k': Season.drizzle_2022,
    'liter4k_scope': Season.drizzle_2022,
    'rpen_5h': Season.chill_2022,
    'soytuber': Season.drizzle_2022,
    'splatcharger': Season.drizzle_2022,
    'splatcharger_collabo': Season.fresh_2023,
    'splatscope': Season.drizzle_2022,
    'splatscope_collabo': Season.fresh_2023,
    'squiclean_a': Season.drizzle_2022,
    'bucketslosher': Season.drizzle_2022,
    'bucketslosher_deco': Season.chill_2022,
    'explosher': Season.drizzle_2022,
    'furo': Season.drizzle_2022,
    'hissen': Season.drizzle_2022,
    'hissen_hue': Season.fresh_2023,
    'screwslosher': Season.drizzle_2022,
    'barrelspinner': Season.drizzle_2022,
    'barrelspinner_deco': Season.sizzle_2023,
    'hydra': Season.drizzle_2022,
    'kugelschreiber': Season.drizzle_2022,
    'nautilus47': Season.drizzle_2022,
    'splatspinner': Season.drizzle_2022,
    'splatspinner_collabo': Season.chill_2022,
    'campingshelter': Season.drizzle_2022,
    'campingshelter_sorella': Season.sizzle_2023,
    'parashelter': Season.drizzle_2022,
    'spygadget': Season.drizzle_2022,
    'lact450': Season.drizzle_2022,
    'tristringer': Season.drizzle_2022,
}


class Weapon:
    def __init__(self, key, name, category, sub, special, release_season):
        self.key = key
        self.name = name
        self.category = category
        # self.xmatch_group = xmatch_group
        self.sub = sub
        self.special = special
        self.release_season = release_season


class SubWeapon:
    def __init__(self, key, name):
        self.key = key
        self.name = name


class SpecialWeapon:
    def __init__(self, key, name):
        self.key = key
        self.name = name


weapon_list = []

with (open('statink_csv_schema\\weapon.json', encoding="utf-8") as f):

    weapon_json_list = json.load(f)
    for weapon_json in weapon_json_list:
        key = weapon_json['key']
        name = weapon_json['name']['ja_JP']
        category = weapon_json['type']['key']
        sub = SubWeapon(weapon_json['sub']['key'],
                        weapon_json['sub']['name']['ja_JP'])
        special = SpecialWeapon(weapon_json['special']['key'],
                                weapon_json['special']['name']['ja_JP'])
        release_season = weapon_release_season_dict[weapon_json['key']]
        weapon = Weapon(key, name, category, sub, special, release_season)
        weapon_list.append(weapon)

    # ヒーローシューターレプリカは除外
    weapon_list = filter(lambda weapon: weapon.key != 'heroshooter_replica', weapon_list)


def get_weapon_list_by_season(season: Season):
    result = []
    for w in weapon_list:
        if w.release_season <= season:
            result.append(w)
    return result
