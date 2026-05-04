<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { sampleImageData, type ImageDetectionData, type SubMethod } from './mocks/sampleData'

interface Props {
  task_id?: string
  task_type?: string
}

const props = defineProps<Props>()

// 使用样例数据
const data = ref<ImageDetectionData>(sampleImageData)

// Canvas引用
const mainCanvas = ref<HTMLCanvasElement>()
const maskCanvas = ref<HTMLCanvasElement>()

// 当前选中的子方法
const selectedMethod = ref<SubMethod | null>(data.value.sub_methods[0])

// AI贡献度
const aiContribution = computed(() => ({
  llm: 35,
  deep_learning: 45,
  traditional: 20
}))

// 综合结论
const overallConclusion = computed(() => {
  if (data.value.overall.is_fake) {
    return {
      result: '判定为伪造图片',
      confidence: (data.value.overall.confidence_score * 100).toFixed(1) + '%',
      color: 'error'
    }
  } else {
    return {
      result: '判定为真实图片',
      confidence: ((1 - data.value.overall.confidence_score) * 100).toFixed(1) + '%',
      color: 'success'
    }
  }
})

// 在挂载时绘制
onMounted(() => {
  nextTick(() => {
    drawMainImage()
    drawMask()
  })
})

// 绘制主图
function drawMainImage() {
  if (!mainCanvas.value) return
  
  const canvas = mainCanvas.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  // 设置canvas大小
  canvas.width = 512
  canvas.height = 512

  // 加载并绘制图片
  const img = new Image()
  img.crossOrigin = 'anonymous'
  img.onload = () => {
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
  }
  img.src = data.value.image
}

// 绘制mask
function drawMask() {
  if (!maskCanvas.value || !selectedMethod.value) return
  
  const canvas = maskCanvas.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  // 设置canvas大小
  canvas.width = 512
  canvas.height = 512

  // 绘制mask矩阵
  const matrix = selectedMethod.value.mask_matrix
  const maskImage = ctx.createImageData(512, 512)
  
  for (let y = 0; y < 512; y++) {
    for (let x = 0; x < 512; x++) {
      // 矩阵是256x256，需要放大到512x512
      const sourceY = Math.floor(y / 2)
      const sourceX = Math.floor(x / 2)
      const value = matrix[sourceY][sourceX]
      
      const index = (y * 512 + x) * 4
      
      // 使用红色透明度表示概率
      maskImage.data[index] = 255     // R
      maskImage.data[index + 1] = 0   // G
      maskImage.data[index + 2] = 0   // B
      maskImage.data[index + 3] = value * 255 // A
    }
  }
  
  ctx.putImageData(maskImage, 0, 0)
}

// 选择子方法
function selectMethod(method: SubMethod) {
  selectedMethod.value = method
  nextTick(() => {
    drawMask()
  })
}

// 获取概率颜色
function getProbabilityColor(probability: number): string {
  if (probability > 0.8) return 'error'
  if (probability > 0.6) return 'warning'
  return 'success'
}

// 获取概率等级
function getProbabilityLevel(probability: number): string {
  if (probability > 0.8) return '高概率'
  if (probability > 0.6) return '中概率'
  return '低概率'
}
</script>

<template>
  <v-container fluid class="pa-4">
    <!-- 标题栏 -->
    <v-row>
      <v-col cols="12">
        <h2 class="text-h4 mb-2">图片检测结果审核</h2>
        <p class="text-body-1 text-grey">
          检测ID: {{ data.result_id }} | 检测时间: {{ data.timestamps }}
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
      <!-- 左侧：图片展示 -->
      <v-col cols="12" md="8">
        <v-card class="mb-4">
          <v-card-title>
            <span class="text-h6">可疑区域可视化</span>
          </v-card-title>
          <v-card-text>
            <v-row>
              <!-- 原图 -->
              <v-col cols="12" sm="6">
                <div class="image-container">
                  <div class="image-label">原图</div>
                  <canvas ref="mainCanvas" class="detection-canvas"></canvas>
                </div>
              </v-col>
              <!-- Mask叠加 -->
              <v-col cols="12" sm="6">
                <div class="image-container">
                  <div class="image-label">可疑区域叠加 ({{ selectedMethod?.method }})</div>
                  <canvas ref="maskCanvas" class="detection-canvas"></canvas>
                </div>
              </v-col>
            </v-row>
            
            <!-- 选中方法的详细信息 -->
            <v-alert v-if="selectedMethod" class="mt-4" :color="getProbabilityColor(selectedMethod.probability)">
              <template #prepend>
                <v-icon>{{ getProbabilityColor(selectedMethod.probability) === 'error' ? 'mdi-alert' : 'mdi-information' }}</v-icon>
              </template>
              <div class="text-body-1">
                <strong>{{ selectedMethod.method }}:</strong> 
                检测概率 {{ (selectedMethod.probability * 100).toFixed(1) }}% 
                ({{ getProbabilityLevel(selectedMethod.probability) }})
              </div>
            </v-alert>
          </v-card-text>
        </v-card>

        <!-- 大模型分析 -->
        <v-card class="mb-4">
          <v-card-title>
            <span class="text-h6">大语言模型分析</span>
          </v-card-title>
          <v-card-text>
            <div class="text-body-1">{{ data.llm }}</div>
            <div class="mt-4">
              <v-img 
                :src="data.llm_image" 
                max-width="200" 
                class="ma-auto"
                alt="LLM分析结果"
              ></v-img>
            </div>
          </v-card-text>
        </v-card>

        <!-- EXIF信息 -->
        <v-card>
          <v-card-title>
            <span class="text-h6">EXIF元数据分析</span>
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="6">
                <v-chip 
                  :color="data.exif.photoshop_edited ? 'error' : 'success'"
                  class="ma-1"
                >
                  <v-icon start>mdi-image-edit</v-icon>
                  {{ data.exif.photoshop_edited ? '检测到Photoshop编辑' : '未检测到Photoshop编辑' }}
                </v-chip>
              </v-col>
              <v-col cols="6">
                <v-chip 
                  :color="data.exif.time_modified ? 'warning' : 'success'"
                  class="ma-1"
                >
                  <v-icon start>mdi-clock-edit</v-icon>
                  {{ data.exif.time_modified ? '时间被修改' : '时间未修改' }}
                </v-chip>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- 右侧：方法对比和AI贡献度 -->
      <v-col cols="12" md="4">
        <!-- AI贡献度分析 -->
        <v-card class="mb-4">
          <v-card-title>
            <span class="text-h6">AI贡献度分析</span>
          </v-card-title>
          <v-card-text>
            <div class="contribution-chart">
              <v-progress-linear
                :model-value="aiContribution.llm"
                color="purple"
                height="30"
                class="mb-2"
              >
                <template #default="{ value }">
                  <strong>{{ value }}%</strong> 大语言模型
                </template>
              </v-progress-linear>
              
              <v-progress-linear
                :model-value="aiContribution.deep_learning"
                color="blue"
                height="30"
                class="mb-2"
              >
                <template #default="{ value }">
                  <strong>{{ value }}%</strong> 深度学习
                </template>
              </v-progress-linear>
              
              <v-progress-linear
                :model-value="aiContribution.traditional"
                color="green"
                height="30"
              >
                <template #default="{ value }">
                  <strong>{{ value }}%</strong> 传统方法
                </template>
              </v-progress-linear>
            </div>
          </v-card-text>
        </v-card>

        <!-- 7种子方法对比 -->
        <v-card>
          <v-card-title>
            <span class="text-h6">检测方法对比</span>
          </v-card-title>
          <v-card-text>
            <v-list density="compact">
              <v-list-item
                v-for="method in data.sub_methods"
                :key="method.method"
                :class="{ 'selected-method': selectedMethod?.method === method.method }"
                @click="selectMethod(method)"
                class="method-item"
              >
                <template #prepend>
                  <v-icon :color="getProbabilityColor(method.probability)">
                    {{ getProbabilityColor(method.probability) === 'error' ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                  </v-icon>
                </template>
                <v-list-item-title>
                  <strong>{{ method.method }}</strong>
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ (method.probability * 100).toFixed(1) }}% - {{ getProbabilityLevel(method.probability) }}
                </v-list-item-subtitle>
                <template #append>
                  <v-chip
                    :color="getProbabilityColor(method.probability)"
                    size="small"
                  >
                    {{ (method.probability * 100).toFixed(1) }}%
                  </v-chip>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.detection-canvas {
  width: 100%;
  height: auto;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
}

.image-container {
  text-align: center;
}

.image-label {
  margin-bottom: 8px;
  font-weight: bold;
  color: #666;
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

.method-item.selected-method {
  background-color: #e3f2fd;
  border-left: 4px solid #2196f3;
}

.contribution-chart {
  padding: 8px;
}
</style>