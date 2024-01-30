# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['BYTE_TO_PNG.py'],
    pathex=['C:\\Users\\jpmartinm\\Documents\\Programas Python\\PRUEBAS IMAGENES\\Programa'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
a.datas += [("./logo.png", "logo.png", "DATA")]
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='BYTE TO PNG',
    debug=False,
    icon='descarga.ico',
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    bootloader_version=None,
    prefix='',
    onefile=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
