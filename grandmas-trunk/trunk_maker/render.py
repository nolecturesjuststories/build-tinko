"""Draw Grandma's trunk: fictional family papers rendered as old, scanned pages.

Every document is drawn with code (no AI images), so every word in it is known and the answers can be checked.
Pages get the look of a real scan: paper texture, a slight tilt, faded ink, a stain or a fold, so that
Document Intelligence has real work to do (handwriting, tables, forms, stamps).

Fonts are the ones that ship with macOS. The finished PDFs are committed in ../trunk, so you only need this file
if you want to change or regenerate the trunk.
"""
import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

DPI = 150
A5 = (874, 1240)
A4 = (1240, 1754)
CARD = (900, 600)  # 6 x 4 inch recipe / index card

SYS = '/System/Library/Fonts/'
SUP = SYS + 'Supplemental/'
FONTS = {
    'mohan': SUP + 'Bradley Hand Bold.ttf',  # Grandpa's slanted hand
    'kamla': SYS + 'Noteworthy.ttc',  # Grandma's round hand
    'savitri': SUP + 'ChalkboardSE.ttc',  # Kamla's sister
    'young': SYS + 'MarkerFelt.ttc',  # Arun and Meera as young adults
    'typewriter': SUP + 'AmericanTypewriter.ttc',
    'telegram': SUP + 'Courier New Bold.ttf',
    'mono': SUP + 'Courier New.ttf',
    'print': SYS + 'Helvetica.ttc',
    'serif': SUP + 'Georgia.ttf',
    'serif_bold': SUP + 'Georgia Bold.ttf',
    'fancy': SUP + 'Apple Chancery.ttf',
}

INK = {
    'blue': (28, 46, 120),
    'black': (32, 30, 34),
    'royal': (24, 60, 150),
    'brown': (70, 45, 30),
    'red': (160, 30, 30),
}


def font(name, size):
    return ImageFont.truetype(FONTS[name], size)


# ── Paper ──────────────────────────────────────────────────────────────────────────────────────────────────────────

def paper(size, tone=(244, 236, 214), grain=10, seed=0):
    """Aged paper: a base tone, fine grain and a soft darker edge."""
    rnd = random.Random(seed)
    w, h = size
    img = Image.new('RGB', size, tone)
    noise = Image.effect_noise(size, grain).convert('L')
    img = Image.blend(img, Image.merge('RGB', (noise, noise, noise)), 0.06)
    # yellowed edges
    edge = Image.new('L', size, 0)
    d = ImageDraw.Draw(edge)
    for i in range(40):
        a = int(70 * (1 - i / 40) ** 2)
        d.rectangle((i, i, w - 1 - i, h - 1 - i), outline=a)
    tint = Image.new('RGB', size, (190, 160, 110))
    img = Image.composite(tint, img, edge.filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * 0.55)))
    # a few fibres
    d = ImageDraw.Draw(img)
    for _ in range(int(w * h / 60000)):
        x, y = rnd.randrange(w), rnd.randrange(h)
        d.line((x, y, x + rnd.randint(-12, 12), y + rnd.randint(-12, 12)), fill=tuple(c - 25 for c in tone), width=1)
    return img


def ruled(img, top, gap, left_margin=None, color=(150, 170, 205)):
    d = ImageDraw.Draw(img)
    w, h = img.size
    y = top
    while y < h - 40:
        d.line((30, y, w - 30, y), fill=color, width=1)
        y += gap
    if left_margin:
        d.line((left_margin, 20, left_margin, h - 20), fill=(215, 140, 140), width=2)
    return img


# ── Writing ────────────────────────────────────────────────────────────────────────────────────────────────────────

def wrap(text, f, width):
    lines = []
    for para in text.split('\n'):
        words, cur = para.split(' '), ''
        for wd in words:
            t = (cur + ' ' + wd).strip()
            if f.getlength(t) <= width:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = wd
        lines.append(cur)
    return lines


def write(img, xy, text, fname, size, ink, width, gap=None, hand=True, seed=1, align='left'):
    """Write wrapped text. Handwriting gets a wobbling baseline, uneven pressure and a slight per-line tilt.
    Returns the y position after the last line."""
    rnd = random.Random(seed)
    f = font(fname, size)
    gap = gap or int(size * 1.45)
    x0, y = xy
    for line in wrap(text, f, width):
        if not line:
            y += gap
            continue
        lw = int(f.getlength(line)) + 20
        layer = Image.new('L', (lw + 40, gap + size), 0)
        d = ImageDraw.Draw(layer)
        cx = 10
        for word in line.split(' '):
            dy = rnd.uniform(-2.2, 2.2) if hand else 0
            alpha = rnd.randint(205, 255) if hand else 245
            d.text((cx, size * 0.25 + dy), word, font=f, fill=alpha)
            cx += f.getlength(word + ' ')
        if hand:
            layer = layer.rotate(rnd.uniform(-0.7, 0.7), resample=Image.BICUBIC, expand=False)
        x = x0 if align == 'left' else x0 + (width - lw) // 2 if align == 'center' else x0 + width - lw
        ink_layer = Image.new('RGB', layer.size, ink)
        img.paste(ink_layer, (int(x), int(y - size * 0.25)), layer)
        y += gap
    return y


def text(img, xy, s, fname, size, fill=INK['black'], anchor='la'):
    ImageDraw.Draw(img).text(xy, s, font=font(fname, size), fill=fill, anchor=anchor)


# ── Age and scan ───────────────────────────────────────────────────────────────────────────────────────────────────

def stain(img, seed, n=1, color=(150, 110, 60), max_r=90):
    """Tea / turmeric / ghee rings."""
    rnd = random.Random(seed)
    w, h = img.size
    for _ in range(n):
        r = rnd.randint(max_r // 2, max_r)
        cx, cy = rnd.randint(r, w - r), rnd.randint(r, h - r)
        mask = Image.new('L', img.size, 0)
        d = ImageDraw.Draw(mask)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=38)
        d.ellipse((cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5), fill=16)
        mask = mask.filter(ImageFilter.GaussianBlur(4))
        img = Image.composite(Image.new('RGB', img.size, color), img, mask)
    return img


def blot(img, xy, r=10, color=INK['blue'], seed=0):
    """An ink smudge (used on purpose: it can make a 6 look like a 5)."""
    rnd = random.Random(seed)
    mask = Image.new('L', img.size, 0)
    d = ImageDraw.Draw(mask)
    x, y = xy
    for _ in range(14):
        rr = rnd.uniform(r * 0.4, r)
        ox, oy = rnd.uniform(-r * 0.6, r * 0.6), rnd.uniform(-r * 0.4, r * 0.4)
        d.ellipse((x + ox - rr, y + oy - rr * 0.7, x + ox + rr, y + oy + rr * 0.7), fill=150)
    mask = mask.filter(ImageFilter.GaussianBlur(1.6))
    return Image.composite(Image.new('RGB', img.size, color), img, mask)


def fold(img, horizontal=True, at=0.5):
    w, h = img.size
    d = ImageDraw.Draw(img, 'RGBA')
    if horizontal:
        y = int(h * at)
        d.line((0, y, w, y), fill=(120, 100, 80, 70), width=2)
        d.line((0, y + 2, w, y + 2), fill=(255, 255, 255, 60), width=2)
    else:
        x = int(w * at)
        d.line((x, 0, x, h), fill=(120, 100, 80, 70), width=2)
        d.line((x + 2, 0, x + 2, h), fill=(255, 255, 255, 60), width=2)
    return img


def stamp(img, xy, label, sub='', color=INK['red'], angle=-12, size=34):
    """A rubber stamp: PAID, RECEIVED, a post-office date stamp."""
    f, fs = font('print', size), font('print', int(size * 0.45))
    w = int(max(f.getlength(label), fs.getlength(sub)) + 40)
    h = int(size * (2.1 if sub else 1.6))
    layer = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((3, 3, w - 3, h - 3), radius=10, outline=200, width=4)
    d.text((w // 2, size * 0.75), label, font=f, fill=200, anchor='mm')
    if sub:
        d.text((w // 2, size * 1.55), sub, font=fs, fill=190, anchor='mm')
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    noise = Image.effect_noise(layer.size, 60).point(lambda v: 255 if v > 90 else 120)
    layer = ImageChops.multiply(layer, noise)
    img.paste(Image.new('RGB', layer.size, color), xy, layer)
    return img


def scan(img, seed, tilt=1.2, fade=0.12, blur=0.55):
    """Make it look scanned: faded, a little soft, slightly crooked on a grey scanner bed."""
    rnd = random.Random(seed)
    img = Image.blend(img, Image.new('RGB', img.size, (236, 228, 210)), fade)
    img = img.filter(ImageFilter.GaussianBlur(blur))
    angle = rnd.uniform(-tilt, tilt)
    bed = (205, 205, 200)
    img = img.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=bed)
    pad = Image.new('RGB', (img.width + 40, img.height + 40), bed)
    pad.paste(img, (20, 20))
    return pad


def save_pdf(pages, path):
    pages[0].save(path, save_all=True, append_images=pages[1:], resolution=DPI, quality=82)


# ── Layouts ────────────────────────────────────────────────────────────────────────────────────────────────────────

def letter(doc):
    """A handwritten letter on ruled paper (1–2 pages). doc: hand, ink, date, place, greeting, body, closing, sign."""
    seed = doc['seed']
    hand = doc.get('hand', 'mohan')
    size = doc.get('size', 34 if hand == 'mohan' else 31)
    body = doc['body']
    pages, chunk = [], []
    # split long letters over two pages by paragraph
    paras = body.split('\n\n')
    first, second = (paras, []) if len(body) < 1100 else (paras[: len(paras) // 2 + 1], paras[len(paras) // 2 + 1 :])
    for i, part in enumerate([first, second]):
        if not part:
            continue
        pg = ruled(paper(A5, seed=seed + i), top=150, gap=int(size * 1.45))
        y = 70
        if i == 0:
            write(pg, (480, 60), doc['place'] + '\n' + doc['date'], hand, size - 4, INK[doc['ink']], 340, seed=seed, align='right')
            if doc.get('smudge_year'):
                # an ink smudge on the lower loop of the year's third digit (the 6 of 1968), the way a real scan
                # can turn a 6 into a 5; used for the "Meera born 1958?" mistake in Part 3
                f = font(hand, size - 4)
                line = doc['date']
                x = 480 + 340 - (int(f.getlength(line)) + 20) + 10 + f.getlength(line[:-2])
                yy = 60 + int((size - 4) * 1.45) + (size - 4) * 0.72
                pg = blot(pg, (x + f.getlength('6') * 0.3, yy), r=(size - 4) * 0.2, color=INK[doc['ink']], seed=seed)
            y = write(pg, (70, 190), doc['greeting'], hand, size, INK[doc['ink']], 740, gap=int(size * 1.45), seed=seed + 2)
        else:
            y = 150
        y = write(pg, (90, y + 6), '\n\n'.join(part), hand, size, INK[doc['ink']], 720, gap=int(size * 1.45), seed=seed + 3 + i)
        if i == (1 if second else 0):
            y = write(pg, (380, y + 20), doc['closing'], hand, size, INK[doc['ink']], 420, seed=seed + 5)
            write(pg, (420, y), doc['sign'], hand, size + 4, INK[doc['ink']], 380, seed=seed + 6)
        for xy, r in doc.get('blots', []):
            pg = blot(pg, xy, r, INK[doc['ink']], seed)
        if doc.get('stain'):
            pg = stain(pg, seed, 1)
        pg = fold(pg, True, 0.33)
        pg = fold(pg, True, 0.66)
        pages.append(scan(pg, seed + i))
    return pages


def telegram(doc):
    """A telegram form with pasted ticker-tape strips. doc: date, origin, to, words (list of strips)."""
    seed = doc['seed']
    pg = paper((1240, 760), tone=(232, 226, 200), seed=seed)
    d = ImageDraw.Draw(pg)
    text(pg, (620, 50), 'TELEGRAM', 'serif_bold', 56, INK['black'], anchor='mm')
    text(pg, (620, 100), 'POSTS AND TELEGRAPHS', 'print', 22, INK['black'], anchor='mm')
    for x0, label, val in ((60, 'Office of Origin', doc['origin']), (520, 'Date', doc['date']), (900, 'Time', doc.get('time', '10.40'))):
        text(pg, (x0, 150), label, 'print', 22)
        text(pg, (x0, 182), val, 'mono', 28, INK['blue'])
    d.line((50, 230, 1190, 230), fill=INK['black'], width=2)
    text(pg, (60, 255), 'To', 'print', 22)
    write(pg, (130, 252), doc['to'], 'kamla' if doc.get('hand_to') else 'mono', 30, INK['blue'], 1000, hand=bool(doc.get('hand_to')), seed=seed)
    y = 340
    for strip in doc['words']:
        f = font('telegram', 30)
        w = int(f.getlength(strip)) + 30
        d.rectangle((70, y, 70 + w, y + 46), fill=(250, 248, 240), outline=(200, 195, 180))
        d.text((85, y + 8), strip, font=f, fill=INK['black'])
        y += 62
    stamp(pg, (900, 520), doc['origin'].split()[0], doc['date'], INK['brown'], angle=8, size=30)
    pg = fold(pg, False, 0.5)
    return [scan(pg, seed, tilt=1.5)]


def recipe(doc):
    """A recipe card in Grandma's hand. doc: title, year, ingredients (list), method, note."""
    seed = doc['seed']
    pg = ruled(paper(CARD, tone=(250, 246, 232), seed=seed), top=120, gap=40, color=(170, 190, 215))
    d = ImageDraw.Draw(pg)
    d.line((30, 100, 870, 100), fill=(210, 120, 120), width=2)
    write(pg, (40, 34), doc['title'], 'kamla', 40, INK['black'], 600, seed=seed)
    write(pg, (690, 44), doc['year'], 'kamla', 26, INK['black'], 180, seed=seed + 1)
    ing = doc['ingredients']
    half = (len(ing) + 1) // 2
    y1 = write(pg, (50, 116), '\n'.join('- ' + i for i in ing[:half]), 'kamla', 25, INK['blue'], 400, gap=40, seed=seed + 2)
    y2 = write(pg, (460, 116), '\n'.join('- ' + i for i in ing[half:]), 'kamla', 25, INK['blue'], 400, gap=40, seed=seed + 7)
    y = write(pg, (50, max(y1, y2) + 2), doc['method'], 'kamla', 25, INK['blue'], 800, gap=40, seed=seed + 3)
    if doc.get('note'):
        write(pg, (300, y + 2), doc['note'], 'kamla', 27, INK['red'], 560, gap=40, seed=seed + 4)
    pg = stain(pg, seed, doc.get('stains', 2), color=(205, 160, 40) if doc.get('turmeric') else (160, 120, 70), max_r=70)
    return [scan(pg, seed, tilt=2.0, fade=0.16)]


def diary(doc):
    """One diary page: printed day heading, Grandma's entry. doc: day (e.g. 'THURSDAY 26 JUNE 1975'), entry, year."""
    seed = doc['seed']
    pg = ruled(paper(A5, tone=(246, 242, 228), seed=seed), top=200, gap=44, color=(190, 200, 215))
    d = ImageDraw.Draw(pg)
    text(pg, (437, 60), doc['year'], 'serif', 26, (120, 120, 120), anchor='mm')
    text(pg, (70, 110), doc['day'], 'serif_bold', 32, INK['black'])
    d.line((60, 160, 814, 160), fill=INK['black'], width=2)
    write(pg, (70, 182), doc['entry'], 'kamla', 30, INK['royal'], 740, gap=44, seed=seed)
    if doc.get('stain'):
        pg = stain(pg, seed, 1, max_r=70)
    return [scan(pg, seed, tilt=0.9)]


def bill(doc):
    """A printed electricity bill. doc: month, period, bill_date, due, consumer, name, address, prev, pres, rate,
    duty, fixed, total, paid."""
    seed = doc['seed']
    pg = paper(A5, tone=(240, 238, 228), grain=6, seed=seed)
    d = ImageDraw.Draw(pg)
    green = (40, 95, 70)
    d.rectangle((40, 40, 834, 150), fill=green)
    text(pg, (437, 70), 'WESTERN SUBURBS ELECTRICITY BOARD', 'print', 30, (255, 255, 255), anchor='mm')
    text(pg, (437, 115), 'ELECTRICITY BILL  ·  Goregaon Division, Bombay', 'print', 22, (230, 240, 230), anchor='mm')
    rows = [
        ('Consumer No.', doc['consumer']),
        ('Name', doc['name']),
        ('Address', doc['address']),
        ('Bill for the month of', doc['month']),
        ('Billing period', doc['period']),
        ('Bill date', doc['bill_date']),
        ('Due date', doc['due']),
    ]
    y = 180
    for k, v in rows:
        text(pg, (60, y), k, 'print', 22, (70, 70, 70))
        text(pg, (330, y), v, 'mono', 23, INK['black'])
        y += 38
    # meter table
    y += 14
    cols = [60, 270, 470, 660]
    d.rectangle((50, y, 824, y + 40), fill=(220, 230, 222))
    for x, h in zip(cols, ('Meter No.', 'Previous', 'Present', 'Units')):
        text(pg, (x, y + 8), h, 'print', 21, INK['black'])
    y += 46
    units = doc['pres'] - doc['prev']
    for x, v in zip(cols, (doc.get('meter', 'GR-40817'), str(doc['prev']), str(doc['pres']), str(units))):
        text(pg, (x, y), v, 'mono', 24, INK['black'])
    y += 54
    # charges table
    energy = round(units * doc['rate'], 2)
    charges = [
        (f'Energy charges ({units} units @ Rs {doc["rate"]:.2f})', energy),
        ('Fixed charges', doc['fixed']),
        ('Electricity duty', doc['duty']),
    ]
    d.rectangle((50, y, 824, y + 40), fill=(220, 230, 222))
    text(pg, (60, y + 8), 'Particulars', 'print', 21, INK['black'])
    text(pg, (814, y + 8), 'Amount (Rs)', 'print', 21, INK['black'], anchor='ra')
    y += 48
    for k, v in charges:
        text(pg, (60, y), k, 'print', 21, INK['black'])
        text(pg, (814, y), f'{v:.2f}', 'mono', 23, INK['black'], anchor='ra')
        y += 36
    d.line((50, y + 4, 824, y + 4), fill=INK['black'], width=2)
    y += 16
    text(pg, (60, y), 'TOTAL AMOUNT PAYABLE', 'print', 25, INK['black'])
    text(pg, (814, y), f'Rs {doc["total"]:.2f}', 'mono', 27, INK['black'], anchor='ra')
    y += 70
    text(pg, (60, y), 'Pay at any WSEB cash counter before the due date to avoid disconnection.', 'print', 17, (90, 90, 90))
    if doc.get('paid'):
        stamp(pg, (470, 980), 'PAID', doc['paid'], INK['red'], angle=-14, size=40)
    return [scan(pg, seed, tilt=0.8, fade=0.1)]


def report(doc):
    """A school progress report: printed form, handwritten marks. doc: school, year, name, cls, roll, subjects
    [(subject, marks, grade)], total, result, remarks, teacher."""
    seed = doc['seed']
    pg = paper(A4, tone=(242, 238, 224), grain=7, seed=seed)
    d = ImageDraw.Draw(pg)
    text(pg, (620, 90), doc['school'], 'serif_bold', 40, INK['black'], anchor='mm')
    text(pg, (620, 140), 'PROGRESS REPORT  ·  Annual Examination ' + doc['year'], 'serif', 28, INK['black'], anchor='mm')
    d.line((80, 175, 1160, 175), fill=INK['black'], width=3)
    fields = [('Name of the student', doc['name']), ('Class', doc['cls']), ('Roll No.', doc['roll']), ('Year', doc['year'])]
    y = 220
    for k, v in fields:
        text(pg, (100, y), k + ':', 'serif', 28)
        d.line((420, y + 36, 1100, y + 36), fill=(120, 120, 120), width=1)
        write(pg, (440, y - 6), v, 'kamla' if doc.get('hand') == 'kamla' else 'mohan', 34, INK['blue'], 640, seed=seed + y)
        y += 70
    y += 30
    cols = (100, 560, 880, 1000)
    d.rectangle((90, y, 1150, y + 56), fill=(225, 220, 205), outline=INK['black'], width=2)
    for x, h in zip(cols, ('Subject', 'Marks (out of 100)', 'Grade', '')):
        text(pg, (x, y + 14), h, 'serif_bold', 26)
    y += 56
    for i, (sub, marks, grade) in enumerate(doc['subjects']):
        d.rectangle((90, y, 1150, y + 58), outline=INK['black'], width=1)
        text(pg, (100, y + 14), sub, 'serif', 27)
        write(pg, (600, y + 6), str(marks), 'mohan', 34, INK['blue'], 150, seed=seed + 50 + i)
        write(pg, (900, y + 6), grade, 'mohan', 34, INK['blue'], 120, seed=seed + 80 + i)
        y += 58
    d.rectangle((90, y, 1150, y + 58), outline=INK['black'], width=2)
    text(pg, (100, y + 14), 'TOTAL', 'serif_bold', 27)
    write(pg, (600, y + 6), doc['total'], 'mohan', 34, INK['blue'], 200, seed=seed + 99)
    y += 110
    text(pg, (100, y), 'Result:', 'serif', 28)
    write(pg, (240, y - 6), doc['result'], 'mohan', 34, INK['red'], 800, seed=seed + 120)
    y += 70
    text(pg, (100, y), 'Remarks:', 'serif', 28)
    y = write(pg, (260, y - 6), doc['remarks'], 'mohan', 32, INK['blue'], 860, seed=seed + 130)
    y += 120
    for x, lab in ((140, 'Class Teacher'), (520, 'Principal'), (880, 'Parent')):
        d.line((x, y, x + 240, y), fill=INK['black'], width=1)
        text(pg, (x + 120, y + 14), lab, 'serif', 24, anchor='ma')
    write(pg, (150, y - 52), doc['teacher'], 'mohan', 30, INK['blue'], 240, seed=seed + 140)
    write(pg, (900, y - 52), doc['parent_sign'], 'mohan', 30, INK['blue'], 240, seed=seed + 141)
    write(pg, (540, y - 52), doc.get('principal', 'R. Desai'), 'savitri', 28, INK['black'], 240, seed=seed + 142)
    stamp(pg, (450, y + 50), doc['school'].split(',')[0].upper()[:22], 'PRINCIPAL', (40, 60, 140), angle=-6, size=24)
    return [scan(pg, seed, tilt=0.9)]


def typed(doc):
    """A typewritten official paper on letterhead. doc: letterhead (lines), ref, date, title, body, sign (lines)."""
    seed = doc['seed']
    pages = []
    paras = doc['body'].split('\n\n')
    split = len(paras) if len(doc['body']) < 1800 else len(paras) // 2 + 1
    for i, part in enumerate([paras[:split], paras[split:]]):
        if not part:
            continue
        pg = paper(A4, tone=(240, 236, 222), grain=6, seed=seed + i)
        d = ImageDraw.Draw(pg)
        y = 90
        if i == 0:
            for j, line in enumerate(doc['letterhead']):
                text(pg, (620, y), line, 'serif_bold' if j == 0 else 'serif', 38 if j == 0 else 24, INK['black'], anchor='ma')
                y += 50 if j == 0 else 34
            d.line((100, y + 10, 1140, y + 10), fill=INK['black'], width=2)
            y += 50
            if doc.get('ref'):
                text(pg, (110, y), doc['ref'], 'typewriter', 26)
            text(pg, (1130, y), doc['date'], 'typewriter', 26, anchor='ra')
            y += 80
            if doc.get('title'):
                text(pg, (620, y), doc['title'], 'typewriter', 32, anchor='ma')
                y += 80
        else:
            y = 130
        y = write(pg, (110, y), '\n\n'.join(part), 'typewriter', 27, INK['black'], 1020, gap=44, hand=False, seed=seed)
        if i == (1 if len(paras) > split else 0):
            y += 40
            for j, line in enumerate(doc['sign']):
                text(pg, (760, y + j * 40), line, 'typewriter', 26)
            if doc.get('signature'):
                write(pg, (760, y - 60), doc['signature'], 'mohan', 38, INK['blue'], 380, seed=seed + 9)
            if doc.get('stamp'):
                stamp(pg, (180, y), doc['stamp'][0], doc['stamp'][1], (60, 40, 130), angle=-8, size=30)
        pages.append(scan(pg, seed + i, tilt=0.7))
    return pages


def invitation(doc):
    """A printed invitation card. doc: top, names, lines (list), venue, date_line, rsvp."""
    seed = doc['seed']
    size = (1100, 760)
    pg = paper(size, tone=(250, 238, 210), grain=6, seed=seed)
    d = ImageDraw.Draw(pg)
    gold, maroon = (170, 120, 40), (120, 25, 35)
    d.rectangle((24, 24, size[0] - 24, size[1] - 24), outline=gold, width=6)
    d.rectangle((40, 40, size[0] - 40, size[1] - 40), outline=gold, width=2)
    y = 90
    text(pg, (550, y), doc['top'], 'serif', 26, maroon, anchor='ma')
    y += 60
    for line in doc['lines_before']:
        text(pg, (550, y), line, 'serif', 25, INK['black'], anchor='ma')
        y += 40
    y += 10
    text(pg, (550, y), doc['names'], 'fancy', 58, maroon, anchor='ma')
    y += 100
    for line in doc['lines_after']:
        text(pg, (550, y), line, 'serif', 25, INK['black'], anchor='ma')
        y += 40
    if doc.get('rsvp'):
        text(pg, (550, size[1] - 90), doc['rsvp'], 'serif', 21, (90, 70, 50), anchor='ma')
    pg = stain(pg, seed, 1, max_r=60)
    return [scan(pg, seed, tilt=1.4)]


def ration(doc):
    """A ration card page: printed form, handwritten household entries. doc: card_no, issued, office, head, address,
    members [(name, relation, age)], shop."""
    seed = doc['seed']
    pg = paper(A5, tone=(225, 232, 214), grain=8, seed=seed)  # greenish card stock
    d = ImageDraw.Draw(pg)
    text(pg, (437, 60), 'FAMILY RATION CARD', 'serif_bold', 34, INK['black'], anchor='ma')
    text(pg, (437, 104), doc['office'], 'serif', 20, INK['black'], anchor='ma')
    d.line((50, 140, 824, 140), fill=INK['black'], width=2)
    y = 165
    for k, v in (('Card No.', doc['card_no']), ('Date of issue', doc['issued']), ('Head of household', doc['head']), ('Address', doc['address'])):
        text(pg, (60, y), k, 'serif', 21)
        y = max(y + 42, write(pg, (310, y - 6), v, 'mohan', 28, INK['blue'], 500, seed=seed + y))
    y += 20
    d.rectangle((50, y, 824, y + 42), fill=(205, 215, 195), outline=INK['black'])
    for x, h in ((60, 'No.'), (130, 'Name'), (470, 'Relation'), (690, 'Age')):
        text(pg, (x, y + 10), h, 'serif_bold', 21)
    y += 42
    for i, (name, rel, age) in enumerate(doc['members']):
        d.rectangle((50, y, 824, y + 50), outline=INK['black'])
        text(pg, (70, y + 13), str(i + 1), 'serif', 22)
        write(pg, (130, y + 4), name, 'mohan', 28, INK['blue'], 330, seed=seed + 200 + i)
        write(pg, (470, y + 4), rel, 'mohan', 28, INK['blue'], 210, seed=seed + 220 + i)
        write(pg, (695, y + 4), str(age), 'mohan', 28, INK['blue'], 110, seed=seed + 240 + i)
        y += 50
    y += 30
    text(pg, (60, y), 'Fair price shop: ' + doc['shop'], 'serif', 20)
    stamp(pg, (470, y + 50), 'RATIONING OFFICE', doc['issued'], (70, 50, 140), angle=-10, size=26)
    return [scan(pg, seed, tilt=1.0, fade=0.14)]


LAYOUTS = {
    'letter': letter,
    'telegram': telegram,
    'recipe': recipe,
    'diary': diary,
    'bill': bill,
    'report': report,
    'typed': typed,
    'invitation': invitation,
    'ration': ration,
}
