#!/bin/bash

echo "🚀 准备部署到Streamlit Cloud"
echo ""

# 检查是否已初始化Git
if [ ! -d ".git" ]; then
    echo "📦 初始化Git仓库..."
    git init
fi

# 添加文件
echo "📝 添加文件到Git..."
git add streamlit_app.py ai_generator.py requirements.txt .gitignore .streamlit/ README_DEPLOY.md

# 提交
echo "💾 提交更改..."
git commit -m "Deploy: UI走查用例生成助手"

echo ""
echo "✅ 准备完成！"
echo ""
echo "📋 下一步操作："
echo "1. 在GitHub创建新仓库"
echo "2. 执行以下命令（替换为你的仓库地址）："
echo ""
echo "   git remote add origin https://github.com/你的用户名/仓库名.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. 访问 https://streamlit.io/cloud 部署应用"
echo ""
