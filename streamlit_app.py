#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI走查用例生成助手 - 简化版
"""

import streamlit as st
import os
from pathlib import Path
import pandas as pd
from ai_generator import AIGenerator

# 配置页面
st.set_page_config(
    page_title="UI走查用例生成助手",
    page_icon="🎨",
    layout="wide"
)

# 标题
st.title("🎨 UI走查用例生成助手")
st.caption("自动生成UI走查用例 - 简化版")

# 侧边栏 - AI配置
with st.sidebar:
    st.header("⚙️ AI配置")
    
    use_ai = st.checkbox("使用AI生成", value=False)
    
    if use_ai:
        ai_provider = st.selectbox(
            "选择AI服务",
            ["deepseek", "openai"],
            index=0
        )
        
        api_key = st.text_input(
            f"{ai_provider.upper()} API Key",
            type="password",
            help=f"输入你的{ai_provider} API密钥"
        )
        
        if api_key:
            st.session_state['ai_api_key'] = api_key
            st.session_state['ai_provider'] = ai_provider
            st.success("✅ API Key已配置")

# 主界面
tab1, tab2 = st.tabs(["📤 上传文档", "📊 生成结果"])

with tab1:
    st.header("上传需求文档")
    
    uploaded_file = st.file_uploader(
        "选择需求文档",
        type=['md', 'txt', 'docx'],
        help="支持格式：Markdown (.md)、文本文件 (.txt)、Word文档 (.docx)"
    )
    
    if uploaded_file:
        # 根据文件类型读取内容
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'docx':
            # 读取Word文档
            from docx import Document
            import io
            doc = Document(io.BytesIO(uploaded_file.read()))
            content = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        elif file_extension in ['md', 'txt']:
            # 读取文本文件
            content = uploaded_file.read().decode('utf-8')
        else:
            st.error(f"不支持的文件格式: {file_extension}")
            st.stop()
        
        st.success(f"✅ 已上传: {uploaded_file.name}")
        st.text_area("文档预览", content[:500] + "...", height=200)
        
        st.divider()
        
        # 生成按钮
        if st.button("🚀 生成UI走查用例", type="primary", use_container_width=True):
            with st.spinner("正在生成..."):
                try:
                    # 检查是否使用AI
                    use_ai_gen = use_ai and 'ai_api_key' in st.session_state
                    
                    if use_ai_gen:
                        # 使用AI生成
                        generator = AIGenerator(
                            provider=st.session_state.get('ai_provider', 'deepseek'),
                            api_key=st.session_state.get('ai_api_key')
                        )
                        
                        # 分析需求
                        st.info("📖 正在分析需求文档...")
                        analysis = generator.analyze_requirement(content)
                        modules = analysis.get('modules', [])
                        
                        # 生成用例
                        st.info(f"✍️ 正在为 {len(modules)} 个模块生成用例...")
                        all_cases = []
                        for module in modules:
                            cases = generator.generate_test_cases(content, module)
                            all_cases.extend(cases)
                    else:
                        # 使用模板生成
                        st.info("📝 使用模板生成用例...")
                        generator = AIGenerator()
                        
                        # 简单识别模块
                        modules = []
                        for line in content.split('\n'):
                            if line.startswith('##'):
                                module_name = line.replace('##', '').strip()
                                if module_name:
                                    modules.append({'name': module_name})
                        
                        all_cases = []
                        for module in modules[:5]:  # 最多5个模块
                            cases = generator._template_cases(module['name'])
                            all_cases.extend(cases)
                    
                    # 添加用例编号
                    for i, case in enumerate(all_cases, 1):
                        case['用例编号'] = f'UI-TC{i:03d}'
                        case['是否通过'] = '待测试'
                        case['截图/备注'] = ''
                    
                    # 保存到CSV
                    import csv
                    from datetime import datetime
                    
                    output_dir = Path('output')
                    output_dir.mkdir(exist_ok=True)
                    
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = uploaded_file.name.replace('.md', '')
                    csv_file = output_dir / f"{filename}-UI走查用例-{timestamp}.csv"
                    
                    headers = ['用例编号', '页面/模块', '检查点', '设计原则', '检查项', 
                              '优先级', '预期结果/设计标准', '是否通过', '截图/备注']
                    
                    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=headers)
                        writer.writeheader()
                        writer.writerows(all_cases)
                    
                    # 保存到session
                    st.session_state['generated_file'] = str(csv_file)
                    st.session_state['all_cases'] = all_cases
                    st.session_state['module_count'] = len(modules)
                    
                    st.success(f"✅ 生成完成！共 {len(all_cases)} 个用例")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ 生成失败: {str(e)}")
                    import traceback
                    with st.expander("查看错误详情"):
                        st.code(traceback.format_exc())

with tab2:
    st.header("生成结果")
    
    if 'generated_file' in st.session_state:
        # 显示统计
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("用例总数", len(st.session_state.get('all_cases', [])))
        with col2:
            st.metric("模块数量", st.session_state.get('module_count', 0))
        with col3:
            st.metric("输出格式", "CSV")
        
        st.divider()
        
        # 下载按钮
        generated_file = st.session_state['generated_file']
        if os.path.exists(generated_file):
            with open(generated_file, 'r', encoding='utf-8') as f:
                csv_data = f.read()
            
            st.download_button(
                label="📥 下载用例文件",
                data=csv_data,
                file_name=os.path.basename(generated_file),
                mime="text/csv",
                use_container_width=True
            )
        
        # 预览
        st.subheader("用例预览")
        if 'all_cases' in st.session_state:
            df = pd.DataFrame(st.session_state['all_cases'])
            display_cols = ['用例编号', '页面/模块', '检查点', '优先级']
            st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
    else:
        st.info("👈 请先在左侧上传文档并生成用例")

# 页脚
st.divider()
st.caption("💡 提示：使用AI生成可以获得更智能、更全面的用例")
