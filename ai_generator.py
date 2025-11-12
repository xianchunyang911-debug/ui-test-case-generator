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
    
    def generate_test_cases(self, content: str, module: Dict, categories: List[str] = None) -> List[Dict]:
        """
        为指定模块生成UI走查用例
        
        Args:
            content: 需求文档内容
            module: 模块信息
            categories: 建议选项列表（全局页面、场景流程、异常场景、上下游验证）
            
        Returns:
            用例列表
        """
        # 如果没有客户端，使用模板生成
        if not self.client:
            return self._template_cases(module['name'], categories)
        
        # 加载规则文档内容
        rules_context = ""
        if self.rules:
            rules_context = f"""
请严格遵循以下UI走查规则：

{self.rules[:3000]}

"""
        
        # 根据建议选项增强提示词
        category_guidance = self._build_category_guidance(categories)
        
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

{category_guidance}

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
                    return self._template_cases(module['name'], categories)
            
            cases = result.get('cases', [])
            
            if not cases:
                print("AI返回的用例为空，使用模板生成")
                return self._template_cases(module['name'], categories)
            
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
                return self._template_cases(module['name'], categories)
            
            print(f"成功生成 {len(valid_cases)} 个用例")
            return valid_cases
            
        except Exception as e:
            print(f"AI生成用例失败: {e}")
            import traceback
            traceback.print_exc()
            # 返回模板用例
            return self._template_cases(module['name'], categories)
    
    def _build_category_guidance(self, categories: List[str] = None) -> str:
        """
        根据建议选项构建提示词指导
        
        Args:
            categories: 建议选项列表
            
        Returns:
            提示词片段
        """
        if not categories:
            return ""
        
        guidance_parts = []
        
        # 定义每个建议选项的提示词片段
        category_prompts = {
            '全局页面': """
【全局页面测试重点】
请特别关注以下通用组件和全局元素的测试用例：
- 页面头部（Header）：Logo、导航菜单、用户信息、搜索框等
- 页面底部（Footer）：版权信息、链接、联系方式等
- 侧边导航栏：菜单项、展开/收起状态、选中状态
- 面包屑导航：层级显示、点击跳转
- 全局提示组件：Toast、Message、Notification
- 全局加载状态：页面级Loading、骨架屏
- 通用按钮和图标：确保在不同页面中保持一致
- 响应式布局：在不同屏幕尺寸下的表现
请为这些全局组件生成至少3-4个专门的测试用例。
""",
            '场景流程': """
【场景流程测试重点】
请特别关注以下多步骤操作流程的测试用例：
- 完整的用户操作路径：从进入页面到完成目标的全流程
- 多步骤表单：步骤指示器、上一步/下一步、数据保存
- 向导式流程：引导提示、进度展示、步骤跳转
- 数据提交流程：填写→预览→确认→提交→反馈
- 审批流程：提交→审核→通过/驳回→通知
- 搜索筛选流程：输入条件→搜索→结果展示→详情查看
- 状态流转：草稿→待审核→已发布等状态变化
请为关键业务流程生成至少3-4个端到端的测试用例，覆盖正常路径和分支路径。
""",
            '异常场景': """
【异常场景测试重点】
请特别关注以下错误处理和边界条件的测试用例：
- 输入验证：必填项、格式校验、长度限制、特殊字符
- 网络异常：请求超时、网络断开、服务器错误（500、502等）
- 权限异常：无权限访问、登录过期、Token失效
- 数据异常：空数据、数据加载失败、数据格式错误
- 操作冲突：并发操作、重复提交、数据已被修改
- 边界条件：最大值、最小值、空值、极限数据量
- 错误提示：清晰的错误信息、友好的错误页面、错误恢复指引
- 降级处理：功能不可用时的降级方案
请为各类异常情况生成至少4-5个测试用例，确保系统的健壮性。
""",
            '上下游验证': """
【上下游验证测试重点】
请特别关注以下数据流转和接口调用的测试用例：
- 数据传递：页面间参数传递、数据回显、数据同步
- 接口调用：请求参数正确性、响应数据处理、错误处理
- 状态同步：操作后相关页面/组件的状态更新
- 缓存处理：数据缓存、缓存更新、缓存失效
- 消息通知：操作后的消息推送、通知展示
- 关联数据：主数据变更后关联数据的更新
- 跨页面影响：在A页面操作后，B页面的数据是否正确更新
- 数据一致性：列表页和详情页数据一致、编辑前后数据一致
请为数据流转和接口交互生成至少3-4个测试用例，确保上下游数据的正确性。
"""
        }
        
        # 根据选中的建议选项构建指导文本
        for category in categories:
            if category in category_prompts:
                guidance_parts.append(category_prompts[category])
        
        if guidance_parts:
            return "\n" + "\n".join(guidance_parts) + "\n"
        
        return ""
    
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
    
    def _template_cases(self, module_name: str, categories: List[str] = None) -> List[Dict]:
        """
        模板用例（不使用AI）
        
        Args:
            module_name: 模块名称
            categories: 建议选项列表
            
        Returns:
            用例列表
        """
        # 基础用例
        base_cases = [
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
        
        # 根据建议选项添加额外用例
        if categories:
            additional_cases = self._get_category_template_cases(module_name, categories)
            base_cases.extend(additional_cases)
        
        return base_cases
    
    def _get_category_template_cases(self, module_name: str, categories: List[str]) -> List[Dict]:
        """
        根据建议选项生成额外的模板用例
        
        Args:
            module_name: 模块名称（可以是实际模块名或建议选项名称）
            categories: 建议选项列表
            
        Returns:
            额外的用例列表
        """
        additional_cases = []
        
        # 全局页面用例
        if '全局页面' in categories:
            additional_cases.extend([
                {
                    '页面/模块': module_name,
                    '检查点': '页面头部',
                    '设计原则': '视觉一致性原则',
                    '检查项': f'检查{module_name}的页面头部Logo、导航菜单、用户信息等全局元素',
                    '优先级': '高',
                    '预期结果/设计标准': '头部高度64px，Logo尺寸120x32px，导航菜单字号14px'
                },
                {
                    '页面/模块': module_name,
                    '检查点': '页面底部',
                    '设计原则': '视觉一致性原则',
                    '检查项': f'检查{module_name}的页面底部版权信息、链接等全局元素',
                    '优先级': '中',
                    '预期结果/设计标准': '底部高度48px，文字颜色#999999，字号12px'
                },
                {
                    '页面/模块': module_name,
                    '检查点': '全局提示组件',
                    '设计原则': '交互与反馈原则',
                    '检查项': f'检查{module_name}中Toast、Message等全局提示组件的样式和行为',
                    '优先级': '高',
                    '预期结果/设计标准': 'Toast自动消失时间3秒，位置居中顶部，有淡入淡出动画'
                }
            ])
        
        # 场景流程用例
        if '场景流程' in categories:
            additional_cases.extend([
                {
                    '页面/模块': module_name,
                    '检查点': '完整操作流程',
                    '设计原则': '场景法',
                    '检查项': f'检查{module_name}的完整用户操作路径，从进入到完成目标',
                    '优先级': '高',
                    '预期结果/设计标准': '流程步骤清晰，每步有明确的操作指引和反馈'
                },
                {
                    '页面/模块': module_name,
                    '检查点': '多步骤表单',
                    '设计原则': '场景法',
                    '检查项': f'检查{module_name}中多步骤表单的步骤指示器、上一步/下一步按钮',
                    '优先级': '高',
                    '预期结果/设计标准': '步骤指示器显示当前步骤，已完成步骤可点击返回，数据自动保存'
                },
                {
                    '页面/模块': module_name,
                    '检查点': '状态流转',
                    '设计原则': '场景法',
                    '检查项': f'检查{module_name}中数据状态的流转过程（如草稿→待审核→已发布）',
                    '优先级': '中',
                    '预期结果/设计标准': '状态变化有明确的视觉标识，状态流转符合业务逻辑'
                }
            ])
        
        # 异常场景用例
        if '异常场景' in categories:
            additional_cases.extend([
                {
                    '页面/模块': module_name,
                    '检查点': '输入验证',
                    '设计原则': '异常与负向流程验证',
                    '检查项': f'检查{module_name}中表单的输入验证（必填项、格式、长度、特殊字符）',
                    '优先级': '高',
                    '预期结果/设计标准': '必填项未填提示"该字段不能为空"，格式错误提示具体要求'
                },
                {
                    '页面/模块': module_name,
                    '检查点': '网络异常处理',
                    '设计原则': '异常与负向流程验证',
                    '检查项': f'检查{module_name}在网络异常时的处理（超时、断网、服务器错误）',
                    '优先级': '高',
                    '预期结果/设计标准': '网络异常时显示友好的错误提示，提供重试按钮'
                },
                {
                    '页面/模块': module_name,
                    '检查点': '权限异常处理',
                    '设计原则': '异常与负向流程验证',
                    '检查项': f'检查{module_name}在无权限或登录过期时的处理',
                    '优先级': '高',
                    '预期结果/设计标准': '无权限时跳转到403页面，登录过期时跳转到登录页'
                },
                {
                    '页面/模块': module_name,
                    '检查点': '边界条件',
                    '设计原则': '异常与负向流程验证',
                    '检查项': f'检查{module_name}在极限数据量、空数据等边界条件下的表现',
                    '优先级': '中',
                    '预期结果/设计标准': '空数据时显示空状态提示，大数据量时有分页或虚拟滚动'
                }
            ])
        
        # 上下游验证用例
        if '上下游验证' in categories:
            additional_cases.extend([
                {
                    '页面/模块': module_name,
                    '检查点': '数据传递',
                    '设计原则': '场景法',
                    '检查项': f'检查{module_name}与其他页面之间的数据传递和回显',
                    '优先级': '高',
                    '预期结果/设计标准': '页面间参数正确传递，数据准确回显，无数据丢失'
                },
                {
                    '页面/模块': module_name,
                    '检查点': '状态同步',
                    '设计原则': '场景法',
                    '检查项': f'检查{module_name}操作后相关页面/组件的状态更新',
                    '优先级': '高',
                    '预期结果/设计标准': '操作后相关数据实时更新，列表页和详情页数据一致'
                },
                {
                    '页面/模块': module_name,
                    '检查点': '接口调用',
                    '设计原则': '异常与负向流程验证',
                    '检查项': f'检查{module_name}的接口调用参数和响应数据处理',
                    '优先级': '中',
                    '预期结果/设计标准': '请求参数正确，响应数据正确解析，接口错误有友好提示'
                }
            ])
        
        return additional_cases


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
