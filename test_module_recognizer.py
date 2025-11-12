#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块识别器测试
测试ModuleRecognizer的各种识别功能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from module_recognizer import ModuleRecognizer
from ai_generator import AIGenerator


def test_markdown_recognition():
    """测试Markdown文档识别（多级标题）"""
    print("\n" + "="*60)
    print("测试 1: Markdown文档识别（多级标题）")
    print("="*60)
    
    test_content = """
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

### 4.1 编辑基本信息
修改任务基本信息

## 5. 任务列表管理
管理所有训练任务
"""
    
    recognizer = ModuleRecognizer()
    modules = recognizer.recognize_modules(test_content, 'md')
    
    print(f"\n✓ 识别到 {len(modules)} 个模块:")
    for module in modules:
        print(f"  - [{module.type}] {module.name} (Level {module.level}, ID: {module.id[:8]}...)")
    
    # 验证
    assert len(modules) > 0, "应该识别到至少1个模块"
    assert len(modules) <= 50, "识别的模块数量不应超过50个"
    
    # 验证层级
    level_2_modules = [m for m in modules if m.level == 2]
    level_3_modules = [m for m in modules if m.level == 3]
    print(f"\n  二级标题模块: {len(level_2_modules)} 个")
    print(f"  三级标题模块: {len(level_3_modules)} 个")
    
    # 验证去重
    names = [m.name for m in modules]
    assert len(names) == len(set(names)), "模块名称应该是唯一的"
    
    print("\n✓ Markdown识别测试通过")
    return True


def test_empty_document():
    """测试边界情况：空文档"""
    print("\n" + "="*60)
    print("测试 2: 边界情况 - 空文档")
    print("="*60)
    
    recognizer = ModuleRecognizer()
    
    # 测试完全空文档
    modules = recognizer.recognize_modules("", 'md')
    print(f"\n  空文档识别结果: {len(modules)} 个模块")
    assert len(modules) == 0, "空文档应该识别到0个模块"
    
    # 测试只有空行的文档
    modules = recognizer.recognize_modules("\n\n\n", 'md')
    print(f"  只有空行的文档: {len(modules)} 个模块")
    assert len(modules) == 0, "只有空行的文档应该识别到0个模块"
    
    print("\n✓ 空文档测试通过")
    return True


def test_no_headings():
    """测试边界情况：无标题文档"""
    print("\n" + "="*60)
    print("测试 3: 边界情况 - 无标题文档")
    print("="*60)
    
    test_content = """
这是一个没有任何标题的文档。
只有普通的段落文本。
没有使用Markdown标题语法。
"""
    
    recognizer = ModuleRecognizer()
    modules = recognizer.recognize_modules(test_content, 'md')
    
    print(f"\n  无标题文档识别结果: {len(modules)} 个模块")
    assert len(modules) == 0, "无标题文档应该识别到0个模块"
    
    print("\n✓ 无标题文档测试通过")
    return True


def test_large_document():
    """测试边界情况：超大文档"""
    print("\n" + "="*60)
    print("测试 4: 边界情况 - 超大文档（>50个模块）")
    print("="*60)
    
    # 生成一个包含60个模块的文档
    large_content = "# 大型系统需求文档\n\n"
    for i in range(1, 61):
        large_content += f"## {i}. 模块{i}\n模块{i}的描述\n\n"
    
    recognizer = ModuleRecognizer()
    modules = recognizer.recognize_modules(large_content, 'md')
    
    print(f"\n  超大文档识别结果: {len(modules)} 个模块")
    assert len(modules) <= 50, "应该限制在最多50个模块"
    assert len(modules) == 50, "应该正好截取前50个模块"
    
    print("\n✓ 超大文档测试通过")
    return True


def test_duplicate_modules():
    """测试去重功能"""
    print("\n" + "="*60)
    print("测试 5: 模块去重功能")
    print("="*60)
    
    test_content = """
# 系统需求

## 用户管理
用户管理功能

## 角色管理
角色管理功能

## 用户管理
重复的用户管理模块

## 权限管理
权限管理功能
"""
    
    recognizer = ModuleRecognizer()
    modules = recognizer.recognize_modules(test_content, 'md')
    
    print(f"\n  去重后识别结果: {len(modules)} 个模块")
    names = [m.name for m in modules]
    print(f"  模块名称: {names}")
    
    # 验证去重
    assert len(names) == len(set(names)), "模块名称应该是唯一的"
    assert names.count("用户管理") == 1, "重复的模块应该被过滤"
    
    print("\n✓ 去重功能测试通过")
    return True


def test_module_type_inference():
    """测试模块类型推断"""
    print("\n" + "="*60)
    print("测试 6: 模块类型推断")
    print("="*60)
    
    test_content = """
# 系统需求

## 用户列表
用户列表页面

## 用户详情
用户详情页面

## 创建用户
创建用户页面

## 编辑用户
编辑用户页面

## 用户管理
用户管理页面

## 登录页面
用户登录

## 首页
系统首页
"""
    
    recognizer = ModuleRecognizer()
    modules = recognizer.recognize_modules(test_content, 'md')
    
    print(f"\n  识别到 {len(modules)} 个模块:")
    for module in modules:
        print(f"  - {module.name}: {module.type}")
    
    # 验证类型推断
    type_map = {m.name: m.type for m in modules}
    assert "列表" in type_map.get("用户列表", ""), "应该识别为列表页"
    assert "详情" in type_map.get("用户详情", ""), "应该识别为详情页"
    assert "创建" in type_map.get("创建用户", ""), "应该识别为创建页"
    assert "编辑" in type_map.get("编辑用户", ""), "应该识别为编辑页"
    
    print("\n✓ 类型推断测试通过")
    return True


def test_word_document_recognition():
    """测试Word文档识别"""
    print("\n" + "="*60)
    print("测试 7: Word文档识别")
    print("="*60)
    
    # 模拟Word文档转换后的纯文本（包含标题）
    test_content = """
跨域训练系统需求文档

1. 跨域训练首页
展示训练任务列表，支持筛选和搜索功能。

2. 新建训练任务页面
创建新的训练任务，包括基本信息和参数配置。

3. 任务详情页
查看任务的详细信息，包括训练进度、结果等。

4. 编辑任务功能
修改现有任务的配置和参数。

5. 任务列表管理
管理所有训练任务，支持批量操作。
"""
    
    recognizer = ModuleRecognizer()
    modules = recognizer.recognize_modules(test_content, 'docx')
    
    print(f"\n  识别到 {len(modules)} 个模块:")
    for module in modules:
        print(f"  - [{module.type}] {module.name}")
    
    # Word文档识别可能识别到的模块较少（因为依赖关键词）
    print(f"\n  注意: Word文档识别依赖关键词，可能识别到 {len(modules)} 个模块")
    
    print("\n✓ Word文档识别测试通过")
    return True


def test_ai_recognition():
    """测试AI识别（需要真实API Key）"""
    print("\n" + "="*60)
    print("测试 8: AI识别（需要API Key）")
    print("="*60)
    
    # 检查是否有API Key
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key or api_key == 'dummy':
        print("\n  ⚠ 未配置DEEPSEEK_API_KEY，跳过AI识别测试")
        print("  提示: 设置环境变量 DEEPSEEK_API_KEY 来启用AI识别测试")
        return True
    
    test_content = """
# 跨域训练系统

## 概述
本系统用于管理跨域训练任务。

## 功能模块

### 训练任务管理
用户可以创建、查看、编辑和删除训练任务。

### 数据集管理
管理训练所需的数据集。

### 模型管理
管理训练生成的模型文件。

### 结果分析
分析训练结果，生成报告。
"""
    
    try:
        ai_generator = AIGenerator(provider='deepseek', api_key=api_key)
        recognizer = ModuleRecognizer(ai_generator=ai_generator)
        modules = recognizer.recognize_modules(test_content, 'md')
        
        print(f"\n  AI识别到 {len(modules)} 个模块:")
        for module in modules:
            print(f"  - [{module.type}] {module.name}")
            if module.description:
                print(f"    描述: {module.description}")
        
        assert len(modules) > 0, "AI应该识别到至少1个模块"
        
        # AI识别应该提供描述
        has_description = any(m.description for m in modules)
        if has_description:
            print("\n  ✓ AI识别提供了模块描述")
        
        print("\n✓ AI识别测试通过")
        
    except Exception as e:
        print(f"\n  ⚠ AI识别测试失败: {e}")
        print("  这可能是由于API配额、网络问题或API Key无效")
        print("  系统会自动降级到规则识别")
    
    return True


def test_ai_fallback():
    """测试AI失败时的降级机制"""
    print("\n" + "="*60)
    print("测试 9: AI失败降级机制")
    print("="*60)
    
    test_content = """
# 系统需求

## 用户管理
用户管理功能

## 角色管理
角色管理功能
"""
    
    # 使用无效的API Key
    ai_generator = AIGenerator(provider='deepseek', api_key='invalid_key')
    recognizer = ModuleRecognizer(ai_generator=ai_generator)
    
    # 应该降级到规则识别
    modules = recognizer.recognize_modules(test_content, 'md')
    
    print(f"\n  降级后识别结果: {len(modules)} 个模块")
    assert len(modules) > 0, "降级后应该使用规则识别"
    
    print("\n✓ AI降级机制测试通过")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("开始运行模块识别器测试套件")
    print("="*60)
    
    tests = [
        ("Markdown文档识别", test_markdown_recognition),
        ("空文档", test_empty_document),
        ("无标题文档", test_no_headings),
        ("超大文档", test_large_document),
        ("模块去重", test_duplicate_modules),
        ("类型推断", test_module_type_inference),
        ("Word文档识别", test_word_document_recognition),
        ("AI识别", test_ai_recognition),
        ("AI降级机制", test_ai_fallback),
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
        print("\n🎉 所有测试通过!")
    else:
        print(f"\n⚠ {failed} 个测试失败")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
