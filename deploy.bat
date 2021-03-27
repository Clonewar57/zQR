:: This rmdir command is dangerous.  Be careful when changing.
rmdir /Q /S  dist\
python -m PyInstaller zqr\__main__.py -F --name="zqr"
Xcopy /E templates dist\templates\
copy templates\background.jpg dist\background.jpg