<template>
  <div class="task-detail pa-4">
    <!-- 返回按钮 -->
    <div class="d-flex align-center mb-6">
      <v-btn icon="mdi-arrow-left" variant="text" @click="router.back()" class="mr-2 return-btn">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <span class="text-h6 font-weight-medium">返回我的任务</span>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content rounded-lg">

      <!-- ==================== 图片审核模式 ==================== -->
      <template v-if="reviewMode === 'image'">
        <!-- 顶部信息区域 -->
        <div class="info-section pa-6">
          <div class="content-wrapper d-flex justify-center">
            <div class="content-container">
              <div class="info-content d-flex align-center justify-space-between pa-4">
                <!-- 左侧进度和标签 -->
                <div class="d-flex align-center" style="min-width: 320px; margin-left: 200px">
                  <div class="progress-circle mr-3 elevation-1">
                    <span class="text-h5 font-weight-bold primary--text">{{
                      formatNumber(overall?.confidence_score) }}</span>
                    <span class="text-caption">为假</span>
                  </div>
                  <v-card class="ml-4 pa-2 elevation-1" flat rounded="lg" width="250">
                    <v-card-title class="pa-2 pb-1 text-subtitle-2 font-weight-bold">AI 检测结果</v-card-title>
                    <v-card-text class="pa-2 pt-1">
                      <div v-for="(dimension, index) in detection_results" :key="index"
                        class="d-flex justify-space-between text-body-2 text-grey">
                        <span class="font-weight-medium">{{ convert(index) }}:</span>
                        <span class="text-primary">{{ dimension.probability.toFixed(2) }}</span>
                      </div>
                    </v-card-text>
                  </v-card>
                </div>

                <!-- 右侧任务信息 -->
                <div class="task-stats d-flex align-center">
                  <div class="answer-card">
                    <v-row align="center" justify="start">
                      <v-col class="d-flex" cols="auto">
                        <div class="text-h6 font-weight-medium mb-4">审核进度</div>
                      </v-col>
                      <v-col class="d-flex align-center ml-4" cols="auto">
                        <v-btn color="primary" @click="handleSubmit">
                          提交
                        </v-btn>
                      </v-col>
                    </v-row>
                    <div class="answer-grid">
                      <v-btn v-for="(image, index) in images" :key="index" :color="getAnswerButtonColor(index)"
                        variant="outlined" size="small" class="answer-btn" density="compact"
                        @click="handleImageSelect(index)">
                        {{ index + 1 }}
                      </v-btn>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <v-divider></v-divider>

        <div class="content-wrapper d-flex pa-2 justify-center">
          <div class="content-container d-flex" style="gap: 12px;">
            <!-- 图片列表 -->
            <div class="image-list rounded-lg elevation-1"
              style="background-color: rgb(var(--v-theme-surface)); padding: 20px;">
              <div class="text-h6 font-weight-medium text-center mb-4" style="white-space: nowrap;">图片列表</div>
              <div class="image-grid">
                <div v-for="(image, index) in images" :key="index" class="image-grid-item"
                  :class="{ 'active': currentImageIndex === index }" @click="handleImageSelect(index)">
                  <v-img v-if="image.url" :src="getImageUrl(image.url)" cover width="100%" height="100%" class="rounded-lg">
                    <template #error>
                      <div class="d-flex align-center justify-center fill-width fill-height bg-grey-lighten-2 rounded-lg">
                        <v-icon color="grey" size="24">mdi-image-broken-variant</v-icon>
                      </div>
                    </template>
                  </v-img>
                  <div v-else class="d-flex align-center justify-center fill-width fill-height bg-grey-lighten-2 rounded-lg">
                    <v-icon color="grey" size="24">mdi-image-off-outline</v-icon>
                  </div>
                </div>
              </div>
            </div>

            <!-- 图片预览区域 -->
            <div class="preview-section">
              <div class="preview-box">
                <v-img v-if="currentImage && currentImage.url" :src="getImageUrl(currentImage.url)" contain height="100%"
                  class="rounded-lg">
                  <template #error>
                    <div class="d-flex flex-column align-center justify-center fill-height">
                      <v-icon color="grey" size="64">mdi-image-broken-variant</v-icon>
                      <span class="text-caption text-grey mt-2">图片加载失败</span>
                    </div>
                  </template>
                </v-img>
                <div v-else-if="currentImage && !currentImage.url" class="d-flex flex-column align-center justify-center fill-height">
                  <v-icon color="grey" size="64">mdi-image-off-outline</v-icon>
                  <span class="text-caption text-grey mt-2">图片不可用</span>
                </div>
                <template v-for="(dimension, index) in dimensionsPerImage[currentImageIndex]" :key="index">
                  <canvas v-show="currentDrawingDimension === index"
                    :ref="el => { if (el) drawingCanvases[index] = el as HTMLCanvasElement }" class="drawing-canvas"
                    :class="{ 'active': currentDrawingDimension === index }"
                    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;">
                  </canvas>
                </template>
                <transition name="fade">
                  <v-img v-if="activeOverlay && isOverlayVisible" :src="activeOverlay"
                    class="rounded-lg overlay-image"></v-img>
                </transition>
                <div class="preview-controls">
                  <v-btn icon="mdi-chevron-left" variant="flat" @click="handlePrevImage"
                    :disabled="currentImageIndex <= 0" class="control-btn" color="black" size="x-large"></v-btn>
                  <v-btn icon="mdi-chevron-right" variant="flat" @click="handleNextImage"
                    :disabled="currentImageIndex >= images.length - 1" class="control-btn" color="black"
                    size="x-large"></v-btn>
                </div>
              </div>
            </div>

            <!-- 评分维度区域 -->
            <div class="dimension-section rounded-lg elevation-1">
              <div class="text-h6 font-weight-medium mb-4">评分维度</div>
              <div class="text-caption text-medium-emphasis mb-4">
                请根据图片特征，对每个造假方式进行可能性评估，分值越大表示相应维度造假可能性越大，必要时可使用绘制标注功能标记具体位置。
              </div>
              <div class="dimension-list">
                <div v-for="(dimension, index) in dimensionsPerImage[currentImageIndex]" :key="index"
                  class="dimension-item mb-6">
                  <div class="d-flex align-center justify-space-between mb-2">
                    <span class="text-subtitle-1">{{ dimension.name }}</span>
                    <div class="d-flex">
                      <v-btn size="small" color="primary" variant="tonal" @click="openDrawingDialog(index)" class="mr-2">
                        <v-icon size="small" icon="mdi-pencil" class="mr-1"></v-icon>
                        绘制标注
                      </v-btn>
                      <v-btn size="small" :color="urn[index]?.visible ? 'error' : 'grey'" variant="tonal"
                        @click="handleDisplayFake(urn[index])" class="fake-area-btn">
                        <v-icon size="small" :icon="urn[index]?.visible ? 'mdi-eye-off' : 'mdi-eye'"
                          class="mr-1"></v-icon>
                        {{ urn[index]?.visible ? '隐藏造假区域' : '显示造假区域' }}
                      </v-btn>
                    </div>
                  </div>
                  <div class="degree-buttons mb-2">
                    <v-btn-group variant="outlined" class="d-flex">
                      <v-btn v-for="option in degreeOptions" :key="option.value"
                        :color="dimension.value === option.value ? getDegreeColor(option.value) : 'grey'"
                        :variant="dimension.value === option.value ? 'flat' : 'outlined'" class="flex-grow-1"
                        @click="dimension.value = option.value" size="small">
                        {{ option.value }}
                      </v-btn>
                    </v-btn-group>
                  </div>
                  <v-text-field v-model="dimension.reason" :label="'请输入' + dimension.name + '的理由'" variant="outlined"
                    density="compact" hide-details class="mt-2"></v-text-field>
                </div>

                <div class="fake-judge-section mt-4 pt-4">
                  <div class="text-subtitle-1 mb-4">造假判定</div>
                  <div class="d-flex justify-space-between">
                    <v-btn :color="imageJudgements[currentImageIndex] === true ? 'error' : 'grey-lighten-1'"
                      variant="tonal" class="flex-grow-1 mr-2" @click="handleJudgement(true)">
                      造假图片
                    </v-btn>
                    <v-btn :color="imageJudgements[currentImageIndex] === false ? 'success' : 'grey-lighten-1'"
                      variant="tonal" class="flex-grow-1" @click="handleJudgement(false)">
                      真实图片
                    </v-btn>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- ==================== 文本审核模式 ==================== -->
      <template v-else-if="reviewMode === 'text'">
        <div class="pa-6">
          <v-row>
            <!-- 左侧：文本列表 -->
            <v-col cols="12" md="3">
              <v-card elevation="2" rounded="lg" class="text-sidebar">
                <v-card-title class="pa-4">
                  <v-icon class="mr-2">mdi-file-document-multiple</v-icon>
                  文本列表
                  <v-spacer></v-spacer>
                  <v-chip size="small" color="primary">{{ textResources.length }}</v-chip>
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-2" style="max-height: calc(100vh - 260px); overflow-y: auto;">
                  <div v-for="(text, index) in textResources" :key="text.id"
                    class="text-sidebar-item pa-3 mb-2 rounded-lg cursor-pointer"
                    :class="{ 'text-sidebar-item-active': currentTextIndex === index }"
                    @click="currentTextIndex = index">
                    <div class="d-flex align-center mb-1">
                      <v-chip size="x-small" :color="text.source_type === 'paste' ? 'info' : 'success'" class="mr-2">
                        {{ text.source_type === 'paste' ? '粘贴' : '文件' }}
                      </v-chip>
                      <span class="text-caption text-grey">ID: {{ text.id }}</span>
                    </div>
                    <div class="text-body-2 text-truncate">{{ text.raw_text?.substring(0, 60) }}...</div>
                    <div v-if="textReviews[index]?.result !== undefined && textReviews[index]?.result !== null"
                      class="mt-1">
                      <v-chip size="x-small" :color="textReviews[index].result ? 'error' : 'success'">
                        {{ textReviews[index].result ? '判定为假' : '判定为真' }}
                      </v-chip>
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </v-col>

            <!-- 中间：文本内容和审核 -->
            <v-col cols="12" md="6">
              <template v-if="currentTextResource">
                <!-- 文本内容 -->
                <v-card elevation="2" rounded="lg" class="mb-4">
                  <v-card-title class="pa-4 d-flex align-center">
                    <v-icon class="mr-2">mdi-text-box</v-icon>
                    文本内容
                    <v-spacer></v-spacer>
                    <v-btn size="small" variant="text" @click="toggleFullText">
                      {{ showFullText ? '收起' : '展开全文' }}
                    </v-btn>
                  </v-card-title>
                  <v-divider></v-divider>
                  <v-card-text class="pa-4" style="max-height: 300px; overflow-y: auto;">
                    <div class="text-body-2" style="white-space: pre-wrap; line-height: 1.8;">
                      {{ displayText }}
                    </div>
                  </v-card-text>
                </v-card>

                <!-- AI检测结果摘要 -->
                <v-card v-if="currentAiDetection" elevation="2" rounded="lg" class="mb-4">
                  <v-card-title class="pa-4">
                    <v-icon class="mr-2" color="primary">mdi-robot</v-icon>
                    AI 检测结果参考
                  </v-card-title>
                  <v-divider></v-divider>
                  <v-card-text class="pa-4">
                    <v-row class="mb-3">
                      <v-col cols="6">
                        <div class="text-body-2 text-grey mb-1">AI判定</div>
                        <v-chip :color="currentAiDetection.is_fake ? 'error' : 'success'" size="small">
                          {{ currentAiDetection.is_fake ? '疑似造假' : '可能真实' }}
                        </v-chip>
                      </v-col>
                      <v-col cols="6">
                        <div class="text-body-2 text-grey mb-1">置信度</div>
                        <span class="text-h6" :class="currentAiDetection.confidence_score > 0.7 ? 'error--text' : 'primary--text'">
                          {{ (currentAiDetection.confidence_score * 100).toFixed(1) }}%
                        </span>
                      </v-col>
                    </v-row>

                    <!-- 论文专属：AI生成段落 -->
                    <template v-if="currentAiDetection.ai_generated_paragraphs?.length > 0">
                      <div class="text-subtitle-2 mb-2">AI生成段落标记</div>
                      <div class="paragraph-review-list">
                        <div v-for="(para, pIdx) in currentAiDetection.ai_generated_paragraphs" :key="pIdx"
                          class="pa-2 mb-2 rounded" style="background: rgba(var(--v-theme-error), 0.05); border-left: 3px solid rgb(var(--v-theme-error));">
                          <div class="d-flex align-center mb-1">
                            <v-chip size="x-small" color="error" class="mr-2">段落 {{ para.paragraph_index }}</v-chip>
                            <span class="text-caption text-grey">AI概率: {{ (para.ai_probability * 100).toFixed(1) }}%</span>
                          </div>
                          <div class="text-caption" style="max-height: 60px; overflow: hidden;">{{ para.text?.substring(0, 150) }}...</div>
                          <div v-if="para.reason" class="text-caption text-grey mt-1">原因: {{ para.reason }}</div>
                        </div>
                      </div>
                    </template>

                    <!-- Review专属：模板化倾向 -->
                    <template v-if="currentAiDetection.template_tendency_score !== null && currentAiDetection.template_tendency_score !== undefined">
                      <div class="text-subtitle-2 mb-2">模板化倾向分析</div>
                      <v-progress-linear
                        :model-value="currentAiDetection.template_tendency_score * 100"
                        :color="currentAiDetection.template_tendency_score > 0.7 ? 'error' : currentAiDetection.template_tendency_score > 0.4 ? 'warning' : 'success'"
                        height="20"
                        class="mb-2"
                      >
                        <template #default="{ value }">
                          <span class="text-caption">{{ value.toFixed(0) }}%</span>
                        </template>
                      </v-progress-linear>
                      <div v-if="currentAiDetection.template_analysis_reason" class="text-body-2 text-grey mt-2">
                        {{ currentAiDetection.template_analysis_reason }}
                      </div>
                    </template>
                  </v-card-text>
                </v-card>

                <!-- 审核表单 -->
                <v-card elevation="2" rounded="lg" class="mb-4">
                  <v-card-title class="pa-4">
                    <v-icon class="mr-2" color="warning">mdi-pencil-box</v-icon>
                    人工审核
                  </v-card-title>
                  <v-divider></v-divider>
                  <v-card-text class="pa-4">
                    <!-- 论文类型：段落级别复核 -->
                    <template v-if="(currentAiDetection?.ai_generated_paragraphs?.length ?? 0) > 0">
                      <div class="text-subtitle-2 mb-3">段落复核</div>
                      <div class="text-caption text-grey mb-3">请对AI标记的每个段落进行复核，确认是否同意AI的判定。</div>
                      <div v-for="(para, pIdx) in currentAiDetection!.ai_generated_paragraphs" :key="'pr-' + pIdx"
                        class="pa-3 mb-3 rounded-lg" style="border: 1px solid rgba(var(--v-theme-primary), 0.2);">
                        <div class="d-flex align-center mb-2">
                          <v-chip size="small" color="primary" class="mr-2">段落 {{ para.paragraph_index }}</v-chip>
                          <span class="text-caption text-grey">AI概率: {{ (para.ai_probability * 100).toFixed(1) }}%</span>
                        </div>
                        <div class="text-body-2 mb-2" style="max-height: 80px; overflow: auto;">{{ para.text }}</div>
                        <v-row dense>
                          <v-col cols="12" sm="4">
                            <div class="text-caption text-grey mb-1">是否同意AI判定</div>
                            <v-btn-toggle v-model="getParagraphReview(pIdx).is_ai_agreed" mandatory density="compact">
                              <v-btn size="small" :value="true" color="error" variant="outlined">同意(AI生成)</v-btn>
                              <v-btn size="small" :value="false" color="success" variant="outlined">不同意</v-btn>
                            </v-btn-toggle>
                          </v-col>
                          <v-col cols="12" sm="8">
                            <v-textarea v-model="getParagraphReview(pIdx).comment"
                              :label="'段落 ' + para.paragraph_index + ' 复核意见'" variant="outlined" density="compact"
                              rows="2" hide-details class="mt-1"></v-textarea>
                          </v-col>
                        </v-row>
                      </div>
                    </template>

                    <!-- Review类型：模板化倾向复核 -->
                    <template v-if="currentAiDetection?.template_tendency_score !== null && currentAiDetection?.template_tendency_score !== undefined">
                      <div class="text-subtitle-2 mb-3 mt-4">模板化倾向复核</div>
                      <v-row dense>
                        <v-col cols="12" sm="6">
                          <div class="text-caption text-grey mb-1">您对模板化程度的评分 (0-100)</div>
                          <v-slider :model-value="currentTextReview.template_review_score ?? undefined" @update:model-value="currentTextReview.template_review_score = $event" :min="0" :max="100" step="1"
                            thumb-label color="primary" track-color="grey-lighten-2">
                            <template #append>
                              <v-text-field :model-value="currentTextReview.template_review_score ?? undefined" @update:model-value="currentTextReview.template_review_score = Number($event)" type="number" density="compact"
                                style="width: 70px" variant="outlined" hide-details></v-text-field>
                            </template>
                          </v-slider>
                        </v-col>
                        <v-col cols="12" sm="6">
                          <v-textarea v-model="currentTextReview.template_review_comment" label="模板化复核意见"
                            variant="outlined" density="compact" rows="3" hide-details></v-textarea>
                        </v-col>
                      </v-row>
                    </template>

                    <!-- 综合审核意见 -->
                    <div class="text-subtitle-2 mb-3 mt-4">综合审核意见</div>
                    <v-textarea v-model="currentTextReview.overall_comment" label="请输入您的综合审核意见"
                      variant="outlined" rows="4" class="mb-4"></v-textarea>

                    <!-- 最终判定 -->
                    <div class="text-subtitle-2 mb-3">最终判定</div>
                    <div class="d-flex">
                      <v-btn :color="currentTextReview.result === true ? 'error' : 'grey'" variant="tonal"
                        class="flex-grow-1 mr-2" size="large" @click="currentTextReview.result = true">
                        <v-icon class="mr-1">mdi-alert-circle</v-icon>
                        判定为假（AI生成/模板化）
                      </v-btn>
                      <v-btn :color="currentTextReview.result === false ? 'success' : 'grey'" variant="tonal"
                        class="flex-grow-1" size="large" @click="currentTextReview.result = false">
                        <v-icon class="mr-1">mdi-check-circle</v-icon>
                        判定为真（原创/非模板化）
                      </v-btn>
                    </div>
                  </v-card-text>
                </v-card>
              </template>
              <template v-else>
                <v-card elevation="2" rounded="lg">
                  <v-card-text class="text-center pa-8 text-grey">
                    请从左侧选择一个文本进行审核
                  </v-card-text>
                </v-card>
              </template>
            </v-col>

            <!-- 右侧：审核进度和提交 -->
            <v-col cols="12" md="3">
              <v-card elevation="2" rounded="lg" class="mb-4">
                <v-card-title class="pa-4">
                  <v-icon class="mr-2">mdi-clipboard-check</v-icon>
                  审核进度
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pa-4">
                  <div v-for="(text, index) in textResources" :key="'prog-' + text.id" class="d-flex align-center mb-2">
                    <v-icon :color="isTextReviewComplete(index) ? 'success' : 'grey'" class="mr-2" size="small">
                      {{ isTextReviewComplete(index) ? 'mdi-check-circle' : 'mdi-circle-outline' }}
                    </v-icon>
                    <span class="text-body-2" :class="isTextReviewComplete(index) ? 'success--text' : ''">
                      文本 {{ index + 1 }}
                    </span>
                  </div>
                  <v-divider class="my-3"></v-divider>
                  <div class="text-body-2 text-grey mb-3">
                    已完成 {{ textReviewCompleteCount }} / {{ textResources.length }}
                  </div>
                  <v-progress-linear :model-value="textReviewProgress" color="primary" height="8" rounded>
                  </v-progress-linear>
                </v-card-text>
              </v-card>

              <v-btn color="primary" block size="large" @click="handleSubmit" :disabled="textReviewProgress < 100">
                <v-icon class="mr-2">mdi-send</v-icon>
                提交审核结果
              </v-btn>
            </v-col>
          </v-row>
        </div>
      </template>

      <!-- ==================== 综合审核模式（图片+文本） ==================== -->
      <template v-else-if="reviewMode === 'multi'">
        <div class="pa-6">
          <!-- 标签页切换 -->
          <v-tabs v-model="multiTab" color="primary" class="mb-4">
            <v-tab value="images">
              <v-icon class="mr-2">mdi-image-multiple</v-icon>
              图片审核
              <v-chip size="x-small" class="ml-2" :color="imageJudgements.every(j => j !== null) ? 'success' : 'grey'">
                {{ imageJudgements.filter(j => j !== null).length }}/{{ images.length }}
              </v-chip>
            </v-tab>
            <v-tab value="texts">
              <v-icon class="mr-2">mdi-file-document-multiple</v-icon>
              文本审核
              <v-chip size="x-small" class="ml-2" :color="textReviewProgress >= 100 ? 'success' : 'grey'">
                {{ textReviewCompleteCount }}/{{ textResources.length }}
              </v-chip>
            </v-tab>
          </v-tabs>

          <v-tabs-window v-model="multiTab">
            <!-- 图片审核标签页 -->
            <v-tab-item value="images">
              <div class="content-wrapper d-flex pa-2 justify-center">
                <div class="content-container d-flex" style="gap: 12px;">
                  <!-- 图片列表 -->
                  <div class="image-list rounded-lg elevation-1"
                    style="background-color: rgb(var(--v-theme-surface)); padding: 20px;">
                    <div class="text-h6 font-weight-medium text-center mb-4" style="white-space: nowrap;">图片列表</div>
                    <div class="image-grid">
                      <div v-for="(image, index) in images" :key="'m-img-' + index" class="image-grid-item"
                        :class="{ 'active': currentImageIndex === index }" @click="handleImageSelect(index)">
                        <v-img :src="getImageUrl(image.url)" cover width="100%" height="100%" class="rounded-lg"></v-img>
                      </div>
                    </div>
                  </div>

                  <!-- 图片预览区域 -->
                  <div class="preview-section">
                    <div class="preview-box">
                      <v-img v-if="currentImage" :src="getImageUrl(currentImage.url)" contain height="100%"
                        class="rounded-lg"></v-img>
                      <template v-for="(dimension, index) in dimensionsPerImage[currentImageIndex]" :key="'m-canvas-' + index">
                        <canvas v-show="currentDrawingDimension === index"
                          :ref="el => { if (el) drawingCanvases[index] = el as HTMLCanvasElement }" class="drawing-canvas"
                          :class="{ 'active': currentDrawingDimension === index }"
                          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;">
                        </canvas>
                      </template>
                      <transition name="fade">
                        <v-img v-if="activeOverlay && isOverlayVisible" :src="activeOverlay"
                          class="rounded-lg overlay-image"></v-img>
                      </transition>
                      <div class="preview-controls">
                        <v-btn icon="mdi-chevron-left" variant="flat" @click="handlePrevImage"
                          :disabled="currentImageIndex <= 0" class="control-btn" color="black" size="x-large"></v-btn>
                        <v-btn icon="mdi-chevron-right" variant="flat" @click="handleNextImage"
                          :disabled="currentImageIndex >= images.length - 1" class="control-btn" color="black"
                          size="x-large"></v-btn>
                      </div>
                    </div>
                  </div>

                  <!-- 评分维度区域 -->
                  <div class="dimension-section rounded-lg elevation-1">
                    <div class="text-h6 font-weight-medium mb-4">评分维度</div>
                    <div class="text-caption text-medium-emphasis mb-4">
                      请根据图片特征，对每个造假方式进行可能性评估。
                    </div>
                    <div class="dimension-list">
                      <div v-for="(dimension, index) in dimensionsPerImage[currentImageIndex]" :key="'m-dim-' + index"
                        class="dimension-item mb-6">
                        <div class="d-flex align-center justify-space-between mb-2">
                          <span class="text-subtitle-1">{{ dimension.name }}</span>
                          <div class="d-flex">
                            <v-btn size="small" color="primary" variant="tonal" @click="openDrawingDialog(index)" class="mr-2">
                              <v-icon size="small" icon="mdi-pencil" class="mr-1"></v-icon>
                              绘制标注
                            </v-btn>
                            <v-btn size="small" :color="urn[index]?.visible ? 'error' : 'grey'" variant="tonal"
                              @click="handleDisplayFake(urn[index])" class="fake-area-btn">
                              <v-icon size="small" :icon="urn[index]?.visible ? 'mdi-eye-off' : 'mdi-eye'"
                                class="mr-1"></v-icon>
                              {{ urn[index]?.visible ? '隐藏' : '显示' }}
                            </v-btn>
                          </div>
                        </div>
                        <div class="degree-buttons mb-2">
                          <v-btn-group variant="outlined" class="d-flex">
                            <v-btn v-for="option in degreeOptions" :key="option.value"
                              :color="dimension.value === option.value ? getDegreeColor(option.value) : 'grey'"
                              :variant="dimension.value === option.value ? 'flat' : 'outlined'" class="flex-grow-1"
                              @click="dimension.value = option.value" size="small">
                              {{ option.value }}
                            </v-btn>
                          </v-btn-group>
                        </div>
                        <v-text-field v-model="dimension.reason" :label="'请输入' + dimension.name + '的理由'" variant="outlined"
                          density="compact" hide-details class="mt-2"></v-text-field>
                      </div>

                      <div class="fake-judge-section mt-4 pt-4">
                        <div class="text-subtitle-1 mb-4">造假判定</div>
                        <div class="d-flex justify-space-between">
                          <v-btn :color="imageJudgements[currentImageIndex] === true ? 'error' : 'grey-lighten-1'"
                            variant="tonal" class="flex-grow-1 mr-2" @click="handleJudgement(true)">
                            造假图片
                          </v-btn>
                          <v-btn :color="imageJudgements[currentImageIndex] === false ? 'success' : 'grey-lighten-1'"
                            variant="tonal" class="flex-grow-1" @click="handleJudgement(false)">
                            真实图片
                          </v-btn>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </v-tab-item>

            <!-- 文本审核标签页 -->
            <v-tab-item value="texts">
              <v-row>
                <!-- 左侧：文本列表 -->
                <v-col cols="12" md="3">
                  <v-card elevation="2" rounded="lg" class="text-sidebar">
                    <v-card-title class="pa-4">
                      <v-icon class="mr-2">mdi-file-document-multiple</v-icon>
                      文本列表
                      <v-spacer></v-spacer>
                      <v-chip size="small" color="primary">{{ textResources.length }}</v-chip>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="pa-2" style="max-height: calc(100vh - 300px); overflow-y: auto;">
                      <div v-for="(text, index) in textResources" :key="'m-text-' + text.id"
                        class="text-sidebar-item pa-3 mb-2 rounded-lg cursor-pointer"
                        :class="{ 'text-sidebar-item-active': currentTextIndex === index }"
                        @click="currentTextIndex = index">
                        <div class="d-flex align-center mb-1">
                          <v-chip size="x-small" :color="text.source_type === 'paste' ? 'info' : 'success'" class="mr-2">
                            {{ text.source_type === 'paste' ? '粘贴' : '文件' }}
                          </v-chip>
                          <span class="text-caption text-grey">ID: {{ text.id }}</span>
                        </div>
                        <div class="text-body-2 text-truncate">{{ text.raw_text?.substring(0, 60) }}...</div>
                        <div v-if="textReviews[index]?.result !== undefined && textReviews[index]?.result !== null"
                          class="mt-1">
                          <v-chip size="x-small" :color="textReviews[index].result ? 'error' : 'success'">
                            {{ textReviews[index].result ? '判定为假' : '判定为真' }}
                          </v-chip>
                        </div>
                      </div>
                    </v-card-text>
                  </v-card>
                </v-col>

                <!-- 中间：文本内容和审核 -->
                <v-col cols="12" md="6">
                  <template v-if="currentTextResource">
                    <!-- 文本内容 -->
                    <v-card elevation="2" rounded="lg" class="mb-4">
                      <v-card-title class="pa-4 d-flex align-center">
                        <v-icon class="mr-2">mdi-text-box</v-icon>
                        文本内容
                        <v-spacer></v-spacer>
                        <v-btn size="small" variant="text" @click="toggleFullText">
                          {{ showFullText ? '收起' : '展开全文' }}
                        </v-btn>
                      </v-card-title>
                      <v-divider></v-divider>
                      <v-card-text class="pa-4" style="max-height: 300px; overflow-y: auto;">
                        <div class="text-body-2" style="white-space: pre-wrap; line-height: 1.8;">
                          {{ displayText }}
                        </div>
                      </v-card-text>
                    </v-card>

                    <!-- AI检测结果摘要 -->
                    <v-card v-if="currentAiDetection" elevation="2" rounded="lg" class="mb-4">
                      <v-card-title class="pa-4">
                        <v-icon class="mr-2" color="primary">mdi-robot</v-icon>
                        AI 检测结果参考
                      </v-card-title>
                      <v-divider></v-divider>
                      <v-card-text class="pa-4">
                        <v-row class="mb-3">
                          <v-col cols="6">
                            <div class="text-body-2 text-grey mb-1">AI判定</div>
                            <v-chip :color="currentAiDetection.is_fake ? 'error' : 'success'" size="small">
                              {{ currentAiDetection.is_fake ? '疑似造假' : '可能真实' }}
                            </v-chip>
                          </v-col>
                          <v-col cols="6">
                            <div class="text-body-2 text-grey mb-1">置信度</div>
                            <span class="text-h6" :class="currentAiDetection.confidence_score > 0.7 ? 'error--text' : 'primary--text'">
                              {{ (currentAiDetection.confidence_score * 100).toFixed(1) }}%
                            </span>
                          </v-col>
                        </v-row>

                        <!-- 论文专属：AI生成段落 -->
                        <template v-if="currentAiDetection.ai_generated_paragraphs?.length > 0">
                          <div class="text-subtitle-2 mb-2">AI生成段落标记</div>
                          <div class="paragraph-review-list">
                            <div v-for="(para, pIdx) in currentAiDetection.ai_generated_paragraphs" :key="'m-aip-' + pIdx"
                              class="pa-2 mb-2 rounded" style="background: rgba(var(--v-theme-error), 0.05); border-left: 3px solid rgb(var(--v-theme-error));">
                              <div class="d-flex align-center mb-1">
                                <v-chip size="x-small" color="error" class="mr-2">段落 {{ para.paragraph_index }}</v-chip>
                                <span class="text-caption text-grey">AI概率: {{ (para.ai_probability * 100).toFixed(1) }}%</span>
                              </div>
                              <div class="text-caption" style="max-height: 60px; overflow: hidden;">{{ para.text?.substring(0, 150) }}...</div>
                              <div v-if="para.reason" class="text-caption text-grey mt-1">原因: {{ para.reason }}</div>
                            </div>
                          </div>
                        </template>

                        <!-- Review专属：模板化倾向 -->
                        <template v-if="currentAiDetection.template_tendency_score !== null && currentAiDetection.template_tendency_score !== undefined">
                          <div class="text-subtitle-2 mb-2">模板化倾向分析</div>
                          <v-progress-linear
                            :model-value="currentAiDetection.template_tendency_score * 100"
                            :color="currentAiDetection.template_tendency_score > 0.7 ? 'error' : currentAiDetection.template_tendency_score > 0.4 ? 'warning' : 'success'"
                            height="20"
                            class="mb-2"
                          >
                            <template #default="{ value }">
                              <span class="text-caption">{{ value.toFixed(0) }}%</span>
                            </template>
                          </v-progress-linear>
                          <div v-if="currentAiDetection.template_analysis_reason" class="text-body-2 text-grey mt-2">
                            {{ currentAiDetection.template_analysis_reason }}
                          </div>
                        </template>
                      </v-card-text>
                    </v-card>

                    <!-- 审核表单 -->
                    <v-card elevation="2" rounded="lg" class="mb-4">
                      <v-card-title class="pa-4">
                        <v-icon class="mr-2" color="warning">mdi-pencil-box</v-icon>
                        人工审核
                      </v-card-title>
                      <v-divider></v-divider>
                      <v-card-text class="pa-4">
                        <!-- 论文类型：段落级别复核 -->
                        <template v-if="(currentAiDetection?.ai_generated_paragraphs?.length ?? 0) > 0">
                          <div class="text-subtitle-2 mb-3">段落复核</div>
                          <div class="text-caption text-grey mb-3">请对AI标记的每个段落进行复核。</div>
                          <div v-for="(para, pIdx) in currentAiDetection!.ai_generated_paragraphs" :key="'m-pr-' + pIdx"
                            class="pa-3 mb-3 rounded-lg" style="border: 1px solid rgba(var(--v-theme-primary), 0.2);">
                            <div class="d-flex align-center mb-2">
                              <v-chip size="small" color="primary" class="mr-2">段落 {{ para.paragraph_index }}</v-chip>
                              <span class="text-caption text-grey">AI概率: {{ (para.ai_probability * 100).toFixed(1) }}%</span>
                            </div>
                            <div class="text-body-2 mb-2" style="max-height: 80px; overflow: auto;">{{ para.text }}</div>
                            <v-row dense>
                              <v-col cols="12" sm="4">
                                <div class="text-caption text-grey mb-1">是否同意AI判定</div>
                                <v-btn-toggle v-model="getParagraphReview(pIdx).is_ai_agreed" mandatory density="compact">
                                  <v-btn size="small" :value="true" color="error" variant="outlined">同意(AI生成)</v-btn>
                                  <v-btn size="small" :value="false" color="success" variant="outlined">不同意</v-btn>
                                </v-btn-toggle>
                              </v-col>
                              <v-col cols="12" sm="8">
                                <v-textarea v-model="getParagraphReview(pIdx).comment"
                                  :label="'段落 ' + para.paragraph_index + ' 复核意见'" variant="outlined" density="compact"
                                  rows="2" hide-details class="mt-1"></v-textarea>
                              </v-col>
                            </v-row>
                          </div>
                        </template>

                        <!-- Review类型：模板化倾向复核 -->
                        <template v-if="currentAiDetection?.template_tendency_score !== null && currentAiDetection?.template_tendency_score !== undefined">
                          <div class="text-subtitle-2 mb-3 mt-4">模板化倾向复核</div>
                          <v-row dense>
                            <v-col cols="12" sm="6">
                              <div class="text-caption text-grey mb-1">您对模板化程度的评分 (0-100)</div>
                              <v-slider :model-value="currentTextReview.template_review_score ?? undefined" @update:model-value="currentTextReview.template_review_score = $event" :min="0" :max="100" step="1"
                                thumb-label color="primary" track-color="grey-lighten-2">
                                <template #append>
                                  <v-text-field :model-value="currentTextReview.template_review_score ?? undefined" @update:model-value="currentTextReview.template_review_score = Number($event)" type="number" density="compact"
                                    style="width: 70px" variant="outlined" hide-details></v-text-field>
                                </template>
                              </v-slider>
                            </v-col>
                            <v-col cols="12" sm="6">
                              <v-textarea v-model="currentTextReview.template_review_comment" label="模板化复核意见"
                                variant="outlined" density="compact" rows="3" hide-details></v-textarea>
                            </v-col>
                          </v-row>
                        </template>

                        <!-- 综合审核意见 -->
                        <div class="text-subtitle-2 mb-3 mt-4">综合审核意见</div>
                        <v-textarea v-model="currentTextReview.overall_comment" label="请输入您的综合审核意见"
                          variant="outlined" rows="4" class="mb-4"></v-textarea>

                        <!-- 最终判定 -->
                        <div class="text-subtitle-2 mb-3">最终判定</div>
                        <div class="d-flex">
                          <v-btn :color="currentTextReview.result === true ? 'error' : 'grey'" variant="tonal"
                            class="flex-grow-1 mr-2" size="large" @click="currentTextReview.result = true">
                            <v-icon class="mr-1">mdi-alert-circle</v-icon>
                            判定为假
                          </v-btn>
                          <v-btn :color="currentTextReview.result === false ? 'success' : 'grey'" variant="tonal"
                            class="flex-grow-1" size="large" @click="currentTextReview.result = false">
                            <v-icon class="mr-1">mdi-check-circle</v-icon>
                            判定为真
                          </v-btn>
                        </div>
                      </v-card-text>
                    </v-card>
                  </template>
                  <template v-else>
                    <v-card elevation="2" rounded="lg">
                      <v-card-text class="text-center pa-8 text-grey">
                        请从左侧选择一个文本进行审核
                      </v-card-text>
                    </v-card>
                  </template>
                </v-col>

                <!-- 右侧：审核进度和提交 -->
                <v-col cols="12" md="3">
                  <v-card elevation="2" rounded="lg" class="mb-4">
                    <v-card-title class="pa-4">
                      <v-icon class="mr-2">mdi-clipboard-check</v-icon>
                      审核进度
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-card-text class="pa-4">
                      <div class="text-subtitle-2 mb-2">图片</div>
                      <div v-for="(img, index) in images" :key="'m-prog-img-' + index" class="d-flex align-center mb-1">
                        <v-icon :color="imageJudgements[index] !== null ? 'success' : 'grey'" class="mr-2" size="small">
                          {{ imageJudgements[index] !== null ? 'mdi-check-circle' : 'mdi-circle-outline' }}
                        </v-icon>
                        <span class="text-body-2">图片 {{ index + 1 }}</span>
                      </div>
                      <v-divider class="my-3"></v-divider>
                      <div class="text-subtitle-2 mb-2">文本</div>
                      <div v-for="(text, index) in textResources" :key="'m-prog-text-' + text.id" class="d-flex align-center mb-2">
                        <v-icon :color="isTextReviewComplete(index) ? 'success' : 'grey'" class="mr-2" size="small">
                          {{ isTextReviewComplete(index) ? 'mdi-check-circle' : 'mdi-circle-outline' }}
                        </v-icon>
                        <span class="text-body-2" :class="isTextReviewComplete(index) ? 'success--text' : ''">
                          文本 {{ index + 1 }}
                        </span>
                      </div>
                    </v-card-text>
                  </v-card>

                  <v-btn color="primary" block size="large" @click="handleSubmit"
                    :disabled="imageJudgements.some(j => j === null) || textReviewProgress < 100">
                    <v-icon class="mr-2">mdi-send</v-icon>
                    提交全部审核结果
                  </v-btn>
                </v-col>
              </v-row>
            </v-tab-item>
          </v-tabs-window>
        </div>
      </template>

      <!-- ==================== 加载中 ==================== -->
      <template v-else-if="reviewMode === 'loading'">
        <div class="d-flex justify-center align-center" style="min-height: 60vh;">
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        </div>
      </template>

      <!-- ==================== 空状态 ==================== -->
      <template v-else>
        <div class="d-flex flex-column justify-center align-center" style="min-height: 60vh;">
          <v-icon size="64" color="grey">mdi-help-circle-outline</v-icon>
          <div class="text-h6 text-grey mt-4">无法加载审核任务</div>
        </div>
      </template>
    </div>

    <!-- 提示对话框 -->
    <v-dialog v-model="showAlert" max-width="400">
      <v-card>
        <v-card-text class="pa-4">
          <div class="text-center">{{ alertMessage }}</div>
        </v-card-text>
        <v-card-actions class="justify-center pb-4">
          <v-btn color="primary" variant="text" @click="showAlert = false">
            确定
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 绘制弹窗（仅图片模式） -->
    <DrawingDialog v-if="reviewMode === 'image' || reviewMode === 'multi'" v-model="showDrawingDialog"
      :image-url="currentImage ? getImageUrl(currentImage.url) : ''" :initial-paths="currentDimensionPaths"
      @save="handleDrawingSave" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import reviewer from '@/api/reviewer'
import type { RouteParams } from 'vue-router'
import { useSnackbarStore } from '@/stores/snackbar'
import DrawingDialog from '@/components/DrawingDialog.vue'
import publisher from '@/api/publisher'
import { resolveImageUrl } from '@/utils/preview-url'

const router = useRouter()
const snackbar = useSnackbarStore()
const route = useRoute()

// ==================== 通用 ====================
const manual_review_id = computed(() => (route.params as RouteParams & { manual_review_id: number }).manual_review_id)
const showAlert = ref(false)
const alertMessage = ref('')
const reviewMode = ref<'image' | 'text' | 'multi' | 'loading' | 'empty'>('loading')
const multiTab = ref<'images' | 'texts'>('images')

// ==================== 图片审核相关 ====================
interface Image {
  id: number,
  url: string
}

interface SubMethod {
  method: string
  probability: number
  mask_image: string
  mask_matrix: any | null
  visible: boolean
}

interface Dimension {
  name: string;
  value: number | null;
  reason: string;
  showFakeArea: boolean;
  drawingPaths: Array<{
    points: Array<{ x: number, y: number }>;
    color: string;
  }>;
}

interface dimension {
  method: string,
  probability: number
}

const currentImageIndex = ref(0)
const images = ref<Image[]>([])
const imageJudgements = ref<(boolean | null)[]>([])
const dimensionsPerImage = ref<Dimension[][]>([])
const urn = ref<SubMethod[]>([])
const activeOverlay = ref()
const isOverlayVisible = ref(false)
const overall = ref()
const detection_results = ref<dimension[]>([])

const drawingCanvases = ref<HTMLCanvasElement[]>([])
const imageRect = ref<DOMRect | null>(null)
const currentDrawingDimension = ref<number>(-1)
const showDrawingDialog = ref(false)

const degreeOptions = [
  { value: 1, label: '轻微' },
  { value: 2, label: '一般' },
  { value: 3, label: '中等' },
  { value: 4, label: '明显' },
  { value: 5, label: '严重' }
]

const convert = (index: number) => {
  switch (index) {
    case 0: return '高斯模糊'
    case 1: return '亮度/对比度调节'
    case 2: return '智能修复'
    case 3: return '暴力覆盖'
    case 4: return '同图复制'
    case 5: return '重叠切割'
    case 6: return '跨图拼接'
    default: return ''
  }
}

const formatNumber = (result: number) => {
  return `${(result * 100).toFixed(2)}%`
}

const getImageUrl = (url: string) => {
  return resolveImageUrl(url)
}

const fetchDetectionResults = async () => {
  try {
    const id = (await publisher.getDetectionID({ img_id: currentImage.value?.id })).data.detection_result_id
    const response = (await publisher.getSingleImageResult(id)).data
    detection_results.value = response.sub_methods
  } catch (error) {
    snackbar.showMessage('获取检测结果失败', 'error')
  }
}

const currentImage = computed(() => {
  if (
    Array.isArray(images.value) &&
    typeof currentImageIndex.value === 'number' &&
    currentImageIndex.value >= 0 &&
    currentImageIndex.value < images.value.length
  ) {
    return images.value[currentImageIndex.value];
  }
  return null;
});

const fetchMaskImage = async () => {
  try {
    const res = (await reviewer.getMaskImage({ img_id: currentImage.value?.id })).data
    urn.value = res.sub_methods.map((item: Omit<SubMethod, 'visible'>) => ({
      ...item,
      visible: false
    }))
    overall.value = res.overall
  } catch (error) {
    snackbar.showMessage('获取mask失败', 'error')
  }
}

const handleDisplayFake = (dimension: SubMethod) => {
  if (dimension.visible) {
    dimension.visible = false
    isOverlayVisible.value = false
    activeOverlay.value = null
    return
  }
  urn.value.forEach(d => {
    if (d !== dimension) d.visible = false
  })
  dimension.visible = true
  isOverlayVisible.value = true
  activeOverlay.value = resolveImageUrl(dimension.mask_image)
}

const handleImageSelect = (index: number) => {
  currentImageIndex.value = index
  currentDrawingDimension.value = -1
  fetchMaskImage()
  fetchDetectionResults()
}

const handlePrevImage = () => {
  if (currentImageIndex.value > 0) currentImageIndex.value--
}

const handleNextImage = () => {
  if (currentImageIndex.value < images.value.length - 1) currentImageIndex.value++
}

const currentDimensionPaths = computed(() => {
  if (currentDrawingDimension.value === -1) return []
  const currentImg = dimensionsPerImage.value[currentImageIndex.value]
  if (!currentImg) return []
  const currentDim = currentImg[currentDrawingDimension.value]
  return currentDim?.drawingPaths || []
})

const openDrawingDialog = (index: number) => {
  currentDrawingDimension.value = index
  showDrawingDialog.value = true
}

const handleDrawingSave = (paths: Array<{ points: Array<{ x: number; y: number }>; color: string }>) => {
  if (currentDrawingDimension.value === -1) return
  const currentImg = dimensionsPerImage.value[currentImageIndex.value]
  if (!currentImg) return
  currentImg[currentDrawingDimension.value].drawingPaths = [...paths]
}

const getDegreeColor = (value: number) => {
  switch (value) {
    case 1: return 'success'
    case 2: return 'info'
    case 3: return 'yellow'
    case 4: return 'warning'
    case 5: return 'error'
    default: return 'grey'
  }
}

const handleJudgement = (isFake: boolean) => {
  imageJudgements.value[currentImageIndex.value] = isFake
}

const getAnswerButtonColor = (index: number) => {
  if (index === currentImageIndex.value) return 'primary'
  const judgement = imageJudgements.value[index]
  if (judgement === null) return 'grey'
  return judgement ? 'error' : 'success'
}

// 图片提交验证
const checkImageAnswerCompletion = () => {
  for (let i = 0; i < images.value.length; i++) {
    if (imageJudgements.value[i] === null) {
      return { complete: false, message: `第 ${i + 1} 张图片尚未进行造假判定` }
    }
  }
  for (let i = 0; i < dimensionsPerImage.value.length; i++) {
    const dims = dimensionsPerImage.value[i]
    if (dims.some(dim => dim.value === null)) {
      return { complete: false, message: `第 ${i + 1} 张图片的评分维度尚未评分完整` }
    }
    if (dims.some(dim => !dim.reason)) {
      return { complete: false, message: `第 ${i + 1} 张图片的评分维度理由尚未填写完整` }
    }
  }
  return { complete: true, message: '所有图片已完成评分' }
}

interface ImageItem {
  img_id: number
  score: Array<number | null>
  reason: Array<string | null>
  final: boolean | null
  points: Array<Array<{}>>
}

const constructImageData = () => {
  const data = { result: [] as ImageItem[], text_reviews: [] as any[] }
  for (let i = 0; i < images.value.length; i++) {
    data.result.push({
      img_id: images.value[i].id,
      score: dimensionsPerImage.value[i].map(dim => dim.value),
      reason: dimensionsPerImage.value[i].map(dim => dim.reason),
      final: imageJudgements.value[i],
      points: dimensionsPerImage.value[i].map(dim => dim.drawingPaths)
    })
  }
  return data
}

// ==================== 文本审核相关 ====================
interface TextResource {
  id: number
  raw_text: string
  source_type: string
  ai_detection?: {
    is_fake: boolean
    confidence_score: number
    ai_generated_paragraphs: any[]
    factual_fake_reason: string
    template_tendency_score: number | null
    template_analysis_reason: string
  } | null
}

interface TextReviewItem {
  text_id: number
  paragraph_reviews: any[] | null
  template_review_score: number | null
  template_review_comment: string
  overall_comment: string
  result: boolean | null
}

const textResources = ref<TextResource[]>([])
const textReviews = ref<TextReviewItem[]>([])
const currentTextIndex = ref(0)
const showFullText = ref(false)

const currentTextResource = computed(() => {
  if (currentTextIndex.value >= 0 && currentTextIndex.value < textResources.value.length) {
    return textResources.value[currentTextIndex.value]
  }
  return null
})

const currentAiDetection = computed(() => {
  return currentTextResource.value?.ai_detection || null
})

const currentTextReview = computed(() => {
  if (currentTextIndex.value >= 0 && currentTextIndex.value < textReviews.value.length) {
    return textReviews.value[currentTextIndex.value]
  }
  return { text_id: 0, paragraph_reviews: null, template_review_score: null, template_review_comment: '', overall_comment: '', result: null }
})

const displayText = computed(() => {
  if (!currentTextResource.value?.raw_text) return ''
  if (showFullText.value) return currentTextResource.value.raw_text
  return currentTextResource.value.raw_text.substring(0, 500) + '...'
})

const toggleFullText = () => {
  showFullText.value = !showFullText.value
}

// 段落复核辅助方法
const getParagraphReview = (pIdx: number) => {
  const review = textReviews.value[currentTextIndex.value]
  if (!review) return { is_ai_agreed: null, comment: '' }

  if (!review.paragraph_reviews) {
    review.paragraph_reviews = []
  }
  while (review.paragraph_reviews.length <= pIdx) {
    // Use the actual paragraph_index from AI detection if available
    const aiParas = currentAiDetection.value?.ai_generated_paragraphs
    const originalIndex = aiParas?.[pIdx]?.paragraph_index ?? (pIdx + 1)
    review.paragraph_reviews.push({ paragraph_index: originalIndex, is_ai_agreed: null, comment: '' })
  }

  return review.paragraph_reviews[pIdx]
}

const isTextReviewComplete = (index: number) => {
  const review = textReviews.value[index]
  if (!review) return false
  return review.result !== null && review.result !== undefined && review.overall_comment.trim() !== ''
}

const textReviewCompleteCount = computed(() => {
  return textReviews.value.filter(r => r.result !== null && r.result !== undefined && r.overall_comment.trim() !== '').length
})

const textReviewProgress = computed(() => {
  if (textResources.value.length === 0) return 0
  return (textReviewCompleteCount.value / textResources.value.length) * 100
})

const constructTextData = () => {
  return {
    result: [],
    text_reviews: textReviews.value.map((review, index) => {
      // Ensure template_review_score is a number 0-1 (slider is 0-100)
      let normalizedTemplateScore = null
      if (review.template_review_score !== null && review.template_review_score !== undefined) {
        const raw = Number(review.template_review_score)
        if (!isNaN(raw)) {
          normalizedTemplateScore = Math.min(1, Math.max(0, raw / 100))
        }
      }
      return {
        text_id: textResources.value[index].id,
        paragraph_reviews: review.paragraph_reviews,
        template_review_score: normalizedTemplateScore,
        template_review_comment: review.template_review_comment || '',
        overall_comment: review.overall_comment || '',
        result: review.result
      }
    })
  }
}

// ==================== 文本审核验证 ====================
const validateTextReviews = (): { valid: boolean; message: string } => {
  if (textResources.value.length === 0) return { valid: true, message: '' }
  const incomplete = textReviews.value.findIndex(r => r.result === null || r.result === undefined)
  if (incomplete >= 0) {
    return { valid: false, message: `第 ${incomplete + 1} 个文本尚未完成审核判定` }
  }
  const noComment = textReviews.value.findIndex(r => !r.overall_comment?.trim())
  if (noComment >= 0) {
    return { valid: false, message: `第 ${noComment + 1} 个文本尚未填写综合审核意见` }
  }
  return { valid: true, message: '' }
}

// ==================== 通用提交 ====================
const handleSubmit = async () => {
  if (reviewMode.value === 'image') {
    const result = checkImageAnswerCompletion()
    if (!result.complete) {
      snackbar.showMessage(result.message, 'error')
      return
    }
    try {
      await reviewer.submitReview(manual_review_id.value as any, constructImageData())
      snackbar.showMessage('提交成功', 'success')
      router.push('/review')
    } catch (error) {
      snackbar.showMessage('提交失败', 'error')
    }
  } else if (reviewMode.value === 'text') {
    const validation = validateTextReviews()
    if (!validation.valid) {
      snackbar.showMessage(validation.message, 'error')
      return
    }
    try {
      await reviewer.submitReview(manual_review_id.value as any, constructTextData())
      snackbar.showMessage('提交成功', 'success')
      router.push('/review')
    } catch (error) {
      snackbar.showMessage('提交失败', 'error')
    }
  } else if (reviewMode.value === 'multi') {
    // Multi-material mode: validate both image and text
    const imgResult = checkImageAnswerCompletion()
    if (!imgResult.complete) {
      snackbar.showMessage(imgResult.message, 'error')
      return
    }
    const txtResult = validateTextReviews()
    if (!txtResult.valid) {
      snackbar.showMessage(txtResult.message, 'error')
      return
    }
    try {
      // Merge image and text data into one submission
      const imgData = constructImageData()
      const txtData = constructTextData()
      const mergedData = {
        result: imgData.result,
        text_reviews: txtData.text_reviews
      }
      await reviewer.submitReview(manual_review_id.value as any, mergedData)
      snackbar.showMessage('提交成功', 'success')
      router.push('/review')
    } catch (error) {
      snackbar.showMessage('提交失败', 'error')
    }
  }
}

// ==================== 初始化文本审核数据 ====================
const initTextReviewData = (texts: TextResource[]) => {
  textResources.value = texts
  textReviews.value = texts.map((t: TextResource) => ({
    text_id: t.id,
    paragraph_reviews: null,
    template_review_score: t.ai_detection?.template_tendency_score !== null && t.ai_detection?.template_tendency_score !== undefined
      ? Math.round((t.ai_detection.template_tendency_score) * 100) : null,
    template_review_comment: '',
    overall_comment: '',
    result: null
  }))
}

// ==================== 初始化加载 ====================
onMounted(async () => {
  try {
    const response = (await reviewer.getReviewTaskDetail({ manual_review_id: manual_review_id.value })).data
    const imgs = response.imgs || []
    const texts = response.texts || []

    if (imgs.length > 0 && texts.length > 0) {
      // 综合审核模式（图片+文本）
      reviewMode.value = 'multi'
      images.value = imgs
      imageJudgements.value = new Array(imgs.length).fill(null)
      dimensionsPerImage.value = imgs.map(() => [
        { name: '高斯模糊', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
        { name: '亮度/对比度调节', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
        { name: '智能修复', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
        { name: '暴力覆盖', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
        { name: '同图复制', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
        { name: '重叠切割', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
        { name: '跨图拼接', value: null, reason: '', showFakeArea: false, drawingPaths: [] }
      ])
      initTextReviewData(texts)
      fetchMaskImage()
      fetchDetectionResults()
    } else if (imgs.length > 0) {
      // 图片审核模式
      reviewMode.value = 'image'
      images.value = imgs
      imageJudgements.value = new Array(imgs.length).fill(null)
      dimensionsPerImage.value = imgs.map(() => [
        { name: '高斯模糊', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
        { name: '亮度/对比度调节', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
        { name: '智能修复', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
        { name: '暴力覆盖', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
        { name: '同图复制', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
        { name: '重叠切割', value: null, reason: '', showFakeArea: false, drawingPaths: [] },
        { name: '跨图拼接', value: null, reason: '', showFakeArea: false, drawingPaths: [] }
      ])
      fetchMaskImage()
      fetchDetectionResults()
    } else if (texts.length > 0) {
      // 文本审核模式
      reviewMode.value = 'text'
      initTextReviewData(texts)
    } else {
      // 无内容
      reviewMode.value = 'empty'
    }
  } catch (error) {
    snackbar.showMessage('获取任务详情失败', 'error')
    reviewMode.value = 'empty'
  }
})

// ==================== 图片模式事件监听 ====================
watch(() => currentImage.value?.url, () => {
  if (reviewMode.value !== 'image' && reviewMode.value !== 'multi') return
  const imgElement = document.querySelector('.preview-box .v-img img') as HTMLImageElement
  if (imgElement) {
    if (imgElement.complete) {
      imageRect.value = imgElement.getBoundingClientRect()
    } else {
      imgElement.onload = () => {
        imageRect.value = imgElement.getBoundingClientRect()
      }
    }
  }
})

onMounted(() => {
  window.addEventListener('resize', () => {
    const imgElement = document.querySelector('.preview-box .v-img img') as HTMLImageElement
    if (imgElement) {
      imageRect.value = imgElement.getBoundingClientRect()
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('resize', () => { })
})

watch(() => currentImageIndex.value, () => {
  currentDrawingDimension.value = -1
})

watch(() => currentDrawingDimension.value, (newVal) => {
  drawingCanvases.value.forEach((canvas) => {
    if (canvas) canvas.style.display = 'none'
  })
  if (newVal !== -1) {
    const newCanvas = drawingCanvases.value[newVal]
    if (newCanvas) newCanvas.style.display = 'block'
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
  justify-content: center;
  gap: 24px;
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

.answer-card {
  padding: 16px;
  border-radius: 8px;
  background-color: rgb(var(--v-theme-surface));
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  min-width: 280px;
  margin-right: 200px;
}

.answer-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.overlay-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  mix-blend-mode: multiply;
  opacity: 0.7;
  object-fit: contain;
}

.answer-btn {
  width: 36px !important;
  min-width: 0 !important;
  height: 36px !important;
  padding: 0 !important;
}

@media (max-width: 1280px) {
  .task-stats {
    min-width: clamp(280px, 25vw, 320px);
  }
  .answer-card {
    padding: 12px;
  }
  .answer-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.image-list {
  width: clamp(100px, 8vw, 120px);
  height: calc(100vh - 380px);
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.image-grid {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
  margin-top: -8px;
}

.image-grid-item {
  width: 80px;
  height: 80px;
  cursor: pointer;
  border-radius: 4px;
  overflow: hidden;
  transition: border-color 0.2s ease;
  border: 2px solid transparent;
  flex-shrink: 0;
}

.image-grid-item:hover {
  border-color: rgba(var(--v-theme-primary), 0.5);
}

.image-grid-item.active {
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

@media (max-width: 960px) {
  .content-container {
    flex-wrap: wrap;
    justify-content: flex-start;
  }
  .preview-section {
    max-width: 100%;
    order: -1;
  }
  .image-list {
    height: auto;
    min-height: 300px;
  }
  .answer-card {
    padding: 12px;
  }
  .answer-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.dimension-section {
  width: 360px;
  padding: 20px;
  background-color: rgb(var(--v-theme-surface));
  height: calc(100vh - 380px);
  overflow-y: auto;
}

.dimension-list {
  padding-right: 12px;
}

.dimension-item {
  border-bottom: 1px solid rgba(var(--v-theme-primary), 0.1);
  padding-bottom: 16px;
}

.dimension-item:last-child {
  border-bottom: none;
}

@media (max-width: 1280px) {
  .dimension-section {
    width: 260px;
  }
}

.fake-judge-section {
  border-top: 1px solid rgba(var(--v-theme-primary), 0.1);
}

.degree-buttons {
  width: 100%;
}

.degree-buttons .v-btn {
  text-transform: none;
  letter-spacing: 0;
  font-size: 0.875rem;
}

.fake-area-btn {
  font-size: 0.75rem;
  text-transform: none;
  letter-spacing: 0;
  min-width: 120px;
}

.drawing-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
  display: none;
}

.drawing-canvas.active {
  pointer-events: auto;
  cursor: crosshair;
  display: block;
}

/* 文本审核模式样式 */
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
  border-color: rgb(var(--v-theme-primary));
  background-color: rgba(var(--v-theme-primary), 0.1);
}

.cursor-pointer {
  cursor: pointer;
}
</style>
