<template>
  <div class="history-tab">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>📜 生成历史</span>
          <el-button type="primary" size="small" @click="loadHistory">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </template>
      
      <el-table
        v-loading="loading"
        :data="history"
        border
        stripe
      >
        <el-table-column prop="timestamp" label="生成时间" width="180">
          <template #default="scope">
            {{ formatTime(scope.row.timestamp) }}
          </template>
        </el-table-column>
        <el-table-column prop="filename" label="文件名" />
        <el-table-column prop="case_count" label="用例数" width="100" />
        <el-table-column prop="module_count" label="模块数" width="100" />
        <el-table-column prop="format" label="格式" width="100" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              link
              @click="downloadFile(scope.row.output_file)"
            >
              下载
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

export default {
  name: 'HistoryTab',
  setup() {
    const history = ref([])
    const loading = ref(false)
    
    const loadHistory = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/history')
        if (response.data.success) {
          history.value = response.data.history
        }
      } catch (error) {
        ElMessage.error('加载历史记录失败')
      } finally {
        loading.value = false
      }
    }
    
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleString('zh-CN')
    }
    
    const downloadFile = (filename) => {
      const url = `http://localhost:5000/api/download/${filename}`
      window.open(url, '_blank')
    }
    
    onMounted(() => {
      loadHistory()
    })
    
    return {
      history,
      loading,
      loadHistory,
      formatTime,
      downloadFile
    }
  }
}
</script>

<style lang="scss" scoped>
.history-tab {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    font-size: 16px;
  }
}
</style>
