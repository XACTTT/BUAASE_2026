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

def _is_mask_blank(image_path):
    """Return True if mask image is entirely black (no forgery detected)."""
    try:
        from PIL import Image
        import numpy as np
        return bool(np.array(Image.open(image_path).convert('L')).max() == 0)
    except Exception:
        return False

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
    """Draw a branded cover page. Does NOT call c.showPage() — caller handles page transitions."""
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
            METHOD_LABELS = {
                'splicing': '拼接检测', 'blurring': '模糊检测',
                'bruteforce': '暴力篡改检测', 'contrast': '对比度检测',
                'inpainting': '修复检测',
            }
            for sub in sub_results:
                method_name = METHOD_LABELS.get(sub.method, sub.method)
                prob = sub.probability if sub.probability is not None else 0.0
                sub_rows.append((method_name, f"{prob:.4f}"))

            y, page_num = _ensure_space(c, y, W, H, len(sub_rows) * 20 + 30, page_num, header_title, gen_time)
            y = _draw_info_box(c, y, W, sub_rows, col_widths=110)

            # Mask images for each sub result
            for sub in sub_results:
                if sub.mask_image and hasattr(sub.mask_image, 'path') and os.path.exists(sub.mask_image.path):
                    method_label = METHOD_LABELS.get(sub.method, sub.method)
                    if _is_mask_blank(sub.mask_image.path):
                        y, page_num = _ensure_space(c, y, W, H, 30, page_num, header_title, gen_time)
                        c.setFont(FONT_REGULAR, 8)
                        c.setFillColor(COLOR_FOOTER_TEXT)
                        c.drawString(MARGIN + 8, y, f"{method_label} - 热力图：未检测到异常区域")
                        c.setFillColor(Color(0, 0, 0))
                        y -= 20
                        continue
                    y, page_num = _ensure_space(c, y, W, H, 90, page_num, header_title, gen_time)
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
                    except Exception as e:
                        import logging
                        logging.getLogger(__name__).warning(f"Failed to draw mask for {sub.method}: {e}")

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

    # ── Structured Detection Result Page (rich content from StructuredDetectionResult) ──
    structured = None
    try:
        structured = task.structured_result
    except Exception:
        pass

    if structured:
        c.showPage()
        page_num += 1
        _draw_header(c, (W, H), header_title)
        _draw_footer(c, (W, H), page_num, gen_time)
        y = H - HEADER_BAR_HEIGHT - 16

        # ── 1. Overall Conclusion ──
        y = _draw_section_title(c, y, W, "综合检测结论")

        overall_fake = structured.overall_is_fake if structured.overall_is_fake is not None else False
        overall_conf = structured.confidence_score if structured.confidence_score is not None else 0.0
        y = _draw_verdict_badge(c, MARGIN + 8, y, overall_fake, overall_conf)
        y -= 4

        # Parse payload for risk_level and other structured data
        payload = {}
        if structured.result_payload:
            try:
                payload = structured.result_payload
                if isinstance(payload, str):
                    payload = json.loads(payload)
            except Exception:
                payload = {}

        overall_data = payload.get("overall", {})
        risk_level = overall_data.get("risk_level", "-")

        conclusion_rows = [
            ("综合判定", "造假" if overall_fake else "真实"),
            ("综合置信度", f"{overall_conf:.1%}"),
            ("风险等级", str(risk_level)),
        ]
        y, page_num = _ensure_space(c, y, W, H, 80, page_num, header_title, gen_time)
        y = _draw_info_box(c, y, W, conclusion_rows, col_widths=110)
        y -= 6

        # ── 2. Summary ──
        if structured.summary:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "检测摘要", level=2)
            y = _draw_multiline(c, MARGIN + 8, y, structured.summary, max_chars=72)
            y -= 8

        # ── 3. Dimensions Table ──
        dimensions = payload.get("dimensions", [])
        if dimensions:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "检测维度评分", level=2)

            dim_rows = []
            for dim in dimensions:
                dim_name = dim.get("name", "-")
                dim_score = dim.get("score", 0)
                dim_summary = dim.get("summary", "")
                if isinstance(dim_score, (int, float)):
                    dim_rows.append((dim_name, f"{dim_score:.2f}  |  {dim_summary}"))
                else:
                    dim_rows.append((dim_name, str(dim_summary)))

            y, page_num = _ensure_space(c, y, W, H, len(dim_rows) * 20 + 20, page_num, header_title, gen_time)
            y = _draw_info_box(c, y, W, dim_rows, col_widths=130)
            y -= 8

        # ── 4. Evidence Statistics ──
        evidence = payload.get("evidence", {})
        if evidence:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "AIGC 检测统计", level=2)

            ev_stat_rows = [
                ("检测模型", str(evidence.get("model_dir", "-"))),
                ("文本语言", str(evidence.get("lang", "-"))),
                ("总段落数", str(evidence.get("section_count", "-"))),
                ("AIGC段落数", str(evidence.get("aigc_section_count", "-"))),
            ]

            aggregate = evidence.get("aggregate", {})
            if aggregate:
                ev_stat_rows.extend([
                    ("AIGC比例", f"{aggregate.get('aigc_ratio', 0):.1%}"),
                    ("平均AIGC概率", f"{aggregate.get('mean_aigc_probability', 0):.4f}"),
                    ("平均置信度", f"{aggregate.get('mean_confidence', 0):.4f}"),
                    ("最高置信度", f"{aggregate.get('max_confidence', 0):.4f}"),
                    ("最低置信度", f"{aggregate.get('min_confidence', 0):.4f}"),
                ])

            y, page_num = _ensure_space(c, y, W, H, len(ev_stat_rows) * 20 + 20, page_num, header_title, gen_time)
            y = _draw_info_box(c, y, W, ev_stat_rows, col_widths=130)
            y -= 8

        # ── 5. Per-Section Analysis ──
        per_section = evidence.get("per_section", [])
        if per_section:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "逐段落 AI 生成检测", level=2)

            for sec_idx, sec in enumerate(per_section):
                # Each section needs ~80px minimum
                y, page_num = _ensure_space(c, y, W, H, 80, page_num, header_title, gen_time)

                sec_title = sec.get("title", f"段落 {sec_idx + 1}")
                sec_is_aigc = sec.get("is_aigc", False)
                sec_label_name = sec.get("label_name", "")
                sec_confidence = sec.get("confidence_score", 0)
                sec_item_id = sec.get("item_id", "")
                sec_page_num = sec.get("page_number")
                sec_source = sec.get("source_file", "")
                sec_text = sec.get("text", "")
                sec_probs = sec.get("probabilities", {})

                # Color-coded header line
                if sec_is_aigc:
                    c.setFillColor(COLOR_RED)
                    status_tag = " [AIGC]"
                else:
                    c.setFillColor(COLOR_GREEN)
                    status_tag = " [非AIGC]"

                header_text = f"{sec_title}{status_tag}"
                c.setFont(FONT_BOLD, 9)
                c.drawString(MARGIN + 8, y, header_text)

                # Confidence and label on the same line, right-aligned area
                c.setFillColor(COLOR_BODY_TEXT)
                c.setFont(FONT_REGULAR, 8)
                conf_text = f"{sec_label_name}  置信度: {sec_confidence:.2%}"
                c.drawString(MARGIN + 220, y, conf_text)
                y -= 14

                # Probabilities row
                human_prob = sec_probs.get("human", 0)
                aigc_prob = sec_probs.get("aigc", 0)
                c.setFont(FONT_REGULAR, 8)
                c.drawString(MARGIN + 16, y, f"人工概率: {human_prob:.2%}  AIGC概率: {aigc_prob:.2%}")
                y -= 12

                # Source metadata
                meta_parts = []
                if sec_page_num is not None:
                    meta_parts.append(f"页码: {sec_page_num}")
                if sec_source:
                    meta_parts.append(f"来源: {sec_source}")
                if meta_parts:
                    c.setFont(FONT_REGULAR, 7)
                    c.setFillColor(COLOR_FOOTER_TEXT)
                    c.drawString(MARGIN + 16, y, "  |  ".join(meta_parts))
                    c.setFillColor(COLOR_BODY_TEXT)
                    y -= 12

                # Text preview (shorten to 300 chars)
                if sec_text:
                    text_preview = sec_text[:300] + ("..." if len(sec_text) > 300 else "")
                    y = _draw_multiline(c, MARGIN + 16, y, text_preview, max_chars=68, size=8, leading=11)

                # Divider
                y -= 4
                c.setStrokeColor(COLOR_LIGHT_GRAY)
                c.setLineWidth(0.3)
                c.line(MARGIN + 16, y, W - MARGIN - 16, y)
                c.setLineWidth(1)
                y -= 8

        # ── LLM Analysis from payload ──
        llm_analysis = payload.get("llm_analysis", "")
        if llm_analysis:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "大语言模型分析", level=2)
            y = _draw_multiline(c, MARGIN + 8, y, str(llm_analysis), max_chars=72)
            y -= 8

    # ── End of Structured Result Section ──

    if not text_results.exists() and not structured:
        # No data at all — draw a notice on the cover page
        c.setFont(FONT_REGULAR, 11)
        c.setFillColor(COLOR_FOOTER_TEXT)
        c.drawCentredString(W / 2, 280, "暂无检测数据")
        c.setFillColor(COLOR_BODY_TEXT)
        c.save()
        return _save_task_report(task, rel_path)

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

        # ── Dimensions (paper/review tasks) ───────────────────────────────────
        dimensions = payload.get("dimensions", [])
        if dimensions:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "评分维度", level=2)
            for dim in dimensions:
                y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
                dim_name = dim.get("name", "维度")
                dim_score = dim.get("score", None)
                dim_summary = dim.get("summary", "")

                c.setFont(FONT_BOLD, 9)
                c.drawString(MARGIN + 8, y, dim_name)
                if isinstance(dim_score, (int, float)):
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 250, y, f"评分：{dim_score:.2f}")
                y -= 14
                if dim_summary:
                    y = _draw_multiline(c, MARGIN + 16, y, str(dim_summary), max_chars=68, size=8, leading=11)
                y -= 4
                c.setStrokeColor(COLOR_LIGHT_GRAY)
                c.setLineWidth(0.3)
                c.line(MARGIN + 16, y, W - MARGIN - 16, y)
                c.setLineWidth(1)
                y -= 6

        # ── Validation info ───────────────────────────────────────────────────
        validation = payload.get("validation", {})
        if validation:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "数据校验", level=2)
            val_rows = []
            if "valid" in validation:
                val_rows.append(("校验结果", "通过" if validation["valid"] else "未通过"))
            if "message" in validation:
                val_rows.append(("校验信息", str(validation["message"])[:100]))
            if "missing_required" in validation:
                missing = validation["missing_required"]
                if isinstance(missing, list):
                    val_rows.append(("缺失项", ", ".join(str(m) for m in missing)[:100]))
                else:
                    val_rows.append(("缺失项", str(missing)[:100]))
            for k, v in validation.items():
                if k not in ("valid", "message", "missing_required"):
                    val_rows.append((str(k), str(v)[:80]))
            if val_rows:
                y, page_num = _ensure_space(c, y, W, H, len(val_rows) * 20 + 20, page_num, header_title, gen_time)
                y = _draw_info_box(c, y, W, val_rows, col_widths=110)
                y -= 6

        # ── Evidence statistics ────────────────────────────────────────────────
        evidence_data = payload.get("evidence", {})
        if evidence_data:
            aggregate = evidence_data.get("aggregate", {})
            has_aggregate = bool(aggregate)
            section_count = evidence_data.get("section_count")
            aigc_section_count = evidence_data.get("aigc_section_count")
            lang = evidence_data.get("lang", "")
            model_dir = evidence_data.get("model_dir", "")

            if has_aggregate or section_count is not None or lang:
                y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
                y = _draw_section_title(c, y, W, "证据统计", level=2)
                stat_rows = []
                if lang:
                    stat_rows.append(("文档语言", lang))
                if model_dir:
                    stat_rows.append(("检测模型", model_dir))
                if section_count is not None:
                    stat_rows.append(("总章节数", str(section_count)))
                if aigc_section_count is not None:
                    stat_rows.append(("AIGC章节数", str(aigc_section_count)))
                if aggregate:
                    aigc_ratio = aggregate.get("aigc_ratio")
                    if isinstance(aigc_ratio, (int, float)):
                        stat_rows.append(("AIGC占比", f"{aigc_ratio:.2%}"))
                    mean_prob = aggregate.get("mean_aigc_probability")
                    if isinstance(mean_prob, (int, float)):
                        stat_rows.append(("平均AIGC概率", f"{mean_prob:.4f}"))
                    mean_conf = aggregate.get("mean_confidence")
                    if isinstance(mean_conf, (int, float)):
                        stat_rows.append(("平均置信度", f"{mean_conf:.4f}"))
                    max_conf = aggregate.get("max_confidence")
                    if isinstance(max_conf, (int, float)):
                        stat_rows.append(("最大置信度", f"{max_conf:.4f}"))
                    min_conf = aggregate.get("min_confidence")
                    if isinstance(min_conf, (int, float)):
                        stat_rows.append(("最小置信度", f"{min_conf:.4f}"))
                if stat_rows:
                    y, page_num = _ensure_space(c, y, W, H, len(stat_rows) * 20 + 20, page_num, header_title, gen_time)
                    y = _draw_info_box(c, y, W, stat_rows, col_widths=120)
                    y -= 6

        # ── Material cards (multi tasks) ──────────────────────────────────────
        material_cards = payload.get("material_cards", [])
        if material_cards:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "材料卡片", level=2)
            for mc_idx, card in enumerate(material_cards):
                y, page_num = _ensure_space(c, y, W, H, 60, page_num, header_title, gen_time)
                mc_type = card.get("type", "未知")
                mc_label = card.get("label", f"材料 {mc_idx + 1}")
                mc_summary = card.get("summary", "")
                mc_score = card.get("score", None)
                mc_file_count = card.get("file_count", 0)

                # Card header
                type_label = {"paper": "论文", "review": "评审", "image": "图像"}.get(mc_type, mc_type)
                c.setFont(FONT_BOLD, 10)
                c.setFillColor(COLOR_ACCENT)
                c.drawString(MARGIN + 8, y, f"[{type_label}] {mc_label}")
                c.setFillColor(COLOR_BODY_TEXT)
                if isinstance(mc_score, (int, float)):
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 250, y, f"评分：{mc_score:.2f}")
                y -= 14

                if mc_summary:
                    y = _draw_multiline(c, MARGIN + 16, y, str(mc_summary), max_chars=68, size=8, leading=11)

                if mc_file_count:
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 16, y, f"文件数量：{mc_file_count}")
                    y -= 12

                # Files list
                mc_files = card.get("files", [])
                if mc_files:
                    c.setFont(FONT_REGULAR, 8)
                    for f_idx, f_info in enumerate(mc_files[:10]):
                        f_name = f_info.get("file_name", f_info.get("name", f"文件{f_idx + 1}"))
                        f_id = f_info.get("file_id", f_info.get("id", ""))
                        c.drawString(MARGIN + 24, y, f"- {f_name} (ID: {f_id})")
                        y -= 11
                        if y < CONTENT_MIN_Y:
                            y, page_num = _ensure_space(c, y, W, H, 30, page_num, header_title, gen_time)

                y -= 4
                c.setStrokeColor(COLOR_LIGHT_GRAY)
                c.setLineWidth(0.3)
                c.line(MARGIN + 16, y, W - MARGIN - 16, y)
                c.setLineWidth(1)
                y -= 6

        # ── Per-section analysis (from evidence.per_section) ──────────────────
        per_section = evidence_data.get("per_section", []) if evidence_data else []
        if per_section:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "分章节分析", level=2)

            for sec_idx, section in enumerate(per_section):
                y, page_num = _ensure_space(c, y, W, H, 60, page_num, header_title, gen_time)

                sec_title = section.get("title", section.get("item_id", f"章节 {sec_idx + 1}"))
                sec_is_aigc = section.get("is_aigc", None)
                sec_conf = section.get("confidence_score", 0)
                sec_label = section.get("label_name", "")
                sec_text = section.get("text", "")
                sec_page = section.get("page_number")
                sec_source = section.get("source_file", "")
                probabilities = section.get("probabilities", {})

                # Section header with color
                if sec_is_aigc is True:
                    c.setFillColor(COLOR_RED)
                    label = f"{sec_title}  - 疑似AIGC"
                elif sec_is_aigc is False:
                    c.setFillColor(COLOR_GREEN)
                    label = f"{sec_title}  - 正常"
                else:
                    c.setFillColor(COLOR_BODY_TEXT)
                    label = sec_title

                c.setFont(FONT_BOLD, 10)
                c.drawString(MARGIN + 8, y, label)
                c.setFillColor(COLOR_BODY_TEXT)

                # Confidence and label on the right
                detail_parts = []
                if isinstance(sec_conf, (int, float)):
                    detail_parts.append(f"置信度：{sec_conf:.4f}")
                if sec_label:
                    detail_parts.append(f"标签：{sec_label}")
                if detail_parts:
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 250, y, "  ".join(detail_parts))

                y -= 14

                # Probabilities
                if probabilities:
                    prob_str = f"Human: {probabilities.get('human', 0):.2%}  AIGC: {probabilities.get('aigc', 0):.2%}"
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 16, y, prob_str)
                    y -= 12

                # Page number and source
                meta_parts = []
                if sec_page is not None:
                    meta_parts.append(f"页码：{sec_page}")
                if sec_source:
                    meta_parts.append(f"来源：{sec_source[:40]}")
                if meta_parts:
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 16, y, "  ".join(meta_parts))
                    y -= 12

                # Text excerpt
                if sec_text:
                    excerpt = sec_text[:200] + ("..." if len(sec_text) > 200 else "")
                    y = _draw_multiline(c, MARGIN + 16, y, excerpt, max_chars=68, size=8, leading=11)

                y -= 4
                c.setStrokeColor(COLOR_LIGHT_GRAY)
                c.setLineWidth(0.3)
                c.line(MARGIN + 16, y, W - MARGIN - 16, y)
                c.setLineWidth(1)
                y -= 6

        # ── Image analysis (from material_cards type='image') ─────────────────
        img_cards = [mc for mc in material_cards if mc.get("type") == "image"] if material_cards else []
        img_analysis = []
        for ic in img_cards:
            for img in ic.get("images", []):
                img_analysis.append(img)
        if img_analysis:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "图像分析结果", level=2)

            for ia in img_analysis:
                y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
                ia_id = ia.get("image_id", "图像")
                ia_fake = ia.get("is_fake", None)
                ia_conf = ia.get("confidence", 0)
                ia_methods = ia.get("sub_methods", [])

                if ia_fake is True:
                    c.setFillColor(COLOR_RED)
                    label = f"图像 {ia_id}  - 疑似造假"
                elif ia_fake is False:
                    c.setFillColor(COLOR_GREEN)
                    label = f"图像 {ia_id}  - 正常"
                else:
                    c.setFillColor(COLOR_BODY_TEXT)
                    label = f"图像 {ia_id}"
                c.setFont(FONT_BOLD, 9)
                c.drawString(MARGIN + 8, y, label)
                c.setFillColor(COLOR_BODY_TEXT)

                if isinstance(ia_conf, (int, float)):
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 250, y, f"置信度：{ia_conf:.4f}")
                y -= 14

                if ia_methods:
                    methods_str = ", ".join(str(m) for m in ia_methods)[:120]
                    c.setFont(FONT_REGULAR, 8)
                    c.drawString(MARGIN + 16, y, f"子方法：{methods_str}")
                    y -= 12
                y -= 6

        # ── Cross material analysis ───────────────────────────────────────────
        cross_analysis = payload.get("cross_material_analysis", {})
        if cross_analysis:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "交叉分析", level=2)

            cross_checks = cross_analysis.get("cross_checks", [])
            mismatches = cross_analysis.get("mismatches", [])
            recommendations = cross_analysis.get("recommendations", [])

            if cross_checks:
                c.setFont(FONT_BOLD, 9)
                c.drawString(MARGIN + 8, y, "交叉校验项")
                y -= 14
                for cc in cross_checks:
                    y, page_num = _ensure_space(c, y, W, H, 14, page_num, header_title, gen_time)
                    y = _draw_multiline(c, MARGIN + 16, y, str(cc), max_chars=68, size=8, leading=11)
                y -= 4

            if mismatches:
                y, page_num = _ensure_space(c, y, W, H, 30, page_num, header_title, gen_time)
                c.setFont(FONT_BOLD, 9)
                c.setFillColor(COLOR_RED)
                c.drawString(MARGIN + 8, y, "不一致项")
                c.setFillColor(COLOR_BODY_TEXT)
                y -= 14
                for mm in mismatches:
                    y, page_num = _ensure_space(c, y, W, H, 14, page_num, header_title, gen_time)
                    y = _draw_multiline(c, MARGIN + 16, y, str(mm), max_chars=68, size=8, leading=11)
                y -= 4

            if recommendations:
                y, page_num = _ensure_space(c, y, W, H, 30, page_num, header_title, gen_time)
                c.setFont(FONT_BOLD, 9)
                c.drawString(MARGIN + 8, y, "建议")
                y -= 14
                for rec in recommendations:
                    y, page_num = _ensure_space(c, y, W, H, 14, page_num, header_title, gen_time)
                    y = _draw_multiline(c, MARGIN + 16, y, str(rec), max_chars=68, size=8, leading=11)
                y -= 4

            # Fallback: render any other keys in cross_analysis
            other_keys = [k for k in cross_analysis if k not in ("cross_checks", "mismatches", "recommendations")]
            if other_keys:
                other_rows = [(str(k), str(cross_analysis[k])[:100]) for k in other_keys]
                y, page_num = _ensure_space(c, y, W, H, len(other_rows) * 20 + 20, page_num, header_title, gen_time)
                y = _draw_info_box(c, y, W, other_rows, col_widths=120)
                y -= 6

        # ── AI contribution ───────────────────────────────────────────────────
        ai_contribution = payload.get("ai_contribution", [])
        if ai_contribution:
            y, page_num = _ensure_space(c, y, W, H, 50, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "AI 贡献分析", level=2)
            for ac_item in ai_contribution:
                y, page_num = _ensure_space(c, y, W, H, 16, page_num, header_title, gen_time)
                if isinstance(ac_item, str):
                    y = _draw_multiline(c, MARGIN + 16, y, ac_item, max_chars=68, size=8, leading=11)
                else:
                    y = _draw_multiline(c, MARGIN + 16, y, str(ac_item), max_chars=68, size=8, leading=11)
                y -= 4

        # AI Response (from structured.ai_response field)
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
# Manual Review Report
# ══════════════════════════════════════════════════════════════════════════════

from ..models import (
    ManualReview, ImageReview, TextReview,
    ReviewRequest, TextDetectionResult, StructuredDetectionResult,
)

DIMENSION_NAMES = {
    1: '高斯模糊', 2: '亮度/对比度调节', 3: '智能修复',
    4: '暴力覆盖', 5: '同图复制', 6: '重叠切割', 7: '跨图拼接',
}
SCORE_LABELS = {1: '轻微', 2: '一般', 3: '中等', 4: '明显', 5: '严重'}
METHOD_LABELS = {
    'splicing': '拼接检测', 'blurring': '模糊检测',
    'bruteforce': '暴力篡改检测', 'contrast': '对比度检测',
    'inpainting': '修复检测', 'method6': '同图复制检测', 'method7': '跨图拼接检测',
}
TASK_TYPE_LABELS = {
    'image': '图像检测', 'paper_text': '论文文本检测',
    'review_text': '审稿文本检测', 'multi_material': '综合材料检测',
    'paper': '论文文本检测', 'review': '审稿文本检测', 'multi': '综合材料检测',
}


def _resolve_detection_task_rr(rr):
    """Resolve the DetectionTask from a ReviewRequest (same logic as views_review)."""
    dt = getattr(rr, 'detection_task', None)
    if dt:
        return dt
    if rr.detection_result and hasattr(rr.detection_result, 'detection_task'):
        return rr.detection_result.detection_task
    if rr.text_detection_result and hasattr(rr.text_detection_result, 'detection_task'):
        return rr.text_detection_result.detection_task
    return None


def _resolve_task_type_rr(rr):
    """Resolve task_type string from a ReviewRequest."""
    dt = _resolve_detection_task_rr(rr)
    if dt:
        return dt.task_type or dt.detect_type or 'unknown'
    return 'unknown'


def _normalize_task_type(raw):
    """Normalize detect_type values to standard task_type names."""
    mapping = {'multi': 'multi_material', 'paper': 'paper_text', 'review': 'review_text'}
    return mapping.get(raw, raw)


def _manual_report_path(review_request):
    rel_path = f"reports/manual_review_rr_{review_request.id}_report.pdf"
    abs_path = os.path.join(settings.MEDIA_ROOT, rel_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    return rel_path, abs_path


# ─── Cover page for manual review report ─────────────────────────────────────

def _draw_manual_cover_page(c, W, H, review_request, task_type, manual_reviews, detection_task):
    gen_time = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")

    cover_bg_h = 220
    c.setFillColor(COLOR_HEADER_BG)
    c.rect(0, H - cover_bg_h, W, cover_bg_h, fill=1, stroke=0)
    c.setStrokeColor(COLOR_ACCENT)
    c.setLineWidth(3)
    c.line(0, H - cover_bg_h, W, H - cover_bg_h)

    c.setFillColor(COLOR_WHITE)
    c.setFont(FONT_BOLD, 38)
    c.drawCentredString(W / 2, H - 90, "听泉鉴图")
    c.setFont(FONT_REGULAR, 14)
    c.drawCentredString(W / 2, H - 120, "AI-Powered Academic Integrity Analysis Platform")

    title_map = {
        'image': '图像造假人工审核报告',
        'paper_text': '论文文本人工审核报告',
        'review_text': '审稿文本人工审核报告',
        'multi_material': '综合材料人工审核报告',
    }
    title = title_map.get(task_type, '人工审核报告')
    c.setFont(FONT_BOLD, 18)
    c.drawCentredString(W / 2, H - 170, title)

    c.setFillColor(COLOR_BODY_TEXT)
    y = H - cover_bg_h - 50
    reviewer_names = ', '.join(
        mr.reviewer.username for mr in manual_reviews if mr.reviewer
    ) or '未指定'
    task_name = detection_task.task_name if detection_task and detection_task.task_name else "无"
    type_label = TASK_TYPE_LABELS.get(task_type, task_type)
    info_items = [
        ("审核请求编号", str(review_request.id)),
        ("任务类型", type_label),
        ("提交用户", review_request.user.username if review_request.user else ""),
        ("审核员", reviewer_names),
        ("申请时间", timezone.localtime(review_request.request_time).strftime("%Y-%m-%d %H:%M") if review_request.request_time else "-"),
        ("关联检测任务", task_name),
    ]
    for label, value in info_items:
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, y, label)
        c.setFont(FONT_REGULAR, 11)
        c.drawString(MARGIN + 100, y, f"：{value}")
        y -= 22

    c.setFillColor(COLOR_FOOTER_TEXT)
    c.setFont(FONT_REGULAR, 8)
    c.drawCentredString(W / 2, 50, f"报告生成时间：{gen_time}")
    c.setFillColor(COLOR_BODY_TEXT)
    return gen_time


# ─── Image review page ───────────────────────────────────────────────────────

def _draw_image_review_pages(c, y, W, H, page_num, header_title, gen_time,
                              img_upload, image_reviews_list, ai_dr):
    """Draw all reviewer results for one image. Returns (y, page_num)."""
    c.showPage()
    page_num += 1
    _draw_header(c, (W, H), header_title)
    _draw_footer(c, (W, H), page_num, gen_time)
    y = H - HEADER_BAR_HEIGHT - 16

    y = _draw_section_title(c, y, W, f"图片审核 (ID: {img_upload.id})")

    # thumbnail
    img_path = img_upload.image.path if img_upload.image else None
    if img_path and os.path.exists(img_path):
        try:
            reader = ImageReader(img_path)
            iw, ih = reader.getSize()
            scale = min(120.0 / iw, 120.0 / ih, 1.0)
            dw, dh = int(iw * scale), int(ih * scale)
            c.drawImage(reader, MARGIN + 8, y - dh, width=dw, height=dh, preserveAspectRatio=True)
            y -= dh + 8
        except Exception:
            pass

    # aggregate verdict
    any_fake = any(ir.result for ir in image_reviews_list if ir.result is not None)
    y = _draw_verdict_badge(c, MARGIN + 8, y, any_fake)
    y -= 4

    # per-reviewer
    for ir in image_reviews_list:
        reviewer_name = ir.manual_review.reviewer.username if ir.manual_review and ir.manual_review.reviewer else "未知"
        review_time_str = timezone.localtime(ir.review_time).strftime("%Y-%m-%d %H:%M") if ir.review_time else "-"

        y, page_num = _ensure_space(c, y, W, H, 200, page_num, header_title, gen_time)
        y = _draw_section_title(c, y, W, f"审核员：{reviewer_name}（{review_time_str}）", level=2)

        y = _draw_verdict_badge(c, MARGIN + 8, y, bool(ir.result))
        y -= 4

        # 7-dimension scores table
        score_rows = []
        for dim_id in range(1, 8):
            score_val = getattr(ir, f'score{dim_id}', None)
            label = SCORE_LABELS.get(score_val, '-') if score_val else '-'
            score_rows.append((DIMENSION_NAMES[dim_id], f"{score_val or '-'} ({label})"))
        y, page_num = _ensure_space(c, y, W, H, len(score_rows) * 20 + 30, page_num, header_title, gen_time)
        y = _draw_info_box(c, y, W, score_rows, col_widths=120)
        y -= 6

        # reasons
        y = _draw_section_title(c, y, W, "各维度审核理由", level=3)
        for dim_id in range(1, 8):
            reason = getattr(ir, f'reason{dim_id}', None)
            if reason:
                y, page_num = _ensure_space(c, y, W, H, 30, page_num, header_title, gen_time)
                c.setFont(FONT_BOLD, 9)
                c.drawString(MARGIN + 8, y, f"{DIMENSION_NAMES[dim_id]}：")
                y -= 14
                y = _draw_multiline(c, MARGIN + 16, y, reason, max_chars=70)
                y -= 4

    # AI detection reference
    if ai_dr:
        y, page_num = _ensure_space(c, y, W, H, 120, page_num, header_title, gen_time)
        y = _draw_section_title(c, y, W, "AI 检测参考", level=2)
        ai_rows = [
            ("AI 判定", "造假" if ai_dr.is_fake else "真实"),
            ("AI 置信度", f"{ai_dr.confidence_score:.4f}" if ai_dr.confidence_score else "-"),
            ("Photoshop 痕迹", "有" if ai_dr.exif_photoshop else "无"),
            ("时间修改痕迹", "有" if ai_dr.exif_time_modified else "无"),
        ]
        if ai_dr.detection_time:
            ai_rows.append(("AI 检测时间", timezone.localtime(ai_dr.detection_time).strftime("%Y-%m-%d %H:%M")))
        y, page_num = _ensure_space(c, y, W, H, len(ai_rows) * 20 + 30, page_num, header_title, gen_time)
        y = _draw_info_box(c, y, W, ai_rows, col_widths=110)
        y -= 4

        # sub-method probabilities
        sub_results = list(ai_dr.sub_results.all())
        if sub_results:
            sub_rows = []
            for sub in sub_results:
                method_label = METHOD_LABELS.get(sub.method, sub.method)
                prob = sub.probability if sub.probability is not None else 0.0
                sub_rows.append((method_label, f"{prob:.4f}"))
            y, page_num = _ensure_space(c, y, W, H, len(sub_rows) * 20 + 30, page_num, header_title, gen_time)
            y = _draw_info_box(c, y, W, sub_rows, col_widths=120)

    return y, page_num


# ─── Text review page ────────────────────────────────────────────────────────

def _draw_text_review_pages(c, y, W, H, page_num, header_title, gen_time,
                             text_resource, text_reviews_list, ai_text_det,
                             task_type, structured_result):
    """Draw all reviewer results for one text resource. Returns (y, page_num)."""
    c.showPage()
    page_num += 1
    _draw_header(c, (W, H), header_title)
    _draw_footer(c, (W, H), page_num, gen_time)
    y = H - HEADER_BAR_HEIGHT - 16

    is_paper = task_type in ('paper_text', 'paper')
    is_review = task_type in ('review_text', 'review')
    type_tag = "论文" if is_paper else "审稿" if is_review else "文本"

    y = _draw_section_title(c, y, W, f"{type_tag}文本审核 (ID: {text_resource.id})")

    # aggregate verdict
    any_fake = any(tr.result for tr in text_reviews_list if tr.result is not None)
    y = _draw_verdict_badge(c, MARGIN + 8, y, any_fake)
    y -= 4

    # text summary
    if text_resource.raw_text:
        y, page_num = _ensure_space(c, y, W, H, 60, page_num, header_title, gen_time)
        y = _draw_section_title(c, y, W, "文本摘要", level=2)
        summary_text = text_resource.raw_text[:500] + ('...' if len(text_resource.raw_text) > 500 else '')
        y = _draw_multiline(c, MARGIN + 8, y, summary_text, max_chars=72)
        y -= 6

    # per-reviewer
    for tr in text_reviews_list:
        reviewer_name = tr.manual_review.reviewer.username if tr.manual_review and tr.manual_review.reviewer else "未知"
        review_time_str = timezone.localtime(tr.review_time).strftime("%Y-%m-%d %H:%M") if tr.review_time else "-"

        y, page_num = _ensure_space(c, y, W, H, 100, page_num, header_title, gen_time)
        y = _draw_section_title(c, y, W, f"审核员：{reviewer_name}（{review_time_str}）", level=2)

        y = _draw_verdict_badge(c, MARGIN + 8, y, bool(tr.result))
        y -= 4

        # template review (review_text)
        if is_review and tr.template_review_score is not None:
            template_rows = [
                ("模板化倾向评分", f"{tr.template_review_score:.1%}"),
            ]
            if tr.template_review_comment:
                template_rows.append(("模板化倾向评论", tr.template_review_comment[:80]))
            y, page_num = _ensure_space(c, y, W, H, len(template_rows) * 20 + 30, page_num, header_title, gen_time)
            y = _draw_info_box(c, y, W, template_rows, col_widths=120)
            y -= 4

        # paragraph reviews
        if tr.paragraph_reviews:
            try:
                paragraphs = tr.paragraph_reviews if isinstance(tr.paragraph_reviews, list) else json.loads(tr.paragraph_reviews)
            except Exception:
                paragraphs = []
            if paragraphs:
                y, page_num = _ensure_space(c, y, W, H, 40, page_num, header_title, gen_time)
                y = _draw_section_title(c, y, W, "段落 AI 生成复核", level=3)
                for pr in paragraphs[:10]:
                    idx = pr.get('paragraph_index', '?')
                    agreed = "同意AI判定" if pr.get('is_ai_agreed') else "不同意AI判定"
                    comment = pr.get('comment', '')
                    y, page_num = _ensure_space(c, y, W, H, 30, page_num, header_title, gen_time)
                    c.setFont(FONT_REGULAR, 9)
                    c.drawString(MARGIN + 8, y, f"段落 {idx}：[{agreed}]")
                    y -= 14
                    if comment:
                        y = _draw_multiline(c, MARGIN + 16, y, f"意见：{comment}", max_chars=68)
                        y -= 4

        # overall comment
        if tr.overall_comment:
            y, page_num = _ensure_space(c, y, W, H, 40, page_num, header_title, gen_time)
            y = _draw_section_title(c, y, W, "综合审核意见", level=3)
            y = _draw_multiline(c, MARGIN + 8, y, tr.overall_comment, max_chars=72)
            y -= 6

    # AI detection reference
    y, page_num = _ensure_space(c, y, W, H, 80, page_num, header_title, gen_time)
    y = _draw_section_title(c, y, W, "AI 检测参考", level=2)

    if ai_text_det:
        ai_rows = [
            ("AI 判定", "造假" if ai_text_det.is_fake else "真实"),
            ("AI 置信度", f"{ai_text_det.confidence_score:.4f}" if ai_text_det.confidence_score else "-"),
        ]
        if ai_text_det.detection_time:
            ai_rows.append(("AI 检测时间", timezone.localtime(ai_text_det.detection_time).strftime("%Y-%m-%d %H:%M")))
        y, page_num = _ensure_space(c, y, W, H, len(ai_rows) * 20 + 30, page_num, header_title, gen_time)
        y = _draw_info_box(c, y, W, ai_rows, col_widths=110)
        y -= 4

        # paper-specific: factual fake reason
        if is_paper and ai_text_det.factual_fake_reason:
            y, page_num = _ensure_space(c, y, W, H, 40, page_num, header_title, gen_time)
            c.setFont(FONT_BOLD, 9)
            c.drawString(MARGIN + 8, y, "事实性鉴伪分析：")
            y -= 14
            y = _draw_multiline(c, MARGIN + 16, y, ai_text_det.factual_fake_reason[:300], max_chars=70)
            y -= 4

        # review-specific: template tendency
        if is_review and ai_text_det.template_tendency_score is not None:
            template_ai_rows = [
                ("AI 模板化倾向评分", f"{ai_text_det.template_tendency_score:.1%}"),
            ]
            if ai_text_det.template_analysis_reason:
                template_ai_rows.append(("AI 模板化分析", ai_text_det.template_analysis_reason[:80]))
            y, page_num = _ensure_space(c, y, W, H, len(template_ai_rows) * 20 + 30, page_num, header_title, gen_time)
            y = _draw_info_box(c, y, W, template_ai_rows, col_widths=130)
            y -= 4

        # AI generated paragraphs
        if ai_text_det.ai_generated_paragraphs:
            try:
                paragraphs = ai_text_det.ai_generated_paragraphs if isinstance(ai_text_det.ai_generated_paragraphs, list) else json.loads(ai_text_det.ai_generated_paragraphs)
            except Exception:
                paragraphs = []
            if paragraphs:
                y, page_num = _ensure_space(c, y, W, H, 40, page_num, header_title, gen_time)
                y = _draw_section_title(c, y, W, "AI 生成段落标记", level=3)
                for para in paragraphs[:8]:
                    pidx = para.get('paragraph_index', '?')
                    prob = para.get('ai_probability', 0)
                    reason = para.get('reason', '')
                    text_preview = para.get('text', '')[:50]
                    y, page_num = _ensure_space(c, y, W, H, 40, page_num, header_title, gen_time)
                    c.setFont(FONT_BOLD, 9)
                    c.drawString(MARGIN + 8, y, f"段落 {pidx} [AI生成] 概率：{prob:.1%}")
                    y -= 14
                    if text_preview:
                        y = _draw_multiline(c, MARGIN + 16, y, text_preview, max_chars=68)
                    if reason:
                        y = _draw_multiline(c, MARGIN + 16, y, f"原因：{reason}", max_chars=68)
                    y -= 4
    elif structured_result:
        # fallback to structured result for AI reference
        payload = {}
        if structured_result.result_payload:
            try:
                payload = structured_result.result_payload if isinstance(structured_result.result_payload, dict) else json.loads(structured_result.result_payload)
            except Exception:
                pass
        overall = payload.get('overall', {})
        sdr_rows = [
            ("AI 综合判定", "造假" if overall.get('is_fake') else "真实"),
            ("AI 综合置信度", f"{overall.get('confidence_score', 0):.1%}"),
            ("风险等级", str(overall.get('risk_level', '-'))),
        ]
        y, page_num = _ensure_space(c, y, W, H, len(sdr_rows) * 20 + 30, page_num, header_title, gen_time)
        y = _draw_info_box(c, y, W, sdr_rows, col_widths=110)

    return y, page_num


# ─── Main function ───────────────────────────────────────────────────────────

def generate_manual_review_report(review_request):
    """
    Generate a comprehensive manual review PDF report for a ReviewRequest.
    Covers all reviewers, all material types (image/paper_text/review_text/multi_material).
    """
    rel_path, abs_path = _manual_report_path(review_request)
    c = canvas.Canvas(abs_path, pagesize=A4)
    W, H = A4

    # ── 1. Data preloading ──
    manual_reviews = list(
        ManualReview.objects.filter(review_request=review_request)
        .select_related('reviewer')
        .prefetch_related('image_reviews', 'text_reviews')
    )

    task_type = _normalize_task_type(_resolve_task_type_rr(review_request))
    detection_task = _resolve_detection_task_rr(review_request)

    # index image reviews: {img_id: [ImageReview, ...]}
    img_reviews_by_img = {}
    for mr in manual_reviews:
        for ir in mr.image_reviews.all():
            img_reviews_by_img.setdefault(ir.img_id, []).append(ir)

    # index text reviews: {text_resource_id: [TextReview, ...]}
    text_reviews_by_res = {}
    for mr in manual_reviews:
        for tr in mr.text_reviews.all():
            text_reviews_by_res.setdefault(tr.text_resource_id, []).append(tr)

    # AI detection data
    ai_image_results = {}
    ai_text_results = {}
    structured_result = None
    if detection_task:
        for dr in detection_task.detection_results.select_related('image_upload').prefetch_related('sub_results'):
            ai_image_results[dr.image_upload_id] = dr
        for tdr in detection_task.text_detection_results.select_related('text_resource'):
            ai_text_results[tdr.text_resource_id] = tdr
        try:
            structured_result = detection_task.structured_result
        except Exception:
            pass

    # ── 2. Cover page ──
    gen_time = _draw_manual_cover_page(c, W, H, review_request, task_type, manual_reviews, detection_task)

    page_num = 1
    header_title = "听泉鉴图 - 人工审核报告"

    # ── 3. Summary page ──
    c.showPage()
    page_num += 1
    _draw_header(c, (W, H), header_title)
    _draw_footer(c, (W, H), page_num, gen_time)
    y = H - HEADER_BAR_HEIGHT - 16

    y = _draw_section_title(c, y, W, "审核结果汇总")

    # overall verdict
    all_reviewer_results = []
    for mr in manual_reviews:
        for ir in mr.image_reviews.all():
            if ir.result is not None:
                all_reviewer_results.append(ir.result)
        for tr in mr.text_reviews.all():
            if tr.result is not None:
                all_reviewer_results.append(tr.result)
    overall_fake = any(all_reviewer_results)
    y = _draw_verdict_badge(c, MARGIN + 8, y, overall_fake)
    y -= 4

    images = list(review_request.imgs.all())
    texts = list(review_request.text_resources.all())
    # fallback texts from manual reviews
    if not texts:
        for mr in manual_reviews:
            for tr in mr.text_reviews.all():
                if tr.text_resource and tr.text_resource not in texts:
                    texts.append(tr.text_resource)

    fake_count = sum(1 for r in all_reviewer_results if r)
    real_count = sum(1 for r in all_reviewer_results if not r)

    summary_rows = [
        ("审核员数量", str(len(manual_reviews))),
        ("审核材料数量", f"{len(images)} 张图片, {len(texts)} 份文本"),
        ("判定为假", str(fake_count)),
        ("判定为真", str(real_count)),
    ]
    y, page_num = _ensure_space(c, y, W, H, len(summary_rows) * 20 + 30, page_num, header_title, gen_time)
    y = _draw_info_box(c, y, W, summary_rows, col_widths=110)
    y -= 8

    # per-reviewer summary
    y, page_num = _ensure_space(c, y, W, H, 40, page_num, header_title, gen_time)
    y = _draw_section_title(c, y, W, "各审核员判定", level=2)
    for mr in manual_reviews:
        name = mr.reviewer.username if mr.reviewer else "未知"
        status_str = "已完成" if mr.status == 'completed' else "未审核"
        time_str = timezone.localtime(mr.review_time).strftime("%Y-%m-%d %H:%M") if mr.review_time and mr.status == 'completed' else "-"
        mr_fake = False
        for ir in mr.image_reviews.all():
            if ir.result:
                mr_fake = True
        for tr in mr.text_reviews.all():
            if tr.result:
                mr_fake = True
        verdict = "造假" if mr_fake else "真实"
        y = _draw_metric_row(c, y, f"{name}（{status_str}）", verdict, is_fake=mr_fake if mr.status == 'completed' else None)
        y -= 2
    y -= 4

    # AI detection summary
    if detection_task:
        y, page_num = _ensure_space(c, y, W, H, 60, page_num, header_title, gen_time)
        y = _draw_section_title(c, y, W, "AI 检测参考摘要", level=2)
        if structured_result:
            overall = {}
            if structured_result.result_payload:
                try:
                    payload = structured_result.result_payload if isinstance(structured_result.result_payload, dict) else json.loads(structured_result.result_payload)
                    overall = payload.get('overall', {})
                except Exception:
                    pass
            ai_sum_rows = [
                ("AI 综合判定", "造假" if overall.get('is_fake') else "真实"),
                ("AI 综合置信度", f"{overall.get('confidence_score', 0):.1%}"),
            ]
            y, page_num = _ensure_space(c, y, W, H, len(ai_sum_rows) * 20 + 30, page_num, header_title, gen_time)
            y = _draw_info_box(c, y, W, ai_sum_rows, col_widths=110)
        elif ai_image_results:
            for img_id, dr in ai_image_results.items():
                ai_sum_rows = [
                    ("图片 AI 判定", "造假" if dr.is_fake else "真实"),
                    ("AI 置信度", f"{dr.confidence_score:.4f}" if dr.confidence_score else "-"),
                ]
                y, page_num = _ensure_space(c, y, W, H, len(ai_sum_rows) * 20 + 30, page_num, header_title, gen_time)
                y = _draw_info_box(c, y, W, ai_sum_rows, col_widths=110)
                y -= 4

    # ── 4. Content pages by type ──
    is_image = task_type == 'image'
    is_text = task_type in ('paper_text', 'review_text')
    is_multi = task_type == 'multi_material'

    if is_image or is_multi:
        for img in images:
            ir_list = img_reviews_by_img.get(img.id, [])
            ai_dr = ai_image_results.get(img.id)
            y, page_num = _draw_image_review_pages(
                c, y, W, H, page_num, header_title, gen_time,
                img, ir_list, ai_dr,
            )

    if is_text or is_multi:
        for txt in texts:
            tr_list = text_reviews_by_res.get(txt.id, [])
            ai_td = ai_text_results.get(txt.id)
            y, page_num = _draw_text_review_pages(
                c, y, W, H, page_num, header_title, gen_time,
                txt, tr_list, ai_td, task_type, structured_result,
            )

    # ── 5. Save ──
    c.save()
    # write report_file to the first completed ManualReview
    for mr in manual_reviews:
        if mr.status == 'completed':
            mr.report_file = rel_path
            mr.save(update_fields=["report_file"])
            break
    return rel_path
