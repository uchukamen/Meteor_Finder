# Python 流れ星検出スターターキット

1. shooting_starについて
    このプログラムは、ハワイ・マウナケアの星空ライブから、流れ星を検出する Python プログラムの入門キットを提供します。

2. Copyright
    ここに掲載するプログラム・文書は、MIT licenseに準拠します。
    The source code and strings are licensed under the MIT license.

3. 動作環境
    Windows 10.0 以上
    macOS 12.0 以上

4. 環境設定
    ## Visual Studio Code （推奨）
   Microsoft の公式サイトより、Visual Studio Code をインストールします
   https://code.visualstudio.com/download

   ## Visual Studio Code Extension （推奨）
   Visual Studio Code を起動し、次の Extension をインストールする
    ### Japanese Language Pack for Visual Studio Code
    ### Python extension for Visual Studio Code
    ### Pylance

    ## Python （必須）
    Python.org の公式サイトより、Python 3.9 をインストールします
    https://www.python.org/ 

    ## OpenCV （必須）
    OpenCV.org の公式サイトより、OpenCV 4.5.5 をインストールします
    https://docs.opencv.org/4.5.5/

    ## ffmpeg （必須）
    FFmpeg.org FFnpeg をインストールします
    https://ffmpeg.org/

5. Python モジュールのインストール （必須）
    Windows の場合cmd、macOSの場合ターミナルを開く
    shooting_star ディレクトリに移動する
    pip install -r requirements.txt を実行し、
    必要なモジュールをインストールする

6. 動作確認
    # step1_camera.py を実行し、動画が表示されることを確認する
    # step2_hawaii.py を実行し、ハワイ・マウナケアの星空ライブが表示されることを確認する
