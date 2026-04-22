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

          <!-- 资源状态 -->
          <v-col cols="12" sm="6" md="2">
            <v-menu v-model="statusMenu" :close-on-content-click="false" open-on-hover>
              <template v-slot:activator="{ props }">
                <v-text-field
                  v-bind="props"
                  :model-value="getStatusName(filters.status)"
                  label="资源状态"
                  variant="outlined"
                  density="comfortable"
                  color="amber"
                  bg-color="surface"
                  readonly
                  hide-details
                >
                  <template v-slot:prepend-inner>
                    <v-icon color="amber" class="mr-2">mdi-clock-outline</v-icon>
                  </template>
                  <template v-if="filters.status" v-slot:append-inner>
                    <v-icon @click.stop="filters.status = null; handleFilterChange()" size="small" color="error">mdi-close-circle</v-icon>
                  </template>
                </v-text-field>
              </template>
              <v-list>
                <v-list-item
                  v-for="item in statusOptions"
                  :key="item.value"
                  @click="filters.status = item.value; statusMenu = false; handleFilterChange()"
                >
                  <v-list-item-title>
                    <v-icon size="small" class="mr-2" :color="getStatusColor(item.value)">mdi-circle-small</v-icon>
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
                  :model-value="filters.detectionResult === 'real' ? '真实' : (filters.detectionResult === 'fake' ? '虚假' : '')"
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
                    <v-icon size="small" class="mr-2" :color="item.value === 'real' ? 'success' : 'error'">
                      {{ item.value === 'real' ? 'mdi-check-circle' : 'mdi-alert-circle' }}
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

                <div>
                  <div class="text-caption text-medium-emphasis">虚假资源</div>
                  <div class="text-body-2 error--text font-weight-bold">{{ getDetectionResultCount('fake') }}</div>
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
                  <div class="text-caption text-medium-emphasis">已发布</div>
                  <div class="text-body-2 success--text font-weight-bold">{{ getStatusCount('published') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">审核中</div>
                  <div class="text-body-2 warning--text font-weight-bold">{{ getStatusCount('reviewing') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">草稿</div>
                  <div class="text-body-2 grey--text font-weight-bold">{{ getStatusCount('draft') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">已提交</div>
                  <div class="text-body-2 info--text font-weight-bold">{{ getStatusCount('submitted') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">已拒绝</div>
                  <div class="text-body-2 error--text font-weight-bold">{{ getStatusCount('rejected') }}</div>
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
                  <div class="text-caption text-medium-emphasis">已发布</div>
                  <div class="text-body-2 success--text font-weight-bold">{{ getStatusCount('published') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">审核中</div>
                  <div class="text-body-2 warning--text font-weight-bold">{{ getStatusCount('reviewing') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">草稿</div>
                  <div class="text-body-2 grey--text font-weight-bold">{{ getStatusCount('draft') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">已提交</div>
                  <div class="text-body-2 info--text font-weight-bold">{{ getStatusCount('submitted') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">已拒绝</div>
                  <div class="text-body-2 error--text font-weight-bold">{{ getStatusCount('rejected') }}</div>
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
                  <div class="text-caption text-medium-emphasis">已发布</div>
                  <div class="text-body-2 success--text font-weight-bold">{{ getStatusCount('published') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">审核中</div>
                  <div class="text-body-2 warning--text font-weight-bold">{{ getStatusCount('reviewing') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">草稿</div>
                  <div class="text-body-2 grey--text font-weight-bold">{{ getStatusCount('draft') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">已提交</div>
                  <div class="text-body-2 info--text font-weight-bold">{{ getStatusCount('submitted') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">已拒绝</div>
                  <div class="text-body-2 error--text font-weight-bold">{{ getStatusCount('rejected') }}</div>
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
                  <div class="text-caption text-medium-emphasis">已发布</div>
                  <div class="text-body-2 success--text font-weight-bold">{{ getStatusCount('published') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">审核中</div>
                  <div class="text-body-2 warning--text font-weight-bold">{{ getStatusCount('reviewing') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">草稿</div>
                  <div class="text-body-2 grey--text font-weight-bold">{{ getStatusCount('draft') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">已提交</div>
                  <div class="text-body-2 info--text font-weight-bold">{{ getStatusCount('submitted') }}</div>
                </div>

                <div class="mb-2">
                  <div class="text-caption text-medium-emphasis">已拒绝</div>
                  <div class="text-body-2 error--text font-weight-bold">{{ getStatusCount('rejected') }}</div>
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

              <template v-slot:item.author="{ item }">
                <span>{{ item.author || item.uploader_name || '-' }}</span>
              </template>

              <template v-slot:item.organization="{ item }">
                <span>{{ item.organization || '-' }}</span>
              </template>

              <template v-slot:item.editor="{ item }">
                <span>{{ item.editor || '-' }}</span>
              </template>

              <template v-slot:item.subject="{ item }">
                <v-chip size="small" color="info">
                  {{ getSubjectName(item.subject) }}
                </v-chip>
              </template>

              <template v-slot:item.status="{ item }">
                <v-chip :color="getStatusColor(item.status)" size="small">
                  {{ getStatusName(item.status) }}
                </v-chip>
              </template>

              <template v-slot:item.detection_result="{ item }">
                <v-chip
                  :color="item.detection_result === 'real' ? 'success' : 'error'"
                  size="small"
                >
                  {{ item.detection_result === 'real' ? '真实' : (item.detection_result === 'fake' ? '虚假' : '-') }}
                </v-chip>
              </template>

              <template v-slot:item.has_review="{ item }">
                <v-chip :color="(item.review_count || 0) > 0 ? 'success' : 'grey'" size="small">
                  {{ (item.review_count || 0) > 0 ? '是' : '否' }}
                </v-chip>
              </template>

              <template v-slot:item.upload_time="{ item }">
                <span>{{ formatTime(item.upload_time) }}</span>
              </template>

              <template v-slot:item.actions="{ item }">
                <v-btn
                  icon
                  variant="text"
                  size="small"
                  color="primary"
                  @click="viewResource(item.id)"
                >
                  <v-icon>mdi-eye</v-icon>
                </v-btn>
                <v-btn
                  icon
                  variant="text"
                  size="small"
                  color="error"
                  @click="openDeleteDialog(item)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
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
          <v-btn color="primary" @click="showDetailDialog = false">
            确定
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
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useSnackbarStore } from '@/stores/snackbar'
import resourceApi, { type Resource } from '@/api/resource'

const snackbar = useSnackbarStore()

// 主页面搜索
const searchQuery = ref('')

// 菜单状态
const statusMenu = ref(false)
const detectionResultMenu = ref(false)
const subjectMenu = ref(false)

// 筛选条件
const filters = ref<{
  subject: string | null
  status: string | null
  detectionResult: string | null
  startTime: Date | null
  endTime: Date | null
}>({
  subject: null,
  status: null,
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
  { title: '其他', value: 'other' }
]

const statusOptions = [
  { title: '全部状态', value: 'all' },
  { title: '草稿', value: 'draft' },
  { title: '已提交', value: 'submitted' },
  { title: '审核中', value: 'reviewing' },
  { title: '已发布', value: 'published' },
  { title: '已拒绝', value: 'rejected' }
]

const detectionResultOptions = [
  { title: '真实', value: 'real' },
  { title: '虚假', value: 'fake' }
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
  { title: '论文 ID', key: 'id', align: 'start' as const, sortable: true },
  { title: '论文标题', key: 'title', align: 'start' as const, sortable: true },
  { title: '作者信息', key: 'author', align: 'start' as const, sortable: true },
  { title: '所属组织', key: 'organization', align: 'start' as const, sortable: true },
  { title: '编辑负责人', key: 'editor', align: 'start' as const, sortable: true },
  { title: '学科', key: 'subject', align: 'center' as const, sortable: true },
  { title: '状态', key: 'status', align: 'center' as const, sortable: true },
  { title: '检测结果', key: 'detection_result', align: 'center' as const, sortable: true },
  { title: '关联Review', key: 'has_review', align: 'center' as const, sortable: true },
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
  
  if (filters.value.status && filters.value.status !== 'all') {
    filtered = filtered.filter(r => r.status === filters.value.status)
  }
  
  if (filters.value.detectionResult) {
    filtered = filtered.filter(r => r.detection_result === filters.value.detectionResult)
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
}

// 获取学科名称
const getSubjectName = (subject: string | null) => {
  if (!subject) return '全部学科'
  const option = subjectOptions.find(opt => opt.value === subject)
  return option ? option.title : subject
}

// 获取状态名称
const getStatusName = (status: string | null) => {
  if (!status) return '全部状态'
  const option = statusOptions.find(opt => opt.value === status)
  return option ? option.title : status
}

// 获取状态颜色
const getStatusColor = (status: string | null) => {
  const colors: { [key: string]: string } = {
    draft: 'grey',
    submitted: 'info',
    reviewing: 'warning',
    published: 'success',
    rejected: 'error'
  }
  return status ? colors[status] || 'grey' : 'grey'
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
    const response = await resourceApi.getResources()
    resources.value = response.data || []
  } catch (error) {
    console.error('加载资源失败:', error)
    snackbar.show('加载资源失败', 'error')
    // 使用模拟数据
    resources.value = [
      {
        id: 1,
        file_name: '深度学习在图像识别中的应用.pdf',
        type: 'paper',
        title: '深度学习在图像识别中的应用',
        author: '张三',
        organization: '北京大学',
        editor: '李四',
        subject: 'computer_science',
        status: 'published',
        detection_result: 'real',
        detection_status: 'completed',
        review_count: 5,
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
        editor: '赵六',
        subject: 'artificial_intelligence',
        status: 'reviewing',
        detection_result: 'real',
        detection_status: 'completed',
        review_count: 3,
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
  console.log('搜索执行')
}

// 筛选条件改变
const handleFilterChange = () => {
  console.log('筛选条件改变')
}

// 清除所有筛选条件
const clearAllFilters = () => {
  searchQuery.value = ''
  filters.value = {
    subject: null,
    status: null,
    detectionResult: null,
    startTime: null,
    endTime: null
  }
  selectedType.value = null
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
const getDetectionResultCount = (result: string) => {
  return filteredResources.value.filter(r => r.detection_result === result).length
}

// 获取特定状态的资源数量
const getStatusCount = (status: string) => {
  return filteredResources.value.filter(r => r.status === status).length
}

// 删除资源
const deleteResource = async () => {
  if (!selectedResource.value) return
  
  try {
    await resourceApi.deleteResource(selectedResource.value.id)
    snackbar.show('删除成功', 'success')
    showDeleteDialog.value = false
    loadResources()
  } catch (error) {
    console.error('删除资源失败:', error)
    snackbar.show('删除失败', 'error')
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
