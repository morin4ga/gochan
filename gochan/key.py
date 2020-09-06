import re
from typing import Union

from asciimatics.event import KeyboardEvent
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, Text


class KeyLogger(Frame):
    def __init__(self, screen: Screen):
        super().__init__(screen,
                         screen.height,
                         screen.width,
                         hover_focus=True,
                         can_scroll=False,
                         has_border=True
                         )

        self._text = Text()

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._text)

        self.fix()

    def process_event(self, event):
        if isinstance(event, KeyboardEvent):
            self._text.value = str(event.key_code)

        return None


class Key:
    def __init__(self, value: int, representation: str) -> None:
        self.value = value
        self.representation = representation


class Shift:
    A = Key(ord('A'), "Shift-A")
    B = Key(ord('B'), "Shift-B")
    C = Key(ord('C'), "Shift-C")
    D = Key(ord('D'), "Shift-D")
    E = Key(ord('E'), "Shift-E")
    F = Key(ord('F'), "Shift-F")
    G = Key(ord('G'), "Shift-G")
    H = Key(ord('H'), "Shift-H")
    I = Key(ord('I'), "Shift-I")  # noqa: E741
    J = Key(ord('J'), "Shift-J")
    K = Key(ord('K'), "Shift-K")
    L = Key(ord('L'), "Shift-L")
    M = Key(ord('M'), "Shift-M")
    N = Key(ord('N'), "Shift-N")
    O = Key(ord('O'), "Shift-O")  # noqa: E741
    P = Key(ord('P'), "Shift-P")
    Q = Key(ord('Q'), "Shift-Q")
    R = Key(ord('R'), "Shift-R")
    S = Key(ord('S'), "Shift-S")
    T = Key(ord('T'), "Shift-T")
    U = Key(ord('U'), "Shift-U")
    V = Key(ord('V'), "Shift-V")
    W = Key(ord('W'), "Shift-W")
    X = Key(ord('X'), "Shift-X")
    Y = Key(ord('Y'), "Shift-Y")
    Z = Key(ord('Z'), "Shift-Z")


class CtrlShift:
    A = Key(Screen.ctrl('A'), "Ctrl-Shift-A")
    B = Key(Screen.ctrl('B'), "Ctrl-Shift-B")
    C = Key(Screen.ctrl('C'), "Ctrl-Shift-C")
    D = Key(Screen.ctrl('D'), "Ctrl-Shift-D")
    E = Key(Screen.ctrl('D'), "Ctrl-Shift-D")
    F = Key(Screen.ctrl('F'), "Ctrl-Shift-F")
    G = Key(Screen.ctrl('G'), "Ctrl-Shift-G")
    H = Key(Screen.ctrl('H'), "Ctrl-Shift-H")
    I = Key(Screen.ctrl('I'), "Ctrl-Shift-I")  # noqa: E741
    J = Key(Screen.ctrl('J'), "Ctrl-Shift-J")
    K = Key(Screen.ctrl('K'), "Ctrl-Shift-K")
    L = Key(Screen.ctrl('L'), "Ctrl-Shift-L")
    M = Key(Screen.ctrl('M'), "Ctrl-Shift-M")
    N = Key(Screen.ctrl('N'), "Ctrl-Shift-N")
    O = Key(Screen.ctrl('O'), "Ctrl-Shift-O")  # noqa: E741
    P = Key(Screen.ctrl('P'), "Ctrl-Shift-P")
    Q = Key(Screen.ctrl('Q'), "Ctrl-Shift-Q")
    R = Key(Screen.ctrl('R'), "Ctrl-Shift-R")
    S = Key(Screen.ctrl('S'), "Ctrl-Shift-S")
    T = Key(Screen.ctrl('T'), "Ctrl-Shift-T")
    U = Key(Screen.ctrl('U'), "Ctrl-Shift-U")
    V = Key(Screen.ctrl('V'), "Ctrl-Shift-V")
    W = Key(Screen.ctrl('W'), "Ctrl-Shift-W")
    X = Key(Screen.ctrl('X'), "Ctrl-Shift-X")
    Y = Key(Screen.ctrl('Y'), "Ctrl-Shift-Y")
    Z = Key(Screen.ctrl('Z'), "Ctrl-Shift-Z")


class Ctrl:
    HOME = Key(535, "Ctrl-HOME")
    END = Key(530, "Ctrl-END")
    LEFT = Key(545, "Ctrl-LEFT")
    UP = Key(566, "Ctrl-UP")
    RIGHT = Key(560, "Ctrl-RIGHT")
    DOWN = Key(525, "Ctrl-DOWN")

    A = Key(Screen.ctrl('a'), "Ctrl-A")
    B = Key(Screen.ctrl('b'), "Ctrl-B")
    C = Key(Screen.ctrl('c'), "Ctrl-C")
    D = Key(Screen.ctrl('d'), "Ctrl-D")
    E = Key(Screen.ctrl('e'), "Ctrl-E")
    F = Key(Screen.ctrl('f'), "Ctrl-F")
    G = Key(Screen.ctrl('g'), "Ctrl-G")
    H = Key(Screen.ctrl('h'), "Ctrl-H")
    I = Key(Screen.ctrl('i'), "Ctrl-I")  # noqa: E741
    J = Key(Screen.ctrl('j'), "Ctrl-J")
    K = Key(Screen.ctrl('k'), "Ctrl-K")
    L = Key(Screen.ctrl('l'), "Ctrl-L")
    M = Key(Screen.ctrl('m'), "Ctrl-M")
    N = Key(Screen.ctrl('n'), "Ctrl-N")
    O = Key(Screen.ctrl('o'), "Ctrl-O")  # noqa: E741
    P = Key(Screen.ctrl('p'), "Ctrl-P")
    Q = Key(Screen.ctrl('q'), "Ctrl-Q")
    R = Key(Screen.ctrl('r'), "Ctrl-R")
    S = Key(Screen.ctrl('s'), "Ctrl-S")
    T = Key(Screen.ctrl('t'), "Ctrl-T")
    U = Key(Screen.ctrl('u'), "Ctrl-U")
    V = Key(Screen.ctrl('v'), "Ctrl-V")
    W = Key(Screen.ctrl('w'), "Ctrl-W")
    X = Key(Screen.ctrl('x'), "Ctrl-X")
    Y = Key(Screen.ctrl('y'), "Ctrl-Y")
    Z = Key(Screen.ctrl('z'), "Ctrl-Z")

    Shift = CtrlShift


class Keys:
    ENTER = Key(10, "ENTER")

    # Standard extended key codes.
    ESCAPE = Key(-1, "ESCAPE")
    F1 = Key(-2, "F1")
    F2 = Key(-3, "F2")
    F3 = Key(-4, "F3")
    F4 = Key(-5, "F4")
    F5 = Key(-6, "F5")
    F6 = Key(-7, "F6")
    F7 = Key(-8, "F7")
    F8 = Key(-9, "F8")
    F9 = Key(-10, "F9")
    F10 = Key(-11, "F10")
    F11 = Key(-12, "F11")
    F12 = Key(-13, "F12")
    F13 = Key(-14, "F13")
    F14 = Key(-15, "F14")
    F15 = Key(-16, "F15")
    F16 = Key(-17, "F16")
    F17 = Key(-18, "F17")
    F18 = Key(-19, "F18")
    F19 = Key(-20, "F19")
    F20 = Key(-21, "F20")
    F21 = Key(-22, "F21")
    F22 = Key(-23, "F22")
    F23 = Key(-24, "F23")
    F24 = Key(-25, "F24")
    PRINT_SCREEN = Key(-100, "PRINT_SCREEN")
    INSERT = Key(-101, "INSERT")
    DELETE = Key(-102, "DELETE")
    HOME = Key(-200, "HOME")
    END = Key(-201, "END")
    LEFT = Key(-203, "LEFT")
    UP = Key(-204, "UP")
    RIGHT = Key(-205, "RIGHT")
    DOWN = Key(-206, "DOWN")
    PAGE_UP = Key(-207, "PAGE_UP")
    PAGE_DOWN = Key(-208, "PAGE_DOWN")
    BACK = Key(-300, "BACK")
    TAB = Key(-301, "TAB")
    BACK_TAB = Key(-302, "BACK_TAB")
    NUMPAD0 = Key(-400, "NUMPAD0")
    NUMPAD1 = Key(-401, "NUMPAD1")
    NUMPAD2 = Key(-402, "NUMPAD2")
    NUMPAD3 = Key(-403, "NUMPAD3")
    NUMPAD4 = Key(-404, "NUMPAD4")
    NUMPAD5 = Key(-405, "NUMPAD5")
    NUMPAD6 = Key(-406, "NUMPAD6")
    NUMPAD7 = Key(-407, "NUMPAD7")
    NUMPAD8 = Key(-408, "NUMPAD8")
    NUMPAD9 = Key(-409, "NUMPAD9")
    MULTIPLY = Key(-410, "MULTIPLY")
    ADD = Key(-411, "ADD")
    SUBTRACT = Key(-412, "SUBTRACT")
    DECIMAL = Key(-413, "DECIMAL")
    DIVIDE = Key(-414, "DIVIDE")
    CAPS_LOCK = Key(-500, "CAPS_LOCK")
    NUM_LOCK = Key(-501, "NUM_LOCK")
    SCROLL_LOCK = Key(-502, "SCROLL_LOCK")
    SHIFT = Key(-600, "SHIFT")
    CONTROL = Key(-601, "CONTROL")
    MENU = Key(-602, "MENU")

    A = Key(ord('a'), "A")
    B = Key(ord('b'), "B")
    C = Key(ord('c'), "C")
    D = Key(ord('d'), "D")
    E = Key(ord('e'), "E")
    F = Key(ord('f'), "F")
    G = Key(ord('g'), "G")
    H = Key(ord('h'), "H")
    I = Key(ord('i'), "I")  # noqa: E741
    J = Key(ord('j'), "J")
    K = Key(ord('k'), "K")
    L = Key(ord('l'), "L")
    M = Key(ord('m'), "M")
    N = Key(ord('n'), "N")
    O = Key(ord('o'), "O")  # noqa: E741
    P = Key(ord('p'), "P")
    Q = Key(ord('q'), "Q")
    R = Key(ord('r'), "R")
    S = Key(ord('s'), "S")
    T = Key(ord('t'), "T")
    U = Key(ord('u'), "U")
    V = Key(ord('v'), "V")
    W = Key(ord('w'), "W")
    X = Key(ord('x'), "X")
    Y = Key(ord('y'), "Y")
    Z = Key(ord('z'), "Z")
    N1 = Key(ord('1'), "1")
    N2 = Key(ord('2'), "2")
    N3 = Key(ord('3'), "3")
    N4 = Key(ord('4'), "4")
    N5 = Key(ord('5'), "5")
    N6 = Key(ord('6'), "6")
    N7 = Key(ord('7'), "7")
    N8 = Key(ord('8'), "8")
    N9 = Key(ord('9'), "9")
    N0 = Key(ord('0'), "0")

    Shift = Shift
    Ctrl = Ctrl


def _parse_key_with_ctrlshift(key: str) -> Union[Key, None]:
    return getattr(CtrlShift, key, None)


def _parse_key_with_ctrl(key: str) -> Union[Key, None]:
    if re.match(r'(S|SHIFT)-', key):
        return _parse_key_with_ctrlshift(re.sub(r'(S|SHIFT)-', "", key))

    return getattr(Ctrl, key, None)


def _parse_key_with_shift(key: str) -> Union[Key, None]:
    if re.match(r'(C|CTRL)-', key):
        return _parse_key_with_ctrlshift(re.sub(r'(C|CTRL)-', "", key))

    return getattr(Shift, key, None)


def parse_key(key: str) -> Union[Key, None]:
    key = key.upper()

    if re.match(r'(C|CTRL)-', key):
        return _parse_key_with_ctrl(re.sub(r'(C|CTRL)-', "", key))

    if re.match(r'(S|SHIFT)-', key):
        return _parse_key_with_shift(re.sub(r'(S|SHIFT)-', "", key))

    return getattr(Keys, key, None)
