from asciimatics.widgets import Frame, ListBox, Widget, Layout, VerticalDivider, Divider, Text, Label
from asciimatics.screen import Screen
from typing import List

from gochan.view_models import NGViewModel
from gochan.models.ng import NGItem
from gochan.effects import NGForm


class NGView(Frame):
    def __init__(self, screen: Screen, data_context: NGViewModel):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         has_border=False,
                         hover_focus=True,
                         can_scroll=False,
                         )

        self.set_theme("user_theme")

        self._data_context = data_context

        self._kind_list = ListBox(4,
                                  [("Title", 0), ("Name", 1), ("Id", 2), ("Word", 3)],
                                  name="kind_list",
                                  on_change=self._on_pick_kind)
        self._ng_list = ListBox(Widget.FILL_COLUMN, [], name="ng_list", add_scroll_bar=True,
                                on_change=self._on_pick_ng, on_select=self._on_select_ng)
        self._scope_label = Label("")
        self._use_reg_label = Label("")
        self._hide_label = Label("")

        self._form = None

        layout = Layout([20, 1, 79], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._kind_list, 0)
        layout.add_widget(Divider(), 0)
        layout.add_widget(self._scope_label, 0)
        layout.add_widget(self._use_reg_label, 0)
        layout.add_widget(self._hide_label, 0)
        layout.add_widget(VerticalDivider(), 1)
        layout.add_widget(self._ng_list, 2)
        self.fix()

    def _on_pick_kind(self):
        self.save()
        idx = self.data.get("kind_list")

        if idx == 0:
            self._ng_list.options = _to_options(self._data_context.config.titles)
        elif idx == 1:
            self._ng_list.options = _to_options(self._data_context.config.names)
        elif idx == 2:
            self._ng_list.options = _to_options(self._data_context.config.ids)
        elif idx == 3:
            self._ng_list.options = _to_options(self._data_context.config.words)

        self._on_pick_ng()

    def _on_pick_ng(self):
        self.save()
        idx1 = self.data.get("kind_list")
        idx2 = self.data.get("ng_list")

        if idx1 is None or idx2 is None:
            self._scope_label.text = ""
            self._use_reg_label.text = ""
            self._hide_label.text = ""
            return

        if idx1 == 0:
            self._scope_label.text = "scope: " + self._data_context.config.titles[idx2].scope
            self._use_reg_label.text = "use_reg: " + str(self._data_context.config.titles[idx2].use_reg)
            self._hide_label.text = "hide: " + str(self._data_context.config.titles[idx2].hide)
        elif idx1 == 1:
            self._scope_label.text = "scope: " + self._data_context.config.names[idx2].scope
            self._use_reg_label.text = "use_reg: " + str(self._data_context.config.names[idx2].use_reg)
            self._hide_label.text = "hide: " + str(self._data_context.config.names[idx2].hide)
        elif idx1 == 2:
            self._scope_label.text = "scope: " + self._data_context.config.ids[idx2].scope
            self._use_reg_label.text = "use_reg: " + str(self._data_context.config.ids[idx2].use_reg)
            self._hide_label.text = "hide: " + str(self._data_context.config.ids[idx2].hide)
        elif idx1 == 3:
            self._scope_label.text = "scope: " + self._data_context.config.words[idx2].scope
            self._use_reg_label.text = "use_reg: " + str(self._data_context.config.words[idx2].use_reg)
            self._hide_label.text = "hide: " + str(self._data_context.config.words[idx2].hide)

    def _on_select_ng(self):
        self.save()
        idx1 = self.data.get("kind_list")
        idx2 = self.data.get("ng_list")

        if idx1 is None or idx2 is None:
            return

        self._form = NGForm(self.screen, self._form_closed)
        self._scene.add_effect(self._form)

    def _form_closed(self, scope, kind, use_reg, hide, value):
        pass


def _to_options(from_: List[NGItem]):
    result = []

    for i, item in enumerate(from_):
        result.append((item.value, i))

    return result
