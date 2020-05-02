# Gochan

ターミナルで動く専用ブラウザ

スレを開いてテキストを表示させる以外の機能はない

![image](doc/gochan.gif)

## 動作環境

- Linux or WSL
- Python >= 3.5

Macは動くかどうか分からない

## インストール方法

`pip install gochan`

## 既知の問題

Windows Terminalにおいて、本来２マスとるべき一部の絵文字が１マスに描画されるバグがあり、
それによってリスト等のレイアウトの表示が崩れることがある

参照 - [Certain "emoji" are still half-sized #900](https://github.com/microsoft/terminal/issues/900)

UbuntuのGNOME Terminalとかは多分大丈夫なはず
