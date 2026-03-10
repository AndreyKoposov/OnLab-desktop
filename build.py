"""Сборка приложения"""
import os
import shutil
import PyInstaller.__main__

# Очистка старых сборок
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

# Через консоль из папки src/
# pyinstaller --onedir --windowed --add-data "web;web"
# --add-data "processes;processes" --icon "web\favicon.ico"
# --add-data "data.json;." main.py

# Параметры сборки
PyInstaller.__main__.run([
    'src/main.py',
    '--onedir',
    '--name=OnLab',
    '--add-data=src/web;web',
    '--add-data=src/processes;processes',
    '--add-data=src/data.json;.',
    '--icon=src/web/favicon.ico',
    '--windowed',
    '--clean'
])
#os.system('hide_internal.bat')
