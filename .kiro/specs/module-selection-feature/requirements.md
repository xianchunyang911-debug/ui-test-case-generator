# 需求文档 - 模块/页面识别与选择功能

## 简介

本功能旨在改进UI走查用例生成助手的工作流程，将原有的"一键生成"改为"先识别后选择"的两步流程。用户上传需求文档后，系统首先识别文档中的所有模块/页面，然后允许用户通过复选框自定义选择需要生成用例的模块，同时提供建议选项（全局页面、场景流程、异常场景、上下游验证）。

## 术语表

- **System**: UI走查用例生成助手应用
- **Module**: 需求文档中识别出的功能模块或页面
- **Checkbox**: 复选框UI组件，用于选择模块
- **Suggested Category**: 建议选项类别，包括全局页面、场景流程、异常场景、上下游验证
- **Session State**: Streamlit会话状态，用于在页面交互时保持数据不丢失
- **Document Content**: 用户上传的需求文档内容

## 需求

### 需求 1: 模块识别功能

**用户故事:** 作为测试人员，我希望上传需求文档后能看到系统识别出的所有模块/页面列表，以便了解文档结构并决定为哪些模块生成用例

#### 验收标准

1. WHEN 用户上传需求文档并点击"模块/页面识别"按钮, THE System SHALL 分析Document Content并提取所有模块和页面信息
2. THE System SHALL 在识别完成后显示模块总数统计
3. THE System SHALL 将识别结果存储在Session State中以防止页面刷新时数据丢失
4. THE System SHALL 支持从Markdown标题（##、###）、Word文档标题样式中识别Module
5. WHEN 识别过程发生错误, THE System SHALL 显示友好的错误提示信息

### 需求 2: 模块选择界面

**用户故事:** 作为测试人员，我希望通过复选框选择需要生成用例的模块，以便只为关注的功能生成用例，提高工作效率

#### 验收标准

1. THE System SHALL 为每个识别出的Module显示一个Checkbox
2. THE System SHALL 在模块列表上方显示"全选"和"全不选"快捷操作按钮
3. WHEN 用户点击Checkbox, THE System SHALL 更新选中状态但不触发页面刷新
4. THE System SHALL 使用Session State保存用户的选择状态
5. THE System SHALL 在界面上实时显示已选择的模块数量
6. THE System SHALL 默认选中所有识别出的Module

### 需求 3: 建议选项功能

**用户故事:** 作为测试人员，我希望系统提供建议的测试类别选项，以便快速选择特定类型的测试场景

#### 验收标准

1. THE System SHALL 提供四个Suggested Category复选框：全局页面、场景流程、异常场景、上下游验证
2. THE System SHALL 将Suggested Category与Module列表分开显示
3. WHEN 用户选中Suggested Category, THE System SHALL 将该类别信息传递给用例生成逻辑
4. THE System SHALL 使用Session State保存Suggested Category的选择状态
5. THE System SHALL 允许用户同时选择多个Suggested Category

### 需求 4: 用例生成集成

**用户故事:** 作为测试人员，我希望在选择完模块和建议选项后点击生成按钮，系统只为选中的模块生成用例，以便获得精准的测试用例

#### 验收标准

1. THE System SHALL 在模块选择界面下方显示"生成UI走查用例"按钮
2. WHEN 用户未选择任何Module, THE System SHALL 禁用生成按钮并显示提示信息
3. WHEN 用户点击生成按钮, THE System SHALL 仅为选中的Module生成用例
4. THE System SHALL 将Suggested Category信息作为生成参数传递给AI Generator
5. WHEN 生成完成, THE System SHALL 显示生成的用例数量和涉及的模块数量

### 需求 5: 数据持久化

**用户故事:** 作为测试人员，我希望在选择模块时页面不会刷新导致数据丢失，以便流畅地完成模块选择和用例生成流程

#### 验收标准

1. THE System SHALL 使用Session State存储所有用户交互数据
2. WHEN 用户点击Checkbox, THE System SHALL 更新状态但不触发st.rerun()
3. THE System SHALL 在页面刷新后恢复用户的模块选择状态
4. THE System SHALL 在页面刷新后恢复识别出的Module列表
5. THE System SHALL 提供"重新识别"按钮以清除当前识别结果并重新开始

### 需求 6: 用户体验优化

**用户故事:** 作为测试人员，我希望界面清晰易用，操作流程顺畅，以便快速完成工作

#### 验收标准

1. THE System SHALL 使用清晰的视觉层次区分模块列表和建议选项
2. THE System SHALL 在识别过程中显示加载动画和进度提示
3. THE System SHALL 使用不同颜色标识已选择和未选择的Module
4. THE System SHALL 在模块列表中显示每个Module的简要描述（如果可识别）
5. THE System SHALL 提供搜索或过滤功能以快速定位特定Module
