pyinstaller --noconsole --onefile --hidden-import=keyboard --icon=boringx.ico --add-data "boringx.ico;." slide/main.py

mv dist/main.exe slideCooldown.exe

rm -rf build
rm -rf dist
rm -rf *.spec
