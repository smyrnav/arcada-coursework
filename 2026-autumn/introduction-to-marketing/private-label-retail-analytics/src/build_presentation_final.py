"""Build the final narrated presentation (15 slides, 16:9)."""
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / 'presentation' / 'assets'
EV = ROOT / 'evidence' / 'screenshots'
OUT = ROOT / 'presentation' / 'presentation.pptx'

INK = RGBColor(0x1F, 0x29, 0x37)
GRAY = RGBColor(0x6B, 0x72, 0x80)
ACCENT = RGBColor(0x0F, 0x4C, 0x81)
GREEN = RGBColor(0x2E, 0x7D, 0x32)
RED = RGBColor(0xC6, 0x28, 0x28)
NAVY = RGBColor(0x2F, 0x54, 0x7D)
LIGHT = RGBColor(0xF3, 0xF4, 0xF6)
LINE = RGBColor(0xE5, 0xE7, 0xEB)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FONT = 'Arial'
MARGIN = Inches(0.65)
SW, SH = Inches(13.333), Inches(7.5)

prs = Presentation()
prs.slide_width = SW
prs.slide_height = SH
BLANK = prs.slide_layouts[6]
_page = [0]


def slide():
    s = prs.slides.add_slide(BLANK)
    _page[0] += 1
    tb = s.shapes.add_textbox(SW - Inches(0.75), SH - Inches(0.42), Inches(0.5), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    r = p.add_run(); r.text = f'{_page[0]:02d}'
    r.font.size = Pt(9); r.font.color.rgb = GRAY; r.font.name = FONT
    p.alignment = PP_ALIGN.RIGHT
    return s


def box(s, l, t, w, h):
    tb = s.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tf


def runs(p, parts, size, color, bold=False, align=None):
    if align is not None:
        p.alignment = align
    for part in parts:
        text, kw = (part, {}) if isinstance(part, str) else part
        r = p.add_run(); r.text = text
        r.font.size = Pt(kw.get('size', size)); r.font.name = FONT
        r.font.color.rgb = kw.get('color', color)
        r.font.bold = kw.get('bold', bold)
        if kw.get('italic'):
            r.font.italic = True
        if kw.get('link'):
            r.hyperlink.address = kw['link']
            r.font.color.rgb = ACCENT
            r.font.underline = True
    return p


def para(tf, parts, size=14, color=INK, bold=False, align=None, space_after=6, space_before=0, first=False, line=None):
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.space_after = Pt(space_after); p.space_before = Pt(space_before)
    if line:
        p.line_spacing = line
    return runs(p, parts, size, color, bold, align)


def kicker_title(s, kicker, title, title_size=28):
    tf = box(s, MARGIN, Inches(0.42), SW - 2 * MARGIN, Inches(0.32))
    para(tf, [(kicker, {})], size=11, color=ACCENT, bold=True, first=True)
    tf2 = box(s, MARGIN, Inches(0.74), SW - 2 * MARGIN, Inches(1.0))
    para(tf2, [(title, {})], size=title_size, color=INK, bold=True, first=True, space_after=0)


def source_line(s, parts, top=None):
    tf = box(s, MARGIN, top if top is not None else SH - Inches(0.52), SW - 2 * MARGIN, Inches(0.4))
    para(tf, parts, size=9.5, color=GRAY, first=True, space_after=0)


def pic(s, path, left, top, width=None, height=None):
    return s.shapes.add_picture(str(path), left, top, width=width, height=height)


def pic_w(path, w):
    im = Image.open(path)
    return w, Emu(int(w * im.size[1] / im.size[0]))


def pic_h(path, h):
    im = Image.open(path)
    return Emu(int(h * im.size[0] / im.size[1])), h


def panel(s, l, t, w, h, fill=LIGHT, line_color=None):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line_color:
        sh.line.color.rgb = line_color; sh.line.width = Pt(0.75)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def panel_text(s, l, t, w, h, pad=0.16):
    return box(s, l + Inches(pad), t + Inches(pad), w - Inches(2 * pad), h - Inches(2 * pad))


def notes(s, text):
    s.notes_slide.notes_text_frame.text = text


# ---------------------------------------------------------------- slide 1: cover
s = slide()
cover = A / 'cover_photo_1.jpg'
w, h = pic_h(cover, SH)
pic(s, cover, SW - w, 0, width=w, height=SH)
panel(s, 0, 0, Inches(0.14), SH, fill=ACCENT)
tf = box(s, Inches(0.75), Inches(1.5), Inches(4.55), Inches(4.6))
para(tf, [('MARKETING RESEARCH · INDIVIDUAL STUDY', {})], size=11, color=ACCENT, bold=True, first=True, space_after=18)
para(tf, [('Private labels are more than a cheaper option', {})], size=33, color=INK, bold=True, space_after=18, line=1.05)
para(tf, [('A digital comparison of private labels in Finnish grocery and convenience retail.', {})], size=16, color=GRAY, space_after=30, line=1.2)
para(tf, [('Smyrna V.', {})], size=14, color=INK, bold=True, space_after=2)
para(tf, [('Introduction to Marketing 2026 · Arcada University of Applied Sciences', {})], size=12, color=GRAY, space_after=0)
tf = box(s, Inches(0.75), SH - Inches(0.55), Inches(6.5), Inches(0.35))
para(tf, [('Cover photo: ', {}), ('Helsinki Times', {'link': 'https://www.helsinkitimes.com/finland/finland-news/domestic/16483-grocery-retailers-in-the-dark-about-plans-to-tackle-private-label-products.html'})], size=9.5, color=GRAY, first=True, space_after=0)
notes(s, "Hi, I'm Smyrna. This is my individual marketing research project on private labels in Finnish grocery and convenience retail. I compared own-brand products and prices at Kesko, S Group and Lidl, looked at R-kioski menus in different locations, and asked what all of this tells us about why customers choose a retailer's own brand — or don't.")

# ---------------------------------------------------------------- slide 2: scope & method
s = slide()
kicker_title(s, 'RESEARCH DESIGN', 'What I compared and how')
cols = [
    ('RETAIL CATALOGUES', 'Kesko, S Group and Lidl',
     'Own-brand ranges, product categories, pack sizes and unit prices from K-Ruoka, S-kaupat and Lidl.fi listings.'),
    ('DELIVERY MENUS', 'Three R-kioski locations',
     'Wolt menus for Rautatieasema, Vuosaari and Punavuori, plus my own observations at the Sello and Tripla kiosks.'),
    ('CONSUMER SOURCES', 'Research and discussion',
     'KKV\u2019s 2025 market report, PTT\u2019s 2025 consumer survey (n = 1,197), the McKinsey article and one r/arkisuomi discussion.'),
]
cw = Inches(3.85); gap = Inches(0.25); top = Inches(1.75)
for i, (k, h, b) in enumerate(cols):
    l = MARGIN + i * (cw + gap)
    panel(s, l, top, cw, Inches(2.5))
    tf = panel_text(s, l, top, cw, Inches(2.5))
    para(tf, [(k, {})], size=10.5, color=ACCENT, bold=True, first=True, space_after=4)
    para(tf, [(h, {})], size=15, color=INK, bold=True, space_after=6)
    para(tf, [(b, {})], size=12, color=GRAY, space_after=0, line=1.25)
tf = box(s, MARGIN, Inches(4.55), SW - 2 * MARGIN, Inches(0.5))
para(tf, [('Sources  →  API collection  →  CSV datasets  →  Python analysis  →  Charts and interpretation', {})], size=14, color=INK, bold=True, align=PP_ALIGN.CENTER, first=True)
panel(s, MARGIN, Inches(5.25), SW - 2 * MARGIN, Inches(1.45))
tf = panel_text(s, MARGIN, Inches(5.25), SW - 2 * MARGIN, Inches(1.45))
para(tf, [('LIMITATIONS', {})], size=10.5, color=RED, bold=True, first=True, space_after=4)
para(tf, [('No physical shelf audit or shelf photography  ·  Wolt shows delivery availability, not the full store range  ·  No systematic customer observation or purchase data  ·  Part C uses the McKinsey article reflection instead of the classroom survey, as agreed with the teacher.', {})], size=11.5, color=GRAY, space_after=0, line=1.3)
source_line(s, [('Data collected 24 November 2026 · data, code and sources: ', {}), ('github.com/smyrnav/arcada-coursework', {'link': 'https://github.com/smyrnav/arcada-coursework/tree/main/2026-autumn/introduction-to-marketing/private-label-retail-analytics'})])
notes(s, "I did this research digitally instead of a physical store audit. I pulled product data from retailer websites through their APIs, compiled it into CSV datasets and used Python with Matplotlib for the calculations and charts. The limitations matter: I did not photograph shelves, I did not observe customers, and Wolt menus only show what can be ordered for delivery — not the full store range. Everything you will see is catalogue, menu or published research evidence.")

# ---------------------------------------------------------------- slide 3: price pairs
s = slide()
kicker_title(s, 'PART A · PRICE COMPARISON', 'Pirkka and Xtra were 28–33% cheaper per kg than Taffel')
chart = A / 'updated_chart_1_matched_crisp_prices.png'
w, h = pic_w(chart, Inches(9.3))
pic(s, chart, (SW - w) // 2, Inches(1.45), width=w, height=h)
source_line(s, [('Matched salted-crisp pairs from each retailer\u2019s own online catalogue, 24 Nov 2026. Two matched pairs — not a market-wide estimate. Catalogue store selection was not consistently confirmed as Helsinki. Sources: ', {}), ('K-Ruoka', {'link': 'https://www.k-ruoka.fi/kauppa/tuotehaku/makeiset-ja-naposteltavat/sipsit-ja-snacksit'}), (' · ', {}), ('S-kaupat', {'link': 'https://www.s-kaupat.fi/tuotteet/snacksit/sipsit/perunalastut'})])
notes(s, "This is my main price finding. I compared matched salted crisps: Pirkka Original cost 7.96 euros per kilo against Taffel at 11.12 — 28.4 percent lower. Xtra cost 6.84 against Taffel at 10.19 — 32.9 percent lower. Two caveats: these are two matched pairs, not an estimate for the whole market, and the catalogue store selection was not consistently confirmed as Helsinki. Lidl had no comparable regular-price pair, so it is not in this chart.")

# ---------------------------------------------------------------- slide 4: six products
s = slide()
kicker_title(s, 'PART A · PRODUCT CATEGORIES', 'The sample covered snacks and ready-to-eat convenience foods')
chart2 = A / 'updated_chart_2_selected_private_label_products.png'
w, h = pic_w(chart2, Inches(7.3))
pic(s, chart2, MARGIN, Inches(1.8), width=w, height=h)
lx = MARGIN + Inches(7.6); lw = SW - lx - MARGIN
tf = box(s, lx, Inches(1.8), lw, Inches(4.6))
para(tf, [('KESKO', {})], size=11, color=ACCENT, bold=True, first=True, space_after=2)
para(tf, [('Pirkka Original crisps, 275 g', {})], size=12, space_after=1)
para(tf, [('Pirkka chicken triangle sandwich, 150 g', {})], size=12, space_after=8)
para(tf, [('S GROUP', {})], size=11, color=ACCENT, bold=True, space_after=2)
para(tf, [('Xtra salted crisps, 250 g', {})], size=12, space_after=1)
para(tf, [('Coop salami triangle sandwich, 150 g', {})], size=12, space_after=8)
para(tf, [('LIDL', {})], size=11, color=ACCENT, bold=True, space_after=2)
para(tf, [('Snack Day truffle crisps, 150 g*', {})], size=12, space_after=1)
para(tf, [('Kartanon ready-meal range**', {})], size=12, space_after=10)
para(tf, [('* Older limited-batch listing, not a current regular price.\n** Lidl\u2019s brand page publishes no price.', {})], size=10, color=GRAY, space_after=0, line=1.25)
source_line(s, [('Two categories verified per retailer in my sample — not a count of each retailer\u2019s full range. Unit prices from online listings, accessed 24 Nov 2026.')])
notes(s, "The assignment asked for product examples from different categories. My sample verifies two categories at each retailer: snacks and ready-to-eat convenience foods. Crisps and sandwiches, six products in total. Two honest gaps: the Snack Day price comes from an older limited-batch listing, so I do not treat it as a current price, and Lidl's Kartanon brand page publishes no price at all, so I show it as not published rather than estimating one.")

# ---------------------------------------------------------------- slide 5: brand structures
s = slide()
kicker_title(s, 'PART A · BRAND PORTFOLIOS', 'Kesko, S Group and Lidl use different brand structures')
thumbs = [
    (A / 'kesko_thumb.png', 'KESKO — one tiered family',
     'K-Menu — low price\nPirkka — mainstream\nPirkka Parhaat — premium'),
    (A / 'skaupat_thumb.png', 'S GROUP — separate brands',
     'Xtra — low price\nCoop — everyday\nKotimaista — Finnish origin'),
    (A / 'lidl_thumb.png', 'LIDL — many category names',
     '150+ own-brand names in KKV\u2019s 2015–2023 dataset. Examples: Snack Day, Deluxe, Kartanon. Most of the ~3,000-item standard range is own brands (Lidl).'),
]
cw = Inches(3.9); gap = Inches(0.16); top = Inches(1.7)
for i, (img, head, body) in enumerate(thumbs):
    l = MARGIN + i * (cw + gap)
    tw, th = pic_w(img, cw)
    pic(s, img, l, top, width=tw, height=th)
    tf = box(s, l, top + th + Inches(0.12), cw, Inches(2.4))
    para(tf, [(head, {})], size=13, color=INK, bold=True, first=True, space_after=5)
    para(tf, [(body, {})], size=11.5, color=GRAY, space_after=0, line=1.25)
source_line(s, [('The 150+ figure is a historical dataset count (KKV, Jan 2015–Apr 2023), not a live count of Lidl\u2019s 2026 range. Sources: ', {}), ('Kesko', {'link': 'https://www.kesko.fi/en/company/brands/own-brands/pirkka-and-k-menu/'}), (' · ', {}), ('S-kaupat', {'link': 'https://www.s-kaupat.fi/sivu/omat-merkit'}), (' · ', {}), ('Lidl', {'link': 'https://corporate.lidl.fi/laatu-kuuluu-kaikille'}), (' · ', {}), ('KKV 2025', {'link': 'https://www.kkv.fi/tutkimus-ja-vaikuttaminen/julkaisut/tutkimusraportit/kaupan-omat-merkit-eli-private-label-tuotteet-elintarvikemarkkinoilla-tutkimusraportteja-3-2025/'})])
notes(s, "The three retailers organise their own brands differently. Kesko uses one family with three price tiers: K-Menu, Pirkka and Pirkka Parhaat. S Group uses separate brands with distinct roles — Xtra for low price, Coop for everyday, Kotimaista for Finnish origin. Lidl is different again: the competition authority's dataset contains over 150 Lidl brand names, though that is a historical count from 2015 to 2023, not a live number. Three different answers to what an own brand is for.")

# ---------------------------------------------------------------- slide 6: online placement
s = slide()
kicker_title(s, 'PART A · ONLINE PLACEMENT', 'Online catalogues show private labels beside national brands')
k = A / 'kesko_mixed_crop.png'
sk = A / 'skaupat_crop.png'
h_img = Inches(3.55)
wk, _ = pic_h(k, h_img)
wsk, _ = pic_h(sk, h_img)
top = Inches(1.75)
lk = MARGIN
lsk = lk + wk + Inches(0.35)
pic(s, k, lk, top, width=wk, height=h_img)
pic(s, sk, lsk, top, width=wsk, height=h_img)
tf = box(s, lk, top + h_img + Inches(0.1), wk, Inches(1.0))
para(tf, [('K-Ruoka, search “perunalastu”, K-Citymarket Easton (Helsinki): Pirkka at its regular €2.19 beside Taffel Plussa multi-buy offers.', {})], size=10.5, color=GRAY, first=True, line=1.2)
tf = box(s, lsk, top + h_img + Inches(0.1), wsk, Inches(1.0))
para(tf, [('S-kaupat crisp category: Xtra, Coop and Kotimaista in the same grid as Taffel, Estrella and Pringles. Both sites offer brand filters.', {})], size=10.5, color=GRAY, first=True, line=1.2)
source_line(s, [('Online catalogue merchandising only — this says nothing about physical shelf height, facings or in-store visibility. Online listings, not shelf photographs. Sources: ', {}), ('K-Ruoka', {'link': 'https://www.k-ruoka.fi/kauppa/tuotehaku/makeiset-ja-naposteltavat/sipsit-ja-snacksit'}), (' · ', {}), ('S-kaupat', {'link': 'https://www.s-kaupat.fi/tuotteet/snacksit/sipsit/perunalastut'}), (' · accessed 24 Nov 2026', {})])
notes(s, "Since I did not visit stores, I compared how products are presented in the online catalogues. In both K-Ruoka and S-kaupat, private labels appear in the same category listings as national brands, and both sites let you filter by brand. One detail: in the K-Ruoka listing, Taffel had Plussa multi-buy promotions while the private-label products sat at regular prices. But this is digital merchandising — it cannot tell me anything about real shelf height or visibility in the store.")

# ---------------------------------------------------------------- slide 8: R-branded range
s = slide()
kicker_title(s, 'PART B · R-BRANDED PRODUCTS', 'R-kioski also sells R-branded sweets, sandwiches and baguettes')
tile = A / 'rkarkit_tile.png'
th_ = Inches(3.7)
tw, _ = pic_h(tile, th_)
pic(s, tile, MARGIN, Inches(1.9), width=tw, height=th_)
tf = box(s, MARGIN, Inches(1.9) + th_ + Inches(0.08), tw + Inches(0.4), Inches(0.6))
para(tf, [('Actual Wolt product tile: R-karkit Herkku Mix 250 g, €3.00 (€12/kg).', {})], size=10, color=GRAY, first=True, line=1.2)
lx = MARGIN + tw + Inches(0.55); lw = SW - lx - MARGIN
ph = Inches(2.2)
panel(s, lx, Inches(1.9), lw, ph)
tf = panel_text(s, lx, Inches(1.9), lw, ph)
para(tf, [('R-KARKIT — SWEETS', {})], size=11, color=ACCENT, bold=True, first=True, space_after=4)
para(tf, [('Klassikko Mix 300 g · Salmiakki Mix 300 g · Herkku Mix 250 g · Kirpeä Mix 250 g', {})], size=13, space_after=4, line=1.25)
para(tf, [('All €3 each → €10/kg for 300 g bags, €12/kg for 250 g bags. The same four products appeared at Rautatieasema, Vuosaari and Punavuori.', {})], size=11.5, color=GRAY, space_after=0, line=1.25)
panel(s, lx, Inches(4.35), lw, ph)
tf = panel_text(s, lx, Inches(4.35), lw, ph)
para(tf, [('R-BRANDED SANDWICHES & BAGUETTES', {})], size=11, color=ACCENT, bold=True, first=True, space_after=4)
para(tf, [('R Patonki · R Kolmis · R rukiinen · R viljaisa', {})], size=13, space_after=4)
para(tf, [('Ten sandwiches and baguettes at €4.20–4.80 on the Punavuori menu — chicken Caesar, ham and cheese, chicken-bacon-BBQ, tuna, tomato-mozzarella, vegetarian. Plus the six filled breads prepared on site, €3.90–4.60.', {})], size=11.5, color=GRAY, space_after=0, line=1.25)
source_line(s, [('R-branded names in Wolt listings — the listings do not independently establish trademark ownership. Sources: Wolt menus, 24 Nov 2026.')])
notes(s, "The R-kioski delivery menus turned out to be more interesting than I expected. Yes, they list filled breads prepared on site — but they also revealed a wider R-branded range. R-karkit is the clearest example — four candy mixes, all three euros, listed at all three locations I checked. Note the quiet unit-price difference: the 300-gram bags work out at 10 euros per kilo, the 250-gram bags at 12. The Punavuori menu also lists ten sandwiches and baguettes under R-branded names, from 4.20 to 4.80 euros. One honest caveat: these are R-branded names in the listings; the menus alone do not prove legal trademark ownership.")

# ---------------------------------------------------------------- slide 9: R Patonki comparison
s = slide()
kicker_title(s, 'PART B · PRICE COMPARISON', 'The R Patonki baguette cost 37.5% more than the supermarket comparison')
chart_data = CategoryChartData()
chart_data.categories = ['R Patonki Chicken Caesar\n(R-kioski, Wolt)', 'Chef Lunden Chicken Caesar\n(K-Ruoka)']
chart_data.add_series('Listed price (€)', (4.80, 3.49))
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, MARGIN, Inches(1.95), Inches(6.9), Inches(4.3), chart_data)
ch = gf.chart
ch.has_legend = False
ch.has_title = False
plot = ch.plots[0]
plot.gap_width = 80
plot.has_data_labels = True
dl = plot.data_labels
dl.number_format = '€0.00'; dl.number_format_is_linked = False
dl.font.size = Pt(16); dl.font.bold = True; dl.font.name = FONT; dl.font.color.rgb = INK
dl.position = XL_LABEL_POSITION.OUTSIDE_END
ser = plot.series[0]
ser.format.fill.solid(); ser.format.fill.fore_color.rgb = NAVY
pt = ser.points[1]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = RGBColor(0x9C, 0xA3, 0xAF)
cat = ch.category_axis
cat.tick_labels.font.size = Pt(13); cat.tick_labels.font.name = FONT
val = ch.value_axis
val.maximum_scale = 5.5; val.minimum_scale = 0
val.tick_labels.font.size = Pt(11); val.tick_labels.font.name = FONT
val.tick_labels.number_format = '€0'; val.tick_labels.number_format_is_linked = False
val.has_major_gridlines = True
val.major_gridlines.format.line.color.rgb = LINE
lx = MARGIN + Inches(7.3); lw = SW - lx - MARGIN
panel(s, lx, Inches(1.95), lw, Inches(4.3))
tf = panel_text(s, lx, Inches(1.95), lw, Inches(4.3))
para(tf, [('SAME WEIGHT, DIFFERENT PRICE', {})], size=11, color=ACCENT, bold=True, first=True, space_after=8)
para(tf, [('Both are 200 g chicken Caesar baguettes.', {})], size=12.5, space_after=6, line=1.25)
para(tf, [('R Patonki: ', {'bold': True}), ('€4.80 · €24.00/kg', {})], size=12.5, space_after=2)
para(tf, [('Chef Lunden: ', {'bold': True}), ('€3.49 · €17.45/kg', {})], size=12.5, space_after=10)
para(tf, [('My read: R-kioski sells immediate availability in a transit location, not the cheapest everyday lunch.', {})], size=12.5, space_after=6, line=1.25)
para(tf, [('Formulations may differ — this is a price comparison, not a quality judgement.', {})], size=11, color=GRAY, space_after=0, line=1.25)
source_line(s, [('Sources: ', {}), ('Wolt R-kioski Punavuori menu', {'link': 'https://wolt.com/en/fin/helsinki/venue/r-kioski-helsinki-punavuori-fredrikinkatu-12'}), (' · ', {}), ('K-Ruoka', {'link': 'https://www.k-ruoka.fi/'}), (' · accessed 24 Nov 2026', {})])
notes(s, "How does that R-branded range price against a supermarket? K-Ruoka lists a Chef Lunden chicken Caesar baguette — same filling, same 200-gram weight — at 3.49 euros. The R Patonki equivalent costs 4.80, which is 37.5 percent more for the same weight. My interpretation is that R-kioski is selling immediate availability in a transit location, not the cheapest everyday lunch. But I am careful here: the formulations may differ, so this is a price comparison, not a quality judgement.")

# ---------------------------------------------------------------- slide 10: Sello & Tripla
s = slide()
kicker_title(s, 'PART B · PERSONAL OBSERVATIONS', 'Sello and Tripla illustrate how location affects the kiosk experience')
cw = Inches(5.85); gap = Inches(0.35); top = Inches(1.8); ph = Inches(3.6)
panel(s, MARGIN, top, cw, ph)
tf = panel_text(s, MARGIN, top, cw, ph)
para(tf, [('SELLO', {})], size=12, color=ACCENT, bold=True, first=True, space_after=6)
para(tf, [('A compact kiosk before the train', {})], size=16, bold=True, space_after=8)
para(tf, [('Small format. I mostly see office workers, students and passengers picking up a small meal before boarding.', {})], size=13, color=GRAY, space_after=0, line=1.3)
panel(s, MARGIN + cw + gap, top, cw, ph)
tf = panel_text(s, MARGIN + cw + gap, top, cw, ph)
para(tf, [('TRIPLA', {})], size=12, color=ACCENT, bold=True, first=True, space_after=6)
para(tf, [('A larger stop between train and tram', {})], size=16, bold=True, space_after=8)
para(tf, [('Recently renovated into an open pass-through by platforms 8–11. Upgraded self-service coffee station and meal combinations — one offer I used bundled a hot dog and coffee with a free Red Bull. Convenient for people changing between trains and trams.', {})], size=13, color=GRAY, space_after=0, line=1.3)
panel(s, MARGIN, Inches(5.7), SW - 2 * MARGIN, Inches(0.85))
tf = panel_text(s, MARGIN, Inches(5.7), SW - 2 * MARGIN, Inches(0.85))
para(tf, [('Personal observations only — I did not measure footfall, sales or the effect of the Tripla renovation.', {})], size=11.5, color=GRAY, first=True, align=PP_ALIGN.CENTER, space_after=0)
notes(s, "Outside the digital research, two kiosks I use myself show how location shapes the format. Sello is a small, traditional kiosk — people grab something quick before the train. Tripla has been renovated into an open pass-through right by the platforms, with a proper self-service coffee station and meal combos; one combo I bought came with a free Red Bull. And a personal note: after nearly three years in Finland, R-kioski's blue and yellow has become a familiar, almost reassuring sight in cold, grey weather — a bit like a traveller spotting an inn through the snow, except the warm meal is a grilled-sausage hot dog and a coffee. These are my observations, not measurements.")

# ---------------------------------------------------------------- slide 11: PTT + Reddit
s = slide()
kicker_title(s, 'CONSUMER EVIDENCE · PTT 2025 + REDDIT', 'Finnish consumers consider price, quality and origin')
ptt = A / 'ptt_chart.png'
hp = Inches(4.35)
wp, _ = pic_h(ptt, hp)
pic(s, ptt, MARGIN, Inches(1.8), width=wp, height=hp)
tf = box(s, MARGIN, Inches(1.8) + hp + Inches(0.05), wp + Inches(0.5), Inches(0.5))
para(tf, [('Kuva 6, PTT 2025 (N = 1,197).', {})], size=9.5, color=GRAY, first=True, space_after=0)
lx = MARGIN + wp + Inches(0.55); lw = SW - lx - MARGIN
tf = box(s, lx, Inches(1.8), lw, Inches(2.1))
stats = [('63%', 'consider private labels clearly cheaper'),
         ('42%', 'consider quality equal to manufacturer brands'),
         ('58%', 'prefer a Finnish manufacturer brand over a foreign private label')]
for i, (n, d) in enumerate(stats):
    para(tf, [(n + '  ', {'bold': True, 'size': 22, 'color': ACCENT}), (d, {})], size=12.5, first=(i == 0), space_after=7, line=1.15)
para(tf, [('When both options are Finnish: 49% prefer the private label, 45% say it makes no difference.', {})], size=11, color=GRAY, space_after=0, line=1.2)
panel(s, lx, Inches(4.15), lw, Inches(2.5))
tf = panel_text(s, lx, Inches(4.15), lw, Inches(2.5))
para(tf, [('REDDIT, r/arkisuomi — “Parhaat ja paskat halpatuotteet” (c. 2023)', {})], size=10.5, color=ACCENT, bold=True, first=True, space_after=5)
para(tf, [('Pragmatic and product-specific: people recommended some products and rejected others from the same retailer. Interest in ingredients, recipes and actual manufacturers — one commenter identified Valio behind a Pirkka cheese. Occasional concern about pressure on supplier margins and Finnish production.', {})], size=11.5, color=GRAY, space_after=4, line=1.25)
para(tf, [('Anecdotal, ~3 years old, not representative — I use it for the questions consumers raise, not for measuring views.', {})], size=10.5, color=GRAY, space_after=0, line=1.2)
source_line(s, [('Sources: ', {}), ('PTT 2025', {'link': 'https://www.ptt.fi/julkaisut/ruuan-hinta-ratkaisee-kuluttajien-nakokulmia-ruuan-kulutukseen-ja-ruokamarkkinoihin/'}), (' · ', {}), ('Reddit thread', {'link': 'https://www.reddit.com/r/arkisuomi/comments/1d5glms/'})])
notes(s, "What do Finnish consumers actually think? In PTT's survey of almost 1,200 people, 63 percent consider private labels clearly cheaper and 42 percent consider the quality equal. But origin matters: 58 percent prefer a Finnish manufacturer brand over a foreign private label — and when both options are Finnish, preference shifts toward the private label. The Reddit discussion adds colour: people judge products individually, they check who actually manufactures them, and some worry about pressure on suppliers' margins. It is anecdotal, so I treat it as qualitative context, not measurement.")

# ---------------------------------------------------------------- slide 12: McKinsey
s = slide()
kicker_title(s, 'ARTICLE REFLECTION · McKINSEY 2020', 'Trying a product is not the same as buying it again')
tf = box(s, MARGIN, Inches(1.95), Inches(4.1), Inches(3.2))
para(tf, [('≈40%', {'bold': True, 'size': 34, 'color': ACCENT})], first=True, space_after=2)
para(tf, [('of surveyed US consumers tried new products or brands during COVID-19', {})], size=13, space_after=14, line=1.2)
para(tf, [('>45%', {'bold': True, 'size': 34, 'color': ACCENT})], space_after=2)
para(tf, [('of private-label switchers named price as their main reason — availability was another', {})], size=13, space_after=14, line=1.2)
para(tf, [('A lower price or a missing national brand can trigger trial. It does not establish preference or repeat purchase.', {})], size=12.5, color=GRAY, space_after=0, line=1.25)
mck = A / 'mckinsey_exhibit.png'
wm = Inches(7.4)
wm2, hm = pic_w(mck, wm)
pic(s, mck, SW - MARGIN - wm2, Inches(2.15), width=wm2, height=hm)
source_line(s, [('Begley & McOuat (2020) ', {}), ('Turning private labels into powerhouse brands', {'link': 'https://www.mckinsey.com/industries/retail/our-insights/turning-private-labels-into-powerhouse-brands'}), (', pp. 2–5. US pandemic-era research — not Finnish 2026 data.', {})])
notes(s, "The McKinsey article gave me the frame for interpreting all of this. During COVID, nearly 40 percent of surveyed US consumers tried new brands, and among those who switched to private labels, over 45 percent named price as the main reason. But trying is not the same as staying. The article's maturity model describes how retailers move from basic price-led ranges, through managing a portfolio of brands, to owning brands that compete on identity and quality. That distinction — trial versus loyalty — is what my price comparisons cannot see. And remember this is US data from 2020, not Finland in 2026.")

# ---------------------------------------------------------------- slide 13: KKV
s = slide()
kicker_title(s, 'FINNISH MARKET · KKV 2025', 'Private labels held around 26% of Finnish food sales value')
kkv = A / 'kkv_panels.png'
wk2 = Inches(7.2)
wk3, hk = pic_w(kkv, wk2)
pic(s, kkv, MARGIN, Inches(1.95), width=wk3, height=hk)
lx = MARGIN + wk3 + Inches(0.5); lw = SW - lx - MARGIN
tf = box(s, lx, Inches(2.1), lw, Inches(4.3))
para(tf, [('≈26%', {'bold': True, 'size': 34, 'color': ACCENT})], first=True, space_after=4)
para(tf, [('of Finnish food retail sales value, 2016–2023 — relatively stable', {})], size=13, space_after=12, line=1.25)
para(tf, [('Panels a–b: value share ≈ a quarter. Panels c–d: volume share ≈ a third. Two different measures — do not mix them.', {})], size=12, color=GRAY, space_after=12, line=1.3)
para(tf, [('The number of private-label products increased considerably over the same period, but the sales-value share did not grow with it.', {})], size=12.5, space_after=8, line=1.3)
para(tf, [('The data does not identify the reason — I do not claim one.', {})], size=11, color=GRAY, space_after=0, line=1.25)
source_line(s, [('Source: ', {}), ('Kilpailu- ja kuluttajavirasto (2025) Research Reports 3/2025', {'link': 'https://www.kkv.fi/tutkimus-ja-vaikuttaminen/julkaisut/tutkimusraportit/kaupan-omat-merkit-eli-private-label-tuotteet-elintarvikemarkkinoilla-tutkimusraportteja-3-2025/'}), (', Kuvio 1.', {})])
notes(s, "Finally, the market-level picture from the Finnish competition authority. Between 2016 and 2023, private labels held roughly a quarter of Finnish food sales value — and that share stayed relatively stable even as the number of private-label products increased considerably. The chart also shows why precision matters: the value share is about a quarter, while the volume share is about a third. They are different measures. For me this is the most interesting number in the whole project: more products did not automatically mean a bigger share. The data does not tell me why — and I do not pretend it does.")

# ---------------------------------------------------------------- slide 14: learnings
s = slide()
kicker_title(s, 'PART D · REFLECTION', 'What I learned from the research')
blocks = [
    ('SEGMENTATION', 'I expected different ranges at a station kiosk and a neighbourhood kiosk — the delivery menus were identical. Location suggests segments, but confirming them needs observation or sales data.'),
    ('BRANDING', 'Kesko, S Group and Lidl organise own brands differently, and consumers judge individual products, not whole ranges. I found no clear co-branded product.'),
    ('PACKAGING & PLACEMENT', 'Catalogues show prices, pack sizes, filters and promotions — not physical shelf position, packaging in use or in-store visibility.'),
    ('RESEARCH METHODS', 'Catalogues, Wolt menus, the PTT survey and Reddit comments each answer different questions. Their evidence is not interchangeable.'),
]
cw = Inches(5.85); chh = Inches(1.95); gap = Inches(0.3)
for i, (h, b) in enumerate(blocks):
    l = MARGIN + (i % 2) * (cw + gap)
    t = Inches(1.8) + (i // 2) * (chh + gap)
    panel(s, l, t, cw, chh)
    tf = panel_text(s, l, t, cw, chh)
    para(tf, [(h, {})], size=11, color=ACCENT, bold=True, first=True, space_after=5)
    para(tf, [(b, {})], size=12.5, color=INK, space_after=0, line=1.3)
panel(s, MARGIN, Inches(6.1), SW - 2 * MARGIN, Inches(0.95), fill=RGBColor(0xEA, 0xF0, 0xF6))
tf = panel_text(s, MARGIN, Inches(6.1), SW - 2 * MARGIN, Inches(0.95))
para(tf, [('The question I am left with:  what makes a customer choose an own-brand product again when their usual brand is available?', {})], size=15, color=ACCENT, bold=True, first=True, align=PP_ALIGN.CENTER, space_after=0)
notes(s, "Four things I take from this assignment. Segmentation: I expected a station kiosk and a neighbourhood kiosk to offer different food — the delivery menus listed the same six filled breads at the same prices. Location hints at who shops somewhere, but menus cannot confirm it. Branding: the three retailers run genuinely different brand structures, and consumers judge products one by one — I did not find a clear co-branded product. Packaging and placement: digital catalogues show a lot, but not the physical shelf. And methods: each source answers a different question, so I tried not to treat them as interchangeable. My own question shifted during the project — from which product is cheaper, to what makes someone choose it again when their usual brand is available.")

# ---------------------------------------------------------------- slide 15: sources
s = slide()
kicker_title(s, 'SOURCES', 'Sources and research material')
colw = (SW - 2 * MARGIN - Inches(0.4)) / 2
lx2 = MARGIN + colw + Inches(0.4)
links_left = [
    ('RETAIL & MARKET DATA', None),
    ('Kesko — Pirkka and K-Menu', 'https://www.kesko.fi/en/company/brands/own-brands/pirkka-and-k-menu/'),
    ('S-kaupat — Own brands', 'https://www.s-kaupat.fi/sivu/omat-merkit'),
    ('S-kaupat — Crisp listings', 'https://www.s-kaupat.fi/tuotteet/snacksit/sipsit/perunalastut'),
    ('K-Ruoka — Snacks catalogue', 'https://www.k-ruoka.fi/kauppa/tuotehaku/makeiset-ja-naposteltavat/sipsit-ja-snacksit'),
    ('Lidl — Quality and own-brand range', 'https://corporate.lidl.fi/laatu-kuuluu-kaikille'),
    ('Lidl — Kartanon', 'https://www.lidl.fi/c/kartanon/s10034513'),
    ('KKV — Private labels in Finnish food markets (3/2025)', 'https://www.kkv.fi/tutkimus-ja-vaikuttaminen/julkaisut/tutkimusraportit/kaupan-omat-merkit-eli-private-label-tuotteet-elintarvikemarkkinoilla-tutkimusraportteja-3-2025/'),
]
links_right = [
    ('R-KIOSKI, CONSUMERS & RESEARCH', None),
    ('Wolt — Rautatieasema', 'https://wolt.com/en/fin/helsinki/venue/r-kioski-helsinki-rautatieasema-scandic-grand-central'),
    ('Wolt — Vuosaari', 'https://wolt.com/fi/fin/helsinki/venue/r-kioski-helsinki-vuosaari-kaivonkatsojantie-13'),
    ('Wolt — Punavuori', 'https://wolt.com/en/fin/helsinki/venue/r-kioski-helsinki-punavuori-fredrikinkatu-12'),
    ('Begley & McOuat — McKinsey (2020)', 'https://www.mckinsey.com/industries/retail/our-insights/turning-private-labels-into-powerhouse-brands'),
    ('PTT — Ruuan hinta ratkaisee (2025)', 'https://www.ptt.fi/julkaisut/ruuan-hinta-ratkaisee-kuluttajien-nakokulmia-ruuan-kulutukseen-ja-ruokamarkkinoihin/'),
    ('Reddit — Parhaat ja paskat halpatuotteet', 'https://www.reddit.com/r/arkisuomi/comments/1d5glms/'),
    ('GitHub — data and code', 'https://github.com/smyrnav/arcada-coursework/tree/main/2026-autumn/introduction-to-marketing/private-label-retail-analytics'),
]
for lx3, links in ((MARGIN, links_left), (lx2, links_right)):
    tf = box(s, lx3, Inches(1.85), colw, Inches(4.3))
    for i, (label, url) in enumerate(links):
        if url is None:
            para(tf, [(label, {})], size=11, color=ACCENT, bold=True, first=(i == 0), space_after=8)
        else:
            para(tf, [(label, {'link': url})], size=12.5, first=False, space_after=8)
tf = box(s, MARGIN, Inches(6.35), SW - 2 * MARGIN, Inches(0.7))
para(tf, [('AI disclosure: AI assisted with report and slide structure and text editing. Research, source selection, observations, analysis and findings are my own. All calculations were run in Python. Product and menu listings accessed 24 November 2026 unless otherwise stated.', {})], size=9.5, color=GRAY, first=True, space_after=0, line=1.3)
notes(s, "These are the sources behind everything you have seen — the retailer catalogues, the three Wolt menus, the KKV and PTT research, the McKinsey article and the Reddit thread. The full dataset, code and evidence screenshots are in the GitHub repository if you want to verify any figure. Thank you.")

prs.save(OUT)
print('saved', OUT, prs.slide_width, prs.slide_height, len(prs.slides.__iter__.__self__._sldIdLst))
