<template>
  <div class="task-detail pa-4">
    <!-- Back button -->
    <div class="d-flex align-center mb-6">
      <v-btn icon="mdi-arrow-left" variant="text" @click="router.back()" class="mr-2 return-btn">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <span class="text-h6 font-weight-medium">返回检测历史</span>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="d-flex align-center justify-center" style="height: calc(100vh - 80px)">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </div>

    <div v-else class="main-content rounded-lg">
      <!-- Top info section (shared across all modes) -->
      <div class="info-section pa-6">
        <div class="content-wrapper d-flex justify-center">
          <div class="content-container">
            <div class="info-content d-flex align-center justify-space-between pa-4">
              <!-- Left: progress circle + download + AI detection card -->
              <div class="d-flex align-center" style="min-width: 320px">
                <div class="progress-circle mr-3 elevation-1">
                  <span class="text-h5 font-weight-bold primary--text">{{ formatNumber(AI_detection) }}</span>
                  <span class="text-caption">为假</span>
                </div>
                <v-btn color="primary" variant="elevated" prepend-icon="mdi-download" @click="handleDownloadReport"
                  class="ml-4">
                  下载人工审核报告
                </v-btn>
                <v-card class="ml-4 pa-2 elevation-1" flat rounded="lg" width="250">
                  <v-card-title class="pa-2 pb-1 text-subtitle-2 font-weight-bold">AI 检测结果</v-card-title>
                  <v-card-text class="pa-2 pt-1">
                    <template v-if="isMultiMaterial">
                      <div class="d-flex flex-column text-body-2 text-grey">
                        <div class="d-flex justify-space-between mb-1">
                          <span class="font-weight-medium">任务类型:</span>
                          <span class="text-primary">综合检测</span>
                        </div>
                        <div class="d-flex justify-space-between mb-1">
                          <span class="font-weight-medium">图片数量:</span>
                          <span class="text-primary">{{ images.length }} 张</span>
                        </div>
                        <div class="d-flex justify-space-between">
                          <span class="font-weight-medium">文本数量:</span>
                          <span class="text-primary">{{ textResults.length }} 份</span>
                        </div>
                      </div>
                    </template>
                    <template v-else-if="!isTextTask">
                      <div v-for="(dimension, index) in detection_results" :key="index"
                        class="d-flex justify-space-between text-body-2 text-grey">
                        <span class="font-weight-medium">{{ convert(index) }}:</span>
                        <span class="text-primary">{{ (dimension.probability ?? 0).toFixed(2) }}</span>
                      </div>
                    </template>
                    <template v-else>
                      <div class="d-flex flex-column text-body-2 text-grey">
                        <div class="d-flex justify-space-between mb-1">
                          <span class="font-weight-medium">当前任务类型:</span>
                          <span class="text-primary">{{ taskType === 'paper_text' ? '论文检测' : 'Review检测' }}</span>
                        </div>
                        <div class="d-flex justify-space-between">
                          <span class="font-weight-medium">包含文本数量:</span>
                          <span class="text-primary">{{ textResults.length }} 份</span>
                        </div>
                      </div>
                    </template>
                  </v-card-text>
                </v-card>
              </div>

              <!-- Right: task stats -->
              <div class="task-stats d-flex align-center">
                <div class="stat-item mr-4">
                  <div class="text-subtitle-1 d-flex justify-center">
                    <v-chip variant="flat" size="x-large" class="unprocessed-chip font-weight-medium px-3"
                      style="min-width: 80px">
                      未处理
                    </v-chip>
                  </div>
                  <div class="text-h6 font-weight-bold">{{ process }}份</div>
                </div>
                <div class="stat-item">
                  <div class="text-subtitle-1 d-flex justify-center">
                    <v-chip variant="flat" size="x-large" class="sent-chip font-weight-medium px-3"
                      style="min-width: 80px">
                      已发送
                    </v-chip>
                  </div>
                  <div class="text-h6 font-weight-bold">{{ done }}份</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <v-divider></v-divider>

      <!-- ==================== IMAGE MODE ==================== -->
      <template v-if="taskType === 'image'">
        <div class="content-wrapper d-flex pa-2 justify-center">
          <div class="content-container d-flex" style="gap: 12px;">
            <!-- Left: image thumbnails -->
            <div class="resource-list rounded-lg elevation-1"
              style="background-color: rgb(var(--v-theme-surface)); padding: 20px;">
              <div class="text-h6 font-weight-medium text-center mb-4" style="white-space: nowrap;">图片列表</div>
              <div class="resource-grid">
                <div v-for="(image, index) in images" :key="index" class="resource-grid-item"
                  :class="{ 'active': currentImageIndex === index }" @click="handleImageSelect(index)">
                  <v-img :src="getImageUrl(image.img_url)" cover width="100%" height="100%" class="rounded-lg"></v-img>
                </div>
              </div>
            </div>

            <!-- Center: image preview with prev/next -->
            <div class="preview-section">
              <div class="preview-box">
                <v-img v-if="currentImage" :src="getImageUrl(currentImage.img_url)" contain height="100%"
                  class="rounded-lg"></v-img>
                <span v-else class="text-h4">PIC</span>
                <div class="preview-controls">
                  <v-btn icon="mdi-chevron-left" variant="flat" @click="handlePrevImage"
                    :disabled="currentImageIndex <= 0" class="control-btn" color="black" size="x-large"></v-btn>
                  <v-btn icon="mdi-chevron-right" variant="flat" @click="handleNextImage"
                    :disabled="currentImageIndex >= images.length - 1" class="control-btn" color="black"
                    size="x-large"></v-btn>
                </div>
              </div>
            </div>

            <!-- Right: reviewer list -->
            <div class="review-section rounded-lg elevation-1 pa-4">
              <div class="review-header">
                <div class="text-h6 font-weight-medium text-center mb-4">人工审核</div>
                <div class="reviewer-info mt-4">
                  <template v-if="review_results.length > 0">
                    <div v-for="(review, index) in review_results" :key="index"
                      class="reviewer-item d-flex align-center pa-3 mb-4 rounded" style="min-height: 64px;">
                      <v-avatar size="40" class="mr-3" color="primary">
                        <v-img v-if="review.avatar" :src="getImageUrl(review.avatar)" cover></v-img>
                        <span v-else class="text-h6">{{ review.username.charAt(0) }}</span>
                      </v-avatar>
                      <div class="flex-grow-1">
                        <div class="text-body-1 font-weight-medium">{{ review.username }}</div>
                        <div class="text-caption text-grey mt-1">结果：{{ getResult(review.result) }}</div>
                      </div>
                      <v-btn variant="text" density="comfortable" class="details-btn" color="primary"
                        @click="handleViewDetail(review)">
                        查看详情
                        <v-icon size="16" class="ml-1">mdi-chevron-right</v-icon>
                      </v-btn>
                    </div>
                  </template>
                  <template v-else>
                    <div class="d-flex flex-column align-center justify-center" style="height: 200px;">
                      <v-icon size="48" color="grey" class="mb-4">mdi-information-outline</v-icon>
                      <div class="text-body-1 text-grey">暂无人工审核结果</div>
                    </div>
                  </template>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- ==================== TEXT MODE ==================== -->
      <template v-else-if="isTextTask">
        <div class="pa-6">
          <v-row>
            <!-- Left col (md=3): text list + text content + AI detection reference -->
            <v-col cols="12" md="3">
              <!-- Text list card -->
              <v-card elevation="2" rounded="lg" class="text-sidebar mb-4">
                <v-card-title class="pa-4">
                  <v-icon class="mr-2">mdi-file-document-multiple</v-icon>
                  文本列表
                  <v-spacer></v-spacer>
                  <v-chip size="small" color="primary">{{ textResults.length }}</v-chip>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-2" style="max-height: calc(50vh - 120px); overflow-y: auto;">
                  <div v-for="(textRes, index) in textResults" :key="textRes.result_id"
                    class="text-sidebar-item pa-3 mb-2 rounded-lg cursor-pointer"
                    :class="{ 'text-sidebar-item-active': currentTextIndex === index }"
                    @click="handleTextSelect(index)">
                    <div class="d-flex align-center mb-1">
                      <v-chip size="x-small" :color="getTextChipColor(textRes)" class="mr-2">
                        {{ getTextChipLabel(textRes) }}
                      </v-chip>
                      <span class="text-caption text-grey">ID: {{ textRes.resource_id }}</span>
                    </div>
                    <div class="text-body-2 text-truncate">
                      {{ getRawTextForTextResult(textRes).substring(0, 60) }}{{ getRawTextForTextResult(textRes).length > 60 ? '...' : '' }}
                    </div>
                  </div>
                </v-card-text>
              </v-card>

              <!-- Text content card -->
              <v-card v-if="currentTextResult" elevation="2" rounded="lg" class="mb-4">
                <v-card-title class="pa-4 d-flex align-center">
                  <v-icon class="mr-2">mdi-text-box</v-icon>
                  文本内容
                  <v-spacer></v-spacer>
                  <v-btn size="small" variant="text" @click="showFullText = !showFullText">
                    {{ showFullText ? '收起' : '展开全文' }}
                  </v-btn>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-4" style="max-height: 200px; overflow-y: auto;">
                  <div class="text-body-2" style="white-space: pre-wrap; line-height: 1.8;">
                    {{ displayText }}
                  </div>
                </v-card-text>
              </v-card>

              <!-- AI detection reference card -->
              <v-card v-if="currentTextResult" elevation="2" rounded="lg">
                <v-card-title class="pa-4">
                  <v-icon class="mr-2" color="primary">mdi-robot</v-icon>
                  AI 检测结果参考
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-4" style="max-height: 300px; overflow-y: auto;">
                  <v-row class="mb-3">
                    <v-col cols="6">
                      <div class="text-body-2 text-grey mb-1">AI判定</div>
                      <v-chip :color="currentTextResult.is_fake ? 'error' : 'success'" size="small">
                        {{ currentTextResult.is_fake ? '疑似造假' : '可能真实' }}
                      </v-chip>
                    </v-col>
                    <v-col cols="6">
                      <div class="text-body-2 text-grey mb-1">置信度</div>
                      <span class="text-h6" :class="currentTextResult.confidence_score > 0.7 ? 'error--text' : 'primary--text'">
                        {{ ((currentTextResult.confidence_score || 0) * 100).toFixed(1) }}%
                      </span>
                    </v-col>
                  </v-row>

                  <!-- AI generated paragraphs (paper_text mode) -->
                  <template v-if="(currentTextResult.ai_generated_paragraphs?.length ?? 0) > 0">
                    <div class="text-subtitle-2 mb-2">AI生成段落标记</div>
                    <div class="paragraph-review-list">
                      <div v-for="(para, pIdx) in currentTextResult.ai_generated_paragraphs" :key="pIdx"
                        class="pa-2 mb-2 rounded"
                        style="background: rgba(var(--v-theme-error), 0.05); border-left: 3px solid rgb(var(--v-theme-error));">
                        <template v-if="typeof para === 'object'">
                          <div class="d-flex align-center mb-1">
                            <v-chip size="x-small" color="error" class="mr-2">段落 {{ para.paragraph_index ?? pIdx + 1 }}</v-chip>
                            <span class="text-caption text-grey">AI概率: {{ ((para.ai_probability || 0) * 100).toFixed(1) }}%</span>
                          </div>
                          <div class="text-caption" style="max-height: 60px; overflow: hidden;">{{ (para.text || '').substring(0, 150) }}{{ (para.text || '').length > 150 ? '...' : '' }}</div>
                        </template>
                        <template v-else>
                          <div class="text-caption text-error mb-1">段落 {{ pIdx + 1 }}</div>
                          <div class="text-caption">{{ (String(para)).substring(0, 150) }}{{ String(para).length > 150 ? '...' : '' }}</div>
                        </template>
                      </div>
                    </div>
                  </template>

                  <!-- Factual fake reason (paper_text) -->
                  <v-alert v-if="currentTextResult.factual_fake_reason" type="warning" variant="tonal" class="mb-3">
                    <div class="text-subtitle-2 mb-1">AI检测分析</div>
                    {{ currentTextResult.factual_fake_reason }}
                  </v-alert>

                  <!-- Template tendency score (review_text) -->
                  <template v-if="currentTextResult.template_tendency_score !== null && currentTextResult.template_tendency_score !== undefined">
                    <div class="text-subtitle-2 mb-2">模板化倾向分析</div>
                    <v-progress-linear
                      :model-value="(currentTextResult.template_tendency_score || 0) * 100"
                      :color="(currentTextResult.template_tendency_score || 0) > 0.7 ? 'error' : (currentTextResult.template_tendency_score || 0) > 0.4 ? 'warning' : 'success'"
                      height="20"
                      class="mb-2"
                    >
                      <template #default="{ value }">
                        <span class="text-caption">{{ value.toFixed(0) }}%</span>
                      </template>
                    </v-progress-linear>
                    <div v-if="currentTextResult.template_analysis_reason" class="text-body-2 text-grey mt-2">
                      {{ currentTextResult.template_analysis_reason }}
                    </div>
                  </template>
                </v-card-text>
              </v-card>
            </v-col>

            <!-- Center col (md=6): reviewer detail (read-only) -->
            <v-col cols="12" md="6">
              <!-- No reviewer selected placeholder -->
              <v-card v-if="selectedReviewerIndex === -1" elevation="2" rounded="lg">
                <v-card-text class="text-center pa-8 text-grey">
                  <v-icon size="64" color="grey" class="mb-4">mdi-account-search</v-icon>
                  <div class="text-h6">请从右侧选择审核员查看审核详情</div>
                </v-card-text>
              </v-card>

              <!-- Reviewer detail display -->
              <template v-else-if="textReviewDetail">
                <!-- Final judgment alert -->
                <v-alert :color="textReviewDetail.result ? 'error' : 'success'" variant="tonal" class="mb-4">
                  <div class="d-flex align-center">
                    <v-icon :icon="textReviewDetail.result ? 'mdi-alert-circle' : 'mdi-check-circle'" class="mr-2"></v-icon>
                    人工判定：{{ textReviewDetail.result ? '疑似造假/AI生成' : '真实' }}
                  </div>
                </v-alert>

                <!-- Paragraph reviews section (paper_text) -->
                <template v-if="filteredParagraphReviews.length">
                  <div class="text-subtitle-1 font-weight-bold mb-2">段落复核</div>
                  <v-card v-for="(item, index) in filteredParagraphReviews" :key="index"
                    variant="outlined" class="pa-3 mb-3"
                    :style="item.is_ai_agreed ? 'border-left: 3px solid rgb(var(--v-theme-error))' : item.is_ai_agreed === false ? 'border-left: 3px solid rgb(var(--v-theme-success))' : ''"
                  >
                    <div class="d-flex align-center mb-2">
                      <v-chip size="small" class="mr-2">段落 {{ item.paragraph_index ?? index + 1 }}</v-chip>
                      <v-chip v-if="item.is_ai_agreed != null"
                        :color="item.is_ai_agreed ? 'error' : 'success'" size="small" variant="tonal">
                        <v-icon start size="x-small">{{ item.is_ai_agreed ? 'mdi-check' : 'mdi-close' }}</v-icon>
                        {{ item.is_ai_agreed ? '同意AI判定' : '不同意AI判定' }}
                      </v-chip>
                    </div>
                    <div class="text-body-1">{{ item.comment || item.reason || '暂无说明' }}</div>
                  </v-card>
                </template>

                <!-- Template review section (review_text) -->
                <template v-if="textReviewDetail.template_review_score != null">
                  <div class="text-subtitle-1 font-weight-bold mb-2 mt-4">模板化复核</div>
                  <v-card variant="outlined" class="pa-3 mb-3">
                    <div class="text-body-2 mb-2">评分</div>
                    <v-progress-linear
                      :model-value="Math.round((textReviewDetail.template_review_score ?? 0) * 100)"
                      :color="(textReviewDetail.template_review_score ?? 0) > 0.7 ? 'error' : (textReviewDetail.template_review_score ?? 0) > 0.4 ? 'warning' : 'success'"
                      height="20"
                      class="mb-2"
                    >
                      <template #default>
                        <span class="text-white text-caption">{{ Math.round((textReviewDetail.template_review_score ?? 0) * 100) }}%</span>
                      </template>
                    </v-progress-linear>
                    <div class="text-body-1">{{ textReviewDetail.template_review_comment || '暂无说明' }}</div>
                  </v-card>
                </template>

                <!-- Overall comment -->
                <div class="text-subtitle-1 font-weight-bold mb-2 mt-4">综合审核意见</div>
                <v-card variant="outlined" class="pa-3">
                  <div class="text-body-1">{{ textReviewDetail.overall_comment || '暂无说明' }}</div>
                </v-card>
              </template>

              <!-- Loading reviewer detail -->
              <v-card v-else-if="selectedReviewerIndex >= 0" elevation="2" rounded="lg">
                <v-card-text class="text-center pa-8">
                  <v-progress-circular indeterminate color="primary" size="32"></v-progress-circular>
                  <div class="text-body-2 text-grey mt-4">加载审核详情...</div>
                </v-card-text>
              </v-card>
            </v-col>

            <!-- Right col (md=3): reviewer list -->
            <v-col cols="12" md="3">
              <v-card elevation="2" rounded="lg" class="mb-4">
                <v-card-title class="pa-4">
                  <v-icon class="mr-2">mdi-account-group</v-icon>
                  审核员列表
                  <v-spacer></v-spacer>
                  <v-chip size="small" color="primary">{{ review_results.length }}</v-chip>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-2" style="max-height: calc(80vh - 200px); overflow-y: auto;">
                  <template v-if="review_results.length > 0">
                    <div v-for="(review, index) in review_results" :key="review.id"
                      class="reviewer-item d-flex align-center pa-3 mb-2 rounded-lg cursor-pointer"
                      :class="{ 'text-sidebar-item-active': selectedReviewerIndex === index }"
                      @click="handleSelectReviewer(index)">
                      <v-avatar size="36" class="mr-3" color="primary">
                        <v-img v-if="review.avatar" :src="getImageUrl(review.avatar)" cover></v-img>
                        <span v-else class="text-body-2">{{ review.username.charAt(0) }}</span>
                      </v-avatar>
                      <div class="flex-grow-1">
                        <div class="text-body-2 font-weight-medium">{{ review.username }}</div>
                        <v-chip size="x-small" :color="review.result ? 'error' : 'success'" variant="tonal" class="mt-1">
                          {{ review.result ? '判定为假' : '判定为真' }}
                        </v-chip>
                      </div>
                      <v-icon size="small" :color="selectedReviewerIndex === index ? 'primary' : 'grey'">
                        {{ selectedReviewerIndex === index ? 'mdi-chevron-left' : 'mdi-chevron-right' }}
                      </v-icon>
                    </div>
                  </template>
                  <template v-else>
                    <div class="d-flex flex-column align-center justify-center py-8">
                      <v-icon size="40" color="grey" class="mb-3">mdi-information-outline</v-icon>
                      <div class="text-body-2 text-grey">暂无人工审核结果</div>
                    </div>
                  </template>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </div>
      </template>

      <!-- ==================== MULTI MODE ==================== -->
      <template v-else-if="isMultiMaterial">
        <div class="pa-6">
          <v-row>
            <!-- Left col (md=2): unified sidebar -->
            <v-col cols="12" md="2">
              <v-card elevation="2" rounded="lg" style="max-height: calc(100vh - 160px); overflow-y: auto;">
                <!-- Image group -->
                <div class="pa-3 d-flex align-center">
                  <v-icon class="mr-2" size="small">mdi-image-multiple</v-icon>
                  <span class="text-subtitle-2">图像</span>
                  <v-spacer />
                  <v-chip size="x-small" color="primary">{{ images.length }}</v-chip>
                </div>
                <v-divider />
                <div class="pa-2">
                  <div class="d-flex flex-wrap" style="gap: 6px;">
                    <div v-for="(image, index) in images" :key="'m-sb-img-' + index"
                      class="multi-sidebar-thumb"
                      :class="{ 'active': multiSelectedType === 'image' && currentImageIndex === index }"
                      @click="handleMultiImageSelect(index)">
                      <v-img :src="getImageUrl(image.img_url)" cover width="56" height="56" class="rounded">
                        <template #error>
                          <div class="d-flex align-center justify-center fill-width fill-height bg-grey-lighten-2 rounded">
                            <v-icon color="grey" size="16">mdi-image-broken-variant</v-icon>
                          </div>
                        </template>
                      </v-img>
                    </div>
                  </div>
                </div>

                <v-divider />

                <!-- Text group -->
                <div class="pa-3 d-flex align-center">
                  <v-icon class="mr-2" size="small">mdi-file-document-multiple</v-icon>
                  <span class="text-subtitle-2">文本</span>
                  <v-spacer />
                  <v-chip size="x-small" color="primary">{{ textResults.length }}</v-chip>
                </div>
                <v-divider />
                <div class="pa-2">
                  <div v-for="(textRes, index) in textResults" :key="'m-sb-txt-' + textRes.result_id"
                    class="text-sidebar-item pa-2 mb-1 rounded-lg cursor-pointer"
                    :class="{ 'text-sidebar-item-active': multiSelectedType === 'text' && currentTextIndex === index }"
                    @click="handleMultiTextSelect(index)">
                    <div class="d-flex align-center mb-1">
                      <v-chip size="x-small" :color="getTextChipColor(textRes)" class="mr-1">
                        {{ getTextChipLabel(textRes) }}
                      </v-chip>
                    </div>
                    <div class="text-caption text-truncate">{{ getRawTextForTextResult(textRes).substring(0, 40) }}{{ getRawTextForTextResult(textRes).length > 40 ? '...' : '' }}</div>
                  </div>
                </div>
              </v-card>
            </v-col>

            <!-- Center col (md=7): conditional content -->
            <v-col cols="12" md="7">
              <!-- Image content -->
              <template v-if="multiSelectedType === 'image'">
                <div class="d-flex" style="gap: 12px;">
                  <!-- Image preview -->
                  <div class="preview-section">
                    <div class="preview-box">
                      <v-img v-if="currentImage" :src="getImageUrl(currentImage.img_url)" contain height="100%"
                        class="rounded-lg"></v-img>
                      <div v-else class="d-flex flex-column align-center justify-center fill-height">
                        <v-icon color="grey" size="64">mdi-image-off-outline</v-icon>
                        <span class="text-caption text-grey mt-2">图片不可用</span>
                      </div>
                      <div class="preview-controls">
                        <v-btn icon="mdi-chevron-left" variant="flat" @click="handlePrevImage"
                          :disabled="currentImageIndex <= 0" class="control-btn" color="black" size="x-large"></v-btn>
                        <v-btn icon="mdi-chevron-right" variant="flat" @click="handleNextImage"
                          :disabled="currentImageIndex >= images.length - 1" class="control-btn" color="black"
                          size="x-large"></v-btn>
                      </div>
                    </div>
                  </div>

                  <!-- Reviewer list for image (inline) -->
                  <div class="review-section rounded-lg elevation-1 pa-4" style="width: 280px;">
                    <div class="text-subtitle-2 font-weight-medium mb-3">审核员</div>
                    <template v-if="review_results.length > 0">
                      <div v-for="(review, index) in review_results" :key="'img-r-' + index"
                        class="reviewer-item d-flex align-center pa-2 mb-2 rounded" style="min-height: 48px;">
                        <v-avatar size="32" class="mr-2" color="primary">
                          <v-img v-if="review.avatar" :src="getImageUrl(review.avatar)" cover></v-img>
                          <span v-else class="text-body-2">{{ review.username.charAt(0) }}</span>
                        </v-avatar>
                        <div class="flex-grow-1">
                          <div class="text-caption font-weight-medium">{{ review.username }}</div>
                          <v-chip size="x-small" :color="review.result ? 'error' : 'success'" variant="tonal">
                            {{ getResult(review.result) }}
                          </v-chip>
                        </div>
                        <v-btn variant="text" size="small" color="primary"
                          @click="handleViewDetail(review)">
                          详情
                        </v-btn>
                      </div>
                    </template>
                    <template v-else>
                      <div class="text-caption text-grey text-center py-4">暂无审核结果</div>
                    </template>
                  </div>
                </div>
              </template>

              <!-- Text content -->
              <template v-else>
                <!-- Text content card -->
                <v-card v-if="currentTextResult" elevation="2" rounded="lg" class="mb-4">
                  <v-card-title class="pa-4 d-flex align-center">
                    <v-icon class="mr-2">mdi-text-box</v-icon>
                    文本内容
                    <v-spacer></v-spacer>
                    <v-btn size="small" variant="text" @click="showFullText = !showFullText">
                      {{ showFullText ? '收起' : '展开全文' }}
                    </v-btn>
                  </v-card-title>
                  <v-divider></v-divider>
                  <v-card-text class="pa-4" style="max-height: 200px; overflow-y: auto;">
                    <div class="text-body-2" style="white-space: pre-wrap; line-height: 1.8;">
                      {{ displayText }}
                    </div>
                  </v-card-text>
                </v-card>

                <!-- AI detection reference -->
                <v-card v-if="currentTextResult" elevation="2" rounded="lg" class="mb-4">
                  <v-card-title class="pa-4">
                    <v-icon class="mr-2" color="primary">mdi-robot</v-icon>
                    AI 检测结果参考
                  </v-card-title>
                  <v-divider></v-divider>
                  <v-card-text class="pa-4" style="max-height: 250px; overflow-y: auto;">
                    <v-row class="mb-3">
                      <v-col cols="6">
                        <div class="text-body-2 text-grey mb-1">AI判定</div>
                        <v-chip :color="currentTextResult.is_fake ? 'error' : 'success'" size="small">
                          {{ currentTextResult.is_fake ? '疑似造假' : '可能真实' }}
                        </v-chip>
                      </v-col>
                      <v-col cols="6">
                        <div class="text-body-2 text-grey mb-1">置信度</div>
                        <span class="text-h6" :class="currentTextResult.confidence_score > 0.7 ? 'error--text' : 'primary--text'">
                          {{ ((currentTextResult.confidence_score || 0) * 100).toFixed(1) }}%
                        </span>
                      </v-col>
                    </v-row>

                    <template v-if="(currentTextResult.ai_generated_paragraphs?.length ?? 0) > 0">
                      <div class="text-subtitle-2 mb-2">AI生成段落标记</div>
                      <div class="paragraph-review-list">
                        <div v-for="(para, pIdx) in currentTextResult.ai_generated_paragraphs" :key="'m-aip-' + pIdx"
                          class="pa-2 mb-2 rounded"
                          style="background: rgba(var(--v-theme-error), 0.05); border-left: 3px solid rgb(var(--v-theme-error));">
                          <template v-if="typeof para === 'object'">
                            <div class="d-flex align-center mb-1">
                              <v-chip size="x-small" color="error" class="mr-2">段落 {{ para.paragraph_index ?? pIdx + 1 }}</v-chip>
                              <span class="text-caption text-grey">AI概率: {{ ((para.ai_probability || 0) * 100).toFixed(1) }}%</span>
                            </div>
                            <div class="text-caption" style="max-height: 60px; overflow: hidden;">{{ (para.text || '').substring(0, 150) }}{{ (para.text || '').length > 150 ? '...' : '' }}</div>
                          </template>
                          <template v-else>
                            <div class="text-caption text-error mb-1">段落 {{ pIdx + 1 }}</div>
                            <div class="text-caption">{{ (String(para)).substring(0, 150) }}{{ String(para).length > 150 ? '...' : '' }}</div>
                          </template>
                        </div>
                      </div>
                    </template>

                    <v-alert v-if="currentTextResult.factual_fake_reason" type="warning" variant="tonal" class="mb-3">
                      <div class="text-subtitle-2 mb-1">AI检测分析</div>
                      {{ currentTextResult.factual_fake_reason }}
                    </v-alert>

                    <template v-if="currentTextResult.template_tendency_score !== null && currentTextResult.template_tendency_score !== undefined">
                      <div class="text-subtitle-2 mb-2">模板化倾向分析</div>
                      <v-progress-linear
                        :model-value="(currentTextResult.template_tendency_score || 0) * 100"
                        :color="(currentTextResult.template_tendency_score || 0) > 0.7 ? 'error' : (currentTextResult.template_tendency_score || 0) > 0.4 ? 'warning' : 'success'"
                        height="20"
                        class="mb-2"
                      >
                        <template #default="{ value }">
                          <span class="text-caption">{{ value.toFixed(0) }}%</span>
                        </template>
                      </v-progress-linear>
                      <div v-if="currentTextResult.template_analysis_reason" class="text-body-2 text-grey mt-2">
                        {{ currentTextResult.template_analysis_reason }}
                      </div>
                    </template>
                  </v-card-text>
                </v-card>

                <!-- Reviewer detail (read-only, inline for multi text) -->
                <v-card v-if="selectedReviewerIndex === -1" elevation="2" rounded="lg">
                  <v-card-text class="text-center pa-6 text-grey">
                    <v-icon size="48" color="grey" class="mb-3">mdi-account-search</v-icon>
                    <div class="text-body-1">请从右侧选择审核员查看审核详情</div>
                  </v-card-text>
                </v-card>

                <template v-else-if="textReviewDetail">
                  <!-- Final judgment alert -->
                  <v-alert :color="textReviewDetail.result ? 'error' : 'success'" variant="tonal" class="mb-4">
                    <div class="d-flex align-center">
                      <v-icon :icon="textReviewDetail.result ? 'mdi-alert-circle' : 'mdi-check-circle'" class="mr-2"></v-icon>
                      人工判定：{{ textReviewDetail.result ? '疑似造假/AI生成' : '真实' }}
                    </div>
                  </v-alert>

                  <!-- Paragraph reviews -->
                  <template v-if="filteredParagraphReviews.length">
                    <div class="text-subtitle-1 font-weight-bold mb-2">段落复核</div>
                    <v-card v-for="(item, index) in filteredParagraphReviews" :key="'m-pr-' + index"
                      variant="outlined" class="pa-3 mb-3"
                      :style="item.is_ai_agreed ? 'border-left: 3px solid rgb(var(--v-theme-error))' : item.is_ai_agreed === false ? 'border-left: 3px solid rgb(var(--v-theme-success))' : ''"
                    >
                      <div class="d-flex align-center mb-2">
                        <v-chip size="small" class="mr-2">段落 {{ item.paragraph_index ?? index + 1 }}</v-chip>
                        <v-chip v-if="item.is_ai_agreed != null"
                          :color="item.is_ai_agreed ? 'error' : 'success'" size="small" variant="tonal">
                          <v-icon start size="x-small">{{ item.is_ai_agreed ? 'mdi-check' : 'mdi-close' }}</v-icon>
                          {{ item.is_ai_agreed ? '同意AI判定' : '不同意AI判定' }}
                        </v-chip>
                      </div>
                      <div class="text-body-1">{{ item.comment || item.reason || '暂无说明' }}</div>
                    </v-card>
                  </template>

                  <!-- Template review -->
                  <template v-if="textReviewDetail.template_review_score != null">
                    <div class="text-subtitle-1 font-weight-bold mb-2 mt-4">模板化复核</div>
                    <v-card variant="outlined" class="pa-3 mb-3">
                      <div class="text-body-2 mb-2">评分</div>
                      <v-progress-linear
                        :model-value="Math.round((textReviewDetail.template_review_score ?? 0) * 100)"
                        :color="(textReviewDetail.template_review_score ?? 0) > 0.7 ? 'error' : (textReviewDetail.template_review_score ?? 0) > 0.4 ? 'warning' : 'success'"
                        height="20"
                        class="mb-2"
                      >
                        <template #default>
                          <span class="text-white text-caption">{{ Math.round((textReviewDetail.template_review_score ?? 0) * 100) }}%</span>
                        </template>
                      </v-progress-linear>
                      <div class="text-body-1">{{ textReviewDetail.template_review_comment || '暂无说明' }}</div>
                    </v-card>
                  </template>

                  <!-- Overall comment -->
                  <div class="text-subtitle-1 font-weight-bold mb-2 mt-4">综合审核意见</div>
                  <v-card variant="outlined" class="pa-3">
                    <div class="text-body-1">{{ textReviewDetail.overall_comment || '暂无说明' }}</div>
                  </v-card>
                </template>
              </template>
            </v-col>

            <!-- Right col (md=3): reviewer list (for text) + task summary -->
            <v-col cols="12" md="3">
              <!-- Reviewer list card (shown when text is selected) -->
              <v-card v-if="multiSelectedType === 'text'" elevation="2" rounded="lg" class="mb-4">
                <v-card-title class="pa-4">
                  <v-icon class="mr-2">mdi-account-group</v-icon>
                  审核员列表
                  <v-spacer></v-spacer>
                  <v-chip size="small" color="primary">{{ review_results.length }}</v-chip>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-2" style="max-height: 400px; overflow-y: auto;">
                  <template v-if="review_results.length > 0">
                    <div v-for="(review, index) in review_results" :key="'m-rev-' + review.id"
                      class="reviewer-item d-flex align-center pa-3 mb-2 rounded-lg cursor-pointer"
                      :class="{ 'text-sidebar-item-active': selectedReviewerIndex === index }"
                      @click="handleSelectReviewer(index)">
                      <v-avatar size="36" class="mr-3" color="primary">
                        <v-img v-if="review.avatar" :src="getImageUrl(review.avatar)" cover></v-img>
                        <span v-else class="text-body-2">{{ review.username.charAt(0) }}</span>
                      </v-avatar>
                      <div class="flex-grow-1">
                        <div class="text-body-2 font-weight-medium">{{ review.username }}</div>
                        <v-chip size="x-small" :color="review.result ? 'error' : 'success'" variant="tonal" class="mt-1">
                          {{ review.result ? '判定为假' : '判定为真' }}
                        </v-chip>
                      </div>
                    </div>
                  </template>
                  <template v-else>
                    <div class="text-caption text-grey text-center py-4">暂无审核结果</div>
                  </template>
                </v-card-text>
              </v-card>

              <!-- Task summary card -->
              <v-card elevation="2" rounded="lg">
                <v-card-title class="pa-4">
                  <v-icon class="mr-2">mdi-clipboard-list</v-icon>
                  任务摘要
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-4">
                  <div class="d-flex justify-space-between mb-3">
                    <span class="text-body-2 text-grey">图片数量</span>
                    <span class="text-body-2 font-weight-bold">{{ images.length }} 张</span>
                  </div>
                  <div class="d-flex justify-space-between mb-3">
                    <span class="text-body-2 text-grey">文本数量</span>
                    <span class="text-body-2 font-weight-bold">{{ textResults.length }} 份</span>
                  </div>
                  <v-divider class="my-3"></v-divider>
                  <div class="d-flex justify-space-between mb-2">
                    <span class="text-body-2 text-grey">已处理</span>
                    <span class="text-body-2 font-weight-bold text-success">{{ done }}份</span>
                  </div>
                  <div class="d-flex justify-space-between">
                    <span class="text-body-2 text-grey">未处理</span>
                    <span class="text-body-2 font-weight-bold text-error">{{ process }}份</span>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </div>
      </template>
    </div>

    <!-- Image detail dialog (image mode and multi image mode) -->
    <v-dialog v-model="showDetailDialog" max-width="90vw" scrollable>
      <v-card>
        <v-toolbar dark color="primary" density="compact">
          <v-btn icon dark @click="showDetailDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>图像审核详情</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-card-text v-if="showDetailDialog && currentImage && !isTextTask" class="pa-0">
          <v-row no-gutters>
            <!-- Left: Image preview with annotation overlay -->
            <v-col cols="12" md="7" class="pa-4">
              <div style="position: relative; background: #f5f5f5; border-radius: 8px; overflow: hidden;">
                <v-img :src="getImageUrl(currentImage.img_url)" contain
                  :max-height="'70vh'" class="rounded-lg">
                  <template #placeholder>
                    <div class="d-flex align-center justify-center fill-height">
                      <v-progress-circular indeterminate color="primary" />
                    </div>
                  </template>
                </v-img>
                <!-- Annotation overlay SVG -->
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;">
                  <svg width="100%" height="100%">
                    <g v-for="(dimAnnotations, dimIdx) in annotations" :key="dimIdx">
                      <g v-for="(obj, objIdx) in dimAnnotations" :key="objIdx">
                        <polyline :points="obj.points.map(p => `${p.x},${p.y}`).join(' ')"
                          :stroke="obj.color" stroke-width="3" fill="none" opacity="0.7"
                          stroke-linecap="round" stroke-linejoin="round" />
                        <circle v-for="(pt, ptIdx) in obj.points" :key="ptIdx"
                          :cx="pt.x" :cy="pt.y" r="3" :fill="obj.color" opacity="0.7" />
                      </g>
                    </g>
                  </svg>
                </div>
              </div>
              <div class="d-flex align-center justify-center mt-3">
                <v-chip :color="result ? 'success' : 'error'" variant="tonal" size="small">
                  <v-icon start size="x-small">{{ result ? 'mdi-check-circle' : 'mdi-alert-circle' }}</v-icon>
                  AI检测置信度：{{ Math.round(AI_detection * 100) }}%
                </v-chip>
              </div>
            </v-col>
            <!-- Right: Scoring dimensions + judgment -->
            <v-col cols="12" md="5" class="pa-4" style="max-height: 80vh; overflow-y: auto;">
              <div class="text-h6 font-weight-medium mb-4">人工审查结果</div>
              <div v-for="(dim, idx) in imageReviewDimensions" :key="idx" class="mb-4"
                style="border-bottom: 1px solid rgba(0,0,0,0.08); padding-bottom: 12px;">
                <div class="d-flex align-center justify-space-between mb-1">
                  <span class="text-subtitle-2">{{ dim.name }}</span>
                  <v-btn v-if="annotations[idx]?.length > 0" size="x-small" variant="text" color="primary"
                    @click="toggleAnnotation(idx)">
                    <v-icon start size="x-small">{{ showAnnotations[idx] ? 'mdi-eye-off' : 'mdi-eye' }}</v-icon>
                    {{ showAnnotations[idx] ? '隐藏标注' : '显示标注' }}
                  </v-btn>
                </div>
                <div class="d-flex align-center mb-1">
                  <v-icon :color="getDegreeColor(scores[idx])" size="small" class="mr-1">
                    {{ getDegreeIcon(scores[idx]) }}
                  </v-icon>
                  <span class="text-body-2">{{ getDegreeLabel(scores[idx]) }}</span>
                </div>
                <div class="text-caption text-grey">理由：{{ reasons[idx] || '暂无理由' }}</div>
              </div>
              <v-divider class="my-3" />
              <div class="text-subtitle-1 font-weight-bold mb-3">造假判定</div>
              <v-alert :color="result ? 'success' : 'error'" variant="tonal" density="compact">
                <div class="d-flex align-center">
                  <v-icon :icon="result ? 'mdi-check-circle' : 'mdi-alert-circle'" class="mr-2" />
                  {{ result ? '真实图片' : '造假图片' }}
                </div>
              </v-alert>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-text v-else-if="showDetailDialog && textReviewDetail" class="pa-4">
          <v-row>
            <!-- Left: AI Detection Reference -->
            <v-col cols="12" md="3">
              <v-card variant="outlined" class="mb-3">
                <v-card-title class="text-subtitle-1 py-2 px-3">
                  <v-icon start size="small">mdi-robot</v-icon>AI检测参考
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-3">
                  <div class="d-flex align-center mb-3">
                    <v-chip :color="currentTextResult?.is_fake ? 'error' : 'success'" size="small" variant="tonal">
                      {{ currentTextResult?.is_fake ? '疑似造假' : '可能真实' }}
                    </v-chip>
                    <span class="ml-2 text-body-2">
                      置信度：{{ Math.round((currentTextResult?.confidence_score ?? 0) * 100) }}%
                    </span>
                  </div>
                  <template v-if="currentTextResult?.ai_generated_paragraphs?.length">
                    <div class="text-subtitle-2 mb-2">AI标记段落</div>
                    <div v-for="(para, idx) in currentTextResult.ai_generated_paragraphs" :key="idx"
                      class="mb-2 pa-2"
                      style="border-left: 3px solid rgb(var(--v-theme-error)); background: rgba(var(--v-theme-error), 0.05); border-radius: 4px;">
                      <template v-if="typeof para === 'object'">
                        <div class="text-caption text-error mb-1">段落 {{ para.paragraph_index ?? idx + 1 }}</div>
                        <div class="text-body-2">{{ (para.text || '').substring(0, 150) }}{{ (para.text || '').length > 150 ? '...' : '' }}</div>
                      </template>
                      <template v-else>
                        <div class="text-caption text-error mb-1">段落 {{ idx + 1 }}</div>
                        <div class="text-body-2">{{ (String(para)).substring(0, 150) }}{{ String(para).length > 150 ? '...' : '' }}</div>
                      </template>
                    </div>
                  </template>
                  <template v-if="currentTextResult?.factual_fake_reason">
                    <v-alert type="warning" variant="tonal" density="compact" class="mt-3">
                      <div class="text-subtitle-2">AI检测分析</div>
                      {{ currentTextResult.factual_fake_reason.substring(0, 300) }}{{ currentTextResult.factual_fake_reason.length > 300 ? '...' : '' }}
                    </v-alert>
                  </template>
                  <template v-if="currentTextResult?.template_tendency_score != null">
                    <div class="text-subtitle-2 mt-3 mb-1">模板化倾向分析</div>
                    <v-progress-linear
                      :model-value="Math.round((currentTextResult.template_tendency_score ?? 0) * 100)"
                      :color="(currentTextResult.template_tendency_score ?? 0) > 0.7 ? 'error' : (currentTextResult.template_tendency_score ?? 0) > 0.4 ? 'warning' : 'success'"
                      height="20"
                      class="mb-1"
                    >
                      <template #default>
                        <span class="text-white text-caption">{{ Math.round((currentTextResult.template_tendency_score ?? 0) * 100) }}%</span>
                      </template>
                    </v-progress-linear>
                    <div v-if="currentTextResult?.template_analysis_reason" class="text-body-2 text-grey mt-1">
                      {{ currentTextResult.template_analysis_reason.substring(0, 200) }}{{ currentTextResult.template_analysis_reason.length > 200 ? '...' : '' }}
                    </div>
                  </template>
                </v-card-text>
              </v-card>
            </v-col>
            <!-- Center: Review Detail -->
            <v-col cols="12" md="6">
              <v-alert :color="textReviewDetail.result ? 'error' : 'success'" variant="tonal" class="mb-4">
                <div class="d-flex align-center">
                  <v-icon :icon="textReviewDetail.result ? 'mdi-alert-circle' : 'mdi-check-circle'" class="mr-2"></v-icon>
                  人工判定：{{ textReviewDetail.result ? '疑似造假/AI生成' : '真实' }}
                </div>
              </v-alert>
              <template v-if="filteredParagraphReviews.length">
                <div class="text-subtitle-1 font-weight-bold mb-2">段落复核</div>
                <v-card v-for="(item, index) in filteredParagraphReviews" :key="index"
                  variant="outlined" class="pa-3 mb-3"
                  :style="item.is_ai_agreed ? 'border-left: 3px solid rgb(var(--v-theme-error))' : item.is_ai_agreed === false ? 'border-left: 3px solid rgb(var(--v-theme-success))' : ''"
                >
                  <div class="d-flex align-center mb-2">
                    <v-chip size="small" class="mr-2">段落 {{ item.paragraph_index ?? index + 1 }}</v-chip>
                    <v-chip v-if="item.is_ai_agreed != null"
                      :color="item.is_ai_agreed ? 'error' : 'success'" size="small" variant="tonal">
                      <v-icon start size="x-small">{{ item.is_ai_agreed ? 'mdi-check' : 'mdi-close' }}</v-icon>
                      {{ item.is_ai_agreed ? '同意AI判定' : '不同意AI判定' }}
                    </v-chip>
                  </div>
                  <div class="text-body-1">{{ item.comment || item.reason || '暂无说明' }}</div>
                </v-card>
              </template>
              <template v-if="textReviewDetail.template_review_score != null">
                <div class="text-subtitle-1 font-weight-bold mb-2 mt-4">模板化复核</div>
                <v-card variant="outlined" class="pa-3 mb-3">
                  <div class="text-body-2 mb-2">评分</div>
                  <v-progress-linear
                    :model-value="Math.round((textReviewDetail.template_review_score ?? 0) * 100)"
                    :color="(textReviewDetail.template_review_score ?? 0) > 0.7 ? 'error' : (textReviewDetail.template_review_score ?? 0) > 0.4 ? 'warning' : 'success'"
                    height="20"
                    class="mb-2"
                  >
                    <template #default>
                      <span class="text-white text-caption">{{ Math.round((textReviewDetail.template_review_score ?? 0) * 100) }}%</span>
                    </template>
                  </v-progress-linear>
                  <div class="text-body-1">{{ textReviewDetail.template_review_comment || '暂无说明' }}</div>
                </v-card>
              </template>
              <div class="text-subtitle-1 font-weight-bold mb-2 mt-4">综合审核意见</div>
              <v-card variant="outlined" class="pa-3">
                <div class="text-body-1">{{ textReviewDetail.overall_comment || '暂无说明' }}</div>
              </v-card>
            </v-col>
            <!-- Right: Final Judgment & Summary -->
            <v-col cols="12" md="3">
              <v-card variant="outlined" class="mb-3">
                <v-card-title class="text-subtitle-1 py-2 px-3">最终判定</v-card-title>
                <v-divider></v-divider>
                <v-card-text class="d-flex flex-column ga-3 pt-3">
                  <v-btn :color="textReviewDetail.result === true ? 'error' : 'grey'" variant="tonal" size="large" disabled>
                    <v-icon start>mdi-alert-circle</v-icon>
                    判定为假
                  </v-btn>
                  <v-btn :color="textReviewDetail.result === false ? 'success' : 'grey'" variant="tonal" size="large" disabled>
                    <v-icon start>mdi-check-circle</v-icon>
                    判定为真
                  </v-btn>
                </v-card-text>
              </v-card>
              <v-card variant="outlined">
                <v-card-title class="text-subtitle-1 py-2 px-3">审核摘要</v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-3">
                  <div class="d-flex justify-space-between mb-2">
                    <span class="text-body-2">最终判定</span>
                    <v-chip :color="textReviewDetail.result ? 'error' : 'success'" size="small" variant="tonal">
                      {{ textReviewDetail.result ? '疑似造假' : '真实' }}
                    </v-chip>
                  </div>
                  <div v-if="filteredParagraphReviews.length" class="d-flex justify-space-between mb-2">
                    <span class="text-body-2">段落复核数</span>
                    <span class="text-body-2 font-weight-bold">{{ filteredParagraphReviews.length }}</span>
                  </div>
                  <div v-if="textReviewDetail.template_review_score != null" class="d-flex justify-space-between mb-2">
                    <span class="text-body-2">模板化评分</span>
                    <span class="text-body-2 font-weight-bold">{{ Math.round((textReviewDetail.template_review_score ?? 0) * 100) }}%</span>
                  </div>
                  <v-divider class="my-2"></v-divider>
                  <div class="d-flex justify-space-between">
                    <span class="text-body-2">AI置信度</span>
                    <span class="text-body-2 font-weight-bold" :class="currentTextResult?.is_fake ? 'text-error' : 'text-success'">
                      {{ Math.round((currentTextResult?.confidence_score ?? 0) * 100) }}%
                    </span>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useTheme } from 'vuetify'
import { useUserStore } from '@/stores/user'
import { useSnackbarStore } from '@/stores/snackbar'
import publisher from '@/api/publisher'
import { resolveImageUrl } from '@/utils/preview-url'

const router = useRouter()
const route = useRoute()
const theme = useTheme()
const userStore = useUserStore()
const snackbar = useSnackbarStore()

const review_request_id = computed(() => (route.params as RouteParams & { review_request_id: number }).review_request_id)

// ==================== Interfaces ====================
interface Task {
  id: string
  publishTime: string
  reviewer: string
  progress: number
  publisherId: string
}

interface Image {
  img_id: string
  img_url: string
  thumbnail: string
  reviewStatus: string
  reviewComment?: string
}

interface Review {
  id: number
  username: string
  avatar: string
  result: boolean
}

interface TextReviewDetail {
  overall_comment?: string
  paragraph_reviews?: any[]
  template_review_score?: number | null
  template_review_comment?: string | null
  result: boolean
}

interface RouteParams {
  id: string
}

interface dimension {
  method: string
  probability: number
}

interface TextResult {
  result_id: number
  resource_id: number
  text_type: string
  status: string
  is_fake: boolean
  confidence_score: number
  ai_generated_paragraphs?: any[]
  factual_fake_reason?: string
  template_tendency_score?: number
  template_analysis_reason?: string
  raw_text?: string
}

// ==================== State ====================
const taskData = ref<Task | null>(null)
const images = ref<Image[]>([])
const textResults = ref<TextResult[]>([])
const taskType = ref<string>('image')
const structuredTaskId = ref<number | null>(null)
const isTextTask = computed(() => ['paper_text', 'review_text'].includes(taskType.value))
const isMultiMaterial = computed(() => taskType.value === 'multi_material')
const done = ref(0)
const process = ref(0)
const AI_detection = ref(0)
const loading = ref(true)
const review_results = ref<Review[]>([])
const textReviewDetail = ref<TextReviewDetail | null>(null)
const reasons = ref<string[]>([])
const result = ref(false)
const scores = ref<number[]>([])
const annotations = ref<Array<Array<{ points: { x: number; y: number; }[]; color: string; }>>>([])
const detection_results = ref<dimension[]>([])

// New refs
const currentImageIndex = ref(0)
const currentTextIndex = ref(0)
const selectedReviewerIndex = ref(-1)
const showFullText = ref(false)
const multiSelectedType = ref<'image' | 'text'>('image')
const rawTexts = ref<Record<number, string>>({})
const showDetailDialog = ref(false)

// ==================== Computed ====================
const currentImage = computed(() => {
  if (currentImageIndex.value >= 0 && currentImageIndex.value < images.value.length) {
    return images.value[currentImageIndex.value]
  }
  return undefined
})

const currentTextResult = computed(() => {
  if (currentTextIndex.value >= 0 && currentTextIndex.value < textResults.value.length) {
    return textResults.value[currentTextIndex.value]
  }
  return undefined
})

const displayText = computed(() => {
  const raw = currentTextResult.value?.raw_text || getRawTextForTextResult(currentTextResult.value) || ''
  if (!raw) return ''
  if (showFullText.value) return raw
  return raw.substring(0, 500) + (raw.length > 500 ? '...' : '')
})

const selectedReviewer = computed(() => {
  if (selectedReviewerIndex.value >= 0 && selectedReviewerIndex.value < review_results.value.length) {
    return review_results.value[selectedReviewerIndex.value]
  }
  return null
})

const filteredParagraphReviews = computed(() => {
  return textReviewDetail.value?.paragraph_reviews || []
})

// ==================== Utility functions ====================
const convert = (index: number) => {
  switch (index) {
    case 0: return '高斯模糊'
    case 1: return '亮度/对比度调节'
    case 2: return '智能修复'
    case 3: return '暴力覆盖'
    case 4: return '同图复制'
    case 5: return '重叠切割'
    case 6: return '跨图拼接'
    default: return '未知'
  }
}

const formatNumber = (val: number) => {
  return `${((val ?? 0) * 100).toFixed(2)}%`
}

const getImageUrl = (url: string) => {
  return resolveImageUrl(url)
}

const getResult = (res: boolean) => {
  return res === true ? '疑似造假/AI生成' : '真实'
}

// Image review detail helpers
const imageReviewDimensions = [
  { name: '高斯模糊' },
  { name: '亮度/对比度调节' },
  { name: '智能修复' },
  { name: '暴力覆盖' },
  { name: '同图复制' },
  { name: '重叠切割' },
  { name: '跨图拼接' },
]

const showAnnotations = ref<boolean[]>(Array(7).fill(false))
const toggleAnnotation = (idx: number) => { showAnnotations.value[idx] = !showAnnotations.value[idx] }

const getDegreeColor = (val: number | null | undefined) => {
  if (val == null) return 'grey'
  switch (val) {
    case 1: return 'success'
    case 2: return 'info'
    case 3: return 'yellow'
    case 4: return 'warning'
    case 5: return 'error'
    default: return 'grey'
  }
}

const getDegreeIcon = (val: number | null | undefined) => {
  if (val == null) return 'mdi-emoticon-neutral'
  switch (val) {
    case 1: return 'mdi-emoticon-happy'
    case 2: return 'mdi-emoticon-smile'
    case 3: return 'mdi-emoticon-neutral'
    case 4: return 'mdi-emoticon-sad'
    case 5: return 'mdi-emoticon-frown'
    default: return 'mdi-emoticon-neutral'
  }
}

const getDegreeLabel = (val: number | null | undefined) => {
  if (val == null) return '未评分'
  switch (val) {
    case 1: return '基本没有'
    case 2: return '轻微'
    case 3: return '不明显'
    case 4: return '较严重'
    case 5: return '严重'
    default: return '未评分'
  }
}

const isPaperTextRes = (textRes: TextResult | undefined) => {
  if (!textRes) return false
  if (textRes.factual_fake_reason != null) return true
  if ((textRes.ai_generated_paragraphs?.length ?? 0) > 0) return true
  return false
}

const isReviewTextRes = (textRes: TextResult | undefined) => {
  if (!textRes) return false
  if (textRes.template_tendency_score != null) return true
  return false
}

const getTextChipColor = (textRes: TextResult | undefined) => {
  if (!textRes) return 'grey'
  if (taskType.value === 'paper_text' || isPaperTextRes(textRes)) return 'green'
  if (taskType.value === 'review_text' || isReviewTextRes(textRes)) return 'orange'
  return 'grey'
}

const getTextChipLabel = (textRes: TextResult | undefined) => {
  if (!textRes) return '文本'
  if (taskType.value === 'paper_text' || isPaperTextRes(textRes)) return '论文'
  if (taskType.value === 'review_text' || isReviewTextRes(textRes)) return '评审'
  return '文本'
}

const getRawTextForTextResult = (textRes: TextResult | undefined) => {
  if (!textRes) return ''
  if (textRes.raw_text) return textRes.raw_text
  return rawTexts.value[textRes.resource_id] || ''
}

// ==================== Task type resolution ====================
const resolveTaskType = (response: any) => {
  const detectType = response?.detect_type
  const responseTaskType = response?.task_type
  if (responseTaskType === 'multi_material' || detectType === 'multi') return 'multi_material'
  if (responseTaskType === 'review_text' || detectType === 'review') return 'review_text'
  if (responseTaskType === 'paper_text' || detectType === 'paper') return 'paper_text'
  if (responseTaskType === 'unknown' || !responseTaskType) {
    const hasImages = response?.images?.length > 0
    const hasTexts = response?.texts?.length > 0
    if (hasImages && hasTexts) return 'multi_material'
    if (hasTexts) return 'paper_text'
    return 'image'
  }
  return responseTaskType
}

// ==================== Build text results ====================

// Extract resource key from item_id for grouping sections by text resource.
// Patterns: {detectType}_paper_{fileIdx}_{secIdx}, {detectType}_review_file_{fileIdx}_{secIdx},
//           {detectType}_review_text_{textIdx}
const extractResourceKey = (itemId: string): string => {
  const parts = itemId.split('_')
  const reviewFilePos = parts.findIndex((p: string, i: number) => p === 'review' && parts[i + 1] === 'file')
  if (reviewFilePos >= 0) return `review_file_${parts[reviewFilePos + 2]}`
  const reviewTextPos = parts.findIndex((p: string, i: number) => p === 'review' && parts[i + 1] === 'text')
  if (reviewTextPos >= 0) return `review_text_${parts[reviewTextPos + 2]}`
  const paperPos = parts.lastIndexOf('paper')
  if (paperPos >= 0) return `paper_${parts[paperPos + 1]}`
  return itemId
}

const buildTextResultsFromStructuredResult = (structured: any, fallbackTexts: any[] = []) => {
  const overall = structured?.overall || structured?.result?.overall || {}
  const sections = structured?.sections || structured?.result?.evidence?.per_section || []
  const summary = structured?.summary || structured?.result?.summary || ''
  const detectType = structured?.detect_type

  if (!Array.isArray(sections) || sections.length === 0) {
    return fallbackTexts.map((text: any, index: number) => ({
      result_id: text.text_id || index + 1,
      resource_id: text.text_id || index + 1,
      text_type: text.source_type || detectType || 'structured',
      status: structured?.status || 'completed',
      is_fake: Boolean(overall?.is_fake ?? structured?.overall_is_fake),
      confidence_score: Number(overall?.confidence_score ?? structured?.confidence_score ?? 0),
      ai_generated_paragraphs: [],
      factual_fake_reason: detectType === 'paper' ? summary : undefined,
      template_tendency_score: detectType === 'review' ? Number(overall?.confidence_score ?? structured?.confidence_score ?? 0) : undefined,
      template_analysis_reason: detectType === 'review' ? summary : undefined,
      raw_text: text.raw_text || '',
    }))
  }

  // Group sections by resource key
  const groups = new Map<string, any[]>()
  sections.forEach((section: any) => {
    const key = extractResourceKey(String(section?.item_id || ''))
    if (!groups.has(key)) groups.set(key, [])
    groups.get(key)!.push(section)
  })

  // Build a lookup: resourceKey → resourceIndex → fallbackText
  const groupKeys = Array.from(groups.keys())

  return groupKeys.map((key: string, groupIndex: number) => {
    const groupSections = groups.get(key)!
    const isPaper = detectType === 'paper' || key.startsWith('paper')
    const isReview = detectType === 'review' || key.startsWith('review')

    // Aggregate: any section flagged as AIGC → whole resource is fake
    const anyFake = groupSections.some((s: any) => Boolean(s?.is_aigc))
    const maxConfidence = Math.max(...groupSections.map((s: any) =>
      Number(s?.probabilities?.aigc ?? s?.confidence_score ?? 0)
    ))
    const avgConfidence = groupSections.reduce((sum: number, s: any) =>
      sum + Number(s?.probabilities?.aigc ?? s?.confidence_score ?? 0), 0
    ) / groupSections.length

    // Collect AI-generated paragraphs
    const aiParagraphs = groupSections
      .filter((s: any) => Boolean(s?.is_aigc))
      .map((s: any, idx: number) => ({
        paragraph_index: idx,
        ai_probability: Number(s?.probabilities?.aigc ?? s?.confidence_score ?? 0),
        text: s?.text || '',
        reason: s?.label_name || '',
      }))

    // Determine resource_id from fallback texts
    let resourceIndex = -1
    const parts = key.split('_')
    if (key.startsWith('review_file')) resourceIndex = Number(parts[2])
    else if (key.startsWith('review_text')) resourceIndex = Number(parts[2])
    else if (key.startsWith('paper')) resourceIndex = Number(parts[1])

    const fallbackText = fallbackTexts[resourceIndex >= 0 ? resourceIndex : groupIndex]
    const resourceId = fallbackText?.text_id || (groupIndex + 1)

    return {
      result_id: groupIndex + 1,
      resource_id: Number(resourceId),
      text_type: isPaper ? 'paper' : isReview ? 'review' : (detectType || 'structured'),
      status: structured?.status || 'completed',
      is_fake: anyFake,
      confidence_score: Number(maxConfidence || avgConfidence || overall?.confidence_score ?? 0),
      ai_generated_paragraphs: aiParagraphs,
      factual_fake_reason: isPaper ? summary : undefined,
      template_tendency_score: isReview ? Number(maxConfidence || avgConfidence || overall?.confidence_score ?? 0) : undefined,
      template_analysis_reason: isReview ? summary : undefined,
      raw_text: fallbackText?.raw_text || '',
    }
  })
}

// ==================== Data fetching ====================
const fetchStructuredDetectionResults = async (fallbackTexts: any[] = []) => {
  if (!structuredTaskId.value) {
    // No linked detection task — use fallback text data without error
    if (fallbackTexts.length > 0 && textResults.value.length === 0) {
      textResults.value = fallbackTexts.map((t: any, index: number) => ({
        result_id: t.text_id || index + 1,
        resource_id: t.text_id || index + 1,
        text_type: t.source_type || 'structured',
        status: 'completed',
        is_fake: false,
        confidence_score: 0,
        raw_text: t.raw_text || '',
      }))
    }
    return
  }
  try {
    const structured = (await publisher.getStructuredTaskResult(structuredTaskId.value)).data
    const overall = structured?.overall || structured?.result?.overall || {}
    taskType.value = structured?.task_type || resolveTaskType(structured)
    AI_detection.value = Number(overall?.confidence_score ?? structured?.confidence_score ?? 0)
    textResults.value = buildTextResultsFromStructuredResult(structured, fallbackTexts)
    done.value = textResults.value.filter(t => t.status === 'completed').length
    process.value = Math.max(textResults.value.length - done.value, 0)
    // Populate rawTexts ref
    textResults.value.forEach(tr => {
      if (tr.raw_text) rawTexts.value[tr.resource_id] = tr.raw_text
    })
  } catch (error) {
    // Don't show error — structured results are optional, fallback data already populated
  }
}

const fetchDetectionResults = async () => {
  try {
    if (isTextTask.value) {
      await fetchStructuredDetectionResults(textResults.value)
    } else if (isMultiMaterial.value && multiSelectedType.value === 'text') {
      await fetchStructuredDetectionResults(textResults.value)
    } else {
      if (currentImage.value) {
        const id = (await publisher.getDetectionID({ img_id: currentImage.value.img_id })).data?.detection_result_id
        if (!id) return
        const response = (await publisher.getSingleImageResult(id)).data
        detection_results.value = response?.sub_methods || []
      }
    }
  } catch (error) {
    // Detection results are supplementary — don't block the page
  }
}

const fetchReview = async (img?: Image) => {
  try {
    selectedReviewerIndex.value = -1
    textReviewDetail.value = null

    if (isTextTask.value || (isMultiMaterial.value && multiSelectedType.value === 'text')) {
      if (!currentTextResult.value?.resource_id) {
        review_results.value = []
        return
      }
      review_results.value = (await publisher.getTextReviewAll({
        review_request_id: review_request_id.value,
        text_id: currentTextResult.value.resource_id,
      })).data.reviewers_results || []
      return
    }
    if (!img) {
      review_results.value = []
      return
    }
    review_results.value = (await publisher.getImageReviewAll({
      review_request_id: review_request_id.value,
      img_id: img.img_id
    })).data.reviewers_results || []
  } catch (error) {
    snackbar.showMessage('获取人工审核结果失败', 'error')
  }
}

const fetchReviewDetail = async (review: Review) => {
  try {
    if (isTextTask.value || (isMultiMaterial.value && multiSelectedType.value === 'text')) {
      if (!currentTextResult.value?.resource_id) return
      textReviewDetail.value = (await publisher.getTextReviewDetail({
        review_request_id: review_request_id.value,
        text_id: currentTextResult.value.resource_id,
        reviewer_id: review.id,
      })).data
      return
    }
    if (!currentImage.value) return
    textReviewDetail.value = null
    const response = (await publisher.getImageReviewDetail({
      review_request_id: review_request_id.value,
      img_id: currentImage.value.img_id,
      reviewer_id: review.id
    })).data
    reasons.value = response.reasons
    result.value = response.result
    scores.value = response.scores
    annotations.value = response.points
  } catch (error) {
    snackbar.showMessage('获取人工审核详情失败', 'error')
  }
}

// ==================== Event handlers ====================
const handleImageSelect = (index: number) => {
  currentImageIndex.value = index
  selectedReviewerIndex.value = -1
  textReviewDetail.value = null
  fetchReview(currentImage.value)
  fetchDetectionResults()
}

const handleTextSelect = (index: number) => {
  currentTextIndex.value = index
  selectedReviewerIndex.value = -1
  textReviewDetail.value = null
  showFullText.value = false
  fetchReview()
}

const handleSelectReviewer = (index: number) => {
  selectedReviewerIndex.value = index
  const reviewer = review_results.value[index]
  if (reviewer) {
    fetchReviewDetail(reviewer)
  }
}

const handleMultiImageSelect = (index: number) => {
  multiSelectedType.value = 'image'
  currentImageIndex.value = index
  selectedReviewerIndex.value = -1
  textReviewDetail.value = null
  fetchReview(currentImage.value)
}

const handleMultiTextSelect = (index: number) => {
  multiSelectedType.value = 'text'
  currentTextIndex.value = index
  selectedReviewerIndex.value = -1
  textReviewDetail.value = null
  showFullText.value = false
  fetchReview()
}

const handlePrevImage = () => {
  if (currentImageIndex.value > 0) {
    currentImageIndex.value--
    if (isMultiMaterial.value) {
      fetchReview(currentImage.value)
    } else {
      fetchReview(currentImage.value)
      fetchDetectionResults()
    }
  }
}

const handleNextImage = () => {
  if (currentImageIndex.value < images.value.length - 1) {
    currentImageIndex.value++
    if (isMultiMaterial.value) {
      fetchReview(currentImage.value)
    } else {
      fetchReview(currentImage.value)
      fetchDetectionResults()
    }
  }
}

const handleViewDetail = (review: Review) => {
  textReviewDetail.value = null
  showDetailDialog.value = true
  fetchReviewDetail(review)
}

const handleDownloadReport = async () => {
  try {
    const response = await publisher.downloadReviewReport({ review_request_id: review_request_id.value })
    console.log('Downloaded data is a Blob. Type:', response.data.type, 'Size:', response.data.size);

    if (!(response.data instanceof Blob)) {
      console.error('Expected Blob data, but received:', response.data);
      snackbar.showMessage('下载失败：未收到文件数据', 'error');
      return;
    }

    const blob = response.data

    if (blob.type !== 'application/pdf') {
      console.warn('Downloaded Blob type is not application/pdf:', blob.type);
      snackbar.showMessage('下载的文件不是PDF格式', 'warning');
      return;
    }

    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `人工审核报告_${review_request_id.value}.pdf`
    link.target = '_blank'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    snackbar.showMessage('报告下载成功', 'success')
  } catch (error) {
    snackbar.showMessage('报告下载失败', 'error')
  }
}

// ==================== onMounted ====================
onMounted(async () => {
  const hasPermission = true
  if (!hasPermission) return
  try {
    const response = (await publisher.getRequestDetail({ review_request_id: review_request_id.value })).data
    const hasImages = response.images && response.images.length > 0
    const hasTexts = response.texts && response.texts.length > 0
    const resolvedTaskType = resolveTaskType(response)
    const isStructuredTask = ['paper_text', 'review_text', 'multi_material'].includes(resolvedTaskType)

    structuredTaskId.value = response.task_id ? Number(response.task_id) : null
    done.value = response.status?.done ?? 0
    process.value = response.status?.process ?? 0
    AI_detection.value = response.ai_detection_result?.confidence_score ?? 0

    // Store raw texts mapping
    if (response.texts) {
      response.texts.forEach((t: any) => {
        if (t.text_id && t.raw_text) {
          rawTexts.value[t.text_id] = t.raw_text
        }
      })
    }

    if (isStructuredTask) {
      taskType.value = resolvedTaskType
      images.value = resolvedTaskType === 'multi_material' ? response.images : []
      multiSelectedType.value = resolvedTaskType === 'multi_material' ? 'image' : 'text'

      // Build initial text results from response.texts
      const initialTexts = (response.texts || []).map((t: any) => ({
        result_id: t.text_id,
        resource_id: t.text_id,
        text_type: t.source_type,
        status: 'completed',
        is_fake: false,
        confidence_score: 0,
        raw_text: t.raw_text || '',
      }))

      textResults.value = initialTexts
      currentTextIndex.value = 0

      // Fetch structured detection results (will overwrite with real data)
      await fetchStructuredDetectionResults(response.texts || [])

      // If structured detection didn't populate text results, fallback
      if (textResults.value.length === 0 && (response.texts || []).length > 0) {
        textResults.value = (response.texts || []).map((t: any, index: number) => ({
          result_id: t.text_id || index + 1,
          resource_id: t.text_id || index + 1,
          text_type: t.source_type || 'structured',
          status: 'completed',
          is_fake: false,
          confidence_score: 0,
          raw_text: t.raw_text || '',
        }))
      }

      // Fetch initial reviewers
      if (resolvedTaskType === 'multi_material' && images.value.length > 0) {
        currentImageIndex.value = 0
        review_results.value = (await publisher.getImageReviewAll({
          review_request_id: review_request_id.value,
          img_id: images.value[0].img_id
        })).data.reviewers_results || []
      } else {
        currentTextIndex.value = 0
        await fetchReview()
      }
    } else if (hasImages && hasTexts) {
      // multi_material: both images and texts
      taskType.value = 'multi_material'
      images.value = response.images
      multiSelectedType.value = 'image'

      textResults.value = response.texts.map((t: any) => ({
        result_id: t.text_id,
        resource_id: t.text_id,
        text_type: t.source_type,
        status: 'completed',
        is_fake: false,
        confidence_score: 0,
        raw_text: t.raw_text || '',
      }))

      if (images.value.length > 0) {
        currentImageIndex.value = 0
        review_results.value = (await publisher.getImageReviewAll({
          review_request_id: review_request_id.value,
          img_id: images.value[0].img_id
        })).data.reviewers_results || []
      }
      fetchDetectionResults()
    } else if (hasImages) {
      // Pure image task
      taskType.value = 'image'
      images.value = response.images
      currentImageIndex.value = 0
      if (images.value.length > 0) {
        review_results.value = (await publisher.getImageReviewAll({
          review_request_id: review_request_id.value,
          img_id: images.value[0].img_id
        })).data.reviewers_results || []
      }
      fetchDetectionResults()
    } else if (hasTexts) {
      // Pure text task
      taskType.value = resolvedTaskType
      textResults.value = response.texts.map((t: any) => ({
        result_id: t.text_id,
        resource_id: t.text_id,
        text_type: t.source_type,
        status: 'completed',
        is_fake: false,
        confidence_score: 0,
        raw_text: t.raw_text || '',
      }))
      currentTextIndex.value = 0
      done.value = textResults.value.filter(t => t.status === 'completed').length
      process.value = textResults.value.length - done.value
      if (textResults.value.length > 0) {
        AI_detection.value = textResults.value[0].confidence_score || 0
      }
      fetchDetectionResults()
      fetchReview()
    } else {
      taskType.value = 'image'
    }
    loading.value = false
  } catch (error) {
    console.error('Failed to load task data:', error)
    snackbar.showMessage('获取数据失败', 'error')
    loading.value = false
  }
})
</script>

<style scoped>
.task-detail {
  position: relative;
  min-height: 100vh;
  max-height: 100vh;
  background-color: rgb(var(--v-theme-surface));
  overflow: hidden;
}

.main-content {
  height: calc(100vh - 80px);
  overflow: auto;
  background-color: rgb(var(--v-theme-surface));
}

.info-section {
  background-color: rgb(var(--v-theme-surface));
  padding: 16px 0;
}

.info-content {
  width: 100%;
  background-color: rgb(var(--v-theme-surface));
  min-height: 160px;
  padding: 12px 16px !important;
}

.progress-circle {
  width: clamp(100px, 8vw, 130px);
  height: clamp(100px, 8vw, 130px);
  border-radius: 50%;
  border: 5px solid rgb(var(--v-theme-primary));
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgb(var(--v-theme-surface));
}

.progress-circle .text-h5 {
  font-size: clamp(1.8rem, 2vw, 2.5rem) !important;
  line-height: 1.2;
}

.progress-circle .text-caption {
  font-size: 1rem !important;
  margin-top: 4px;
}

.content-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.content-container {
  width: 100%;
  max-width: min(1200px, 95vw);
  display: flex;
  justify-content: center;
}

.task-stats {
  min-width: 320px;
  justify-content: center;
}

.stat-item {
  min-width: 120px;
}

.stat-item .text-h6 {
  font-size: 1.8rem !important;
  text-align: center;
  margin-top: 8px;
}

/* Image mode styles */
.resource-list {
  width: clamp(100px, 8vw, 120px);
  height: calc(100vh - 380px);
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.resource-grid {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  margin-top: -8px;
}

.resource-grid-item {
  width: 80px;
  height: 80px;
  cursor: pointer;
  border-radius: 4px;
  overflow: hidden;
  transition: border-color 0.2s ease;
  border: 2px solid transparent;
  flex-shrink: 0;
}

.resource-grid-item:hover {
  border-color: rgba(var(--v-theme-primary), 0.5);
}

.resource-grid-item.active {
  border-color: rgb(var(--v-theme-primary));
}

.preview-section {
  flex: 1;
  min-width: 0;
  max-width: min(800px, 60vw);
  margin: 0 12px;
}

.preview-box {
  position: relative;
  height: calc(100vh - 380px);
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  overflow: hidden;
}

.preview-box .v-img {
  max-width: 800px;
  max-height: 100%;
  object-fit: contain;
}

.preview-controls {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 0 16px;
}

.control-btn {
  opacity: 0.7;
  transition: opacity 0.2s ease !important;
}

.control-btn:hover {
  opacity: 1;
  transform: none;
}

.review-section {
  width: clamp(260px, 20vw, 300px);
  padding: 20px;
  background-color: rgb(var(--v-theme-surface));
  height: calc(100vh - 380px);
  overflow-y: auto;
  flex-shrink: 0;
  position: relative;
}

.review-header {
  position: sticky;
  top: 0;
  background-color: rgb(var(--v-theme-surface));
  z-index: 1;
  padding-bottom: 8px;
  margin-bottom: 8px;
}

.reviewer-item {
  position: relative;
  padding: 12px;
  border-radius: 8px;
  transition: all 0.2s ease;
  background-color: rgba(var(--v-theme-surface), 0.5);
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
}

.reviewer-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.details-btn {
  opacity: 0;
  transition: opacity 0.2s ease;
  white-space: nowrap;
}

.reviewer-item:hover .details-btn {
  opacity: 1;
}

.unprocessed-chip {
  background-color: rgba(244, 67, 54, 0.1) !important;
  color: rgb(244, 67, 54) !important;
}

.sent-chip {
  background-color: rgba(76, 175, 80, 0.1) !important;
  color: rgb(76, 175, 80) !important;
}

/* Text mode styles */
.text-sidebar {
  position: sticky;
  top: 0;
}

.text-sidebar-item {
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.text-sidebar-item:hover {
  border-color: rgba(var(--v-theme-primary), 0.3);
  background-color: rgba(var(--v-theme-primary), 0.05);
}

.text-sidebar-item-active {
  border-color: rgb(var(--v-theme-primary) ) !important;
  background-color: rgba(var(--v-theme-primary), 0.1) !important;
}

.cursor-pointer {
  cursor: pointer;
}

/* Multi mode styles */
.multi-sidebar-thumb {
  position: relative;
  width: 56px;
  height: 56px;
  cursor: pointer;
  border-radius: 4px;
  overflow: hidden;
  border: 2px solid transparent;
  transition: border-color 0.2s ease;
}

.multi-sidebar-thumb:hover {
  border-color: rgba(var(--v-theme-primary), 0.5);
}

.multi-sidebar-thumb.active {
  border-color: rgb(var(--v-theme-primary));
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.2);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.4);
}

/* Dialog transition */
.dialog-bottom-transition-enter-active,
.dialog-bottom-transition-leave-active {
  transition: transform 0.2s ease-in-out;
}

.dialog-bottom-transition-enter-from,
.dialog-bottom-transition-leave-to {
  transform: translateY(100%);
}

/* Responsive */
@media (max-width: 1280px) {
  .task-stats {
    min-width: clamp(280px, 25vw, 320px);
  }

  .stat-item {
    min-width: clamp(100px, 10vw, 120px);
  }

  .stat-item .text-h6 {
    font-size: clamp(1.4rem, 1.5vw, 1.8rem) !important;
  }
}

@media (max-width: 960px) {
  .content-container {
    flex-wrap: wrap;
    justify-content: flex-start;
  }

  .preview-section {
    max-width: 100%;
    order: -1;
  }

  .resource-list,
  .review-section {
    height: auto;
    min-height: 300px;
  }
}
</style>
