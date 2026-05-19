<template>
  <v-card class="chart-card" elevation="3">
    <v-card-title class="text-h6 font-weight-medium primary--text d-flex align-center">
      <v-icon color="primary" class="mr-2">mdi-history</v-icon>
      操作日志统计
      <v-spacer></v-spacer>
      <v-chip v-if="anomalyCount > 0" color="error" size="small" variant="flat" class="mr-2">
        最近异常: {{ anomalyCount }}
      </v-chip>
      <v-select
        v-model="days"
        :items="[7, 30, 90]"
        density="compact"
        variant="outlined"
        hide-details
        suffix="天"
        style="max-width: 100px"
        @update:model-value="fetchData"
      ></v-select>
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="12" md="8">
          <div ref="lineChartRef" class="chart-container"></div>
        </v-col>
        <v-col cols="12" md="4">
          <div ref="pieChartRef" class="chart-container"></div>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import logApi from '@/api/log'
import { useSnackbarStore } from '@/stores/snackbar'
import { useThemeStore } from '@/stores/theme'

const lineChartRef = ref<HTMLElement | null>(null)
const pieChartRef = ref<HTMLElement | null>(null)
let lineChartInstance: echarts.ECharts | null = null
let pieChartInstance: echarts.ECharts | null = null

const days = ref(30)
const anomalyCount = ref(0)
const snackbar = useSnackbarStore()
const themeStore = useThemeStore()

const fetchData = async () => {
  try {
    const res = await logApi.getLogStatistics({ days: days.value })
    const data = res.data
    anomalyCount.value = data.anomaly_count
    renderCharts(data)
  } catch (error) {
    console.error('获取日志统计失败:', error)
    snackbar.showMessage('获取日志统计失败')
  }
}

const renderCharts = (data: any) => {
  renderLineChart(data.daily_stats)
  renderPieChart(data.type_stats)
}

const renderLineChart = (dailyStats: any[]) => {
  if (!lineChartRef.value) return
  if (lineChartInstance) lineChartInstance.dispose()
  lineChartInstance = echarts.init(lineChartRef.value)

  const isDark = themeStore.theme === 'dark'
  const textColor = isDark ? '#fff' : '#333'
  
  const option: echarts.EChartsOption = {
    title: { text: '每日操作趋势', left: 'center', textStyle: { color: textColor, fontSize: 14 } },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: dailyStats.map(i => i.date),
      axisLabel: { color: textColor }
    },
    yAxis: { type: 'value', axisLabel: { color: textColor } },
    series: [{
      data: dailyStats.map(i => i.count),
      type: 'line',
      smooth: true,
      areaStyle: { opacity: 0.3 },
      itemStyle: { color: '#42A5F5' }
    }]
  }
  lineChartInstance.setOption(option)
}

const renderPieChart = (typeStats: any[]) => {
  if (!pieChartRef.value) return
  if (pieChartInstance) pieChartInstance.dispose()
  pieChartInstance = echarts.init(pieChartRef.value)

  const isDark = themeStore.theme === 'dark'
  const textColor = isDark ? '#fff' : '#333'
  
  const typeMap: Record<string, string> = {
    login: '用户登录',
    logout: '用户登出',
    upload: '上传文件',
    ai_detect: 'AI检测',
    paper_detect: '论文文本检测',
    review_detect: '评审文本检测',
    audit_submit: '发起审核',
    audit_op: '执行审核',
    entity_create: '实体创建',
    entity_delete: '实体删除',
    entity_update: '实体更新',
    mark_anomaly: '异常标记'
  }

  const option: echarts.EChartsOption = {
    title: { text: '操作类型占比', left: 'center', textStyle: { color: textColor, fontSize: 14 } },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: typeStats.map(i => ({ name: typeMap[i.operation_type] || i.operation_type, value: i.count })),
      emphasis: {
        itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0, 0, 0, 0.5)' }
      }
    }]
  }
  pieChartInstance.setOption(option)
}

const handleResize = () => {
  lineChartInstance?.resize()
  pieChartInstance?.resize()
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  lineChartInstance?.dispose()
  pieChartInstance?.dispose()
  window.removeEventListener('resize', handleResize)
})

watch(() => themeStore.theme, fetchData)
</script>

<style scoped>
.chart-card { border-radius: 12px; margin-bottom: 24px; }
.chart-container { width: 100%; height: 350px; }
</style>