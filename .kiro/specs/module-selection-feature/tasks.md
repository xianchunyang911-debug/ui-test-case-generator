# 实现计划 - 模块/页面识别与选择功能

- [x] 1. 创建模块数据模型和工具类
  - 创建Module数据类，包含id、name、description、type、level、selected字段
  - 实现to_dict()和from_dict()方法用于序列化
  - 创建session_state_utils.py工具类，封装Session State初始化和管理逻辑
  - _需求: 1.3, 2.4, 5.1_

- [x] 2. 实现ModuleRecognizer模块识别器
  - [x] 2.1 创建module_recognizer.py文件，实现ModuleRecognizer类
    - 实现__init__方法，接收可选的AIGenerator参数
    - 实现recognize_modules主方法，根据文件类型调用不同识别策略
    - _需求: 1.1, 1.4_
  
  - [x] 2.2 实现规则识别方法
    - 实现_recognize_from_markdown方法，从##、###标题识别模块
    - 实现_recognize_from_docx方法，从Word标题样式识别模块
    - 为每个识别的模块生成唯一ID（使用uuid或hash）
    - 识别模块的层级（level）和类型（type）
    - _需求: 1.4_
  
  - [x] 2.3 实现AI识别方法
    - 实现_recognize_with_ai方法，调用AIGenerator.analyze_requirement
    - 将AI返回的JSON结果转换为Module对象列表
    - 实现错误处理，AI失败时降级到规则识别
    - _需求: 1.1, 1.5_
  
  - [x] 2.4 添加识别结果验证
    - 验证识别出的模块数量（至少1个，最多50个）
    - 过滤重复模块（基于name去重）
    - 为模块添加默认描述（如果AI未提供）
    - _需求: 1.2_

- [x] 3. 实现ModuleSelector模块选择器UI组件
  - [x] 3.1 创建module_selector.py文件，实现ModuleSelector类
    - 实现__init__方法，初始化Session State
    - 实现_init_session_state方法，初始化modules、selected_module_ids、suggested_categories等状态
    - _需求: 2.4, 5.1_
  
  - [x] 3.2 实现模块列表渲染
    - 实现render_module_list方法，使用st.checkbox渲染每个模块
    - 为每个复选框设置唯一的key（基于module.id）
    - 使用st.session_state存储选中状态，避免页面刷新
    - 显示模块名称、描述、类型信息
    - _需求: 2.1, 2.3, 5.2_
  
  - [x] 3.3 实现快捷操作按钮
    - 添加"全选"按钮，点击时选中所有模块
    - 添加"全不选"按钮，点击时取消所有选择
    - 添加"重新识别"按钮，清除当前识别结果
    - 使用st.columns布局按钮
    - _需求: 2.2, 5.5_
  
  - [x] 3.4 实现建议选项渲染
    - 实现render_suggested_categories方法
    - 渲染4个建议选项复选框：全局页面、场景流程、异常场景、上下游验证
    - 使用Session State存储选中状态
    - 使用st.divider分隔模块列表和建议选项
    - _需求: 3.1, 3.2, 3.4_
  
  - [x] 3.5 实现选择状态管理
    - 实现get_selected_modules方法，返回选中的Module对象列表
    - 实现get_selected_categories方法，返回选中的建议选项列表
    - 实时显示已选择的模块数量（X/Y格式）
    - _需求: 2.5, 3.3_
  
  - [x] 3.6 实现搜索和过滤功能
    - 添加st.text_input搜索框
    - 根据搜索关键词过滤模块列表
    - 支持按模块名称和描述搜索
    - _需求: 6.5_

- [x] 4. 实现TestCaseCoordinator用例生成协调器
  - [x] 4.1 创建test_case_coordinator.py文件，实现TestCaseCoordinator类
    - 实现__init__方法，接收AIGenerator参数
    - 实现generate_cases_for_selected主方法
    - _需求: 4.1, 4.3_
  
  - [x] 4.2 实现建议选项提示词增强
    - 实现_enhance_prompt_with_categories方法
    - 根据选中的建议选项，在AI提示词中添加特定指导
    - 全局页面：强调通用组件和导航
    - 场景流程：强调用户操作流程和步骤
    - 异常场景：强调错误处理和边界情况
    - 上下游验证：强调数据流转和接口验证
    - _需求: 3.5, 4.4_
  
  - [x] 4.3 实现批量生成逻辑
    - 遍历选中的模块列表
    - 为每个模块调用AIGenerator.generate_test_cases
    - 使用st.progress显示生成进度
    - 收集所有生成的用例到统一列表
    - _需求: 4.3, 4.5_
  
  - [x] 4.4 实现错误处理和降级
    - 捕获单个模块生成失败的异常
    - 失败时使用模板生成（_template_cases）
    - 显示警告信息但继续生成其他模块
    - 记录生成成功和失败的模块数量
    - _需求: 4.5_

- [x] 5. 集成到streamlit_app.py主应用
  - [x] 5.1 重构文档上传流程
    - 修改tab1（上传文档）的逻辑
    - 上传后将内容存储到st.session_state['uploaded_content']
    - 存储文件名和文件类型
    - 移除原有的"生成UI走查用例"按钮
    - _需求: 1.1_
  
  - [x] 5.2 添加模块识别按钮和逻辑
    - 在文档预览下方添加"🔍 模块/页面识别"按钮
    - 点击时调用ModuleRecognizer.recognize_modules
    - 将识别结果存储到st.session_state['modules']
    - 显示识别成功提示和模块数量
    - 使用st.spinner显示识别进度
    - _需求: 1.1, 1.2, 6.2_
  
  - [x] 5.3 渲染模块选择界面
    - 识别成功后，实例化ModuleSelector
    - 调用render_module_list渲染模块列表
    - 调用render_suggested_categories渲染建议选项
    - 使用st.expander可折叠显示模块列表（如果模块数量>10）
    - _需求: 2.1, 3.1, 6.1_
  
  - [x] 5.4 添加生成按钮和逻辑
    - 在模块选择界面下方添加"🚀 生成UI走查用例"按钮
    - 检查是否有选中的模块，无选中时禁用按钮
    - 点击时调用TestCaseCoordinator.generate_cases_for_selected
    - 传递选中的模块和建议选项
    - _需求: 4.1, 4.2_
  
  - [x] 5.5 保持原有的CSV生成和下载逻辑
    - 生成完成后，保存到CSV文件
    - 更新st.session_state['generated_file']和st.session_state['all_cases']
    - 在tab2（生成结果）中显示结果
    - 保持原有的下载和预览功能
    - _需求: 4.5_
  
  - [x] 5.6 实现数据持久化和恢复
    - 页面加载时检查Session State中是否有识别结果
    - 如果有，直接显示模块选择界面
    - 保持用户的选择状态（复选框状态）
    - 提供"清除数据"按钮重置所有状态
    - _需求: 5.3, 5.4, 5.5_

- [x] 6. 优化用户体验
  - [x] 6.1 添加视觉反馈
    - 使用st.success显示成功消息
    - 使用st.error显示错误消息
    - 使用st.info显示提示信息
    - 使用st.warning显示警告信息
    - _需求: 6.2_
  
  - [x] 6.2 优化布局和样式
    - 使用st.columns优化按钮布局
    - 使用st.divider分隔不同区域
    - 为模块列表添加边框和背景色（使用st.container）
    - 高亮显示选中的模块
    - _需求: 6.1, 6.3_
  
  - [x] 6.3 添加帮助文本和提示
    - 为"模块/页面识别"按钮添加help参数
    - 为建议选项添加说明文本
    - 在未选择模块时显示提示信息
    - 添加使用指南（可折叠）
    - _需求: 6.1_

- [x] 7. 更新AI生成器以支持建议选项
  - [x] 7.1 修改AIGenerator.generate_test_cases方法
    - 添加可选参数categories: List[str]
    - 根据categories调整生成提示词
    - 全局页面：增加导航、头部、底部等通用组件的用例
    - 场景流程：增加多步骤操作流程的用例
    - 异常场景：增加错误处理、边界条件的用例
    - 上下游验证：增加数据流转、接口调用的用例
    - _需求: 3.5, 4.4_
  
  - [x] 7.2 优化提示词模板
    - 为每个建议选项创建专门的提示词片段
    - 在主提示词中动态插入选中的建议选项指导
    - 确保生成的用例覆盖建议选项的重点
    - _需求: 4.4_

- [x] 8. 测试和验证
  - [x] 8.1 测试模块识别功能
    - 测试Markdown文档识别（多级标题）
    - 测试Word文档识别
    - 测试AI识别（使用真实API Key）
    - 测试边界情况（空文档、无标题、超大文档）
    - _需求: 1.1, 1.4, 1.5_
  
  - [x] 8.2 测试模块选择功能
    - 测试复选框交互（选中、取消）
    - 测试全选/全不选功能
    - 测试搜索过滤功能
    - 验证点击复选框时页面不刷新
    - _需求: 2.1, 2.2, 2.3, 5.2_
  
  - [x] 8.3 测试建议选项功能
    - 测试建议选项复选框
    - 验证建议选项传递到生成器
    - 检查生成的用例是否符合建议选项要求
    - _需求: 3.1, 3.3, 3.5_
  
  - [x] 8.4 测试完整流程
    - 上传文档 → 识别 → 选择 → 生成 → 下载
    - 测试数据持久化（刷新页面后状态保持）
    - 测试错误处理（AI失败、网络错误等）
    - 测试性能（大量模块、大文档）
    - _需求: 所有需求_

- [x] 9. 文档更新
  - [x] 9.1 更新README.md
    - 添加模块识别与选择功能的说明
    - 更新使用流程说明
    - 添加建议选项的使用建议
    - 更新截图和示例
  
  - [x] 9.2 更新帮助文档
    - 在应用内添加使用指南
    - 说明建议选项的含义和使用场景
    - 提供最佳实践建议
