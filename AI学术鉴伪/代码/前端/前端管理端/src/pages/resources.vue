<template>
  <v-container>
    <!-- 标题 -->
    <v-row class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold">学术资源管理</h1>
      </v-col>
    </v-row>

    <!-- 筛选条件区域 - 浅蓝色背景框 -->
    <v-card class="mb-4 rounded-lg" color="blue-lighten-5" variant="flat">
      <v-card-text>
        <!-- 搜索栏 - 关键词搜索 -->
        <v-row class="mb-4">
          <v-col cols="12" md="10">
            <v-text-field
              v-model="searchQuery"
              label="关键词搜索"
              placeholder="按「标题 / ID / 作者 / 编辑 / 组织」检索"
              variant="outlined"
              color="primary"
              bg-color="surface"
              density="comfortable"
              clearable
              hide-details
              @keyup.enter="handleSearch"
            >
              <template v-slot:prepend-inner>
                <v-icon color="primary" class="mr-2">mdi-text-search</v-icon>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="12" md="2">
            <v-btn
              color="primary"
              prepend-icon="mdi-filter-multiple"
              variant="elevated"
              size="large"
              class="h-100 w-100"
              @click="handleSearch"
            >
              筛选
            </v-btn>
          </v-col>
        </v-row>

        <!-- 筛选条件行 -->
        <v-row>
          <!-- 学科分类 -->
          <v-col cols="12" sm="6" md="2">
            <v-menu v-model="subjectMenu" :close-on-content-click="false" open-on-hover>
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-bind="props"
                  :model-value="getSubjectName(filters.subject)"
                  label="学科分类"
                  variant="outlined"
                  density="comfortable"
                  color="indigo"
                  bg-color="surface"
                  readonly
                  hide-details
                >
                  <template v-slot:prepend-inner>
                    <v-icon color="indigo" class="mr-2">mdi-bookshelf</v-icon>
                  </template>
                  <template v-if="filters.subject" v-slot:append-inner>
                    <v-icon @click.stop="filters.subject = null; handleFilterChange()" size="small" color="error">mdi-close-circle</v-icon>
                  </template>
                </v-text-field>
              </template>
              <v-list>
                <v-list-item
                  v-for="item in subjectOptions"
                  :key="item.value"
                  @click="filters.subject = item.value; subjectMenu = false; handleFilterChange()"
                >
                  <v-list-item-title>
                    <v-icon size="small" class="mr-2" color="indigo">mdi-bookshelf</v-icon>
                    {{ item.title }}
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-col>

          <!-- 检测结果 -->
          <v-col cols="12" sm="6" md="2">
            <v-menu v-model="detectionResultMenu" :close-on-content-click="false" open-on-hover>
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-bind="props"
                  :model-value="detectionResultOptions.find(o => o.value === filters.detectionResult)?.title || ''"
                  label="检测结果"
                  variant="outlined"
                  density="comfortable"
                  color="teal"
                  bg-color="surface"
                  readonly
                  hide-details
                >
                  <template v-slot:prepend-inner>
                    <v-icon color="teal" class="mr-2">mdi-file-document-check</v-icon>
                  </template>
                  <template v-if="filters.detectionResult" v-slot:append-inner>
                    <v-icon @click.stop="filters.detectionResult = null; handleFilterChange()" size="small" color="error">mdi-close-circle</v-icon>
                  </template>
                </v-text-field>
              </template>
              <v-list>
                <v-list-item
                  v-for="item in detectionResultOptions"
                  :key="item.value"
                  @click="filters.detectionResult = item.value; detectionResultMenu = false; handleFilterChange()"
                >
                  <v-list-item-title>
                    <v-icon size="small" class="mr-2" :color="item.color">
                      {{ item.icon }}
                    </v-icon>
                    {{ item.title }}
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-col>

          <!-- 开始时间 -->
          <v-col cols="12" sm="6" md="2">
            <v-text-field
              v-model="filters.startTime"
              type="datetime-local"
              label="开始时间"
              variant="outlined"
              density="compact"
              color="blue"
              bg-color="surface"
              clearable
              hide-details
              @update:model-value="handleFilterChange"
            >
              <template v-slot:prepend-inner>
                <v-icon color="blue" class="mr-2">mdi-calendar-start</v-icon>
              </template>
            </v-text-field>
          </v-col>

          <!-- 结束时间 -->
          <v-col cols="12" sm="6" md="2">
            <v-text-field
              v-model="filters.endTime"
              type="datetime-local"
              label="结束时间"
              variant="outlined"
              density="compact"
              color="blue"
              bg-color="surface"
              clearable
              hide-details
              @update:model-value="handleFilterChange"
            >
              <template v-slot:prepend-inner>
                <v-icon color="blue" class="mr-2">mdi-calendar-end</v-icon>
              </template>
            </v-text-field>
          </v-col>

          <!-- 重置按钮 -->
          <v-col cols="12" sm="6" md="2">
            <v-btn
              variant="elevated"
              color="grey"
              prepend-icon="mdi-refresh"
              size="large"
              class="h-100 w-100"
              @click="clearAllFilters"
            >
              重置
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- 左右栏布局 -->
    <v-row>
      <!-- 左侧边栏 - 资源类型选择和数据统计 -->
      <v-col cols="12" md="2">
        <div class="d-flex flex-column gap-4">
          <!-- 资源类型选择 -->
          <v-card class="rounded-lg" variant="elevated">
            <v-card-title class="primary white--text pa-4">
              <div class="d-flex align-center gap-2">
                <v-icon>mdi-filter-outline</v-icon>
                <span>资源类型</span>
              </div>
            </v-card-title>
            <v-card-text class="pt-4">
              <v-select
                v-model="selectedType"
                :items="resourceTypes"
                item-title="title"
                item-value="value"
                variant="outlined"
                density="comfortable"
                color="primary"
                clearable
                hide-details
                @update:model-value="loadResources"
              >
                <template v-slot:selection="{ item }">
                  <div class="d-flex align-center">
                    <v-icon size="small" class="mr-2" :color="item.raw.color">{{ item.raw.icon }}</v-icon>
                    <span>{{ item.raw.title }}</span>
                  </div>
                </template>
                <template v-slot:item="{ props, item }">
                  <v-list-item v-bind="props">
                    <template v-slot:prepend>
                      <v-icon :color="item.raw.color">{{ item.raw.icon }}</v-icon>
                    </template>
                    <v-list-item-title>{{ item.raw.title }}</v-list-item-title>
                    <v-list-item-subtitle>{{ item.raw.count }} 条</v-list-item-subtitle>
                  </v-list-item>
                </template>
              </v-select>
            </v-card-text>
          </v-card>

          <!-- 数据统计 -->
          <v-card class="rounded-lg" variant="elevated">
            <v-card-title class="info white--text pa-4">
              <div class="d-flex align-center gap-2">
                <v-icon>mdi-chart-box-outline</v-icon>
                <span>数据统计</span>
              </div>
            </v-card-title>
            <v-card-text>
              <!-- 全部资源统计 -->
              <div v-if="!selectedType">
                <div class="mb-3">
                  <div class="text-caption text-medium-emphasis">筛选结果总数</div>
                  <div class="text-h4 font-weight-bold primary--text">{{ filteredResources.length }}</div>
                </div>

                <v-divider class="mb-3"></v-divider>

                <div class="mb-3">
                  <div class="text-caption text-medium-emphasis">论文数量</div>
                  <div class="text-h6 font-weight-bold">{{ getTypeCount('paper') }}</div>
                </div>

                <div class="mb-3">
                  <div class="text-caption text-medium-emphasis">Review数量</div>
                  <div class="text-h6 font-weight-bold">{{ getTypeCount('review') }}</div>
                </div>

                <div class="mb-3">
                  <div class="text-caption text-medium-emphasis">图片数量</div>
                  <div class="text-h6 font-weight-bold">{{ getTypeCount('image') }}</div>
                </div>

                <div class="mb-3">
                  <div class="text-caption text-medium-emphasis">综合资源数量</div>
                  <div class="text-h6 font-weight-bold">{{ getTypeCount('comprehensive') }}</div>
                </div>

                <v-divider class="mb-3"></v-divider>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">真实资源</div>
                  <div class="text-body-2 success--text font-weight-bold">{{ getDetectionResultCount('real') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">虚假资源</div>
                  <div class="text-body-2 error--text font-weight-bold">{{ getDetectionResultCount('fake') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">未检测</div>
                  <div class="text-body-2 grey--text font-weight-bold">{{ getDetectionResultCount('undetected') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">检测失败</div>
                  <div class="text-body-2 warning--text font-weight-bold">{{ getDetectionResultCount('failed') }}</div>
                </div>

                <div>
                  <div class="text-caption text-medium-emphasis">检测中</div>
                  <div class="text-body-2 info--text font-weight-bold">{{ getDetectionResultCount('detecting') }}</div>
                </div>
              </div>

              <!-- 论文资源统计 -->
              <div v-else-if="selectedType === 'paper'">
                <div class="mb-3">
                  <div class="text-caption text-medium-emphasis">论文总数</div>
                  <div class="text-h4 font-weight-bold primary--text">{{ filteredResources.length }}</div>
                </div>

                <v-divider class="mb-3"></v-divider>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">真实论文</div>
                  <div class="text-body-2 success--text font-weight-bold">{{ getDetectionResultCount('real') }}</div>
                </div>

                <div>
                  <div class="text-caption text-medium-emphasis">虚假论文</div>
                  <div class="text-body-2 error--text font-weight-bold">{{ getDetectionResultCount('fake') }}</div>
                </div>
              </div>

              <!-- Review资源统计 -->
              <div v-else-if="selectedType === 'review'">
                <div class="mb-3">
                  <div class="text-caption text-medium-emphasis">Review总数</div>
                  <div class="text-h4 font-weight-bold primary--text">{{ filteredResources.length }}</div>
                </div>

                <v-divider class="mb-3"></v-divider>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">真实Review</div>
                  <div class="text-body-2 success--text font-weight-bold">{{ getDetectionResultCount('real') }}</div>
                </div>

                <div>
                  <div class="text-caption text-medium-emphasis">虚假Review</div>
                  <div class="text-body-2 error--text font-weight-bold">{{ getDetectionResultCount('fake') }}</div>
                </div>
              </div>

              <!-- 图片资源统计 -->
              <div v-else-if="selectedType === 'image'">
                <div class="mb-3">
                  <div class="text-caption text-medium-emphasis">图片总数</div>
                  <div class="text-h4 font-weight-bold primary--text">{{ filteredResources.length }}</div>
                </div>

                <v-divider class="mb-3"></v-divider>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">真实图片</div>
                  <div class="text-body-2 success--text font-weight-bold">{{ getDetectionResultCount('real') }}</div>
                </div>

                <div>
                  <div class="text-caption text-medium-emphasis">虚假图片</div>
                  <div class="text-body-2 error--text font-weight-bold">{{ getDetectionResultCount('fake') }}</div>
                </div>
              </div>

              <!-- 综合资源统计 -->
              <div v-else-if="selectedType === 'comprehensive'">
                <div class="mb-3">
                  <div class="text-caption text-medium-emphasis">综合资源总数</div>
                  <div class="text-h4 font-weight-bold primary--text">{{ filteredResources.length }}</div>
                </div>

                <v-divider class="mb-3"></v-divider>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">真实资源</div>
                  <div class="text-body-2 success--text font-weight-bold">{{ getDetectionResultCount('real') }}</div>
                </div>

                <div>
                  <div class="text-caption text-medium-emphasis">虚假资源</div>
                  <div class="text-body-2 error--text font-weight-bold">{{ getDetectionResultCount('fake') }}</div>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </div>
      </v-col>

      <!-- 右侧内容区 - 资源列表 -->
      <v-col cols="12" md="10">
        <v-card class="rounded-lg" variant="elevated">
          <v-card-text>
            <v-data-table
              :headers="resourceTableHeaders"
              :items="filteredResources"
              :loading="loading"
              :items-per-page="10"
              :search="searchQuery"
              density="comfortable"
              hover
              class="rounded-lg"
            >
              <template v-slot:bottom>
                <div class="d-flex justify-center align-center pa-4">
                  <v-data-table-footer
                    :items-per-page-options="[5, 10, 20, 50]"
                  ></v-data-table-footer>
                </div>
              </template>
              <template v-slot:item.id="{ item }">
                <span class="font-weight-medium">#{{ item.id }}</span>
              </template>

              <template v-slot:item.title="{ item }">
                <span class="text-truncate">{{ item.title || item.file_name || '-' }}</span>
              </template>

              <template v-slot:item.type="{ item }">
                <v-chip :color="getTypeColor(item.type)" size="small">
                  {{ getTypeName(item.type) }}
                </v-chip>
              </template>

              <template v-slot:item.author="{ item }">
                <span>{{ item.author || item.uploader_name || '-' }}</span>
              </template>

              <template v-slot:item.organization="{ item }">
                <span>{{ item.organization || '-' }}</span>
              </template>

              <template v-slot:item.subject="{ item }">
                <v-chip size="small" :color="getSubjectColor(item.subject)">
                  {{ getSubjectName(item.subject) }}
                </v-chip>
              </template>

              <template v-slot:item.detection_result="{ item }">
                <v-chip
                  :color="getDetectionResultColor(item)"
                  size="small"
                >
                  {{ getDetectionResultText(item) }}
                </v-chip>
              </template>

              <template v-slot:item.detection_type="{ item }">
                <v-chip
                  :color="getDetectionTypeColor(item.detection_type)"
                  size="small"
                  variant="tonal"
                >
                  {{ item.detection_type }}
                </v-chip>
              </template>

              <template v-slot:item.related_resources="{ item }">
                <v-btn
                  size="small"
                  variant="text"
                  color="primary"
                  @click="openRelatedResourcesDialog(item)"
                  :disabled="!item.related_resources || item.related_resources.length === 0"
                >
                  {{ item.related_resources ? item.related_resources.length : 0 }} 个资源
                  <v-icon end size="small">mdi-open-in-new</v-icon>
                </v-btn>
              </template>

              <template v-slot:item.upload_time="{ item }">
                <span>{{ formatTime(item.upload_time) }}</span>
              </template>

              <template v-slot:item.actions="{ item }">
                <v-tooltip text="资源预览" location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn icon variant="text" size="small" color="info" v-bind="props" @click="previewResource(item)">
                      <v-icon>mdi-file-find</v-icon>
                    </v-btn>
                  </template>
                </v-tooltip>
                <v-tooltip text="检测结果" location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn icon variant="text" size="small" color="warning" v-bind="props" @click="viewDetectionResult(item)" :disabled="!item.task_id">
                      <v-icon>mdi-magnify-scan</v-icon>
                    </v-btn>
                  </template>
                </v-tooltip>
                <v-tooltip text="删除" location="top">
                  <template v-slot:activator="{ props }">
                    <v-btn icon variant="text" size="small" color="error" v-bind="props" @click="openDeleteDialog(item)">
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-tooltip>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- 资源详情对话框 -->
    <v-dialog v-model="showDetailDialog" max-width="800">
      <v-card v-if="selectedResource">
        <v-card-title class="d-flex justify-space-between align-center">
          <span class="text-h5 font-weight-bold">资源详情</span>
          <v-btn icon @click="showDetailDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text>
          <v-row class="mb-4">
            <v-col cols="12" sm="6">
              <div class="mb-2">
                <span class="text-medium-emphasis">资源名称：</span>
                <span class="font-weight-bold">{{ selectedResource.file_name }}</span>
              </div>
              <div class="mb-2">
                <span class="text-medium-emphasis">资源类型：</span>
                <v-chip :color="getTypeColor(selectedResource.type)" size="small" class="ml-2">
                  {{ getTypeName(selectedResource.type) }}
                </v-chip>
              </div>
              <div class="mb-2">
                <span class="text-medium-emphasis">上传用户：</span>
                <span class="font-weight-bold">{{ selectedResource.uploader_name }}</span>
              </div>
            </v-col>
            <v-col cols="12" sm="6">
              <div class="mb-2">
                <span class="text-medium-emphasis">上传时间：</span>
                <span class="font-weight-bold">{{ formatTime(selectedResource.upload_time) }}</span>
              </div>
              <div class="mb-2">
                <span class="text-medium-emphasis">检测状态：</span>
                <v-chip
                  :color="getDetectionStatusColor(selectedResource.detection_status)"
                  size="small"
                  class="ml-2"
                >
                  {{ getDetectionStatusName(selectedResource.detection_status) }}
                </v-chip>
              </div>
              <div class="mb-2">
                <span class="text-medium-emphasis">检测结果：</span>
                <span class="font-weight-bold">{{ selectedResource.detection_result || '-' }}</span>
              </div>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            v-if="selectedResource.detection_status === 'completed' && selectedResource.task_id"
            color="teal"
            variant="elevated"
            prepend-icon="mdi-magnify-scan"
            @click="viewDetectionResult(selectedResource)"
          >
            查看检测结果
          </v-btn>
          <v-btn color="primary" @click="showDetailDialog = false">
            确定
          </v-btn>
        </v-card-actions>
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

          <!-- 检测结果内容 - 使用专用组件 -->
          <div v-else>
            <!-- 图片检测 -->
            <ImageDetectionResult
              v-if="detectionResultData.task_type === 'image'"
              :task_id="String(detectionResultData.task_id)"
              :detection_time="detectionResultData.detection_time || ''"
            />
            <!-- 论文/Review 文本检测 -->
            <TextDetectionResult
              v-else-if="detectionResultData.task_type === 'paper_text' || detectionResultData.task_type === 'review_text'"
              :task-meta="detectionResultData"
              :task-id="detectionResultData.task_id"
            />
            <!-- 综合材料检测 -->
            <MultiMaterialResult
              v-else-if="detectionResultData.task_type === 'multi_material'"
              :task-meta="detectionResultData"
              :task-id="detectionResultData.task_id"
            />
            <!-- 未知类型兜底 -->
            <div v-else class="text-center pa-8 text-grey">
              <v-icon size="64" color="grey-lighten-1">mdi-help-circle-outline</v-icon>
              <div class="text-h6 mt-4">未知检测类型：{{ detectionResultData.task_type }}</div>
            </div>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="showDetectionResultDialog = false">
            关闭
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 删除确认对话框 -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h6 font-weight-bold">确认删除</v-card-title>
        <v-card-text>
          确定要删除该资源吗？此操作不可撤销。
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="showDeleteDialog = false">取消</v-btn>
          <v-btn color="error" @click="deleteResource">删除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 资源预览对话框 -->
    <v-dialog v-model="showPreviewDialog" max-width="900" scrollable>
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span class="text-h5 font-weight-bold">资源预览</span>
          <v-btn icon @click="showPreviewDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text style="max-height: 75vh;">
          <!-- 加载中 -->
          <div v-if="previewLoading" class="d-flex justify-center align-center pa-8">
            <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
            <span class="ml-4 text-body-1">正在加载资源预览...</span>
          </div>
          <!-- 无数据 -->
          <div v-else-if="!previewUrl" class="text-center pa-8 text-grey">
            <v-icon size="64" color="grey-lighten-1">mdi-file-question-outline</v-icon>
            <div class="text-h6 mt-4">无法预览该资源</div>
          </div>
          <!-- 图片预览 -->
          <div v-else-if="previewType === 'image'" class="text-center">
            <v-img :src="previewUrl" contain max-height="65vh"></v-img>
          </div>
          <!-- PDF预览 -->
          <div v-else-if="previewType === 'pdf'" class="text-center">
            <iframe :src="previewUrl" width="100%" height="65vh" style="border: none;"></iframe>
          </div>
          <!-- 文本预览 -->
          <div v-else-if="previewType === 'text'" class="pa-4">
            <pre class="text-body-2" style="white-space: pre-wrap; word-break: break-word; max-height: 60vh; overflow-y: auto;">{{ previewTextContent }}</pre>
          </div>
          <!-- 其他文件：提供下载 -->
          <div v-else class="text-center pa-8">
            <v-icon size="64" color="primary">mdi-file-download-outline</v-icon>
            <div class="text-h6 mt-4 mb-2">{{ previewFileName }}</div>
            <div class="text-body-2 text-grey mb-4">该文件格式不支持在线预览</div>
            <v-btn color="primary" :href="previewUrl" target="_blank">
              <v-icon class="mr-2">mdi-download</v-icon>
              下载文件
            </v-btn>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" variant="text" @click="showPreviewDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 关联资源对话框 -->
    <v-dialog v-model="showRelatedResourcesDialog" max-width="1000" scrollable>
      <v-card>
        <v-card-title class="d-flex justify-space-between align-center">
          <span class="text-h5 font-weight-bold">关联资源</span>
          <v-btn icon @click="showRelatedResourcesDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text style="max-height: 70vh;">
          <v-data-table
            v-if="relatedResourcesList.length > 0"
            :items="relatedResourcesList"
            :headers="relatedResourceHeaders"
            item-value="id"
            density="comfortable"
            hover
            class="elevation-1"
          >
            <template v-slot:item.id="{ item }">
              <span class="font-weight-medium">{{ item.id }}</span>
            </template>
            <template v-slot:item.title="{ item }">
              <span>{{ item.title || item.file_name || '-' }}</span>
            </template>
            <template v-slot:item.type="{ item }">
              <v-chip :color="getTypeColor(item.type)" size="small">
                {{ getTypeName(item.type) }}
              </v-chip>
            </template>
            <template v-slot:item.actions="{ item }">
              <v-tooltip text="资源预览" location="top">
                <template v-slot:activator="{ props }">
                  <v-btn icon variant="text" size="small" color="info" v-bind="props" @click="previewRelatedResource(item)">
                    <v-icon>mdi-file-find</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
              <v-tooltip text="检测结果" location="top">
                <template v-slot:activator="{ props }">
                  <v-btn icon variant="text" size="small" color="warning" v-bind="props" @click="viewRelatedDetectionResult(item)" :disabled="!item.task_id">
                    <v-icon>mdi-magnify-scan</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
              <v-tooltip text="删除" location="top">
                <template v-slot:activator="{ props }">
                  <v-btn icon variant="text" size="small" color="error" v-bind="props" @click="deleteRelatedResource(item)">
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
            </template>
          </v-data-table>
          <div v-else class="text-center pa-8 text-grey">
            <v-icon size="64" color="grey-lighten-1">mdi-file-search-outline</v-icon>
            <div class="text-h6 mt-4">暂无关联资源</div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="showRelatedResourcesDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useSnackbarStore } from '@/stores/snackbar'
import resourceApi, { type Resource, type StructuredResult, type RelatedResource } from '@/api/resource'
import ImageDetectionResult from '@/components/detection/ImageDetectionResult.vue'
import TextDetectionResult from '@/components/detection/TextDetectionResult.vue'
import MultiMaterialResult from '@/components/detection/MultiMaterialResult.vue'

const snackbar = useSnackbarStore()

// 主页面搜索
const searchQuery = ref('')

// 菜单状态
const detectionResultMenu = ref(false)
const subjectMenu = ref(false)

// 筛选条件
const filters = ref<{
  subject: string | null
  detectionResult: string | null
  startTime: Date | null
  endTime: Date | null
}>({
  subject: null,
  detectionResult: null,
  startTime: null,
  endTime: null
})

// 选中的资源类型
const selectedType = ref<string | null>(null)

// 资源数据
const resources = ref<Resource[]>([])
const loading = ref(false)

// 资源详情
const showDetailDialog = ref(false)
const showDeleteDialog = ref(false)
const selectedResource = ref<Resource | null>(null)

// 检测结果对话框
const showDetectionResultDialog = ref(false)
const detectionResultLoading = ref(false)
const detectionResultData = ref<StructuredResult | null>(null)

// 资源预览对话框
const showPreviewDialog = ref(false)
const previewLoading = ref(false)
const previewUrl = ref<string | null>(null)
const previewType = ref<'image' | 'pdf' | 'text' | 'other'>('other')
const previewTextContent = ref('')
const previewFileName = ref('')

// 关联资源对话框
const showRelatedResourcesDialog = ref(false)
const relatedResourceHeaders = [
  { title: 'ID', key: 'id', align: 'center' as const, sortable: true, width: '120px' },
  { title: '标题', key: 'title', align: 'start' as const, sortable: true },
  { title: '类型', key: 'type', align: 'center' as const, sortable: true },
  { title: '操作', key: 'actions', align: 'center' as const, sortable: false, width: '200px' },
]
const relatedResourcesList = ref<any[]>([])


// 选项配置
const subjectOptions = [
  { title: '全部学科', value: 'all' },
  { title: '计算机科学', value: 'computer_science' },
  { title: '人工智能', value: 'artificial_intelligence' },
  { title: '数学', value: 'mathematics' },
  { title: '物理学', value: 'physics' },
  { title: '化学', value: 'chemistry' },
  { title: '生物学', value: 'biology' },
  { title: '医学', value: 'medicine' },
  { title: '工程学', value: 'engineering' },
  { title: '图形学', value: 'graphics' },
  { title: '其他', value: 'other' }
]

const detectionResultOptions = [
  { title: '真实', value: 'real', icon: 'mdi-check-circle', color: 'success' },
  { title: '虚假', value: 'fake', icon: 'mdi-alert-circle', color: 'error' },
  { title: '未检测', value: 'undetected', icon: 'mdi-minus-circle', color: 'grey' },
  { title: '检测失败', value: 'failed', icon: 'mdi-close-circle', color: 'warning' },
  { title: '检测中', value: 'detecting', icon: 'mdi-progress-clock', color: 'info' },
]

// 资源类型配置
const resourceTypes = computed(() => [
  { title: '全部资源', value: null, icon: 'mdi-database', color: 'grey-darken-1', count: resources.value.length },
  { title: '论文', value: 'paper', icon: 'mdi-file-document', color: 'primary', count: resources.value.filter(r => r.type === 'paper').length },
  { title: 'Review', value: 'review', icon: 'mdi-comment-text', color: 'success', count: resources.value.filter(r => r.type === 'review').length },
  { title: '图片', value: 'image', icon: 'mdi-image', color: 'warning', count: resources.value.filter(r => r.type === 'image').length },
  { title: '综合资源', value: 'comprehensive', icon: 'mdi-folder-multiple', color: 'info', count: resources.value.filter(r => r.type === 'comprehensive').length }
])

// 资源表格表头
const resourceTableHeaders = [
  { title: 'ID', key: 'id', align: 'start' as const, sortable: true },
  { title: '标题', key: 'title', align: 'start' as const, sortable: true },
  { title: '类型', key: 'type', align: 'center' as const, sortable: true },
  { title: '作者', key: 'author', align: 'start' as const, sortable: true },
  { title: '组织', key: 'organization', align: 'start' as const, sortable: true },
  { title: '学科', key: 'subject', align: 'center' as const, sortable: true },
  { title: '检测结果', key: 'detection_result', align: 'center' as const, sortable: true },
  { title: '检测类型', key: 'detection_type', align: 'center' as const, sortable: true },
  { title: '关联资源', key: 'related_resources', align: 'center' as const, sortable: false },
  { title: '更新时间', key: 'upload_time', align: 'center' as const, sortable: true },
  { title: '操作', key: 'actions', align: 'center' as const, sortable: false }
]

// 过滤后的资源数据
const filteredResources = computed(() => {
  let filtered = [...resources.value]
  
  // 根据选中的类型过滤
  if (selectedType.value) {
    filtered = filtered.filter(r => r.type === selectedType.value)
  }
  
  // 根据筛选条件过滤
  if (filters.value.subject && filters.value.subject !== 'all') {
    filtered = filtered.filter(r => r.subject === filters.value.subject)
  }
  
  if (filters.value.detectionResult) {
    const dr = filters.value.detectionResult
    if (dr === 'undetected') {
      filtered = filtered.filter(r => r.detection_result === null && r.detection_status !== 'detecting' && r.detection_status !== 'failed')
    } else if (dr === 'detecting') {
      filtered = filtered.filter(r => r.detection_status === 'detecting')
    } else if (dr === 'failed') {
      filtered = filtered.filter(r => r.detection_result === 'failed' || r.detection_status === 'failed')
    } else {
      filtered = filtered.filter(r => r.detection_result === dr)
    }
  }
  
  if (filters.value.startTime) {
    filtered = filtered.filter(r => new Date(r.upload_time) >= filters.value.startTime!)
  }
  
  if (filters.value.endTime) {
    filtered = filtered.filter(r => new Date(r.upload_time) <= filters.value.endTime!)
  }
  
  return filtered
})

// 选择资源类型
const selectType = (type: string | null) => {
  selectedType.value = type
  loadResources()
}

// 获取学科颜色
const getSubjectColor = (subject?: string | null) => {
  switch (subject) {
    case 'biology':
      return 'success'
    case 'medicine':
      return 'info'
    case 'chemistry':
      return 'warning'
    case 'graphics':
      return 'primary'
    case 'computer_science':
      return 'indigo'
    case 'artificial_intelligence':
      return 'deep-purple'
    case 'mathematics':
      return 'teal'
    case 'physics':
      return 'blue-grey'
    case 'engineering':
      return 'brown'
    case 'other':
      return 'grey'
    default:
      return 'grey'
  }
}

// 获取学科名称
const getSubjectName = (subject?: string | null) => {
  if (!subject) return '全部学科'
  const option = subjectOptions.find(opt => opt.value === subject)
  return option ? option.title : subject
}

// 获取资源类型名称
const getTypeName = (type: string | null) => {
  if (!type) return '全部类型'
  const names: { [key: string]: string } = {
    paper: '论文',
    review: 'Review',
    image: '图片',
    comprehensive: '综合资源'
  }
  return names[type] || type
}

// 获取资源类型颜色
const getTypeColor = (type: string | null) => {
  const colors: { [key: string]: string } = {
    paper: 'primary',
    review: 'success',
    image: 'warning',
    comprehensive: 'info'
  }
  return type ? colors[type] || 'grey' : 'grey'
}

// 获取检测类型颜色
const getDetectionTypeColor = (type: string) => {
  const colors: { [key: string]: string } = {
    '图像': 'warning',
    '论文': 'primary',
    'review': 'success',
    '综合': 'info',
    '未检测': 'grey'
  }
  return colors[type] || 'grey'
}

// 打开关联资源对话框
const openRelatedResourcesDialog = (resource: Resource) => {
  relatedResourcesList.value = resource.related_resources || []
  showRelatedResourcesDialog.value = true
}

// 获取关联资源类型图标
const getRelatedTypeIcon = (type: string) => {
  const icons: { [key: string]: string } = {
    paper: 'mdi-file-document',
    review: 'mdi-comment-text',
    image: 'mdi-image',
    comprehensive: 'mdi-folder-multiple'
  }
  return icons[type] || 'mdi-file'
}

// 获取关联资源类型颜色
const getRelatedTypeColor = (type: string) => {
  const colors: { [key: string]: string } = {
    paper: 'primary',
    review: 'success',
    image: 'warning',
    comprehensive: 'info'
  }
  return colors[type] || 'grey'
}

// 获取检测状态名称
const getDetectionStatusName = (status: string | null) => {
  if (!status) return '未知'
  const names: { [key: string]: string } = {
    pending: '待检测',
    detecting: '检测中',
    completed: '已完成',
    failed: '失败'
  }
  return names[status] || status
}

// 获取检测状态颜色
const getDetectionStatusColor = (status: string | null) => {
  const colors: { [key: string]: string } = {
    pending: 'grey',
    detecting: 'info',
    completed: 'success',
    failed: 'error'
  }
  return status ? colors[status] || 'grey' : 'grey'
}

// 格式化时间
const formatTime = (time: string | null) => {
  if (!time) return '-'
  const date = new Date(time)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day} ${hours}:${minutes}`
}

// 加载资源数据
const loadResources = async () => {
  loading.value = true
  try {
    const params: any = { 
      page: 1, 
      page_size: 200,
      query: searchQuery.value || undefined,
      type: selectedType.value || undefined,
      classification: filters.value.subject && filters.value.subject !== 'all' ? filters.value.subject : undefined,
      detection_result: filters.value.detectionResult || undefined,
      start_time: filters.value.startTime || undefined,
      end_time: filters.value.endTime || undefined
    }
    const response = await resourceApi.getResources(params)
    resources.value = response.data.resources || []
  } catch (error) {
    console.error('加载资源失败:', error)
    snackbar.showMessage('加载资源失败', 'error')
    // 使用模拟数据
    resources.value = [
      {
        id: 1,
        file_name: '深度学习在图像识别中的应用.pdf',
        type: 'paper',
        title: '深度学习在图像识别中的应用',
        author: '张三',
        organization: '北京大学',
        subject: 'computer_science',
        detection_result: 'real',
        detection_status: 'completed',
        detection_type: '论文',
        related_resources: [],
        upload_time: '2026-04-15T10:30:00',
        uploader_name: '张三',
        uploader_id: 1,
        uploader_email: 'zhangsan@example.com',
        file_format: 'pdf',
        classification: 'paper',
        detection_time: '2026-04-15T11:00:00',
        task_id: 1
      },
      {
        id: 2,
        file_name: '机器学习算法综述.pdf',
        type: 'paper',
        title: '机器学习算法综述',
        author: '王五',
        organization: '清华大学',
        subject: 'artificial_intelligence',
        detection_result: 'real',
        detection_status: 'completed',
        detection_type: '论文',
        related_resources: [],
        upload_time: '2026-04-16T14:20:00',
        uploader_name: '王五',
        uploader_id: 2,
        uploader_email: 'wangwu@example.com',
        file_format: 'pdf',
        classification: 'paper',
        detection_time: '2026-04-16T15:00:00',
        task_id: 2
      }
    ]
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  loadResources()
}

// 筛选条件改变
const handleFilterChange = () => {
  loadResources()
}

// 清除所有筛选条件
const clearAllFilters = () => {
  searchQuery.value = ''
  filters.value = {
    subject: null,
    detectionResult: null,
    startTime: null,
    endTime: null
  }
  selectedType.value = null
  loadResources()
}

// 关联资源操作
const viewRelatedDetail = async (res: RelatedResource) => {
  try {
    const response = await resourceApi.getResourceDetail(res.id)
    selectedResource.value = response.data
    showDetailDialog.value = true
  } catch (error) {
    console.error('获取资源详情失败:', error)
    snackbar.showMessage('获取资源详情失败', 'error')
  }
}

const previewRelatedResource = async (res: RelatedResource) => {
  showPreviewDialog.value = true
  previewLoading.value = true
  previewUrl.value = null
  previewType.value = 'other'
  previewTextContent.value = ''
  previewFileName.value = res.title || res.file_name || ''

  try {
    const fileType = res.type === 'image' ? 'image' : 'file'
    const response = await resourceApi.previewResource(res.id, fileType)
    const blob = response.data as any
    const contentType = blob.type || ''

    if (res.type === 'image' || contentType.startsWith('image/')) {
      previewType.value = 'image'
      previewUrl.value = URL.createObjectURL(blob)
    } else if (contentType === 'application/pdf' || (res.file_name && res.file_name.toLowerCase().endsWith('.pdf'))) {
      previewType.value = 'pdf'
      previewUrl.value = URL.createObjectURL(blob)
    } else if (contentType.startsWith('text/') || (res.file_name && /\.(txt|md|csv|json|xml)$/i.test(res.file_name))) {
      previewType.value = 'text'
      previewUrl.value = URL.createObjectURL(blob)
      const text = await blob.text()
      previewTextContent.value = text
    } else {
      previewType.value = 'other'
      previewUrl.value = URL.createObjectURL(blob)
    }
  } catch (error: any) {
    console.error('预览资源失败:', error)
    if (error?.response?.status === 404) {
      snackbar.showMessage('资源文件不存在或已被删除', 'warning')
    } else {
      snackbar.showMessage('预览资源失败', 'error')
    }
    previewUrl.value = null
  } finally {
    previewLoading.value = false
  }
}

const viewRelatedDetectionResult = async (res: RelatedResource) => {
  if (!res.task_id) {
    snackbar.showMessage('该资源没有关联的检测任务', 'warning')
    return
  }
  showDetectionResultDialog.value = true
  detectionResultLoading.value = true
  detectionResultData.value = null
  try {
    const response = await resourceApi.getDetectionResult(res.task_id)
    detectionResultData.value = response.data
  } catch (error) {
    console.error('获取检测结果失败:', error)
    snackbar.showMessage('获取检测结果失败', 'error')
  } finally {
    detectionResultLoading.value = false
  }
}

const deleteRelatedResource = async (res: RelatedResource) => {
  if (!confirm(`确定要删除资源 "${res.title || res.file_name}" (ID: ${res.id}) 吗？此操作不可撤销。`)) return
  try {
    await resourceApi.deleteResource(res.id)
    snackbar.showMessage('删除成功', 'success')
    // Refresh related resources list by reloading resources
    loadResources()
  } catch (error) {
    console.error('删除资源失败:', error)
    snackbar.showMessage('删除失败', 'error')
  }
}

// 查看资源详情
const viewResource = (id: number) => {
  selectedResource.value = resources.value.find(r => r.id === id) || null
  if (selectedResource.value) {
    showDetailDialog.value = true
  }
}

// 打开删除对话框
const openDeleteDialog = (resource: Resource) => {
  selectedResource.value = resource
  showDeleteDialog.value = true
}

// 获取特定类型的资源数量
const getTypeCount = (type: string) => {
  return filteredResources.value.filter(r => r.type === type).length
}

// 获取特定检测结果的数量
const getDetectionResultColor = (item: Resource) => {
  if (item.detection_result === 'real') return 'success'
  if (item.detection_result === 'fake') return 'error'
  if (item.detection_status === 'detecting') return 'info'
  if (item.detection_status === 'failed' || item.detection_result === 'failed') return 'warning'
  return 'grey'
}

const getDetectionResultText = (item: Resource) => {
  if (item.detection_result === 'real') return '真实'
  if (item.detection_result === 'fake') return '虚假'
  if (item.detection_status === 'detecting') return '检测中'
  if (item.detection_status === 'failed' || item.detection_result === 'failed') return '检测失败'
  return '未检测'
}

const getDetectionResultCount = (result: string) => {
  if (result === 'undetected') return filteredResources.value.filter(r => r.detection_result === null && r.detection_status !== 'detecting' && r.detection_status !== 'failed').length
  if (result === 'detecting') return filteredResources.value.filter(r => r.detection_status === 'detecting').length
  if (result === 'failed') return filteredResources.value.filter(r => r.detection_result === 'failed' || r.detection_status === 'failed').length
  return filteredResources.value.filter(r => r.detection_result === result).length
}

// 查看检测结果
const viewDetectionResult = async (resource: Resource) => {
  if (!resource.task_id) {
    snackbar.showMessage('该资源没有关联的检测任务', 'warning')
    return
  }
  showDetectionResultDialog.value = true
  detectionResultLoading.value = true
  detectionResultData.value = null
  try {
    const response = await resourceApi.getDetectionResult(resource.task_id!)
    detectionResultData.value = response.data
  } catch (error) {
    console.error('获取检测结果失败:', error)
    snackbar.showMessage('获取检测结果失败', 'error')
  } finally {
    detectionResultLoading.value = false
  }
}

// 预览资源
const previewResource = async (resource: Resource) => {
  showPreviewDialog.value = true
  previewLoading.value = true
  previewUrl.value = null
  previewType.value = 'other'
  previewTextContent.value = ''
  previewFileName.value = resource.file_name || resource.title || ''

  try {
    // 对于主列表中的 FileManagement 资源，统一使用 'file' 类型进行预览
    // 因为后端 /api/preview/file/{id}/ 对应的是 FileManagement ID，
    // 而 /api/preview/image/{id}/ 对应的是具体的 ImageUpload ID。
    const response = await resourceApi.previewResource(resource.id, 'file')

    const blob = response.data as any
    const contentType = blob.type || ''

    // 根据资源类型和 Content-Type 判断预览方式
    if (resource.type === 'image' || contentType.startsWith('image/')) {
      previewType.value = 'image'
      previewUrl.value = URL.createObjectURL(blob)
    } else if (contentType === 'application/pdf' || (resource.file_name && resource.file_name.toLowerCase().endsWith('.pdf'))) {
      previewType.value = 'pdf'
      previewUrl.value = URL.createObjectURL(blob)
    } else if (contentType.startsWith('text/') || (resource.file_name && /\.(txt|md|csv|json|xml)$/i.test(resource.file_name))) {
      previewType.value = 'text'
      previewUrl.value = URL.createObjectURL(blob)
      const text = await blob.text()
      previewTextContent.value = text
    } else {
      previewType.value = 'other'
      previewUrl.value = URL.createObjectURL(blob)
    }
  } catch (error: any) {
    console.error('预览资源失败:', error)
    if (error?.response?.status === 404) {
      snackbar.showMessage('资源文件不存在或已被删除', 'warning')
    } else {
      snackbar.showMessage('预览资源失败', 'error')
    }
    previewUrl.value = null
  } finally {
    previewLoading.value = false
  }
}

// 删除资源
const deleteResource = async () => {
  if (!selectedResource.value) return
  
  try {
    await resourceApi.deleteResource(selectedResource.value.id)
    snackbar.showMessage('删除成功', 'success')
    showDeleteDialog.value = false
    loadResources()
  } catch (error) {
    console.error('删除资源失败:', error)
    snackbar.showMessage('删除失败', 'error')
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadResources()
})
</script>

<style scoped>
/* 无需特殊样式 */
</style>
