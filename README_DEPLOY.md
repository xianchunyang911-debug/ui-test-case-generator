# UI走查用例生成助手

自动生成UI走查用例的智能工具，支持AI生成和模板生成。

## 功能特点

- 📤 支持多种文档格式（Markdown、Word、文本）
- 🤖 AI智能生成（DeepSeek/OpenAI）
- 📋 遵循8大UI走查原则
- 📊 CSV格式输出
- 🎯 简洁易用的Web界面

## 在线使用

访问：[你的Streamlit Cloud地址]

## 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
streamlit run streamlit_app.py
```

## 使用说明

1. **上传需求文档**：支持 .md、.txt、.docx 格式
2. **配置AI**（可选）：输入DeepSeek或OpenAI的API Key
3. **生成用例**：点击"生成UI走查用例"按钮
4. **下载结果**：下载生成的CSV文件

## 技术栈

- Streamlit - Web框架
- OpenAI API - AI生成
- Pandas - 数据处理
- Python-docx - Word文档处理

## 许可证

MIT License
