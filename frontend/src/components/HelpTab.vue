<template>
  <div class="help-tab">
    <el-card shadow="hover">
      <div class="help-content">
        <h2>📖 使用说明</h2>
        
        <el-steps :active="0" finish-status="success" align-center>
          <el-step title="上传文档" description="上传Markdown格式的需求文档" />
          <el-step title="配置选项" description="选择输出格式和高级选项" />
          <el-step title="生成用例" description="点击按钮生成UI走查用例" />
          <el-step title="下载文件" description="下载生成的用例和计划文档" />
        </el-steps>
        
        <el-divider />
        
        <h3>🎯 输出格式说明</h3>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card shadow="never">
              <h4>CSV格式</h4>
              <ul>
                <li>✅ 单文件，所有用例在一起</li>
                <li>✅ 适合用例数 &lt; 50</li>
                <li>✅ 文件小，易于版本控制</li>
                <li>❌ 不支持下拉选择</li>
              </ul>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="never" class="recommended">
              <h4>Excel多Sheet（推荐）</h4>
              <ul>
                <li>✅ 多Sheet，按模块分组</li>
                <li>✅ 适合用例数 &gt; 50</li>
                <li>✅ 支持下拉选择</li>
                <li>✅ 自动统计完成率</li>
              </ul>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="never">
              <h4>自动选择</h4>
              <ul>
                <li>✅ 智能判断</li>
                <li>✅ 根据用例数量</li>
                <li>✅ 根据模块数量</li>
                <li>✅ 最佳实践</li>
              </ul>
            </el-card>
          </el-col>
        </el-row>
        
        <el-divider />
        
        <h3>💡 最佳实践</h3>
        <el-alert
          title="需求文档规范"
          type="info"
          :closable="false"
        >
          <ul>
            <li>使用清晰的标题层级（# ## ###）</li>
            <li>每个功能模块独立章节</li>
            <li>包含字段说明表格</li>
            <li>说明交互流程</li>
          </ul>
        </el-alert>
        
        <el-divider />
        
        <h3>📊 效果对比</h3>
        <el-table :data="comparisonData" border>
          <el-table-column prop="item" label="对比项" width="150" />
          <el-table-column prop="manual" label="手动生成" />
          <el-table-column prop="auto" label="智能生成" />
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'HelpTab',
  setup() {
    const comparisonData = ref([
      { item: '时间成本', manual: '3小时', auto: '3分钟' },
      { item: '用例数量', manual: '50-80个', auto: '100+个' },
      { item: '覆盖率', manual: '70-80%', auto: '90%+' },
      { item: '一致性', manual: '中等', auto: '高' },
      { item: '可维护性', manual: '低', auto: '高' }
    ])
    
    return {
      comparisonData
    }
  }
}
</script>

<style lang="scss" scoped>
.help-tab {
  .help-content {
    h2 {
      color: #409EFF;
      margin-bottom: 20px;
    }
    
    h3 {
      color: #606266;
      margin: 20px 0 15px;
    }
    
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
    
    .recommended {
      border: 2px solid #67C23A;
      background: #f0f9ff;
    }
  }
}
</style>
