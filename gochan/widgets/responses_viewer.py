import re
from typing import Dict, List, Tuple, Union

from gochan.models.ng import NGResponse
from gochan.models.thread import Response
from gochan.widgets.richtext import Brush, Buffer, RichText

link_reg = re.compile(r'(https?://.*?)(?=$|\n| )')


class ThreadBrushes:
    def __init__(self, normal: Brush, name: Brush, bookmark: Brush, highlight1: Brush, highlight2: Brush) -> None:
        self.normal = normal
        self.name = name
        self.bookmark = bookmark
        self.highlight1 = highlight1
        self.highlight2 = highlight2


def _convert_to_buffer(responses: List[Union[Response, NGResponse]], replies: Dict[int, List[Response]],
                       ids: Dict[str, List[Response]], bookmark: int, width: int, brushes: ThreadBrushes)\
        -> Tuple[Buffer, Dict[int, Tuple[int, int]]]:
    buf = Buffer(width)
    anchors = {}
    link_idx = 0

    for r in responses:
        if isinstance(r, NGResponse):
            if r.hide:
                anchors[r.origin] = ((len(buf), len(buf)))
                continue
            else:
                start = len(buf)
                buf.push(str(r.origin.number) + " " + "あぼーん", brushes.normal)
                buf.break_line(1)
                end = len(buf)
                anchors[r.origin.number] = ((start, end))
                buf.break_line(1)
                continue

        start = len(buf)

        if r.number in replies:
            if len(replies[r.number]) >= 3:
                buf.push(str(r.number) + "(" + str(len(replies[r.number])) + ")", brushes.highlight2)
            else:
                buf.push(str(r.number) + "(" + str(len(replies[r.number])) + ")", brushes.highlight1)
        else:
            buf.push(str(r.number), brushes.normal)

        buf.push(" " + r.name, brushes.name)

        buf.push(" " + r.date + " ", brushes.normal)

        idx = ids[r.id].index(r) + 1

        if len(ids[r.id]) == 1:
            buf.push(r.id, brushes.normal)
        elif len(ids[r.id]) >= 5:
            buf.push(r.id + "(" + str(idx) + "/" + str(len(ids[r.id])) + ")", brushes.highlight2)
        elif len(ids[r.id]) >= 3:
            buf.push(r.id + "(" + str(idx) + "/" + str(len(ids[r.id])) + ")", brushes.highlight1)
        else:
            buf.push(r.id + "(" + str(idx) + "/" + str(len(ids[r.id])) + ")", brushes.normal)

        buf.break_line(2)

        # Add index suffix so that user can select url easily
        def _mark_link(match):
            nonlocal link_idx
            url = match.group(1)
            repl = url + "(" + str(link_idx) + ")"
            link_idx += 1
            return repl

        marked_msg = link_reg.sub(_mark_link, r.message)

        for l in marked_msg.split("\n"):
            buf.push(l, brushes.normal)
            buf.break_line(1)

        end = len(buf)

        anchors[r.number] = ((start, end))

        buf.break_line(1)

        # don't render bookmark if bookmark points last response
        if r.number == bookmark and \
                len(responses) != bookmark:
            buf.push("─" * width, brushes.bookmark)
            buf.break_line(2)

    return (buf, anchors)


class ResponsesViewer(RichText):
    def __init__(self, height, brushes: ThreadBrushes, keybindings, **kwargs):
        super().__init__(height, brushes.normal, keybindings, **kwargs)
        self._brushes = brushes
        self._bookmark = None
        self._anchors = None

    def set_data(self, responses: List[Response], replies: Dict[int, List[Response]],
                 ids: Dict[str, List[Response]], bookmark: int = None):
        self._bookmark = bookmark
        (buffer, anchors) = _convert_to_buffer(responses, replies, ids, bookmark, self.width, self._brushes)
        self._anchors = anchors
        self._value = buffer

    def jump_to(self, number: int):
        if number in self._anchors:
            self.go_to(self._anchors[number][0])

    def get_last_respones_displayed(self):
        displayed_end_line = self.scroll_offset + self._h

        last_response = 0
        for k, v in self._anchors.items():
            if displayed_end_line >= v[1]:
                last_response = k

        return last_response

    def scroll_to_bookmark(self):
        for k, v in self._anchors.items():
            if k == self._bookmark:
                self.go_to(v[1] + 2)
                return

        self.reset_offset()
