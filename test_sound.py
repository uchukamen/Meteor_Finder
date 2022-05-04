import os


def beep(freq, dur=100):
    """
        ビープ音を鳴らす.
        @param freq 周波数
        @param dur  継続時間（ms）
    """
    if os.name == 'nt':
        # Windowsの場合は、winsoundというPython標準ライブラリを使います.
        import winsound
        winsound.Beep(freq, dur)
    elif os.name == 'posix':
        # Macの場合には、Macに標準インストールされたplayコマンドを使います.
        os.system('play -n synth %s sin %s' % (dur/1000, freq))


#  2000Hzで500ms秒鳴らす
beep(2000, 500)
