# astropyを使って星座をいじってみたり
# https://qiita.com/phyblas/items/a801b0f319742245ad2e

import os
import numpy as np
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
from astroquery.simbad import Simbad
from astropy import units as u
import astropy.wcs
import astropy.io.fits
from scipy.spatial.transform import Rotation as R
from icecream import ic
import math
import japanize_matplotlib
import seiza_data
import pandas as pd
from matplotlib import collections


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


def _get_seiza_all():
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
    _ra, _dec, _siz, _seiza = _get_seiza_all()

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
        _draw_text(axis, -_ra[o].degree[0], _dec[o].degree[0],
                   seiza_data.seiza_name_dict[_s], color=_col)


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


def _scatter_degree(axis, ra, dec, color, marker="*", size=1):
    ''' r, d を描画する。描画時に r軸を反転する
    '''
    axis.scatter(ra,
                 dec, c=color, marker=marker, s=500)


def _get_great_circle(ra, dec):
    ''' r, d を通る大円（流星の経路）の ra, dec の配列 (degree)を得る
    '''
    _x, _y, _z = _np_rd_to_xyz([ra], [dec])

    # r, d から、放射点　[a,b,c]を求める
    _rp_x, _rp_y, _rp_z = _rd_to_xyz(ra, dec)
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
        for _ra in np.arange(-150, 150, 1):
            _q = _quat(_vec_res, _ra)
            _quat_v = R.from_quat(_q)
            _gc = _quat_v.apply(_vec_r)
            _great_circle.append(_gc)
        [_x, _y, _z] = np.array(_great_circle).T

        _ra, dec = _np_xyz_to_rd(_x, _y, _z)
        _r_all.append(_ra)
        _d_all.append(dec)
    return _r_all, _d_all


def _draw_great_circle(axis, ra, dec, color, size=1):
    ''' r, d を通る大円（流星の経路）を描画する
    '''
    _scatter(axis, [ra], [dec], "green", marker="+", size=500)

    _r_all, _d_all = _get_great_circle(ra, dec)
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
    _r = math.radians(-ra)
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


def _draw_meteor_lines_from_csv(axis):
    ''' 長谷川さん作成の流星経路データ（CSVファイル）から、
        チャートに流星の経路の線分を描画する
    '''
    filename = "20220531-L1_results.csv"
    _df = pd.read_csv(filename)
    _df = _df[np.abs(_df['Distance']) <= 10.0]
    _df = _df[_df['Direction'] < 0.0]
    # 開始点
    _ra1 = _df['RA1']
    _dec1 = _df['DEC1']
    # 修了点
    _ra2 = _df['RA2']
    _dec2 = _df['DEC2']
    # 座標を描画用に変換
    _ra1 = np.multiply(-1.0, np.deg2rad(np.where(_ra1 >=
                                                 180, _ra1 - 360.0, _ra1)))
    _dec1 = np.deg2rad(_dec1)
    _ra2 = np.multiply(-1.0, np.deg2rad(np.where(_ra2 >=
                                                 180, _ra2 - 360.0, _ra2)))
    _dec2 = np.deg2rad(_dec2)

    _lines = np.array(([_ra1, _ra2], [_dec1, _dec2])).T

    _line_collection = collections.LineCollection(_lines)
    axis.add_collection(_line_collection)


def test_wcs1():
    ''' fits から、WCS, PIX 座標を求める
        Astro : 解析によく使う python モジュール/関数
        https://qiita.com/nishimuraatsushi/items/f422c624027dcd34b820
    '''
    # test URL
    # _url = 'http://www.astro.s.osakafu-u.ac.jp/~nishimura/Orion/data/Orion.CO1221.Osaka.beam204.mom0.fits.gz'
    _url = 'trianglum.fits'
    fits = astropy.io.fits.open(_url)
    _fits_image = fits[0].data
    wcs = astropy.wcs.WCS(fits[0].header)
    print(wcs)

    _wc = wcs.wcs_pix2world([[1920, 1080]], 0)   # (x=150, y=60) の物理座標を取得
    print("WCS: ", _wc)

    _pix = wcs.wcs_world2pix(_wc, 0)   # (l=210, b=-19) の index を取得
    print("PIX: ", _pix)
    # >>> array([[ 359.00009815,  120.00221429]])

    # >>> array([[ 213.48334194,  -20.0000389 ]])

    plt.imshow(_fits_image)
    plt.show()


def _get_fits_data(url):
    ''' url から、fitsのヘッダーと画像を取得する
    '''
    _fits = astropy.io.fits.open(url)
    _header = _fits[0].header
    _fits_image = _fits[0].data
    wcs = astropy.wcs.WCS(_header, naxis=2)
    return wcs, _fits_image


def _get_fits_area(wcs):
    ''' fitsデータの対象エリアを取得する
    '''
    _pix = [[0, 0], [1919, 0], [1079, 0], [1919, 1079]]
    _wcs = wcs.wcs_pix2world(_pix, 0)
    _ra_min = np.min(_wcs.T[0])
    _ra_max = np.max(_wcs.T[0])
    _dec_min = np.min(_wcs.T[1])
    _dec_max = np.max(_wcs.T[1])
    return (_ra_min, _ra_max, _dec_min, _dec_max)


def _select_seiza(wcs):
    ''' 対象領域の星座データを取得する
    '''
    _ra_min, _ra_max, _dec_min, _dec_max = _get_fits_area(wcs)
    _ra, _dec, _size, _s = _get_seiza_all()
    _ra_np = np.array(_ra)
    _dec_np = np.array(_dec)
    _is_inside = (_ra_max >= _ra_np) & (_ra_np >= _ra_min) & (
        _dec_max >= _dec_np) & (_dec_np >= _dec_min)
    _ra_selected = _ra[_is_inside]
    _dec_selected = _dec[_is_inside]
    _size_selected = _size[_is_inside]
    _s_selected = _s[_is_inside]
    return _ra_selected, _dec_selected, _size_selected, _s_selected


def _plot_seiza(axis, wcs):
    ''' 星座をプロットする
    '''
    _seiza = _select_seiza(wcs)    # 対象の星座を抽出する
    _seizaT = np.array(_seiza).T

    _xy_seiza = []
    for w in _seizaT:
        _pix = wcs.wcs_world2pix(np.float64([w[0:2]]), 0)
        if (1920 > _pix[0][0] and _pix[0][0] > 0 and 1080 >= _pix[0][1] and _pix[0][1] >= 0):
            _xy_seiza.append(_pix[0])
    # print("PIX: ", _xy_seiza)

    _xy_seizaT = np.array(_xy_seiza).T
    axis.scatter(_xy_seizaT[0], _xy_seizaT[1], c='red', marker='+', s=10)


def _draw_seiza_name(axis, wcs, size=5):
    ''' 星座名を描画する
    '''
    _ra, _dec, _siz, _seiza = _select_seiza(wcs)    # 対象の星座を抽出する

    _seiza_name = np.unique(_seiza)
    _ra180 = _ra.wrap_at(180 * u.deg)  # -180度 から 180度 でラップする

    _col_map = plt.get_cmap("tab10")

    for _i, _s in enumerate(_seiza_name):
        o = (_seiza == _s)

        _col = _col_map.colors[_i % 10]

        # 星座の中心点を求める
        wc = [[np.average(_ra[o].degree), np.average(_dec[o].degree)]]
        # WCSから、ピクセル座標に変換する
        _pix = wcs.wcs_world2pix(wc, 0)[0]
        # 星座名を描画する
        axis.text(_pix[0], _pix[1],
                  seiza_data.seiza_name_dict[_s], color='white')


def _draw_radiation_lines(axis, wcs, ra, dec):
    _ra, _dec = _get_great_circle(ra, dec)
    _wc = np.vstack([np.array(_ra).flatten(), np.array(_dec).flatten()]).T

    _xy = []
    for w in _wc:
        _pix = wcs.wcs_world2pix([w], 0)
        if (1920 > _pix[0][0] and _pix[0][0] > 0 and 1080 >= _pix[0][1] and _pix[0][1] >= 0):
            _xy.append(_pix[0])

    _xyT = np.array(_xy).T
    axis.scatter(_xyT[0], _xyT[1], c='white', marker='+', s=10)

def main():
    ''' fits 画像を読み込み、流星の経路を描画する
    '''
    # fits データを取得する
    # _url = 'orion.fits'
    _url = '20220805030600_HM_L5.fits'
    
    _wcs, _fits_image = _get_fits_data(_url)

    # チャートを描画する
    _fig = plt.figure(figsize=(10, 10))     # サイズを指定
    _axis = _fig.add_subplot(
        1, 1, 1, xlim=[0, 1919], ylim=[1079, 0], projection=None)
    _axis.imshow(_fits_image.transpose(1, 2, 0))

    # 星座を描画する
    _draw_seiza_name(_axis, _wcs)

    # 星座を描画する
    # _plot_seiza(_axis, _wcs)

    
    # plt.title('みずがめ座η流星群')
    # ra = 338
    # dec = -1
    
    # plt.title('ペルセウス座流星群')
    # ra = 48
    # dec = 58

    plt.title('ペルセウス座流星群　8月5日') # 8/5 の放射点
    ra = 37
    dec = 56

    # 放射点を通る大円を描画する
    _draw_radiation_lines(_axis, _wcs, ra, dec)

    plt.show()


if __name__ == "__main__":
    if os.name == 'nt':
        # Windows VSCodeで、ic()の背景色がおかしくなる問題対応
        ic.configureOutput(outputFunction=print)
    main()
