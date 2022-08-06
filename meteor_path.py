import os
import numpy as np
import math
from astropy import units as u
from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
from scipy.spatial.transform import Rotation as R
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import collections
from seiza_data import seiza_name_dict
from icecream import ic
import japanize_matplotlib


def _quat(vec, degree) -> [4]:
    ''' 単位ベクトル vec, 角度（degree) から、クォータニオンを返す
    '''
    _x, _y, _z = vec
    _rad = math.radians(degree)
    _sin = math.sin(_rad/2)
    _quat = np.array([_x * _sin, _y * _sin, _z * _sin, math.cos(_rad/2)])
    return _quat


def _test_quat():
    ''' クォータニオンのテスト
    '''
    _deg = 90.
    _vec = [1., 0., 0.]
    _q_vec = [0., 1., 0.]

    _rot1 = R.from_rotvec([0., 0., _deg], degrees=True)
    _vec_res = _rot1.apply(np.array(_vec))
    _q = _rot1.as_quat()
    _quat = R.from_quat(_q)
    _vec_res1 = _quat.apply(np.array(_vec))

    _vec_quat = _quat(_q_vec, _deg)
    _quat_r = R.from_quat(_vec_quat)
    _vec_res = _quat_r.apply(_vec)

    print("vec: ", _vec)
    print("quat_r: ", _deg, _quat_r)
    print("vec_res: ", _vec_res)
    print("========================")


def _np_rd_to_xyz(r, d) -> (float):
    ''' numpy.array 形式の極座標(Degree)から直交座標へ変換
    '''
    _r_rad = np.deg2rad(r)
    _d_rad = np.deg2rad(d)
    _x = np.multiply(-1.0, np.cos(_d_rad) * np.sin(_r_rad))
    _y = np.sin(_d_rad)
    _z = np.cos(_d_rad) * np.cos(_r_rad)
    return _x, _y, _z


def _np_xyz_to_rd(x, y, z) -> (float):
    ''' numpy.array 形式の直交座標から極座標(Degree)へ
    '''
    _r = np.arctan2(np.multiply(-1.0, x), z)
    _d = np.arctan2(y, np.sqrt(np.multiply(x, x) + np.multiply(z, z)))
    return np.rad2deg(_r), np.rad2deg(_d)


def _rd_to_xyz(r, d) -> (float):
    ''' 極座標(Degree)から直交座標へ
    '''
    _r_rad = math.radians(r)
    _d_rad = math.radians(d)
    _x = -math.cos(_d_rad) * math.sin(_r_rad)
    _y = math.sin(_d_rad)
    _z = math.cos(_d_rad) * math.cos(_r_rad)
    return _x, _y, _z


def _xyz_to_rd(x, y, z) -> (float):
    ''' 直交座標から極座標(Degree)へ
    '''
    _r = math.atan2(-x, z)
    _d = math.atan2(y, math.sqrt((x, x) + (z, z)))
    return math.rad2deg(_r), math.rad2deg(_d)


def draw_chart(projection, figsize=(10, 10)):
    ''' matplotlib のチャートのフレームを描画する 
    '''
    _fig = plt.figure(figsize=figsize)     # サイズを指定
    if projection == 'rect':    # 矩形チャートの場合
        projection = None
    if projection in radians:   # mallweide などの天球座標の場合
        _axis = _fig.add_subplot(
            1, 1, 1, projection=projection, facecolor='black')
        _axis.tick_params(axis='x', colors="white")
        # X軸は反転する必要がある
        _axis.set_xticklabels(
            [150, 120, 90, 60, 30, 0, -30, -60, -90, -120, -150])
        _axis.grid(True)
    else:   # 矩形チャートの場合
        _axis = _fig.add_subplot(
            1, 1, 1, xlim=[180, -180], ylim=[-90, 90], projection=None, facecolor='black')
        _axis.grid(True)
    return _axis


def get_seiza_all():
    ''' 星座の全データを取得する
    '''
    _simbad = Simbad()
    _simbad.add_votable_fields('flux(V)')
    _hoshi = _simbad.query_criteria('Vmag<5', otype='star')

    _sc = SkyCoord(ra=_hoshi['RA'], dec=_hoshi['DEC'],
                  frame='icrs', unit=['hourangle', 'deg'])

    _seiza = _sc.get_constellation()

    _size = (5-_hoshi['FLUX_V'])*10

    return _sc.ra, _sc.dec, _size, _seiza


def _draw_seiza_all(axis, projection, size=1):
    ''' 全ての星座を描画する
    '''
    _ra, _dec, _siz, _seiza = get_seiza_all()

    _seiza_name = np.unique(_seiza)

    _ra180 = _ra.wrap_at(180 * u.deg)  # -180度 から 180度 でラップする

    if projection in radians:
        _ra = np.deg2rad(-_ra180)
        _dec = np.deg2rad(_dec)

    _col_map = plt.get_cmap("tab10")

    for _i, _s in enumerate(_seiza_name):
        o = (_seiza == _s)
        _col = _col_map.colors[_i % 10]
        axis.scatter(_ra[o], _dec[o], c=_col, marker="*", s=_siz[o]*size)
        _ra_center = np.average(_ra[o].degree)
        _dec_center = np.average(_dec[o].degree)
        _draw_text(axis, _ra_center, _dec_center,
                  seiza_name_dict[_s], color=_col)


def _get_seiza(seiza: str):
    ''' 指定した星座のデータを取得する
    '''
    _simbad = Simbad()
    _simbad.add_votable_fields('flux(V)')
    _hoshi = _simbad.query_criteria('Vmag<5', otype='star')

    _sc = SkyCoord(ra=_hoshi['RA'], dec=_hoshi['DEC'],
                  frame='icrs', unit=['hourangle', 'deg'])

    _seiza = _sc.get_constellation()

    _ra, _dec = _sc.ra, _sc.dec

    _size = (5-_hoshi['FLUX_V'])*10

    o = (_seiza == seiza)

    return _ra[o], _dec[o], _size[o]


def _draw_seiza(axis, projection, seiza, color='yellow', size=1):
    ''' 星座を描画する
    '''
    _ra, _dec, _size = _get_seiza(seiza)

    _ra180 = _ra.wrap_at(180 * u.deg)  # -180度 から 180度 でラップする

    if projection in radians:
        _ra = -_ra180.radian
        _dec = _dec.radian

    axis.scatter(_ra, _dec, c=color, marker="*", s=_size*size)


def _scatter(axis, ra, dec, color, marker="*", size=1):
    ''' r, d を描画する。描画時に r軸を反転する
    '''
    axis.scatter(np.multiply(-1.0, np.deg2rad(ra)),
                 np.deg2rad(dec), c=color, marker=marker, s=size)


def _draw_great_circle(axis, _ra, dec, color, size=1):
    ''' r, d を通る大円（流星の経路）を描画する
    '''
    _scatter(axis, [_ra], [dec], "green", marker="+", size=500)

    _x, _y, _z = _np_rd_to_xyz([_ra], [dec])

    # r, d から、放射点　[a,b,c]を求める
    _rp_x, _rp_y, _rp_z = _rd_to_xyz(_ra, dec)
    print("放射点: ", _rp_x, _rp_y, _rp_z)

    _x = []
    _y = []
    _z = []
    _r_all = []
    _d_all = []

    # 放射点の軸上で、直交ベクトル vec を回転する
    for _deg in np.arange(0, 360, 10):
        # 放射点ベクトル
        _vec_r = [_rp_x, _rp_y, _rp_z]
        # quat_r 放射点のクオータニオン
        _quat_r = R.from_quat(_quat(_vec_r, _deg))
        # 放射点の軸に直行するベクトル
        if _rp_y == 0 and _rp_x == 0:
            _vec = [1., 0., 0]
        else:
            _vec = [_rp_y, -_rp_x, 0]

        # 放射点の軸に直行するベクトルを放射点の軸上で回転する
        _vec_res = _quat_r.apply(_vec)

        _great_circle = []
        # 放射点ベクトル vec_r を、直行する平面にあるクオータニオン(quat_v)で回転する
        for _ra in np.arange(-150, 150, 2):
            _q = _quat(_vec_res, _ra)
            _quat_v = R.from_quat(_q)
            _gc = _quat_v.apply(_vec_r)
            _great_circle.append(_gc)
        [_x, _y, _z] = np.array(_great_circle).T

        _ra, dec = _np_xyz_to_rd(_x, _y, _z)
        _r_all.append(_ra)
        _d_all.append(dec)

    _scatter(axis, _r_all, _d_all, color=color, marker='.', size=size)


# ================================
# 投影方法
# ================================
radians = [
    'aitoff',
    'hammer',
    'polar',
    'lambert',
    'polar',
    'mollweide'
]


# オリオン 'Orion'
# おおくま座 'Ursa Major'
# カシオペア座 'Cassiopeia'
# 白鳥座 'Cygnus'

def _draw_text(axis, ra, dec, text, color='white'):
    ''' チャートに文字を描く
    '''
    _r = math.radians(ra)
    _d = math.radians(dec)
    axis.text(_r, _d, text, color=color)


def _draw_line(axis, ra, dec, color='white'):
    ''' チャートに、線分を描画する
    '''
    line_1 = [[0, 0], [math.pi/6.0, math.pi/6.0]]
    line_2 = [(0, 0), (-math.pi/4.0, -math.pi/4.0)]
    line_3 = [(0, 0), (-math.pi/4.0, -math.pi/4.0)]

    collection_1_2 = collections.LineCollection(
        [line_1, line_2, line_3], color=["red", "green"])
    axis.add_collection(collection_1_2)


def main():
    # グラフ表示
    projection = 'mollweide' # 'aifoff', 'polar', '
    _axis = draw_chart(projection, figsize=(10, 10))

    # 星座を全て描画する
    _draw_seiza_all(_axis, projection, size=1)

    # ペルセウス座流星群
    plt.title('ペルセウス座流星群')
    r = 48
    d = 58
    _draw_great_circle(_axis, r, d, color="red", size=5)

    # # ヘルクレス座τ流星群
    # plt.title('ヘルクレス座τ流星群')
    # r = 209
    # d = 28
    # draw_great_circle(ax1, r, d, color="red", size=5)

    # # みずがめ座η流星群
    # plt.title('みずがめ座η流星群')
    # r = 338
    # d = -1
    # draw_great_circle(ax1, r, d, color="cyan", size=1)

    plt.show()


if __name__ == "__main__":
    if os.name == 'nt':
        # Windows VSCodeで、ic()の背景色がおかしくなる問題対応
        ic.configureOutput(outputFunction=print)
    main()
