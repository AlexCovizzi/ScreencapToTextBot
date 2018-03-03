import azureocr

LINES = [{"text":"fake1", "top":10, "left":25, "w":32, "h":32},
        {"text":"fake2", "top":24, "left":25, "w":32, "h":32},
        {"text":"fake3", "top":86, "left":25, "w":32, "h":32},
        {"text":"fake4", "top":97, "left":25, "w":32, "h":32},
        {"text":"fake5", "top":2, "left":25, "w":32, "h":32},
        {"text":"fake6", "top":34, "left":25, "w":32, "h":32},
        {"text":"fake7", "top":7, "left":25, "w":32, "h":32}]

EXPECTED = [
    {"text":"fake5", "top":2, "left":25, "w":32, "h":32},
    {"text":"fake7", "top":7, "left":25, "w":32, "h":32},
    {"text":"fake1", "top":10, "left":25, "w":32, "h":32},
    {"text":"fake2", "top":24, "left":25, "w":32, "h":32},
    {"text":"fake6", "top":34, "left":25, "w":32, "h":32},
    {"text":"fake3", "top":86, "left":25, "w":32, "h":32},
    {"text":"fake4", "top":97, "left":25, "w":32, "h":32}
    ]

def test_sortLinesByY(lines):
    result = azureocr.sortLinesByY(lines)
    if result == EXPECTED:
        print("sortLinesByY: success")
    else:
        print("sortLinesByY: failed")

test_sortLinesByY(LINES)