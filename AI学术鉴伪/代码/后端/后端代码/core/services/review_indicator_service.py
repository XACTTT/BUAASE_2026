"""
材料审核指标配置服务

为四种材料类型(image/paper/review/multi)定义各自的:
- 检测指标维度
- 审核方式和表单
- AI辅助信息字段
"""

# ============================================================
# 图像审核指标配置
# ============================================================
IMAGE_REVIEW_DIMENSIONS = [
    {
        'index': 1,
        'key': 'gaussian_blur',
        'name': '高斯模糊',
        'description': '检测图像中高斯模糊伪造痕迹，通常用于掩盖篡改区域',
        'score_type': 'degree',  # 1-5等级评分
        'score_labels': {1: '轻微', 2: '一般', 3: '中等', 4: '明显', 5: '严重'},
        'has_annotation': True,   # 是否支持绘图标注
        'ai_field': 'probability',  # AI检测结果中的对应字段
    },
    {
        'index': 2,
        'key': 'brightness_contrast',
        'name': '亮度/对比度调节',
        'description': '检测图像中亮度或对比度异常调整的痕迹',
        'score_type': 'degree',
        'score_labels': {1: '轻微', 2: '一般', 3: '中等', 4: '明显', 5: '严重'},
        'has_annotation': True,
        'ai_field': 'probability',
    },
    {
        'index': 3,
        'key': 'inpainting',
        'name': '智能修复',
        'description': '检测使用智能修复(Inpainting)工具进行篡改的痕迹',
        'score_type': 'degree',
        'score_labels': {1: '轻微', 2: '一般', 3: '中等', 4: '明显', 5: '严重'},
        'has_annotation': True,
        'ai_field': 'probability',
    },
    {
        'index': 4,
        'key': 'brute_force',
        'name': '暴力覆盖',
        'description': '检测图像区域被直接覆盖或替换的痕迹',
        'score_type': 'degree',
        'score_labels': {1: '轻微', 2: '一般', 3: '中等', 4: '明显', 5: '严重'},
        'has_annotation': True,
        'ai_field': 'probability',
    },
    {
        'index': 5,
        'key': 'same_image_copy',
        'name': '同图复制',
        'description': '检测同一图像内区域复制移动的伪造痕迹',
        'score_type': 'degree',
        'score_labels': {1: '轻微', 2: '一般', 3: '中等', 4: '明显', 5: '严重'},
        'has_annotation': True,
        'ai_field': 'probability',
    },
    {
        'index': 6,
        'key': 'overlap_cut',
        'name': '重叠切割',
        'description': '检测图像中重叠切割拼接的伪造痕迹',
        'score_type': 'degree',
        'score_labels': {1: '轻微', 2: '一般', 3: '中等', 4: '明显', 5: '严重'},
        'has_annotation': True,
        'ai_field': 'probability',
    },
    {
        'index': 7,
        'key': 'cross_image_splice',
        'name': '跨图拼接',
        'description': '检测从不同图像中截取区域进行拼接的伪造痕迹',
        'score_type': 'degree',
        'score_labels': {1: '轻微', 2: '一般', 3: '中等', 4: '明显', 5: '严重'},
        'has_annotation': True,
        'ai_field': 'probability',
    },
]

# ============================================================
# 论文文本审核指标配置
# ============================================================
PAPER_REVIEW_INDICATORS = {
    'material_type': 'paper_text',
    'display_name': '论文文本',
    'review_mode': 'text',
    'indicators': [
        {
            'key': 'paragraph_ai_review',
            'name': '段落AI生成复核',
            'description': '逐段验证AI标记的疑似生成段落，判断是否确实为AI生成',
            'input_type': 'paragraph_toggle',  # 每段：同意AI/不同意AI + 评论
            'ai_fields': ['ai_generated_paragraphs', 'factual_fake_reason'],
            'per_item': True,  # 是否针对每个段落独立评分
        },
        {
            'key': 'overall_comment',
            'name': '综合审核意见',
            'description': '对论文文本整体的真实性和原创性给出综合评价',
            'input_type': 'textarea',
            'required': True,
        },
        {
            'key': 'final_judgment',
            'name': '最终判定',
            'description': '综合所有审核维度给出最终判定',
            'input_type': 'boolean',  # 造假/真实
            'required': True,
        },
    ],
    'ai_assist_fields': [
        {'field': 'is_fake', 'label': 'AI判定', 'type': 'boolean'},
        {'field': 'confidence_score', 'label': 'AI置信度', 'type': 'score'},
        {'field': 'ai_generated_paragraphs', 'label': 'AI生成段落', 'type': 'paragraph_list',
         'sub_fields': ['paragraph_index', 'ai_probability', 'text', 'reason']},
        {'field': 'factual_fake_reason', 'label': '事实性造假分析', 'type': 'text'},
    ],
}

# ============================================================
# 审稿文本审核指标配置
# ============================================================
REVIEW_REVIEW_INDICATORS = {
    'material_type': 'review_text',
    'display_name': '审稿文本',
    'review_mode': 'text',
    'indicators': [
        {
            'key': 'template_tendency',
            'name': '模板化倾向评分',
            'description': '评估审稿文本的模板化程度，判断是否使用了固定模板或AI生成',
            'input_type': 'slider',  # 0-100滑块
            'min': 0,
            'max': 100,
            'ai_field': 'template_tendency_score',
            'required': True,
        },
        {
            'key': 'template_comment',
            'name': '模板化倾向评论',
            'description': '对模板化倾向的具体分析和说明',
            'input_type': 'textarea',
            'required': False,
        },
        {
            'key': 'paragraph_ai_review',
            'name': '段落AI生成复核',
            'description': '逐段验证AI标记的疑似生成段落(如存在)',
            'input_type': 'paragraph_toggle',
            'ai_fields': ['ai_generated_paragraphs'],
            'per_item': True,
        },
        {
            'key': 'overall_comment',
            'name': '综合审核意见',
            'description': '对审稿文本整体的质量和真实性给出综合评价',
            'input_type': 'textarea',
            'required': True,
        },
        {
            'key': 'final_judgment',
            'name': '最终判定',
            'description': '综合所有审核维度给出最终判定',
            'input_type': 'boolean',
            'required': True,
        },
    ],
    'ai_assist_fields': [
        {'field': 'is_fake', 'label': 'AI判定', 'type': 'boolean'},
        {'field': 'confidence_score', 'label': 'AI置信度', 'type': 'score'},
        {'field': 'template_tendency_score', 'label': '模板化倾向', 'type': 'score',
         'thresholds': {'high': 0.7, 'medium': 0.4}},
        {'field': 'template_analysis_reason', 'label': '模板化分析', 'type': 'text'},
        {'field': 'ai_generated_paragraphs', 'label': 'AI生成段落', 'type': 'paragraph_list',
         'sub_fields': ['paragraph_index', 'ai_probability', 'text', 'reason']},
    ],
}

# ============================================================
# 综合材料审核指标配置(组合以上三种)
# ============================================================
MULTI_REVIEW_INDICATORS = {
    'material_type': 'multi_material',
    'display_name': '综合材料',
    'review_mode': 'multi',
    'sub_materials': {
        'image': {
            'dimensions': IMAGE_REVIEW_DIMENSIONS,
            'review_method': '逐图7维度评分+标注',
        },
        'paper': {
            'indicators': PAPER_REVIEW_INDICATORS['indicators'],
            'ai_assist_fields': PAPER_REVIEW_INDICATORS['ai_assist_fields'],
            'review_method': '段落复核+综合意见',
        },
        'review': {
            'indicators': REVIEW_REVIEW_INDICATORS['indicators'],
            'ai_assist_fields': REVIEW_REVIEW_INDICATORS['ai_assist_fields'],
            'review_method': '模板化评估+段落复核+综合意见',
        },
    },
}

# ============================================================
# 材料类型统一配置映射
# ============================================================
MATERIAL_REVIEW_CONFIG = {
    'image': {
        'task_types': ['image'],
        'display_name': '图像检测',
        'review_mode': 'image',
        'review_method': '逐图7维度评分+标注+最终判定',
        'dimensions': IMAGE_REVIEW_DIMENSIONS,
        'indicators': [],
        'ai_assist_fields': [
            {'field': 'is_fake', 'label': 'AI判定', 'type': 'boolean'},
            {'field': 'confidence_score', 'label': 'AI置信度', 'type': 'score'},
            {'field': 'sub_methods', 'label': '子方法概率', 'type': 'method_list'},
            {'field': 'llm_judgment', 'label': 'LLM判定', 'type': 'text'},
            {'field': 'exif_photoshop', 'label': 'PS检测', 'type': 'boolean'},
        ],
    },
    'paper_text': {
        'task_types': ['paper_text'],
        'display_name': '论文文本',
        'review_mode': 'text',
        'review_method': '段落AI复核+综合意见+最终判定',
        'dimensions': [],
        'indicators': PAPER_REVIEW_INDICATORS['indicators'],
        'ai_assist_fields': PAPER_REVIEW_INDICATORS['ai_assist_fields'],
    },
    'review_text': {
        'task_types': ['review_text'],
        'display_name': '审稿文本',
        'review_mode': 'text',
        'review_method': '模板化评估+段落复核+综合意见+最终判定',
        'dimensions': [],
        'indicators': REVIEW_REVIEW_INDICATORS['indicators'],
        'ai_assist_fields': REVIEW_REVIEW_INDICATORS['ai_assist_fields'],
    },
    'multi_material': {
        'task_types': ['multi_material'],
        'display_name': '综合检测',
        'review_mode': 'multi',
        'review_method': '图像7维度+文本段落复核+模板化评估+最终判定',
        'dimensions': IMAGE_REVIEW_DIMENSIONS,
        'indicators': (
            PAPER_REVIEW_INDICATORS['indicators'] +
            REVIEW_REVIEW_INDICATORS['indicators']
        ),
        'ai_assist_fields': (
            [{'field': 'overall_is_fake', 'label': 'AI综合判定', 'type': 'boolean'},
             {'field': 'confidence_score', 'label': 'AI综合置信度', 'type': 'score'}] +
            PAPER_REVIEW_INDICATORS['ai_assist_fields'] +
            REVIEW_REVIEW_INDICATORS['ai_assist_fields']
        ),
    },
}

# 统一的任务类型标签(中文)
TASK_TYPE_LABELS = {
    'image': '图像检测',
    'paper_text': '论文文本',
    'review_text': '审稿文本',
    'multi_material': '综合检测',
}

# 统一的任务类型颜色
TASK_TYPE_COLORS = {
    'image': 'blue',
    'paper_text': 'green',
    'review_text': 'orange',
    'multi_material': 'purple',
}


def get_review_config(task_type):
    """根据任务类型获取审核配置"""
    # 映射detect_type到task_type
    type_mapping = {
        'image': 'image',
        'paper': 'paper_text',
        'review': 'review_text',
        'multi': 'multi_material',
    }
    normalized = type_mapping.get(task_type, task_type)
    return MATERIAL_REVIEW_CONFIG.get(normalized)


def get_review_mode(task_type):
    """根据任务类型获取审核模式(image/text/multi)"""
    config = get_review_config(task_type)
    return config['review_mode'] if config else 'image'


def get_review_dimensions(task_type):
    """根据任务类型获取审核维度列表"""
    config = get_review_config(task_type)
    return config.get('dimensions', []) if config else []


def get_review_indicators(task_type):
    """根据任务类型获取审核指标列表"""
    config = get_review_config(task_type)
    return config.get('indicators', []) if config else []


def get_task_type_label(task_type):
    """获取任务类型的中文标签"""
    return TASK_TYPE_LABELS.get(task_type, '未知类型')


def get_task_type_color(task_type):
    """获取任务类型的颜色"""
    return TASK_TYPE_COLORS.get(task_type, 'grey')
