# Gochan

ターミナルで動く専用ブラウザ

![image](doc/gochan.gif)

## 動作環境

- Linux or WSL
- Python >= 3.7

Macは動くかどうか分からない

## インストール方法

`pip install gochan`

## コマンド

グローバル
- Ctrl-C : 終了
- Ctrl-N1 : 板一覧に移動
- Ctrl-N2 : スレッド一覧に移動
- Ctrl-N3 : スレッドに移動
- Ctrl-N4 : お気に入りに移動
- Ctrl-N5 : NG一覧に移動
- Ctrl-H : ヘルプを表示

スレッド一覧
- Q : レス番号昇順でソート
- Shift-Q : レス番号降順 
- W : タイトル昇順
- Shift-W : タイトル降順
- E : レス数昇順
- Shift-E : レス数降順
- R : 勢い昇順
- Shift-R : 勢い降順
- N : スレッドをNGに追加
- Ctrl-F : スレを検索
- F : お気に入りに登録
- U : 板を更新する
- B : 板一覧に戻る

スレッドビュー
- O : リンクをブラウザで開く(*WSLの場合は追加設定が必要)
- S : 画像をASCIIで表示する
- G : 対象のレスにジャンプする
- N : NGネームを追加
- W : NGワードを追加
- I : NGIDを追加
- E : IDでレスを抽出
- R : 対象のレスに付いたリプライを表示
- Shift-R : レスをポップアップ表示
- Q : ポップアップを閉じる
- F : お気に入りに登録
- U : スレッドを更新する
- B : スレッド一覧に戻る

NGビュー
- D : NGを削除
- E : NGを編集


## 一般設定
~/.gochan/conf.json に記述する(JSON形式)

項目
- browser_path : 

    リンクを開く際に使用するブラウザのパス

    指定されなければデフォルトのブラウザが使用される
    
    ただしWSLにおいてはデフォルトブラウザのパスが設定されていないので自分で書く必要がある

    Chromeを指定したいのなら、以下のように設定すれば動くはず(WSLからCドライブへは/mnt/cでアクセスすることに注意)

    ```
    {
        "browser_path" : "/mnt/c/Program Files (x86)/Google/Chrome/Application/chorome.exe"
    }
    ```

- cache_image :
 
    画像をASCIIで表示する場合、画像のダウンロードが必要になるがそれをキャッシュするかどうか（規定値:true）

- max_image_cache : 保存するキャッシュの最大数 (規定値:5)

- cache_thread : スレッドをキャッシュするかどうか (規定値:true)

- max_thread_cache : 保存するスレッドのキャッシュの最大数 (規定値:50)

- cache_board : 板をキャッシュするかどうか (規定値:true)

- max_board_cache : 保存する板のキャッシュの最大数 (規定値:50)

- default_sort : 

    スレッド一覧のデフォルトのソート方法 (規定値:number)

    number, title, count, speed のいずれか

    降順にしたい場合は頭に！を付ける (例: !number)

- max_history : 保存する閲覧履歴の最大数 (規定値:50)

- user_agent : 5chに書き込みする際に使用するUA (規定値:Mozilla/5.0)

- cookie : 5chに書き込みする際に使用するクッキー (規定値:yuki=akari)


## キーバインディング

~/.gochan/keybindings.jsonに記述する(JSON形式)

デフォルトの設定は以下の通り

```
{
    "global": {
        "exit": "C-C",
        "bbsmenu_view": "N1",
        "board_view": "N2",
        "thread_view": "N3",
        "favorites_view": "N4",
        "ng_view": "N5",
        "help": "C-H"
    },
    "bbsmenu": {
        "select_up": "UP",
        "select_down": "DOWN",
        "page_up": "PAGE_UP",
        "page_down": "PAGE_DOWN",
        "select_top": "HOME",
        "select_bottom": "END",
        "select": "ENTER"
    },
    "board": {
        "select_up": "UP",
        "select_down": "DOWN",
        "page_up": "PAGE_UP",
        "page_down": "PAGE_DOWN",
        "select_top": "HOME",
        "select_bottom": "END",
        "select": "ENTER",
        "num_sort": "Q",
        "num_des_sort": "S-Q",
        "title_sort": "W",
        "title_des_sort": "S-W",
        "count_sort": "E",
        "count_des_sort": "S-E",
        "speed_sort": "T",
        "speed_des_sort": "S-T",
        "active_sort": "R",
        "find": "C-F",
        "ng_title": "N",
        "update": "U",
        "back": "B",
        "favorite": "F"
    },
    "thread": {
        "scroll_up": "UP",
        "scroll_down": "DOWN",
        "page_up": "PAGE_UP",
        "page_down": "PAGE_DOWN",
        "go_to_top": "C-HOME",
        "go_to_bottom": "Ctrl-END",
        "open_link": "O",
        "show_image": "S",
        "go_to": "G",
        "ng_name": "N",
        "ng_id": "I",
        "ng_word": "W",
        "update": "U",
        "back": "B",
        "favorite": "F",
        "extract_id": "E",
        "show_replies": "R",
        "show_response": "S-R",
        "close_popup": "Q"
    },
    "ng": {
        "delete": "D",
        "edit": "E"
    }
}
```

### キーの指定方法

小文字と大文字の違いはない

修飾キーは頭に、Ctrl-, Shift-、またはC-, S-を付ける

組み合わせても使える Ctrl-S-X

数字キーはN0 ~ N9で指定する

その他有効特殊キー

```
ESCAPE
F1 ~ F24
PRINT_SCREEN
INSERT
DELETE
HOME
END
LEFT
UP
RIGHT
DOWN
PAGE_UP
PAGE_DOWN
BACK
TAB
BACK_TAB
NUMPAD0 ~ NUMPAD9
MULTIPLY
ADD
SUBTRACT
DECIMAL
DIVIDE
CAPS_LOCK
NUM_LOCK
SCROLL_LOCK
SHIFT
CONTROL
MENU
```

特殊キーと修飾キーの組み合わせは列挙するのが面倒だったので、Ctrl-HOME、Ctrl-END、Ctrl-UP/DOWN/LEFT/RIGHTのみ対応してる


## NG設定

NGはアプリ内から追加できる他、~/.gochan/ng.jsonを編集することで設定を変更できる

以下は設定例

```
{
    "names": [
        {
            "value": "NGにしたい名前",
            "use_reg": true,
            "hide": true,
            "auto_ng_id": true,
            "board": "news4vip",
            "key": "159375084"
        }
    ],
    "words": [
        {
            "value": "NGワード！",
            "use_reg": true,
            "hide": true,
            "auto_ng_id": true,
            "board": "news4vip"
        }
    ],
    "ids": [
        {
            "value": "ID:NGID",
            "use_reg": true,
            "hide": true
        }
    ],
    "titles": [
        {
            "value": "NGタイトル",
            "use_reg": true,
            "board": "news4vip"
        }
    ]
}
```

- value: NG対象文字列

- use_reg: 正規表現を使用するかどうか

- hide: NGを非表示にするかどうか。 names, words, idsで有効

- auto_ng_id: 自動的にIDもNGにするかどうか。 names, wordsで有効

- board : 適用対象の板。 省略可能であり、省略した場合は全板に適用される

- key:
 
    適用対象のスレッド。 省略可能であり、省略した場合は全板もしくはboardで指定した板のみ適用される

    names, words, idsで有効
