#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BLM2512 Odev 2 - PDF rapor uretici
Kullanim: python3 generate_pdf.py [video_link]
"""

import sys
import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, Preformatted, KeepTogether
)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ─── Fontlar ───────────────────────────────────────────────────────────────
D = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV",     D + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB",    D + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVM",    D + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("DVMB",   D + "DejaVuSansMono-Bold.ttf"))

# ─── Renkler ───────────────────────────────────────────────────────────────
DARK   = colors.HexColor("#1a2b4a")
MID    = colors.HexColor("#2e5fa3")
LIGHT  = colors.HexColor("#e8f0fb")
MONO   = colors.HexColor("#f4f6f8")
BDR    = colors.HexColor("#c5d5ea")
WHITE  = colors.white
TEXT   = colors.HexColor("#1e1e1e")
GREY   = colors.HexColor("#555555")

# ─── Öğrenci bilgileri ─────────────────────────────────────────────────────
NAME       = "Omar Nuriyev"
STNO       = "24011902"
COURSE     = "BLM2512 Veri Yapıları ve Algoritmalar"
INSTRUCTOR = "Doç.Dr. Mehmet Amaç Güvensan"
SEMESTER   = "2025-2026 Bahar Yarıyılı"
TITLE      = "Ödev 2 – Stack & Queue"
VIDEO      = sys.argv[1] if len(sys.argv) > 1 else "[VİDEO LİNKİ EKLENECEKTİR]"

# ─── Stil fabrikası ────────────────────────────────────────────────────────
def sty(name, font="DV", size=10, lead=14, clr=TEXT,
        align=TA_LEFT, sb=0, sa=4, li=0):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=lead,
                          textColor=clr, alignment=align,
                          spaceBefore=sb, spaceAfter=sa, leftIndent=li)

# Stilleri bir kere tanımla
S_TITLE  = sty("ti",  "DVB", 20, 26, WHITE,  TA_CENTER, 0, 6)
S_SUB    = sty("su",  "DV",  11, 15, LIGHT,  TA_CENTER, 0, 4)
S_UNIV   = sty("un",  "DV",   9, 12, LIGHT,  TA_CENTER, 0, 3)
S_H1     = sty("h1",  "DVB", 13, 17, DARK,   TA_LEFT,  16, 6)
S_H2     = sty("h2",  "DVB", 10, 14, MID,    TA_LEFT,   8, 4)
S_BODY   = sty("bo",  "DV",  10, 14, TEXT,   TA_JUSTIFY, 0, 5)
S_BUL    = sty("bu",  "DV",  10, 14, TEXT,   TA_JUSTIFY, 0, 4, li=10)
S_CODE   = sty("co",  "DVM",  8, 11, TEXT,   TA_LEFT)
S_CAP    = sty("ca",  "DV",   8, 11, GREY,   TA_CENTER, 2, 6)
S_LBL    = sty("lb",  "DVB", 10, 14, DARK,   TA_LEFT)
S_VAL    = sty("va",  "DV",  10, 14, TEXT,   TA_LEFT)
S_IOLBL  = sty("io",  "DVB",  9, 12, DARK,   TA_LEFT)
S_CAHDR  = sty("ch",  "DVB",  9, 13, WHITE,  TA_LEFT)

def hr():
    return HRFlowable(width="100%", thickness=1.0, color=BDR,
                      spaceBefore=2, spaceAfter=6)

def bullet(txt):
    return Paragraph("•  " + txt, S_BUL)

def code_box(txt):
    p = Preformatted(txt, S_CODE)
    t = Table([[p]], colWidths=[16.2*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), MONO),
        ("BOX",          (0,0),(-1,-1), 0.5, BDR),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ]))
    return t

# ─── Kapak sayfası ─────────────────────────────────────────────────────────
def draw_cover_bg(canvas, doc):
    W, H = A4
    canvas.saveState()
    canvas.setFillColor(DARK)
    canvas.rect(0, H - 8.8*cm, W, 8.8*cm, fill=1, stroke=0)
    canvas.setFillColor(MID)
    canvas.rect(0, H - 9.0*cm, W, 0.2*cm, fill=1, stroke=0)
    canvas.setFillColor(LIGHT)
    canvas.rect(0, 0, W, 2.0*cm, fill=1, stroke=0)
    canvas.setFillColor(BDR)
    canvas.rect(0, 2.0*cm, W, 0.12*cm, fill=1, stroke=0)
    canvas.restoreState()

def build_cover():
    items = []
    items.append(Spacer(1, 2.2*cm))
    items.append(Paragraph("YILDIZ TEKNİK ÜNİVERSİTESİ", S_SUB))
    items.append(Paragraph(
        "Elektrik Elektronik Fakültesi / Bilgisayar Mühendisliği Bölümü", S_UNIV))
    items.append(Spacer(1, 0.5*cm))
    items.append(Paragraph(TITLE, S_TITLE))
    items.append(Spacer(1, 0.3*cm))
    items.append(Paragraph(SEMESTER, S_SUB))
    items.append(Spacer(1, 4.5*cm))   # konumlandırma boşluğu — kapak kutusuna kadar

    rows = [
        ("Öğrenci Adı",      NAME),
        ("Öğrenci Numarası", STNO),
        ("Ders",             COURSE),
        ("Dersin Eğitmeni",  INSTRUCTOR),
        ("Video Linki",      VIDEO),
    ]
    tdata = [[Paragraph(k + ":", S_LBL), Paragraph(v, S_VAL)] for k, v in rows]
    t = Table(tdata, colWidths=[5.5*cm, 11.0*cm])
    t.setStyle(TableStyle([
        ("ROWBACKGROUNDS", (0,0),(-1,-1), [WHITE, LIGHT]),
        ("BACKGROUND",     (0,0),(0,-1),  LIGHT),
        ("BOX",            (0,0),(-1,-1), 0.8, BDR),
        ("INNERGRID",      (0,0),(-1,-1), 0.4, BDR),
        ("TOPPADDING",     (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 7),
        ("LEFTPADDING",    (0,0),(-1,-1), 10),
        ("RIGHTPADDING",   (0,0),(-1,-1), 10),
    ]))
    items.append(t)
    return items

# ─── Rapor içeriği ─────────────────────────────────────────────────────────
def build_body():
    items = []

    # Bölüm 1
    sec1 = [
        Paragraph("1.  Problemin Çözümü (Algoritma)", S_H1),
        hr(),
        Paragraph(
            "Bu ödevde, T adet müşteri temsilcisine sahip bir çağrı merkezinin "
            "simülasyonu gerçekleştirilmiştir. Sistemde üç tip olay işlenmektedir: "
            "müşteri araması (Tip 1), temsilci görüşme bitişi (Tip 2) ve müşteri "
            "aktarma talebi (Tip 3).", S_BODY),
    ]
    items.append(KeepTogether(sec1))

    items.append(Paragraph("Kullanılan Veri Yapıları", S_H2))
    items.append(KeepTogether([
        bullet("<b>Kuyruk (Queue – FIFO):</b> Normal bekleme sırası için "
               "kullanılmıştır. Erken arayan müşteri, boş temsilci bulunduğunda "
               "önce bağlanır. Bağlı liste üzerine inşa edilmiştir."),
        bullet("<b>Yığın (Stack – LIFO):</b> Aktarma bekleme alanı için "
               "kullanılmıştır. En son aktarılan müşteri, bir temsilci boşa "
               "çıktığında önce bağlanır. Bağlı liste üzerine inşa edilmiştir."),
    ]))

    items.append(Paragraph("Algoritmanın İşleyişi", S_H2))
    items.append(KeepTogether([
        bullet("<b>Tip 1 – Müşteri araması:</b> Temsilciler [0..T‑1] sırasıyla "
               "taranır. En küçük sicil numaralı boş temsilci bulunursa müşteri "
               "hemen bağlanır; tüm temsilciler meşgulse bekleme kuyruğuna "
               "(enqueue) alınır."),
        bullet("<b>Tip 2 – Temsilci bitişi:</b> Temsilci serbest bırakılır, "
               "ardından önce aktarma yığını (pop) kontrol edilir. Yığın boşsa "
               "kuyruktan (dequeue) bir sonraki müşteri alınır."),
        bullet("<b>Tip 3 – Aktarma talebi:</b> Müşteri aktarma yığınına (push) "
               "eklenir ve hizmet veren temsilci serbest kalır. Temsilci hemen "
               "yığından müşteriyi geri alır (pop) ve yeni bağlantı kurulur; "
               "böylece LIFO önceliği korunur."),
    ]))

    items.append(Paragraph("Sözde Kod", S_H2))
    pseudo = (
        "İçin her olay:\n"
        "  EĞER tip == 1:\n"
        "    freeRep <- en küçük boş temsilci indisi\n"
        "    EĞER freeRep bulundu : bağla, çıktı ver\n"
        "    DEĞİLSE              : ENQUEUE(musteri)\n"
        "\n"
        "  EĞER tip == 2:\n"
        "    temsilci[sicilNo] <- serbest\n"
        "    EĞER Stack doluysa    : POP -> bağla, çıktı ver\n"
        "    DEĞİLSE EĞER Queue dolu : DEQUEUE -> bağla, çıktı ver\n"
        "\n"
        "  EĞER tip == 3:\n"
        "    PUSH(musteri) -> yığın\n"
        "    temsilci <- serbest\n"
        "    POP -> aynı temsilciye bağla, çıktı ver"
    )
    items.append(KeepTogether([code_box(pseudo), Spacer(1, 0.3*cm)]))

    # Bölüm 2
    sec2_hdr = [
        Paragraph("2.  Karşılaşılan Sorunlar", S_H1),
        hr(),
    ]
    items.append(KeepTogether(sec2_hdr + [
        Paragraph(
            "Aktarma olayının (Tip 3) işlenmesinde öncelik mantığının doğru "
            "kurulması en kritik nokta olmuştur. Müşteri yığına push edildikten "
            "hemen sonra temsilci serbest kalmakta ve pop ile aynı müşteriyi geri "
            "almaktadır. Bu akışın doğru sırada tasarlanması dikkat gerektirmiştir.",
            S_BODY),
    ]))

    items.append(KeepTogether([
        Paragraph(
            "Bağlı liste tabanlı dinamik bellek yönetiminde her düğüm işlemi "
            "sonrasında belleğin doğru serbest bırakılması (free) sağlanmış; "
            "kuyruk ve yığının ön/arka/üst göstericilerinin tutarlı biçimde "
            "güncellenmesine özen gösterilmiştir.", S_BODY),
        Paragraph(
            "ANSI-C standardına uygunluk kapsamında tüm değişken bildirimleri "
            "blok başına taşınmış, döngü içi değişken tanımından kaçınılmış ve "
            "tüm yorumlar /* */ biçiminde yazılmıştır.", S_BODY),
        Spacer(1, 0.2*cm),
    ]))

    return items

# ─── Ekran görüntüleri ─────────────────────────────────────────────────────
def run(f):
    r = subprocess.run(["./cagri", f], capture_output=True, text=True,
                       cwd="/home/user/VeriYapilari-Odev2")
    return r.stdout.strip()

def read(path):
    with open(path) as f:
        return f.read().strip()

def io_table(inp, out):
    ib = Preformatted(inp, S_CODE)
    ob = Preformatted(out, S_CODE)
    t = Table(
        [[Paragraph("Girdi", S_IOLBL), Paragraph("Çıktı", S_IOLBL)],
         [ib, ob]],
        colWidths=[8.1*cm, 8.1*cm]
    )
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,0),  LIGHT),
        ("BACKGROUND",   (0,1),(-1,-1), MONO),
        ("BOX",          (0,0),(-1,-1), 0.5, BDR),
        ("INNERGRID",    (0,0),(-1,-1), 0.4, BDR),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("VALIGN",       (0,0),(-1,-1), "TOP"),
    ]))
    return t

def section_hdr(title):
    t = Table([[Paragraph(title, S_CAHDR)]], colWidths=[16.2*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), MID),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
        ("TOPPADDING",   (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1), 5),
    ]))
    return t

def build_screenshots():
    base = "/home/user/VeriYapilari-Odev2/"
    tests = [
        ("Test 1 – Örnek Girdi (input01.txt)",
         "T=2, 9 olay — ödev dokümanındaki örnek girdi",
         read(base+"input01.txt"), run("input01.txt")),
        ("Test 2 – Tek Temsilci (input02.txt)",
         "T=1, 8 olay — tek temsilcide kuyruk birikimi",
         read(base+"input02.txt"), run("input02.txt")),
        ("Test 3 – Çoklu Aktarma (input03.txt)",
         "T=2, 12 olay — birden fazla aktarma senaryosu",
         read(base+"input03.txt"), run("input03.txt")),
    ]

    items = []
    items.append(KeepTogether([
        Paragraph("3.  Ekran Görüntüleri", S_H1),
        hr(),
    ]))

    for title, desc, inp, out in tests:
        block = [
            Spacer(1, 0.3*cm),
            section_hdr(title),
            io_table(inp, out),
            Paragraph(desc, S_CAP),
        ]
        items.append(KeepTogether(block))

    # Uç durum testleri
    items.append(Spacer(1, 0.4*cm))
    items.append(KeepTogether([
        Paragraph("Uç Durum Testleri", S_H2),
    ]))

    edges = [
        ("Uç Durum 1 – Tek müşteri, tek temsilci",
         "1\n1\n1 1 999",
         "Çıktı: 1 999 0  (boş sistem, tek müşteri hemen bağlanır)"),
        ("Uç Durum 2 – Kuyruk birikimi (1 temsilci, 3 müşteri)",
         "1\n5\n1 1 100\n2 1 200\n3 1 300\n4 2 0\n5 2 0",
         "Çıktı: 1 100 0 / 4 200 0 / 5 300 0  (200 ve 300 FIFO sırasıyla alınır)"),
        ("Uç Durum 3 – Aktarma önceliği (yığın kuyruğu geçer)",
         "2\n7\n1 1 11\n2 1 22\n3 1 33\n4 3 11\n5 2 1\n6 2 0\n7 2 0",
         "Çıktı: 1 11 0 / 2 22 1 / 4 11 0 / 5 33 1\n"
         "(t=4: 11 aktarılır ve anında yeniden alınır; 33 kuyrukta bekler)"),
    ]

    for title, inp, note in edges:
        block = [
            Spacer(1, 0.25*cm),
            section_hdr(title),
            code_box(inp),
            Paragraph(note, S_CAP),
        ]
        items.append(KeepTogether(block))

    return items

# ─── Header / footer çizimi (iç sayfalar) ──────────────────────────────────
def later_pages(canvas, doc):
    W, H = A4
    M = 2*cm
    canvas.saveState()
    # Üst bant
    canvas.setFillColor(DARK)
    canvas.rect(0, H - 1.05*cm, W, 1.05*cm, fill=1, stroke=0)
    canvas.setFillColor(MID)
    canvas.rect(0, H - 1.18*cm, W, 0.13*cm, fill=1, stroke=0)
    canvas.setFont("DVB", 8)
    canvas.setFillColor(WHITE)
    canvas.drawString(M, H - 0.7*cm, "BLM2512 Ödev 2  |  Stack & Queue")
    canvas.drawRightString(W - M, H - 0.7*cm, NAME + "   " + STNO)
    # Alt bant
    canvas.setFillColor(LIGHT)
    canvas.rect(0, 0, W, 1.3*cm, fill=1, stroke=0)
    canvas.setFillColor(BDR)
    canvas.rect(0, 1.3*cm, W, 0.1*cm, fill=1, stroke=0)
    canvas.setFont("DV", 7.5)
    canvas.setFillColor(DARK)
    canvas.drawString(M, 0.48*cm,
        "Yıldız Teknik Üniversitesi  •  " + COURSE + "  •  " + SEMESTER)
    canvas.drawRightString(W - M, 0.48*cm, f"Sayfa  {doc.page - 1}")
    canvas.restoreState()

# ─── PDF oluştur ───────────────────────────────────────────────────────────
def build():
    M = 2*cm
    out = f"/home/user/VeriYapilari-Odev2/{STNO}.pdf"
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=M, rightMargin=M,
        topMargin=1.6*cm, bottomMargin=2.0*cm,
        title=f"BLM2512 Ödev 2 – {NAME}",
        author=NAME,
    )

    story = []
    story += build_cover()
    story.append(PageBreak())           # Kapaktan sonra yeni sayfa (zorunlu)
    story += build_body()               # Problemin Çözümü + Karşılaşılan Sorunlar
    story += build_screenshots()        # Ekran Görüntüleri — doğal akışla devam eder

    doc.build(story,
              onFirstPage=draw_cover_bg,
              onLaterPages=later_pages)
    print(f"Olusturuldu: {out}")

if __name__ == "__main__":
    build()
