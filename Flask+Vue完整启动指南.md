# Flask + Vue.js 完整启动指南

## 🎯 项目结构

```
ui-test-gen-web/
├── backend/                    # Flask后端
│   ├── app.py                 # 主应用
│   ├── requirements.txt       # Python依赖
│   ├── uploads/               # 上传文件目录
│   ├── output/                # 输出文件目录
│   └── history.json           # 生成历史
│
├── frontend/                   # Vue.js前端
│   ├── src/
│   │   ├── App.vue           # 主组件
│   │   ├── main.js           # 入口文件
│   │   └── components/       # 子组件
│   │       ├── UploadTab.vue
│   │       ├── ResultTab.vue
│   │       ├── HistoryTab.vue
│   │       └── HelpTab.vue
│   ├── package.json          # Node依赖
│   └── public/
│       └── index.html
│
└── csv_to_excel_multi_sheet.py  # Excel生成脚本
```

## 🚀 快速开始（10分钟）

### 步骤1: 安装后端依赖（2分钟）

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 复制Excel生成脚本
cp ../csv_to_excel_multi_sheet.py .
```

### 步骤2: 启动后端服务（1分钟）

```bash
# 在backend目录下
python app.py
```

看到以下输出表示成功：
```
🚀 UI走查用例生成助手 - 后端服务
📍 访问地址: http://localhost:5000
📖 API文档: http://localhost:5000/api/health
 * Running on http://0.0.0.0:5000
```

### 步骤3: 安装前端依赖（5分钟）

打开新终端：

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
# 或使用yarn
yarn install
```

### 步骤4: 启动前端服务（1分钟）

```bash
# 在frontend目录下
npm run serve
# 或
yarn serve
```

看到以下输出表示成功：
```
  App running at:
  - Local:   http://localhost:8080/
  - Network: http://192.168.x.x:8080/
```

### 步骤5: 访问应用（1分钟）

浏览器打开：`http://localhost:8080`

## 📦 详细安装步骤

### 后端安装

#### 1. 安装Python依赖

```bash
cd backend

# 方式1: 使用pip
pip install Flask==3.0.0
pip install flask-cors==4.0.0
pip install pandas==2.1.0
pip install openpyxl==3.1.2
pip install python-dotenv==1.0.0

# 方式2: 使用requirements.txt
pip install -r requirements.txt
```

#### 2. 创建必要目录

```bash
mkdir -p uploads output
```

#### 3. 配置环境变量（可选）

创建 `.env` 文件：
```bash
# Flask配置
FLASK_ENV=development
FLASK_DEBUG=True

# 文件上传配置
MAX_CONTENT_LENGTH=16777216  # 16MB

# OpenAI配置（可选）
# OPENAI_API_KEY=your-api-key
```

### 前端安装

#### 1. 安装Node.js

确保已安装Node.js 16+：
```bash
node --version  # 应该显示 v16.x.x 或更高
npm --version
```

如未安装，访问：https://nodejs.org/

#### 2. 安装Vue CLI（可选）

```bash
npm install -g @vue/cli
```

#### 3. 安装项目依赖

```bash
cd frontend
npm install
```

如果安装慢，可以使用国内镜像：
```bash
npm install --registry=https://registry.npmmirror.com
```

#### 4. 创建必要文件

创建 `frontend/public/index.html`:
```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>UI走查用例生成助手</title>
  </head>
  <body>
    <div id="app"></div>
  </body>
</html>
```

创建 `frontend/vue.config.js`:
```javascript
module.exports = {
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
}
```

## 🔧 配置说明

### 后端配置

#### CORS配置
在 `backend/app.py` 中：
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许所有跨域请求

# 或者限制特定域名
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8080"]
    }
})
```

#### 文件上传配置
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['UPLOAD_FOLDER'] = 'uploads'
```

### 前端配置

#### API地址配置
在 `frontend/src/main.js` 中：
```javascript
// 开发环境
axios.defaults.baseURL = 'http://localhost:5000'

// 生产环境
// axios.defaults.baseURL = 'https://your-api-domain.com'
```

#### Element Plus配置
```javascript
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

app.use(ElementPlus, {
  locale: zhCn,
})
```

## 🐛 故障排查

### 问题1: 后端端口被占用

```bash
# 查看端口占用
lsof -i :5000

# 杀死进程
kill -9 <PID>

# 或使用其他端口
python app.py --port 5001
```

### 问题2: 前端端口被占用

```bash
# 修改 vue.config.js
module.exports = {
  devServer: {
    port: 8081  # 改为其他端口
  }
}
```

### 问题3: CORS错误

确保后端已安装并启用flask-cors：
```bash
pip install flask-cors
```

在app.py中：
```python
from flask_cors import CORS
CORS(app)
```

### 问题4: 文件上传失败

检查：
1. uploads目录是否存在
2. 文件大小是否超过限制
3. 文件格式是否正确

### 问题5: 依赖安装失败

```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# npm使用国内镜像
npm install --registry=https://registry.npmmirror.com
```

## 📊 API文档

### 1. 健康检查
```
GET /api/health
```

响应：
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T12:00:00"
}
```

### 2. 上传文件
```
POST /api/upload
Content-Type: multipart/form-data
```

参数：
- file: 文件对象

响应：
```json
{
  "success": true,
  "filename": "需求文档.md",
  "size": 12345,
  "preview": "文档内容预览...",
  "analysis": {
    "lines": 150,
    "words": 3000,
    "modules": 11
  }
}
```

### 3. 生成用例
```
POST /api/generate
Content-Type: application/json
```

请求体：
```json
{
  "filename": "需求文档.md",
  "config": {
    "format": "auto",
    "generatePlan": true,
    "generateGuide": true
  }
}
```

响应：
```json
{
  "success": true,
  "result": {
    "caseCount": 113,
    "moduleCount": 11,
    "highPriority": 85,
    "format": "Excel",
    "caseFile": "需求文档-UI走查用例-20240101_120000.xlsx",
    "planFile": "需求文档-UI走查计划-20240101_120000.md"
  }
}
```

### 4. 下载文件
```
GET /api/download/<filename>
```

### 5. 获取历史
```
GET /api/history
```

响应：
```json
{
  "success": true,
  "history": [
    {
      "timestamp": "2024-01-01T12:00:00",
      "filename": "需求文档",
      "case_count": 113,
      "module_count": 11,
      "format": "excel"
    }
  ]
}
```

## 🚢 部署方案

### 方案1: Docker部署

创建 `Dockerfile.backend`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY csv_to_excel_multi_sheet.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

创建 `Dockerfile.frontend`:
```dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

创建 `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend/uploads:/app/uploads
      - ./backend/output:/app/output
    environment:
      - FLASK_ENV=production
  
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

启动：
```bash
docker-compose up -d
```

### 方案2: 传统部署

#### 后端部署（使用Gunicorn）

```bash
# 安装Gunicorn
pip install gunicorn

# 启动
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 前端部署

```bash
# 构建
cd frontend
npm run build

# 部署到Nginx
cp -r dist/* /var/www/html/
```

Nginx配置：
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 性能优化

### 后端优化

1. **使用缓存**
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/data')
@cache.cached(timeout=300)
def get_data():
    return jsonify(data)
```

2. **异步处理**
```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

@app.route('/api/generate', methods=['POST'])
def generate_cases():
    future = executor.submit(generate_test_cases, content, config)
    return jsonify({'task_id': future})
```

### 前端优化

1. **路由懒加载**
```javascript
const UploadTab = () => import('./components/UploadTab.vue')
```

2. **组件缓存**
```vue
<keep-alive>
  <component :is="currentTab"></component>
</keep-alive>
```

## 🎉 完成检查清单

- [ ] Python 3.9+ 已安装
- [ ] Node.js 16+ 已安装
- [ ] 后端依赖已安装
- [ ] 前端依赖已安装
- [ ] 后端服务已启动（http://localhost:5000）
- [ ] 前端服务已启动（http://localhost:8080）
- [ ] 可以访问Web界面
- [ ] 可以上传文件
- [ ] 可以生成用例
- [ ] 可以下载文件

## 📚 相关文档

- Flask文档: https://flask.palletsprojects.com/
- Vue.js文档: https://vuejs.org/
- Element Plus文档: https://element-plus.org/
- Axios文档: https://axios-http.com/

---

**现在就开始使用Flask + Vue.js搭建你的Web智能体吧！** 🚀
