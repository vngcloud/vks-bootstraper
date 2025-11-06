# -*- mode: python ; coding: utf-8 -*-

# ======================================================
# PyInstaller SPEC file for vks-bootstraper CLI tool
# Author: Cuong. Duong Manh <cuongdm3@vng.com.vn>
# ======================================================

block_cipher = None

a = Analysis(
    ['vks-bootstraper.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'click',
        'requests',
        'yaml',
        'python_hosts',
        'sshkey_tools',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

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
)
