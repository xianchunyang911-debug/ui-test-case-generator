# Excel多Sheet格式UI走查用例生成规范

## 目标要求
当用户请求生成UI走查用例时，创建Excel格式（.xlsx）的用例文档，按"页面/模块"分成多个工作表（Sheet），通过Tab切换查看。文件存放在`/Users/macbook/Desktop/1移动云/UI走查用例/UI用例`目录下。

## Excel格式规范

### 文件命名规范
- 文件名格式：`{页面或模块名称}-UI走查用例-{序号}.xlsx`
- 存放目录：`/Users/macbook/Desktop/1移动云/UI走查用例/UI用例`
- 示例：`/Users/macbook/Desktop/1移动云/UI走查用例/UI用例/跨域训练-UI走查用例-1.xlsx`

### Excel文件结构
Excel文件包含多个工作表（Sheet），每个Sheet对应一个页面/模块的UI走查用例。

### Sheet命名规范
- Sheet名称使用"页面/模块"名称
- Sheet名称简洁明了，不超过31个字符（Excel限制）
- 示例：`跨域训练首页`、`新建任务`、`任务详情`、`全局检查`

### Sheet组织规则
1. **按模块分Sheet**：根据需求文档的功能模块，将用例分配到不同的Sheet
2. **Sheet顺序**：按照用户操作流程顺序排列Sheet
   - 首页/列表页
   - 创建/编辑页面
   - 详情页面
   - 子模块页面
   - 场景流程
   - 异常场景
   - 上下游模块验证
   - 全局检查（放在最后）
3. **汇总Sheet**：第一个Sheet为"用例汇总"，包含所有用例的统计信息

### 用例汇总Sheet结构
第一个Sheet命名为"用例汇总"，包含以下内容：

| 列名 | 说明 | 公式 |
|------|------|------|
| 序号 | 1、2、3... | - |
| 模块名称 | 对应Sheet名称 | - |
| 用例数量 | 该模块的用例总数 | - |
| 高优先级 | 高优先级用例数量 | - |
| 中优先级 | 中优先级用例数量 | - |
| 低优先级 | 低优先级用例数量 | - |
| 完成数量 | 已完成的用例数量（自动统计） | `=COUNTIF('模块名'!H:H,"是")+COUNTIF('模块名'!H:H,"否")` |
| 完成率 | 完成数量/用例数量（自动计算） | `=IF(C2=0,"0%",TEXT(G2/C2,"0%"))` |
| 备注 | 模块说明 | - |

**自动计算说明**：
- **完成数量**：使用COUNTIF公式统计各模块Sheet中"是否通过"列（H列）选择了"是"或"否"的单元格数量
- **完成率**：使用公式计算完成数量占用例总数的百分比
- 用户在各模块Sheet中选择"是"或"否"后，汇总表会自动更新，无需手动填写

### 各模块Sheet结构
每个模块Sheet包含该模块的UI走查用例清单，列结构如下：

| 列名 | 说明 | 必填 | 列宽 | 数据验证 |
|------|------|------|------|----------|
| 用例编号 | UI-TC001、UI-TC002格式 | 是 | 12 | - |
| 页面/模块 | 所属页面或UI模块名称 | 是 | 18 | - |
| 检查点 | 具体的设计元素或组件 | 是 | 20 | - |
| 设计原则 | 具体的设计方法与原则 | 是 | 20 | - |
| 检查项 | 描述具体的检查内容 | 是 | 35 | - |
| 优先级 | 高/中/低 | 是 | 8 | - |
| 预期结果/设计标准 | 设计稿中的具体规范或期望表现 | 是 | 40 | - |
| 是否通过 | 测试结果：待测试/是/否 | 是 | 12 | 下拉选择 |
| 截图/备注 | 用于辅助说明的截图或备注信息 | 否 | 25 | - |

**"是否通过"列说明**：
- **待测试**：默认值，尚未执行测试
- **是**：UI符合预期，通过验证
- **否**：UI不符合预期，存在问题
- 使用Excel数据验证功能，提供下拉选择
- 选择"是"或"否"后，会自动更新"用例汇总"Sheet的完成进度

### Excel样式规范

#### 表头样式
- 背景色：#4472C4（蓝色）
- 字体颜色：#FFFFFF（白色）
- 字体：微软雅黑
- 字号：11pt
- 字重：加粗
- 对齐：居中
- 边框：全边框，颜色#FFFFFF

#### 数据行样式
- 字体：微软雅黑
- 字号：10pt
- 对齐：左对齐（文本列）、居中（优先级列）
- 边框：全边框，颜色#D0D0D0
- 行高：自动调整，最小20pt
- 奇偶行交替背景色：
  - 奇数行：#FFFFFF（白色）
  - 偶数行：#F2F2F2（浅灰色）

#### 优先级单元格样式
- 高优先级：背景色#FFC7CE，字体颜色#9C0006
- 中优先级：背景色#FFEB9C，字体颜色#9C6500
- 低优先级：背景色#C6EFCE，字体颜色#006100

#### 冻结窗格
- 冻结第一行（表头）
- 冻结第一列（用例编号）

## 生成方法

### 方法一：使用Python脚本生成（推荐）
由于Excel格式需要特定的库支持，推荐使用Python的`openpyxl`或`xlsxwriter`库生成。

#### 生成步骤
1. 分析需求文档，识别功能模块
2. 按模块分组用例数据
3. 创建Excel工作簿
4. 创建"用例汇总"Sheet
5. 为每个模块创建独立Sheet
6. 应用样式和格式
7. 保存Excel文件

#### Python脚本示例
```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def create_ui_test_cases_excel(output_path, modules_data):
    """
    创建UI走查用例Excel文件
    
    Args:
        output_path: 输出文件路径
        modules_data: 模块数据字典，格式：
            {
                '模块名称': [
                    {
                        '用例编号': 'UI-TC001',
                        '页面/模块': '跨域训练首页',
                        '检查点': '页面标题',
                        '设计原则': '视觉一致性原则',
                        '检查项': '检查页面标题的字体、字号、颜色',
                        '优先级': '高',
                        '预期结果/设计标准': '标题字号16px，字重500',
                        '实际结果': '',
                        '截图/备注': ''
                    },
                    ...
                ],
                ...
            }
    """
    # 创建工作簿
    wb = openpyxl.Workbook()
    wb.remove(wb.active)  # 删除默认Sheet
    
    # 定义样式
    header_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    
    data_font = Font(name='微软雅黑', size=10)
    data_alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    center_alignment = Alignment(horizontal='center', vertical='center')
    
    border = Border(
        left=Side(style='thin', color='D0D0D0'),
        right=Side(style='thin', color='D0D0D0'),
        top=Side(style='thin', color='D0D0D0'),
        bottom=Side(style='thin', color='D0D0D0')
    )
    
    # 优先级样式
    priority_styles = {
        '高': {'fill': PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid'),
               'font': Font(name='微软雅黑', size=10, color='9C0006')},
        '中': {'fill': PatternFill(start_color='FFEB9C', end_color='FFEB9C', fill_type='solid'),
               'font': Font(name='微软雅黑', size=10, color='9C6500')},
        '低': {'fill': PatternFill(start_color='C6EFCE', end_color='C6EFCE', fill_type='solid'),
               'font': Font(name='微软雅黑', size=10, color='006100')}
    }
    
    # 创建用例汇总Sheet
    summary_ws = wb.create_sheet('用例汇总', 0)
    summary_headers = ['序号', '模块名称', '用例数量', '高优先级', '中优先级', '低优先级', '完成数量', '完成率', '备注']
    summary_ws.append(summary_headers)
    
    # 应用汇总表头样式
    for col_num, header in enumerate(summary_headers, 1):
        cell = summary_ws.cell(1, col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = border
    
    # 设置汇总Sheet列宽
    summary_ws.column_dimensions['A'].width = 8
    summary_ws.column_dimensions['B'].width = 25
    summary_ws.column_dimensions['C'].width = 12
    summary_ws.column_dimensions['D'].width = 12
    summary_ws.column_dimensions['E'].width = 12
    summary_ws.column_dimensions['F'].width = 12
    summary_ws.column_dimensions['G'].width = 12
    summary_ws.column_dimensions['H'].width = 12
    summary_ws.column_dimensions['I'].width = 30
    
    # 填充汇总数据
    row_num = 2
    for module_name, cases in modules_data.items():
        total = len(cases)
        high = sum(1 for c in cases if c.get('优先级') == '高')
        medium = sum(1 for c in cases if c.get('优先级') == '中')
        low = sum(1 for c in cases if c.get('优先级') == '低')
        
        summary_ws.append([row_num - 1, module_name, total, high, medium, low, 0, '0%', ''])
        
        # 应用数据行样式
        for col_num in range(1, 10):
            cell = summary_ws.cell(row_num, col_num)
            cell.font = data_font
            cell.alignment = center_alignment if col_num <= 8 else data_alignment
            cell.border = border
            if row_num % 2 == 0:
                cell.fill = PatternFill(start_color='F2F2F2', end_color='F2F2F2', fill_type='solid')
        
        row_num += 1
    
    # 冻结汇总Sheet首行
    summary_ws.freeze_panes = 'A2'
    
    # 为每个模块创建Sheet
    headers = ['用例编号', '页面/模块', '检查点', '设计原则', '检查项', '优先级', '预期结果/设计标准', '实际结果', '截图/备注']
    col_widths = [12, 18, 20, 20, 35, 8, 40, 30, 25]
    
    for module_name, cases in modules_data.items():
        # 创建Sheet（Sheet名称不超过31字符）
        sheet_name = module_name[:31] if len(module_name) > 31 else module_name
        ws = wb.create_sheet(sheet_name)
        
        # 写入表头
        ws.append(headers)
        
        # 应用表头样式
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(1, col_num)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = border
        
        # 设置列宽
        for col_num, width in enumerate(col_widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(col_num)].width = width
        
        # 写入数据
        for row_num, case in enumerate(cases, 2):
            row_data = [
                case.get('用例编号', ''),
                case.get('页面/模块', ''),
                case.get('检查点', ''),
                case.get('设计原则', ''),
                case.get('检查项', ''),
                case.get('优先级', ''),
                case.get('预期结果/设计标准', ''),
                case.get('实际结果', ''),
                case.get('截图/备注', '')
            ]
            ws.append(row_data)
            
            # 应用数据行样式
            for col_num in range(1, 10):
                cell = ws.cell(row_num, col_num)
                cell.font = data_font
                cell.alignment = center_alignment if col_num == 6 else data_alignment
                cell.border = border
                
                # 奇偶行交替背景色
                if row_num % 2 == 0:
                    cell.fill = PatternFill(start_color='F2F2F2', end_color='F2F2F2', fill_type='solid')
                
                # 优先级单元格特殊样式
                if col_num == 6:  # 优先级列
                    priority = case.get('优先级', '')
                    if priority in priority_styles:
                        cell.fill = priority_styles[priority]['fill']
                        cell.font = priority_styles[priority]['font']
        
        # 冻结首行首列
        ws.freeze_panes = 'B2'
    
    # 保存文件
    wb.save(output_path)
    print(f'Excel文件已生成：{output_path}')

# 使用示例
if __name__ == '__main__':
    modules_data = {
        '跨域训练首页': [
            {
                '用例编号': 'UI-TC001',
                '页面/模块': '跨域训练首页',
                '检查点': '页面标题',
                '设计原则': '视觉一致性原则',
                '检查项': '检查页面标题"跨域训练"的字体、字号、颜色',
                '优先级': '高',
                '预期结果/设计标准': '标题字号16px，字重500，颜色#262626',
                '实际结果': '',
                '截图/备注': ''
            },
            # 更多用例...
        ],
        '新建跨域训练任务': [
            # 用例数据...
        ],
        # 更多模块...
    }
    
    output_path = '/Users/macbook/Desktop/1移动云/UI走查用例/UI用例/跨域训练-UI走查用例-1.xlsx'
    create_ui_test_cases_excel(output_path, modules_data)
```

### 方法二：CSV转Excel（备选）
如果已经生成了CSV文件，可以使用脚本将CSV转换为多Sheet的Excel文件。

## 模块分组规则

### 自动识别模块
根据需求文档自动识别功能模块，分组规则：

1. **按需求文档章节**：根据需求文档的一级、二级标题识别模块
2. **按页面功能**：根据页面功能划分（首页、创建、详情、列表等）
3. **按用例类型**：场景流程、异常场景、全局检查等作为独立模块

### 跨域训练功能模块分组示例
```
Sheet 1: 用例汇总
Sheet 2: 跨域训练首页
Sheet 3: 新建跨域训练任务
Sheet 4: 跨域训练任务详情
Sheet 5: 跨域训练子任务
Sheet 6: 场景流程
Sheet 7: 异常场景
Sheet 8: 上下游模块验证
Sheet 9: 全局检查
```

## 使用建议

### 执行走查时
1. 打开Excel文件
2. 从"用例汇总"Sheet了解整体进度
3. 按Sheet顺序逐个模块执行走查
4. 在"实际结果"列填写走查结果
5. 发现问题时在"截图/备注"列记录
6. 完成后更新"用例汇总"Sheet的完成数量和完成率

### 团队协作时
1. 可以将不同Sheet分配给不同的走查人员
2. 使用Excel的共享工作簿功能（如果需要）
3. 定期汇总各Sheet的走查进度
4. 使用Excel的筛选和排序功能快速定位问题

## 注意事项

1. **Sheet名称限制**：Excel的Sheet名称不能超过31个字符，需要适当缩写
2. **文件大小**：如果用例数量很大（>1000条），考虑拆分为多个Excel文件
3. **兼容性**：使用.xlsx格式，确保Excel 2007及以上版本可以打开
4. **编码问题**：使用UTF-8编码，确保中文字符正确显示
5. **公式使用**：在"用例汇总"Sheet中可以使用公式自动计算完成率
6. **版本控制**：Excel文件不适合Git版本控制，建议使用文件命名版本号管理

## 与CSV格式对比

| 特性 | CSV格式 | Excel多Sheet格式 |
|------|---------|------------------|
| 文件大小 | 小 | 较大 |
| 打开速度 | 快 | 较慢 |
| 编辑便利性 | 一般 | 好 |
| 模块分组 | 不支持 | 支持（多Sheet） |
| 样式支持 | 不支持 | 支持（颜色、字体等） |
| 公式支持 | 不支持 | 支持 |
| 版本控制 | 友好 | 不友好 |
| 团队协作 | 一般 | 好 |
| 适用场景 | 简单项目、自动化处理 | 复杂项目、人工走查 |

## 推荐使用场景

### 使用Excel多Sheet格式
- 用例数量较多（>50条）
- 功能模块较多（>3个）
- 需要团队协作执行走查
- 需要直观的进度统计
- 需要丰富的样式和格式

### 使用CSV格式
- 用例数量较少（<50条）
- 功能模块单一
- 需要自动化处理
- 需要版本控制
- 需要快速生成和编辑
