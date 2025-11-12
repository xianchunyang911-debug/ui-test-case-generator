<template>
  <div id="app">
    <el-container class="app-container">
      <!-- 头部 -->
      <el-header class="app-header">
        <div class="header-content">
          <h1 class="title">
            <el-icon><Document /></el-icon>
            UI走查用例生成助手
          </h1>
          <p class="subtitle">从3小时到3分钟，让UI走查更高效</p>
        </div>
      </el-header>
      
      <!-- 主体 -->
      <el-main class="app-main">
        <el-tabs v-model="activeTab" class="main-tabs">
          <!-- Tab 1: 上传文档 -->
          <el-tab-pane label="上传文档" name="upload">
            <template #label>
              <span class="tab-label">
                <el-icon><Upload /></el-icon>
                上传文档
              </span>
            </template>
            <UploadTab 
              @upload-success="handleUploadSuccess"
              @generate-success="handleGenerateSuccess"
            />
          </el-tab-pane>
          
          <!-- Tab 2: 生成结果 -->
          <el-tab-pane label="生成结果" name="result">
            <template #label>
              <span class="tab-label">
                <el-icon><DataAnalysis /></el-icon>
                生成结果
              </span>
            </template>
            <ResultTab :result="result" />
          </el-tab-pane>
          
          <!-- Tab 3: 生成历史 -->
          <el-tab-pane label="生成历史" name="history">
            <template #label>
              <span class="tab-label">
                <el-icon><Clock /></el-icon>
                生成历史
              </span>
            </template>
            <HistoryTab />
          </el-tab-pane>
          
          <!-- Tab 4: 使用说明 -->
          <el-tab-pane label="使用说明" name="help">
            <template #label>
              <span class="tab-label">
                <el-icon><QuestionFilled /></el-icon>
                使用说明
              </span>
            </template>
            <HelpTab />
          </el-tab-pane>
        </el-tabs>
      </el-main>
      
      <!-- 页脚 -->
      <el-footer class="app-footer">
        <p>© 2024 UI走查用例生成助手 v1.0 | Made with ❤️</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { ref } from 'vue'
import UploadTab from './components/UploadTab.vue'
import ResultTab from './components/ResultTab.vue'
import HistoryTab from './components/HistoryTab.vue'
import HelpTab from './components/HelpTab.vue'

export default {
  name: 'App',
  components: {
    UploadTab,
    ResultTab,
    HistoryTab,
    HelpTab
  },
  setup() {
    const activeTab = ref('upload')
    const result = ref(null)
    
    const handleUploadSuccess = (data) => {
      console.log('文件上传成功:', data)
    }
    
    const handleGenerateSuccess = (data) => {
      result.value = data
      activeTab.value = 'result'
    }
    
    return {
      activeTab,
      result,
      handleUploadSuccess,
      handleGenerateSuccess
    }
  }
}
</script>

<style lang="scss">
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.app-container {
  height: 100%;
}

.app-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  
  .header-content {
    text-align: center;
    
    .title {
      font-size: 28px;
      color: #409EFF;
      margin: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      
      .el-icon {
        font-size: 32px;
      }
    }
    
    .subtitle {
      font-size: 14px;
      color: #909399;
      margin-top: 5px;
    }
  }
}

.app-main {
  padding: 20px;
  overflow: auto;
  
  .main-tabs {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    min-height: calc(100vh - 200px);
    
    .tab-label {
      display: flex;
      align-items: center;
      gap: 5px;
    }
  }
}

.app-footer {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  text-align: center;
  line-height: 60px;
  color: #909399;
  font-size: 14px;
}
</style>
