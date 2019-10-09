GUI Translate
-------------

To translate the program or make a translation in your language, insert in the complete.pro your language code.

```
pylupdate5 for_crowdin.pro
```

translate your language file: acherrank.xx.ts, and produce the .ts translation files with:

```
lrelease complete.pro
```

At Linux should you install the pyqt5-dev-tools to use the pylupdate5 command and qttools5-dev-tools for the lrelease:

apt-get install pyqt5-dev-tools qttools5-dev-tools

