def generate_gradient(start_color, end_color, num_colors, gamma=1.0):
    # 開始色と終了色をRGB値に変換
    start_r, start_g, start_b = start_color
    end_r, end_g, end_b = end_color

    # RGB値の範囲を計算
    r_range = (end_r - start_r) / (num_colors - 1)
    g_range = (end_g - start_g) / (num_colors - 1)
    b_range = (end_b - start_b) / (num_colors - 1)

    # グラデーションのリストを生成
    gradient = []
    for i in range(num_colors):
        r = (start_r + i * r_range) ** gamma
        g = (start_g + i * g_range) ** gamma
        b = (start_b + i * b_range) ** gamma
        gradient.append((r, g, b))

    return gradient


# 任意の点(x, y)を直線y=kx上に直交射影
def orthogonal_projection(x, y, k):

    # y=kx上の任意のベクトル
    bx = 1
    by = k

    # 直交射影後のベクトルはy=kx上の任意のベクトルの定数倍となる
    c = (x*bx+y*by)/(bx*bx+by*by)

    return c*bx, c*by
