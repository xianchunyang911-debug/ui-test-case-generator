# 需求文档 - 在线检验功能

## 简介

在线检验功能允许测试人员在生成用例后，直接在Web界面中进行UI走查检验，实时更新每个用例的检验状态（待检验、通过、不通过），提高测试效率。

## 术语表

- **Online Verification Tab**: 在线检验标签页，位于"生成结果"标签页之后
- **Module Tabs**: 模块切换标签，用于在不同模块之间切换
- **Test Case List**: 用例列表，显示当前模块的所有用例
- **Status Dropdown**: 状态下拉框，包含"待检验"、"通过"、"不通过"三个选项
- **Verification Status**: 检验状态，记录每个用例的检验结果
- **Session State**: Streamlit会话状态，用于保存检验状态

## 需求

### 需求 1: 在线检验标签页

**用户故事:** 作为测试人员，我希望在生成用例后能看到"在线检验"标签页，以便直接在界面中进行UI走查检验

#### 验收标准

1. THE System SHALL 在"生成结果"标签页之后添加"在线检验"标签页
2. WHEN 用户未生成用例, THE System SHALL 在"在线检验"标签页显示提示信息
3. WHEN 用户已生成用例, THE System SHALL 在"在线检验"标签页显示模块切换和用例列表
4. THE System SHALL 使用Session State保存检验状态
5. THE System SHALL 在页面刷新后恢复检验状态

### 需求 2: 模块切换功能

**用户故事:** 作为测试人员，我希望能在不同模块之间切换，以便分模块进行UI走查检验

#### 验收标准

1. THE System SHALL 在"在线检验"标签页顶部显示模块切换标签
2. THE System SHALL 为每个生成用例的模块创建一个标签
3. WHEN 用户点击模块标签, THE System SHALL 切换到对应模块的用例列表
4. THE System SHALL 高亮显示当前选中的模块标签
5. THE System SHALL 在模块标签上显示该模块的用例数量

### 需求 3: 用例列表展示

**用户故事:** 作为测试人员，我希望看到当前模块的所有用例详细信息，以便进行逐条检验

#### 验收标准

1. THE System SHALL 显示当前模块的所有用例
2. THE System SHALL 为每个用例显示：用例编号、检查点、设计原则、检查项、优先级、预期结果
3. THE System SHALL 使用清晰的表格或卡片布局展示用例
4. THE System SHALL 为高优先级用例添加视觉标识
5. THE System SHALL 支持用例列表的滚动浏览

### 需求 4: 检验状态下拉框

**用户故事:** 作为测试人员，我希望为每个用例选择检验状态，以便记录检验结果

#### 验收标准

1. THE System SHALL 在每个用例的最后添加状态下拉框
2. THE System SHALL 提供三个状态选项：待检验、通过、不通过
3. WHEN 用户选择状态, THE System SHALL 立即更新并保存到Session State
4. THE System SHALL 使用不同颜色标识不同状态（待检验-灰色、通过-绿色、不通过-红色）
5. THE System SHALL 默认所有用例状态为"待检验"

### 需求 5: 检验进度统计

**用户故事:** 作为测试人员，我希望看到整体和分模块的检验进度统计，以便了解检验完成情况

#### 验收标准

1. THE System SHALL 在页面顶部显示整体检验进度
2. THE System SHALL 显示：总用例数、已检验数、通过数、不通过数、通过率
3. THE System SHALL 为每个模块显示该模块的检验进度
4. THE System SHALL 使用进度条可视化展示检验进度
5. THE System SHALL 实时更新统计数据

### 需求 6: 数据持久化和导出

**用户故事:** 作为测试人员，我希望检验状态能够保存并导出，以便后续查看和报告

#### 验收标准

1. THE System SHALL 使用Session State保存所有检验状态
2. THE System SHALL 在页面刷新后恢复检验状态
3. THE System SHALL 提供"导出检验结果"按钮
4. WHEN 用户点击导出, THE System SHALL 生成包含检验状态的CSV文件
5. THE System SHALL 在CSV文件中添加"检验状态"和"检验时间"列

### 需求 7: 快捷操作

**用户故事:** 作为测试人员，我希望有快捷操作功能，以便快速完成批量检验

#### 验收标准

1. THE System SHALL 提供"全部标记为通过"按钮
2. THE System SHALL 提供"全部标记为待检验"按钮
3. THE System SHALL 提供"重置当前模块"按钮
4. THE System SHALL 在执行批量操作前显示确认对话框
5. THE System SHALL 支持按优先级筛选用例

### 需求 8: 用户体验优化

**用户故事:** 作为测试人员，我希望界面清晰易用，操作流畅，以便高效完成检验工作

#### 验收标准

1. THE System SHALL 使用清晰的视觉层次区分不同状态的用例
2. THE System SHALL 在状态变更时提供视觉反馈
3. THE System SHALL 支持键盘快捷键操作（可选）
4. THE System SHALL 在用例较多时提供分页或虚拟滚动
5. THE System SHALL 提供搜索和过滤功能
