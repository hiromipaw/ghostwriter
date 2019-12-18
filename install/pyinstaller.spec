# -*- mode: python -*-

import platform
p = platform.system()

version = open('share/version.txt').read().strip()

a = Analysis(
    ['scripts/ghostwriter-pyinstaller'],
    pathex=['.'],
    binaries=None,
    datas=[
        ('../share/version.txt', 'share'),
        ('../share/images/ghostwriter-grayscale.png', 'share/images'),
        ('../share/images/GhostWriter.png', 'share/images'),
        ('../share/images/ghostwriter.svg', 'share/images'),
        ('../share/images/icons/*', 'share/images/icons'),
        ('../share/locale/*', 'share/locale'),
        ('../share/containers/website/tor/*', 'share/containers/website/tor'),
        ('../install/licenses/*', 'licenses')
    ],
    hiddenimports=[
      'PyQt5.sip',
    ],
    hookspath=[],
    runtime_hooks=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None)

pyz = PYZ(
    a.pure, a.zipped_data,
    cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='ghostwriter-gui',
    debug=False,
    strip=False,
    upx=True,
    console=False)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='ghostwriter')

if p == 'Darwin':
    app = BUNDLE(
        coll,
        name='GhostWriter.app',
        icon='install/ghostwriter.icns',
        bundle_identifier='com.hiro.ghostwriter',
        info_plist={
            'CFBundleShortVersionString': version,
            'NSHighResolutionCapable': 'True'
        }
    )
