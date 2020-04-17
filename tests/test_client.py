from client import get_bbsmenu, get_board


def test_get_bbsmenu():
    bbs = get_bbsmenu()
    assert bbs.categories[0].name == '地震'


def test_get_board():
    board = get_board("hebi", "news4vip")

    for t in board.threads:
        print(t.server)
        print(t.board)
