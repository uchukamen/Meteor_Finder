# Meteor_Finder

## 概要

このプログラムは、ハワイ・マウナケアの星空ライブから、流れ星を検出する Python プログラムの入門キットを提供します。

## 注意
本プログラムは、無保証、無サポートです。
予告なしに仕様変更、機能追加(削除)が行われる場合があります。

## 対象データ、デバイス
* YouTubeのライブストリーミングデータ(ハワイ・マウナケアの星空ライブ)
* USBカメラ
* ATOM Cam2 (RTSP対応)
* mp4動画

## 動作環境
* m1 macOS
* Windows PC 
  
## 環境設定 mac/Windows 共通
  Visual Studio Code をインストール
  $ brew install python@3.9
  $ brew install opencv
  $ brew install ffmpeg
  $ pip install -r requirements.txt

  ### Visual Studio Code （推奨）
  Microsoft の公式サイトより、Visual Studio Code をインストールします
  https://code.visualstudio.com/download

  ### Visual Studio Code Extension （推奨）
  Visual Studio Code を起動し、次の Extension をインストールする
  #### Japanese Language Pack for Visual Studio Code
  #### Python extension for Visual Studio Code
  #### Pylance

  ### Python （必須）
  Python.org の公式サイトより、Python 3.9 をインストールします
  https://www.python.org/ 

  ### OpenCV （必須）
  OpenCV.org の公式サイトより、OpenCV 4.5.5 をインストールします
  https://docs.opencv.org/4.5.5/

  ### ffmpeg （必須）
  FFmpeg.org の公式サイトより、FFmpeg をインストールします
  https://ffmpeg.org/

## ATOM Cam2の設定
  ### 時刻設定
  モバイルデバイスから再起動を実行することにより、ATOM Cam2の時間がモバイルデバイスと同期される
  ### 動体検知をオフ
  デフォルトで動体検知が動いているので、これをOFFにする。
  不要な処理が動いていると、本体の温度が上がり、一定以上の温度になると、カメラの保護のため、自動的に処理速度が遅くなる。
  ### ロゴマーク
  画面の左下のロゴマークをOFFにする。

## ソースコードの説明
### 時刻設定
