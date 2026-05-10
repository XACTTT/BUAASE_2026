<script setup lang="ts">
import { computed } from 'vue'
import { sampleReviewData, sampleReviewDataTemplate, type ReviewTextDetectionData } from './mocks/sampleData'

interface Props {
  task_id?: string
  task_type?: string
}

const props = defineProps<Props>()

// 使用样例数据（可以切换到sampleReviewDataTemplate查看模板化倾向高的案例）
const data = ref<ReviewTextDetectionData>(sampleReviewData)

// 综合结论
const overallConclusion = computed(() => {
  if (data.value.is_fake) {
    return {
      result: '判定为模板化Review',
      confidence: (data.value.confidence_score * 100).toFixed(1) + '%',
      color: 'error'
    }
  } else {
    return {
      result: '判定为原创Review',
      confidence: ((1 - data.value.confidence_score) * 100).toFixed(1) + '%',
      color: 'success'
    }
  }
})

// 模板化倾向等级
const templateLevel = computed(() => {
  const score = data.value.template_tendency_score
  if (score > 0.7) {
    return { level: '高度模板化', color: 'error', icon: 'mdi-alert-octagon' }
  } else if (score > 0.4) {
    return { level: '中度模板化', color: 'warning', icon: 'mdi-alert' }
  } else {
    return { level: '低度模板化', color: 'success', icon: 'mdi-check-circle' }
  }
})

// 获取建议
const getSuggestion = () => {
  if (data.value.template_tendency_score > 0.7) {
    return '建议：该评审意见模板化倾向严重，建议审稿人重新审视并提供更具针对性的专业意见。'
  } else if (data.value.template_tendency_score > 0.4) {
    return '建议：该评审意见存在一定模板化痕迹，建议审稿人结合论文具体内容补充更多细节分析。'
  } else {
    return '建议：该评审意见个性化程度较高，展现了独立的学术判断，质量较好。'
  }
}
</script>

<template>
  <v-container fluid class="pa-4">
    <!-- 标题栏 -->
    <v-row>
      <v-col cols="12">
        <h2 class="text-h4 mb-2">Review文本检测结果审核</h2>
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

    <!-- 主要内容区域 -->
    <v-row>
      <!-- 左侧：模板化倾向分析 -->
      <v-col cols="12" md="8">
        <!-- 模板化倾向评分 -->
        <v-card class="mb-4">
          <v-card-title>
            <v-icon :color="templateLevel.color" class="mr-2">
              {{ templateLevel.icon }}
            </v-icon>
            <span class="text-h6">模板化倾向分析</span>
          </v-card-title>
          <v-card-text>
            <!-- 仪表盘样式 -->
            <div class="d-flex flex-column align-center mb-6">
              <v-progress-circular
                :model-value="data.template_tendency_score * 100"
                :size="250"
                :width="25"
                :color="templateLevel.color"
                class="mb-4"
              >
                <div class="text-center">
                  <div class="text-h2">{{ (data.template_tendency_score * 100).toFixed(0) }}%</div>
                  <div class="text-h6">{{ templateLevel.level }}</div>
                </div>
              </v-progress-circular>
              
              <v-chip :color="templateLevel.color" size="large">
                <v-icon start>mdi-gauge</v-icon>
                模板化倾向评分: {{ (data.template_tendency_score * 100).toFixed(1) }}%
              </v-chip>
            </div>

            <!-- 评分说明 -->
            <v-alert :color="templateLevel.color" variant="tonal" class="mb-4">
              <template #prepend>
                <v-icon>mdi-information</v-icon>
              </template>
              <div class="text-body-1">
                <strong>评分说明：</strong>
                <ul class="mt-2">
                  <li>0-40%：低度模板化，Review个性化程度高，建议保持</li>
                  <li>40-70%：中度模板化，Review存在一定模板化痕迹，建议改进</li>
                  <li>70-100%：高度模板化，Review模板化严重，需要重新撰写</li>
                </ul>
              </div>
            </v-alert>

            <!-- 建议 -->
            <v-alert color="info" variant="tonal">
              <template #prepend>
                <v-icon>mdi-lightbulb</v-icon>
              </template>
              <div class="text-body-1">
                <strong>改进建议：</strong>
                {{ getSuggestion() }}
              </div>
            </v-alert>
          </v-card-text>
        </v-card>

        <!-- 模板化分析原因 -->
        <v-card>
          <v-card-title>
            <v-icon start color="primary">mdi-text-box-search</v-icon>
            <span class="text-h6">模板化分析原因</span>
          </v-card-title>
          <v-card-text>
            <div class="text-body-1 analysis-text">
              {{ data.template_analysis_reason }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- 右侧：详细指标和建议 -->
      <v-col cols="12" md="4">
        <!-- 评分分布 -->
        <v-card class="mb-4">
          <v-card-title>
            <span class="text-h6">评分等级分布</span>
          </v-card-title>
          <v-card-text>
            <div class="score-distribution">
              <div class="score-item">
                <div class="score-label">低度模板化 (0-40%)</div>
                <v-progress-linear
                  :model-value="data.template_tendency_score <= 0.4 ? 100 : 0"
                  color="success"
                  height="20"
                >
                  <template #default="{ value }">
                    <span v-if="value > 0">{{ templateLevel.level === '低度模板化' ? '当前状态' : '0%' }}</span>
                  </template>
                </v-progress-linear>
              </div>
              
              <div class="score-item">
                <div class="score-label">中度模板化 (40-70%)</div>
                <v-progress-linear
                  :model-value="data.template_tendency_score > 0.4 && data.template_tendency_score <= 0.7 ? 100 : 0"
                  color="warning"
                  height="20"
                >
                  <template #default="{ value }">
                    <span v-if="value > 0">{{ templateLevel.level === '中度模板化' ? '当前状态' : '0%' }}</span>
                  </template>
                </v-progress-linear>
              </div>
              
              <div class="score-item">
                <div class="score-label">高度模板化 (70-100%)</div>
                <v-progress-linear
                  :model-value="data.template_tendency_score > 0.7 ? 100 : 0"
                  color="error"
                  height="20"
                >
                  <template #default="{ value }">
                    <span v-if="value > 0">{{ templateLevel.level === '高度模板化' ? '当前状态' : '0%' }}</span>
                  </template>
                </v-progress-linear>
              </div>
            </div>
          </v-card-text>
        </v-card>

        <!-- 质量评估指标 -->
        <v-card class="mb-4">
          <v-card-title>
            <span class="text-h6">质量评估指标</span>
          </v-card-title>
          <v-card-text>
            <v-list density="compact">
              <v-list-item>
                <template #prepend>
                  <v-icon color="primary">mdi-star</v-icon>
                </template>
                <v-list-item-title>个性化程度</v-list-item-title>
                <v-list-item-subtitle>
                  {{ ((1 - data.template_tendency_score) * 100).toFixed(1) }}%
                </v-list-item-subtitle>
                <template #append>
                  <v-chip :color="(1 - data.template_tendency_score) > 0.5 ? 'success' : 'warning'" size="small">
                    {{ ((1 - data.template_tendency_score) * 100).toFixed(1) }}%
                  </v-chip>
                </template>
              </v-list-item>

              <v-list-item>
                <template #prepend>
                  <v-icon color="primary">mdi-pencil</v-icon>
                </template>
                <v-list-item-title>专业深度</v-list-item-title>
                <v-list-item-subtitle>
                  基于{{ (data.template_tendency_score < 0.5 ? '高' : '中低') }}模板化倾向评估
                </v-list-item-subtitle>
                <template #append>
                  <v-chip :color="data.template_tendency_score < 0.5 ? 'success' : 'warning'" size="small">
                    {{ data.template_tendency_score < 0.5 ? '优秀' : '一般' }}
                  </v-chip>
                </template>
              </v-list-item>

              <v-list-item>
                <template #prepend>
                  <v-icon color="primary">mdi-text-box</v-icon>
                </template>
                <v-list-item-title>内容质量</v-list-item-title>
                <v-list-item-subtitle>
                  {{ data.template_tendency_score < 0.4 ? '高质量原创内容' : '存在模板化内容' }}
                </v-list-item-subtitle>
                <template #append>
                  <v-chip :color="data.template_tendency_score < 0.4 ? 'success' : 'warning'" size="small">
                    {{ data.template_tendency_score < 0.4 ? '优秀' : '一般' }}
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>

        <!-- 快速操作 -->
        <v-card>
          <v-card-title>
            <span class="text-h6">快速操作</span>
          </v-card-title>
          <v-card-text>
            <v-btn 
              block 
              color="primary" 
              variant="outlined" 
              class="mb-2"
              @click="data = sampleReviewData"
            >
              <v-icon start>mdi-refresh</v-icon>
              加载低模板化样例
            </v-btn>
            
            <v-btn 
              block 
              color="warning" 
              variant="outlined"
              @click="data = sampleReviewDataTemplate"
            >
              <v-icon start>mdi-alert-circle</v-icon>
              加载高模板化样例
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.analysis-text {
  line-height: 1.8;
  color: #333;
  text-align: justify;
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.score-distribution {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.score-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.score-label {
  font-size: 14px;
  font-weight: 500;
  color: #666;
}
</style>