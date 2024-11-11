# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['vks-bootstraper.py'],
    pathex=['/home/cuongdm/anaconda3/envs/vks-bootstraper/lib/python3.10/site-packages', '/home/cuongdm/anaconda3/envs/vks-bootstraper/lib/python310.zip', '/home/cuongdm/anaconda3/envs/vks-bootstraper/lib/python3.10', '/home/cuongdm/anaconda3/envs/vks-bootstraper/lib/python3.10/lib-dynload', '/home/cuongdm/.local/lib/python3.10/site-packages'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='vks-bootstraper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
