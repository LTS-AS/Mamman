# -*- mode: python -*-
import os
from pprint import pprint

block_cipher = None

a = Analysis(['main.py'],
             pathex=[os.getcwd()],
             binaries= [],
             datas= [ (os.path.join('res', '*.png'), 'res' ) ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          console=False,
          debug=False,
          icon='res/app.ico',
          name='mamman',
          runtime_tmpdir=None,
          strip=False,
          upx=True,
          version='version.txt')