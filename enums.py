from enum import Enum


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
