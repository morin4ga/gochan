from gochan.key import Key
from typing import Dict

from asciimatics.event import KeyboardEvent
from asciimatics.widgets import MultiColumnListBox


class MultiColumnListBoxK(MultiColumnListBox):
    """
    Key-bindable MultiColumnListBox
    """

    def __init__(self, height, columns, options, keybindings: Dict[str, Key], titles=None, label=None, name=None,
                 add_scroll_bar=False, on_change=None, on_select=None):
        super().__init__(height, columns, options, titles=titles, label=label, name=name,
                         add_scroll_bar=add_scroll_bar, on_change=on_change, on_select=on_select)

        self._keybindings = keybindings

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == self._keybindings["select_up"].value:
                self.select_up()
                return None
            elif event.key_code == self._keybindings["select_down"].value:
                self.select_down()
                return None
            elif event.key_code == self._keybindings["page_up"].value:
                self.page_up()
                return None
            elif event.key_code == self._keybindings["page_down"].value:
                self.page_down()
                return None
            elif event.key_code == self._keybindings["select_top"].value:
                self.select_top()
                return None
            elif event.key_code == self._keybindings["select_bottom"].value:
                self.select_bottom()
                return None
            elif event.key_code == self._keybindings["select"].value:
                self.select()
                return None

        return super().process_event(event)

    def select_up(self):
        if len(self._options) > 0:
            # Move up one line in text - use value to trigger on_select.
            self._line = max(0, self._line - 1)
            self.value = self._options[self._line][1]

    def select_down(self):
        if len(self._options) > 0:
            # Move down one line in text - use value to trigger on_select.
            self._line = min(len(self._options) - 1, self._line + 1)
            self.value = self._options[self._line][1]

    def page_up(self):
        if len(self._options) > 0:
            # Move up one page.
            self._line = max(0, self._line - self._h + (1 if self._titles else 0))
            self.value = self._options[self._line][1]

    def page_down(self):
        if len(self._options) > 0:
            # Move down one page.
            self._line = min(
                len(self._options) - 1, self._line + self._h - (1 if self._titles else 0))
            self.value = self._options[self._line][1]

    def select_top(self):
        if len(self._options) > 0:
            self._line = 0
            self.value = self._options[self._line][1]

    def select_bottom(self):
        if len(self._options) > 0:
            self._line = len(self._options) - 1
            self.value = self._options[self._line][1]

    def select(self):
        if len(self._options) > 0:
            # Fire select callback.
            if self._on_select:
                self._on_select()
