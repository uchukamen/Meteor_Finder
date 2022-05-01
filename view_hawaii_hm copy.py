import numpy as np 
import cv2
import math

ESC_KEY = 27

def get_bounding_box(X, Y):
    x_max = int(np.max(X))
    x_min = int(np.min(X))
    y_max = int(np.max(Y))
    y_min = int(np.min(Y))
    return (x_min, y_min, x_max, y_max)

def draw_bounding_box(img, bbox):
    img = cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3],), (0, 255, 0), 3)
    return img


def find_moving_objects(frame_sum, fgmask, frame_no):
    ''' 動き検出
        frame_sum (cv2 のフレーム), 
        fgmask (動き検出箇所),
        frame_no から、
        流れ星を認識して、
        stars (Star の配列), info_frame を返す
    '''

    contours, hierarchy = cv2.findContours(
        fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    moving_objects = []

    for i in range(0, len(contours)):
        contour = contours[i]

        if len(contour) < 5:    # 領域が小さいものは除外
            continue

        size = cv2.contourArea(contour)

        ellipse = cv2.fitEllipse(contour)

        # エラーケースを除外
        if math.isnan(ellipse[0][0]) or math.isnan(ellipse[0][1]):
            continue

        _draw_contours(info_frame, contours, i, color_red)


def _find_star(cap, fgbg):
    ''' 
    '''

    _frame_sum = None  # 比較明合成結果

    while True:
        ret, _frame = cap.read()
        if ret == False:
            ic("動画読込ができませんでした。_cap_read を終了します。")
            break

        if _frame is None:
            break
        if _frame_sum is None:
            _frame_sum = _frame

        # 比較明合成を実行
        if _frame_sum is None:
            _frame_sum = _frame
        _frame_sum = np.maximum(_frame, _frame_sum)

        # 動き検出用 BW フレーム
        _frame_bw = cv2.cvtColor(_frame, cv2.COLOR_RGB2GRAY)
        # 動き検出した場所
        _fgmask = fgbg.apply(_frame_bw)
        # 輪郭を求める　find contours
        _candidates, _info_frame = cv2_extend.find_moving_objects(
            _frame_sum, _fgmask, _frame_no)


        cv2.imshow('frame', _frame_with_info)

        # waitKey の間に描画している。
        keyboard = cv2.waitKey(1) & 0xFF
        if keyboard == ESC_KEY:
            break

def main():        
    cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    _find_star(cap, fgbg)


if __name__ == "__main__":
    main()    

