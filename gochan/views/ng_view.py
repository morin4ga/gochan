from asciimatics.widgets import Frame, ListBox, Widget, Layout, VerticalDivider, Divider, Text, Label, PopUpDialog
from asciimatics.screen import Screen
from typing import List

from gochan.view_models import NGVM
from gochan.models.ng import NGItem
from gochan.effects import NGEditor


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

        self._data_context = data_context
        self._data_context.on_property_changed = self._context_changed

        self._selected_list = None
        self._selected_item = None

        self._kind_list = ListBox(4,
                                  [("Title", 0), ("Name", 1), ("Id", 2), ("Word", 3)],
                                  name="kind_list",
                                  on_change=self._on_pick_kind)
        self._ng_list = ListBox(Widget.FILL_COLUMN, [], name="ng_list", add_scroll_bar=True,
                                on_change=self._on_pick_ng, on_select=self._on_select_ng)
        self._board_label = Label("")
        self._key_label = Label("")
        self._use_reg_label = Label("")
        self._hide_label = Label("")

        self._form = None

        layout = Layout([20, 1, 79], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._kind_list, 0)
        layout.add_widget(Divider(), 0)
        layout.add_widget(self._board_label, 0)
        layout.add_widget(self._key_label, 0)
        layout.add_widget(self._use_reg_label, 0)
        layout.add_widget(self._hide_label, 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._ng_list, 2)
        self.fix()

    def _context_changed(self, property_name: str):
        self._selected_list = None
        self._selected_item = None
        self._kind_list.value = 0
        self._ng_list.value = None
        self.switch_focus(self._layouts[0], 0, 0)

    def _on_pick_kind(self):
        self.save()
        idx = self.data.get("kind_list")

        if idx == 0:
            self._selected_list = self._data_context.title_ngs
        elif idx == 1:
            self._selected_list = self._data_context.name_ngs
        elif idx == 2:
            self._selected_list = self._data_context.id_ngs
        elif idx == 3:
            self._selected_list = self._data_context.word_ngs

        if self._selected_list is not None:
            self._ng_list.options = _to_options(self._selected_list)

        self._on_pick_ng()

    def _on_pick_ng(self):
        self.save()
        idx = self.data.get("ng_list")

        if self._selected_list is None or idx is None:
            self._board_label.text = ""
            self._key_label.text = ""
            self._use_reg_label.text = ""
            self._hide_label.text = ""
            return

        self._selected_item = self._selected_list[idx]

        self._board_label.text = "board: " + \
            (self._selected_item.board if self._selected_item.board is not None else "")
        self._key_label.text = "key: " + (self._selected_item.key if self._selected_item.key is not None else "")
        self._use_reg_label.text = "use_reg: " + str(self._selected_item.use_reg)
        self._hide_label.text = "hide: " + str(self._selected_item.hide)

    def _on_select_ng(self):
        if self._selected_item is not None:
            def on_select_manipilation(idx):
                if idx == 0:
                    self._form = NGEditor(self.screen, self._selected_item,
                                          lambda values: self._data_context.update(self._selected_item.id, values))
                    self._scene.add_effect(self._form)
                elif idx == 1:
                    def on_close_del_dialog(idx):
                        if idx == 0:
                            self._data_context.delete(self._selected_item.id)

                    self._scene.add_effect(PopUpDialog(self._screen, "Really want to delete it?",
                                                       ["Delete", "Cancel"], on_close=on_close_del_dialog,
                                                       theme="user_theme"))

            self._scene.add_effect(PopUpDialog(self._screen, "Choose manipulation", [
                                   "Edit", "Delete", "Cancel"], on_close=on_select_manipilation, theme="user_theme"))


def _to_options(from_: List[NGItem]):
    result = []

    for i, item in enumerate(from_):
        result.append((item.value.split("\n")[0], i))

    return result
