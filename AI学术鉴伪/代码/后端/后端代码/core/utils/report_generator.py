# utils/report_generator.py
import os, textwrap, json
from datetime import datetime
from pathlib import Path
from django.conf import settings
from django.utils import timezone

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import Color

from ..models import DetectionTask, DetectionResult, SubDetectionResult

# ─── 字体注册（优先使用本地宋体文件，缺失时回退到内置中文字体） ──────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
FONT_REGULAR = 'SimSun'
FONT_BOLD = 'SimSun-Bold'

_font_candidates = [
    BASE_DIR / 'SimSun.ttf',
    BASE_DIR / 'SimSun-Bold.ttf',
    Path(__file__).resolve().parent / 'SimSun.ttf',
    Path(__file__).resolve().parent / 'SimSun-Bold.ttf',
]

try:
    if (_font_candidates[0]).exists():
        pdfmetrics.registerFont(TTFont('SimSun', str(_font_candidates[0])))
        if (_font_candidates[1]).exists():
            pdfmetrics.registerFont(TTFont('SimSun-Bold', str(_font_candidates[1])))
        else:
            pdfmetrics.registerFont(TTFont('SimSun-Bold', str(_font_candidates[0])))
    else:
        pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
        FONT_REGULAR = 'STSong-Light'
        FONT_BOLD = 'STSong-Light'
except Exception:
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    FONT_REGULAR = 'STSong-Light'
    FONT_BOLD = 'STSong-Light'


# ══════════════════════════════════════════════════════════════════════════════
# Color Palette
# ══════════════════════════════════════════════════════════════════════════════
COLOR_HEADER_BG     = Color(0.10, 0.12, 0.22)        # dark navy
COLOR_HEADER_TEXT   = Color(1, 1, 1)
COLOR_ACCENT        = Color(0.16, 0.47, 0.80)         # blue accent
COLOR_GREEN         = Color(0.18, 0.49, 0.20)         # #2e7d32  真/真实
COLOR_GREEN_BG      = Color(0.90, 0.96, 0.90)
COLOR_RED           = Color(0.78, 0.16, 0.16)         # #c62828  假/造假
COLOR_RED_BG        = Color(0.98, 0.90, 0.90)
COLOR_SECTION_LINE  = Color(0.16, 0.47, 0.80)
COLOR_INFO_BG       = Color(0.94, 0.95, 0.97)
COLOR_FOOTER_TEXT   = Color(0.45, 0.45, 0.45)
COLOR_BODY_TEXT     = Color(0.15, 0.15, 0.15)
COLOR_LIGHT_GRAY    = Color(0.82, 0.82, 0.82)
COLOR_WHITE         = Color(1, 1, 1)

# ─── Layout Constants ──────────────────────────────────────────────────────────
MARGIN = 50
HEADER_BAR_HEIGHT = 36
FOOTER_HEIGHT = 30
CONTENT_MIN_Y = MARGIN + FOOTER_HEIGHT + 10


# ══════════════════════════════════════════════════════════════════════════════
# Shared Helper Functions
# ══════════════════════════════════════════════════════════════════════════════

def _draw_header(c, W, title):
    """Draw the navy header bar with white title text at the top of a page."""
    c.setFillColor(COLOR_HEADER_BG)
    c.rect(0, W[1] - HEADER_BAR_HEIGHT, W[0], HEADER_BAR_HEIGHT, fill=1, stroke=0)
    c.setFillColor(COLOR_HEADER_TEXT)
    c.setFont(FONT_BOLD, 12)
    c.drawString(MARGIN, W[1] - HEADER_BAR_HEIGHT + 11, title)
    # Thin accent line under header bar
    c.setStrokeColor(COLOR_ACCENT)
    c.setLineWidth(1.5)
    c.line(0, W[1] - HEADER_BAR_HEIGHT - 1, W[0], W[1] - HEADER_BAR_HEIGHT - 1)
    c.setFillColor(COLOR_BODY_TEXT)


def _draw_footer(c, W, page_num, gen_time):
    """Draw footer with page number and generation timestamp."""
    c.setStrokeColor(COLOR_LIGHT_GRAY)
    c.setLineWidth(0.5)
    c.line(MARGIN, FOOTER_HEIGHT + 8, W[0] - MARGIN, FOOTER_HEIGHT + 8)
    c.setFillColor(COLOR_FOOTER_TEXT)
    c.setFont(FONT_REGULAR, 7)
    c.drawString(MARGIN, FOOTER_HEIGHT - 4, f"报告生成时间：{gen_time}")
    c.drawRightString(W[0] - MARGIN, FOOTER_HEIGHT - 4, f"第 {page_num} 页")
    c.setFillColor(COLOR_BODY_TEXT)


def _draw_cover_page(c, W, H, title, subtitle, task):
    """Draw a branded cover page. Returns nothing; caller should call c.showPage()."""
    gen_time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")

    # Navy background block at top
    cover_bg_h = 220
    c.setFillColor(COLOR_HEADER_BG)
    c.rect(0, H - cover_bg_h, W, cover_bg_h, fill=1, stroke=0)

    # Accent line at bottom of navy block
    c.setStrokeColor(COLOR_ACCENT)
    c.setLineWidth(3)
    c.line(0, H - cover_bg_h, W, H - cover_bg_h)

    # Brand text
    c.setFillColor(COLOR_WHITE)
    c.setFont(FONT_BOLD, 38)
    c.drawCentredString(W / 2, H - 90, "听泉鉴图")
    c.setFont(FONT_REGULAR, 14)
    c.drawCentredString(W / 2, H - 120, "AI-Powered Academic Integrity Analysis Platform")

    # Report title
    c.setFont(FONT_BOLD, 18)
    c.drawCentredString(W / 2, H - 170, title)
    if subtitle:
        c.setFont(FONT_REGULAR, 12)
        c.drawCentredString(W / 2, H - 192, subtitle)

    # Info section below cover bg
    c.setFillColor(COLOR_BODY_TEXT)
    y = H - cover_bg_h - 50

    info_items = [
        ("任务编号", str(task.id)),
        ("任务名称", task.task_name or ""),
        ("提交用户", task.user.username if task.user else ""),
        ("任务类型", task.get_task_type_display() if hasattr(task, 'get_task_type_display') else (task.task_type or "")),
    ]

    create_time = timezone.localtime(task.upload_time).strftime("%Y-%m-%d %H:%M") if task.upload_time else "-"
    finish_time = "-"
    if task.completion_time:
        finish_time = timezone.localtime(task.completion_time).strftime("%Y-%m-%d %H:%M")
    info_items.append(("创建时间", create_time))
    info_items.append(("完成时间", finish_time))

    for label, value in info_items:
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, y, label)
        c.setFont(FONT_REGULAR, 11)
        c.drawString(MARGIN + 90, y, f"：{value}")
        y -= 22

    # Generation timestamp at bottom
    c.setFillColor(COLOR_FOOTER_TEXT)
    c.setFont(FONT_REGULAR, 8)
    c.drawCentredString(W / 2, 50, f"报告生成时间：{gen_time}")
    c.setFillColor(COLOR_BODY_TEXT)

    c.showPage()
    return gen_time


def _draw_section_title(c, y, W, title, level=1):
    """Draw a section heading with colored underline. Returns new y."""
    if level == 1:
        font_size = 14
        line_offset = -5
    elif level == 2:
        font_size = 12
        line_offset = -4
    else:
        font_size = 10
        line_offset = -3

    c.setFont(FONT_BOLD, font_size)
    c.setFillColor(COLOR_BODY_TEXT)
    c.drawString(MARGIN, y, title)

    line_y = y + line_offset
    c.setStrokeColor(COLOR_SECTION_LINE)
    c.setLineWidth(1.2 if level == 1 else 0.8)
    c.line(MARGIN, line_y, W - MARGIN, line_y)
    c.setLineWidth(1)
    c.setFillColor(COLOR_BODY_TEXT)

    return y - (font_size + 10)


def _draw_info_box(c, y, W, rows, col_widths=None):
    """Draw an info box with light background. rows is list of (label, value) tuples.
    col_widths can customize label column width. Returns new y."""
    if not rows:
        return y

    label_w = col_widths or 100
    row_h = 20
    box_h = len(rows) * row_h + 8

    # Background rectangle
    c.setFillColor(COLOR_INFO_BG)
    c.roundRect(MARGIN, y - box_h + 4, W - 2 * MARGIN, box_h, 4, fill=1, stroke=0)
    c.setFillColor(COLOR_BODY_TEXT)

    cy = y - 6
    for label, value in rows:
        c.setFont(FONT_BOLD, 9)
        c.drawString(MARGIN + 8, cy, str(label))
        c.setFont(FONT_REGULAR, 9)
        c.drawString(MARGIN + 8 + label_w, cy, str(value))
        cy -= row_h

    # Border
    c.setStrokeColor(COLOR_LIGHT_GRAY)
    c.setLineWidth(0.5)
    c.roundRect(MARGIN, y - box_h + 4, W - 2 * MARGIN, box_h, 4, fill=0, stroke=1)
    c.setLineWidth(1)

    return y - box_h - 6


def _draw_metric_row(c, y, label, value, is_fake=None):
    """Draw a label: value row. If is_fake is set, color the value green/red. Returns new y."""
    c.setFont(FONT_REGULAR, 10)
    c.setFillColor(COLOR_BODY_TEXT)
    c.drawString(MARGIN + 8, y, str(label))

    if is_fake is True:
        c.setFillColor(COLOR_RED)
    elif is_fake is False:
        c.setFillColor(COLOR_GREEN)
    else:
        c.setFillColor(COLOR_BODY_TEXT)

    c.setFont(FONT_BOLD, 10)
    c.drawString(MARGIN + 120, y, str(value))
    c.setFillColor(COLOR_BODY_TEXT)
    return y - 18


def _draw_verdict_badge(c, x, y, is_fake, confidence=None):
    """Draw a colored verdict badge (造假/真实) with optional confidence. Returns new y."""
    label = "造假" if is_fake else "真实"
    color = COLOR_RED if is_fake else COLOR_GREEN
    bg = COLOR_RED_BG if is_fake else COLOR_GREEN_BG

    badge_w = 60
    badge_h = 20

    c.setFillColor(bg)
    c.roundRect(x, y - badge_h + 4, badge_w, badge_h, 3, fill=1, stroke=0)
    c.setFillColor(color)
    c.setFont(FONT_BOLD, 10)
    c.drawCentredString(x + badge_w / 2, y - badge_h + 9, label)

    if confidence is not None:
        c.setFillColor(COLOR_BODY_TEXT)
        c.setFont(FONT_REGULAR, 9)
        c.drawString(x + badge_w + 10, y - badge_h + 9, f"置信度：{confidence:.1%}")

    c.setFillColor(COLOR_BODY_TEXT)
    return y - badge_h - 8


def _draw_multiline(c, x, y, text, max_chars=68, leading=14, font=None, size=9):
    """Wrap long text and draw multiple lines. Returns new y."""
    if not text:
        return y
    c.setFont(font or FONT_REGULAR, size)
    for line in textwrap.wrap(str(text), width=max_chars):
        if y < CONTENT_MIN_Y:
            return y  # caller must handle page break
        c.drawString(x, y, line)
        y -= leading
    return y


def _ensure_space(c, y, W, H, needed, page_num, header_title, gen_time):
    """Check if enough vertical space remains. If not, start a new page with header/footer.
    Returns (y, page_num)."""
    if y - needed < CONTENT_MIN_Y:
        c.showPage()
        page_num += 1
        _draw_header(c, (W, H), header_title)
        _draw_footer(c, (W, H), page_num, gen_time)
        y = H - HEADER_BAR_HEIGHT - 16
    return y, page_num


def _task_report_path(task):
    """Return (rel_path, abs_path) for a task report PDF."""
    rel_path = f"reports/task_{task.id}_report.pdf"
    abs_path = os.path.join(settings.MEDIA_ROOT, rel_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    return rel_path, abs_path


def _save_task_report(task, rel_path):
    """Write report_file on the task and save."""
    task.report_file = rel_path
    task.save(update_fields=["report_file"])
    return rel_path


# ══════════════════════════════════════════════════════════════════════════════
# 1. Image Detection Report
# ══════════════════════════════════════════════════════════════════════════════

def generate_detection_task_report(task: DetectionTask) -> str:
    """
    Generate a PDF report for image detection tasks.
    Writes task.report_file and returns the relative path.
    """
    rel_path, abs_path = _task_report_path(task)
    c = canvas.Canvas(abs_path, pagesize=A4)
    W, H = A4
    gen_time = _draw_cover_page(c, W, H, "图像造假检测报告", None, task)

    page_num = 1
    header_title = "听泉鉴图 - 图像检测报告"

    detection_results = task.detection_results.select_related(
        "image_upload"
    ).prefetch_related("sub_results").order_by("id")

    for idx, dr in enumerate(detection_results, start=1):
        # --- Each image starts on a new page ---
        c.showPage()
        page_num += 1
        _draw_header(c, (W, H), header_title)
        _draw_footer(c, (W, H), page_num, gen_time)
        y = H - HEADER_BAR_HEIGHT - 16

        img_id = dr.image_upload_id
        img_title = f"图片 {idx}  (ID: {img_id})"

        # Section: Image header
        y = _draw_section_title(c, y, W, img_title)

        # Verdict badge
        is_fake_val = dr.is_fake if dr.is_fake is not None else False
        conf = dr.confidence_score if dr.confidence_score is not None else 0.0
        y = _draw_verdict_badge(c, MARGIN + 8, y, is_fake_val, conf)
        y -= 4

        # Original image
        orig_path = dr.image_upload.image.path if dr.image_upload.image else None
        if orig_path and os.path.exists(orig_path):
            try:
                img_reader = ImageReader(orig_path)
                iw, ih = img_reader.getSize()
                # Scale to fit 160px wide, max 160px tall
                scale = min(160.0 / iw, 160.0 / ih, 1.0)
                dw, dh = int(iw * scale), int(ih * scale)
                y = _draw_section_title(c, y, W, "原始图像", level=2)
                c.drawImage(img_reader, MARGIN + 8, y - dh, width=dw, height=dh, preserveAspectRatio=True)
                y -= dh + 8
            except Exception:
                pass

        y -= 4

        # Info box with EXIF data
        exif_rows = [
            ("判定结果", "造假" if is_fake_val else "真实"),
            ("置信度分数", f"{conf:.4f}"),
            ("Photoshop痕迹", "有" if dr.exif_photoshop else "无"),
            ("时间修改痕迹", "有" if dr.exif_time_modified else "无"),
        ]
        if dr.detection_time:
            exif_rows.append(("检测时间", timezone.localtime(dr.detection_time).strftime("%Y-%m-%d %H:%M")))

        y, page_num = _ensure_space(c, y, W, H, 140, page_num, header_title, gen_time)
        y = _draw_info_box(c, y, W, exif_rows, col_widths=110)
        y -= 4

        # LLM judgment
        if task.if_use_llm and dr.llm_judgment:
            y, page_num = _ensure_space(c, y, W, H, 60, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "大语言模型分析", level=2)
            y = _draw_multiline(c, MARGIN + 8, y, dr.llm_judgment, max_chars=72)
            y -= 4

            # LLM visualization image
            if dr.llm_image and hasattr(dr.llm_image, 'path') and os.path.exists(dr.llm_image.path):
                y, page_num = _ensure_space(c, y, W, H, 120, page_num, header_title, gen_time)
                try:
                    llm_reader = ImageReader(dr.llm_image.path)
                    lw, lh = llm_reader.getSize()
                    scale = min(140.0 / lw, 140.0 / lh, 1.0)
                    c.drawImage(llm_reader, MARGIN + 8, y - int(lh * scale),
                                width=int(lw * scale), height=int(lh * scale), preserveAspectRatio=True)
                    y -= int(lh * scale) + 8
                except Exception:
                    pass

        # ELA visualization
        if dr.ela_image and hasattr(dr.ela_image, 'path') and os.path.exists(dr.ela_image.path):
            y, page_num = _ensure_space(c, y, W, H, 120, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "ELA 可视化分析", level=2)
            try:
                ela_reader = ImageReader(dr.ela_image.path)
                ew, eh = ela_reader.getSize()
                scale = min(140.0 / ew, 140.0 / eh, 1.0)
                c.drawImage(ela_reader, MARGIN + 8, y - int(eh * scale),
                            width=int(ew * scale), height=int(eh * scale), preserveAspectRatio=True)
                y -= int(eh * scale) + 8
            except Exception:
                pass

        # Sub-method results
        sub_results = list(dr.sub_results.all())
        if sub_results:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "深度学习检测方法", level=2)

            sub_rows = []
            for sub in sub_results:
                method_name = sub.get_method_display() if hasattr(sub, 'get_method_display') else sub.method
                prob = sub.probability if sub.probability is not None else 0.0
                sub_rows.append((method_name, f"{prob:.4f}"))

            y, page_num = _ensure_space(c, y, W, H, len(sub_rows) * 20 + 30, page_num, header_title, gen_time)
            y = _draw_info_box(c, y, W, sub_rows, col_widths=110)

            # Mask images for each sub result
            for sub in sub_results:
                if sub.mask_image and hasattr(sub.mask_image, 'path') and os.path.exists(sub.mask_image.path):
                    y, page_num = _ensure_space(c, y, W, H, 90, page_num, header_title, gen_time)
                    method_label = sub.get_method_display() if hasattr(sub, 'get_method_display') else sub.method
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 8, y, f"{method_label} - 热力图：")
                    y -= 12
                    try:
                        mask_reader = ImageReader(sub.mask_image.path)
                        mw, mh = mask_reader.getSize()
                        scale = min(100.0 / mw, 100.0 / mh, 1.0)
                        c.drawImage(mask_reader, MARGIN + 8, y - int(mh * scale),
                                    width=int(mw * scale), height=int(mh * scale), preserveAspectRatio=True)
                        y -= int(mh * scale) + 8
                    except Exception:
                        pass

    c.save()
    return _save_task_report(task, rel_path)


# ══════════════════════════════════════════════════════════════════════════════
# 2. Text Detection Report (paper_text / review_text)
# ══════════════════════════════════════════════════════════════════════════════

def generate_text_detection_report(task: DetectionTask) -> str:
    """
    Generate a PDF report for paper_text or review_text detection tasks.
    Writes task.report_file and returns the relative path.
    """
    rel_path, abs_path = _task_report_path(task)
    c = canvas.Canvas(abs_path, pagesize=A4)
    W, H = A4

    is_paper = task.detect_type == 'paper'
    report_subtitle = "论文文本 AI 生成检测" if is_paper else "同行评审文本模板化检测"
    gen_time = _draw_cover_page(c, W, H, "文本检测报告", report_subtitle, task)

    page_num = 1
    header_title = "听泉鉴图 - 文本检测报告"

    text_results = task.text_detection_results.select_related("text_resource").order_by("id")

    for idx, tr in enumerate(text_results, start=1):
        # Each text result gets its own page(s)
        c.showPage()
        page_num += 1
        _draw_header(c, (W, H), header_title)
        _draw_footer(c, (W, H), page_num, gen_time)
        y = H - HEADER_BAR_HEIGHT - 16

        res_title = f"文本资源 {idx}  (ID: {tr.text_resource_id})"
        y = _draw_section_title(c, y, W, res_title)

        # Verdict
        is_fake_val = tr.is_fake if tr.is_fake is not None else False
        conf = tr.confidence_score if tr.confidence_score is not None else 0.0
        y = _draw_verdict_badge(c, MARGIN + 8, y, is_fake_val, conf)
        y -= 4

        # Info box
        info_rows = [
            ("检测状态", tr.get_status_display() if hasattr(tr, 'get_status_display') else (tr.status or "-")),
            ("置信度分数", f"{conf:.4f}"),
        ]
        if tr.detection_time:
            info_rows.append(("检测时间", timezone.localtime(tr.detection_time).strftime("%Y-%m-%d %H:%M")))
        y, page_num = _ensure_space(c, y, W, H, 100, page_num, header_title, gen_time)
        y = _draw_info_box(c, y, W, info_rows, col_widths=110)
        y -= 6

        # Raw text preview
        text_res = tr.text_resource
        raw_text = text_res.raw_text if text_res and text_res.raw_text else ""
        if raw_text:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "原始文本摘要", level=2)
            preview = raw_text[:500] + ("..." if len(raw_text) > 500 else "")
            y = _draw_multiline(c, MARGIN + 8, y, preview, max_chars=72, size=8, leading=12)
            y -= 8

        # ── Paper-specific: AI generated paragraphs ──────────────────────────
        if is_paper:
            # Factual fake reason
            factual_reason = tr.factual_fake_reason or ""
            if factual_reason:
                y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
                y = _draw_section_title(c, y, W, "事实性鉴伪分析", level=2)
                y = _draw_multiline(c, MARGIN + 8, y, factual_reason, max_chars=72)
                y -= 8

            # AI generated paragraphs detail
            ai_paragraphs = []
            if tr.ai_generated_paragraphs:
                try:
                    ai_paragraphs = tr.ai_generated_paragraphs
                    if isinstance(ai_paragraphs, str):
                        ai_paragraphs = json.loads(ai_paragraphs)
                except Exception:
                    ai_paragraphs = []

            if ai_paragraphs:
                y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
                y = _draw_section_title(c, y, W, "AI 生成段落分析", level=2)

                for para in ai_paragraphs:
                    p_idx = para.get("paragraph_index", "?")
                    p_text = para.get("text", "")
                    p_prob = para.get("ai_probability", 0)
                    p_is_aigc = para.get("is_aigc", False)
                    p_reason = para.get("reason", "")

                    y, page_num = _ensure_space(c, y, W, H, 80, page_num, header_title, gen_time)

                    # Paragraph header with color coding
                    para_label = f"段落 {p_idx}"
                    if p_is_aigc:
                        c.setFillColor(COLOR_RED)
                        para_label += "  [AI生成]"
                    else:
                        c.setFillColor(COLOR_GREEN)
                        para_label += "  [非AI生成]"

                    c.setFont(FONT_BOLD, 9)
                    c.drawString(MARGIN + 8, y, para_label)
                    c.setFillColor(COLOR_BODY_TEXT)

                    # Probability
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 200, y, f"AI概率：{p_prob:.2%}")
                    y -= 14

                    # Text preview (shorten)
                    if p_text:
                        text_preview = p_text[:200] + ("..." if len(p_text) > 200 else "")
                        y = _draw_multiline(c, MARGIN + 16, y, text_preview, max_chars=68, size=8, leading=11)
                        y -= 4

                    # Reason
                    if p_reason:
                        y = _draw_multiline(c, MARGIN + 16, y, f"原因：{p_reason}", max_chars=68, size=8, leading=11)

                    # Divider
                    y -= 4
                    c.setStrokeColor(COLOR_LIGHT_GRAY)
                    c.setLineWidth(0.3)
                    c.line(MARGIN + 16, y, W - MARGIN - 16, y)
                    c.setLineWidth(1)
                    y -= 8

        # ── Review-specific: template tendency ────────────────────────────────
        else:
            template_score = tr.template_tendency_score
            template_reason = tr.template_analysis_reason or ""

            score_rows = []
            if template_score is not None:
                score_rows.append(("模板化倾向评分", f"{template_score:.4f}"))
            if template_reason:
                score_rows.append(("模板化分析", template_reason[:200]))

            if score_rows:
                y, page_num = _ensure_space(c, y, W, H, 60, page_num, header_title, gen_time)
                y = _draw_section_title(c, y, W, "模板化倾向分析", level=2)
                y = _draw_info_box(c, y, W, score_rows, col_widths=130)

                # If the template_reason is long, draw full text below
                if template_reason and len(template_reason) > 200:
                    y -= 4
                    y = _draw_multiline(c, MARGIN + 8, y, template_reason, max_chars=72, size=9)
                    y -= 6

            # Also show AI paragraphs if present (review texts may have them too)
            ai_paragraphs = []
            if tr.ai_generated_paragraphs:
                try:
                    ai_paragraphs = tr.ai_generated_paragraphs
                    if isinstance(ai_paragraphs, str):
                        ai_paragraphs = json.loads(ai_paragraphs)
                except Exception:
                    ai_paragraphs = []

            if ai_paragraphs:
                y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
                y = _draw_section_title(c, y, W, "AI 生成段落分析", level=2)

                for para in ai_paragraphs:
                    p_idx = para.get("paragraph_index", "?")
                    p_prob = para.get("ai_probability", 0)
                    p_is_aigc = para.get("is_aigc", False)
                    p_reason = para.get("reason", "")

                    y, page_num = _ensure_space(c, y, W, H, 60, page_num, header_title, gen_time)

                    para_label = f"段落 {p_idx}"
                    if p_is_aigc:
                        c.setFillColor(COLOR_RED)
                        para_label += "  [AI生成]"
                    else:
                        c.setFillColor(COLOR_GREEN)
                        para_label += "  [非AI生成]"
                    c.setFont(FONT_BOLD, 9)
                    c.drawString(MARGIN + 8, y, para_label)
                    c.setFillColor(COLOR_BODY_TEXT)
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 200, y, f"AI概率：{p_prob:.2%}")
                    y -= 14
                    if p_reason:
                        y = _draw_multiline(c, MARGIN + 16, y, p_reason, max_chars=68, size=8, leading=11)
                    y -= 6

    c.save()
    return _save_task_report(task, rel_path)


# ══════════════════════════════════════════════════════════════════════════════
# 3. Structured Detection Report (multi_material / 综合)
# ══════════════════════════════════════════════════════════════════════════════

def generate_structured_detection_report(task: DetectionTask) -> str:
    """
    Generate a PDF report for multi_material (综合检测) tasks.
    Writes task.report_file and returns the relative path.
    """
    rel_path, abs_path = _task_report_path(task)
    c = canvas.Canvas(abs_path, pagesize=A4)
    W, H = A4
    gen_time = _draw_cover_page(c, W, H, "综合检测报告", "多维度学术材料鉴伪分析", task)

    page_num = 1
    header_title = "听泉鉴图 - 综合检测报告"

    # ─── Page 1: Overall Summary ─────────────────────────────────────────────
    c.showPage()
    page_num += 1
    _draw_header(c, (W, H), header_title)
    _draw_footer(c, (W, H), page_num, gen_time)
    y = H - HEADER_BAR_HEIGHT - 16

    structured = None
    try:
        structured = task.structured_result
    except Exception:
        pass

    if structured:
        y = _draw_section_title(c, y, W, "总体结论")

        # Verdict badge
        overall_fake = structured.overall_is_fake if structured.overall_is_fake is not None else False
        overall_conf = structured.confidence_score if structured.confidence_score is not None else 0.0
        y = _draw_verdict_badge(c, MARGIN + 8, y, overall_fake, overall_conf)
        y -= 4

        # Summary info box
        summary_rows = [
            ("综合判定", "造假" if overall_fake else "真实"),
            ("综合置信度", f"{overall_conf:.4f}"),
        ]
        y = _draw_info_box(c, y, W, summary_rows, col_widths=110)
        y -= 6

        # Summary text
        if structured.summary:
            y = _draw_section_title(c, y, W, "检测摘要", level=2)
            y = _draw_multiline(c, MARGIN + 8, y, structured.summary, max_chars=72)
            y -= 8

        # ─── Result Payload Sections ──────────────────────────────────────────
        payload = {}
        if structured.result_payload:
            try:
                payload = structured.result_payload
                if isinstance(payload, str):
                    payload = json.loads(payload)
            except Exception:
                payload = {}

        # Overall section from payload
        overall_data = payload.get("overall", {})
        if overall_data:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "整体分析数据", level=2)
            rows = []
            for k, v in overall_data.items():
                rows.append((str(k), str(v)[:80]))
            if rows:
                y, page_num = _ensure_space(c, y, W, H, len(rows) * 20 + 20, page_num, header_title, gen_time)
                y = _draw_info_box(c, y, W, rows, col_widths=120)
                y -= 6

        # Per-section analysis
        per_section = payload.get("per_section", [])
        if per_section:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "分章节分析", level=2)

            for sec_idx, section in enumerate(per_section):
                y, page_num = _ensure_space(c, y, W, H, 60, page_num, header_title, gen_time)

                sec_name = section.get("section_name", section.get("name", f"章节 {sec_idx + 1}"))
                sec_fake = section.get("is_fake", section.get("fake", None))
                sec_conf = section.get("confidence", section.get("score", 0))
                sec_reason = section.get("reason", section.get("analysis", ""))

                # Section header with color
                if sec_fake is True:
                    c.setFillColor(COLOR_RED)
                    label = f"{sec_name}  - 疑似造假"
                elif sec_fake is False:
                    c.setFillColor(COLOR_GREEN)
                    label = f"{sec_name}  - 正常"
                else:
                    c.setFillColor(COLOR_BODY_TEXT)
                    label = sec_name

                c.setFont(FONT_BOLD, 10)
                c.drawString(MARGIN + 8, y, label)
                c.setFillColor(COLOR_BODY_TEXT)

                if isinstance(sec_conf, (int, float)):
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 250, y, f"置信度：{sec_conf:.4f}")

                y -= 14
                if sec_reason:
                    y = _draw_multiline(c, MARGIN + 16, y, str(sec_reason), max_chars=68, size=8, leading=11)
                y -= 4
                c.setStrokeColor(COLOR_LIGHT_GRAY)
                c.setLineWidth(0.3)
                c.line(MARGIN + 16, y, W - MARGIN - 16, y)
                c.setLineWidth(1)
                y -= 6

        # Image analysis from payload
        img_analysis = payload.get("image_analysis", [])
        if img_analysis:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "图像分析结果", level=2)

            for ia in img_analysis:
                y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
                ia_name = ia.get("image_name", ia.get("name", "图像"))
                ia_fake = ia.get("is_fake", ia.get("fake", None))
                ia_conf = ia.get("confidence", ia.get("score", 0))
                ia_reason = ia.get("reason", ia.get("analysis", ""))

                if ia_fake is True:
                    c.setFillColor(COLOR_RED)
                    label = f"{ia_name}  - 疑似造假"
                elif ia_fake is False:
                    c.setFillColor(COLOR_GREEN)
                    label = f"{ia_name}  - 正常"
                else:
                    c.setFillColor(COLOR_BODY_TEXT)
                    label = ia_name
                c.setFont(FONT_BOLD, 9)
                c.drawString(MARGIN + 8, y, label)
                c.setFillColor(COLOR_BODY_TEXT)

                if isinstance(ia_conf, (int, float)):
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 250, y, f"置信度：{ia_conf:.4f}")
                y -= 14

                if ia_reason:
                    y = _draw_multiline(c, MARGIN + 16, y, str(ia_reason), max_chars=68, size=8, leading=11)
                y -= 6

        # Text analysis from payload
        txt_analysis = payload.get("text_analysis", [])
        if txt_analysis:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "文本分析结果", level=2)

            for ta in txt_analysis:
                y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
                ta_name = ta.get("section_name", ta.get("name", "文本段"))
                ta_fake = ta.get("is_fake", ta.get("fake", None))
                ta_conf = ta.get("confidence", ta.get("score", 0))
                ta_reason = ta.get("reason", ta.get("analysis", ""))

                if ta_fake is True:
                    c.setFillColor(COLOR_RED)
                    label = f"{ta_name}  - 疑似AI生成"
                elif ta_fake is False:
                    c.setFillColor(COLOR_GREEN)
                    label = f"{ta_name}  - 正常"
                else:
                    c.setFillColor(COLOR_BODY_TEXT)
                    label = ta_name
                c.setFont(FONT_BOLD, 9)
                c.drawString(MARGIN + 8, y, label)
                c.setFillColor(COLOR_BODY_TEXT)

                if isinstance(ta_conf, (int, float)):
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 250, y, f"置信度：{ta_conf:.4f}")
                y -= 14
                if ta_reason:
                    y = _draw_multiline(c, MARGIN + 16, y, str(ta_reason), max_chars=68, size=8, leading=11)
                y -= 6

        # Cross analysis from payload
        cross_analysis = payload.get("cross_analysis", {})
        if cross_analysis:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "交叉分析", level=2)
            if isinstance(cross_analysis, dict):
                rows = [(str(k), str(v)[:100]) for k, v in cross_analysis.items()]
            elif isinstance(cross_analysis, str):
                rows = [("交叉分析", cross_analysis[:200])]
            else:
                rows = [("交叉分析", str(cross_analysis)[:200])]
            if rows:
                y, page_num = _ensure_space(c, y, W, H, len(rows) * 20 + 20, page_num, header_title, gen_time)
                y = _draw_info_box(c, y, W, rows, col_widths=120)
                y -= 6

        # AI Response
        ai_resp = {}
        if structured.ai_response:
            try:
                ai_resp = structured.ai_response
                if isinstance(ai_resp, str):
                    ai_resp = json.loads(ai_resp)
            except Exception:
                ai_resp = {}

        if ai_resp:
            y, page_num = _ensure_space(c, y, W, H, 60, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "AI 综合分析意见", level=2)
            # ai_response could be a dict with keys like 'analysis', 'conclusion', etc.
            if isinstance(ai_resp, dict):
                for resp_key, resp_val in ai_resp.items():
                    y, page_num = _ensure_space(c, y, W, H, 30, page_num, header_title, gen_time)
                    c.setFont(FONT_BOLD, 9)
                    c.drawString(MARGIN + 8, y, str(resp_key))
                    y -= 14
                    y = _draw_multiline(c, MARGIN + 16, y, str(resp_val), max_chars=68, size=8, leading=11)
                    y -= 8
            elif isinstance(ai_resp, str):
                y = _draw_multiline(c, MARGIN + 8, y, ai_resp, max_chars=72)
                y -= 8

    else:
        # No structured result yet
        y = _draw_section_title(c, y, W, "检测状态")
        c.setFont(FONT_REGULAR, 11)
        c.drawString(MARGIN + 8, y, "综合检测结果尚未生成或数据不可用。")
        y -= 30

    # ─── Image detection results (if any) ────────────────────────────────────
    image_results = task.detection_results.select_related(
        "image_upload"
    ).prefetch_related("sub_results").order_by("id")

    img_list = list(image_results)
    if img_list:
        c.showPage()
        page_num += 1
        _draw_header(c, (W, H), header_title)
        _draw_footer(c, (W, H), page_num, gen_time)
        y = H - HEADER_BAR_HEIGHT - 16

        y = _draw_section_title(c, y, W, "图像检测结果明细")

        for i_idx, dr in enumerate(img_list, start=1):
            y, page_num = _ensure_space(c, y, W, H, 120, page_num, header_title, gen_time)

            img_id = dr.image_upload_id
            is_fake_val = dr.is_fake if dr.is_fake is not None else False
            conf = dr.confidence_score if dr.confidence_score is not None else 0.0

            img_label = f"图片 {i_idx} (ID: {img_id})"
            y = _draw_verdict_badge(c, MARGIN + 8, y, is_fake_val, conf)

            # Thumbnail
            orig_path = dr.image_upload.image.path if dr.image_upload.image else None
            if orig_path and os.path.exists(orig_path):
                try:
                    img_reader = ImageReader(orig_path)
                    iw, ih = img_reader.getSize()
                    scale = min(100.0 / iw, 100.0 / ih, 1.0)
                    c.drawImage(img_reader, MARGIN + 200, y - 10,
                                width=int(iw * scale), height=int(ih * scale), preserveAspectRatio=True)
                except Exception:
                    pass

            # Quick info
            sub_count = dr.sub_results.count()
            info_rows = [
                ("判定结果", "造假" if is_fake_val else "真实"),
                ("置信度", f"{conf:.4f}"),
                ("子方法数", str(sub_count)),
                ("PS痕迹", "有" if dr.exif_photoshop else "无"),
                ("时间修改", "有" if dr.exif_time_modified else "无"),
            ]
            y = _draw_info_box(c, y, W, info_rows, col_widths=80)
            y -= 6

    # ─── Text detection results (if any) ─────────────────────────────────────
    text_results = task.text_detection_results.select_related("text_resource").order_by("id")
    txt_list = list(text_results)

    if txt_list:
        c.showPage()
        page_num += 1
        _draw_header(c, (W, H), header_title)
        _draw_footer(c, (W, H), page_num, gen_time)
        y = H - HEADER_BAR_HEIGHT - 16

        y = _draw_section_title(c, y, W, "文本检测结果明细")

        for t_idx, tr in enumerate(txt_list, start=1):
            y, page_num = _ensure_space(c, y, W, H, 120, page_num, header_title, gen_time)

            is_fake_val = tr.is_fake if tr.is_fake is not None else False
            conf = tr.confidence_score if tr.confidence_score is not None else 0.0

            y = _draw_section_title(c, y, W, f"文本资源 {t_idx} (ID: {tr.text_resource_id})", level=2)
            y = _draw_verdict_badge(c, MARGIN + 8, y, is_fake_val, conf)

            info_rows = [("置信度", f"{conf:.4f}")]
            if tr.detection_time:
                info_rows.append(("检测时间", timezone.localtime(tr.detection_time).strftime("%Y-%m-%d %H:%M")))
            if tr.factual_fake_reason:
                info_rows.append(("事实性鉴伪", tr.factual_fake_reason[:100]))
            if tr.template_tendency_score is not None:
                info_rows.append(("模板化评分", f"{tr.template_tendency_score:.4f}"))

            y = _draw_info_box(c, y, W, info_rows, col_widths=110)
            y -= 8

    c.save()
    return _save_task_report(task, rel_path)


# ══════════════════════════════════════════════════════════════════════════════
# Manual Review Report (kept intact from original)
# ══════════════════════════════════════════════════════════════════════════════

from ..models import ManualReview, ImageReview


def generate_manual_review_report(review: ManualReview) -> str:
    """
    生成人工审核 PDF 报告，返回相对路径，并写入 review.report_file
    """
    # 生成路径
    rel_path = f"reports/manual_review_{review.id}_report.pdf"
    abs_path = os.path.join(settings.MEDIA_ROOT, rel_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)

    c = canvas.Canvas(abs_path, pagesize=A4)
    W, H = A4
    MARGIN = 40

    # ─────────────────────── 封面页 ──────────────────────────
    c.bookmarkPage("cover")
    c.addOutlineEntry("人工审核概览", "cover", level=0)

    y = H - MARGIN - 20
    c.setFont(FONT_BOLD, 30)
    c.drawCentredString(W / 2, y, '"听泉鉴图"人工审核报告')
    y -= 60

    c.setFont(FONT_REGULAR, 18)
    c.drawString(MARGIN, y, f"审核编号：{review.id}")
    y -= 30
    # 获取关联的任务名称（通过 DetectionTask）
    task_name = "无"
    if review.review_request and review.review_request.detection_result:
        detection_task = review.review_request.detection_result.detection_task
        if detection_task and detection_task.task_name:
            task_name = detection_task.task_name

    c.drawString(MARGIN, y, f"关联任务名称：{task_name}")

    y -= 30
    c.drawString(MARGIN, y, f"提交用户：{review.reviewer.username}")
    y -= 30

    start_time = timezone.localtime(review.review_time).strftime("%Y-%m-%d %H:%M")
    end_time = review.review_request and review.review_request.review_end_time
    finish_time = end_time and timezone.localtime(end_time).strftime("%Y-%m-%d %H:%M") or '尚未完成'

    c.drawString(MARGIN, y, f"开始时间：{start_time}")
    y -= 30
    c.drawString(MARGIN, y, f"结束时间：{finish_time}")
    y -= 30

    # 审核者列表
    # 因为 ManualReview 只有一个 reviewer 字段
    if review.reviewer:
        reviewer_names = review.reviewer.username
    else:
        reviewer_names = "未指定"

    c.drawString(MARGIN, y, f"审核人员：{reviewer_names}")
    y -= 50

    # 审核图片列表
    image_ids = ", ".join(str(img.id) for img in review.imgs.all())
    c.setFont(FONT_BOLD, 14)
    c.drawString(MARGIN, y, "审核图像列表：")
    y -= 20
    c.setFont(FONT_REGULAR, 12)
    for img in review.imgs.all():
        y = _draw_multiline(c, MARGIN + 10, y, f"图片 {img.id} —— 路径：{img.image.name}", max_chars=90)
        y -= 10
        if y < MARGIN + 50:
            c.showPage()
            y = H - MARGIN
    y -= 20

    # ─────────────────────── 每张图片审核详情 ──────────────────────────
    for img_review in review.img_reviews.all():
        image_upload = img_review.img
        page_label = f"图片 {image_upload.id} 的人工审核"
        c.bookmarkPage(f"manual_img_{image_upload.id}")
        c.addOutlineEntry(page_label, f"manual_img_{image_upload.id}", level=1)

        c.setFont(FONT_BOLD, 14)
        c.drawString(MARGIN, y, page_label)
        y -= 20

        # 图像预览
        image_path = image_upload.image.path
        if os.path.exists(image_path):
            c.drawImage(ImageReader(image_path), MARGIN, y - 120, width=120, height=120, preserveAspectRatio=True)

        # 审核结果
        c.setFont("SimSun", 12)
        y -= 140
        result_text = "判定为假图" if img_review.result else "判定为真图"
        c.drawString(MARGIN, y, f"最终判定：{result_text}")
        y -= 20
        c.drawString(MARGIN, y, f"审核时间：{timezone.localtime(img_review.review_time):%Y-%m-%d %H:%M}")
        y -= 20

        # 各个评分项与理由
        c.setFont("SimSun-Bold", 12)
        c.drawString(MARGIN, y, "各维度评分与理由：")
        y -= 20
        c.setFont("SimSun", 12)

        methods = {
            1: ("Method-1", img_review.score1, img_review.reason1),
            2: ("Method-2", img_review.score2, img_review.reason2),
            3: ("Method-3", img_review.score3, img_review.reason3),
            4: ("Method-4", img_review.score4, img_review.reason4),
            5: ("Method-5", img_review.score5, img_review.reason5),
            6: ("Method-6", img_review.score6, img_review.reason6),
            7: ("Method-7", img_review.score7, img_review.reason7),
        }

        for method_id, (method_name, score, reason) in methods.items():
            reason_text = reason or '无'
            line_text = f"{method_name}：得分 {score}, 理由：“{reason_text}”"
            y = _draw_multiline(c, MARGIN + 10, y, line_text,
                                max_chars=80, font='SimSun', size=11)
            y -= 10
            if y < MARGIN + 50:
                c.showPage()
                y = H - MARGIN

        # JSON 格式的点集
        points_data = {}
        try:
            points_data = json.loads(img_review.points1) if img_review.points1 else []
        except Exception:
            pass
        c.setFont("SimSun", 10)
        y -= 10
        c.drawString(MARGIN, y, "点集数据示例（Method-1）:")
        y -= 20
        sample_points = str(points_data)[:80] + ('...' if len(str(points_data)) > 80 else '')
        y = _draw_multiline(c, MARGIN + 10, y, sample_points, max_chars=80, font='SimSun', size=10)
        y -= 30

        if y < MARGIN + 50:
            c.showPage()
            y = H - MARGIN

        c.showPage()

    # ─────────────────────── 保存文件 ──────────────────────────
    c.save()
    review.report_file = rel_path
    review.save(update_fields=["report_file"])
    return rel_path
