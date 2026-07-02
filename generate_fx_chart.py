#!/usr/bin/env python3
"""Generate English version of the CNGR FX Management Framework chart - optimized layout."""

from PIL import Image, ImageDraw, ImageFont

# Canvas size - larger to accommodate English text
W, H = 1600, 1100
img = Image.new('RGB', (W, H), '#1a1a1a')
draw = ImageDraw.Draw(img)

# Fonts - smaller for English text density
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]
font = None
for fp in font_paths:
    try:
        font = ImageFont.truetype(fp, 13)
        font_bold = ImageFont.truetype(fp, 14)
        font_small = ImageFont.truetype(fp, 11)
        font_title = ImageFont.truetype(fp, 16)
        break
    except:
        continue
if font is None:
    font = ImageFont.load_default()
    font_bold = font_small = font_title = font

def text_size(text, f):
    bbox = draw.textbbox((0, 0), text, font=f)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_box(x, y, w, h, text, fill='white', text_color='black', font=font, border='black'):
    draw.rectangle([x, y, x+w, y+h], fill=fill, outline=border, width=2)
    tw, th = text_size(text, font)
    draw.text((x + (w-tw)//2, y + (h-th)//2), text, fill=text_color, font=font)

def draw_multiline_box(x, y, w, h, lines, fill='white', text_color='black', font=font):
    draw.rectangle([x, y, x+w, y+h], fill=fill, outline='black', width=2)
    total_h = len(lines) * 15
    start_y = y + (h - total_h) // 2
    for j, line in enumerate(lines):
        tw, th = text_size(line, font)
        draw.text((x + (w-tw)//2, start_y + j*15), line, fill=text_color, font=font)

def draw_arrow(x1, y1, x2, y2, color='white'):
    draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
    if abs(x2-x1) > abs(y2-y1):
        if x2 > x1:
            draw.polygon([(x2, y2), (x2-8, y2-4), (x2-8, y2+4)], fill=color)
        else:
            draw.polygon([(x2, y2), (x2+8, y2-4), (x2+8, y2+4)], fill=color)
    else:
        if y2 > y1:
            draw.polygon([(x2, y2), (x2-4, y2-8), (x2+4, y2-8)], fill=color)
        else:
            draw.polygon([(x2, y2), (x2-4, y2+8), (x2+4, y2+8)], fill=color)

# ============================================
# SECTION 1: EX-ANTE MANAGEMENT
# ============================================
y_sep1 = 340

# Left sidebar - main green label (wider for English)
draw.rectangle([20, 30, 85, 300], fill='#7cb342', outline='black', width=2)
# Draw vertical text for "Ex-ante Management"
draw.text((30, 80), "Ex-ante", fill='black', font=font_bold)
draw.text((30, 100), "Manage-", fill='black', font=font_bold)
draw.text((30, 120), "ment", fill='black', font=font_bold)

# Sub-label 1: Investment & New Market Entry FX Risk Assessment
draw.rectangle([105, 30, 170, 300], fill='#aed581', outline='black', width=2)
draw.text((110, 60), "Investment", fill='black', font=font_small)
draw.text((110, 74), "& New Market", fill='black', font=font_small)
draw.text((110, 88), "Entry FX", fill='black', font=font_small)
draw.text((110, 102), "Risk", fill='black', font=font_small)
draw.text((110, 116), "Assessment", fill='black', font=font_small)

# 4 investment boxes
box_w = 220
box_h = 50
for i, lines in enumerate([
    ["New Plant Construction &", "Mining Investment"],
    ["Cost-Profit Calculation"],
    ["Trade Route Planning"],
    ["ODI + Cross-border", "Borrowing Routes"]
]):
    y = 50 + i * 65
    draw_multiline_box(190, y, box_w, box_h, lines, font=font_small)

# Sub-label 2: Pre-emptive Capital Control
draw.rectangle([430, 30, 495, 300], fill='#aed581', outline='black', width=2)
draw.text((435, 80), "Pre-emptive", fill='black', font=font_small)
draw.text((435, 94), "Capital", fill='black', font=font_small)
draw.text((435, 108), "Control", fill='black', font=font_small)

# Top right: Inventory analysis
box_x2 = 520
y_top = 45
h_top = 30
w_top = 260
draw.rectangle([box_x2, y_top, box_x2+w_top, y_top+h_top], fill='white', outline='black', width=2)
tw, th = text_size("Inventory Purchase-Sale-Stock Analysis", font_small)
draw.text((box_x2 + (w_top-tw)//2, y_top + (h_top-th)//2), "Inventory Purchase-Sale-Stock Analysis", fill='black', font=font_small)

# Two middle boxes
w_mid = 270
h_mid = 70
y_mid = 90
# Left
draw.rectangle([box_x2, y_mid, box_x2+w_mid, y_mid+h_mid], fill='white', outline='black', width=2)
lines1 = ['Prepare "Credit Term+3" Month', "Rolling Cash Budget,", "Identify Funding Gaps via", "FX Risk Assessment"]
start_y = y_mid + 5
for j, line in enumerate(lines1):
    tw, th = text_size(line, font_small)
    draw.text((box_x2 + (w_mid-tw)//2, start_y + j*14), line, fill='black', font=font_small)

# Right
draw.rectangle([box_x2+w_mid+15, y_mid, box_x2+w_mid+15+w_mid, y_mid+h_mid], fill='white', outline='black', width=2)
lines2 = ["Ad-hoc Inventory Pressure", "or Procurement,", "Identify Funding Gaps"]
start_y = y_mid + 10
for j, line in enumerate(lines2):
    tw, th = text_size(line, font_small)
    draw.text((box_x2+w_mid+15 + (w_mid-tw)//2, start_y + j*14), line, fill='black', font=font_small)

# Bottom arrow box
y_bot = 180
h_bot = 35
w_bot = 555
draw.rectangle([box_x2, y_bot, box_x2+w_bot, y_bot+h_bot], fill='white', outline='black', width=2)
tw, th = text_size("Financing Cost & FX Risk Assessment", font_small)
draw.text((box_x2 + (w_bot-tw)//2, y_bot + (h_bot-th)//2), "Financing Cost & FX Risk Assessment", fill='black', font=font_small)

# Arrow down
draw_arrow(box_x2 + w_bot//2, y_bot + h_bot, box_x2 + w_bot//2, y_bot + h_bot + 25, 'white')

# Dashed separator 1
for x in range(20, W-20, 15):
    draw.line([(x, y_sep1), (x+8, y_sep1)], fill='white', width=2)

# ============================================
# SECTION 2: ONGOING MANAGEMENT
# ============================================
y2_start = 360
y2_end = 830

# Left sidebar - blue
draw.rectangle([20, y2_start, 85, y2_end], fill='#5c6bc0', outline='black', width=2)
draw.text((30, y2_start+30), "Ongoing", fill='white', font=font_bold)
draw.text((30, y2_start+50), "Manage-", fill='white', font=font_bold)
draw.text((30, y2_start+70), "ment", fill='white', font=font_bold)

# Sub-label: FX Management System
draw.rectangle([105, y2_start, 170, y2_end], fill='#7986cb', outline='black', width=2)
draw.text((110, y2_start+25), "FX Mgmt", fill='black', font=font_small)
draw.text((110, y2_start+39), "System", fill='black', font=font_small)
draw.text((110, y2_start+53), "Supporting", fill='black', font=font_small)
draw.text((110, y2_start+67), "Standardized", fill='black', font=font_small)
draw.text((110, y2_start+81), "Daily", fill='black', font=font_small)
draw.text((110, y2_start+95), "Operations", fill='black', font=font_small)

# Column 1: FX Rate Pricing & Publication
col1_x = 190
# Title
draw.rectangle([col1_x, y2_start+10, col1_x+260, y2_start+38], fill='#c5cae9', outline='black', width=2)
tw, th = text_size("FX Rate Pricing & Publication", font_small)
draw.text((col1_x + (260-tw)//2, y2_start+10 + (28-th)//2), "FX Rate Pricing & Publication", fill='black', font=font_small)

# 4 small boxes (2x2)
box_w2 = 125
box_h2 = 45
for i, lines in enumerate([
    ["Intercompany", "Transaction Rate", "Setting"],
    ["Commercial", "Contract Rate", "Setting"],
    ["Borrowing", "Transfer Pricing", "Rate"],
    ["Budget Rate"]
]):
    row = i // 2
    col_off = (i % 2) * (box_w2 + 10)
    y = y2_start + 50 + row * 55
    draw_multiline_box(col1_x + col_off, y, box_w2, box_h2, lines, font=font_small)

# Arrow box at bottom
draw.rectangle([col1_x, y2_start+160, col1_x+260, y2_start+190], fill='white', outline='black', width=2)
lines_arr = ["Foreign Currency Reporting", "Translation Differences"]
start_y = y2_start + 165
for j, line in enumerate(lines_arr):
    tw, th = text_size(line, font_small)
    draw.text((col1_x + (260-tw)//2, start_y + j*14), line, fill='black', font=font_small)

# Column 2: FX Business Data Collection
col2_x = 470
# Title
draw.rectangle([col2_x, y2_start+10, col2_x+260, y2_start+38], fill='#c5cae9', outline='black', width=2)
tw, th = text_size("FX Business Data Collection", font_small)
draw.text((col2_x + (260-tw)//2, y2_start+10 + (28-th)//2), "FX Business Data Collection", fill='black', font=font_small)

# 6 boxes (3x2)
for i, lines in enumerate([
    ["Import/Export", "Trade Data"],
    ["Internal", "Borrowing"],
    ["FX Trading"],
    ["External", "Borrowing"],
    ["Capital", "Injection"],
    ["Dividend", "Distribution"]
]):
    row = i // 2
    col_off = (i % 2) * (box_w2 + 10)
    y = y2_start + 50 + row * 55
    draw_multiline_box(col2_x + col_off, y, box_w2, box_h2, lines, font=font_small)

# Column 3: FX Exposure Risk Statistics
col3_x = 750
# Title
draw.rectangle([col3_x, y2_start+10, col3_x+260, y2_start+38], fill='#c5cae9', outline='black', width=2)
tw, th = text_size("FX Exposure Risk Statistics", font_small)
draw.text((col3_x + (260-tw)//2, y2_start+10 + (28-th)//2), "FX Exposure Risk Statistics", fill='black', font=font_small)

# 6 boxes with arrow pairs
for i, lines in enumerate([
    ["Currency Exposure", "vs. RMB"],
    ["Exposure Rate", "Cost Calculation"],
    ["Individual Company", "FX Exposure"],
    ["Group Consolidated", "FX Exposure"],
    ["Individual Company", "FX Gains/Losses"],
    ["Group FX Gains/", "Losses Calculation"]
]):
    row = i // 2
    col_off = (i % 2) * (box_w2 + 10)
    y = y2_start + 50 + row * 55
    draw_multiline_box(col3_x + col_off, y, box_w2, box_h2, lines, font=font_small)
    # Arrow between left and right
    if i % 2 == 0 and i < 5:
        arrow_x = col3_x + box_w2 + 5
        arrow_y = y + box_h2 // 2
        draw_arrow(arrow_x, arrow_y, arrow_x + 8, arrow_y, 'black')

# Arrow from col2 to col3
draw_arrow(col2_x + 260, y2_start + 120, col3_x, y2_start + 120, 'white')

# Bottom row of ongoing section
y_ongoing_bottom = y2_start + 200

# Left: Limit Management + Monitoring
w_left = 520
draw.rectangle([col1_x, y_ongoing_bottom, col1_x+w_left, y_ongoing_bottom+30], fill='#ffab91', outline='black', width=2)
tw, th = text_size("Limit Management + System Monitoring & Alerts", font_small)
draw.text((col1_x + (w_left-tw)//2, y_ongoing_bottom + (30-th)//2), "Limit Management + System Monitoring & Alerts", fill='black', font=font_small)

# 3 boxes below
for i, lines in enumerate([
    ["Exposure Limit", "Management"],
    ["Stop-loss Limit", "Management"],
    ["FX Derivatives", "Quota Management"]
]):
    x = col1_x + i * 175
    draw_multiline_box(x, y_ongoing_bottom+40, 160, 45, lines, font=font_small)

# Right: Trading Strategy
w_right = 260
draw.rectangle([col3_x, y_ongoing_bottom, col3_x+w_right, y_ongoing_bottom+30], fill='#ffab91', outline='black', width=2)
tw, th = text_size("Trading Strategy + Regional Risk Plans", font_small)
draw.text((col3_x + (w_right-tw)//2, y_ongoing_bottom + (30-th)//2), "Trading Strategy + Regional Risk Plans", fill='black', font=font_small)

# 2 boxes below
for i, lines in enumerate([
    ["FX Trading", "Decisions"],
    ["Update Risk", "Management Strategy"]
]):
    x = col3_x + i * 135
    draw_multiline_box(x, y_ongoing_bottom+40, 125, 45, lines, font=font_small)

# Arrow from left to right
draw_arrow(col1_x + w_left, y_ongoing_bottom + 15, col3_x, y_ongoing_bottom + 15, 'white')

# Arrow down
draw_arrow(col3_x + w_right//2, y_ongoing_bottom + 85, col3_x + w_right//2, y_ongoing_bottom + 110, 'white')

# Dashed separator 2
y_sep2 = 850
for x in range(20, W-20, 15):
    draw.line([(x, y_sep2), (x+8, y_sep2)], fill='white', width=2)

# ============================================
# SECTION 3: EX-POST MANAGEMENT
# ============================================
y3_start = 870
y3_end = 1060

# Left sidebar - gray
draw.rectangle([20, y3_start, 85, y3_end], fill='#78909c', outline='black', width=2)
draw.text((30, y3_start+20), "Ex-post", fill='white', font=font_bold)
draw.text((30, y3_start+40), "Manage-", fill='white', font=font_bold)
draw.text((30, y3_start+60), "ment", fill='white', font=font_bold)

# Sub-label
draw.rectangle([105, y3_start, 170, y3_end], fill='#90a4ae', outline='black', width=2)
draw.text((110, y3_start+25), "Fund", fill='black', font=font_small)
draw.text((110, y3_start+39), "Settlement", fill='black', font=font_small)
draw.text((110, y3_start+53), "& Risk", fill='black', font=font_small)
draw.text((110, y3_start+67), "Reporting", fill='black', font=font_small)

# Top row: 2 boxes
box_w3 = 300
box_h3 = 35
box_y3 = y3_start + 10
for i, lines in enumerate([
    ["Prevent Liquidation Risk from", "Insufficient Funds or Operational Issues"],
    ["Predict Impact of Adverse Rate Changes", "on Committed Transactions"]
]):
    x = 190 + i * 330
    draw_multiline_box(x, box_y3, box_w3, box_h3, lines, font=font_small)

# Arrow down
draw_arrow(190 + box_w3//2, box_y3 + box_h3, 190 + box_w3//2, box_y3 + box_h3 + 15, 'white')

# Bottom row: 2 boxes
box_y4 = box_y3 + box_h3 + 25
for i, lines in enumerate([
    ["Develop Emergency Response Plans for", "Operational Adjustments or Market Volatility"],
    ["Key Matters", "Reporting"]
]):
    x = 190 + i * 330
    if i == 1:
        w = 200
    else:
        w = box_w3
    draw_multiline_box(x, box_y4, w, box_h3, lines, font=font_small)

# Save
output_path = '/root/.openclaw/workspace/cngr_fx_framework_en.png'
img.save(output_path, 'PNG')
print(f"Saved to {output_path} ({W}x{H})")
