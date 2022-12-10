GUI Translate
-------------

To translate the program or make a translation in your language, insert in the complete.pro your language code.

```sh
pylupdate5 for_crowdin.pro
```

translate your language file: acherrank.xx.ts, and produce the .ts translation files with:

```sh
lrelease complete.pro
```

At Linux should you install the pyqt5-dev-tools to use the pylupdate5 command and qttools5-dev-tools for the lrelease:

```sh
sudo apt install pyqt5-dev-tools qttools5-dev-tools
sudo apt install qt5-default
```
