# Gochan

ターミナルで動く専用ブラウザ

![image](doc/gochan.gif)

## 動作環境

- Linux or WSL
- Python >= 3.5

Macは動くかどうか分からない

## インストール方法

`pip install gochan`

## コマンド

グローバル
- Ctrl-C : 終了
- Ctrl-H : 板一覧に移動
- Ctrl-J : スレッド一覧に移動
- Ctrl-K : スレッドに移動
- Ctrl-L : NG一覧に移動

スレッド一覧
- q : レス番号昇順でソート
- Q : レス番号降順 
- w : タイトル昇順
- W : タイトル降順
- e : レス数昇順
- E : レス数降順
- r : 勢い昇順
- R : 勢い降順
- n : スレッドをNGに追加
- u : 板を更新する
- b : 板一覧に戻る

スレッドビュー
- o : リンクをブラウザで開く(*WSLの場合は追加設定が必要)
- s : 画像をASCIIで表示する
- n : NGネームを追加
- w : NGワードを追加
- i : NGIDを追加
- u : スレッドを更新する
- b : スレッド一覧に戻る


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

- use_image_cache :
 
    画像をASCIIで表示する場合、画像のダウンロードが必要になるがそれをキャッシュとして保存するかどうか（規定値:true）

- max_image_cache : 保存するキャッシュの最大数 (規定値:5)

- save_thread_log : スレッドのログを保存するかどうか (規定値:true)

- max_thread_log : 保存するログの最大数 (規定値:50)

- user_agent : 5chに書き込みする際に使用するUA (規定値:Mozilla/5.0)

- cookie : 5chに書き込みする際に使用するクッキー (規定値:yuki=akari)


## キーバインディング

~/.gochan/keybindings.jsonに記述する(JSON形式)

デフォルトの設定は以下の通り

```
{
    "global": {
        "exit": "C-c",
        "bbsmenu_view": "C-h",
        "board_view": "C-j",
        "thread_view": "C-k",
        "ng_view": "C-l"
    }
    "bbsmenu": {
        "select_up": "up",
        "select_down": "down",
        "page_up": "page_up",
        "page_down": "page_down",
        "select_top": "C-home",
        "select_bottom": "C-end",
        "select": "enter",
    },
    "board": {
        "select_up": "up",
        "select_down": "down",
        "page_up": "page_up",
        "page_down": "page_down",
        "select_top": "C-hoem",
        "select_bottom": "C-end",
        "select": "enter",
        "sort_1": "q",
        "dsort_1": "S-q",
        "sort_2": "w",
        "dsort_2": "S-w",
        "sort_3": "e",
        "dsort_3": "S-e",
        "sort_4": "r",
        "dsort_4": "S-r",
        "ng_title": "n",
        "update": "u",
        "back": "b"
    },
    "thread": {
        "open_link": "o",
        "scroll_up": "up",
        "scroll_down": "down",
        "page_up": "page_up",
        "page_down": "page_down",
        "go_to_top": "C-home",
        "go_to_bottom": "C-end",
        "go_to": "g",
        "show_image": "s",
        "ng_name": "n",
        "ng_id": "i",
        "ng_word": "w",
        "update": "u",
        "back": "b"
    }
}
```

### 修飾キーの指定方法

Ctrl-x, Shift-x, またはC-x, S-x

組み合わせても使える Ctrl-S-x


## NG設定

NGはアプリ内から追加できる他、~/.gochan/ng.jsonを編集することで設定を変更できる

以下は設定例

```
{
    "items": [
        {
            "board": "news4vip",
            "key": "159375084",
            "kind": "word",
            "use_reg": false,
            "hide": false,
            "value": "NGにしたいワード"
        }
    ]
}
```

- board : 適用対象の板。 省略可能であり、省略した場合は全板に適用される

- key : 適用対象のスレッド。 省略可能であり、省略した場合は全板もしくはboardで指定した板のみ適用される

- kind: NGの種類。 title, name, id, wordの４つの中から指定する

- use_reg: 正規表現を使用するかどうか。 省略可能(規定値:false)

- hide: NGを非表示にするかどうか。 省略可能(規定値:false)

- value: NG対象文字列
