"""Build the final reflective presentation (10 slides, 16:9)."""
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / 'presentation' / 'assets'
OUT = ROOT / 'presentation' / 'presentation.pptx'

INK = RGBColor(0x1F, 0x29, 0x37)
GRAY = RGBColor(0x6B, 0x72, 0x80)
ACCENT = RGBColor(0x0F, 0x4C, 0x81)
RED = RGBColor(0xC6, 0x28, 0x28)
LIGHT = RGBColor(0xF3, 0xF4, 0xF6)
SOFT = RGBColor(0xEA, 0xF0, 0xF6)

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
    tf = box(s, MARGIN, Inches(0.45), SW - 2 * MARGIN, Inches(0.32))
    para(tf, [(kicker, {})], size=11, color=ACCENT, bold=True, first=True)
    tf2 = box(s, MARGIN, Inches(0.78), SW - 2 * MARGIN, Inches(1.0))
    para(tf2, [(title, {})], size=title_size, color=INK, bold=True, first=True, space_after=0)


def source_line(s, parts, top=None):
    tf = box(s, MARGIN, top if top is not None else SH - Inches(0.5), SW - 2 * MARGIN, Inches(0.4))
    para(tf, parts, size=9.5, color=GRAY, first=True, space_after=0)


def pic(s, path, left, top, width=None, height=None):
    return s.shapes.add_picture(str(path), left, top, width=width, height=height)


def pic_h(path, h):
    im = Image.open(path)
    return Emu(int(h * im.size[0] / im.size[1])), h


def panel(s, l, t, w, h, fill=LIGHT):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def panel_text(s, l, t, w, h, pad=0.18):
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
para(tf, [('Private labels across Finnish grocery shops', {})], size=33, color=INK, bold=True, space_after=18, line=1.05)
para(tf, [('Reflections on what product data can — and cannot — tell me about why customers choose own brands.', {})], size=16, color=GRAY, space_after=30, line=1.2)
para(tf, [('Smyrna V.', {})], size=14, color=INK, bold=True, space_after=2)
para(tf, [('Introduction to Marketing 2026 · Arcada University of Applied Sciences', {})], size=12, color=GRAY, space_after=0)
tf = box(s, Inches(0.75), SH - Inches(0.55), Inches(6.5), Inches(0.35))
para(tf, [('Cover photo: ', {}), ('Helsinki Times', {'link': 'https://www.helsinkitimes.com/finland/finland-news/domestic/16483-grocery-retailers-in-the-dark-about-plans-to-tackle-private-label-products.html'})], size=9.5, color=GRAY, first=True, space_after=0)
notes(s, "Hi, I'm Smyrna. This presentation is not a repeat of my report — the numbers are all in there if you want them. What I want to do here is tell you what doing this research actually made me think about: what surprised me, what changed my mind, and what I'm still wondering about private labels in Finnish retail.")

# ---------------------------------------------------------------- slide 2: the question
s = slide()
kicker_title(s, 'INTRODUCTION', 'What I set out to understand')
tf = box(s, MARGIN, Inches(1.9), Inches(11.0), Inches(1.6))
para(tf, [('How do Finnish retailers use their own brands — and what can product data tell me about why customers choose them?', {})], size=24, color=INK, bold=True, first=True, line=1.15, space_after=0)
panel(s, MARGIN, Inches(3.7), SW - 2 * MARGIN, Inches(1.5))
tf = panel_text(s, MARGIN, Inches(3.7), SW - 2 * MARGIN, Inches(1.5))
para(tf, [('HOW I RESEARCHED IT', {})], size=10.5, color=ACCENT, bold=True, first=True, space_after=5)
para(tf, [('Digitally, not in stores: retailer catalogues (Kesko, S Group, Lidl), R-kioski delivery menus, and consumer research (KKV, PTT, McKinsey). Listings and prices collected 24 Nov 2026, compiled into datasets and analysed in Python.', {})], size=13, color=GRAY, space_after=0, line=1.3)
tf = box(s, MARGIN, Inches(5.55), SW - 2 * MARGIN, Inches(1.0))
para(tf, [('One honesty note before anything else: ', {'bold': True}), ('no store visits, no shelf photos, no customer observation. A lot of what follows is about exactly that — what this method can show, and where it runs out.', {})], size=14, color=INK, first=True, space_after=0, line=1.3)
source_line(s, [('Data, code and sources: ', {}), ('github.com/smyrnav/arcada-coursework', {'link': 'https://github.com/smyrnav/arcada-coursework/tree/main/2026-autumn/introduction-to-marketing/private-label-retail-analytics'})])
notes(s, "My starting question was simple: how do Finnish retailers use their own brands, and what can product data tell me about why customers choose them. I researched it digitally — retailer catalogues, delivery menus and published consumer research, all analysed in Python. And one honesty note up front: I didn't visit stores or observe customers. That limitation turned out to be one of the most interesting parts of the whole project, so keep it in mind.")

# ---------------------------------------------------------------- slide 3: three surprises
s = slide()
kicker_title(s, 'WHAT SURPRISED ME', 'Three findings I did not expect')
surprises = [
    ('The price gaps were bigger than I expected',
     'Sampled Pirkka, Xtra and Coop crisps were 23–33% cheaper per kg than the matched Taffel products. Which made me ask: if the difference is that big, why doesn\u2019t everyone just buy the cheaper one?'),
    ('Two very different kiosks sold exactly the same food',
     'I expected a central station kiosk and a neighbourhood kiosk to offer different ranges. Their delivery menus listed the same six filled breads at the same prices. My assumption about location-based segmentation was too easy.'),
    ('The same baguette cost 37.5% more at the kiosk',
     'A 200 g chicken Caesar baguette: €4.80 as R Patonki at R-kioski, €3.49 as Chef Lunden at K-Ruoka. Apparently you are not only paying for the bread — location and immediacy are part of the price.'),
]
top = Inches(1.75); ph = Inches(1.55); gap = Inches(0.22)
for i, (h, b) in enumerate(surprises):
    t = top + i * (ph + gap)
    panel(s, MARGIN, t, SW - 2 * MARGIN, ph)
    tf = panel_text(s, MARGIN, t, SW - 2 * MARGIN, ph)
    para(tf, [(f'{i + 1}.  ', {'bold': True, 'color': ACCENT, 'size': 16}), (h, {'bold': True})], size=15, first=True, space_after=4)
    para(tf, [(b, {})], size=12.5, color=GRAY, space_after=0, line=1.25)
source_line(s, [('Full price tables and product data are in the report — this is what they made me think.')])
notes(s, "Three things genuinely surprised me. First, the price gaps: the own-brand crisps I sampled were 23 to 33 percent cheaper per kilo than the matched Taffel products. That's a big gap — and it immediately raises the question of why everyone doesn't just buy the cheaper one. Second, the identical kiosk menus: I was sure a station kiosk and a neighbourhood kiosk would sell different things. Same six products, same prices. My segmentation assumption was too easy. And third, the baguette: same weight, same filling, 37.5 percent more at the kiosk. That told me location and immediacy are literally part of the price.")

# ---------------------------------------------------------------- slide 4: the number that changed the question
s = slide()
kicker_title(s, 'THE FINDING THAT STAYED WITH ME', 'The number that changed my question')
tf = box(s, MARGIN, Inches(2.1), Inches(4.6), Inches(3.6))
para(tf, [('≈26%', {'bold': True, 'size': 60, 'color': ACCENT})], first=True, space_after=6)
para(tf, [('private-label share of Finnish food sales value, 2016–2023', {})], size=14, space_after=8, line=1.25)
para(tf, [('Stable — even though retailers kept adding more own-brand products. (Value share ≈ a quarter; volume share ≈ a third — two different measures.)', {})], size=11.5, color=GRAY, space_after=0, line=1.3)
lx = Inches(5.8); lw = SW - lx - MARGIN
tf = box(s, lx, Inches(2.1), lw, Inches(4.6))
para(tf, [('More products did not mean a bigger share.', {'bold': True, 'size': 17})], size=17, first=True, space_after=10, line=1.25)
para(tf, [('That is when I stopped asking “which product is cheaper?” and started asking what makes people come back.', {})], size=14, space_after=10, line=1.3)
para(tf, [('The McKinsey article gave me the words for it: a low price — or an empty shelf during a crisis — can trigger a trial purchase. But trial is not loyalty. Getting someone to try a product once is a different problem from giving them a reason to choose it again.', {})], size=14, space_after=0, line=1.3)
source_line(s, [('Sources: ', {}), ('KKV, Research Reports 3/2025', {'link': 'https://www.kkv.fi/tutkimus-ja-vaikuttaminen/julkaisut/tutkimusraportit/kaupan-omat-merkit-eli-private-label-tuotteet-elintarvikemarkkinoilla-tutkimusraportteja-3-2025/'}), (' · ', {}), ('Begley & McOuat, McKinsey (2020)', {'link': 'https://www.mckinsey.com/industries/retail/our-insights/turning-private-labels-into-powerhouse-brands'})])
notes(s, "This is the number that stayed with me. Between 2016 and 2023, private labels held roughly a quarter of Finnish food sales value — and that share barely moved, even though retailers kept adding more and more own-brand products. More products, same share. That's when my question changed. It stopped being about which product is cheaper, and became about what makes people come back. The McKinsey article gave me the vocabulary: price or availability can trigger a trial, but trial is not loyalty. And honestly, that reframed everything else I had found.")

# ---------------------------------------------------------------- slide 5: what prices cannot tell me
s = slide()
kicker_title(s, 'METHOD AS A LESSON', 'What a price comparison cannot tell me')
points = [
    'A catalogue shows prices and pack sizes — not who buys the product, or why.',
    'A promotion can flip the comparison. I saw Taffel Plussa multi-buy offers next to regular-price own brands, so any single price snapshot is fragile.',
    'An online listing is not a shelf. No height, no facings, no visibility.',
    'A delivery menu is not a store. Wolt shows what can be ordered, not the full range — and not the customers.',
]
tf = box(s, MARGIN, Inches(1.95), Inches(11.6), Inches(3.6))
for i, p_ in enumerate(points):
    para(tf, [('—  ', {'color': ACCENT, 'bold': True}), (p_, {})], size=15.5, first=(i == 0), space_after=14, line=1.3)
panel(s, MARGIN, Inches(5.6), SW - 2 * MARGIN, Inches(1.15), fill=SOFT)
tf = panel_text(s, MARGIN, Inches(5.6), SW - 2 * MARGIN, Inches(1.15))
para(tf, [('Digital research is good at “what” and “how much”. It is bad at “who” and “why” — and the “why” is the interesting part.', {})], size=15, color=ACCENT, bold=True, first=True, align=PP_ALIGN.CENTER, space_after=0)
notes(s, "Doing this digitally taught me something about research itself. A catalogue gives me prices and pack sizes, but not people. A promotion can flip a price comparison overnight — I literally saw Taffel multi-buy offers sitting next to regular-price own brands. An online listing is not a shelf, and a delivery menu is not a store. So my method is good at answering 'what' and 'how much', and genuinely bad at 'who' and 'why'. And the why is the interesting part. I'd rather tell you that honestly than pretend my data says more than it does.")

# ---------------------------------------------------------------- slide 6: not only about price
s = slide()
kicker_title(s, 'WHAT CONSUMERS ACTUALLY CARE ABOUT', 'It is not only about price')
tf = box(s, MARGIN, Inches(2.0), Inches(5.2), Inches(4.2))
stats = [('63%', 'consider private labels clearly cheaper'),
         ('42%', 'consider the quality equal to manufacturer brands'),
         ('58%', 'prefer a Finnish manufacturer brand over a foreign private label')]
for i, (n, d) in enumerate(stats):
    para(tf, [(n + '  ', {'bold': True, 'size': 30, 'color': ACCENT}), (d, {})], size=13.5, first=(i == 0), space_after=12, line=1.2)
para(tf, [('But when both options are Finnish, 49% prefer the private label.', {})], size=12.5, color=GRAY, space_after=0, line=1.25)
lx = Inches(6.3); lw = SW - lx - MARGIN
panel(s, lx, Inches(2.0), lw, Inches(4.1))
tf = panel_text(s, lx, Inches(2.0), lw, Inches(4.1))
para(tf, [('WHAT I MAKE OF THIS', {})], size=10.5, color=ACCENT, bold=True, first=True, space_after=6)
para(tf, [('Price opens the door. Origin and trust decide.', {'bold': True, 'size': 15})], size=15, space_after=8)
para(tf, [('In a Finnish Reddit thread about budget products, people judged items one by one — recommending some and rejecting others from the same retailer. Several dug into who actually manufactures the product; one identified Valio behind a Pirkka cheese.', {})], size=12.5, color=GRAY, space_after=8, line=1.3)
para(tf, [('Consumers do not buy “the cheap brand”. They buy products they trust — and they do their detective work.', {})], size=12.5, space_after=0, line=1.3)
source_line(s, [('Sources: ', {}), ('PTT 2025 (n = 1,197)', {'link': 'https://www.ptt.fi/julkaisut/ruuan-hinta-ratkaisee-kuluttajien-nakokulmia-ruuan-kulutukseen-ja-ruokamarkkinoihin/'}), (' · ', {}), ('r/arkisuomi thread (anecdotal, c. 2023)', {'link': 'https://www.reddit.com/r/arkisuomi/comments/1d5glms/'})])
notes(s, "So if price gaps of 30 percent don't automatically win customers, what does? The PTT survey gave me part of the answer. Yes, most people see private labels as cheaper, and nearly half see the quality as equal. But 58 percent prefer a Finnish manufacturer brand over a foreign private label — and when both options are Finnish, preference actually flips toward the private label. Origin matters. And the Reddit thread showed me the same thing from the ground level: people judge products individually, and they check who actually makes them. One commenter had identified Valio behind a Pirkka cheese. Consumers do detective work. They don't buy 'the cheap brand' — they buy products they trust.")

# ---------------------------------------------------------------- slide 7: being the customer
s = slide()
kicker_title(s, 'PERSONAL OBSERVATION', 'What I noticed as a customer, not as a researcher')
cw = Inches(5.85); gap = Inches(0.35); top = Inches(1.8); ph = Inches(2.35)
panel(s, MARGIN, top, cw, ph)
tf = panel_text(s, MARGIN, top, cw, ph)
para(tf, [('SELLO', {})], size=11, color=ACCENT, bold=True, first=True, space_after=5)
para(tf, [('A compact kiosk before the train', {'bold': True, 'size': 15})], size=15, space_after=6)
para(tf, [('Small format. I mostly see office workers, students and passengers picking up something small before boarding.', {})], size=12.5, color=GRAY, space_after=0, line=1.3)
panel(s, MARGIN + cw + gap, top, cw, ph)
tf = panel_text(s, MARGIN + cw + gap, top, cw, ph)
para(tf, [('TRIPLA', {})], size=11, color=ACCENT, bold=True, first=True, space_after=5)
para(tf, [('A stop designed for transfer', {'bold': True, 'size': 15})], size=15, space_after=6)
para(tf, [('Renovated into an open pass-through by platforms 8–11, with a proper self-service coffee station and meal combos — one I bought came with a free Red Bull. Built for people changing between trains and trams.', {})], size=12.5, color=GRAY, space_after=0, line=1.3)
panel(s, MARGIN, Inches(4.55), SW - 2 * MARGIN, Inches(2.0), fill=SOFT)
tf = panel_text(s, MARGIN, Inches(4.55), SW - 2 * MARGIN, Inches(2.0), pad=0.25)
para(tf, [('After nearly three years in Finland, R-kioski\u2019s blue and yellow has become a strangely reassuring sight in cold, grey weather — like a traveller in a novel spotting an inn through the snow. Except the warm meal is a grilled-sausage hot dog and a coffee.', {'italic': True})], size=14.5, color=INK, first=True, space_after=6, line=1.35)
para(tf, [('Brand experience is real — and it is not in any dataset I collected. Personal observations, not measurements.', {})], size=11.5, color=GRAY, space_after=0)
notes(s, "And then there's what I noticed simply by being a customer. Sello and Tripla are both R-kiosks, but they're built for completely different moments — a quick stop before the train versus a pass-through between platforms, where the renovation and the coffee station actually changed how the place feels. And a personal note: after almost three years in Finland, that blue and yellow has become a reassuring sight in grey weather — like spotting an inn through the snow, except the warm meal is a grilled-sausage hot dog. None of that is in my dataset. But it's exactly the kind of thing that makes someone choose a brand again.")

# ---------------------------------------------------------------- slide 8: what I learned
s = slide()
kicker_title(s, 'PART D · REFLECTION', 'What I learned from the research')
blocks = [
    ('SEGMENTATION', 'I expected different ranges at a station kiosk and a neighbourhood kiosk — the delivery menus were identical. Location suggests segments; confirming them needs observation or sales data.'),
    ('BRANDING', 'Three retailers, three logics: Kesko uses one tiered family (K-Menu, Pirkka, Pirkka Parhaat), S Group separate brands (Xtra, Coop, Kotimaista), Lidl a long tail of category names. And consumers judge products one by one — I found no clear co-branded product.'),
    ('PACKAGING & PLACEMENT', 'Catalogues show prices, pack sizes, filters and promotions — not physical shelf position, packaging in use or visibility. I can describe the digital shelf, not the real one.'),
    ('RESEARCH METHODS', 'Catalogues, delivery menus, surveys and Reddit comments each answer different questions. Treating them as interchangeable evidence was the first mistake I had to unlearn.'),
]
cw = Inches(5.85); chh = Inches(2.1); gap = Inches(0.28)
for i, (h, b) in enumerate(blocks):
    l = MARGIN + (i % 2) * (cw + gap)
    t = Inches(1.8) + (i // 2) * (chh + gap)
    panel(s, l, t, cw, chh)
    tf = panel_text(s, l, t, cw, chh)
    para(tf, [(h, {})], size=11, color=ACCENT, bold=True, first=True, space_after=5)
    para(tf, [(b, {})], size=12, color=INK, space_after=0, line=1.3)
source_line(s, [('Part D of the report covers each of these in full.')])
notes(s, "Four things I take with me. Segmentation: it's easy to invent customer groups from a location — the identical menus proved my own assumption wrong. Branding: the three retailers run genuinely different brand logics, and consumers still judge products one by one. Placement: I can describe the digital shelf honestly, but not the physical one. And methods: every source answers a different question, and the first mistake I had to unlearn was treating them as interchangeable.")

# ---------------------------------------------------------------- slide 9: closing question
s = slide()
tf = box(s, Inches(1.6), Inches(2.5), SW - Inches(3.2), Inches(2.6))
para(tf, [('What makes a customer choose an own-brand product again — when their usual brand is right there, available?', {})], size=30, color=INK, bold=True, first=True, align=PP_ALIGN.CENTER, space_after=18, line=1.2)
para(tf, [('That is the question this project left me with. And it is the one I would research next.', {})], size=16, color=GRAY, align=PP_ALIGN.CENTER, space_after=0)
notes(s, "So that's where I landed. Price gets a product tried once. What gets it chosen again — trust, quality, origin, habit, even the feeling of a familiar blue-and-yellow kiosk — that's the question this project left me with, and it's the one I'd actually enjoy researching next. Thank you.")

# ---------------------------------------------------------------- slide 10: sources
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
notes(s, "All the sources — catalogues, delivery menus, the research reports and the article — plus the GitHub repository with the full dataset, code and evidence screenshots, if you want to verify anything. Thank you for listening.")

prs.save(OUT)
print('saved', OUT, len(prs.slides._sldIdLst))
