# UI走查用例生成智能体设计方案

## 1. 智能体概述

### 1.1 智能体名称
**UI走查用例生成助手（UI Test Case Generator Agent）**

### 1.2 核心功能
自动化生成UI走查用例和走查计划，支持CSV和Excel多Sheet两种格式输出。

### 1.3 目标用户
- UI设计师
- 前端开发工程师
- 测试工程师
- 产品经理

## 2. 智能体架构

### 2.1 整体架构
```
用户输入（需求文档）
    ↓
智能体处理流程
    ├── 需求分析模块
    ├── 用例生成模块
    ├── 格式转换模块
    └── 文件输出模块
    ↓
输出结果（CSV/Excel + 走查计划）
```

### 2.2 核心模块

#### 模块1：需求分析模块
- 读取需求文档
- 识别功能模块
- 提取页面结构
- 识别上下游关系

#### 模块2：用例生成模块
- 应用8大UI走查原则
- 生成检查点
- 生成检查项
- 生成预期结果

#### 模块3：格式转换模块
- CSV格式生成
- Excel多Sheet格式生成
- 自动统计功能配置

#### 模块4：文件输出模块
- 生成用例文件
- 生成走查计划
- 生成使用说明

## 3. 实现方案

### 方案一：基于Kiro Hook的智能体（推荐）

#### 3.1 创建Hook触发器
在Kiro中创建一个Hook，当用户保存需求文档时自动触发。

#### 3.2 Hook配置
```yaml
name: UI走查用例生成
trigger: 文件保存
file_pattern: "*需求文档*.md"
action: 执行智能体
```

#### 3.3 智能体Prompt

```markdown
你是一个UI走查用例生成专家。请根据用户提供的需求文档，自动生成UI走查用例和走查计划。

## 工作流程
1. 读取需求文档，识别功能模块和页面结构
2. 应用8大UI走查原则，生成UI走查用例
3. 根据用例数量和模块数量，选择输出格式：
   - 用例数 > 50 或 模块数 > 3：生成Excel多Sheet格式
   - 用例数 ≤ 50 且 模块数 ≤ 3：生成CSV格式
4. 生成UI走查计划文档
5. 生成使用说明文档

## 输出要求
- UI走查用例文件（CSV或Excel）
- UI走查计划文档（Markdown）
- 快速开始指南（Markdown）

## 参考规则
- CSV格式：参考 AI生成UI走查用例规则.md
- Excel格式：参考 AI生成Excel多Sheet UI走查用例规则.md
- 走查计划：参考 UI走查计划模板.md
```

### 方案二：基于命令行的智能体

#### 3.1 创建CLI工具
```bash
ui-test-gen --input 需求文档.md --output UI用例/ --format excel
```

#### 3.2 参数说明
- `--input`: 需求文档路径
- `--output`: 输出目录
- `--format`: 输出格式（csv/excel/both）
- `--auto`: 自动选择格式

### 方案三：基于Web界面的智能体

#### 3.1 Web界面设计
```
┌─────────────────────────────────────┐
│  UI走查用例生成助手                  │
├─────────────────────────────────────┤
│  1. 上传需求文档                     │
│     [选择文件] 需求文档.md           │
│                                     │
│  2. 选择输出格式                     │
│     ○ CSV格式                       │
│     ● Excel多Sheet格式（推荐）       │
│     ○ 自动选择                       │
│                                     │
│  3. 高级选项                         │
│     ☑ 生成走查计划                   │
│     ☑ 生成使用说明                   │
│     ☑ 应用优先级颜色                 │
│                                     │
│  [生成用例]                          │
└─────────────────────────────────────┘
```

## 4. 详细实现步骤

### 步骤1：创建智能体配置文件

创建 `ui-test-gen-agent.yaml`:
```yaml
agent:
  name: UI走查用例生成助手
  version: 1.0.0
  description: 自动生成UI走查用例和走查计划
  
triggers:
  - type: file_save
    pattern: "*需求文档*.md"
  - type: command
    command: "生成UI走查用例"
  - type: manual
    button: "生成用例"

inputs:
  - name: requirement_doc
    type: file
    required: true
    description: 需求文档路径
  
  - name: output_format
    type: select
    options: [csv, excel, auto]
    default: auto
    description: 输出格式
  
  - name: output_dir
    type: directory
    default: "UI用例/"
    description: 输出目录

outputs:
  - name: test_cases
    type: file
    description: UI走查用例文件
  
  - name: test_plan
    type: file
    description: UI走查计划文档
  
  - name: quick_start
    type: file
    description: 快速开始指南

rules:
  - file: AI生成UI走查用例规则.md
  - file: AI生成Excel多Sheet UI走查用例规则.md
  - file: UI走查计划模板.md

scripts:
  - file: csv_to_excel_multi_sheet.py
```

### 步骤2：创建智能体主程序

创建 `ui_test_gen_agent.py`:
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI走查用例生成智能体
"""

import os
import yaml
from pathlib import Path

class UITestGenAgent:
    def __init__(self, config_path='ui-test-gen-agent.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
    
    def analyze_requirement(self, doc_path):
        """分析需求文档"""
        # 读取需求文档
        # 识别功能模块
        # 提取页面结构
        pass
    
    def generate_test_cases(self, modules):
        """生成UI走查用例"""
        # 应用8大UI走查原则
        # 生成检查点和检查项
        pass
    
    def choose_format(self, case_count, module_count):
        """选择输出格式"""
        if case_count > 50 or module_count > 3:
            return 'excel'
        return 'csv'
    
    def generate_output(self, cases, format_type):
        """生成输出文件"""
        if format_type == 'excel':
            # 调用Excel生成脚本
            pass
        else:
            # 生成CSV文件
            pass
    
    def run(self, input_path, output_dir, format_type='auto'):
        """运行智能体"""
        # 1. 分析需求
        modules = self.analyze_requirement(input_path)
        
        # 2. 生成用例
        cases = self.generate_test_cases(modules)
        
        # 3. 选择格式
        if format_type == 'auto':
            format_type = self.choose_format(len(cases), len(modules))
        
        # 4. 生成输出
        self.generate_output(cases, format_type)
        
        print(f'✅ UI走查用例已生成：{output_dir}')

if __name__ == '__main__':
    agent = UITestGenAgent()
    agent.run('需求文档.md', 'UI用例/', 'auto')
```

### 步骤3：集成到Kiro

#### 3.1 创建Kiro Hook

在Kiro中打开命令面板（Cmd+Shift+P），搜索"Open Kiro Hook UI"，创建新Hook：

**Hook名称**: UI走查用例生成

**触发条件**: 文件保存

**文件模式**: `*需求文档*.md`

**执行动作**: 
```
读取当前文件内容，根据AI生成UI走查用例规则.md和AI生成Excel多Sheet UI走查用例规则.md，
自动生成UI走查用例和走查计划。
```

#### 3.2 创建Steering规则

在 `.kiro/steering/` 目录下创建 `ui-test-gen.md`:


```markdown
---
inclusion: manual
contextKey: ui-test-gen
---

# UI走查用例生成规则

当用户请求生成UI走查用例时，请遵循以下规则：

## 自动识别输出格式
- 用例数 > 50 或 模块数 > 3：使用Excel多Sheet格式
- 用例数 ≤ 50 且 模块数 ≤ 3：使用CSV格式

## 生成流程
1. 读取需求文档
2. 识别功能模块（根据章节结构）
3. 应用8大UI走查原则生成用例
4. 生成用例文件（CSV或Excel）
5. 生成走查计划文档
6. 生成快速开始指南

## 参考文档
- #[[file:AI生成UI走查用例规则.md]]
- #[[file:AI生成Excel多Sheet UI走查用例规则.md]]
- #[[file:UI走查计划模板.md]]
```

## 5. 使用方式

### 方式1：通过Hook自动触发

1. 创建或编辑需求文档（文件名包含"需求文档"）
2. 保存文件（Cmd+S）
3. Hook自动触发，生成UI走查用例
4. 在输出目录查看生成的文件

### 方式2：通过命令触发

1. 打开需求文档
2. 打开命令面板（Cmd+Shift+P）
3. 输入"生成UI走查用例"
4. 选择输出格式
5. 等待生成完成

### 方式3：通过Chat触发

在Kiro Chat中输入：
```
请根据 #需求文档.md 生成UI走查用例，使用Excel多Sheet格式
```

### 方式4：通过Python脚本

```bash
python3 ui_test_gen_agent.py --input 需求文档.md --format excel
```

## 6. 智能体优化建议

### 6.1 增加AI能力

#### 智能识别模块
使用AI自动识别需求文档中的：
- 功能模块
- 页面结构
- 交互流程
- 上下游关系

#### 智能生成用例
使用AI根据需求自动生成：
- 检查点
- 检查项
- 预期结果
- 优先级判断

### 6.2 增加模板库

创建常用场景的模板：
- 列表页模板
- 详情页模板
- 表单页模板
- 弹窗模板
- 导航菜单模板

### 6.3 增加历史记录

记录生成历史：
- 生成时间
- 需求文档版本
- 用例数量
- 修改记录

### 6.4 增加协作功能

支持团队协作：
- 用例分配
- 进度同步
- 问题跟踪
- 评审流程

## 7. 实现路线图

### Phase 1: 基础功能（已完成）
- ✅ CSV格式生成
- ✅ Excel多Sheet格式生成
- ✅ 自动统计功能
- ✅ 走查计划生成
- ✅ 使用说明文档

### Phase 2: 智能体集成（当前）
- 🔄 创建Hook触发器
- 🔄 创建Steering规则
- 🔄 集成到Kiro工作流
- 🔄 命令行工具

### Phase 3: AI增强
- ⏳ AI识别功能模块
- ⏳ AI生成用例内容
- ⏳ AI优先级判断
- ⏳ AI问题检测

### Phase 4: 协作功能
- ⏳ 用例分配
- ⏳ 进度跟踪
- ⏳ 问题管理
- ⏳ 评审流程

## 8. 快速开始

### 8.1 创建Hook（推荐）

1. 打开Kiro命令面板（Cmd+Shift+P）
2. 搜索"Open Kiro Hook UI"
3. 点击"Create New Hook"
4. 配置Hook：
   - Name: `UI走查用例生成`
   - Trigger: `File Save`
   - File Pattern: `*需求文档*.md`
   - Prompt: 
     ```
     读取当前保存的需求文档，根据以下规则生成UI走查用例：
     
     1. 参考 AI生成UI走查用例规则.md
     2. 参考 AI生成Excel多Sheet UI走查用例规则.md
     3. 参考 UI走查计划模板.md
     
     自动判断输出格式（用例数>50或模块数>3时使用Excel格式）
     生成以下文件：
     - UI走查用例文件（CSV或Excel）
     - UI走查计划文档
     - 快速开始指南
     ```
5. 保存Hook

### 8.2 创建Steering规则

1. 在项目根目录创建 `.kiro/steering/` 目录（如果不存在）
2. 创建 `ui-test-gen.md` 文件
3. 复制上面的Steering规则内容
4. 保存文件

### 8.3 测试智能体

1. 创建或打开需求文档
2. 保存文件
3. 观察Hook是否触发
4. 检查生成的文件

## 9. 故障排查

### 问题1: Hook没有触发
**解决方案**:
- 检查文件名是否包含"需求文档"
- 检查Hook是否启用
- 查看Kiro日志

### 问题2: 生成的文件格式不对
**解决方案**:
- 检查规则文件是否存在
- 检查Python脚本是否可执行
- 查看错误日志

### 问题3: Excel文件无法打开
**解决方案**:
- 检查openpyxl库是否安装
- 检查文件权限
- 尝试重新生成

## 10. 最佳实践

### 10.1 需求文档规范
- 使用清晰的章节结构
- 明确标注功能模块
- 提供页面截图或原型
- 说明交互流程

### 10.2 用例生成规范
- 优先生成高优先级用例
- 覆盖所有功能模块
- 包含异常场景
- 记录边界条件

### 10.3 团队协作规范
- 统一命名规范
- 定期同步进度
- 及时记录问题
- 定期评审用例

## 11. 扩展功能

### 11.1 集成设计工具
- Figma插件：直接从设计稿生成用例
- Sketch插件：导出设计规范
- Pixso集成：自动提取设计元素

### 11.2 集成项目管理
- Jira集成：同步用例到Jira
- Trello集成：创建走查任务卡片
- 飞书集成：发送进度通知

### 11.3 集成CI/CD
- 自动化测试：生成自动化测试脚本
- 持续集成：集成到CI流程
- 自动报告：生成测试报告

## 12. 总结

通过将现有功能封装为智能体，可以实现：

1. **自动化**：保存需求文档即可自动生成用例
2. **智能化**：AI自动识别模块和生成用例
3. **标准化**：统一的用例格式和规范
4. **协作化**：支持团队协作和进度跟踪

**下一步行动**：
1. 创建Kiro Hook
2. 测试自动生成功能
3. 根据实际使用情况优化
4. 逐步添加AI增强功能
