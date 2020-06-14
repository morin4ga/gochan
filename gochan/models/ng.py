import re
import json

from typing import List, Dict

from gochan.config import NG_PATH
from gochan.models import Response


class NGItem:
    def __init__(self, scope: str, kind: str, value: str, use_reg: bool, hide: bool):
        super().__init__()
        self.scope = scope
        self.kind = kind
        self.value = value
        self.use_reg = use_reg
        self.hide = hide


class NGConfig:
    def __init__(self, titles, names, ids, words):
        super().__init__()
        self.titles: List[NGItem] = titles
        self.names: List[NGItem] = names
        self.ids: List[NGItem] = ids
        self.words: List[NGItem] = words

    def add_item(self, item: NGItem):
        if item.kind == "title":
            self.titles.append(item)
        elif item.kind == "name":
            self.names.append(item)
        elif item.kind == "id":
            self.ids.append(item)
        elif item.kind == "word":
            self.words.append(item)

    def is_ng_response(self, r: Response) -> int:
        """
        Returns
        -------
        0: not ng
        1: ng
        2: ng and hide
        """
        for ng_name in self.names:
            if ng_name.use_reg:
                m = re.search(ng_name.value, r.name)
                if m is not None:
                    return 2 if ng_name.hide else 1
            else:
                if ng_name.value in r.name:
                    return 2 if ng_name.hide else 1

        for ng_id in self.ids:
            if ng_id.use_reg:
                m = re.search(ng_id.value, r.id)
                if m is not None:
                    return 2 if ng_id.hide else 1
            else:
                if ng_id.value in r.id:
                    return 2 if ng_id.hide else 1

        for ng_word in self.words:
            if ng_word.use_reg:
                m = re.search(ng_word.value, r.message)
                if m is not None:
                    return 2 if ng_word.hide else 1
            else:
                if ng_word.value in r.message:
                    return 2 if ng_word.hide else 1

        return 0

    def __add__(self, right: "NGConfig") -> "NGConfig":
        return NGConfig(
            self.titles + right.titles,
            self.names + right.names,
            self.ids + right.ids,
            self.words + right.words
        )


class NG:
    def __init__(self):
        super().__init__()
        self.configs: Dict[str, NGConfig] = {"*": NGConfig([], [], [], [])}

    def get_config(self, board: str = None, key: str = None):
        conf = self.configs["*"]

        if board is not None and board in self.configs:
            conf = conf + self.configs[board]

        if key is not None and board + "-" + key in self.configs:
            conf = conf + self.configs[board + "-" + key]

        return conf

    def get_all_config(self):
        conf = None
        for k in self.configs:
            if conf is None:
                conf = self.configs[k]
            else:
                conf = conf + self.configs[k]

        return conf

    def add_item(self, scope: str, kind: str, value: str, use_reg: bool, hide: bool):
        if scope not in self.configs:
            self.configs[scope] = NGConfig()

        self.configs[scope].add_item(NGItem(scope, kind, value, use_reg, hide))


ng = NG()

if NG_PATH.is_file():
    d = json.loads(NG_PATH.read_text())

    for item in d["items"]:
        scope = item["scope"]
        kind = item["kind"]
        value = item["value"]
        use_reg = item["use_reg"]

        hide = item["hide"] if "hide" in d else False

        ng.add_item(scope, kind, value, use_reg, hide)
