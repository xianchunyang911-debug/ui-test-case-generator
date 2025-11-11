#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI用例生成模块 - 支持DeepSeek和OpenAI
"""

import os
from typing import List, Dict
import json

class AIGenerator:
    """AI用例生成器"""
    
    def __init__(self, provider='deepseek', api_key=None):
        """
        初始化AI生成器
        
        Args:
            provider: 'deepseek' 或 'openai'
            api_key: API密钥
        """
        self.provider = provider
        self.api_key = api_key or os.getenv(f'{provider.upper()}_API_KEY')
        self.client = None
        self.model = None
        self.rules = self._load_rules()  # 加载规则文档
        
        # 只有在有API Key时才初始化客户端
        if self.api_key and self.api_key != 'dummy':
            try:
                from openai import OpenAI
                
                if provider == 'deepseek':
                    self.client = OpenAI(
                        api_key=self.api_key,
                        base_url="https://api.deepseek.com"
                    )
                    self.model = "deepseek-chat"
                elif provider == 'openai':
                    self.client = OpenAI(api_key=self.api_key)
                    self.model = "gpt-4"
                else:
                    raise ValueError(f"不支持的provider: {provider}")
            except ImportError:
                print("警告: openai库未安装，将使用模板生成")
                self.client = None
    
    def _load_rules(self) -> str:
        """加载UI走查规则文档"""
        rules_file = 'AI生成UI走查用例规则.md'
        try:
            if os.path.exists(rules_file):
                with open(rules_file, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"警告: 无法加载规则文档 {rules_file}: {e}")
        return ""
    
    def analyze_requirement(self, content: str) -> Dict:
        """
        分析需求文档，识别功能模块
        
        Args:
            content: 需求文档内容
            
        Returns:
            分析结果字典
        """
        # 如果没有客户端，使用基础分析
        if not self.client:
            return self._basic_analysis(content)
        
        prompt = f"""请分析以下需求文档，识别页面级别的功能模块。

需求文档：
{content[:3000]}

请返回JSON格式：
{{
    "modules": [
        {{
            "name": "模块名称",
            "description": "模块描述",
            "type": "页面类型"
        }}
    ],
    "total_modules": 数量
}}

识别规则：
1. 只识别页面级别的模块（如：首页、详情页、创建页、编辑页）
2. 不要识别小组件（如：按钮、输入框、下拉框）
3. 每个二级标题(##)通常代表一个页面模块
4. 弹窗、对话框如果功能独立也算一个模块
5. 模块名称要简洁明了（如：跨域训练首页、新建任务页）
6. 页面类型可以是：列表页、详情页、创建页、编辑页、弹窗等

注意：
- 不要过度拆分，一个完整的页面就是一个模块
- 避免识别出过多的小模块
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的UI需求分析专家。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"AI分析失败: {e}")
            # 返回基础分析结果
            return self._basic_analysis(content)
    
    def generate_test_cases(self, content: str, module: Dict) -> List[Dict]:
        """
        为指定模块生成UI走查用例
        
        Args:
            content: 需求文档内容
            module: 模块信息
            
        Returns:
            用例列表
        """
        # 如果没有客户端，使用模板生成
        if not self.client:
            return self._template_cases(module['name'])
        
        # 加载规则文档内容
        rules_context = ""
        if self.rules:
            rules_context = f"""
请严格遵循以下UI走查规则：

{self.rules[:3000]}

"""
        
        prompt = f"""{rules_context}

请为"{module['name']}"模块生成UI走查用例。

模块信息：
- 模块名称：{module['name']}
- 模块描述：{module.get('description', '')}

需求文档片段：
{content[:1500]}

必须遵循8大UI走查原则：
1. 视觉一致性原则 - 颜色、字体、图标、间距
2. 布局与响应式原则 - 对齐、响应式、内容截断
3. 组件状态完整性原则 - 按钮、输入框、链接状态
4. 内容与文案准确性原则 - 错别字、信息准确性
5. 交互与反馈原则 - 加载状态、操作反馈
6. 可访问性与可用性原则 - 键盘导航、焦点指示
7. 场景法 - 正常场景、分支场景
8. 异常与负向流程验证 - 输入验证、操作失败

严格按照CSV格式规范返回JSON：
{{
    "cases": [
        {{
            "检查点": "具体的设计元素或组件",
            "设计原则": "从8大原则中选择",
            "检查项": "描述具体的检查内容",
            "优先级": "高/中/低",
            "预期结果/设计标准": "设计稿中的具体规范或期望表现"
        }}
    ]
}}

关键要求：
1. 生成8-12个用例，覆盖8大UI走查原则
2. 字段名必须完全匹配：检查点、设计原则、检查项、优先级、预期结果/设计标准
3. 优先级只能是：高、中、低（高优先级占60%以上）
4. 所有文本内容保持单行，不要包含换行符
5. 预期结果必须具体可验证，引用设计规范的具体数值（如：字号16px，颜色#262626，间距24px）
6. 检查点基于具体的设计元素或组件（如按钮、输入框、列表等）
7. 设计原则必须从8大原则中选择：视觉一致性原则、布局与响应式原则、组件状态完整性原则、内容与文案准确性原则、交互与反馈原则、可访问性与可用性原则、场景法、异常与负向流程验证
8. 确保覆盖所有关键UI元素、组件状态、交互场景和异常流程
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的UI测试工程师，擅长编写详细的UI走查用例。请确保返回的JSON格式正确，所有字符串都要正确转义。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # 降低温度，提高稳定性
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            
            # 尝试解析JSON
            try:
                result = json.loads(content)
            except json.JSONDecodeError as je:
                print(f"JSON解析失败: {je}")
                print(f"原始内容: {content[:500]}...")
                # 尝试修复常见的JSON问题
                content = content.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
                try:
                    result = json.loads(content)
                except:
                    print("修复后仍然无法解析，使用模板生成")
                    return self._template_cases(module['name'])
            
            cases = result.get('cases', [])
            
            if not cases:
                print("AI返回的用例为空，使用模板生成")
                return self._template_cases(module['name'])
            
            # 验证和清理用例数据
            valid_cases = []
            required_fields = ['检查点', '设计原则', '检查项', '优先级', '预期结果/设计标准']
            
            for case in cases:
                # 确保所有必需字段都存在
                if all(field in case for field in required_fields):
                    # 添加模块名称
                    case['页面/模块'] = module['name']
                    # 清理字段值，移除多余的换行和空格
                    for key, value in case.items():
                        if isinstance(value, str):
                            case[key] = value.strip().replace('\n', ' ').replace('\r', '')
                    valid_cases.append(case)
                else:
                    print(f"用例缺少必需字段，跳过: {case}")
            
            if not valid_cases:
                print("没有有效的用例，使用模板生成")
                return self._template_cases(module['name'])
            
            print(f"成功生成 {len(valid_cases)} 个用例")
            return valid_cases
            
        except Exception as e:
            print(f"AI生成用例失败: {e}")
            import traceback
            traceback.print_exc()
            # 返回模板用例
            return self._template_cases(module['name'])
    
    def _basic_analysis(self, content: str) -> Dict:
        """基础分析（不使用AI）"""
        lines = content.split('\n')
        modules = []
        
        for line in lines:
            if line.startswith('##'):
                module_name = line.replace('##', '').strip()
                if module_name and not module_name[0].isdigit():
                    modules.append({
                        'name': module_name,
                        'description': '',
                        'pages': []
                    })
        
        return {
            'modules': modules[:10],  # 最多10个
            'total_modules': len(modules)
        }
    
    def _template_cases(self, module_name: str) -> List[Dict]:
        """模板用例（不使用AI）"""
        return [
            {
                '页面/模块': module_name,
                '检查点': '页面标题',
                '设计原则': '视觉一致性原则',
                '检查项': f'检查{module_name}页面标题的字体、字号、颜色',
                '优先级': '高',
                '预期结果/设计标准': '标题字号16px，字重500，颜色#262626'
            },
            {
                '页面/模块': module_name,
                '检查点': '按钮状态',
                '设计原则': '组件状态完整性原则',
                '检查项': f'检查{module_name}中主要按钮的各种状态',
                '优先级': '高',
                '预期结果/设计标准': '按钮有默认、悬停、点击、禁用状态，有平滑过渡动画'
            },
            {
                '页面/模块': module_name,
                '检查点': '操作反馈',
                '设计原则': '交互与反馈原则',
                '检查项': f'检查{module_name}中操作是否有及时反馈',
                '优先级': '高',
                '预期结果/设计标准': '操作成功/失败时显示Toast提示，加载时显示Loading'
            },
            {
                '页面/模块': module_name,
                '检查点': '输入框状态',
                '设计原则': '组件状态完整性原则',
                '检查项': f'检查{module_name}中输入框的各种状态',
                '优先级': '高',
                '预期结果/设计标准': '输入框有占位符、聚焦、已输入、错误、禁用状态'
            },
            {
                '页面/模块': module_name,
                '检查点': '页面布局',
                '设计原则': '布局与响应式原则',
                '检查项': f'检查{module_name}的页面布局和对齐',
                '优先级': '中',
                '预期结果/设计标准': '元素按网格系统对齐，间距统一'
            },
            {
                '页面/模块': module_name,
                '检查点': '错误提示',
                '设计原则': '异常与负向流程验证',
                '检查项': f'检查{module_name}中输入验证的错误提示',
                '优先级': '高',
                '预期结果/设计标准': '输入错误时显示清晰的错误提示信息'
            },
            {
                '页面/模块': module_name,
                '检查点': '文案准确性',
                '设计原则': '内容与文案准确性原则',
                '检查项': f'检查{module_name}中所有文案是否准确无误',
                '优先级': '中',
                '预期结果/设计标准': '无错别字，专业术语准确，语句通顺'
            },
            {
                '页面/模块': module_name,
                '检查点': '加载状态',
                '设计原则': '交互与反馈原则',
                '检查项': f'检查{module_name}中数据加载时的状态',
                '优先级': '中',
                '预期结果/设计标准': '数据加载时显示骨架屏或Loading动画'
            }
        ]


# 使用示例
if __name__ == '__main__':
    # 使用DeepSeek
    generator = AIGenerator(provider='deepseek', api_key='your-deepseek-api-key')
    
    # 分析需求
    content = """
    # 跨域训练功能
    
    ## 1. 跨域训练首页
    展示训练任务列表
    
    ## 2. 新建训练任务
    创建新的训练任务
    """
    
    analysis = generator.analyze_requirement(content)
    print("分析结果:", analysis)
    
    # 生成用例
    if analysis['modules']:
        cases = generator.generate_test_cases(content, analysis['modules'][0])
        print(f"生成了 {len(cases)} 个用例")
        for case in cases:
            print(f"- {case['检查点']}: {case['检查项']}")
