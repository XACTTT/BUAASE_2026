<script setup lang="ts">
import { computed, ref } from 'vue'
import { samplePaperData, type PaperTextDetectionData, type ParagraphInfo } from './mocks/sampleData'

interface Props {
  task_id?: string
  task_type?: string
}

const props = defineProps<Props>()

// 使用样例数据
const data = ref<PaperTextDetectionData>(samplePaperData)

// 统计信息
const statistics = computed(() => {
  const total = data.value.ai_generated_paragraphs.length
  const highProb = data.value.ai_generated_paragraphs.filter(p => p.ai_probability > 0.8).length
  const mediumProb = data.value.ai_generated_paragraphs.filter(p => p.ai_probability > 0.5 && p.ai_probability <= 0.8).length
  const lowProb = data.value.ai_generated_paragraphs.filter(p => p.ai_probability <= 0.5).length
  
  return { total, highProb, mediumProb, lowProb }
})

// 综合结论
const overallConclusion = computed(() => {
  if (data.value.is_fake) {
    return {
      result: '判定为AI生成论文',
      confidence: (data.value.confidence_score * 100).toFixed(1) + '%',
      color: 'error'
    }
  } else {
    return {
      result: '判定为人工撰写论文',
      confidence: ((1 - data.value.confidence_score) * 100).toFixed(1) + '%',
      color: 'success'
    }
  }
})

// 选中的段落（用于显示详情）
const selectedParagraph = ref<ParagraphInfo | null>(null)
const showDetailDialog = ref(false)

// 显示段落详情
function showParagraphDetail(paragraph: ParagraphInfo) {
  selectedParagraph.value = paragraph
  showDetailDialog.value = true
}

// 获取概率颜色
function getProbabilityColor(probability: number): string {
  if (probability > 0.8) return 'error'
  if (probability > 0.5) return 'warning'
  return 'success'
}

// 获取概率等级
function getProbabilityLevel(probability: number): string {
  if (probability > 0.8) return '高风险'
  if (probability > 0.5) return '中风险'
  return '低风险'
}

// 获取概率类名
function getProbabilityClass(probability: number): string {
  if (probability > 0.8) return 'high-probability'
  if (probability > 0.5) return 'medium-probability'
  return 'low-probability'
}
</script>

<template>
  <v-container fluid class="pa-4">
    <!-- 标题栏 -->
    <v-row>
      <v-col cols="12">
        <h2 class="text-h4 mb-2">论文文本检测结果审核</h2>
        <p class="text-body-1 text-grey">
          检测ID: {{ data.result_id }} | 资源ID: {{ data.resource_id }} | 检测时间: {{ data.detection_time }}
        </p>
      </v-col>
    </v-row>

    <!-- 综合结论卡片 -->
    <v-row>
      <v-col cols="12">
        <v-card :color="overallConclusion.color === 'error' ? 'red-lighten-5' : 'green-lighten-5'" class="mb-4">
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon :color="overallConclusion.color" size="48" class="mr-4">
                {{ overallConclusion.color === 'error' ? 'mdi-alert-circle' : 'mdi-check-circle' }}
              </v-icon>
              <div>
                <div class="text-h5">{{ overallConclusion.result }}</div>
                <div class="text-body-1 text-grey">置信度: {{ overallConclusion.confidence }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 统计信息 -->
    <v-row>
      <v-col cols="12" md="3">
        <v-card class="text-center">
          <v-card-text>
            <div class="text-h4 primary--text">{{ statistics.total }}</div>
            <div class="text-body-2 text-grey">总段落数</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card class="text-center" color="red-lighten-5">
          <v-card-text>
            <div class="text-h4 error--text">{{ statistics.highProb }}</div>
            <div class="text-body-2 text-grey">高风险段落</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card class="text-center" color="orange-lighten-5">
          <v-card-text>
            <div class="text-h4 warning--text">{{ statistics.mediumProb }}</div>
            <div class="text-body-2 text-grey">中风险段落</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card class="text-center" color="green-lighten-5">
          <v-card-text>
            <div class="text-h4 success--text">{{ statistics.lowProb }}</div>
            <div class="text-body-2 text-grey">低风险段落</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 主要内容区域 -->
    <v-row>
      <!-- 左侧：段落展示 -->
      <v-col cols="12" md="8">
        <v-card class="mb-4">
          <v-card-title>
            <span class="text-h6">段落AI生成分析</span>
            <v-spacer></v-spacer>
            <v-chip size="small" color="info">
              <v-icon start>mdi-information</v-icon>
              点击段落查看详情
            </v-chip>
          </v-card-title>
          <v-card-text>
            <div class="paragraph-container">
              <div 
                v-for="(para, index) in data.ai_generated_paragraphs"
                :key="index"
                class="paragraph-item"
                :class="getProbabilityClass(para.ai_probability)"
                @click="showParagraphDetail(para)"
              >
                <div class="paragraph-header">
                  <div class="paragraph-number">
                    <v-chip :color="getProbabilityColor(para.ai_probability)" size="small" label>
                      段落 {{ para.paragraph_index }}
                    </v-chip>
                  </div>
                  <div class="paragraph-probability">
                    <v-chip 
                      :color="getProbabilityColor(para.ai_probability)"
                      size="small"
                      variant="outlined"
                    >
                      <v-icon start size="small">mdi-brain</v-icon>
                      AI概率: {{ (para.ai_probability * 100).toFixed(1) }}%
                    </v-chip>
                  </div>
                </div>
                <div class="paragraph-text">{{ para.text }}</div>
              </div>
            </div>
          </v-card-text>
        </v-card>

        <!-- 事实性鉴伪分析 -->
        <v-card class="mb-4" color="orange-lighten-5">
          <v-card-title>
            <v-icon start color="warning">mdi-alert-circle</v-icon>
            <span class="text-h6">事实性鉴伪分析</span>
          </v-card-title>
          <v-card-text>
            <div class="text-body-1">{{ data.factual_fake_reason }}</div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- 右侧：风险分布和详细信息 -->
      <v-col cols="12" md="4">
        <!-- 风险分布图表 -->
        <v-card class="mb-4">
          <v-card-title>
            <span class="text-h6">风险分布</span>
          </v-card-title>
          <v-card-text>
            <v-progress-linear
              :model-value="(statistics.highProb / statistics.total) * 100"
              color="error"
              height="25"
              class="mb-2"
            >
              <template #default="{ value }">
                <strong>高风险: {{ statistics.highProb }} ({{ value.toFixed(0) }}%)</strong>
              </template>
            </v-progress-linear>
            
            <v-progress-linear
              :model-value="(statistics.mediumProb / statistics.total) * 100"
              color="warning"
              height="25"
              class="mb-2"
            >
              <template #default="{ value }">
                <strong>中风险: {{ statistics.mediumProb }} ({{ value.toFixed(0) }}%)</strong>
              </template>
            </v-progress-linear>
            
            <v-progress-linear
              :model-value="(statistics.lowProb / statistics.total) * 100"
              color="success"
              height="25"
            >
              <template #default="{ value }">
                <strong>低风险: {{ statistics.lowProb }} ({{ value.toFixed(0) }}%)</strong>
              </template>
            </v-progress-linear>
          </v-card-text>
        </v-card>

        <!-- 段落风险排名 -->
        <v-card>
          <v-card-title>
            <span class="text-h6">高风险段落TOP5</span>
          </v-card-title>
          <v-card-text>
            <v-list density="compact">
              <v-list-item
                v-for="(para, index) in [...data.ai_generated_paragraphs]
                  .sort((a, b) => b.ai_probability - a.ai_probability)
                  .slice(0, 5)"
                :key="index"
                @click="showParagraphDetail(para)"
                class="method-item"
              >
                <template #prepend>
                  <v-icon :color="getProbabilityColor(para.ai_probability)">
                    mdi-format-paint
                  </v-icon>
                </template>
                <v-list-item-title>
                  段落 {{ para.paragraph_index }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ (para.ai_probability * 100).toFixed(1) }}% - {{ getProbabilityLevel(para.ai_probability) }}
                </v-list-item-subtitle>
                <template #append>
                  <v-chip
                    :color="getProbabilityColor(para.ai_probability)"
                    size="small"
                  >
                    {{ (para.ai_probability * 100).toFixed(1) }}%
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 段落详情弹窗 -->
    <v-dialog v-model="showDetailDialog" max-width="800">
      <v-card v-if="selectedParagraph">
        <v-card-title class="d-flex align-center">
          <v-icon :color="getProbabilityColor(selectedParagraph.ai_probability)" class="mr-2">
            {{ getProbabilityColor(selectedParagraph.ai_probability) === 'error' ? 'mdi-alert-circle' : 'mdi-information' }}
          </v-icon>
          段落 {{ selectedParagraph.paragraph_index }} 详情
        </v-card-title>
        
        <v-card-text>
          <!-- AI概率显示 -->
          <div class="mb-4">
            <v-chip :color="getProbabilityColor(selectedParagraph.ai_probability)" size="large">
              <v-icon start>mdi-brain</v-icon>
              AI生成概率: {{ (selectedParagraph.ai_probability * 100).toFixed(1) }}%
            </v-chip>
            <v-chip 
              :color="getProbabilityColor(selectedParagraph.ai_probability)" 
              size="large" 
              class="ml-2"
            >
              {{ getProbabilityLevel(selectedParagraph.ai_probability) }}
            </v-chip>
          </div>

          <!-- 段落文本 -->
          <div class="mb-4">
            <h3 class="text-h6 mb-2">段落内容</h3>
            <div class="paragraph-detail-text">{{ selectedParagraph.text }}</div>
          </div>

          <!-- AI判断原因 -->
          <div class="mb-4">
            <h3 class="text-h6 mb-2">AI判断原因</h3>
            <v-alert :color="getProbabilityColor(selectedParagraph.ai_probability)" variant="tonal">
              {{ selectedParagraph.reason }}
            </v-alert>
          </div>

          <!-- 概率可视化 -->
          <div>
            <h3 class="text-h6 mb-2">AI生成概率可视化</h3>
            <v-progress-linear
              :model-value="selectedParagraph.ai_probability * 100"
              :color="getProbabilityColor(selectedParagraph.ai_probability)"
              height="30"
            >
              <template #default="{ value }">
                <strong>{{ value.toFixed(1) }}%</strong>
              </template>
            </v-progress-linear>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="showDetailDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<style scoped>
.paragraph-container {
  max-height: 800px;
  overflow-y: auto;
}

.paragraph-item {
  padding: 16px;
  margin-bottom: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
}

.paragraph-item:hover {
  transform: translateX(4px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.high-probability {
  background-color: rgba(255, 0, 0, 0.05);
  border-left: 4px solid #f44336;
}

.medium-probability {
  background-color: rgba(255, 165, 0, 0.05);
  border-left: 4px solid #ff9800;
}

.low-probability {
  background-color: rgba(0, 128, 0, 0.05);
  border-left: 4px solid #4caf50;
}

.paragraph-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.paragraph-number {
  font-weight: bold;
}

.paragraph-probability {
  font-size: 14px;
}

.paragraph-text {
  line-height: 1.8;
  color: #333;
  text-align: justify;
}

.paragraph-detail-text {
  line-height: 1.8;
  color: #333;
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 8px;
  max-height: 300px;
  overflow-y: auto;
}

.method-item {
  cursor: pointer;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.method-item:hover {
  background-color: #f5f5f5;
}
</style>
