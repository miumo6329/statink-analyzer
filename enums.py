from enum import Enum, IntEnum, auto


class Lobby(Enum):
    regular = 'レギュラーマッチ'
    bankara_challenge = 'バンカラマッチ(チャレンジ)'
    bankara_open = 'バンカラマッチ(オープン)'
    xmatch = 'Xマッチ'
    splatfest_challenge = 'フェスマッチ(チャレンジ)'
    splatfest_open = 'フェスマッチ(オープン)'
    event = 'イベントマッチ'

    def get_rules(self):
        if self == self.regular or self == self.splatfest_challenge or self == self.splatfest_open:
            return [Mode.nawabari]
        else:
            return [Mode.area, Mode.yagura, Mode.hoko, Mode.asari]


class Mode(Enum):
    nawabari = 'ナワバリ'
    area = 'エリア'
    yagura = 'ヤグラ'
    hoko = 'ホコ'
    asari = 'アサリ'


class Season(IntEnum):
    drizzle_2022 = auto()
    chill_2022 = auto()
    fresh_2023 = auto()
    sizzle_2023 = auto()

    def to_string(self):
        if self == Season.drizzle_2022:
            return 'Drizzle Season 2022'
        elif self == Season.chill_2022:
            return 'Chill Season 2022'
        elif self == Season.fresh_2023:
            return 'Fresh Season 2023'
        elif self == Season.sizzle_2023:
            return 'Sizzle Season 2023'

    def get_season_list_newer_than(self):
        season_list = []
        for s in Season:
            if s >= self:
                season_list.append(s)
        return season_list

    def get_season_list_older_than(self):
        season_list = []
        for s in Season:
            if s <= self:
                season_list.append(s)
        return season_list
