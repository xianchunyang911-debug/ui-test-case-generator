#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整流程集成测试
测试从文档上传到用例生成的完整流程
"""

import sys
import os
import time

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from module_recognizer import ModuleRecognizer
from ai_generator import AIGenerator
from module import Module


def test_end_to_end_flow():
    """测试完整的端到端流程"""
    print("\n" + "="*60)
    print("测试 1: 完整端到端流程")
    print("="*60)
    print("\n流程: 上传文档 → 识别 → 选择 → 生成")
    
    # 步骤1: 模拟文档上传
    print("\n[步骤 1] 上传文档")
    content = """
# 跨域训练系统需求文档

## 1. 跨域训练首页
展示训练任务列表，支持筛选和搜索

## 2. 新建训练任务
创建新的训练任务

### 2.1 基本信息
填写任务基本信息

### 2.2 参数配置
配置训练参数

## 3. 任务详情页
查看任务详细信息

## 4. 编辑任务
修改现有任务
"""
    print(f"  ✓ 文档内容长度: {len(content)} 字符")
    
    # 步骤2: 模块识别
    print("\n[步骤 2] 模块识别")
    recognizer = ModuleRecognizer()
    modules = recognizer.recognize_modules(content, 'md')
    
    print(f"  ✓ 识别到 {len(modules)} 个模块:")
    for module in modules[:5]:  # 只显示前5个
        print(f"    - {module.name} ({module.type})")
    
    assert len(modules) > 0, "应该识别到模块"
    
    # 步骤3: 模块选择
    print("\n[步骤 3] 模块选择")
    # 模拟用户选择前3个模块
    selected_modules = modules[:3]
    selected_ids = {m.id for m in selected_modules}
    
    print(f"  ✓ 选择了 {len(selected_modules)} 个模块:")
    for module in selected_modules:
        print(f"    - {module.name}")
    
    # 模拟选择建议选项
    selected_categories = ['全局页面', '异常场景']
    print(f"  ✓ 选择了建议选项: {selected_categories}")
    
    # 步骤4: 用例生成
    print("\n[步骤 4] 用例生成")
    generator = AIGenerator(provider='deepseek', api_key='dummy')
    
    all_cases = []
    for module in selected_modules:
        module_dict = {
            'name': module.name,
            'description': module.description,
            'type': module.type
        }
        cases = generator.generate_test_cases(content, module_dict, categories=selected_categories)
        all_cases.extend(cases)
        print(f"  ✓ {module.name}: 生成 {len(cases)} 个用例")
    
    print(f"\n  ✓ 总计生成 {len(all_cases)} 个用例")
    assert len(all_cases) > 0, "应该生成用例"
    
    # 步骤5: 验证用例结构
    print("\n[步骤 5] 验证用例结构")
    required_fields = ['页面/模块', '检查点', '设计原则', '检查项', '优先级', '预期结果/设计标准']
    
    for case in all_cases[:3]:  # 检查前3个用例
        for field in required_fields:
            assert field in case, f"用例应包含字段: {field}"
    
    print(f"  ✓ 所有用例包含必需字段")
    
    print("\n✓ 完整端到端流程测试通过")
    return True


def test_data_persistence_simulation():
    """测试数据持久化（模拟）"""
    print("\n" + "="*60)
    print("测试 2: 数据持久化模拟")
    print("="*60)
    
    # 模拟Session State
    session_state = {}
    
    # 步骤1: 识别模块并保存
    print("\n[步骤 1] 识别并保存模块")
    content = """
# 系统需求

## 用户管理
用户管理功能

## 角色管理
角色管理功能
"""
    
    recognizer = ModuleRecognizer()
    modules = recognizer.recognize_modules(content, 'md')
    
    # 保存到session_state
    session_state['modules'] = modules
    session_state['selected_module_ids'] = {m.id for m in modules}
    session_state['modules_recognized'] = True
    
    print(f"  ✓ 保存了 {len(modules)} 个模块")
    print(f"  ✓ 选中了 {len(session_state['selected_module_ids'])} 个模块")
    
    # 步骤2: 模拟页面刷新
    print("\n[步骤 2] 模拟页面刷新")
    # 在真实的Streamlit中，session_state会保持
    # 这里我们验证数据仍然存在
    
    assert 'modules' in session_state
    assert 'selected_module_ids' in session_state
    assert 'modules_recognized' in session_state
    
    print(f"  ✓ 数据仍然存在")
    print(f"  ✓ 模块数量: {len(session_state['modules'])}")
    print(f"  ✓ 选中数量: {len(session_state['selected_module_ids'])}")
    
    # 步骤3: 修改选择状态
    print("\n[步骤 3] 修改选择状态")
    # 取消选择第一个模块
    first_module_id = list(session_state['selected_module_ids'])[0]
    session_state['selected_module_ids'].remove(first_module_id)
    
    print(f"  ✓ 取消选择一个模块")
    print(f"  ✓ 当前选中: {len(session_state['selected_module_ids'])} 个模块")
    
    # 步骤4: 再次模拟页面刷新
    print("\n[步骤 4] 再次模拟页面刷新")
    assert len(session_state['selected_module_ids']) == 1
    print(f"  ✓ 选择状态保持: {len(session_state['selected_module_ids'])} 个模块")
    
    print("\n✓ 数据持久化模拟测试通过")
    return True


def test_error_handling():
    """测试错误处理"""
    print("\n" + "="*60)
    print("测试 3: 错误处理")
    print("="*60)
    
    # 测试1: AI失败降级
    print("\n[测试 1] AI失败降级到规则识别")
    content = """
## 用户管理
用户管理功能
"""
    
    # 使用无效的API Key
    ai_generator = AIGenerator(provider='deepseek', api_key='invalid_key')
    recognizer = ModuleRecognizer(ai_generator=ai_generator)
    
    try:
        modules = recognizer.recognize_modules(content, 'md')
        print(f"  ✓ 降级成功，识别到 {len(modules)} 个模块")
        assert len(modules) > 0
    except Exception as e:
        print(f"  ✗ 降级失败: {e}")
        return False
    
    # 测试2: 空文档处理
    print("\n[测试 2] 空文档处理")
    recognizer = ModuleRecognizer()
    modules = recognizer.recognize_modules("", 'md')
    print(f"  ✓ 空文档返回 {len(modules)} 个模块")
    assert len(modules) == 0
    
    # 测试3: 生成失败降级到模板
    print("\n[测试 3] 生成失败降级到模板")
    generator = AIGenerator(provider='deepseek', api_key='dummy')
    module = {'name': '测试模块', 'description': '', 'type': '页面'}
    
    try:
        cases = generator.generate_test_cases("测试内容", module)
        print(f"  ✓ 降级到模板，生成 {len(cases)} 个用例")
        assert len(cases) > 0
    except Exception as e:
        print(f"  ✗ 模板生成失败: {e}")
        return False
    
    print("\n✓ 错误处理测试通过")
    return True


def test_performance():
    """测试性能"""
    print("\n" + "="*60)
    print("测试 4: 性能测试")
    print("="*60)
    
    # 测试1: 大量模块识别
    print("\n[测试 1] 大量模块识别性能")
    large_content = "# 大型系统\n\n"
    for i in range(1, 31):
        large_content += f"## {i}. 模块{i}\n模块{i}的描述\n\n"
    
    recognizer = ModuleRecognizer()
    
    start_time = time.time()
    modules = recognizer.recognize_modules(large_content, 'md')
    elapsed = time.time() - start_time
    
    print(f"  ✓ 识别 30 个模块耗时: {elapsed:.2f} 秒")
    print(f"  ✓ 识别到 {len(modules)} 个模块")
    assert elapsed < 5.0, "识别时间应该小于5秒"
    
    # 测试2: 大文档处理
    print("\n[测试 2] 大文档处理性能")
    # 创建一个大文档（约10000字符）
    large_doc = "# 大型需求文档\n\n"
    for i in range(1, 21):
        large_doc += f"## {i}. 模块{i}\n"
        large_doc += "这是一个详细的模块描述。" * 50
        large_doc += "\n\n"
    
    start_time = time.time()
    modules = recognizer.recognize_modules(large_doc, 'md')
    elapsed = time.time() - start_time
    
    print(f"  ✓ 处理大文档（{len(large_doc)} 字符）耗时: {elapsed:.2f} 秒")
    print(f"  ✓ 识别到 {len(modules)} 个模块")
    assert elapsed < 5.0, "处理时间应该小于5秒"
    
    # 测试3: 模板生成性能
    print("\n[测试 3] 模板生成性能")
    generator = AIGenerator(provider='deepseek', api_key='dummy')
    
    start_time = time.time()
    for i in range(10):
        module = {'name': f'模块{i}', 'description': '', 'type': '页面'}
        cases = generator.generate_test_cases("测试", module)
    elapsed = time.time() - start_time
    
    print(f"  ✓ 生成 10 个模块的用例耗时: {elapsed:.2f} 秒")
    print(f"  ✓ 平均每个模块: {elapsed/10:.2f} 秒")
    assert elapsed < 5.0, "生成时间应该小于5秒"
    
    print("\n✓ 性能测试通过")
    return True


def test_edge_cases():
    """测试边界情况"""
    print("\n" + "="*60)
    print("测试 5: 边界情况")
    print("="*60)
    
    recognizer = ModuleRecognizer()
    
    # 测试1: 特殊字符
    print("\n[测试 1] 特殊字符处理")
    content = """
## 用户管理（User Management）
包含特殊字符：@#$%^&*()

## 角色/权限管理
包含斜杠
"""
    modules = recognizer.recognize_modules(content, 'md')
    print(f"  ✓ 识别到 {len(modules)} 个模块")
    assert len(modules) > 0
    
    # 测试2: 中英文混合
    print("\n[测试 2] 中英文混合")
    content = """
## User Management 用户管理
中英文混合标题

## Role Management
纯英文标题
"""
    modules = recognizer.recognize_modules(content, 'md')
    print(f"  ✓ 识别到 {len(modules)} 个模块")
    assert len(modules) > 0
    
    # 测试3: 数字编号
    print("\n[测试 3] 各种数字编号格式")
    content = """
## 1. 模块一
## 1.1 子模块
## 2.3.4 深层子模块
## （1）括号编号
## 一、中文编号
"""
    modules = recognizer.recognize_modules(content, 'md')
    print(f"  ✓ 识别到 {len(modules)} 个模块")
    for m in modules:
        print(f"    - {m.name}")
    
    # 测试4: 极短和极长的模块名
    print("\n[测试 4] 极短和极长的模块名")
    content = """
## A
极短模块名

## 这是一个非常非常非常非常非常非常非常非常非常非常非常非常非常非常非常长的模块名称用来测试系统对长标题的处理能力
极长模块名
"""
    modules = recognizer.recognize_modules(content, 'md')
    print(f"  ✓ 识别到 {len(modules)} 个模块")
    for m in modules:
        print(f"    - {m.name[:50]}{'...' if len(m.name) > 50 else ''}")
    
    print("\n✓ 边界情况测试通过")
    return True


def test_csv_generation_simulation():
    """测试CSV生成模拟"""
    print("\n" + "="*60)
    print("测试 6: CSV生成模拟")
    print("="*60)
    
    # 生成一些测试用例
    generator = AIGenerator(provider='deepseek', api_key='dummy')
    module = {'name': '用户列表', 'description': '用户列表页面', 'type': '列表页'}
    cases = generator.generate_test_cases("测试内容", module)
    
    print(f"\n  生成了 {len(cases)} 个用例")
    
    # 验证CSV字段
    print("\n  验证CSV字段:")
    csv_fields = ['页面/模块', '检查点', '设计原则', '检查项', '优先级', '预期结果/设计标准']
    
    for field in csv_fields:
        assert field in cases[0], f"应包含字段: {field}"
        print(f"  ✓ {field}")
    
    # 验证数据格式
    print("\n  验证数据格式:")
    for case in cases:
        # 检查是否有换行符（CSV不应包含换行）
        for field, value in case.items():
            if isinstance(value, str):
                assert '\n' not in value, f"字段 {field} 不应包含换行符"
                assert '\r' not in value, f"字段 {field} 不应包含回车符"
    
    print(f"  ✓ 所有字段格式正确")
    
    print("\n✓ CSV生成模拟测试通过")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("开始运行完整流程集成测试套件")
    print("="*60)
    
    tests = [
        ("完整端到端流程", test_end_to_end_flow),
        ("数据持久化模拟", test_data_persistence_simulation),
        ("错误处理", test_error_handling),
        ("性能测试", test_performance),
        ("边界情况", test_edge_cases),
        ("CSV生成模拟", test_csv_generation_simulation),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"\n✗ {test_name} 测试失败: {e}")
            failed += 1
        except Exception as e:
            print(f"\n✗ {test_name} 测试出错: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    print(f"总计: {len(tests)} 个测试")
    print(f"通过: {passed} 个")
    print(f"失败: {failed} 个")
    
    if failed == 0:
        print("\n🎉 所有集成测试通过!")
        print("\n💡 提示: 这些测试验证了核心流程和逻辑")
        print("   完整的端到端测试需要在Streamlit应用中手动验证:")
        print("   1. 上传需求文档")
        print("   2. 点击'模块/页面识别'按钮")
        print("   3. 选择需要的模块和建议选项")
        print("   4. 点击'生成UI走查用例'按钮")
        print("   5. 下载生成的CSV文件")
        print("   6. 验证页面刷新后状态保持")
    else:
        print(f"\n⚠ {failed} 个测试失败")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
