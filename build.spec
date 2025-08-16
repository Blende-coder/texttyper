# build.spec
block_cipher = None

a = Analysis(
    ['text_typer_GUI.py'],
    binaries=[],
    datas=[],
    hiddenimports=['threading','tkinter','pyautogui','webbrowser'],
    hookspath=[],
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
    name='AutoTyper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,  # Set to True if you want to see console output
    #icon='app.ico'  # Optional: add an icon file
)