#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates the PDF report for BLM2512 Odev 2.
Usage: python3 generate_pdf.py <VIDEO_LINK>
"""

import sys
import subprocess
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Preformatted
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Fonts ────────────────────────────────────────────────────────────────────
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV",      FONT_DIR + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DV-Bold", FONT_DIR + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVMono",  FONT_DIR + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("DVMono-Bold", FONT_DIR + "DejaVuSansMono-Bold.ttf"))

# ── Colours ──────────────────────────────────────────────────────────────────
C_DARK   = colors.HexColor("#1a2b4a")
C_MID    = colors.HexColor("#2e5fa3")
C_LIGHT  = colors.HexColor("#e8f0fb")
C_MONO   = colors.HexColor("#f4f6f8")
C_BORDER = colors.HexColor("#c5d5ea")
C_WHITE  = colors.white

# ── Student data ─────────────────────────────────────────────────────────────
STUDENT_NAME   = "Omar Nuriyev"
STUDENT_NO     = "24011902"
COURSE         = "BLM2512 Veri Yapıları ve Algoritmalar"
GROUP          = "Gr. 3"
INSTRUCTOR     = "M. Elif Karslıgil"
SEMESTER       = "2025-2026 Bahar Yarıyılı"
ASSIGNMENT     = "Ödev 2 – Stack & Queue"
VIDEO_LINK     = sys.argv[1] if len(sys.argv) > 1 else "[VIDEO LİNKİNİ BURAYA EKLEYİN]"

# ── Style helpers ─────────────────────────────────────────────────────────────
def S(name, font="DV", size=10, leading=14, color=colors.black,
      align=TA_LEFT, spaceBefore=0, spaceAfter=4, leftIndent=0):
    return ParagraphStyle(
        name, fontName=font, fontSize=size, leading=leading,
        textColor=color, alignment=align,
        spaceBefore=spaceBefore, spaceAfter=spaceAfter,
        leftIndent=leftIndent
    )

sTitle    = S("Title",    "DV-Bold", 20, 26, C_WHITE,  TA_CENTER, 0, 6)
sSub      = S("Sub",      "DV",      11, 15, C_WHITE,  TA_CENTER, 0, 4)
sInfo     = S("Info",     "DV",      10, 14, C_LIGHT,  TA_CENTER, 0, 3)
sH1       = S("H1",       "DV-Bold", 13, 17, C_DARK,   TA_LEFT,  14, 4)
sH2       = S("H2",       "DV-Bold", 11, 15, C_MID,    TA_LEFT,   8, 3)
sBody     = S("Body",     "DV",      10, 14, colors.HexColor("#222222"),
              TA_JUSTIFY, 0, 5)
sBullet   = S("Bullet",   "DV",      10, 14, colors.HexColor("#222222"),
              TA_JUSTIFY, 0, 4, leftIndent=12)
sCode     = S("Code",     "DVMono",   8, 11, colors.HexColor("#1a1a1a"),
              TA_LEFT, 0, 0)
sCaption  = S("Caption",  "DV",       8, 11, colors.HexColor("#555555"),
              TA_CENTER, 2, 6)
sVideoBox = S("VideoBox", "DV-Bold", 10, 14, C_DARK,   TA_LEFT)

def bullet(text, style=sBullet):
    return Paragraph("• " + text, style)

def code_block(text):
    """Returns a styled table containing monospace code."""
    p = Preformatted(text, sCode)
    t = Table([[p]], colWidths=[16.2*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), C_MONO),
        ("BOX",         (0,0), (-1,-1), 0.5, C_BORDER),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING",(0,0), (-1,-1), 8),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[C_MONO]),
    ]))
    return t

def section_rule():
    return HRFlowable(width="100%", thickness=1.2, color=C_BORDER,
                      spaceAfter=6, spaceBefore=2)

# ── Build terminal output strings ─────────────────────────────────────────────
def run_program(input_file):
    result = subprocess.run(
        ["./cagri", input_file],
        capture_output=True, text=True, cwd="/home/user/VeriYapilari-Odev2"
    )
    return result.stdout.strip()

out01 = run_program("input01.txt")
out02 = run_program("input02.txt")
out03 = run_program("input03.txt")

# Read input files for display
def read_file(path):
    with open(path) as f:
        return f.read().strip()

in01 = read_file("/home/user/VeriYapilari-Odev2/input01.txt")
in02 = read_file("/home/user/VeriYapilari-Odev2/input02.txt")
in03 = read_file("/home/user/VeriYapilari-Odev2/input03.txt")

# ── Cover page builder ────────────────────────────────────────────────────────
def draw_cover(canvas, doc):
    W, H = A4
    # Dark gradient header block
    canvas.saveState()
    canvas.setFillColor(C_DARK)
    canvas.rect(0, H - 9*cm, W, 9*cm, fill=1, stroke=0)

    # Thin accent line
    canvas.setFillColor(C_MID)
    canvas.rect(0, H - 9*cm - 0.35*cm, W, 0.35*cm, fill=1, stroke=0)

    # Light footer strip
    canvas.setFillColor(C_LIGHT)
    canvas.rect(0, 0, W, 2.2*cm, fill=1, stroke=0)
    canvas.setFillColor(C_BORDER)
    canvas.rect(0, 2.2*cm, W, 0.15*cm, fill=1, stroke=0)

    canvas.restoreState()

def build_cover():
    items = []
    items.append(Spacer(1, 2.4*cm))

    # University / faculty
    items.append(Paragraph("YILDIZ TEKNİK ÜNİVERSİTESİ", sSub))
    items.append(Paragraph(
        "Elektrik Elektronik Fakültesi / Bilgisayar Mühendisliği Bölümü",
        S("sSub2","DV",9,13,C_LIGHT,TA_CENTER)))
    items.append(Spacer(1, 0.5*cm))
    items.append(Paragraph(ASSIGNMENT, sTitle))
    items.append(Spacer(1, 0.3*cm))
    items.append(Paragraph(SEMESTER, sSub))

    # Blue accent line under header (handled by onFirstPage)
    items.append(Spacer(1, 4.2*cm))

    # Info table
    label_style = S("lbl","DV-Bold",10,14,C_DARK,TA_LEFT)
    value_style = S("val","DV",     10,14,colors.HexColor("#333333"),TA_LEFT)

    rows = [
        ("Öğrenci Adı",     STUDENT_NAME),
        ("Öğrenci Numarası",STUDENT_NO),
        ("Ders",            COURSE),
        ("Grup",            GROUP),
        ("Dersin Eğitmeni", INSTRUCTOR),
        ("Video Linki",     VIDEO_LINK),
    ]

    tdata = [[Paragraph(k+":", label_style), Paragraph(v, value_style)]
             for k, v in rows]

    t = Table(tdata, colWidths=[5.5*cm, 11*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1,-1), colors.white),
        ("BACKGROUND",   (0, 0), (0,-1),  C_LIGHT),
        ("BOX",          (0, 0), (-1,-1), 0.8, C_BORDER),
        ("INNERGRID",    (0, 0), (-1,-1), 0.4, C_BORDER),
        ("TOPPADDING",   (0, 0), (-1,-1), 7),
        ("BOTTOMPADDING",(0, 0), (-1,-1), 7),
        ("LEFTPADDING",  (0, 0), (-1,-1), 10),
        ("RIGHTPADDING", (0, 0), (-1,-1), 10),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),
         [colors.white, C_LIGHT]*10),
    ]))
    items.append(t)
    return items

# ── Report pages ──────────────────────────────────────────────────────────────
def build_body():
    items = []

    # ── 1. Problemin Çözümü ────────────────────────────────────────────────
    items.append(Paragraph("1. Problemin Çözümü (Algoritma)", sH1))
    items.append(section_rule())

    items.append(Paragraph(
        "Bu ödevde, T adet müşteri temsilcisine sahip bir çağrı merkezinin "
        "simülasyonu gerçekleştirilmiştir. Sistemde üç tip olay işlenmektedir: "
        "müşteri araması (Tip 1), temsilci görüşme bitişi (Tip 2) ve müşteri "
        "aktarma talebi (Tip 3).", sBody))

    items.append(Paragraph("Kullanılan Veri Yapıları", sH2))
    items.append(bullet(
        "<b>Kuyruk (Queue – FIFO):</b> Normal bekleme sırası için kullanılmıştır. "
        "Erken arayan müşteri, boş temsilci bulunduğunda önce bağlanmaktadır."))
    items.append(bullet(
        "<b>Yığın (Stack – LIFO):</b> Aktarma bekleme alanı için kullanılmıştır. "
        "En son aktarılan müşteri, bir temsilci boşa çıktığında önce bağlanmaktadır."))
    items.append(Spacer(1, 0.3*cm))

    items.append(Paragraph("Algoritmanın İşleyişi", sH2))
    items.append(bullet(
        "<b>Tip 1 – Müşteri araması:</b> Temsilciler [0..T-1] sırasıyla taranmaktadır. "
        "En küçük sicil numaralı boş temsilci bulunursa müşteri hemen bağlanmakta; "
        "tüm temsilciler meşgulse müşteri bekleme kuyruğuna (enqueue) alınmaktadır."))
    items.append(bullet(
        "<b>Tip 2 – Temsilci bitişi:</b> Temsilci serbest bırakılmakta, ardından "
        "önce aktarma yığını (stack) kontrol edilmektedir. Yığında bekleyen varsa "
        "pop ile alınıp bağlanmakta; yoksa kuyruktan (dequeue) bir sonraki müşteri "
        "alınmaktadır."))
    items.append(bullet(
        "<b>Tip 3 – Aktarma talebi:</b> Müşteri, hizmet veren temsilciden ayrılıp "
        "aktarma yığınına (push) eklenmektedir. Temsilci serbest kaldığında "
        "aynı müşteri yığından geri alınarak (pop) yeni bağlantı kurulmaktadır; "
        "bu sayede aktarma sırası LIFO olarak korunmaktadır."))
    items.append(Spacer(1, 0.3*cm))

    items.append(Paragraph("Sözde Kod", sH2))
    pseudo = (
        "İçin her olay sırayla:\n"
        "  EĞER tip == 1:\n"
        "    freeRep ← en küçük boş temsilci indisi\n"
        "    EĞER freeRep bulundu: bağla ve çıktı ver\n"
        "    DEĞİLSE:             kuyruga ekle (ENQUEUE)\n"
        "\n"
        "  EĞER tip == 2:\n"
        "    temsilci[sicilNo] ← serbest\n"
        "    EĞER yığın boş değil: POP → bağla ve çıktı ver\n"
        "    DEĞİLSE EĞER kuyruk boş değil: DEQUEUE → bağla ve çıktı ver\n"
        "\n"
        "  EĞER tip == 3:\n"
        "    müşteriyi hizmet veren temsilciyi bul\n"
        "    PUSH müşteri → yığın\n"
        "    temsilci ← serbest\n"
        "    POP → aynı temsilciye yeniden bağla ve çıktı ver"
    )
    items.append(code_block(pseudo))
    items.append(Spacer(1, 0.5*cm))

    # ── 2. Karşılaşılan Sorunlar ───────────────────────────────────────────
    items.append(Paragraph("2. Karşılaşılan Sorunlar", sH1))
    items.append(section_rule())

    items.append(Paragraph(
        "Aktarma olayının (Tip 3) işlenmesinde öncelik mantığının "
        "doğru kurulması en kritik nokta olmuştur. Müşteri aktarma talebinde "
        "bulunduğunda, müşterinin yığına eklenmesinin ardından aynı temsilcinin "
        "hemen serbest kalması ve yığından müşteriyi geri alması gerekmektedir; "
        "bu durum tasarım aşamasında dikkatle ele alınmıştır.", sBody))

    items.append(Paragraph(
        "Bunun yanı sıra, bağlı liste tabanlı dinamik bellek yönetiminde "
        "her düğüm işlemi sonrasında belleğin doğru serbest bırakılması "
        "(free) sağlanmış; kuyruk ve yığının hem ön hem arka/üst göstericilerinin "
        "tutarlı biçimde güncellenmesine özen gösterilmiştir.", sBody))

    items.append(Paragraph(
        "ANSI-C standardına uygunluk kapsamında tüm değişken bildirimleri "
        "blok başına taşınmış, döngü içi değişken tanımından (C99 stili) "
        "kaçınılmış ve tüm yorumlar <font name='DVMono'>/* */</font> biçiminde "
        "yazılmıştır.", sBody))

    return items

# ── Screenshot page ───────────────────────────────────────────────────────────
def build_screenshots():
    items = []
    items.append(Paragraph("3. Ekran Görüntüleri", sH1))
    items.append(section_rule())

    test_cases = [
        ("Test 1 – Örnek Girdi (input01.txt)",
         "T=2, 9 olay – ödev dokümanındaki örnek",
         in01, out01),
        ("Test 2 – Tek Temsilci (input02.txt)",
         "T=1, 8 olay – tek temsilcide kuyruk birikimi",
         in02, out02),
        ("Test 3 – Çoklu Aktarma (input03.txt)",
         "T=2, 12 olay – birden fazla aktarma senaryosu",
         in03, out03),
    ]

    mono_style = S("mono","DVMono",8,11,colors.HexColor("#1a1a1a"),TA_LEFT)
    hdr_style  = S("hdr","DV-Bold",9,13,C_WHITE,TA_LEFT)
    sub_style  = S("sub","DV",8,12,colors.HexColor("#555"),TA_LEFT)

    for title, desc, inp, out in test_cases:
        items.append(Spacer(1, 0.35*cm))
        # Header row
        hdr = Table([[Paragraph(title, hdr_style)]],
                    colWidths=[16.2*cm])
        hdr.setStyle(TableStyle([
            ("BACKGROUND",  (0,0),(-1,-1), C_MID),
            ("LEFTPADDING", (0,0),(-1,-1), 10),
            ("TOPPADDING",  (0,0),(-1,-1), 5),
            ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ]))
        items.append(hdr)

        # Input / Output side by side
        in_block  = Preformatted(inp, mono_style)
        out_block = Preformatted(out, mono_style)

        io_table = Table(
            [[Paragraph("Girdi", S("g","DV-Bold",8,11,C_DARK,TA_LEFT)),
              Paragraph("Çıktı", S("c","DV-Bold",8,11,C_DARK,TA_LEFT))],
             [in_block, out_block]],
            colWidths=[8.1*cm, 8.1*cm]
        )
        io_table.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1, 0), C_LIGHT),
            ("BACKGROUND",   (0,1), (-1,-1), C_MONO),
            ("BOX",          (0,0), (-1,-1), 0.5, C_BORDER),
            ("INNERGRID",    (0,0), (-1,-1), 0.4, C_BORDER),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("TOPPADDING",   (0,0), (-1,-1), 5),
            ("BOTTOMPADDING",(0,0), (-1,-1), 5),
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ]))
        items.append(io_table)
        items.append(Paragraph(desc, sCaption))

    # ── Edge-case tests ───────────────────────────────────────────────────
    items.append(Spacer(1, 0.5*cm))
    items.append(Paragraph("Uç Durum Testleri", sH2))

    edge_cases = [
        ("Uç Durum 1: Tek müşteri, tek temsilci",
         "1\n1\n1 1 999",
         "Beklenen çıktı:  1 999 0"),
        ("Uç Durum 2: Kuyruk birikimi — tek temsilci, 3 müşteri",
         "1\n5\n1 1 100\n2 1 200\n3 1 300\n4 2 0\n5 2 0",
         "Beklenen çıktı:  1 100 0  /  4 200 0  /  5 300 0\n"
         "(200 ve 300 sıraya girer; temsilci her boşaldığında sıradakini alır)"),
        ("Uç Durum 3: Aktarma önceliği — kuyrukta bekleyen varken aktarma",
         "2\n7\n1 1 11\n2 1 22\n3 1 33\n4 3 11\n5 2 1\n6 2 0\n7 2 0",
         "Beklenen çıktı:  1 11 0  /  2 22 1  /  4 11 0  /  5 33 1\n"
         "(t=4: 11 aktarılır, rep[0] anında 11'i yeniden alır; 33 kuyrukta bekler;\n"
         " t=5: rep[1] boşaldığında yığın boş, kuyruktan 33 alınır)"),
    ]

    for title, inp, note in edge_cases:
        items.append(Spacer(1, 0.25*cm))
        items.append(Paragraph("▸ " + title,
                               S("et","DV-Bold",9,13,C_DARK,TA_LEFT)))
        items.append(code_block(inp))
        items.append(Paragraph(note, sCaption))

    return items

# ── Assemble document ─────────────────────────────────────────────────────────
def build_pdf(output_path):
    M = 2*cm
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=M, rightMargin=M,
        topMargin=M, bottomMargin=2.5*cm,
        title=f"BLM2512 Ödev 2 – {STUDENT_NAME}",
        author=STUDENT_NAME,
    )

    # Page templates
    def on_cover(canvas, doc):
        draw_cover(canvas, doc)

    def on_later(canvas, doc):
        W, H = A4
        canvas.saveState()
        # Top bar
        canvas.setFillColor(C_DARK)
        canvas.rect(0, H - 1.1*cm, W, 1.1*cm, fill=1, stroke=0)
        canvas.setFillColor(C_MID)
        canvas.rect(0, H - 1.25*cm, W, 0.15*cm, fill=1, stroke=0)
        # Header text
        canvas.setFont("DV-Bold", 8)
        canvas.setFillColor(C_WHITE)
        canvas.drawString(M, H - 0.75*cm, f"BLM2512 – Ödev 2 | Stack & Queue")
        canvas.drawRightString(W - M, H - 0.75*cm, STUDENT_NAME + "  |  " + STUDENT_NO)
        # Bottom bar
        canvas.setFillColor(C_LIGHT)
        canvas.rect(0, 0, W, 1.4*cm, fill=1, stroke=0)
        canvas.setFillColor(C_BORDER)
        canvas.rect(0, 1.4*cm, W, 0.12*cm, fill=1, stroke=0)
        canvas.setFont("DV", 7.5)
        canvas.setFillColor(C_DARK)
        canvas.drawString(M, 0.55*cm,
            "Yıldız Teknik Üniversitesi  •  " + COURSE + "  •  " + SEMESTER)
        canvas.drawRightString(W - M, 0.55*cm,
            f"Sayfa {doc.page - 1}")   # page 1 = cover
        canvas.restoreState()

    story = []

    # Cover
    story += build_cover()
    story.append(PageBreak())

    # Body (report pages)
    story += build_body()
    story.append(PageBreak())

    # Screenshots
    story += build_screenshots()

    doc.build(story,
              onFirstPage=on_cover,
              onLaterPages=on_later)
    print(f"PDF created: {output_path}")

if __name__ == "__main__":
    out = f"/home/user/VeriYapilari-Odev2/{STUDENT_NO}.pdf"
    build_pdf(out)
