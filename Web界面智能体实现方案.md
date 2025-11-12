# Web界面智能体实现方案

## 1. 方案概述

### 1.1 目标
创建一个Web应用，让用户通过浏览器上传需求文档，自动生成UI走查用例。

### 1.2 技术栈选择

#### 方案A: Flask + Vue.js（推荐）
- **后端**: Flask (Python)
- **前端**: Vue.js 3 + Element Plus
- **AI**: OpenAI API / 本地LLM
- **优势**: 简单快速，适合快速原型

#### 方案B: FastAPI + React
- **后端**: FastAPI (Python)
- **前端**: React + Ant Design
- **AI**: OpenAI API / 本地LLM
- **优势**: 性能更好，适合生产环境

#### 方案C: Streamlit（最简单）
- **框架**: Streamlit (纯Python)
- **AI**: OpenAI API / 本地LLM
- **优势**: 无需前端开发，快速搭建

## 2. 方案C实现（Streamlit - 最快实现）

### 2.1 安装依赖
```bash
pip install streamlit openai openpyxl pandas
```

### 2.2 创建主程序

创建 `web_ui_test_gen.py`:
```python
import streamlit as st
import openai
import os
from pathlib import Path
import csv_to_excel_multi_sheet as excel_gen

# 配置页面
st.set_page_config(
    page_title="UI走查用例生成助手",
    page_icon="🎨",
    layout="wide"
)

# 标题
st.title("🎨 UI走查用例生成助手")
st.markdown("自动生成UI走查用例和走查计划")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")
    
    # OpenAI API配置
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        openai.api_key = api_key
    
    # 输出格式选择
    output_format = st.radio(
        "输出格式",
        ["自动选择", "CSV格式", "Excel多Sheet格式"],
        index=0
    )
    
    # 高级选项
    st.subheader("高级选项")
    generate_plan = st.checkbox("生成走查计划", value=True)
    generate_guide = st.checkbox("生成使用说明", value=True)
    apply_colors = st.checkbox("应用优先级颜色", value=True)

# 主界面
tab1, tab2, tab3 = st.tabs(["📤 上传文档", "📊 生成结果", "📚 使用说明"])

with tab1:
    st.header("1. 上传需求文档")
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "选择需求文档（Markdown格式）",
        type=['md'],
        help="支持.md格式的需求文档"
    )
    
    if uploaded_file:
        # 显示文件信息
        st.success(f"✅ 已上传: {uploaded_file.name}")
        
        # 显示文档内容预览
        content = uploaded_file.read().decode('utf-8')
        with st.expander("📄 查看文档内容"):
            st.text_area("文档内容", content, height=300)
        
        # 生成按钮
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 生成UI走查用例", type="primary", use_container_width=True):
                with st.spinner("正在生成用例，请稍候..."):
                    try:
                        # 调用AI生成用例
                        result = generate_test_cases(
                            content, 
                            output_format,
                            generate_plan,
                            generate_guide
                        )
                        
                        # 保存结果到session state
                        st.session_state['result'] = result
                        st.session_state['generated'] = True
                        
                        st.success("✅ 生成完成！请切换到"生成结果"标签查看")
                        
                    except Exception as e:
                        st.error(f"❌ 生成失败: {str(e)}")

with tab2:
    st.header("2. 生成结果")
    
    if 'generated' in st.session_state and st.session_state['generated']:
        result = st.session_state['result']
        
        # 显示统计信息
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("用例总数", result['case_count'])
        with col2:
            st.metric("模块数量", result['module_count'])
        with col3:
            st.metric("高优先级", result['high_priority'])
        with col4:
            st.metric("输出格式", result['format'])
        
        st.divider()
        
        # 下载文件
        st.subheader("📥 下载文件")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 下载用例文件
            if result['format'] == 'Excel':
                with open(result['case_file'], 'rb') as f:
                    st.download_button(
                        label="📊 下载Excel用例文件",
                        data=f,
                        file_name=os.path.basename(result['case_file']),
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                with open(result['case_file'], 'r', encoding='utf-8') as f:
                    st.download_button(
                        label="📄 下载CSV用例文件",
                        data=f,
                        file_name=os.path.basename(result['case_file']),
                        mime="text/csv"
                    )
        
        with col2:
            # 下载走查计划
            if generate_plan and 'plan_file' in result:
                with open(result['plan_file'], 'r', encoding='utf-8') as f:
                    st.download_button(
                        label="📋 下载走查计划",
                        data=f,
                        file_name=os.path.basename(result['plan_file']),
                        mime="text/markdown"
                    )
        
        st.divider()
        
        # 预览用例
        st.subheader("👀 用例预览")
        
        # 显示用例表格
        if result['format'] == 'Excel':
            import pandas as pd
            df = pd.read_excel(result['case_file'], sheet_name=0)
            st.dataframe(df.head(10), use_container_width=True)
            st.info(f"显示前10条，共{len(df)}条用例")
        else:
            import pandas as pd
            df = pd.read_csv(result['case_file'])
            st.dataframe(df.head(10), use_container_width=True)
            st.info(f"显示前10条，共{len(df)}条用例")
        
    else:
        st.info("👈 请先在"上传文档"标签页上传需求文档并生成用例")

with tab3:
    st.header("3. 使用说明")
    
    st.markdown("""
    ### 📖 快速开始
    
    1. **配置API Key**
       - 在左侧边栏输入OpenAI API Key
       - 或使用本地LLM（需要额外配置）
    
    2. **上传需求文档**
       - 点击"上传文档"标签
       - 选择Markdown格式的需求文档
       - 预览文档内容
    
    3. **选择输出格式**
       - 自动选择：根据用例数量自动判断
       - CSV格式：适合简单项目
       - Excel多Sheet格式：适合复杂项目（推荐）
    
    4. **生成用例**
       - 点击"生成UI走查用例"按钮
       - 等待生成完成（约2-5分钟）
       - 切换到"生成结果"标签查看
    
    5. **下载文件**
       - 下载用例文件（CSV或Excel）
       - 下载走查计划（可选）
       - 下载使用说明（可选）
    
    ### 🎯 输出格式说明
    
    #### CSV格式
    - 单文件，所有用例在一起
    - 适合用例数 < 50，模块数 < 3
    - 文件小，易于版本控制
    
    #### Excel多Sheet格式（推荐）
    - 多Sheet，按模块分组
    - 适合用例数 > 50，模块数 > 3
    - 支持下拉选择、自动统计
    - 用例汇总自动计算完成率
    
    ### ⚙️ 高级选项
    
    - **生成走查计划**: 自动生成UI走查计划文档
    - **生成使用说明**: 自动生成快速开始指南
    - **应用优先级颜色**: Excel格式中应用颜色标识
    
    ### 💡 最佳实践
    
    1. **需求文档规范**
       - 使用清晰的标题层级
       - 每个功能模块独立章节
       - 包含字段说明表格
    
    2. **命名规范**
       - 需求文档: `{功能名称}需求文档.md`
       - 输出文件: `{功能名称}-UI走查用例-1.xlsx`
    
    3. **版本管理**
       - 需求文档使用Git管理
       - 生成的用例文件也纳入版本控制
    """)

# 辅助函数
def generate_test_cases(content, format_type, gen_plan, gen_guide):
    """生成UI走查用例"""
    
    # 1. 分析需求文档
    modules = analyze_requirement(content)
    
    # 2. 生成用例
    cases = generate_cases_with_ai(content, modules)
    
    # 3. 确定输出格式
    if format_type == "自动选择":
        if len(cases) > 50 or len(modules) > 3:
            format_type = "Excel多Sheet格式"
        else:
            format_type = "CSV格式"
    
    # 4. 生成文件
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    if format_type == "Excel多Sheet格式":
        case_file = output_dir / "UI走查用例.xlsx"
        # 调用Excel生成脚本
        excel_gen.create_excel_with_multiple_sheets(
            cases, 
            str(case_file)
        )
    else:
        case_file = output_dir / "UI走查用例.csv"
        # 生成CSV文件
        save_to_csv(cases, str(case_file))
    
    # 5. 生成走查计划
    plan_file = None
    if gen_plan:
        plan_file = output_dir / "UI走查计划.md"
        generate_plan_doc(modules, str(plan_file))
    
    # 6. 返回结果
    return {
        'case_count': len(cases),
        'module_count': len(modules),
        'high_priority': sum(1 for c in cases if c.get('优先级') == '高'),
        'format': 'Excel' if 'Excel' in format_type else 'CSV',
        'case_file': str(case_file),
        'plan_file': str(plan_file) if plan_file else None
    }

def analyze_requirement(content):
    """分析需求文档，识别功能模块"""
    # 使用AI分析需求文档
    prompt = f"""
    分析以下需求文档，识别功能模块：
    
    {content}
    
    请返回JSON格式的模块列表：
    {{
        "modules": [
            {{"name": "模块名称", "description": "模块描述"}},
            ...
        ]
    }}
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # 解析返回结果
    import json
    result = json.loads(response.choices[0].message.content)
    return result['modules']

def generate_cases_with_ai(content, modules):
    """使用AI生成UI走查用例"""
    cases = []
    
    for module in modules:
        prompt = f"""
        根据以下需求文档和模块信息，生成UI走查用例：
        
        需求文档：
        {content}
        
        模块：{module['name']}
        
        请应用8大UI走查原则生成用例，返回JSON格式：
        {{
            "cases": [
                {{
                    "用例编号": "UI-TC001",
                    "页面/模块": "模块名称",
                    "检查点": "检查点",
                    "设计原则": "设计原则",
                    "检查项": "检查项",
                    "优先级": "高/中/低",
                    "预期结果/设计标准": "预期结果"
                }},
                ...
            ]
        }}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        cases.extend(result['cases'])
    
    return cases

def save_to_csv(cases, filepath):
    """保存为CSV文件"""
    import csv
    
    headers = ['用例编号', '页面/模块', '检查点', '设计原则', '检查项', 
               '优先级', '预期结果/设计标准', '是否通过', '截图/备注']
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for case in cases:
            case['是否通过'] = '待测试'
            case['截图/备注'] = ''
            writer.writerow(case)

def generate_plan_doc(modules, filepath):
    """生成走查计划文档"""
    content = f"""# UI走查计划

## 1. 走查目标
确保UI实现与设计稿一致

## 2. 走查模块
共{len(modules)}个模块：
"""
    
    for i, module in enumerate(modules, 1):
        content += f"\n{i}. {module['name']}: {module['description']}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 运行应用
if __name__ == "__main__":
    st.write("")
```

### 2.3 运行Web应用

```bash
streamlit run web_ui_test_gen.py
```

浏览器会自动打开 `http://localhost:8501`

## 3. 方案A实现（Flask + Vue.js）

### 3.1 后端实现

创建 `backend/app.py`:

```python
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)  # 允许跨域

# 配置
UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('output')
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """上传需求文档"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    # 保存文件
    filepath = UPLOAD_FOLDER / file.filename
    file.save(filepath)
    
    # 读取内容
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return jsonify({
        'success': True,
        'filename': file.filename,
        'content': content[:500]  # 返回前500字符预览
    })

@app.route('/api/generate', methods=['POST'])
def generate_cases():
    """生成UI走查用例"""
    data = request.json
    filename = data.get('filename')
    format_type = data.get('format', 'auto')
    
    # 读取文件
    filepath = UPLOAD_FOLDER / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成用例
    try:
        result = generate_test_cases(content, format_type)
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    """下载生成的文件"""
    filepath = OUTPUT_FOLDER / filename
    return send_file(filepath, as_attachment=True)

def generate_test_cases(content, format_type):
    """生成用例的核心逻辑"""
    # 与Streamlit版本相同的逻辑
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 3.2 前端实现

创建 `frontend/src/App.vue`:
```vue
<template>
  <div id="app">
    <el-container>
      <!-- 头部 -->
      <el-header>
        <h1>🎨 UI走查用例生成助手</h1>
      </el-header>
      
      <!-- 主体 -->
      <el-main>
        <el-tabs v-model="activeTab">
          <!-- 上传文档 -->
          <el-tab-pane label="上传文档" name="upload">
            <el-card>
              <el-upload
                class="upload-demo"
                drag
                action="/api/upload"
                :on-success="handleUploadSuccess"
                :before-upload="beforeUpload"
              >
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">
                  将文件拖到此处，或<em>点击上传</em>
                </div>
                <div class="el-upload__tip" slot="tip">
                  只能上传 .md 文件
                </div>
              </el-upload>
              
              <!-- 文件预览 -->
              <div v-if="uploadedFile" class="file-preview">
                <h3>文件预览</h3>
                <el-input
                  type="textarea"
                  :rows="10"
                  v-model="fileContent"
                  readonly
                ></el-input>
              </div>
              
              <!-- 配置选项 -->
              <div v-if="uploadedFile" class="config-section">
                <h3>配置选项</h3>
                <el-form :model="config" label-width="120px">
                  <el-form-item label="输出格式">
                    <el-radio-group v-model="config.format">
                      <el-radio label="auto">自动选择</el-radio>
                      <el-radio label="csv">CSV格式</el-radio>
                      <el-radio label="excel">Excel多Sheet</el-radio>
                    </el-radio-group>
                  </el-form-item>
                  
                  <el-form-item label="高级选项">
                    <el-checkbox v-model="config.generatePlan">
                      生成走查计划
                    </el-checkbox>
                    <el-checkbox v-model="config.generateGuide">
                      生成使用说明
                    </el-checkbox>
                  </el-form-item>
                  
                  <el-form-item>
                    <el-button
                      type="primary"
                      @click="generateCases"
                      :loading="generating"
                    >
                      生成UI走查用例
                    </el-button>
                  </el-form-item>
                </el-form>
              </div>
            </el-card>
          </el-tab-pane>
          
          <!-- 生成结果 -->
          <el-tab-pane label="生成结果" name="result">
            <el-card v-if="result">
              <!-- 统计信息 -->
              <el-row :gutter="20">
                <el-col :span="6">
                  <el-statistic title="用例总数" :value="result.caseCount" />
                </el-col>
                <el-col :span="6">
                  <el-statistic title="模块数量" :value="result.moduleCount" />
                </el-col>
                <el-col :span="6">
                  <el-statistic title="高优先级" :value="result.highPriority" />
                </el-col>
                <el-col :span="6">
                  <el-statistic title="输出格式" :value="result.format" />
                </el-col>
              </el-row>
              
              <el-divider></el-divider>
              
              <!-- 下载按钮 -->
              <div class="download-section">
                <h3>下载文件</h3>
                <el-button
                  type="primary"
                  icon="el-icon-download"
                  @click="downloadFile(result.caseFile)"
                >
                  下载用例文件
                </el-button>
                <el-button
                  v-if="result.planFile"
                  type="success"
                  icon="el-icon-download"
                  @click="downloadFile(result.planFile)"
                >
                  下载走查计划
                </el-button>
              </div>
              
              <el-divider></el-divider>
              
              <!-- 用例预览 -->
              <div class="preview-section">
                <h3>用例预览</h3>
                <el-table :data="previewData" border>
                  <el-table-column prop="用例编号" label="用例编号" width="120" />
                  <el-table-column prop="页面/模块" label="页面/模块" width="150" />
                  <el-table-column prop="检查点" label="检查点" width="150" />
                  <el-table-column prop="检查项" label="检查项" />
                  <el-table-column prop="优先级" label="优先级" width="80" />
                </el-table>
              </div>
            </el-card>
            
            <el-empty v-else description="请先上传文档并生成用例" />
          </el-tab-pane>
          
          <!-- 使用说明 -->
          <el-tab-pane label="使用说明" name="help">
            <el-card>
              <div class="help-content">
                <h2>📖 使用说明</h2>
                <h3>1. 上传需求文档</h3>
                <p>支持Markdown格式的需求文档</p>
                
                <h3>2. 选择输出格式</h3>
                <ul>
                  <li><strong>自动选择</strong>: 根据用例数量自动判断</li>
                  <li><strong>CSV格式</strong>: 适合简单项目</li>
                  <li><strong>Excel多Sheet</strong>: 适合复杂项目（推荐）</li>
                </ul>
                
                <h3>3. 生成用例</h3>
                <p>点击"生成UI走查用例"按钮，等待生成完成</p>
                
                <h3>4. 下载文件</h3>
                <p>在"生成结果"标签页下载生成的文件</p>
              </div>
            </el-card>
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      activeTab: 'upload',
      uploadedFile: null,
      fileContent: '',
      config: {
        format: 'auto',
        generatePlan: true,
        generateGuide: true
      },
      generating: false,
      result: null,
      previewData: []
    }
  },
  methods: {
    beforeUpload(file) {
      const isMd = file.name.endsWith('.md')
      if (!isMd) {
        this.$message.error('只能上传 .md 文件!')
      }
      return isMd
    },
    
    handleUploadSuccess(response) {
      this.uploadedFile = response.filename
      this.fileContent = response.content
      this.$message.success('文件上传成功!')
    },
    
    async generateCases() {
      this.generating = true
      try {
        const response = await axios.post('/api/generate', {
          filename: this.uploadedFile,
          format: this.config.format
        })
        
        this.result = response.data.result
        this.activeTab = 'result'
        this.$message.success('生成成功!')
      } catch (error) {
        this.$message.error('生成失败: ' + error.message)
      } finally {
        this.generating = false
      }
    },
    
    downloadFile(filename) {
      window.open(`/api/download/${filename}`)
    }
  }
}
</script>

<style>
#app {
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

.el-header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  line-height: 60px;
}

.file-preview,
.config-section,
.download-section,
.preview-section {
  margin-top: 20px;
}

.help-content {
  line-height: 1.8;
}

.help-content h2 {
  color: #409EFF;
}

.help-content h3 {
  margin-top: 20px;
  color: #606266;
}
</style>
```

### 3.3 启动应用

```bash
# 后端
cd backend
python app.py

# 前端
cd frontend
npm install
npm run serve
```

访问 `http://localhost:8080`

## 4. 部署方案

### 4.1 本地部署（Docker）

创建 `Dockerfile`:
```dockerfile
FROM python:3.9

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制代码
COPY . .

# 暴露端口
EXPOSE 8501

# 启动应用
CMD ["streamlit", "run", "web_ui_test_gen.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

创建 `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./output:/app/output
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

启动:
```bash
docker-compose up
```

### 4.2 云端部署

#### Streamlit Cloud（最简单）
1. 将代码推送到GitHub
2. 访问 https://streamlit.io/cloud
3. 连接GitHub仓库
4. 点击Deploy
5. 配置环境变量（API Key）

#### Heroku
```bash
# 创建Procfile
echo "web: streamlit run web_ui_test_gen.py --server.port=$PORT" > Procfile

# 部署
heroku create ui-test-gen
git push heroku main
```

#### AWS/阿里云
使用EC2/ECS部署Docker容器

## 5. 功能增强

### 5.1 添加用户认证
```python
import streamlit_authenticator as stauth

# 配置认证
authenticator = stauth.Authenticate(
    names=['用户1', '用户2'],
    usernames=['user1', 'user2'],
    passwords=['pass1', 'pass2'],
    cookie_name='ui_test_gen',
    key='secret_key'
)

name, authentication_status, username = authenticator.login('登录', 'main')

if authentication_status:
    st.write(f'欢迎 {name}')
    # 主应用逻辑
elif authentication_status == False:
    st.error('用户名或密码错误')
```

### 5.2 添加历史记录
```python
import sqlite3

def save_history(user, filename, case_count):
    """保存生成历史"""
    conn = sqlite3.connect('history.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO history (user, filename, case_count, created_at)
        VALUES (?, ?, ?, datetime('now'))
    ''', (user, filename, case_count))
    conn.commit()
    conn.close()

def get_history(user):
    """获取历史记录"""
    conn = sqlite3.connect('history.db')
    df = pd.read_sql_query(
        'SELECT * FROM history WHERE user = ? ORDER BY created_at DESC',
        conn,
        params=(user,)
    )
    conn.close()
    return df
```

### 5.3 添加进度显示
```python
import time

progress_bar = st.progress(0)
status_text = st.empty()

for i in range(100):
    progress_bar.progress(i + 1)
    status_text.text(f'生成进度: {i+1}%')
    time.sleep(0.01)

status_text.text('生成完成!')
```

### 5.4 添加实时预览
```python
# 使用WebSocket实时推送生成进度
from streamlit_autorefresh import st_autorefresh

# 每5秒自动刷新
count = st_autorefresh(interval=5000, limit=100, key="counter")

st.write(f'已生成 {count} 个用例')
```

## 6. 完整项目结构

```
ui-test-gen-web/
├── backend/
│   ├── app.py                 # Flask后端
│   ├── requirements.txt       # Python依赖
│   └── utils/
│       ├── ai_generator.py    # AI生成逻辑
│       └── excel_generator.py # Excel生成
├── frontend/
│   ├── src/
│   │   ├── App.vue           # 主组件
│   │   ├── components/       # 子组件
│   │   └── main.js
│   ├── package.json
│   └── vue.config.js
├── streamlit/
│   ├── web_ui_test_gen.py    # Streamlit应用
│   └── requirements.txt
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   └── README.md
└── README.md
```

## 7. 快速开始（Streamlit版本）

### 7.1 安装依赖
```bash
pip install streamlit openai openpyxl pandas
```

### 7.2 配置API Key
```bash
export OPENAI_API_KEY="your-api-key"
```

### 7.3 运行应用
```bash
streamlit run web_ui_test_gen.py
```

### 7.4 访问应用
浏览器自动打开 `http://localhost:8501`

## 8. 总结

### 方案对比

| 方案 | 难度 | 开发时间 | 功能 | 适用场景 |
|------|------|----------|------|----------|
| Streamlit | ⭐ | 1天 | 基础 | 快速原型、内部使用 |
| Flask + Vue | ⭐⭐⭐ | 1周 | 完整 | 生产环境、团队使用 |
| FastAPI + React | ⭐⭐⭐⭐ | 2周 | 高级 | 大规模部署 |

### 推荐方案
- **快速验证**: Streamlit（1天完成）
- **团队使用**: Flask + Vue（1周完成）
- **商业产品**: FastAPI + React（2周完成）

### 下一步
1. 选择合适的方案
2. 按照文档实现
3. 部署到服务器
4. 团队开始使用

---

**现在就开始搭建你的Web智能体吧！** 🚀
