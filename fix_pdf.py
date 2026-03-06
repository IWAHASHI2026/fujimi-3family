import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import fitz

src = "富士見会_企画書.pdf"
dst = "富士見会_企画書_v2.pdf"

doc = fitz.open(src)
page = doc[2]  # page 3

BODY_COLOR = fitz.sRGB_to_pdf(7038304)    # body text color
LABEL_COLOR = fitz.sRGB_to_pdf(12097102)   # group label color
WHITE = (1, 1, 1)
BODY_SIZE = 8.0
LABEL_SIZE = 6.0

# Use CJK font for Japanese text
FONT_CJK = "japan"  # PyMuPDF built-in CJK font

def whiteout(rect):
    """Draw a white rectangle over the given area"""
    r = fitz.Rect(rect)
    shape = page.new_shape()
    shape.draw_rect(r)
    shape.finish(color=WHITE, fill=WHITE)
    shape.commit()

def draw_text(x, y, text, size, color):
    """Insert text at given baseline position using insert_text"""
    # insert_text uses bottom-left of first char as reference
    rc = page.insert_text(
        (x, y + size),  # baseline position
        text,
        fontname=FONT_CJK,
        fontsize=size,
        color=color,
    )
    return rc

# === 鈴木家 replacements ===

# 1. ふじ子さん（母親） -> ふじ子さん
whiteout((48, 506, 48+83, 507+9))
draw_text(48, 507, "— ふじ子さん", BODY_SIZE, BODY_COLOR)

# 2. 妻 -> 奥様 (鈴木家 直さんご家族)
whiteout((48, 538, 48+19, 539+9))
draw_text(48, 539, "— 奥様", BODY_SIZE, BODY_COLOR)

# 3. Add 圭さんご家族 section after 子ども line (y=552+8=560)
draw_text(40, 571.7, "圭さんご家族", LABEL_SIZE, LABEL_COLOR)
draw_text(48, 584, "— 奥様", BODY_SIZE, BODY_COLOR)

# === 渡辺家 replacements ===

# 4. 妻 -> 奥様 (渡辺家 哲也さんご家族)
whiteout((223, 551, 223+19, 552+9))
draw_text(223.1, 552, "— 奥様", BODY_SIZE, BODY_COLOR)

# === 岩橋家 replacements ===

# 5. 重人さん（父親） -> 重人さん
whiteout((398, 506, 398+75, 507+9))
draw_text(398.2, 507, "— 重人さん", BODY_SIZE, BODY_COLOR)

# 6. 百合子さん（母親） -> 百合子さん
whiteout((398, 519, 398+83, 520+9))
draw_text(398.2, 520, "— 百合子さん", BODY_SIZE, BODY_COLOR)

# 7. 加名子さん（妻） -> 加名子さん
whiteout((398, 551, 398+75, 552+9))
draw_text(398.2, 552, "— 加名子さん", BODY_SIZE, BODY_COLOR)

# 8. 桑子さん（妻） -> 桑子さん
whiteout((398, 596, 398+67, 597+9))
draw_text(398.2, 597, "— 桑子さん", BODY_SIZE, BODY_COLOR)

doc.save(dst)
doc.close()
print(f"Saved to {dst}")
print("All replacements applied.")
