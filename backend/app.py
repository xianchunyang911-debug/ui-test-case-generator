#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI走查用例生成助手 - Flask后端
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from pathlib import Path
from datetime import datetime
import csv_to_excel_multi_sheet as excel_gen

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
UPLOAD_FOLDER = Path('uploads')
OUTPUT_FOLDER = Path('output')
ALLOWED_EXTENSIONS = {'md', 'markdown', 'txt'}

UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """上传需求文档"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': '没有文件'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': '不支持的文件格式'}), 400
        
        # 保存文件
        filename = secure_filename(file.filename)
        filepath = app.config['UPLOAD_FOLDER'] / filename
        file.save(filepath)
        
        # 读取内容
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分析文档
        analysis = analyze_document(content)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'size': os.path.getsize(filepath),
            'preview': content[:500],  # 前500字符预览
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_cases():
    """生成UI走查用例"""
    try:
        data = request.json
        filename = data.get('filename')
        config = data.get('config', {})
        
        if not filename:
            return jsonify({'error': '缺少文件名'}), 400
        
        # 读取文件
        filepath = app.config['UPLOAD_FOLDER'] / filename
        if not filepath.exists():
            return jsonify({'error': '文件不存在'}), 404
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 生成用例
        result = generate_test_cases(content, config)
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """下载生成的文件"""
    try:
        filepath = app.config['OUTPUT_FOLDER'] / filename
        
        if not filepath.exists():
            return jsonify({'error': '文件不存在'}), 404
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """获取生成历史"""
    try:
        history_file = Path('history.json')
        
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = []
        
        return jsonify({
            'success': True,
            'history': history
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def analyze_document(content):
    """分析需求文档"""
    lines = content.split('\n')
    words = content.split()
    
    # 识别模块（基于二级标题）
    modules = []
    for line in lines:
        if line.startswith('##'):
            module_name = line.replace('##', '').strip()
            if module_name and not module_name.isdigit():
                modules.append(module_name)
    
    # 识别表格
    tables = content.count('|')
    
    return {
        'lines': len(lines),
        'words': len(words),
        'modules': len(modules),
        'module_names': modules[:10],  # 最多返回10个
        'tables': tables // 3,  # 粗略估计表格数量
        'has_images': '![' in content
    }

def generate_test_cases(content, config):
    """生成UI走查用例的核心逻辑"""
    
    # 1. 分析需求文档
    analysis = analyze_document(content)
    modules = analysis['module_names']
    
    # 2. 生成用例数据（这里使用模板，实际可以接入AI）
    cases = generate_cases_from_template(content, modules)
    
    # 3. 确定输出格式
    format_type = config.get('format', 'auto')
    if format_type == 'auto':
        if len(cases) > 50 or len(modules) > 3:
            format_type = 'excel'
        else:
            format_type = 'csv'
    
    # 4. 生成文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = config.get('filename', '需求文档').replace('.md', '')
    
    if format_type == 'excel':
        output_file = f"{base_name}-UI走查用例-{timestamp}.xlsx"
        output_path = app.config['OUTPUT_FOLDER'] / output_file
        
        # 按模块分组
        modules_data = {}
        for case in cases:
            module = case.get('页面/模块', '未分类')
            if module not in modules_data:
                modules_data[module] = []
            modules_data[module].append(case)
        
        # 生成Excel
        excel_gen.create_excel_with_multiple_sheets(
            str(output_path.parent / f"temp_{timestamp}.csv"),
            str(output_path)
        )
    else:
        output_file = f"{base_name}-UI走查用例-{timestamp}.csv"
        output_path = app.config['OUTPUT_FOLDER'] / output_file
        save_to_csv(cases, str(output_path))
    
    # 5. 生成走查计划（如果需要）
    plan_file = None
    if config.get('generatePlan', True):
        plan_file = f"{base_name}-UI走查计划-{timestamp}.md"
        plan_path = app.config['OUTPUT_FOLDER'] / plan_file
        generate_plan_doc(modules, cases, str(plan_path))
    
    # 6. 保存历史记录
    save_history({
        'timestamp': datetime.now().isoformat(),
        'filename': base_name,
        'case_count': len(cases),
        'module_count': len(modules),
        'format': format_type,
        'output_file': output_file
    })
    
    # 7. 返回结果
    return {
        'caseCount': len(cases),
        'moduleCount': len(modules),
        'highPriority': sum(1 for c in cases if c.get('优先级') == '高'),
        'format': 'Excel' if format_type == 'excel' else 'CSV',
        'caseFile': output_file,
        'planFile': plan_file,
        'previewData': cases[:10]  # 返回前10条预览
    }

def generate_cases_from_template(content, modules):
    """基于模板生成用例"""
    cases = []
    case_id = 1
    
    # 为每个模块生成基础用例
    for module in modules:
        # 视觉一致性用例
        cases.append({
            '用例编号': f'UI-TC{case_id:03d}',
            '页面/模块': module,
            '检查点': '页面标题',
            '设计原则': '视觉一致性原则',
            '检查项': f'检查{module}页面标题的字体、字号、颜色',
            '优先级': '高',
            '预期结果/设计标准': '标题字号16px，字重500，颜色#262626，与设计规范一致',
            '是否通过': '待测试',
            '截图/备注': ''
        })
        case_id += 1
        
        # 组件状态用例
        cases.append({
            '用例编号': f'UI-TC{case_id:03d}',
            '页面/模块': module,
            '检查点': '按钮状态',
            '设计原则': '组件状态完整性原则',
            '检查项': f'检查{module}中按钮的默认、悬停、点击、禁用状态',
            '优先级': '高',
            '预期结果/设计标准': '按钮各状态样式符合设计规范，有平滑过渡动画',
            '是否通过': '待测试',
            '截图/备注': ''
        })
        case_id += 1
        
        # 交互反馈用例
        cases.append({
            '用例编号': f'UI-TC{case_id:03d}',
            '页面/模块': module,
            '检查点': '操作反馈',
            '设计原则': '交互与反馈原则',
            '检查项': f'检查{module}中操作是否有及时的反馈提示',
            '优先级': '高',
            '预期结果/设计标准': '操作成功/失败时显示Toast提示，加载时显示loading动画',
            '是否通过': '待测试',
            '截图/备注': ''
        })
        case_id += 1
    
    # 添加全局检查用例
    global_cases = [
        {
            '用例编号': f'UI-TC{case_id:03d}',
            '页面/模块': '全局检查',
            '检查点': '颜色规范',
            '设计原则': '视觉一致性原则',
            '检查项': '检查全局主色、成功色、错误色、警告色使用是否统一',
            '优先级': '高',
            '预期结果/设计标准': '主色#1890FF，成功色#52c41a，错误色#ff4d4f，警告色#faad14',
            '是否通过': '待测试',
            '截图/备注': ''
        },
        {
            '用例编号': f'UI-TC{case_id+1:03d}',
            '页面/模块': '全局检查',
            '检查点': '字体规范',
            '设计原则': '视觉一致性原则',
            '检查项': '检查全局字体类型、字号、字重是否统一',
            '优先级': '高',
            '预期结果/设计标准': '标题16px/字重500，正文14px/字重400，辅助文字12px/字重400',
            '是否通过': '待测试',
            '截图/备注': ''
        }
    ]
    
    cases.extend(global_cases)
    
    return cases

def save_to_csv(cases, filepath):
    """保存为CSV文件"""
    import csv
    
    headers = ['用例编号', '页面/模块', '检查点', '设计原则', '检查项', 
               '优先级', '预期结果/设计标准', '是否通过', '截图/备注']
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(cases)

def generate_plan_doc(modules, cases, filepath):
    """生成走查计划文档"""
    content = f"""# UI走查计划

## 1. 走查目标
确保UI实现与设计稿在视觉和体验上保持一致

## 2. 走查统计
- 用例总数: {len(cases)}
- 模块数量: {len(modules)}
- 高优先级: {sum(1 for c in cases if c.get('优先级') == '高')}

## 3. 走查模块
共{len(modules)}个模块：

"""
    
    for i, module in enumerate(modules, 1):
        module_cases = [c for c in cases if c.get('页面/模块') == module]
        content += f"{i}. **{module}** - {len(module_cases)}个用例\n"
    
    content += """
## 4. 走查方法
采用两种方式相结合：
1. 按点走查：逐条检查每个UI元素
2. 按流程走查：模拟用户操作流程

## 5. 验收标准
- 所有UI元素与设计稿一致度达到100%
- 所有交互状态都有对应的UI表现
- 所有异常场景都有友好的错误提示
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def save_history(record):
    """保存生成历史"""
    history_file = Path('history.json')
    
    if history_file.exists():
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []
    
    history.insert(0, record)  # 最新的在前面
    history = history[:50]  # 只保留最近50条
    
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    print("🚀 UI走查用例生成助手 - 后端服务")
    print("📍 访问地址: http://localhost:5000")
    print("📖 API文档: http://localhost:5000/api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)
