import re
import time

from typing import List, Tuple, Dict, Union
from html import unescape


class CategoryParser():
    def __init__(self, html: str):
        super().__init__()
        self._html = html
        self._lines = html.split("\n")

    @property
    def text(self):
        return self._html

    def name(self) -> str:
        if len(self._lines) == 0:
            return None

        m = re.search(r"<B>(.*?)</B><br>", self._lines[0])

        if m is None:
            return None

        return m.group(1).strip()

    def boards(self) -> List[Dict[str, str]]:
        """
        Returns
        -------
        {'name', 'server', 'board'}
        """

        board_reg = re.compile(r"<A HREF=http://(.*?).5ch.net/(.*?)/>(.*?)</A>")

        boards = []
        for line in self._lines[1:]:
            m = board_reg.search(line)

            if m is None:
                continue

            server = m.group(1).strip()
            board = m.group(2).strip()
            name = m.group(3).strip()

            boards.append({"name": name, "server": server, "board": board})

        return boards


class BbsmenuParser:
    def __init__(self, html):
        super().__init__()
        self._html = html

    @property
    def text(self):
        return self._html

    def categories(self) -> List[Dict[str, Union[str, Dict[str, str]]]]:
        """
        Returns
        -------
        [{'name': str, 'boards': {'server', 'board', 'name'}}]
        """

        cats = self._html.split("<br><br>")

        categories = []
        for cat in cats:
            cat_parser = CategoryParser(cat)
            name = cat_parser.name()

            if name is not None and name != "他のサイト":
                categories.append({"name": name, "boards": cat_parser.boards()})

        return categories


class BoardParser:
    def __init__(self, subject: str):
        super().__init__()
        self._subject = subject

    @property
    def text(self):
        return self._subject

    def threads(self) -> List[Dict[str, Union[str, int]]]:
        """
        Returns
        -------
        [{'key', 'title', 'count', 'speed'}]
        """
        txt = unescape(self._subject)

        threads = []
        now = int(time.time())
        for (i, line) in enumerate(txt.split("\n"), 1):
            m = re.search(r"^(\d{10})\.dat<>(.*)\((\d{1,})\)$", line)
            if m is not None:
                key = m.group(1).strip()
                title = m.group(2).strip()
                count = int(m.group(3).strip())

                since = int(key)

                diff = now - since

                speed = 0

                if diff > 0:
                    res_per_s = count / diff
                    speed = int(res_per_s * 60 * 60 * 24)

                threads.append(
                    {"key": key, "title": title, "count": count, "speed": speed}
                )

        return threads


class ThreadParserH:
    def __init__(self, html: str):
        super().__init__()
        self._html = html

    @property
    def text(self):
        return self._html

    def title(self) -> str:
        m = re.search("<title>(.*?)\n</title>", self._html)

        if m is not None:
            return m.group(1)
        else:
            return None

    def is_pastlog(self) -> bool:
        return re.search('<div class="stoplight stopred stopdone', self._html) is None

    def responses(self) -> List[Dict[str, Union[str, int]]]:
        """
        Returns
        -------
        [{num, mail, name, date, id, mgs}]
        """
        re_res = re.compile(
            r'<div class="post" id="(?P<num>\d+)".*?"name"><b>(<a href="mailto:(?P<mail>.*?)">)?(?P<name>.*?)(</a>)?'
            r'</b></span>.*?"date">(?P<date>.*?)<.*?"uid">(?P<id>.*?)<.*?(<span.*?>)+? (?P<msg>.*?) (</span>)+?</div>'
            r'</div><br>'
        )

        # re_link = re.compile(r'<a href="http.*?>(.*?)</a>|<a class="image".*?>(.*?)</a>')

        # re_anchor = re.compile(r'<a href.*?class="reply_link">(.*?)</a>')

        br = re.compile(r' ?<br> ')
        tag = re.compile(r'<.*?>')

        responses = []
        for res in re_res.finditer(self._html):
            number = int(res.group("num"))
            mail = res.group("mail")
            name = tag.sub("", res.group("name"))
            date = res.group("date")
            id = res.group("id")
            msg = res.group("msg")

            msg = br.sub("\n", msg)
            msg = tag.sub("", msg)
            msg = unescape(msg)

            responses.append({
                "num": number, "name": name, "mail": mail, "date": date, "id": id, "msg": msg
            })

        return responses


class ThreadParserD:
    def __init__(self, dat: str):
        super().__init__()
        self._dat = dat
        self._lines = dat.split("\n")

    @property
    def text(self):
        return self._dat

    def title(self) -> str:
        return re.search(r".*<>(.*?)$", self._lines[0]).group(1)

    def is_pastlog(self) -> bool:
        if len(self._lines) == 2:
            r = self.responses()

            if r[1]["name"] == "５ちゃんねる ★"\
                    and r[1]["message"].startswith("このスレッドは過去ログです"):
                return True

        return False

    def responses(self) -> List[Dict[str, Union[str, int]]]:
        """
        Returns
        -------
        [{num, mail, name, date, id, mgs}]
        """

        re_res = re.compile(r"(.*?)<>(.*?)<>(.*? .*?) (.*?)<> (.*?) <>.*")
        re_b = re.compile(r"</?b>")
        # re_img = re.compile(r'<a class="image".*?>(.*?)</a>')
        # re_link = re.compile(r'(http.*?)(?: |$)')
        br = re.compile(r'< ?<br> >')
        tag = re.compile(r'<.*?>')

        responses = []

        for i, l in enumerate(self._lines, 1):
            m = re_res.search(l)

            if m is None:
                continue

            name = re_b.sub("", m.group(1))
            mail = m.group(2)
            date = m.group(3)
            id = m.group(4)
            msg = m.group(5)

            msg = br.sub("\n", msg)
            msg = tag.sub("", msg)
            msg = unescape(msg)

            responses.append({
                "num": i, "name": name, "mail": mail, "date": date, "id": id, "msg": msg
            })

        return responses
