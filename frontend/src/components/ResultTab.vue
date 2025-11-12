<template>
  <div class="result-tab">
    <div v-if="result">
      <!-- 统计信息 -->
      <el-row :gutter="20" class="stats-row">
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="用例总数" :value="result.caseCount">
              <template #prefix>
                <el-icon color="#409EFF"><Document /></el-icon>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="模块数量" :value="result.moduleCount">
              <template #prefix>
                <el-icon color="#67C23A"><FolderOpened /></el-icon>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="高优先级" :value="result.highPriority">
              <template #prefix>
                <el-icon color="#F56C6C"><Warning /></el-icon>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <el-statistic title="输出格式" :value="result.format" />
          </el-card>
        </el-col>
      </el-row>
      
      <!-- 下载区域 -->
      <el-card shadow="hover" style="margin-top: 20px">
        <template #header>
          <div class="card-header">
            <span>📥 下载文件</span>
          </div>
        </template>
        
        <el-space wrap>
          <el-button
            type="primary"
            size="large"
            @click="downloadFile(result.caseFile)"
          >
            <el-icon><Download /></el-icon>
            下载用例文件
          </el-button>
          
          <el-button
            v-if="result.planFile"
            type="success"
            size="large"
            @click="downloadFile(result.planFile)"
          >
            <el-icon><Download /></el-icon>
            下载走查计划
          </el-button>
          
          <el-button
            type="info"
            size="large"
            @click="shareLink"
          >
            <el-icon><Share /></el-icon>
            分享链接
          </el-button>
        </el-space>
      </el-card>
      
      <!-- 用例预览 -->
      <el-card shadow="hover" style="margin-top: 20px">
        <template #header>
          <div class="card-header">
            <span>👀 用例预览</span>
            <span class="preview-tip">（显示前10条）</span>
          </div>
        </template>
        
        <el-table
          :data="result.previewData"
          border
          stripe
          style="width: 100%"
        >
          <el-table-column prop="用例编号" label="用例编号" width="120" />
          <el-table-column prop="页面/模块" label="页面/模块" width="150" />
          <el-table-column prop="检查点" label="检查点" width="150" />
          <el-table-column prop="设计原则" label="设计原则" width="180" />
          <el-table-column prop="检查项" label="检查项" show-overflow-tooltip />
          <el-table-column prop="优先级" label="优先级" width="80">
            <template #default="scope">
              <el-tag
                :type="getPriorityType(scope.row.优先级)"
                size="small"
              >
                {{ scope.row.优先级 }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
    
    <!-- 空状态 -->
    <el-empty
      v-else
      description="请先上传文档并生成用例"
      :image-size="200"
    >
      <el-button type="primary" @click="goToUpload">
        去上传文档
      </el-button>
    </el-empty>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'

export default {
  name: 'ResultTab',
  props: {
    result: {
      type: Object,
      default: null
    }
  },
  setup() {
    const downloadFile = (filename) => {
      const url = `http://localhost:5000/api/download/${filename}`
      window.open(url, '_blank')
      ElMessage.success('开始下载文件')
    }
    
    const shareLink = () => {
      ElMessage.info('分享功能开发中...')
    }
    
    const goToUpload = () => {
      // 触发父组件切换tab
      window.dispatchEvent(new CustomEvent('switch-tab', { detail: 'upload' }))
    }
    
    const getPriorityType = (priority) => {
      const types = {
        '高': 'danger',
        '中': 'warning',
        '低': 'success'
      }
      return types[priority] || 'info'
    }
    
    return {
      downloadFile,
      shareLink,
      goToUpload,
      getPriorityType
    }
  }
}
</script>

<style lang="scss" scoped>
.result-tab {
  .stats-row {
    .stat-card {
      text-align: center;
    }
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    font-size: 16px;
    
    .preview-tip {
      font-size: 12px;
      color: #909399;
      font-weight: normal;
    }
  }
}
</style>
