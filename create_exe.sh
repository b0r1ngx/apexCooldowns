pyinstaller --noconsole --onefile --hidden-import=keyboard --hidden-import=mouse --icon=boringx.ico --add-data "boringx.ico;." main.py

mv dist/main.exe slideCooldown.exe

rm -rf build
rm -rf dist
rm -rf *.spec
