# プログラムの説明

# STEP1
環境が正しく構築されているか、動作確認します。

## step1_camera.py
USBカメラの画像が表示されることを確認します。

# STEP2
YouTube, Atom Cam2　で正しく動作するか確認します。

## step2_atomcam2.py
ATOM Cam2の画像を表示します。

## step2_youtube.py
YouTube のハワイ・マウナケアの星空ライブを表示します。

# STEP3 処理速度を確認します。
Windows, macOSで最適な処理が異なります。
最適な処理を確認します。
30FPSに達しない場合は、より高速なハードウェアを推奨します。

## step3_1_youtube_fps.py
YouTube のハワイ・マウナケアの星空ライブを表示します。
そのときにコンソールに FPS(1秒あたりの表示フレーム数)を表示します。

## step3_2_hawaii_composit_numpy.py
YouTube のハワイ・マウナケアの星空ライブを表示します。
numpy による比較明合成を実行します。

## step3_3_hawaii_composit_cv2.py
YouTube のハワイ・マウナケアの星空ライブを表示します。
OpenCV による比較明合成を実行します。

## step3_4_hawaii_composit_cv2_UMat.py
YouTube のハワイ・マウナケアの星空ライブを表示します。
OpenCV と UMat による比較明合成を実行します。

## step3_5_hawaii_composit2_numpy.py
YouTube のハワイ・マウナケアの星空ライブを表示します。
古いフレームデータを減光する比較明合成の例。

# step4 動き検出

## step4_1_motion_detection.py
GPU(UMat)を使用しない場合の動き検出の処理速度を確認します。

## step4_2_motion_detection_UMat.py
GPU(UMat)を使用した場合の動き検出の処理速度を確認します。

# STEP5 Hough変換による流れ星検出
## step5_line_detection.py
HoughLines による流れ星検出の例です。

# STEP6 動き検出による流れ星検出
## step6_1_md_ld.py
動き検出と、HoughLines による流れ星検出の例です。

## step6_2_md_ld.py
mp4ファイルに対する、動き検出とHoughLines による流れ星検出の例です。

## step6_3_md_ld2.py
mp4ファイルに対する、動き検出とHoughLines による流れ星検出の例（その2）です。

# STEP21 天文薄明とスケジューリング

## step21_twilight_zone.py
  天文薄明時間の取得と、スケジューリングの例


<hr>

# STEP31 日時の OCRの例

## step31_ocr.py
  ハワイ・マウナケア星空ライブの日時を OCRで読み取り、表示する例

