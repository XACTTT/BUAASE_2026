export interface SubMethod {
  method: string
  probability: number
  mask_matrix: number[][]
}

export interface ImageDetectionData {
  result_id: number
  timestamps: string
  image: string
  llm: string
  llm_image: string
  exif: {
    photoshop_edited: boolean
    time_modified: boolean
  }
  overall: {
    is_fake: boolean
    confidence_score: number
  }
  sub_methods: SubMethod[]
}

export interface ParagraphInfo {
  paragraph_index: number
  text: string
  ai_probability: number
  reason: string
}

export interface PaperTextDetectionData {
  result_id: number
  resource_id: number
  detection_time: string
  is_fake: boolean
  confidence_score: number
  factual_fake_reason: string
  ai_generated_paragraphs: ParagraphInfo[]
}

export interface ReviewTextDetectionData {
  result_id: number
  resource_id: number
  detection_time: string
  is_fake: boolean
  confidence_score: number
  template_tendency_score: number
  template_analysis_reason: string
}

const createMaskMatrix = (size = 256, hotStart = 80, hotEnd = 176) => {
  return Array.from({ length: size }, (_, y) =>
    Array.from({ length: size }, (_, x) => {
      if (x >= hotStart && x <= hotEnd && y >= hotStart && y <= hotEnd) {
        return 0.75
      }
      return 0.08
    })
  )
}

export const sampleImageData: ImageDetectionData = {
  result_id: 1001,
  timestamps: '2026-05-11 09:20:00',
  image: 'https://picsum.photos/seed/fake-image/512/512',
  llm: '大模型认为图像中心区域存在明显不自然纹理与边缘融合痕迹，疑似经过局部编辑。',
  llm_image: 'https://picsum.photos/seed/fake-mask/256/256',
  exif: {
    photoshop_edited: true,
    time_modified: false,
  },
  overall: {
    is_fake: true,
    confidence_score: 0.82,
  },
  sub_methods: [
    {
      method: 'splicing',
      probability: 0.87,
      mask_matrix: createMaskMatrix(),
    },
    {
      method: 'blurring',
      probability: 0.71,
      mask_matrix: createMaskMatrix(256, 96, 160),
    },
    {
      method: 'contrast',
      probability: 0.42,
      mask_matrix: createMaskMatrix(256, 64, 144),
    },
  ],
}

export const samplePaperData: PaperTextDetectionData = {
  result_id: 2001,
  resource_id: 301,
  detection_time: '2026-05-11 09:20:00',
  is_fake: true,
  confidence_score: 0.78,
  factual_fake_reason: '文中多个段落在论证结构和措辞上高度趋同，且存在较明显的模板化总结语气。',
  ai_generated_paragraphs: [
    {
      paragraph_index: 1,
      text: '本文提出了一种高效且鲁棒的统一框架，可显著提升多场景检测性能。',
      ai_probability: 0.91,
      reason: '段落使用了高度模板化的学术表述，信息密度与句式结构呈现典型生成痕迹。',
    },
    {
      paragraph_index: 2,
      text: '实验结果表明，该方法在多个公开数据集上均取得了优于基线方法的表现。',
      ai_probability: 0.73,
      reason: '结论表达较为泛化，缺少与具体实验现象强绑定的解释细节。',
    },
    {
      paragraph_index: 3,
      text: '此外，我们还从可解释性和泛化能力两个维度对模型进行了补充分析。',
      ai_probability: 0.31,
      reason: '该段表述较自然，但仍保留一定总结式句法特征。',
    },
  ],
}

export const sampleReviewData: ReviewTextDetectionData = {
  result_id: 3001,
  resource_id: 401,
  detection_time: '2026-05-11 09:20:00',
  is_fake: false,
  confidence_score: 0.22,
  template_tendency_score: 0.28,
  template_analysis_reason: '该 Review 提供了较具体的问题定位和修改建议，表达方式具有一定个性化特征。',
}

export const sampleReviewDataTemplate: ReviewTextDetectionData = {
  result_id: 3002,
  resource_id: 402,
  detection_time: '2026-05-11 09:20:00',
  is_fake: true,
  confidence_score: 0.84,
  template_tendency_score: 0.83,
  template_analysis_reason: '该 Review 大量使用泛化评价语句，结构重复且缺少与论文内容强绑定的针对性意见。',
}
