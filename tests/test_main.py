import sys
sys.path.append('./')
from main import handler


def test_main():
    event = {
        "text": "Kikusss",
        "style": None
    }
    handler(event, {})


if __name__ == "__main__":
    test_main()
