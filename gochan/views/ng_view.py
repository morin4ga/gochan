from asciimatics.widgets import Frame, ListBox, Widget, Layout, VerticalDivider, Divider, Label, PopUpDialog
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from typing import List, Optional

from gochan.view_models.ngvm import NGVM, NGItem, NGTitle, NGName, NGId, NGWord
from gochan.effects import NGEditor
from gochan.keybinding import KEY_BINDINGS
from gochan.event_handler import PropertyChangedEventArgs


class NGView(Frame):
    def __init__(self, screen: Screen, data_context: NGVM):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         has_border=False,
                         hover_focus=True,
                         can_scroll=False,
                         )

        self.set_theme("user_theme")

        self._keybindings = KEY_BINDINGS["ng"]

        self._data_context = data_context
        self._data_context.on_property_changed = self._context_changed

        self._selected_list: List[NGItem] = None
        self._selected_item: Optional[NGItem] = None

        self._kind_list = ListBox(4, [("Title", 0), ("Name", 1), ("Id", 2), ("Word", 3)],
                                  on_change=self._on_pick_kind)
        self._ng_list = ListBox(Widget.FILL_COLUMN, [], add_scroll_bar=True,
                                on_change=self._on_pick_ng, on_select=self._on_select_ng)

        self._label1 = Label("")
        self._label2 = Label("")
        self._label3 = Label("")
        self._label4 = Label("")
        self._label5 = Label("")

        self._form = None

        layout = Layout([20, 1, 79], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._kind_list, 0)
        layout.add_widget(Divider(), 0)
        layout.add_widget(self._label1, 0)
        layout.add_widget(self._label2, 0)
        layout.add_widget(self._label3, 0)
        layout.add_widget(self._label4, 0)
        layout.add_widget(self._label5, 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._ng_list, 2)
        self.fix()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            if event.key_code == self._keybindings["delete"]:
                if self.focussed_widget == self._ng_list and self._selected_item is not None:
                    self._data_context.delete_ng(self._selected_item.id)
                return None
            elif event.key_code == self._keybindings["edit"]:
                if self.focussed_widget == self._ng_list and self._selected_item is not None:
                    self._open_ng_editor()
                return None

        return super().process_event(event)

    def _context_changed(self, e: PropertyChangedEventArgs):
        self._selected_list = None
        self._selected_item = None
        self._kind_list.value = 0
        self._ng_list.value = 0

        self._on_pick_kind()
        self.switch_focus(self._layouts[0], 0, 0)

    def _on_pick_kind(self):
        self.save()
        idx = self._kind_list.value

        if idx == 0:
            self._selected_list = self._data_context.titles
        elif idx == 1:
            self._selected_list = self._data_context.names
        elif idx == 2:
            self._selected_list = self._data_context.ids
        elif idx == 3:
            self._selected_list = self._data_context.words

        if self._selected_list is not None:
            self._ng_list.options = _to_options(self._selected_list)

        self._on_pick_ng()

    def _on_pick_ng(self):
        self.save()
        idx = self._ng_list.value

        if self._selected_list is None or idx is None:
            self._selected_item = None
            self._label1.text = ""
            self._label2.text = ""
            self._label3.text = ""
            self._label4.text = ""
            self._label5.text = ""
            return

        self._selected_item = self._selected_list[idx]

        if isinstance(self._selected_item, NGName) or isinstance(self._selected_item, NGWord) \
                or isinstance(self._selected_item, NGId):
            self._label1.text = "board: " + \
                (self._selected_item.board if self._selected_item.board is not None else "")
            self._label2.text = "key: " + (self._selected_item.key if self._selected_item.key is not None else "")
            self._label3.text = "use_reg: " + str(self._selected_item.use_reg)
            self._label4.text = "hide: " + str(self._selected_item.hide)

            if not isinstance(self._selected_item, NGId):
                self._label5.text = "auto_ng_id: " + str(self._selected_item.auto_ng_id)
            else:
                self._label5.text = ""
        else:
            self._label1.text = "board: " + \
                (self._selected_item.board if self._selected_item.board is not None else "")
            self._label2.text = "use_reg: " + str(self._selected_item.use_reg)
            self._label3.text = ""
            self._label4.text = ""
            self._label5.text = ""

    def _on_select_ng(self):
        self._scene.add_effect(PopUpDialog(self._screen, "Choose manipulation", [
            "Edit", "Delete", "Cancel"], on_close=self._on_select_manipilation, theme="user_theme"))

    def _on_select_manipilation(self, idx):
        if idx == 0:
            self._open_ng_editor()
        elif idx == 1:
            self._data_context.delete_ng(self._selected_item.id)

    def _open_ng_editor(self):
        if self._selected_item is not None:
            if isinstance(self._selected_item, NGName):
                d = {
                    "value": self._selected_item.value,
                    "use_reg": self._selected_item.use_reg,
                    "hide": self._selected_item.hide,
                    "auto_ng_id": self._selected_item.auto_ng_id,
                    "board": self._selected_item.board,
                    "key": self._selected_item.key
                }

                self._scene.add_effect(NGEditor(self._screen, d,
                                                lambda d: self._data_context.update_ng(self._selected_item.id, d),
                                                "name"))
            elif isinstance(self._selected_item, NGWord):
                d = {
                    "value": self._selected_item.value,
                    "use_reg": self._selected_item.use_reg,
                    "hide": self._selected_item.hide,
                    "auto_ng_id": self._selected_item.auto_ng_id,
                    "board": self._selected_item.board,
                    "key": self._selected_item.key
                }

                self._scene.add_effect(NGEditor(self._screen, d,
                                                lambda d: self._data_context.update_ng(self._selected_item.id, d),
                                                "word"))
            elif isinstance(self._selected_item, NGId):
                d = {
                    "value": self._selected_item.value,
                    "use_reg": self._selected_item.use_reg,
                    "hide": self._selected_item.hide,
                    "board": self._selected_item.board,
                    "key": self._selected_item.key
                }

                self._scene.add_effect(NGEditor(self._screen, d,
                                                lambda d: self._data_context.update_ng(self._selected_item.id, d),
                                                "id"))
            elif isinstance(self._selected_item, NGTitle):
                d = {}
                d["value"] = self._selected_item.value
                d["use_reg"] = self._selected_item.use_reg
                d["board"] = self._selected_item.board

                self._scene.add_effect(NGEditor(self._screen, d,
                                                lambda d: self._data_context.update_ng(self._selected_item.id, d),
                                                "title"))


def _to_options(from_: List[NGItem]):
    result = []

    for i, item in enumerate(from_):
        result.append((item.value.split("\n")[0], i))

    return result
