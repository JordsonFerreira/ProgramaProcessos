# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\\\Users\\\\jords\\\\OneDrive\\\\Área de Trabalho\\\\PROCESSOS\\\\Programa\\\\v2.1 - 6 DIGITOS\\\\Programa Processos v2.1\\\\Programa Processos\\\\anticaptcha', 'anticaptcha'), ('C:\\\\Users\\\\jords\\\\OneDrive\\\\Área de Trabalho\\\\PROCESSOS\\\\Programa\\\\v2.1 - 6 DIGITOS\\\\Programa Processos v2.1\\\\Programa Processos\\\\constants', 'constants'), ('C:\\\\Users\\\\jords\\\\OneDrive\\\\Área de Trabalho\\\\PROCESSOS\\\\Programa\\\\v2.1 - 6 DIGITOS\\\\Programa Processos v2.1\\\\Programa Processos\\\\consumer', 'consumer'), ('C:\\\\Users\\\\jords\\\\OneDrive\\\\Área de Trabalho\\\\PROCESSOS\\\\Programa\\\\v2.1 - 6 DIGITOS\\\\Programa Processos v2.1\\\\Programa Processos\\\\data', 'data'), ('C:\\\\Users\\\\jords\\\\OneDrive\\\\Área de Trabalho\\\\PROCESSOS\\\\Programa\\\\v2.1 - 6 DIGITOS\\\\Programa Processos v2.1\\\\Programa Processos\\\\load', 'load'), ('C:\\\\Users\\\\jords\\\\OneDrive\\\\Área de Trabalho\\\\PROCESSOS\\\\Programa\\\\v2.1 - 6 DIGITOS\\\\Programa Processos v2.1\\\\Programa Processos\\\\schema', 'schema'), ('C:\\\\Users\\\\jords\\\\OneDrive\\\\Área de Trabalho\\\\PROCESSOS\\\\Programa\\\\v2.1 - 6 DIGITOS\\\\Programa Processos v2.1\\\\Programa Processos\\\\service', 'service'), ('C:\\\\Users\\\\jords\\\\OneDrive\\\\Área de Trabalho\\\\PROCESSOS\\\\Programa\\\\v2.1 - 6 DIGITOS\\\\Programa Processos v2.1\\\\Programa Processos\\\\siimm', 'siimm')],
    hiddenimports=['json', 'pandas', 'requests', 'anticaptchaofficial', 'anticaptchaofficial.recaptchav2proxyless', 'selectolax', 'pydantic'],
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
    name='main',
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
