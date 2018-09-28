# -*- mode: python -*-

block_cipher = None


a = Analysis(['RSSfeeder.py'],
             pathex=['C:\\Users\\tubas\\Desktop\\topicos_de_eng_comp\\rssfeeder'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='RSSfeeder',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='icons8_rss_filled_50_jcQ_icon.ico')
