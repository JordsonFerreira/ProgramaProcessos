# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['interface.py'],  # Alterar aqui para o arquivo da interface
    pathex=[],
    binaries=[],
    datas=[
        ('C:\\Users\\jords\\OneDrive\\Área de Trabalho\\PROCESSOS\\Programa\\v2.1 - 6 DIGITOS\\Programa Processos v2.1\\Programa Processos\\anticaptcha', 'anticaptcha'),
        ('C:\\Users\\jords\\OneDrive\\Área de Trabalho\\PROCESSOS\\Programa\\v2.1 - 6 DIGITOS\\Programa Processos v2.1\\Programa Processos\\constants', 'constants'),
        ('C:\\Users\\jords\\OneDrive\\Área de Trabalho\\PROCESSOS\\Programa\\v2.1 - 6 DIGITOS\\Programa Processos v2.1\\Programa Processos\\consumer', 'consumer'),
        ('C:\\Users\\jords\\OneDrive\\Área de Trabalho\\PROCESSOS\\Programa\\v2.1 - 6 DIGITOS\\Programa Processos v2.1\\Programa Processos\\data', 'data'),
        ('C:\\Users\\jords\\OneDrive\\Área de Trabalho\\PROCESSOS\\Programa\\v2.1 - 6 DIGITOS\\Programa Processos v2.1\\Programa Processos\\load', 'load'),
        ('C:\\Users\\jords\\OneDrive\\Área de Trabalho\\PROCESSOS\\Programa\\v2.1 - 6 DIGITOS\\Programa Processos v2.1\\Programa Processos\\schema', 'schema'),
        ('C:\\Users\\jords\\OneDrive\\Área de Trabalho\\PROCESSOS\\Programa\\v2.1 - 6 DIGITOS\\Programa Processos v2.1\\Programa Processos\\service', 'service'),
        ('C:\\Users\\jords\\OneDrive\\Área de Trabalho\\PROCESSOS\\Programa\\v2.1 - 6 DIGITOS\\Programa Processos v2.1\\Programa Processos\\siimm', 'siimm'),
        ('service', 'service'),
        # Incluir o arquivo "Lista processos.txt" e "Processos.xlsx"
		('Lista processos.txt', 'Lista processos.txt'),  # Caminho relativo
        ('Processos.xlsx', 'Processos.xlsx')  # Caminho relativo
    ],
    hiddenimports=['json', 'pandas', 'requests', 'anticaptchaofficial', 'anticaptchaofficial.recaptchav2proxyless', 'selectolax', 'pydantic', 'tkinter'],
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
    name='interface',  # Defina o nome do executável aqui
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Mantenha True se deseja rodar no console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
