# 设计文档 - 模块/页面识别与选择功能

## 概述

本设计文档描述了如何在UI走查用例生成助手中实现模块/页面识别与选择功能。该功能将原有的"一键生成"流程改为"识别→选择→生成"的三步流程，提供更灵活的用例生成控制。

核心设计理念：
- 使用Streamlit的Session State实现无刷新交互
- 分离模块识别和用例生成逻辑
- 提供直观的复选框界面
- 支持建议选项快速选择测试场景

## 架构

### 整体流程

```
用户上传文档 
    ↓
点击"模块/页面识别"
    ↓
AI/规则识别模块列表
    ↓
显示模块复选框 + 建议选项
    ↓
用户选择模块和建议选项
    ↓
点击"生成UI走查用例"
    ↓
仅为选中模块生成用例
```

### 数据流

```
Document Upload → Document Content (st.session_state)
                        ↓
                Module Recognition
                        ↓
                Module List (st.session_state)
                        ↓
                User Selection (st.session_state)
                        ↓
                Test Case Generation
                        ↓
                CSV Output
```

## 组件和接口

### 1. 模块识别器 (ModuleRecognizer)

**职责**: 从需求文档中识别模块/页面

**接口**:
```python
class ModuleRecognizer:
    def __init__(self, ai_generator: AIGenerator = None):
        """初始化识别器，可选AI支持"""
        pass
    
    def recognize_modules(self, content: str, file_type: str) -> List[Module]:
        """
        识别文档中的模块
        
        Args:
            content: 文档内容
            file_type: 文件类型 (md, txt, docx)
            
        Returns:
            模块列表
        """
        pass
    
    def _recognize_from_markdown(self, content: str) -> List[Module]:
        """从Markdown标题识别模块"""
        pass
    
    def _recognize_from_docx(self, content: str) -> List[Module]:
        """从Word文档标题样式识别模块"""
        pass
    
    def _recognize_with_ai(self, content: str) -> List[Module]:
        """使用AI识别模块（更智能）"""
        pass
```

**实现策略**:
- 优先使用AI识别（如果配置了API Key）
- 降级到规则识别（基于标题层级）
- 支持多种文档格式

### 2. 模块选择器 (ModuleSelector)

**职责**: 管理模块选择状态和UI渲染

**接口**:
```python
class ModuleSelector:
    def __init__(self):
        """初始化选择器"""
        self._init_session_state()
    
    def render_module_list(self, modules: List[Module]) -> None:
        """
        渲染模块选择列表
        
        Args:
            modules: 模块列表
        """
        pass
    
    def render_suggested_categories(self) -> None:
        """渲染建议选项"""
        pass
    
    def get_selected_modules(self) -> List[Module]:
        """获取用户选中的模块"""
        pass
    
    def get_selected_categories(self) -> List[str]:
        """获取用户选中的建议选项"""
        pass
    
    def _init_session_state(self) -> None:
        """初始化Session State"""
        pass
```

**UI布局**:
```
┌─────────────────────────────────────┐
│ 📋 识别到 X 个模块                    │
├─────────────────────────────────────┤
│ [全选] [全不选] [重新识别]            │
├─────────────────────────────────────┤
│ 模块列表                              │
│ ☑ 模块1 - 描述                        │
│ ☑ 模块2 - 描述                        │
│ ☐ 模块3 - 描述                        │
│ ...                                  │
├─────────────────────────────────────┤
│ 🎯 建议选项                           │
│ ☐ 全局页面                            │
│ ☐ 场景流程                            │
│ ☐ 异常场景                            │
│ ☐ 上下游验证                          │
├─────────────────────────────────────┤
│ 已选择: X/Y 个模块                    │
│ [🚀 生成UI走查用例]                   │
└─────────────────────────────────────┘
```

### 3. 用例生成协调器 (TestCaseCoordinator)

**职责**: 协调模块选择和用例生成

**接口**:
```python
class TestCaseCoordinator:
    def __init__(self, ai_generator: AIGenerator):
        """初始化协调器"""
        pass
    
    def generate_cases_for_selected(
        self,
        content: str,
        selected_modules: List[Module],
        selected_categories: List[str]
    ) -> List[Dict]:
        """
        为选中的模块生成用例
        
        Args:
            content: 文档内容
            selected_modules: 选中的模块
            selected_categories: 选中的建议选项
            
        Returns:
            用例列表
        """
        pass
    
    def _enhance_prompt_with_categories(
        self,
        base_prompt: str,
        categories: List[str]
    ) -> str:
        """根据建议选项增强生成提示"""
        pass
```

## 数据模型

### Module 数据结构

```python
@dataclass
class Module:
    """模块数据模型"""
    id: str                    # 唯一标识
    name: str                  # 模块名称
    description: str           # 模块描述
    type: str                  # 模块类型（列表页、详情页等）
    level: int                 # 标题层级（1-6）
    selected: bool = True      # 是否选中（默认选中）
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'level': self.level,
            'selected': self.selected
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Module':
        """从字典创建"""
        return cls(**data)
```

### Session State 结构

```python
# st.session_state 中的数据结构
{
    # 文档相关
    'uploaded_content': str,           # 上传的文档内容
    'uploaded_filename': str,          # 文档文件名
    'file_type': str,                  # 文件类型
    
    # 模块识别相关
    'modules_recognized': bool,        # 是否已识别
    'modules': List[Module],           # 识别出的模块列表
    'module_count': int,               # 模块总数
    
    # 模块选择相关
    'selected_module_ids': Set[str],   # 选中的模块ID集合
    'select_all': bool,                # 全选状态
    
    # 建议选项相关
    'suggested_categories': Dict[str, bool],  # 建议选项选中状态
    # {
    #     '全局页面': False,
    #     '场景流程': False,
    #     '异常场景': False,
    #     '上下游验证': False
    # }
    
    # 生成结果相关
    'generated_file': str,             # 生成的CSV文件路径
    'all_cases': List[Dict],           # 所有用例
    
    # 其他
    'data_cleared': bool,              # 数据是否已清除
    'ai_api_key': str,                 # AI API Key
    'ai_provider': str                 # AI提供商
}
```

## 错误处理

### 识别阶段错误

1. **文档解析失败**
   - 捕获异常并显示友好提示
   - 提供重新上传选项
   - 记录错误日志

2. **AI识别失败**
   - 自动降级到规则识别
   - 显示降级提示
   - 继续流程

3. **未识别到模块**
   - 显示"未识别到模块"提示
   - 提供手动添加模块选项
   - 建议检查文档格式

### 选择阶段错误

1. **未选择任何模块**
   - 禁用生成按钮
   - 显示提示信息
   - 高亮选择区域

2. **Session State丢失**
   - 检测状态丢失
   - 提示用户重新识别
   - 保留文档内容

### 生成阶段错误

1. **AI生成失败**
   - 降级到模板生成
   - 显示降级提示
   - 继续生成其他模块

2. **CSV写入失败**
   - 捕获IO异常
   - 提供内存下载选项
   - 显示错误详情

## 测试策略

### 单元测试

1. **ModuleRecognizer测试**
   - 测试Markdown标题识别
   - 测试Word文档识别
   - 测试AI识别（Mock）
   - 测试边界情况（空文档、无标题）

2. **ModuleSelector测试**
   - 测试Session State初始化
   - 测试选择状态管理
   - 测试全选/全不选功能

3. **TestCaseCoordinator测试**
   - 测试用例生成逻辑
   - 测试建议选项集成
   - 测试错误处理

### 集成测试

1. **完整流程测试**
   - 上传→识别→选择→生成
   - 验证数据流转
   - 验证Session State持久化

2. **UI交互测试**
   - 测试复选框交互
   - 测试页面不刷新
   - 测试按钮状态

### 用户验收测试

1. **功能验收**
   - 识别准确性
   - 选择流畅性
   - 生成正确性

2. **性能验收**
   - 识别速度（< 3秒）
   - 选择响应（即时）
   - 生成速度（< 10秒/模块）

## 性能优化

### 识别优化

1. **缓存识别结果**
   - 使用Session State缓存
   - 避免重复识别
   - 提供"重新识别"选项

2. **限制文档大小**
   - 最大10MB
   - 超大文档截取前5000行
   - 显示截取提示

### 渲染优化

1. **虚拟滚动**
   - 模块数量 > 50时启用
   - 只渲染可见区域
   - 提升滚动性能

2. **延迟加载**
   - 模块描述按需加载
   - 减少初始渲染时间

### 生成优化

1. **批量生成**
   - 每次生成5个模块
   - 显示进度条
   - 支持取消操作

2. **并发控制**
   - AI调用限流
   - 避免超出配额
   - 失败重试机制

## 可访问性

1. **键盘导航**
   - Tab键切换复选框
   - Space键切换选中状态
   - Enter键触发生成

2. **屏幕阅读器支持**
   - 为复选框添加aria-label
   - 为按钮添加描述性文本
   - 状态变化时提供反馈

3. **视觉辅助**
   - 高对比度模式
   - 焦点指示器
   - 清晰的选中状态

## 安全考虑

1. **输入验证**
   - 验证文件类型
   - 限制文件大小
   - 过滤恶意内容

2. **API Key保护**
   - 不在日志中记录
   - 使用环境变量
   - Session级别存储

3. **数据隔离**
   - 每个Session独立
   - 定期清理临时文件
   - 不持久化敏感信息

## 部署考虑

1. **Streamlit Cloud兼容**
   - 使用Session State（不依赖本地存储）
   - 文件系统操作限制在output目录
   - 环境变量配置API Key

2. **资源限制**
   - 内存使用 < 512MB
   - CPU使用合理
   - 网络请求限流

3. **监控和日志**
   - 记录识别成功率
   - 记录生成失败率
   - 记录用户操作流程
