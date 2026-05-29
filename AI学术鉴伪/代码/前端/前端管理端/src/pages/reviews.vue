<template>
  <v-container>
    <!-- 标题 -->
    <v-row class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold">人工审核审批</h1>
      </v-col>
    </v-row>

    <!-- 搜索和筛选区域 -->
    <v-row class="mb-4">
      <v-col cols="12" sm="8" md="6">
        <v-text-field
          v-model="searchQuery"
          label="搜索编辑"
          append-inner-icon="mdi-magnify"
          clearable
          density="compact"
          hide-details
          class="search-input"
          @keyup.enter="handleSearch"
          @click:append-inner="handleSearch"
          @click:clear="handleSearch"
          placeholder="请输入编辑名称"
        ></v-text-field>
      </v-col>
      <v-col cols="12" sm="4" md="6" class="d-flex justify-end">
        <v-btn 
          color="primary" 
          class="text-none mr-2" 
          prepend-icon="mdi-filter-variant"
          @click="showFilterDialog = true"
        >
          筛选
        </v-btn>
      </v-col>
    </v-row>

    <v-card class="elevation-2">
      <v-data-table
        :headers="headers"
        :items="requests"
        class="elevation-0"
        :items-per-page="pageSize"
        hover
        :width="'100%'"
        :loading="loading"
        hide-default-footer
      >
        <template v-slot:top>
          <div class="d-flex align-center pa-4">
            <div class="text-caption text-medium-emphasis">
              共 {{ totalRequests }} 条记录
            </div>
          </div>
        </template>

        <template v-slot:item.avatar="{ item }">
          <v-avatar size="40">
            <v-img :src="item.avatar || 'https://randomuser.me/api/portraits/lego/1.jpg'" :alt="item.username"></v-img>
          </v-avatar>
        </template>

        <template v-slot:item.task_type="{ item }">
          <v-chip
            :color="getTaskTypeColor(item.task_type || 'image')"
            size="small"
            variant="tonal"
          >
            {{ getTaskTypeName(item.task_type || 'image') }}
          </v-chip>
        </template>

        <template v-slot:item.state="{ item }">
          <v-chip
            :color="getStateColor(item.state)"
            size="small"
            class="state-chip"
          >
            {{ getStateName(item.state) }}
          </v-chip>
        </template>

        <template v-slot:item.actions="{ item }">
          <v-btn
            icon
            variant="text"
            size="small"
            color="primary"
            class="mr-2"
            @click="openReviewDialog(item)"
          >
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </template>
      </v-data-table>
      
      <div class="d-flex align-center justify-center pa-4">
        <div class="d-flex align-center">
          <span class="text-caption mr-2">每页显示</span>
          <v-select
            v-model="pageSize"
            :items="[5, 10, 20, 50, 100]"
            density="compact"
            variant="outlined"
            hide-details
            style="width: 100px"
            @update:model-value="handlePageSizeChange"
          ></v-select>
          <span class="text-caption ml-2">条</span>
        </div>
        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          :total-visible="7"
          class="ml-4"
          @update:model-value="handlePageChange"
        ></v-pagination>
      </div>
    </v-card>

    <!-- 筛选对话框 -->
    <v-dialog v-model="showFilterDialog" max-width="500">
      <v-card class="elevation-4">
        <v-card-title class="text-h6 font-weight-bold">筛选条件</v-card-title>
        <v-card-text>
          <div class="d-flex flex-column gap-4">
            <v-select
              v-model="filters.status"
              :items="statusOptions"
              label="审核状态"
              clearable
              hide-details
            ></v-select>

            <v-select
              v-model="filters.taskType"
              :items="taskTypeOptions"
              label="材料类型"
              clearable
              density="compact"
              variant="outlined"
              hide-details
            ></v-select>

            <v-select
              v-model="filters.timeRange"
              :items="timeRangeOptions"
              label="快速选择时间范围"
              clearable
              hide-details
              @update:model-value="handleTimeRangeChange"
            ></v-select>

            <div class="d-flex align-center gap-4">
              <v-text-field
                v-model="filters.startDate"
                label="开始时间"
                type="datetime-local"
                hide-details
                density="compact"
                :error-messages="timeError"
                @update:model-value="handleCustomTimeChange"
              ></v-text-field>
              <v-text-field
                v-model="filters.endDate"
                label="结束时间"
                type="datetime-local"
                hide-details
                density="compact"
                :error-messages="timeError"
                @update:model-value="handleCustomTimeChange"
              ></v-text-field>
            </div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="resetFilters">重置</v-btn>
          <v-btn color="primary" @click="applyFilters">应用</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 审核详情对话框 -->
    <v-dialog v-model="showReviewDialog" max-width="1000" scrollable>
      <v-card class="elevation-4">
        <v-card-title class="d-flex justify-space-between align-center">
          <span class="text-h6 font-weight-bold">审核详情</span>
          <v-btn icon variant="text" @click="showReviewDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text style="max-height: 75vh;">
          <div v-if="selectedRequest" class="d-flex flex-column gap-4">
            <!-- 申请人信息 -->
            <div class="d-flex align-center">
              <v-avatar size="40" class="mr-4">
                <v-img :src="selectedRequest.avatar || 'https://randomuser.me/api/portraits/lego/1.jpg'" :alt="selectedRequest.username"></v-img>
              </v-avatar>
              <div>
                <div class="text-h6">{{ selectedRequest.username }}</div>
                <div class="text-caption text-medium-emphasis">{{ formatTime(selectedRequest.time) }}</div>
              </div>
              <v-spacer></v-spacer>
              <v-chip
                :color="getStateColor(selectedRequest.state)"
                size="small"
                class="state-chip"
              >
                {{ getStateName(selectedRequest.state) }}
              </v-chip>
            </div>

            <v-divider></v-divider>

            <div v-if="reviewDetails" class="d-flex flex-column gap-4">
              <!-- 检测任务信息 -->
              <div v-if="reviewDetails.task_id" class="d-flex flex-column gap-2">
                <div class="text-subtitle-1 font-weight-bold">
                  <v-icon class="mr-1" color="primary">mdi-clipboard-text-outline</v-icon>
                  检测任务信息
                </div>
                <v-card variant="outlined" rounded="lg" class="pa-3">
                  <div class="d-flex align-center gap-4 flex-wrap">
                    <div>
                      <span class="text-caption text-medium-emphasis">任务ID：</span>
                      <span class="text-body-2 font-weight-medium">{{ reviewDetails.task_id }}</span>
                    </div>
                    <div v-if="reviewDetails.task_type">
                      <span class="text-caption text-medium-emphasis">任务类型：</span>
                      <v-chip size="small" color="primary">{{ getTaskTypeName(reviewDetails.task_type) }}</v-chip>
                    </div>
                    <div v-if="reviewDetails.detect_type">
                      <span class="text-caption text-medium-emphasis">检测类型：</span>
                      <v-chip size="small" color="teal">{{ getDetectTypeName(reviewDetails.detect_type) }}</v-chip>
                    </div>
                    <div v-if="reviewDetails.organization">
                      <span class="text-caption text-medium-emphasis">所属组织：</span>
                      <span class="text-body-2">{{ reviewDetails.organization }}</span>
                    </div>
                  </div>
                </v-card>
              </div>

              <!-- AI检测结果摘要 -->
              <div v-if="reviewDetails.ai_detection_result && (reviewDetails.ai_detection_result.is_fake != null || reviewDetails.ai_detection_result.confidence_score != null)" class="d-flex flex-column gap-2">
                <div class="text-subtitle-1 font-weight-bold">
                  <v-icon class="mr-1" :color="reviewDetails.ai_detection_result.is_fake ? 'error' : 'success'">
                    {{ reviewDetails.ai_detection_result.is_fake ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                  </v-icon>
                  AI检测结果摘要
                </div>
                <v-card variant="outlined" rounded="lg" class="pa-3"
                  :class="reviewDetails.ai_detection_result.is_fake ? 'bg-error-lighten-5' : 'bg-success-lighten-5'"
                >
                  <div class="d-flex align-center gap-4 flex-wrap">
                    <div class="d-flex align-center">
                      <v-icon size="large" :color="reviewDetails.ai_detection_result.is_fake ? 'error' : 'success'" class="mr-2">
                        {{ reviewDetails.ai_detection_result.is_fake ? 'mdi-alert-octagon' : 'mdi-shield-check' }}
                      </v-icon>
                      <span class="text-h6" :class="reviewDetails.ai_detection_result.is_fake ? 'error--text' : 'success--text'">
                        {{ reviewDetails.ai_detection_result.is_fake ? '检测异常' : '检测正常' }}
                      </span>
                    </div>
                    <v-chip v-if="reviewDetails.ai_detection_result.confidence_score != null" size="small"
                      :color="reviewDetails.ai_detection_result.confidence_score > 0.7 ? 'error' : reviewDetails.ai_detection_result.confidence_score > 0.4 ? 'warning' : 'success'"
                    >
                      置信度: {{ (reviewDetails.ai_detection_result.confidence_score * 100).toFixed(1) }}%
                    </v-chip>
                    <span v-if="reviewDetails.ai_detection_result.detection_time" class="text-caption text-medium-emphasis">
                      {{ reviewDetails.ai_detection_result.detection_time }}
                    </span>
                  </div>
                </v-card>
              </div>

              <!-- 资源预览 -->
              <div class="d-flex flex-column gap-2">
                <div class="text-subtitle-1 font-weight-bold">
                  <v-icon class="mr-1" color="info">mdi-folder-open-outline</v-icon>
                  资源预览
                </div>

                <!-- 论文文件 -->
                <v-card v-if="reviewDetails.paper_files && reviewDetails.paper_files.length > 0" variant="outlined" rounded="lg" class="pa-3">
                  <div class="text-subtitle-2 font-weight-bold mb-2">
                    <v-icon size="small" class="mr-1">mdi-file-document-outline</v-icon>
                    论文文件
                    <v-chip size="x-small" class="ml-2">{{ reviewDetails.paper_files.length }}</v-chip>
                  </div>
                  <div class="d-flex flex-column gap-2">
                    <div v-for="pf in reviewDetails.paper_files" :key="pf.file_id" class="d-flex align-center pa-2 rounded bg-grey-lighten-4">
                      <v-icon class="mr-2" color="primary">mdi-file-document</v-icon>
                      <div class="flex-grow-1">
                        <div class="text-body-2 font-weight-medium">{{ pf.file_name }}</div>
                        <div class="text-caption text-medium-emphasis">
                          <v-chip size="x-small" variant="outlined" class="mr-1">{{ getRoleName(pf.resource_role) }}</v-chip>
                          <span>{{ pf.sections_count }} 段落</span>
                          <span v-if="pf.file_ext" class="ml-2">{{ pf.file_ext }}</span>
                        </div>
                      </div>
                      <v-btn v-if="pf.preview_url" size="small" variant="text" color="primary"
                        @click="openPreviewPanel(pf.file_id, 'file', pf.file_name)" prepend-icon="mdi-eye"
                      >
                        预览
                      </v-btn>
                    </div>
                  </div>
                </v-card>

                <!-- 审稿文件 -->
                <v-card v-if="reviewDetails.review_files && reviewDetails.review_files.length > 0" variant="outlined" rounded="lg" class="pa-3">
                  <div class="text-subtitle-2 font-weight-bold mb-2">
                    <v-icon size="small" class="mr-1">mdi-file-edit-outline</v-icon>
                    审稿文件
                    <v-chip size="x-small" class="ml-2">{{ reviewDetails.review_files.length }}</v-chip>
                  </div>
                  <div class="d-flex flex-column gap-2">
                    <div v-for="rf in reviewDetails.review_files" :key="rf.file_id" class="d-flex align-center pa-2 rounded bg-grey-lighten-4">
                      <v-icon class="mr-2" color="purple">mdi-file-edit</v-icon>
                      <div class="flex-grow-1">
                        <div class="text-body-2 font-weight-medium">{{ rf.file_name }}</div>
                        <div class="text-caption text-medium-emphasis">
                          <v-chip size="x-small" variant="outlined" color="purple" class="mr-1">{{ getRoleName(rf.resource_role) }}</v-chip>
                          <span>{{ rf.sections_count }} 段落</span>
                        </div>
                      </div>
                      <v-btn v-if="rf.preview_url" size="small" variant="text" color="purple"
                        @click="openPreviewPanel(rf.file_id, 'file', rf.file_name)" prepend-icon="mdi-eye"
                      >
                        预览
                      </v-btn>
                    </div>
                  </div>
                </v-card>

                <!-- 审稿文本 -->
                <v-card v-if="reviewDetails.review_texts && reviewDetails.review_texts.length > 0" variant="outlined" rounded="lg" class="pa-3">
                  <div class="text-subtitle-2 font-weight-bold mb-2">
                    <v-icon size="small" class="mr-1">mdi-text-box-outline</v-icon>
                    审稿文本
                    <v-chip size="x-small" class="ml-2">{{ reviewDetails.review_texts.length }}</v-chip>
                  </div>
                  <div class="d-flex flex-column gap-2">
                    <div v-for="rt in reviewDetails.review_texts" :key="rt.review_text_id" class="pa-2 rounded bg-grey-lighten-4">
                      <div class="d-flex align-center mb-1">
                        <v-chip size="x-small" :color="rt.source_type === 'paste' ? 'info' : 'secondary'" class="mr-2">
                          {{ getSourceTypeName(rt.source_type) }}
                        </v-chip>
                        <span v-if="rt.language" class="text-caption text-medium-emphasis mr-2">{{ rt.language }}</span>
                        <span v-if="rt.token_count" class="text-caption text-medium-emphasis">{{ rt.token_count }} tokens</span>
                      </div>
                      <div class="text-body-2 text-truncate" style="max-height: 60px; overflow: hidden;">
                        {{ rt.preview_text }}
                      </div>
                    </div>
                  </div>
                </v-card>

                <!-- 图片资源 (仅图像检测和综合检测显示) -->
                <v-card v-if="reviewDetails.imgs && reviewDetails.imgs.length > 0 && (!reviewDetails.task_type || ['image', 'multi_material'].includes(reviewDetails.task_type))" variant="outlined" rounded="lg" class="pa-3">
                  <div class="text-subtitle-2 font-weight-bold mb-2">
                    <v-icon size="small" class="mr-1">mdi-image-multiple</v-icon>
                    图片资源
                    <v-chip size="x-small" class="ml-2">{{ reviewDetails.imgs.length }}</v-chip>
                  </div>
                  <v-row class="mt-1">
                    <v-col v-for="img in reviewDetails.imgs" :key="img.id" cols="6" sm="4" md="3">
                      <v-card variant="outlined" rounded="lg" class="overflow-hidden">
                        <v-img
                          :src="resolveImageUrl(img.url)"
                          height="160"
                          cover
                          class="cursor-pointer"
                          @click="openImagePreview(img.url)"
                        >
                          <template v-slot:placeholder>
                            <div class="d-flex align-center justify-center fill-height bg-grey-lighten-3">
                              <v-progress-circular indeterminate color="primary" size="24"></v-progress-circular>
                            </div>
                          </template>
                          <template v-slot:error>
                            <div class="d-flex flex-column align-center justify-center fill-height bg-grey-lighten-3">
                              <v-icon size="40" color="grey">mdi-image-broken-variant</v-icon>
                            </div>
                          </template>
                        </v-img>
                      </v-card>
                    </v-col>
                  </v-row>
                </v-card>

                <!-- 文本资源（兼容旧字段） -->
                <v-card v-if="reviewDetails.texts && reviewDetails.texts.length > 0 && (!reviewDetails.paper_files || reviewDetails.paper_files.length === 0) && (!reviewDetails.review_texts || reviewDetails.review_texts.length === 0)" variant="outlined" rounded="lg" class="pa-3">
                  <div class="text-subtitle-2 font-weight-bold mb-2">
                    <v-icon size="small" class="mr-1">mdi-text-box-outline</v-icon>
                    文本资源
                    <v-chip size="x-small" class="ml-2">{{ reviewDetails.texts.length }}</v-chip>
                  </div>
                  <div class="d-flex flex-column gap-2">
                    <v-card v-for="text in reviewDetails.texts" :key="text.id" variant="flat" rounded="lg" class="pa-2 bg-grey-lighten-4">
                      <div class="d-flex align-center mb-1">
                        <v-chip size="x-small" :color="text.source_type === 'paper' || text.source_type === 'file_parsed' ? 'primary' : text.source_type === 'review' || text.source_type === 'paste' ? 'purple' : 'grey'" class="mr-2">
                          {{ getSourceTypeName(text.source_type) }}
                        </v-chip>
                        <span class="text-caption text-medium-emphasis">ID: {{ text.id }}</span>
                      </div>
                      <div class="text-body-2" style="line-height: 1.5; max-height: 120px; overflow-y: auto;">
                        {{ text.raw_text }}
                      </div>
                      <div v-if="text.ai_detection" class="mt-2">
                        <v-divider class="mb-1"></v-divider>
                        <div class="d-flex align-center gap-2">
                          <v-icon size="small" :color="text.ai_detection.is_fake ? 'error' : 'success'">
                            {{ text.ai_detection.is_fake ? 'mdi-alert-circle' : 'mdi-check-circle' }}
                          </v-icon>
                          <span class="text-caption" :class="text.ai_detection.is_fake ? 'error--text' : 'success--text'">
                            {{ text.ai_detection.is_fake ? 'AI判定：异常' : 'AI判定：正常' }}
                          </span>
                          <v-chip v-if="text.ai_detection.confidence_score != null" size="x-small"
                            :color="text.ai_detection.confidence_score > 0.7 ? 'error' : text.ai_detection.confidence_score > 0.4 ? 'warning' : 'success'"
                          >
                            {{ (text.ai_detection.confidence_score * 100).toFixed(1) }}%
                          </v-chip>
                        </div>
                      </div>
                    </v-card>
                  </div>
                </v-card>
              </div>

              <v-divider></v-divider>

              <!-- 检测详情 -->
              <div v-if="reviewDetails.structured_items && reviewDetails.structured_items.length > 0" class="d-flex flex-column gap-2">
                <div class="d-flex align-center">
                  <div class="text-subtitle-1 font-weight-bold">
                    <v-icon class="mr-1" color="teal">mdi-shield-search</v-icon>
                    检测详情
                    <v-chip size="small" class="ml-2">{{ reviewDetails.structured_items.length }}</v-chip>
                  </div>
                </div>
                <v-card variant="outlined" rounded="lg" class="pa-3">
                  <div class="d-flex align-center gap-3 flex-wrap mb-3">
                    <v-chip size="small" variant="outlined">
                      <v-icon start size="small">mdi-format-list-bulleted</v-icon>
                      总段落数: {{ totalSections }}
                    </v-chip>
                    <v-chip size="small" color="error" variant="tonal">
                      <v-icon start size="small">mdi-robot</v-icon>
                      AI生成: {{ flaggedCount }}
                    </v-chip>
                    <v-chip size="small" color="success" variant="tonal">
                      <v-icon start size="small">mdi-account</v-icon>
                      人类写作: {{ humanCount }}
                    </v-chip>
                    <v-chip size="small" color="grey" variant="tonal">
                      <v-icon start size="small">mdi-help-circle</v-icon>
                      未判定: {{ totalSections - flaggedCount - humanCount }}
                    </v-chip>
                    <v-spacer></v-spacer>
                    <v-btn v-if="reviewDetails.task_id"
                      color="teal" variant="text" prepend-icon="mdi-magnify-scan"
                      @click="viewDetectionResult" :loading="detectionResultLoading" size="small"
                    >
                      查看完整检测结果
                    </v-btn>
                  </div>
                  <div v-if="flaggedCount > 0" class="d-flex flex-column gap-1">
                    <div class="text-subtitle-2 font-weight-bold mb-1">AI生成段落：</div>
                    <div v-for="item in reviewDetails.structured_items.filter(i => i.is_aigc)" :key="'flagged-' + item.item_id"
                      class="d-flex align-center pa-2 rounded bg-error-lighten-5 paragraph-item-clickable"
                      @click="openParagraphDetail(item)"
                    >
                      <v-icon size="small" color="error" class="mr-2">mdi-alert</v-icon>
                      <span class="text-caption font-mono mr-2">{{ item.item_id }}</span>
                      <span class="text-body-2 flex-grow-1 text-truncate">{{ (item.text || '').substring(0, 100) }}</span>
                      <v-chip size="x-small" color="error" variant="tonal" class="ml-2">
                        {{ item.confidence_score ? (item.confidence_score * 100).toFixed(1) + '%' : '-' }}
                      </v-chip>
                      <v-icon size="small" color="grey" class="ml-1">mdi-chevron-right</v-icon>
                    </div>
                  </div>
                  <div v-else class="text-body-2 text-grey pa-2">
                    未发现AI生成段落
                  </div>
                </v-card>
              </div>

              <v-divider></v-divider>

              <!-- 审核人列表 -->
              <div class="d-flex flex-column gap-2">
                <div class="text-subtitle-1 font-weight-bold">
                  <v-icon class="mr-1" color="orange">mdi-account-group</v-icon>
                  审核人列表
                  <v-chip size="small" class="ml-2">{{ reviewDetails.persons.length }}</v-chip>
                </div>
                <div v-if="reviewDetails.persons.length > 0" class="d-flex flex-wrap gap-4">
                  <div v-for="person in reviewDetails.persons" :key="person.id" class="d-flex align-center">
                    <v-avatar size="32" class="mr-2">
                      <v-img :src="resolveImageUrl(person.avatar)" :alt="person.username">
                        <template v-slot:error>
                          <v-icon>mdi-account-circle</v-icon>
                        </template>
                      </v-img>
                    </v-avatar>
                    <span class="text-body-2">{{ person.username }}</span>
                  </div>
                </div>
                <div v-else class="text-body-2 text-grey pa-2">暂未分配审核人</div>
              </div>

              <!-- 申请理由 -->
              <div v-if="reviewDetails.reason" class="d-flex flex-column gap-2">
                <div class="text-subtitle-1 font-weight-bold">
                  <v-icon class="mr-1" color="amber">mdi-comment-text-outline</v-icon>
                  申请理由
                </div>
                <v-card variant="outlined" rounded="lg" class="pa-3 bg-amber-lighten-5">
                  <div class="text-body-1">{{ reviewDetails.reason }}</div>
                </v-card>
              </div>
            </div>

            <!-- 加载中 -->
            <div v-else class="d-flex justify-center align-center pa-6">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
              <span class="ml-3 text-body-1">正在加载详情...</span>
            </div>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="showReviewDialog = false">关闭</v-btn>
          <v-btn color="error" variant="text" :disabled="!selectedRequest || selectedRequest.state !== 'pending'" @click="handleReviewRequest(0)">拒绝</v-btn>
          <v-btn color="success" :disabled="!selectedRequest || selectedRequest.state !== 'pending'" @click="handleReviewRequest(1)">通过</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 图片预览对话框 -->
    <v-dialog v-model="showImagePreview" max-width="900">
      <v-card rounded="lg">
        <v-card-title class="d-flex justify-space-between align-center">
          <span class="text-h6">图片预览</span>
          <v-btn icon variant="text" @click="showImagePreview = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text class="pa-2">
          <v-img
            :src="previewImageUrl"
            max-height="75vh"
            contain
          >
            <template v-slot:error>
              <div class="d-flex flex-column align-center justify-center pa-10">
                <v-icon size="64" color="grey">mdi-image-broken-variant</v-icon>
                <div class="text-h6 mt-4 text-grey">图片无法加载</div>
              </div>
            </template>
          </v-img>
        </v-card-text>
      </v-card>
    </v-dialog>

    <!-- 检测结果对话框 -->
    <v-dialog v-model="showDetectionResultDialog" max-width="1100" scrollable>
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span class="text-h5 font-weight-bold">检测结果</span>
          <v-btn icon @click="showDetectionResultDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-divider></v-divider>

        <v-card-text style="max-height: 70vh;">
          <!-- 加载中 -->
          <div v-if="detectionResultLoading" class="d-flex justify-center align-center pa-8">
            <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
            <span class="ml-4 text-body-1">正在加载检测结果...</span>
          </div>

          <!-- 无数据 -->
          <div v-else-if="!detectionResultData" class="text-center pa-8 text-grey">
            <v-icon size="64" color="grey-lighten-1">mdi-file-search-outline</v-icon>
            <div class="text-h6 mt-4">未获取到检测结果</div>
          </div>

          <!-- 检测结果内容：使用对应检测组件渲染 -->
          <div v-else class="pa-2">
            <ImageDetectionResult
              v-if="detectionResultData.task_type === 'image'"
              :task_id="String(detectionResultData.task_id || reviewDetails?.task_id || '')"
              :detection_time="detectionResultData.detection_time || ''"
            />
            <TextDetectionResult
              v-else-if="detectionResultData.task_type === 'paper_text' || detectionResultData.task_type === 'review_text'"
              :task-id="detectionResultData.task_id || reviewDetails?.task_id || ''"
              :task-meta="detectionResultData"
            />
            <MultiMaterialResult
              v-else-if="detectionResultData.task_type === 'multi_material'"
              :task-id="detectionResultData.task_id || reviewDetails?.task_id || ''"
              :task-meta="detectionResultData"
            />
            <div v-else class="text-center pa-8 text-grey">
              <v-icon size="64" color="grey-lighten-1">mdi-help-circle-outline</v-icon>
              <div class="text-h6 mt-4">未知的检测类型：{{ detectionResultData.task_type }}</div>
            </div>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pa-4 justify-end">
          <v-btn color="primary" @click="showDetectionResultDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 拒绝理由对话框 -->
    <v-dialog v-model="showRejectDialog" max-width="500">
      <v-card class="elevation-4">
        <v-card-title class="text-h6 font-weight-bold">拒绝理由</v-card-title>
        <v-card-text>
          <v-textarea
            v-model="rejectReason"
            label="请输入拒绝理由"
            rows="3"
            hide-details
            variant="outlined"
          ></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="showRejectDialog = false">取消</v-btn>
          <v-btn color="error" @click="handleReviewRequest(0)">确认拒绝</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 资源预览侧边面板 -->
    <transition name="slide-panel">
      <div v-if="showPreviewPanel" class="preview-side-panel">
        <div class="preview-panel-header">
          <span class="text-h6 font-weight-bold">资源预览</span>
          <v-btn icon variant="text" @click="closePreviewPanel">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
        <div v-if="previewFileName" class="px-4 py-2 text-body-2 text-medium-emphasis bg-grey-lighten-4">
          <v-icon size="small" class="mr-1">mdi-file-document</v-icon>
          {{ previewFileName }}
        </div>
        <div class="preview-panel-content">
          <div v-if="previewLoading" class="d-flex flex-column align-center justify-center pa-8">
            <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
            <span class="mt-4 text-body-1">正在加载预览...</span>
          </div>
          <div v-else-if="previewBlobUrl">
            <iframe v-if="previewType === 'pdf'" :src="previewBlobUrl"
              style="width: 100%; height: 75vh; border: none; border-radius: 8px;"
            ></iframe>
            <v-img v-else-if="previewType === 'image'" :src="previewBlobUrl"
              contain max-height="75vh"
            >
              <template v-slot:error>
                <div class="d-flex flex-column align-center justify-center pa-10">
                  <v-icon size="64" color="grey">mdi-image-broken-variant</v-icon>
                  <div class="text-h6 mt-4 text-grey">图片无法加载</div>
                </div>
              </template>
            </v-img>
            <pre v-else-if="previewType === 'text'" class="text-preview-content">{{ previewTextContent }}</pre>
            <div v-else class="d-flex flex-column align-center justify-center pa-8">
              <v-icon size="64" color="grey">mdi-file-question-outline</v-icon>
              <div class="text-h6 mt-4 text-grey">该文件格式不支持在线预览</div>
              <v-btn :href="previewBlobUrl" color="primary" class="mt-4" prepend-icon="mdi-download">
                下载文件
              </v-btn>
            </div>
          </div>
          <div v-else class="d-flex flex-column align-center justify-center pa-8">
            <v-icon size="64" color="grey">mdi-file-question-outline</v-icon>
            <div class="text-h6 mt-4 text-grey">无法预览该资源</div>
          </div>
        </div>
      </div>
    </transition>

    <!-- 段落详情侧边面板 -->
    <transition name="slide-panel">
      <div v-if="showParagraphPanel" class="paragraph-side-panel">
        <div class="preview-panel-header">
          <span class="text-h6 font-weight-bold">段落详情</span>
          <v-btn icon variant="text" @click="closeParagraphDetail">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <div class="preview-panel-content" v-if="selectedParagraph">
          <!-- 段落标题 -->
          <v-card variant="outlined" rounded="lg" class="mb-4">
            <div class="d-flex align-center flex-wrap gap-2 pa-4">
              <v-icon :color="getParagraphConfidenceColor(selectedParagraph.confidence_score)" class="mr-1">
                {{ (selectedParagraph.confidence_score || 0) > 0.5 ? 'mdi-alert-circle' : 'mdi-check-circle' }}
              </v-icon>
              <span class="text-subtitle-1 font-weight-bold">{{ selectedParagraph.item_id }}</span>
              <v-chip v-if="selectedParagraph.is_aigc" color="error" size="small" variant="tonal">
                <v-icon start size="x-small">mdi-robot</v-icon>
                AI生成
              </v-chip>
              <v-chip v-else color="success" size="small" variant="tonal">
                <v-icon start size="x-small">mdi-account</v-icon>
                人类撰写
              </v-chip>
            </div>
          </v-card>

          <!-- BERT 检测结果 -->
          <v-card variant="outlined" rounded="lg" class="mb-4">
            <div class="d-flex align-center pa-4 pb-2">
              <v-icon color="primary" class="mr-2">mdi-brain</v-icon>
              <span class="text-subtitle-2 font-weight-bold">BERT 检测结果</span>
            </div>
            <div class="px-4 pb-4">
              <div class="text-caption text-medium-emphasis mb-1">AI生成置信度</div>
              <v-progress-linear
                :model-value="(selectedParagraph.confidence_score || 0) * 100"
                :color="getParagraphConfidenceColor(selectedParagraph.confidence_score)"
                height="24"
                rounded
                class="mb-2"
              >
                <template #default="{ value }">
                  <strong class="text-caption">{{ value.toFixed(1) }}%</strong>
                </template>
              </v-progress-linear>

              <div v-if="selectedParagraph.probabilities" class="mt-4">
                <div class="text-caption text-medium-emphasis mb-2">概率分布</div>
                <div class="d-flex align-center gap-4">
                  <div class="flex-grow-1">
                    <div class="text-caption text-grey mb-1">人类撰写</div>
                    <v-progress-linear
                      :model-value="(selectedParagraph.probabilities.human || 0) * 100"
                      color="success"
                      height="10"
                      rounded
                    />
                    <div class="text-caption text-right">{{ ((selectedParagraph.probabilities.human || 0) * 100).toFixed(1) }}%</div>
                  </div>
                  <div class="flex-grow-1">
                    <div class="text-caption text-grey mb-1">AI生成</div>
                    <v-progress-linear
                      :model-value="(selectedParagraph.probabilities.aigc || 0) * 100"
                      color="error"
                      height="10"
                      rounded
                    />
                    <div class="text-caption text-right">{{ ((selectedParagraph.probabilities.aigc || 0) * 100).toFixed(1) }}%</div>
                  </div>
                </div>
              </div>

              <div v-if="selectedParagraph.label_name" class="mt-3">
                <v-chip :color="selectedParagraph.is_aigc ? 'error' : 'success'" variant="tonal" size="small">
                  模型判定：{{ selectedParagraph.label_name }}
                </v-chip>
              </div>
            </div>
          </v-card>

          <!-- 段落内容 -->
          <v-card variant="outlined" rounded="lg">
            <div class="d-flex align-center pa-4 pb-2">
              <v-icon color="info" class="mr-2">mdi-text-box</v-icon>
              <span class="text-subtitle-2 font-weight-bold">段落内容</span>
            </div>
            <div class="px-4 pb-4">
              <div v-if="selectedParagraph.text" class="paragraph-detail-text">{{ selectedParagraph.text }}</div>
              <div v-else class="text-center py-4">
                <v-icon size="40" color="grey">mdi-text-box-remove-outline</v-icon>
                <div class="text-body-2 text-grey mt-2">该段落文本内容未保存</div>
              </div>
            </div>
          </v-card>
        </div>
      </div>
    </transition>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import reviewApi from '@/api/review'
import resourceApi from '@/api/resource'
import type { StructuredResult } from '@/api/resource'
import { useSnackbarStore } from '@/stores/snackbar'
import ImageDetectionResult from '@/components/detection/ImageDetectionResult.vue'
import TextDetectionResult from '@/components/detection/TextDetectionResult.vue'
import MultiMaterialResult from '@/components/detection/MultiMaterialResult.vue'

const snackbar = useSnackbarStore()

interface ReviewRequest {
  id: number
  username: string
  avatar: string
  state: string
  file_type: string
  time: string
  task_type?: string
  task_type_label?: string
}

const headers = [
  { title: '头像', key: 'avatar', align: 'center', sortable: false },
  { title: '编辑', key: 'username', align: 'start' },
  { title: '材料类型', key: 'task_type', align: 'center', sortable: false },
  { title: '审核状态', key: 'state', align: 'center' },
  { title: '提交时间', key: 'time', align: 'center' },
  { title: '操作', key: 'actions', align: 'center', sortable: false },
] as const

// 分页相关
const requests = ref<ReviewRequest[]>([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const totalRequests = ref(0)
const totalPages = ref(1)

// 搜索相关
const searchQuery = ref('')

// 筛选相关
const showFilterDialog = ref(false)
const filters = ref<{
  status: string | null
  taskType: string | null
  timeRange: string | null
  startDate: string | null
  endDate: string | null
}>({
  status: null,
  taskType: null,
  timeRange: null,
  startDate: null,
  endDate: null
})

const statusOptions = [
  { title: '未处理', value: 'pending' },
  { title: '已拒绝', value: 'refused' },
  { title: '已通过', value: 'accepted' }
]

const timeRangeOptions = [
  { title: '最近一天', value: '1d' },
  { title: '最近一周', value: '7d' },
  { title: '最近一月', value: '30d' },
  { title: '最近三月', value: '90d' },
  { title: '最近一年', value: '365d' }
]

const taskTypeOptions = [
  { title: '图像', value: 'image' },
  { title: '论文', value: 'paper_text' },
  { title: '审稿', value: 'review_text' },
  { title: '综合', value: 'multi_material' },
]


// 图片URL解析：处理相对路径、绝对路径和空值
const resolveImageUrl = (url?: string | null): string => {
  if (!url) return ''
  if (url.startsWith('http://') || url.startsWith('https://')) {
    if (url.includes('/api/preview/')) {
      const token = localStorage.getItem('1-token')
      if (token) {
        const separator = url.includes('?') ? '&' : '?'
        return url + separator + 'token=' + token
      }
    }
    return url
  }
  const baseUrl = import.meta.env.VITE_API_URL || ''
  return baseUrl + url
}

// 审核详情对话框相关
const showReviewDialog = ref(false)
const selectedRequest = ref<ReviewRequest | null>(null)
interface FileDisplay {
  file_id: number
  file_name: string
  resource_role: string
  file_ext: string
  sections_count: number
  preview_url: string | null
}

interface ReviewTextDisplay {
  review_text_id: number | null
  source_type: string
  language: string
  token_count: number
  preview_text: string
}

interface StructuredItem {
  item_id: string
  text: string | null
  is_aigc: boolean | null
  label_name: string | null
  confidence_score: number | null
  probabilities: Record<string, number> | null
  source_file_id: number | null
}

interface AiDetectionSummary {
  is_fake: boolean | null
  confidence_score: number | null
  detection_time: string | null
}

const reviewDetails = ref<{
  imgs: Array<{ id: number, url: string }>
  texts?: Array<{
    id: number
    raw_text: string
    source_type: string
    items?: any[]
    source_file_id?: number
    ai_detection?: {
      is_fake?: boolean
      confidence_score?: number
      factual_fake_reason?: string
    }
  }>
  persons: Array<{ id: number, username: string, avatar: string }>
  reason: string
  task_id?: number
  task_type?: string
  detect_type?: string
  organization?: string
  ai_detection_result?: AiDetectionSummary
  structured_items?: StructuredItem[]
  paper_files?: FileDisplay[]
  review_files?: FileDisplay[]
  review_texts?: ReviewTextDisplay[]
} | null>(null)

const flaggedCount = computed(() => {
  return (reviewDetails.value?.structured_items || []).filter(i => i.is_aigc === true).length
})

const humanCount = computed(() => {
  return (reviewDetails.value?.structured_items || []).filter(i => i.is_aigc === false).length
})

const totalSections = computed(() => {
  return (reviewDetails.value?.structured_items || []).length
})
const rejectReason = ref('')
const showRejectDialog = ref(false)

// 图片预览对话框
const showImagePreview = ref(false)
const previewImageUrl = ref('')

// 检测结果对话框
const showDetectionResultDialog = ref(false)
const detectionResultLoading = ref(false)
const detectionResultData = ref<StructuredResult | null>(null)

// 打开图片预览
const openImagePreview = (url: string) => {
  previewImageUrl.value = resolveImageUrl(url)
  showImagePreview.value = true
}

// 资源预览侧边面板
const showPreviewPanel = ref(false)
const previewLoading = ref(false)
const previewBlobUrl = ref<string | null>(null)
const previewType = ref<'image' | 'pdf' | 'text' | 'other'>('other')
const previewTextContent = ref('')
const previewFileName = ref('')

const openPreviewPanel = async (fileId: number, resourceType: string = 'file', fileName: string = '') => {
  showPreviewPanel.value = true
  previewLoading.value = true
  previewBlobUrl.value = null
  previewFileName.value = fileName

  try {
    const response = await resourceApi.previewResource(fileId, resourceType)
    const blob = response.data as any
    const contentType = blob.type || ''

    if (contentType.startsWith('image/')) {
      previewType.value = 'image'
    } else if (contentType === 'application/pdf' || fileName.toLowerCase().endsWith('.pdf')) {
      previewType.value = 'pdf'
    } else if (contentType.startsWith('text/') || /\.(txt|md|csv|json|xml)$/i.test(fileName)) {
      previewType.value = 'text'
      previewTextContent.value = await blob.text()
    } else {
      previewType.value = 'other'
    }

    previewBlobUrl.value = URL.createObjectURL(blob)
  } catch (error) {
    console.error('预览资源失败:', error)
    snackbar.showMessage('预览资源失败', 'error')
    previewBlobUrl.value = null
  } finally {
    previewLoading.value = false
  }
}

const closePreviewPanel = () => {
  showPreviewPanel.value = false
  if (previewBlobUrl.value) {
    URL.revokeObjectURL(previewBlobUrl.value)
    previewBlobUrl.value = null
  }
}

// 段落详情侧边面板
const showParagraphPanel = ref(false)
const selectedParagraph = ref<StructuredItem | null>(null)

const openParagraphDetail = (item: StructuredItem) => {
  selectedParagraph.value = item
  showParagraphPanel.value = true
}

const closeParagraphDetail = () => {
  showParagraphPanel.value = false
}

const getParagraphConfidenceColor = (score: number | null): string => {
  const s = score || 0
  if (s > 0.8) return 'error'
  if (s > 0.5) return 'warning'
  if (s > 0.3) return 'info'
  return 'success'
}

// 查看完整检测结果
const viewDetectionResult = async () => {
  if (!reviewDetails.value?.task_id) {
    snackbar.showMessage('无法获取检测任务ID', 'warning')
    return
  }
  showDetectionResultDialog.value = true
  detectionResultLoading.value = true
  detectionResultData.value = null
  try {
    const response = await resourceApi.getDetectionResult(reviewDetails.value.task_id)
    detectionResultData.value = response.data
  } catch (error) {
    console.error('获取检测结果失败:', error)
    snackbar.showMessage('获取检测结果失败', 'error')
  } finally {
    detectionResultLoading.value = false
  }
}

// 任务类型名称映射
const getTaskTypeName = (type: string): string => {
  const map: Record<string, string> = {
    'image': '图片检测',
    'paper_text': '论文文本检测',
    'review_text': '审稿文本检测',
    'multi_material': '综合材料检测'
  }
  return map[type] || type
}

// 任务类型颜色映射
const getTaskTypeColor = (type: string): string => {
  const map: Record<string, string> = {
    'image': 'blue',
    'paper_text': 'teal',
    'review_text': 'purple',
    'multi_material': 'orange'
  }
  return map[type] || 'grey'
}

// 来源类型名称映射
const getSourceTypeName = (type: string): string => {
  const map: Record<string, string> = {
    'paper': '论文',
    'review': '审稿意见',
    'image': '图片',
    'paste': '粘贴文本',
    'file_parsed': '文件解析'
  }
  return map[type] || type || '未知'
}

// 检测类型名称映射
const getDetectTypeName = (type: string): string => {
  const map: Record<string, string> = {
    'image': '图片检测',
    'paper': '论文检测',
    'review': '审稿检测',
    'multi': '综合检测'
  }
  return map[type] || type || '未知'
}

// 资源角色名称映射
const getRoleName = (role: string): string => {
  const map: Record<string, string> = {
    'paper_main': '论文正文',
    'paper_supplementary': '论文附件',
    'review_main': '审稿正文',
    'review_attachment': '审稿附件'
  }
  return map[role] || role || '未知'
}

// 获取LLM分析内容
const getLlmAnalysis = (): string | Record<string, any> | null => {
  if (!detectionResultData.value) return null
  const result = detectionResultData.value.result
  if (result?.llm_analysis) return result.llm_analysis
  if (detectionResultData.value.ai_response) return detectionResultData.value.ai_response
  return null
}

// 格式化检测证据
const formatEvidence = (evidence: any): string => {
  if (!evidence) return ''
  if (typeof evidence === 'string') return evidence
  try {
    return JSON.stringify(evidence, null, 2)
  } catch {
    return String(evidence)
  }
}

// 格式化LLM分析值
const formatLlmValue = (value: any): string => {
  if (value === null || value === undefined) return '-'
  if (typeof value === 'string') return value
  if (typeof value === 'number') return String(value)
  if (typeof value === 'boolean') return value ? '是' : '否'
  try {
    return JSON.stringify(value, null, 2)
  } catch {
    return String(value)
  }
}

const getStateColor = (state: string) => {
  switch (state) {
    case 'pending':
      return 'warning'
    case 'refused':
      return 'error'
    case 'accepted':
      return 'success'
    default:
      return 'grey'
  }
}

const getStateName = (state: string) => {
  switch (state) {
    case 'pending':
      return '未处理'
    case 'refused':
      return '已拒绝'
    case 'accepted':
      return '已通过'
    default:
      return state
  }
}

const formatTime = (timestamp: string) => {
  return timestamp // 后端返回的时间格式已经是正确的，直接显示
}

const openReviewDialog = async (request: ReviewRequest) => {
  selectedRequest.value = request
  try {
    const response = await reviewApi.getReviewRequestDetails(request.id)
    reviewDetails.value = response.data
    showReviewDialog.value = true
  } catch (error) {
    console.error('获取审核详情失败:', error)
    snackbar.showMessage('获取审核详情失败', 'error')
  }
}

const handleReviewRequest = async (choice: number) => {
  if (choice === 0 && !rejectReason.value) {
    showRejectDialog.value = true
    return
  }

  try {
    await reviewApi.handleReviewRequest(selectedRequest.value!.id, {
      choice,
      reason: rejectReason.value
    })
    snackbar.showMessage(choice === 1 ? '已通过审核' : '已拒绝审核', 'success')
    showReviewDialog.value = false
    showRejectDialog.value = false
    rejectReason.value = ''
    fetchRequests(currentPage.value, pageSize.value)
  } catch (error) {
    console.error('处理审核请求失败:', error)
    snackbar.showMessage('处理审核请求失败', 'error')
  }
}

// 时间验证相关
const timeError = ref('')

// 处理快速选择时间范围变化
const handleTimeRangeChange = (value: string | null) => {
  if (value) {
    filters.value.startDate = null
    filters.value.endDate = null
    timeError.value = ''
  }
}

// 处理自定义时间变化
const handleCustomTimeChange = () => {
  filters.value.timeRange = null
  
  if (!filters.value.startDate || !filters.value.endDate) {
    timeError.value = '开始时间和结束时间不能为空'
    return
  }

  const startTime = new Date(filters.value.startDate).getTime()
  const endTime = new Date(filters.value.endDate).getTime()
  
  if (startTime >= endTime) {
    timeError.value = '开始时间必须早于结束时间'
  } else {
    timeError.value = ''
  }
}

// 重置筛选条件
const resetFilters = () => {
  filters.value = {
    status: null,
    taskType: null,
    timeRange: null,
    startDate: null,
    endDate: null
  }
  timeError.value = ''
  currentPage.value = 1
  pageSize.value = 10
  fetchRequests(1, 10)
  showFilterDialog.value = false
}

// 应用筛选条件
const applyFilters = () => {
  if (timeError.value) {
    return
  }
  
  currentPage.value = 1
  pageSize.value = 10
  fetchRequests(1, 10)
  showFilterDialog.value = false
}

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1
  pageSize.value = 10
  fetchRequests(1, 10)
}

// 从后端获取审核请求数据
const fetchRequests = async (page: number, pageSize: number) => {
  loading.value = true
  try {
    // 计算时间筛选
    let startTimeFilter: string | undefined
    let endTimeFilter: string | undefined
    if (filters.value.timeRange) {
      const now = Date.now()
      const ranges: Record<string, number> = {
        '1d': 24 * 60 * 60 * 1000,
        '7d': 7 * 24 * 60 * 60 * 1000,
        '30d': 30 * 24 * 60 * 60 * 1000,
        '90d': 90 * 24 * 60 * 60 * 1000,
        '365d': 365 * 24 * 60 * 60 * 1000
      }
      const rangeMs = ranges[filters.value.timeRange as keyof typeof ranges]
      startTimeFilter = formatDateFilter(now - rangeMs)
      endTimeFilter = formatDateFilter(now)
    } else if (filters.value.startDate && filters.value.endDate) {
      startTimeFilter = formatDateFilter(new Date(filters.value.startDate).getTime())
      endTimeFilter = formatDateFilter(new Date(filters.value.endDate).getTime())
    }

    const params = {
      page,
      page_size: pageSize,
      query: searchQuery.value || '',
      status: filters.value.status || '',
      taskType: filters.value.taskType || '',
      startTime: startTimeFilter,
      endTime: endTimeFilter
    }
    const response = await reviewApi.getReviewRequests(params)
    const { requests: requestList, current_page, total_pages, total_requests } = response.data
    
    requests.value = requestList.map((request: any) => ({
      id: request.id,
      username: request.username,
      avatar: resolveImageUrl(request.avatar),
      state: request.state,
      file_type: request.file_type,
      time: request.time,
      task_type: request.task_type,
      task_type_label: request.task_type_label
    }))
    
    currentPage.value = current_page
    totalPages.value = total_pages
    totalRequests.value = total_requests
  } catch (error) {
    console.error('获取审核请求失败:', error)
    snackbar.showMessage('获取审核请求失败 - API可能未实现', 'error')
    // 设置默认值以避免页面卡住
    requests.value = []
    totalRequests.value = 0
    totalPages.value = 0
  } finally {
    loading.value = false
  }
}

// 处理页码变化
const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchRequests(page, pageSize.value)
}

// 处理每页数量变化
const handlePageSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  fetchRequests(1, size)
}

// 时间格式化，用于筛选条件
const formatDateFilter = (timestamp: number) => {
  const date = new Date(timestamp)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

// 初始化
onMounted(() => {
  fetchRequests(currentPage.value, pageSize.value)
})

onBeforeUnmount(() => {
  if (previewBlobUrl.value) {
    URL.revokeObjectURL(previewBlobUrl.value)
  }
})
</script>

<style scoped>
.v-card {
  border-radius: 12px;
  overflow: hidden;
}

.state-chip {
  font-size: 12px;
  padding: 0 12px;
  font-weight: 500;
}

.v-btn.v-btn--size-small {
  width: 32px;
  height: 32px;
  padding: 0;
  border-radius: 8px;
}

.v-btn--icon.v-btn--size-small .v-icon {
  font-size: 18px;
}

:deep(.v-data-table) {
  border-radius: 12px;
  width: 100%;
}

:deep(.v-data-table-header) {
  background-color: rgb(var(--v-theme-surface-variant));
}

:deep(.v-data-table-header th) {
  font-weight: 600;
  font-size: 14px;
  color: rgb(var(--v-theme-on-surface));
  white-space: nowrap;
}

:deep(.v-data-table__tr td) {
  white-space: nowrap;
}

:deep(.v-data-table__tr:hover) {
  background-color: rgba(var(--v-theme-on-surface), 0.04);
}

:deep(.v-chip) {
  font-weight: 500;
}

.search-input {
  max-width: 400px;
}

:deep(.v-text-field .v-field__input) {
  min-height: 40px;
}

:deep(.v-btn--variant-outlined) {
  border-color: rgb(var(--v-theme-outline));
}

:deep(.v-select .v-field__input) {
  min-height: 40px;
}

:deep(.v-select .v-field__append-inner) {
  padding-top: 0;
}

/* 资源预览侧边面板 */
.preview-side-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 520px;
  height: 100vh;
  background: rgb(var(--v-theme-surface));
  z-index: 9999;
  box-shadow: -4px 0 16px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
}

.preview-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid rgb(var(--v-theme-border));
  flex-shrink: 0;
}

.preview-panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.text-preview-content {
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 75vh;
  overflow-y: auto;
  font-size: 13px;
  line-height: 1.6;
  padding: 12px;
  background: rgb(var(--v-theme-surface-variant));
  border-radius: 8px;
}

.slide-panel-enter-active,
.slide-panel-leave-active {
  transition: transform 0.3s ease;
}

.slide-panel-enter-from,
.slide-panel-leave-to {
  transform: translateX(100%);
}

/* 段落详情侧边面板 */
.paragraph-side-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 700px;
  height: 100vh;
  background: rgb(var(--v-theme-surface));
  z-index: 10000;
  box-shadow: -4px 0 16px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
}

.paragraph-item-clickable {
  cursor: pointer;
  transition: background 0.15s ease;
}

.paragraph-item-clickable:hover {
  background: rgb(var(--v-theme-error), 0.08) !important;
}
</style> 