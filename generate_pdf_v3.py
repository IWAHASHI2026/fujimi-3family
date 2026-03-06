"""富士見会 企画書 PDF生成スクリプト (v3: 思い出の写真ページ追加)"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# フォント登録 (Windows system fonts)
pdfmetrics.registerFont(TTFont('YuMincho', 'C:/Windows/Fonts/yumin.ttf'))
pdfmetrics.registerFont(TTFont('YuMinchoBold', 'C:/Windows/Fonts/yumindb.ttf'))
pdfmetrics.registerFont(TTFont('Meiryo', 'C:/Windows/Fonts/meiryo.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('MeiryoBold', 'C:/Windows/Fonts/meiryob.ttc', subfontIndex=0))

SERIF = 'YuMincho'
SERIF_BOLD = 'YuMinchoBold'
SANS = 'Meiryo'
SANS_BOLD = 'MeiryoBold'

# カラー定義
NAVY = HexColor('#1a2744')
NAVY_LIGHT = HexColor('#2a3f6a')
GOLD = HexColor('#b8964e')
GOLD_LIGHT = HexColor('#d4b97a')
CREAM = HexColor('#faf6ef')
WARM_GRAY = HexColor('#6b6560')
TEXT_COLOR = HexColor('#2d2926')
WHITE = HexColor('#ffffff')
LIGHT_BORDER = HexColor('#dddddd')
CONFIRMED_BG = HexColor('#e8f5e9')
CONFIRMED_FG = HexColor('#2e7d32')
PENDING_BG = HexColor('#fff3e0')
PENDING_FG = HexColor('#e65100')

W, H = A4  # 595.28 x 841.89


def draw_photo_clipped(c, img_path, x, y, w, h):
    """写真を指定領域にクリップして描画（中央トリミング）"""
    img = Image.open(img_path)
    iw, ih = img.size

    scale = max(w / iw, h / ih)
    crop_w = w / scale
    crop_h = h / scale
    cx = (iw - crop_w) / 2
    cy = (ih - crop_h) / 2
    cropped = img.crop((int(cx), int(cy), int(cx + crop_w), int(cy + crop_h)))

    c.drawImage(ImageReader(cropped), x, y, w, h)


def draw_cover(c):
    """表紙ページ"""
    margin = 30

    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    footer_h = 30
    c.setFillColor(NAVY)
    c.rect(0, 0, W, footer_h, fill=1, stroke=0)
    c.setFillColor(GOLD_LIGHT)
    c.setFont(SANS, 7)
    c.drawCentredString(W / 2, footer_h / 2 - 3, '鈴木家  ·  渡辺家  ·  岩橋家')

    photo_top = H - margin
    photo_h = H * 0.35
    photo_bottom = photo_top - photo_h

    draw_photo_clipped(c, os.path.join(BASE_DIR, 'main.jpg'),
                       margin, photo_bottom, W - margin * 2, photo_h)

    c.saveState()
    cap_text = '富士見ヶ丘幼稚園'
    cap_w = pdfmetrics.stringWidth(cap_text, SANS, 6.5) + 12
    c.setFillColorRGB(0.1, 0.15, 0.27, alpha=0.6)
    c.rect(W - margin - cap_w - 4, photo_bottom + 4, cap_w + 4, 14, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(SANS, 6.5)
    c.drawRightString(W - margin - 8, photo_bottom + 8, cap_text)
    c.restoreState()

    title_area_top = photo_bottom - 18
    title_cy = title_area_top - 75

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(W / 2 - 80, title_area_top - 2, W / 2 + 80, title_area_top - 2)

    c.setFillColor(GOLD)
    c.setFont(SANS, 7.5)
    c.drawCentredString(W / 2, title_cy + 58, '企 画 書 兼 ご 案 内')

    c.setFillColor(NAVY)
    c.setFont(SERIF_BOLD, 50)
    c.drawCentredString(W / 2, title_cy - 2, '富 士 見 会')

    c.setFillColor(WARM_GRAY)
    c.setFont(SERIF, 11.5)
    c.drawCentredString(W / 2, title_cy - 30, '— 数十年の時を越えて —')

    info_y = title_cy - 62
    c.setFillColor(NAVY)
    c.setFont(SANS_BOLD, 11)
    c.drawCentredString(W / 2, info_y, '2026年 7月 11日（土）  13:00〜')

    c.setFillColor(WARM_GRAY)
    c.setFont(SANS, 9)
    c.drawCentredString(W / 2, info_y - 18, '会場：きじま 戸塚本陣')

    line_y = info_y - 36
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(W / 2 - 80, line_y, W / 2 + 80, line_y)

    strip_top = line_y - 14
    strip_bottom = footer_h + 30
    strip_h = strip_top - strip_bottom
    strip_y = strip_bottom
    gap = 6
    strip_w = (W - margin * 2 - gap * 2) / 3

    photos = ['sub4.jpeg', 'sub2.jpeg', 'sub1.jpeg']
    for i, photo in enumerate(photos):
        px = margin + i * (strip_w + gap)
        draw_photo_clipped(c, os.path.join(BASE_DIR, photo),
                           px, strip_y, strip_w, strip_h)

    c.setFillColor(WARM_GRAY)
    c.setFont(SANS, 6.5)
    c.drawCentredString(W / 2, strip_y - 12,
                        '富士見ヶ丘幼稚園の幼なじみ  —  3家族の再会')

    c.showPage()


def section_header(c, y, number, label, title):
    """セクションヘッダーを描画し、更新後のy座標を返す"""
    c.setFillColor(HexColor('#b8964e1f'))
    c.setFont(SERIF, 48)
    c.drawString(40, y, number)

    c.setFillColor(GOLD)
    c.setFont(SANS, 7)
    c.drawString(40, y - 22, label)

    c.setFillColor(NAVY)
    c.setFont(SERIF_BOLD, 20)
    c.drawString(40, y - 48, title)

    return y - 70


def draw_page2(c):
    """趣旨・日時・会場"""
    y = H - 50

    y = section_header(c, y, '01', 'ABOUT', '趣旨')
    y -= 10

    c.setFillColor(TEXT_COLOR)
    c.setFont(SERIF, 12)
    lines = [
        'かつて富士見ヶ丘幼稚園に通い、',
        '近所で共に育った3つの家族。',
        '',
        '数十年の歳月を経て、',
        '幼なじみとその家族、子どもたちが',
        '一堂に会し、親睦を深める——',
        'それが「富士見会」です。',
    ]
    for line in lines:
        if line == '':
            y -= 10
            continue
        c.drawCentredString(W / 2, y, line)
        y -= 22

    y -= 20

    c.setStrokeColor(LIGHT_BORDER)
    c.setLineWidth(0.5)
    c.line(40, y, W - 40, y)
    y -= 30

    bar_h = 110
    c.setFillColor(NAVY)
    c.rect(0, y - bar_h + 20, W, bar_h, fill=1, stroke=0)

    bar_cy = y - bar_h / 2 + 20

    c.setFillColor(GOLD_LIGHT)
    c.setFont(SANS, 7)
    c.drawCentredString(W / 2, bar_cy + 38, 'DATE & TIME')

    c.setFillColor(WHITE)
    c.setFont(SERIF_BOLD, 16)
    c.drawCentredString(W / 2, bar_cy + 15, '日時')

    c.setFillColor(HexColor('#ffffffcc'))
    c.setFont(SANS, 12)
    c.drawCentredString(W / 2, bar_cy - 8, '2026年 7月 11日（土）')

    c.setFillColor(GOLD_LIGHT)
    c.setFont(SERIF_BOLD, 28)
    c.drawCentredString(W / 2, bar_cy - 38, '13:00〜')

    y = y - bar_h - 10

    c.setStrokeColor(LIGHT_BORDER)
    c.line(40, y, W - 40, y)
    y -= 30

    y = section_header(c, y, '02', 'VENUE', '会場')
    y -= 5

    card_h = 120
    c.setFillColor(CREAM)
    c.roundRect(35, y - card_h, W - 70, card_h, 3, fill=1, stroke=0)

    cx = 55
    cy_start = y - 20

    c.setFillColor(NAVY)
    c.setFont(SERIF_BOLD, 18)
    c.drawString(cx, cy_start, 'きじま')

    c.setFillColor(WARM_GRAY)
    c.setFont(SANS, 9)
    c.drawString(cx, cy_start - 18, '戸塚本陣')

    c.setFillColor(TEXT_COLOR)
    c.setFont(SANS, 9)
    c.drawString(cx, cy_start - 45, '和の趣あふれる個室空間で')
    c.drawString(cx, cy_start - 60, 'ゆったりとお食事をお楽しみいただけます')

    c.setFillColor(WARM_GRAY)
    c.setFont(SANS, 8)
    c.drawString(cx, cy_start - 85, 'https://kijimagroup.co.jp/store/totsuka_honjin/')

    y = y - card_h - 15

    c.setFillColor(WARM_GRAY)
    c.setFont(SANS, 7)
    c.drawCentredString(W / 2, y, '※ 終了時刻は会場・進行により調整')

    c.showPage()


def draw_memories_page(c):
    """思い出の写真ページ"""
    margin = 30
    y = H - 45

    # ページ背景
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # セクションヘッダー（中央揃え）
    c.setFillColor(HexColor('#b8964e1f'))
    c.setFont(SERIF, 48)
    c.drawCentredString(W / 2, y, '02')

    c.setFillColor(GOLD)
    c.setFont(SANS, 7)
    c.drawCentredString(W / 2, y - 22, 'MEMORIES')

    c.setFillColor(NAVY)
    c.setFont(SERIF_BOLD, 20)
    c.drawCentredString(W / 2, y - 48, '思い出の写真')

    y -= 75

    # イントロテキスト
    c.setFillColor(WARM_GRAY)
    c.setFont(SERIF, 10)
    c.drawCentredString(W / 2, y, 'あの頃のわたしたち。富士見ヶ丘で一緒に駆け回った日々。')
    y -= 30

    # 写真レイアウト
    # Row 1: 大きい写真1枚（左4:右2の比率） + 中写真1枚
    gap = 8
    content_w = W - margin * 2

    # Row 1: IMG_2403 (大) + IMG_2399 (中)
    row1_h = 180
    large_w = content_w * 0.62
    medium_w = content_w - large_w - gap

    draw_photo_clipped(c, os.path.join(BASE_DIR, 'IMG_2403.JPG'),
                       margin, y - row1_h, large_w, row1_h)
    draw_photo_clipped(c, os.path.join(BASE_DIR, 'IMG_2399.JPG'),
                       margin + large_w + gap, y - row1_h, medium_w, row1_h)

    y -= row1_h + gap

    # Row 2: IMG_2400 (左半分) + IMG_2401 (右半分)
    row2_h = 165
    half_w = (content_w - gap) / 2

    draw_photo_clipped(c, os.path.join(BASE_DIR, 'IMG_2400.JPG'),
                       margin, y - row2_h, half_w, row2_h)
    draw_photo_clipped(c, os.path.join(BASE_DIR, 'IMG_2401.JPG'),
                       margin + half_w + gap, y - row2_h, half_w, row2_h)

    y -= row2_h + gap

    # Row 3: IMG_2402 (全幅ワイド)
    row3_h = 150
    draw_photo_clipped(c, os.path.join(BASE_DIR, 'IMG_2402.JPG'),
                       margin, y - row3_h, content_w, row3_h)

    y -= row3_h + 20

    # フッターテキスト
    c.setFillColor(WARM_GRAY)
    c.setFont(SERIF, 9)
    c.drawCentredString(W / 2, y, '— あの日の笑顔を、もう一度 —')

    c.showPage()


def draw_badge(c, x, y, text, bg_color, fg_color):
    """小さなバッジを描画"""
    tw = pdfmetrics.stringWidth(text, SANS, 6) + 6
    c.setFillColor(bg_color)
    c.roundRect(x, y - 2, tw, 11, 2, fill=1, stroke=0)
    c.setFillColor(fg_color)
    c.setFont(SANS, 6)
    c.drawString(x + 3, y + 1, text)
    return tw + 3


def draw_family_card(c, x, y, w, h, name_jp, name_en, members, accent_color):
    """家族カードを描画"""
    c.setFillColor(WHITE)
    c.setStrokeColor(LIGHT_BORDER)
    c.setLineWidth(0.5)
    c.rect(x, y, w, h, fill=1, stroke=1)

    c.setFillColor(accent_color)
    c.rect(x, y + h - 3, w, 3, fill=1, stroke=0)

    cy = y + h - 25
    c.setFillColor(NAVY)
    c.setFont(SERIF_BOLD, 14)
    c.drawString(x + 15, cy, name_jp)
    c.setFillColor(WARM_GRAY)
    c.setFont(SANS, 7)
    c.drawString(x + 15, cy - 14, name_en)

    cy -= 35

    c.setFillColor(GOLD)
    c.setFont(SANS, 6)
    c.drawString(x + 15, cy, '幼なじみ')
    cy -= 16

    for name, role in members:
        c.setFillColor(GOLD_LIGHT)
        c.circle(x + 19, cy + 3, 2, fill=1, stroke=0)
        c.setFillColor(TEXT_COLOR)
        c.setFont(SANS, 9)
        c.drawString(x + 27, cy, name)
        bx = x + 27 + pdfmetrics.stringWidth(name, SANS, 9) + 5
        draw_badge(c, bx, cy, role, HexColor('#f3f0ff'), HexColor('#5e35b1'))
        bx += pdfmetrics.stringWidth(role, SANS, 6) + 12
        draw_badge(c, bx, cy, '出席確定', CONFIRMED_BG, CONFIRMED_FG)
        cy -= 18


def draw_page3(c):
    """メンバー紹介"""
    y = H - 50

    y = section_header(c, y, '03', 'MEMBERS', '幼なじみメンバー')
    y -= 5

    c.setFillColor(WARM_GRAY)
    c.setFont(SANS, 9)
    c.drawString(40, y, '富士見ヶ丘幼稚園で共に過ごした6名。全員の出席が決定しています。')
    y -= 30

    card_w = (W - 80 - 20) / 3
    card_h = 150

    families = [
        ('鈴木家', 'Suzuki Family', [('鈴木 直', '長男'), ('鈴木 圭', '弟')], NAVY),
        ('渡辺家', 'Watanabe Family', [('渡辺 哲也', '長男'), ('渡辺 のりこ', '妹')], GOLD),
        ('岩橋家', 'Iwahashi Family', [('岩橋 成信', '長男'), ('岩橋 幸正', '弟')], HexColor('#c27c7c')),
    ]

    for i, (name_jp, name_en, members, color) in enumerate(families):
        fx = 40 + i * (card_w + 10)
        draw_family_card(c, fx, y - card_h, card_w, card_h, name_jp, name_en, members, color)

    y = y - card_h - 40

    c.setStrokeColor(LIGHT_BORDER)
    c.setLineWidth(0.5)
    c.line(40, y, W - 40, y)
    y -= 30

    # === 04 ご家族 (v2: 役職ラベル削除、奥様表記) ===
    y = section_header(c, y, '04', 'GUESTS', 'ご家族のご参加（出欠未定）')
    y -= 5

    c.setFillColor(WARM_GRAY)
    c.setFont(SANS, 9)
    c.drawString(40, y, '親世代・家族世代のみなさまにもお声がけしております。')
    y -= 30

    guests_data = [
        ('鈴木家', [
            ('親世代', ['ふじ子さん']),
            ('直さんご家族', ['奥様', '子ども 3名（大学生1・高校生2）']),
            ('圭さんご家族', ['奥様']),
        ]),
        ('渡辺家', [
            ('親世代', ['喜夫さん', '鈴子さん']),
            ('哲也さんご家族', ['奥様', '子ども 1名']),
        ]),
        ('岩橋家', [
            ('親世代', ['重人さん', '百合子さん']),
            ('成信さんご家族', ['加名子さん', '子ども 3名（大学生2・高校生1）']),
            ('幸正さんご家族', ['桑子さん', '子ども 1名（中学生）']),
        ]),
    ]

    col_w = (W - 80 - 20) / 3

    for i, (family, groups) in enumerate(guests_data):
        gx = 40 + i * (col_w + 10)
        gy = y

        c.setFillColor(NAVY)
        c.setFont(SERIF, 11)
        c.drawString(gx, gy, family)
        bx = gx + pdfmetrics.stringWidth(family, SERIF, 11) + 6
        draw_badge(c, bx, gy, '未定', PENDING_BG, PENDING_FG)
        gy -= 20

        for group_label, members in groups:
            c.setFillColor(GOLD)
            c.setFont(SANS, 6)
            c.drawString(gx, gy, group_label)
            gy -= 14

            for member in members:
                c.setFillColor(WARM_GRAY)
                c.setFont(SANS, 8)
                c.drawString(gx + 8, gy, '— ' + member)
                gy -= 13

            gy -= 5

    c.showPage()


def draw_page4(c):
    """想い + フッター"""
    y = H - 80

    c.setFillColor(HexColor('#b8964e1f'))
    c.setFont(SERIF, 48)
    c.drawCentredString(W / 2, y, '05')

    c.setFillColor(GOLD)
    c.setFont(SANS, 7)
    c.drawCentredString(W / 2, y - 22, 'MESSAGE')

    c.setFillColor(NAVY)
    c.setFont(SERIF_BOLD, 20)
    c.drawCentredString(W / 2, y - 48, 'この会に込める想い')

    y -= 100

    c.setStrokeColor(GOLD_LIGHT)
    c.setLineWidth(0.5)
    c.line(W / 2 - 30, y + 10, W / 2 + 30, y + 10)

    y -= 30

    c.setFillColor(GOLD_LIGHT)
    c.setFont(SERIF, 36)
    c.drawString(W / 2 - 180, y + 30, '\u201c')
    c.drawString(W / 2 + 155, y - 85, '\u201d')

    c.setFillColor(NAVY)
    c.setFont(SERIF, 17)
    quote_lines = [
        '幼なじみとその家族、',
        '子どもたちが一斉に集い、',
        '世代を越えた親睦を図る',
    ]
    for line in quote_lines:
        c.drawCentredString(W / 2, y, line)
        y -= 30

    footer_h = 70
    c.setFillColor(NAVY)
    c.rect(0, 0, W, footer_h, fill=1, stroke=0)

    c.setFillColor(GOLD_LIGHT)
    c.setFont(SERIF, 13)
    c.drawCentredString(W / 2, footer_h - 25, '富 士 見 会')

    c.setFillColor(HexColor('#ffffff66'))
    c.setFont(SANS, 7)
    c.drawCentredString(W / 2, footer_h - 42, '2026年7月11日（土）  |  きじま 戸塚本陣')

    c.setFillColor(HexColor('#ffffff33'))
    c.setFont(SANS, 6)
    c.drawCentredString(W / 2, footer_h - 57, 'この企画書は関係者への案内用として作成されました')

    c.showPage()


def main():
    output = os.path.join(BASE_DIR, '富士見会_企画書_v3.pdf')
    c = canvas.Canvas(output, pagesize=A4)
    c.setTitle('富士見会 — 企画書兼ご案内')
    c.setAuthor('富士見会')

    draw_cover(c)        # P1: 表紙
    draw_page2(c)        # P2: 趣旨・日時・会場
    draw_memories_page(c)  # P3: 思い出の写真 (NEW)
    draw_page3(c)        # P4: メンバー・ご家族
    draw_page4(c)        # P5: 想い・フッター

    c.save()
    print(f'PDF生成完了: {output}')


if __name__ == '__main__':
    main()
