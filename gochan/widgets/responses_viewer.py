import re
from typing import List, Tuple, Union,  Dict
from gochan.models import Response
from gochan.models.ng import NGResponse
from gochan.widgets import RichText, Buffer
from gochan.theme import THREAD_BRUSHES

link_reg = re.compile(r'(https?://.*?)(?=$|\n| )')


def _convert_to_buffer(responses: List[Union[Response, NGResponse]], replies: Dict[int, List[Response]],
                       bookmark: int, width: int) -> Tuple[Buffer, Dict[int, Tuple[int, int]]]:
    buf = Buffer(width)
    anchors = {}
    link_idx = 0

    for r in responses:
        if isinstance(r, NGResponse):
            if r.hide:
                anchors[r.origin.number] = ((len(buf), len(buf)))
                continue
            else:
                start = len(buf)
                buf.push(str(r.origin.number) + " " + "あぼーん", THREAD_BRUSHES["normal"])
                buf.break_line(1)
                end = len(buf)
                anchors[r.origin.number] = ((start, end))
                buf.break_line(1)
                continue

        start = len(buf)

        buf.push(str(r.number), THREAD_BRUSHES["normal"])

        if r.number in replies:
            buf.push("(" + str(len(replies[r.number])) + ")", THREAD_BRUSHES["normal"])

        buf.push(" " + r.name, THREAD_BRUSHES["name"])

        buf.push(" " + r.date + " " + r.id, THREAD_BRUSHES["normal"])

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
            buf.push(l, THREAD_BRUSHES["normal"])
            buf.break_line(1)

        end = len(buf)

        anchors[r.number] = ((start, end))

        buf.break_line(1)

        # don't render bookmark if bookmark points last response
        if r.number == bookmark and \
                len(responses) != bookmark:
            buf.push("─" * width, THREAD_BRUSHES["bookmark"])
            buf.break_line(2)

    return (buf, anchors)


class ResponsesViewer(RichText):
    def __init__(self, height, flush_cell, keybindings, **kwargs):
        super().__init__(height, flush_cell, keybindings, **kwargs)
        self._bookmark = None
        self._anchors = None

    def set_data(self, responses: List[Response], replies: Dict[int, List[Response]], bookmark: int = None):
        self._bookmark = bookmark
        (buffer, anchors) = _convert_to_buffer(responses, replies, bookmark, self.width)
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
