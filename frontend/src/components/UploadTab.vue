<template>
  <div class="upload-tab">
    <el-row :gutter="20">
      <!-- 左侧：上传区域 -->
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>📤 上传需求文档</span>
            </div>
          </template>
          
          <!-- 文件上传 -->
          <el-upload
            ref="uploadRef"
            class="upload-demo"
            drag
            :action="uploadUrl"
            :on-success="handleUploadSuccess"
            :on-error="handleUploadError"
            :before-upload="beforeUpload"
            :show-file-list="false"
            accept=".md,.markdown,.txt"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 .md, .markdown, .txt 格式，文件大小不超过 16MB
              </div>
            </template>
          </el-upload>
          
          <!-- 文件信息 -->
          <div v-if="uploadedFile" class="file-info">
            <el-alert
              title="文件上传成功"
              type="success"
              :closable="false"
              show-icon
            >
              <template #default>
                <p><strong>文件名：</strong>{{ uploadedFile.filename }}</p>
                <p><strong>大小：</strong>{{ formatFileSize(uploadedFile.size) }}</p>
              </template>
            </el-alert>
          </div>
          
          <!-- 文档分析 -->
          <div v-if="analysis" class="document-analysis">
            <el-divider content-position="left">📊 文档分析</el-divider>
            <el-row :gutter="20">
              <el-col :span="6">
                <el-statistic title="总行数" :value="analysis.lines" />
              </el-col>
              <el-col :span="6">
                <el-statistic title="总字数" :value="analysis.words" />
              </el-col>
              <el-col :span="6">
                <el-statistic title="识别模块" :value="analysis.modules" />
              </el-col>
              <el-col :span="6">
                <el-statistic title="表格数量" :value="analysis.tables" />
              </el-col>
            </el-row>
            
            <!-- 模块列表 -->
            <div v-if="analysis.module_names && analysis.module_names.length" class="module-list">
              <el-divider content-position="left">📋 识别的模块</el-divider>
              <el-tag
                v-for="(module, index) in analysis.module_names"
                :key="index"
                type="info"
                style="margin: 5px"
              >
                {{ module }}
              </el-tag>
            </div>
          </div>
          
          <!-- 文档预览 -->
          <div v-if="uploadedFile" class="document-preview">
            <el-divider content-position="left">👀 文档预览</el-divider>
            <el-input
              v-model="uploadedFile.preview"
              type="textarea"
              :rows="10"
              readonly
              placeholder="文档内容预览..."
            />
          </div>
        </el-card>
        
        <!-- 配置选项 -->
        <el-card v-if="uploadedFile" shadow="hover" style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <span>⚙️ 配置选项</span>
            </div>
          </template>
          
          <el-form :model="config" label-width="120px">
            <el-form-item label="输出格式">
              <el-radio-group v-model="config.format">
                <el-radio label="auto">
                  <el-icon><MagicStick /></el-icon>
                  自动选择
                </el-radio>
                <el-radio label="csv">
                  <el-icon><Document /></el-icon>
                  CSV格式
                </el-radio>
                <el-radio label="excel">
                  <el-icon><DataAnalysis /></el-icon>
                  Excel多Sheet
                </el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="高级选项">
              <el-checkbox-group v-model="config.options">
                <el-checkbox label="generatePlan">生成走查计划</el-checkbox>
                <el-checkbox label="generateGuide">生成使用说明</el-checkbox>
                <el-checkbox label="applyColors">应用优先级颜色</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="generating"
                @click="generateCases"
                style="width: 100%"
              >
                <el-icon v-if="!generating"><Promotion /></el-icon>
                {{ generating ? '生成中...' : '🚀 生成UI走查用例' }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      
      <!-- 右侧：提示信息 -->
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>💡 使用提示</span>
            </div>
          </template>
          
          <div class="tips-content">
            <h4>📝 需求文档规范</h4>
            <ul>
              <li>使用清晰的标题层级（# ## ###）</li>
              <li>每个功能模块独立章节</li>
              <li>包含字段说明表格</li>
              <li>说明交互流程</li>
            </ul>
            
            <el-divider />
            
            <h4>📊 输出格式说明</h4>
            <el-descriptions :column="1" border size="small">
              <el-descriptions-item label="自动选择">
                根据用例数量自动判断
              </el-descriptions-item>
              <el-descriptions-item label="CSV格式">
                适合简单项目（&lt;50用例）
              </el-descriptions-item>
              <el-descriptions-item label="Excel格式">
                适合复杂项目（推荐）
              </el-descriptions-item>
            </el-descriptions>
            
            <el-divider />
            
            <h4>⚡ 效果对比</h4>
            <el-row :gutter="10">
              <el-col :span="12">
                <el-card shadow="never" class="compare-card">
                  <div class="compare-title">手动生成</div>
                  <div class="compare-value">⏱️ 3小时</div>
                  <div class="compare-desc">50-80个用例</div>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-card shadow="never" class="compare-card success">
                  <div class="compare-title">智能生成</div>
                  <div class="compare-value">⚡ 3分钟</div>
                  <div class="compare-desc">100+个用例</div>
                </el-card>
              </el-col>
            </el-row>
          </div>
        </el-card>
        
        <!-- 示例文档 -->
        <el-card shadow="hover" style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <span>📄 示例文档</span>
            </div>
          </template>
          
          <el-button type="primary" link @click="showExample">
            查看需求文档示例
          </el-button>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 示例对话框 -->
    <el-dialog
      v-model="exampleVisible"
      title="需求文档示例"
      width="70%"
    >
      <el-input
        v-model="exampleDoc"
        type="textarea"
        :rows="20"
        readonly
      />
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import axios from 'axios'
import { ElMessage, ElNotification } from 'element-plus'

export default {
  name: 'UploadTab',
  emits: ['upload-success', 'generate-success'],
  setup(props, { emit }) {
    const uploadUrl = 'http://localhost:5000/api/upload'
    const uploadRef = ref(null)
    const uploadedFile = ref(null)
    const analysis = ref(null)
    const generating = ref(false)
    const exampleVisible = ref(false)
    
    const config = reactive({
      format: 'auto',
      options: ['generatePlan', 'generateGuide', 'applyColors']
    })
    
    const exampleDoc = ref(`# 跨域训练功能需求文档

## 1. 功能概述
支持三地混训，为超大规模模型预训练提供高效稳定支撑。

## 2. 页面结构

### 2.1 跨域训练首页
- 标题简介
- 操作指引
- 任务列表

### 2.2 新建跨域训练任务
- 训练任务名称
- 选择模型
- 地域及资源配置

## 3. 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| 训练任务名称 | 文本 | 支持小写字母、数字和"-" |
| 模型名称 | 下拉 | Qwen1.5-70B、OPT-70B |
| 地域 | 下拉 | 武汉、苏州、呼和浩特 |
`)
    
    const beforeUpload = (file) => {
      const isValidType = ['md', 'markdown', 'txt'].some(ext => 
        file.name.toLowerCase().endsWith(`.${ext}`)
      )
      const isLt16M = file.size / 1024 / 1024 < 16
      
      if (!isValidType) {
        ElMessage.error('只能上传 .md, .markdown, .txt 格式的文件!')
        return false
      }
      if (!isLt16M) {
        ElMessage.error('文件大小不能超过 16MB!')
        return false
      }
      return true
    }
    
    const handleUploadSuccess = (response) => {
      if (response.success) {
        uploadedFile.value = response
        analysis.value = response.analysis
        emit('upload-success', response)
        ElMessage.success('文件上传成功!')
      } else {
        ElMessage.error(response.error || '上传失败')
      }
    }
    
    const handleUploadError = (error) => {
      console.error('上传错误:', error)
      ElMessage.error('文件上传失败，请重试')
    }
    
    const formatFileSize = (bytes) => {
      if (bytes < 1024) return bytes + ' B'
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
      return (bytes / 1024 / 1024).toFixed(2) + ' MB'
    }
    
    const generateCases = async () => {
      if (!uploadedFile.value) {
        ElMessage.warning('请先上传需求文档')
        return
      }
      
      generating.value = true
      
      try {
        const response = await axios.post('/api/generate', {
          filename: uploadedFile.value.filename,
          config: {
            format: config.format,
            filename: uploadedFile.value.filename,
            generatePlan: config.options.includes('generatePlan'),
            generateGuide: config.options.includes('generateGuide'),
            applyColors: config.options.includes('applyColors')
          }
        })
        
        if (response.data.success) {
          emit('generate-success', response.data.result)
          ElNotification({
            title: '生成成功',
            message: `已生成 ${response.data.result.caseCount} 个用例`,
            type: 'success',
            duration: 3000
          })
        } else {
          ElMessage.error(response.data.error || '生成失败')
        }
      } catch (error) {
        console.error('生成错误:', error)
        ElMessage.error('生成失败: ' + (error.response?.data?.error || error.message))
      } finally {
        generating.value = false
      }
    }
    
    const showExample = () => {
      exampleVisible.value = true
    }
    
    return {
      uploadUrl,
      uploadRef,
      uploadedFile,
      analysis,
      generating,
      config,
      exampleVisible,
      exampleDoc,
      beforeUpload,
      handleUploadSuccess,
      handleUploadError,
      formatFileSize,
      generateCases,
      showExample
    }
  }
}
</script>

<style lang="scss" scoped>
.upload-tab {
  .card-header {
    font-weight: bold;
    font-size: 16px;
  }
  
  .upload-demo {
    margin-bottom: 20px;
    
    :deep(.el-upload-dragger) {
      padding: 40px;
    }
    
    .el-icon--upload {
      font-size: 67px;
      color: #409EFF;
      margin-bottom: 16px;
    }
  }
  
  .file-info {
    margin: 20px 0;
  }
  
  .document-analysis {
    margin: 20px 0;
    
    .module-list {
      margin-top: 15px;
    }
  }
  
  .document-preview {
    margin-top: 20px;
  }
  
  .tips-content {
    h4 {
      color: #409EFF;
      margin-bottom: 10px;
    }
    
    ul {
      padding-left: 20px;
      
      li {
        margin: 5px 0;
        color: #606266;
      }
    }
    
    .compare-card {
      text-align: center;
      padding: 10px;
      
      .compare-title {
        font-size: 14px;
        color: #909399;
        margin-bottom: 5px;
      }
      
      .compare-value {
        font-size: 20px;
        font-weight: bold;
        color: #606266;
        margin: 10px 0;
      }
      
      .compare-desc {
        font-size: 12px;
        color: #909399;
      }
      
      &.success {
        background: #f0f9ff;
        
        .compare-value {
          color: #67C23A;
        }
      }
    }
  }
}
</style>
