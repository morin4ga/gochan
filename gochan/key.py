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


class Shift:
    A = ord('A')
    B = ord('B')
    C = ord('C')
    D = ord('D')
    E = ord('E')
    F = ord('F')
    G = ord('G')
    H = ord('H')
    I = ord('I')
    J = ord('J')
    K = ord('K')
    L = ord('L')
    M = ord('M')
    N = ord('N')
    O = ord('O')
    P = ord('P')
    Q = ord('Q')
    R = ord('R')
    S = ord('S')
    T = ord('T')
    U = ord('U')
    V = ord('V')
    W = ord('W')
    X = ord('X')
    Y = ord('Y')
    Z = ord('Z')


class CtrlShift:
    A = Screen.ctrl('A')
    B = Screen.ctrl('B')
    C = Screen.ctrl('C')
    D = Screen.ctrl('D')
    E = Screen.ctrl('D')
    F = Screen.ctrl('F')
    G = Screen.ctrl('G')
    H = Screen.ctrl('H')
    I = Screen.ctrl('I')
    J = Screen.ctrl('J')
    K = Screen.ctrl('K')
    L = Screen.ctrl('L')
    M = Screen.ctrl('M')
    N = Screen.ctrl('N')
    O = Screen.ctrl('O')
    P = Screen.ctrl('P')
    Q = Screen.ctrl('Q')
    R = Screen.ctrl('R')
    S = Screen.ctrl('S')
    T = Screen.ctrl('T')
    U = Screen.ctrl('U')
    V = Screen.ctrl('V')
    W = Screen.ctrl('W')
    X = Screen.ctrl('X')
    Y = Screen.ctrl('Y')
    Z = Screen.ctrl('Z')


class Ctrl:
    HOME = 535
    END = 530
    LEFT = 545
    UP = 566
    RIGHT = 560
    DOWN = 525

    A = Screen.ctrl('a')
    B = Screen.ctrl('b')
    C = Screen.ctrl('c')
    D = Screen.ctrl('d')
    E = Screen.ctrl('e')
    F = Screen.ctrl('f')
    G = Screen.ctrl('g')
    H = Screen.ctrl('h')
    I = Screen.ctrl('i')
    J = Screen.ctrl('j')
    K = Screen.ctrl('k')
    L = Screen.ctrl('l')
    M = Screen.ctrl('m')
    N = Screen.ctrl('n')
    O = Screen.ctrl('o')
    P = Screen.ctrl('p')
    Q = Screen.ctrl('q')
    R = Screen.ctrl('r')
    S = Screen.ctrl('s')
    T = Screen.ctrl('t')
    U = Screen.ctrl('u')
    V = Screen.ctrl('v')
    W = Screen.ctrl('w')
    X = Screen.ctrl('x')
    Y = Screen.ctrl('y')
    Z = Screen.ctrl('z')

    Shift = CtrlShift


class Key:
    ENTER = 10

    # Standard extended key codes.
    ESCAPE = -1
    F1 = -2
    F2 = -3
    F3 = -4
    F4 = -5
    F5 = -6
    F6 = -7
    F7 = -8
    F8 = -9
    F9 = -10
    F10 = -11
    F11 = -12
    F12 = -13
    F13 = -14
    F14 = -15
    F15 = -16
    F16 = -17
    F17 = -18
    F18 = -19
    F19 = -20
    F20 = -21
    F21 = -22
    F22 = -23
    F23 = -24
    F24 = -25
    PRINT_SCREEN = -100
    INSERT = -101
    DELETE = -102
    HOME = -200
    END = -201
    LEFT = -203
    UP = -204
    RIGHT = -205
    DOWN = -206
    PAGE_UP = -207
    PAGE_DOWN = -208
    BACK = -300
    TAB = -301
    BACK_TAB = -302
    NUMPAD0 = -400
    NUMPAD1 = -401
    NUMPAD2 = -402
    NUMPAD3 = -403
    NUMPAD4 = -404
    NUMPAD5 = -405
    NUMPAD6 = -406
    NUMPAD7 = -407
    NUMPAD8 = -408
    NUMPAD9 = -409
    MULTIPLY = -410
    ADD = -411
    SUBTRACT = -412
    DECIMAL = -413
    DIVIDE = -414
    CAPS_LOCK = -500
    NUM_LOCK = -501
    SCROLL_LOCK = -502
    SHIFT = -600
    CONTROL = -601
    MENU = -602

    A = ord('a')
    B = ord('b')
    C = ord('c')
    D = ord('d')
    E = ord('e')
    F = ord('f')
    G = ord('g')
    H = ord('h')
    I = ord('i')
    J = ord('j')
    K = ord('k')
    L = ord('l')
    M = ord('m')
    N = ord('n')
    O = ord('o')
    P = ord('p')
    Q = ord('q')
    R = ord('r')
    S = ord('s')
    T = ord('t')
    U = ord('u')
    V = ord('v')
    W = ord('w')
    X = ord('x')
    Y = ord('y')
    Z = ord('z')

    Shift = Shift
    Ctrl = Ctrl


def _parse_key_with_ctrlshift(key: str) -> Union[int, None]:
    return getattr(CtrlShift, key, None)


def _parse_key_with_ctrl(key: str) -> Union[int, None]:
    if re.match(r'(S|SHIFT)-', key):
        return _parse_key_with_ctrlshift(re.sub(r'(S|SHIFT)-', "", key))

    return getattr(Ctrl, key, None)


def _parse_key_with_shift(key: str) -> Union[int, None]:
    if re.match(r'(C|CTRL)-', key):
        return _parse_key_with_ctrlshift(re.sub(r'(C|CTRL)-', "", key))

    return getattr(Shift, key, None)


def parse_key(key: str) -> Union[int, None]:
    key = key.upper()

    if re.match(r'(C|CTRL)-', key):
        return _parse_key_with_ctrl(re.sub(r'(C|CTRL)-', "", key))

    if re.match(r'(S|SHIFT)-', key):
        return _parse_key_with_shift(re.sub(r'(S|SHIFT)-', "", key))

    return getattr(Key, key, None)
