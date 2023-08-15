import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import seaborn as sns
from scipy.stats import boxcox, zscore
from utils import generate_gradient, orthogonal_projection
from weapon_info import get_weapon_list_by_season
from enums import Lobby, Mode, Season


DIR_BATTLE_RESULTS = 'battle-results-csv\\'
DIR_WEAPON_IMAGES = 'weapon_images\\'

sns.set()
plt.rcParams['font.family'] = 'Yu Gothic'
# fonts = set([f.name for f in matplotlib.font_manager.fontManager.ttflist])
# print(fonts)


def load_battle_result(dt_start, dt_end):
    dt = dt_start
    df_result = pd.DataFrame()
    while dt <= dt_end:
        path = DIR_BATTLE_RESULTS + dt.strftime('%Y-%m-%d') + '.csv'
        print(path)
        df = pd.read_csv(path)
        df_result = pd.concat([df_result, df])
        dt += datetime.timedelta(days=1)
    return df_result


def count_rules(df, lobby, save_dir):
    df_temp = df[df['lobby'] == lobby.name]
    rules = lobby.get_rules()
    rules_label = [rule.value for rule in rules]
    count = []
    for rule in rules:
        df_rule = df_temp[df_temp['mode'] == rule.name]
        count.append(len(df_rule))

    fig, ax = plt.subplots()
    bar = ax.bar(rules_label, count, alpha=0.8)
    # bar = ax.barh(rules_label, count, alpha=0.8)
    # ax.invert_yaxis()
    ax.bar_label(bar, labels=count)
    plt.savefig(save_dir + 'rule_count.png')


def histogram_xpower(df, lobby, modes, save_dir):
    df_temp = df[df['lobby'] == lobby.name]
    # TODO: modesで指定したルールでフィルタリング
    df_xpower = df_temp.filter(items=['power'])

    print(df_xpower.describe())

    df_xpower.hist(bins=38, alpha=0.8)
    plt.tight_layout()
    plt.xlim(1200, 3000)
    plt.savefig(save_dir + 'xpower_histogram.png')


def preprocess_df(df):
    # A1(stat.ink投稿者)データを除いてDataFrameを再構成
    df_a2 = df.filter(items=[
        '# season', 'period', 'game-ver', 'lobby', 'mode', 'stage', 'time', 'win', 'knockout', 'rank', 'power',
        'alpha-inked', 'alpha-ink-percent', 'alpha-count', 'alpha-color', 'alpha-theme',
        'bravo-inked', 'bravo-ink-percent', 'bravo-count', 'bravo-color', 'bravo-theme',
        'A2-weapon', 'A2-kill-assist', 'A2-kill', 'A2-assist', 'A2-death', 'A2-special', 'A2-inked', 'A2-abilities'])
    df_a2 = df_a2.rename(columns={
        'A2-weapon': 'weapon', 'A2-kill-assist': 'kill-assist', 'A2-kill': 'kill', 'A2-assist': 'assist',
        'A2-death': 'death', 'A2-special': 'special', 'A2-inked': 'inked', 'A2-abilities': 'abilities'})
    df_a3 = df.filter(items=[
        '# season', 'period', 'game-ver', 'lobby', 'mode', 'stage', 'time', 'win', 'knockout', 'rank', 'power',
        'alpha-inked', 'alpha-ink-percent', 'alpha-count', 'alpha-color', 'alpha-theme',
        'bravo-inked', 'bravo-ink-percent', 'bravo-count', 'bravo-color', 'bravo-theme',
        'A3-weapon', 'A3-kill-assist', 'A3-kill', 'A3-assist', 'A3-death', 'A3-special', 'A3-inked', 'A3-abilities'])
    df_a3 = df_a3.rename(columns={
        'A3-weapon': 'weapon', 'A3-kill-assist': 'kill-assist', 'A3-kill': 'kill', 'A3-assist': 'assist',
        'A3-death': 'death', 'A3-special': 'special', 'A3-inked': 'inked', 'A3-abilities': 'abilities'})
    df_a4 = df.filter(items=[
        '# season', 'period', 'game-ver', 'lobby', 'mode', 'stage', 'time', 'win', 'knockout', 'rank', 'power',
        'alpha-inked', 'alpha-ink-percent', 'alpha-count', 'alpha-color', 'alpha-theme',
        'bravo-inked', 'bravo-ink-percent', 'bravo-count', 'bravo-color', 'bravo-theme',
        'A4-weapon', 'A4-kill-assist', 'A4-kill', 'A4-assist', 'A4-death', 'A4-special', 'A4-inked', 'A4-abilities'])
    df_a4 = df_a4.rename(columns={
        'A4-weapon': 'weapon', 'A4-kill-assist': 'kill-assist', 'A4-kill': 'kill', 'A4-assist': 'assist',
        'A4-death': 'death', 'A4-special': 'special', 'A4-inked': 'inked', 'A4-abilities': 'abilities'})
    df_b1 = df.filter(items=[
        '# season', 'period', 'game-ver', 'lobby', 'mode', 'stage', 'time', 'win', 'knockout', 'rank', 'power',
        'alpha-inked', 'alpha-ink-percent', 'alpha-count', 'alpha-color', 'alpha-theme',
        'bravo-inked', 'bravo-ink-percent', 'bravo-count', 'bravo-color', 'bravo-theme',
        'B1-weapon', 'B1-kill-assist', 'B1-kill', 'B1-assist', 'B1-death', 'B1-special', 'B1-inked', 'B1-abilities'])
    df_b1 = df_b1.rename(columns={
        'B1-weapon': 'weapon', 'B1-kill-assist': 'kill-assist', 'B1-kill': 'kill', 'B1-assist': 'assist',
        'B1-death': 'death', 'B1-special': 'special', 'B1-inked': 'inked', 'B1-abilities': 'abilities'})
    df_b2 = df.filter(items=[
        '# season', 'period', 'game-ver', 'lobby', 'mode', 'stage', 'time', 'win', 'knockout', 'rank', 'power',
        'alpha-inked', 'alpha-ink-percent', 'alpha-count', 'alpha-color', 'alpha-theme',
        'bravo-inked', 'bravo-ink-percent', 'bravo-count', 'bravo-color', 'bravo-theme',
        'B2-weapon', 'B2-kill-assist', 'B2-kill', 'B2-assist', 'B2-death', 'B2-special', 'B2-inked', 'B2-abilities'])
    df_b2 = df_b2.rename(columns={
        'B2-weapon': 'weapon', 'B2-kill-assist': 'kill-assist', 'B2-kill': 'kill', 'B2-assist': 'assist',
        'B2-death': 'death', 'B2-special': 'special', 'B2-inked': 'inked', 'B2-abilities': 'abilities'})
    df_b3 = df.filter(items=[
        '# season', 'period', 'game-ver', 'lobby', 'mode', 'stage', 'time', 'win', 'knockout', 'rank', 'power',
        'alpha-inked', 'alpha-ink-percent', 'alpha-count', 'alpha-color', 'alpha-theme',
        'bravo-inked', 'bravo-ink-percent', 'bravo-count', 'bravo-color', 'bravo-theme',
        'B3-weapon', 'B3-kill-assist', 'B3-kill', 'B3-assist', 'B3-death', 'B3-special', 'B3-inked', 'B3-abilities'])
    df_b3 = df_b3.rename(columns={
        'B3-weapon': 'weapon', 'B3-kill-assist': 'kill-assist', 'B3-kill': 'kill', 'B3-assist': 'assist',
        'B3-death': 'death', 'B3-special': 'special', 'B3-inked': 'inked', 'B3-abilities': 'abilities'})
    df_b4 = df.filter(items=[
        '# season', 'period', 'game-ver', 'lobby', 'mode', 'stage', 'time', 'win', 'knockout', 'rank', 'power',
        'alpha-inked', 'alpha-ink-percent', 'alpha-count', 'alpha-color', 'alpha-theme',
        'bravo-inked', 'bravo-ink-percent', 'bravo-count', 'bravo-color', 'bravo-theme',
        'B4-weapon', 'B4-kill-assist', 'B4-kill', 'B4-assist', 'B4-death', 'B4-special', 'B4-inked', 'B4-abilities'])
    df_b4 = df_b4.rename(columns={
        'B4-weapon': 'weapon', 'B4-kill-assist': 'kill-assist', 'B4-kill': 'kill', 'B4-assist': 'assist',
        'B4-death': 'death', 'B4-special': 'special', 'B4-inked': 'inked', 'B4-abilities': 'abilities'})

    # win, loseの切り替え
    df_a2.loc[df_a2['win'] == 'alpha', 'win'] = True
    df_a2.loc[df_a2['win'] == 'bravo', 'win'] = False
    df_a3.loc[df_a3['win'] == 'alpha', 'win'] = True
    df_a3.loc[df_a3['win'] == 'bravo', 'win'] = False
    df_a4.loc[df_a4['win'] == 'alpha', 'win'] = True
    df_a4.loc[df_a4['win'] == 'bravo', 'win'] = False
    df_b1.loc[df_b1['win'] == 'alpha', 'win'] = False
    df_b1.loc[df_b1['win'] == 'bravo', 'win'] = True
    df_b2.loc[df_b2['win'] == 'alpha', 'win'] = False
    df_b2.loc[df_b2['win'] == 'bravo', 'win'] = True
    df_b3.loc[df_b3['win'] == 'alpha', 'win'] = False
    df_b3.loc[df_b3['win'] == 'bravo', 'win'] = True
    df_b4.loc[df_b4['win'] == 'alpha', 'win'] = False
    df_b4.loc[df_b4['win'] == 'bravo', 'win'] = True

    # 全DataFrameを結合
    df_result = pd.DataFrame()
    df_list = [df_a2, df_a3, df_a4, df_b1, df_b2, df_b3, df_b4]
    for df_ab in df_list:
        df_result = pd.concat([df_result, df_ab])

    # ヒーローシューターレプリカはスプラシューターに置換
    df_result.loc[df_result['weapon'] == 'heroshooter_replica', 'weapon'] = 'sshooter'

    return df_result


def weapon_win_rate(df, lobby, mode, weapon_list, save_dir):
    df_xmatch = df[df['lobby'] == lobby.name]
    df_xmatch = df_xmatch[df_xmatch['mode'] == mode.name]
    df_ = preprocess_df(df_xmatch)

    # ブキ毎の勝率のDataFrameを作成
    columns = ['key', 'weapon', 'win_rate', 'win_rate_std', 'win_rate_sem', 'battle_count']
    df_win_rate = pd.DataFrame(columns=columns)
    for weapon in weapon_list:
        df_weapon = df_[df_['weapon'] == weapon.key]
        mean = df_weapon['win'].mean() * 100  # [%]
        std = df_weapon['win'].std() * 100
        sem = df_weapon['win'].sem() * 100
        count = len(df_weapon)
        df_temp = pd.DataFrame([[weapon.key, weapon.name, mean, std, sem, count]], columns=columns)
        df_win_rate = pd.concat([df_win_rate, df_temp])

    # 昇順にソート
    df_win_rate = df_win_rate.sort_values('win_rate', ascending=True)
    print(df_win_rate)

    # プロット
    fig = plt.figure(figsize=(10, 30), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    ax.errorbar(df_win_rate['win_rate'], df_win_rate['weapon'], xerr=df_win_rate['win_rate_sem'],
                capsize=4, fmt='o', ecolor='red', color='black')
    ax.grid(axis='y')
    ax.tick_params(axis='y', pad=25)
    ax.set_xticks([i for i in range(0, 100, 10)])
    ax.set_xlim([0, 100])
    ax.set_ylim([-1, len(df_win_rate)])
    plt.subplots_adjust(left=0.5, right=0.95, bottom=0.1, top=0.95)

    # ブキ画像を挿入
    i = 0
    for idx, row in df_win_rate.iterrows():
        img = plt.imread(DIR_WEAPON_IMAGES + row['key'] + '.png')
        ab = AnnotationBbox(OffsetImage(img, zoom=0.09), (0, 0), xybox=(-2.5, i),
                            frameon=False, annotation_clip=False)
        ax.add_artist(ab)
        i += 1

    plt.tight_layout()
    plt.savefig(save_dir + 'weapon_win_rate.png')

    # 勝率とバトル数の関係をプロット
    fig = plt.figure(figsize=(7, 7), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xscale("log")
    ax.set_xlim([20, 8000])
    ax.set_ylim([25, 65])
    for idx, row in df_win_rate.iterrows():
        x = row['battle_count']
        y = row['win_rate']
        img = plt.imread(DIR_WEAPON_IMAGES + row['key'] + '.png')
        ab = AnnotationBbox(OffsetImage(img, zoom=0.09), (0, 0), xybox=(x, y),
                            frameon=False, annotation_clip=False)
        ax.add_artist(ab)
    # plt.tight_layout()
    plt.savefig(save_dir + 'weapon_win_rate_battle_count.png')

    return df_win_rate


def weapon_use_rate(df, lobby, mode, weapon_list, save_dir):
    df_xmatch = df[df['lobby'] == lobby.name]
    df_xmatch = df_xmatch[df_xmatch['mode'] == mode.name]
    df_weapon = preprocess_df(df_xmatch)

    # ブキ使用率のDataFrameを作成
    columns = ['key', 'weapon', 'use_rate']
    df_weapon_use_rate = pd.DataFrame(columns=columns)
    for weapon in weapon_list:
        use_rate = (df_weapon['weapon'] == weapon.key).mean() * 100  # [%]
        df_temp = pd.DataFrame([[weapon.key, weapon.name, use_rate]], columns=columns)
        df_weapon_use_rate = pd.concat([df_weapon_use_rate, df_temp])

    # 昇順にソート
    df_weapon_use_rate = df_weapon_use_rate.sort_values('use_rate', ascending=True)
    print(df_weapon_use_rate)

    # プロット
    fig = plt.figure(figsize=(10, 30), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    color = generate_gradient((0, 1, 0), (1, 0, 0), len(df_weapon_use_rate), gamma=1/2.2)
    barh = ax.barh(df_weapon_use_rate['weapon'], df_weapon_use_rate['use_rate'], color=color, alpha=0.8)
    ax.bar_label(barh, labels=df_weapon_use_rate['use_rate'].apply(lambda x: round(x, 2)), padding=2.5)
    ax.grid(axis='y')
    ax.tick_params(axis='y', pad=25)
    ax.set_xlim([0, 10])
    ax.set_ylim([-1, len(df_weapon_use_rate)])
    plt.subplots_adjust(left=0.5, right=0.95, bottom=0.1, top=0.95)

    # ブキ画像を挿入
    i = 0
    for idx, row in df_weapon_use_rate.iterrows():
        img = plt.imread(DIR_WEAPON_IMAGES + row['key'] + '.png')
        ab = AnnotationBbox(OffsetImage(img, zoom=0.09), (0, 0), xybox=(-0.28, i),
                            frameon=False, annotation_clip=False)
        ax.add_artist(ab)
        i += 1

    plt.tight_layout()
    plt.savefig(save_dir + 'weapon_use_rate.png')
    return df_weapon_use_rate


def average_xpower_per_weapon(df, lobby, mode, weapon_list, save_dir):
    df_xmatch = df[df['lobby'] == lobby.name]
    df_xmatch = df_xmatch[df_xmatch['mode'] == mode.name]
    df_ = preprocess_df(df_xmatch)

    # ブキ毎の平均XパワーのDataFrameを作成
    columns = ['key', 'weapon', 'average_xpower', 'average_xpower_std', 'average_xpower_sem']
    df_ave_power = pd.DataFrame(columns=columns)
    for weapon in weapon_list:
        df_weapon = df_[df_['weapon'] == weapon.key]
        # print(value, df_weapon['power'].describe())
        mean = df_weapon['power'].mean()
        std = df_weapon['power'].std()
        sem = df_weapon['power'].sem()
        df_temp = pd.DataFrame([[weapon.key, weapon.name, mean, std, sem]], columns=columns)
        df_ave_power = pd.concat([df_ave_power, df_temp])

    # 昇順にソート
    df_ave_power = df_ave_power.sort_values('average_xpower', ascending=True)
    print(df_ave_power)

    # プロット
    fig = plt.figure(figsize=(10, 30), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    ax.errorbar(df_ave_power['average_xpower'], df_ave_power['weapon'], xerr=df_ave_power['average_xpower_sem'],
                capsize=4, fmt='o', ecolor='red', color='black')
    ax.grid(axis='y')
    ax.tick_params(axis='y', pad=25)
    ax.set_xlim([1800, 2300])
    ax.set_ylim([-1, len(df_ave_power)])
    plt.subplots_adjust(left=0.5, right=0.95, bottom=0.1, top=0.95)

    # ブキ画像を挿入
    i = 0
    for idx, row in df_ave_power.iterrows():
        img = plt.imread(DIR_WEAPON_IMAGES + row['key'] + '.png')
        ab = AnnotationBbox(OffsetImage(img, zoom=0.09), (0, 0), xybox=(1785, i),
                            frameon=False, annotation_clip=False)
        ax.add_artist(ab)
        i += 1

    plt.tight_layout()
    plt.savefig(save_dir + 'average_xpower.png')
    return df_ave_power


def weapon_deviation_value(df_use_rate, df_ave_xpower, save_dir):

    df = pd.merge(df_use_rate, df_ave_xpower)

    # プロット
    fig = plt.figure(figsize=(7, 7), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim([-0.5, 10])
    ax.set_ylim([1800, 2300])
    for idx, row in df.iterrows():
        x = row['use_rate']
        y = row['average_xpower']
        img = plt.imread(DIR_WEAPON_IMAGES + row['key'] + '.png')
        ab = AnnotationBbox(OffsetImage(img, zoom=0.09), (0, 0), xybox=(x, y),
                            frameon=False, annotation_clip=False)
        ax.add_artist(ab)
    plt.tight_layout()
    plt.savefig(save_dir + 'weapon_use_rate_ave_xpower.png')

    # ブキ使用率をBox-Cox変換
    print(df['use_rate'].tolist())
    boxcox_use_rate, _ = boxcox(df['use_rate'].tolist())
    df = df.assign(use_rate=boxcox_use_rate.tolist())

    # 標準化(平均0, 分散1)
    zscore_use_rate = zscore(df['use_rate'].tolist())
    zscore_ave_xpower = zscore(df['average_xpower'].tolist())
    df = df.assign(use_rate=zscore_use_rate)
    df = df.assign(average_xpower=zscore_ave_xpower)

    # プロット
    fig = plt.figure(figsize=(7, 7), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    for idx, row in df.iterrows():
        x = row['use_rate']
        y = row['average_xpower']
        img = plt.imread(DIR_WEAPON_IMAGES + row['key'] + '.png')
        ab = AnnotationBbox(OffsetImage(img, zoom=0.09), (0, 0), xybox=(x, y),
                            frameon=False, annotation_clip=False)
        ax.add_artist(ab)
    plt.tight_layout()
    plt.savefig(save_dir + 'weapon_use_rate_ave_xpower_standardization.png')

    # ブキ使用率、平均Xパワーを直交射影しスコア算出、標準化
    weapon_score = []
    for idx, row in df.iterrows():
        value = orthogonal_projection(row['use_rate'], row['average_xpower'], 0.9)
        weapon_score.append(value[0]+value[1])
    weapon_score = zscore(weapon_score)
    df['score'] = weapon_score

    # 偏差値を算出
    score_std = df['score'].std(ddof=0)
    score_mean = df['score'].mean()
    df['deviation_value'] = df['score'].map(lambda x: (x - score_mean) / score_std * 10 + 50).astype(int)

    # 昇順にソート
    df = df.sort_values('deviation_value', ascending=True)
    print(df)

    # プロット
    fig = plt.figure(figsize=(10, 30), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    color = generate_gradient((0, 1, 0), (1, 0, 0), len(df), gamma=1/2.2)
    barh = ax.barh(df['weapon'], df['deviation_value'], color=color, alpha=0.0)
    ax.bar_label(barh, labels=df['deviation_value'].apply(lambda x: round(x, 2)), padding=15)
    ax.grid(axis='y')
    ax.set_xlim([25, 75])
    ax.set_ylim([-1, len(df)])
    plt.subplots_adjust(left=0.5, right=0.95, bottom=0.1, top=0.95)

    # ブキ画像を挿入
    i = 0
    for idx, row in df.iterrows():
        img = plt.imread(DIR_WEAPON_IMAGES + row['key'] + '.png')
        ab = AnnotationBbox(OffsetImage(img, zoom=0.09), (0, 0), xybox=(row['deviation_value'], i),
                            frameon=False, annotation_clip=False)
        ax.add_artist(ab)
        i += 1
    plt.tight_layout()
    plt.savefig(save_dir + 'weapon_deviation_value.png')


def check_season(df):
    season_list = df['# season'].unique()
    if len(season_list) >= 2:
        print('対象期間に複数のシーズンが含まれます。期間内の最新シーズンのブキ情報を基に統計情報を出力します。')

    # Enumの定数名に変換 ex) 'Drizzle Season 2022' -> 'drizzle_2022'
    season_list = [season.replace(' Season ', '_') for season in season_list]
    season_list = [season.lower() for season in season_list]
    season_list = [Season[season] for season in season_list]

    season = max(season_list)
    return season


def analyze(dt_start, dt_end, lobby, mode):
    save_dir = dt_start.strftime('%Y%m%d') + '-' + dt_end.strftime('%Y%m%d') + \
               '-' + lobby.name + '-' + mode.name + '\\'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    df = load_battle_result(dt_start, dt_end)

    season = check_season(df)
    weapon_list = get_weapon_list_by_season(season)

    # 各解析グラフ作成
    if lobby == Lobby.xmatch or lobby == Lobby.bankara_challenge or lobby == Lobby.bankara_open:
        count_rules(df, lobby, save_dir)

    if lobby == Lobby.xmatch:
        # TODO: modesで指定したルールでフィルタリング
        histogram_xpower(df, lobby, [Mode.area, Mode.yagura, Mode.hoko, Mode.asari], save_dir)

    df_win_rate = weapon_win_rate(df, lobby, mode, weapon_list, save_dir)
    df_use_rate = weapon_use_rate(df, lobby, mode, weapon_list, save_dir)

    if lobby == Lobby.xmatch:
        df_ave_xpower = average_xpower_per_weapon(df, lobby, mode, weapon_list, save_dir)
        weapon_deviation_value(df_use_rate, df_ave_xpower, save_dir)


def main():
    dt_start = datetime.datetime(2023, 1, 18)
    dt_end = datetime.datetime(2023, 1, 31)
    lobby = Lobby.xmatch
    mode = Mode.area
    analyze(dt_start, dt_end, lobby, mode)


if __name__ == '__main__':
    main()
