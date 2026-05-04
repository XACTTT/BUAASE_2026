<template>
  <v-card flat border="0">
    <v-card-text class="pa-0 mt-4">
      <!-- 根据任务类型动态渲染不同的审核组件 -->
      <ImageDetectionReview 
        v-if="taskType === 'image' && useSample" 
        :task_id="taskId"
        :task_type="taskType"
      />
      <PaperTextDetectionReview 
        v-else-if="taskType === 'paper_text' && useSample" 
        :task_id="taskId"
        :task_type="taskType"
      />
      <ReviewTextDetectionReview 
        v-else-if="taskType === 'review_text' && useSample" 
        :task_id="taskId"
        :task_type="taskType"
      />
      <!-- 使用现有的年度审核步骤组件 -->
      <DetectionReviewStep 
        v-else 
        :task_id="taskId"
      />
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
//注意鉴权！！！
import { computed, onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import type { RouteParams } from 'vue-router'
import DetectionReviewStep from '@/components/steps/DetectionReviewStep.vue'
import ImageDetectionReview from '@/components/reviews/ImageDetectionReview.vue'
import PaperTextDetectionReview from '@/components/reviews/PaperTextDetectionReview.vue'
import ReviewTextDetectionReview from '@/components/reviews/ReviewTextDetectionReview.vue'
import { useSnackbarStore } from '@/stores/snackbar';
import publisher from '@/api/publisher'

const snackbar = useSnackbarStore();

const router = useRouter()
const route = useRoute()

// 获取任务ID
const taskId = computed(() => (route.params as RouteParams & { id: string }).id)

// 任务类型（从查询参数获取）
const taskType = computed(() => {
  return (route.query.type as string) || 'image'
})

// 是否使用样例数据（用于演示）
const useSample = ref(true)

// 组件挂载时获取任务数据
onMounted(async () => {
  // 使用样例数据时跳过权限检查
  if (useSample.value) {
    console.log('使用样例数据，跳过权限检查')
    return
  }
  
  // 真实数据才检查权限
  try {
    const response = (await publisher.ifHasPermission({task_id: taskId.value})).data.access
    if(response !== true){
      router.push('/404')
    }
  } catch (error) {
    console.error('权限检查失败:', error)
    snackbar.showMessage('权限检查失败', 'error')
    router.push('/404')
  }
})
</script>

<style scoped>
.v-card {
  box-shadow: none;
}
</style>
