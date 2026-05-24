# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# We need to explicitly include the static and templates folders
# so PyInstaller knows to bundle them into the executable.
added_files = [
    ('static', 'static'),
    ('templates', 'templates')
]

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=['webview', 'spm'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PasswordManager', # The final executable name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,           # Compress if UPX is available
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,      # Hide the console window! We use webview.
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico', # We will add the icon here later when provided
)
