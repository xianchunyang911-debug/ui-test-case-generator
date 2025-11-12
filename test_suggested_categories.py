#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
建议选项功能测试
测试建议选项的传递和用例生成增强
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_generator import AIGenerator
from module import Module


def test_category_guidance_building():
    """测试建议选项提示词构建"""
    print("\n" + "="*60)
    print("测试 1: 建议选项提示词构建")
    print("="*60)
    
    generator = AIGenerator(provider='deepseek', api_key='dummy')
    
    # 测试单个建议选项
    categories = ['全局页面']
    guidance = generator._build_category_guidance(categories)
    
    print(f"\n  建议选项: {categories}")
    print(f"  生成的提示词长度: {len(guidance)} 字符")
    assert len(guidance) > 0, "应该生成提示词"
    assert '全局页面' in guidance, "提示词应包含建议选项名称"
    assert '导航' in guidance or '头部' in guidance, "应包含全局页面相关的关键词"
    
    # 测试多个建议选项
    categories = ['场景流程', '异常场景']
    guidance = generator._build_category_guidance(categories)
    
    print(f"\n  建议选项: {categories}")
    print(f"  生成的提示词长度: {len(guidance)} 字符")
    assert '场景流程' in guidance, "应包含场景流程"
    assert '异常场景' in guidance, "应包含异常场景"
    assert '多步骤' in guidance or '流程' in guidance, "应包含场景流程相关的关键词"
    assert '错误' in guidance or '异常' in guidance, "应包含异常场景相关的关键词"
    
    # 测试所有建议选项
    categories = ['全局页面', '场景流程', '异常场景', '上下游验证']
    guidance = generator._build_category_guidance(categories)
    
    print(f"\n  建议选项: {categories}")
    print(f"  生成的提示词长度: {len(guidance)} 字符")
    assert all(cat in guidance for cat in categories), "应包含所有建议选项"
    
    # 测试空建议选项
    categories = []
    guidance = generator._build_category_guidance(categories)
    
    print(f"\n  建议选项: {categories}")
    print(f"  生成的提示词: '{guidance}'")
    assert guidance == "", "空建议选项应返回空字符串"
    
    # 测试None
    guidance = generator._build_category_guidance(None)
    print(f"\n  建议选项: None")
    print(f"  生成的提示词: '{guidance}'")
    assert guidance == "", "None应返回空字符串"
    
    print("\n✓ 建议选项提示词构建测试通过")
    return True


def test_category_keywords():
    """测试每个建议选项的关键词"""
    print("\n" + "="*60)
    print("测试 2: 建议选项关键词验证")
    print("="*60)
    
    generator = AIGenerator(provider='deepseek', api_key='dummy')
    
    # 定义每个建议选项应包含的关键词
    category_keywords = {
        '全局页面': ['导航', '头部', '底部', 'Header', 'Footer', '通用组件'],
        '场景流程': ['多步骤', '流程', '操作路径', '表单', '向导'],
        '异常场景': ['错误', '异常', '边界', '验证', '权限'],
        '上下游验证': ['数据', '接口', '状态', '同步', '传递']
    }
    
    for category, keywords in category_keywords.items():
        guidance = generator._build_category_guidance([category])
        
        print(f"\n  建议选项: {category}")
        found_keywords = [kw for kw in keywords if kw in guidance]
        print(f"  找到的关键词: {found_keywords}")
        
        # 至少应该包含一个关键词
        assert len(found_keywords) > 0, f"{category} 应包含至少一个关键词"
    
    print("\n✓ 建议选项关键词验证测试通过")
    return True


def test_generate_with_categories():
    """测试带建议选项的用例生成"""
    print("\n" + "="*60)
    print("测试 3: 带建议选项的用例生成")
    print("="*60)
    
    # 使用dummy API key，会降级到模板生成
    generator = AIGenerator(provider='deepseek', api_key='dummy')
    
    content = """
# 用户管理系统

## 用户列表
展示所有用户信息
"""
    
    module = {
        'name': '用户列表',
        'description': '展示所有用户信息',
        'type': '列表页'
    }
    
    # 测试不带建议选项
    cases_without = generator.generate_test_cases(content, module, categories=None)
    print(f"\n  不带建议选项生成的用例数: {len(cases_without)}")
    assert len(cases_without) > 0, "应该生成用例"
    
    # 测试带建议选项
    categories = ['全局页面', '异常场景']
    cases_with = generator.generate_test_cases(content, module, categories=categories)
    print(f"  带建议选项生成的用例数: {len(cases_with)}")
    assert len(cases_with) > 0, "应该生成用例"
    
    # 验证用例结构
    for case in cases_with[:3]:
        print(f"\n  用例示例:")
        print(f"  - 检查点: {case.get('检查点', 'N/A')}")
        print(f"  - 设计原则: {case.get('设计原则', 'N/A')}")
        print(f"  - 优先级: {case.get('优先级', 'N/A')}")
        
        assert '检查点' in case, "用例应包含检查点"
        assert '设计原则' in case, "用例应包含设计原则"
        assert '检查项' in case, "用例应包含检查项"
        assert '优先级' in case, "用例应包含优先级"
        assert '预期结果/设计标准' in case, "用例应包含预期结果"
    
    print("\n✓ 带建议选项的用例生成测试通过")
    return True


def test_template_cases_structure():
    """测试模板用例的结构"""
    print("\n" + "="*60)
    print("测试 4: 模板用例结构验证")
    print("="*60)
    
    generator = AIGenerator(provider='deepseek', api_key='dummy')
    
    module_name = "测试模块"
    cases = generator._template_cases(module_name)
    
    print(f"\n  模板用例数量: {len(cases)}")
    assert len(cases) >= 6, "模板应至少生成6个用例"
    
    # 验证必需字段
    required_fields = ['页面/模块', '检查点', '设计原则', '检查项', '优先级', '预期结果/设计标准']
    
    for idx, case in enumerate(cases):
        print(f"\n  用例 {idx + 1}:")
        for field in required_fields:
            assert field in case, f"用例应包含字段: {field}"
            print(f"  - {field}: {case[field][:50]}...")
        
        # 验证页面/模块字段
        assert case['页面/模块'] == module_name, "页面/模块应该是传入的模块名称"
        
        # 验证优先级
        assert case['优先级'] in ['高', '中', '低'], "优先级应该是高/中/低"
    
    # 验证覆盖的设计原则
    principles = set(case['设计原则'] for case in cases)
    print(f"\n  覆盖的设计原则: {principles}")
    assert len(principles) >= 4, "应该覆盖至少4个设计原则"
    
    print("\n✓ 模板用例结构验证测试通过")
    return True


def test_categories_parameter_passing():
    """测试建议选项参数传递"""
    print("\n" + "="*60)
    print("测试 5: 建议选项参数传递")
    print("="*60)
    
    generator = AIGenerator(provider='deepseek', api_key='dummy')
    
    content = "# 测试文档"
    module = {'name': '测试模块', 'description': '', 'type': '页面'}
    
    # 测试传递None
    try:
        cases = generator.generate_test_cases(content, module, categories=None)
        print(f"\n  传递 None: 生成 {len(cases)} 个用例")
        assert len(cases) > 0
    except Exception as e:
        print(f"\n  ✗ 传递 None 失败: {e}")
        return False
    
    # 测试传递空列表
    try:
        cases = generator.generate_test_cases(content, module, categories=[])
        print(f"  传递 []: 生成 {len(cases)} 个用例")
        assert len(cases) > 0
    except Exception as e:
        print(f"\n  ✗ 传递 [] 失败: {e}")
        return False
    
    # 测试传递单个建议选项
    try:
        cases = generator.generate_test_cases(content, module, categories=['全局页面'])
        print(f"  传递 ['全局页面']: 生成 {len(cases)} 个用例")
        assert len(cases) > 0
    except Exception as e:
        print(f"\n  ✗ 传递单个建议选项失败: {e}")
        return False
    
    # 测试传递多个建议选项
    try:
        cases = generator.generate_test_cases(
            content, 
            module, 
            categories=['全局页面', '场景流程', '异常场景', '上下游验证']
        )
        print(f"  传递所有建议选项: 生成 {len(cases)} 个用例")
        assert len(cases) > 0
    except Exception as e:
        print(f"\n  ✗ 传递多个建议选项失败: {e}")
        return False
    
    print("\n✓ 建议选项参数传递测试通过")
    return True


def test_coordinator_integration():
    """测试协调器集成建议选项"""
    print("\n" + "="*60)
    print("测试 6: 协调器集成建议选项")
    print("="*60)
    
    # 注意：这个测试不能完全运行，因为需要Streamlit环境
    # 但我们可以验证TestCaseCoordinator的接口
    
    from test_case_coordinator import TestCaseCoordinator
    
    generator = AIGenerator(provider='deepseek', api_key='dummy')
    
    # 验证TestCaseCoordinator接受建议选项参数
    import inspect
    sig = inspect.signature(TestCaseCoordinator.generate_cases_for_selected)
    params = list(sig.parameters.keys())
    
    print(f"\n  generate_cases_for_selected 参数: {params}")
    assert 'selected_categories' in params, "应该接受 selected_categories 参数"
    
    print("\n  ✓ TestCaseCoordinator 接口正确")
    
    # 验证AIGenerator.generate_test_cases接受categories参数
    sig = inspect.signature(AIGenerator.generate_test_cases)
    params = list(sig.parameters.keys())
    
    print(f"  generate_test_cases 参数: {params}")
    assert 'categories' in params, "应该接受 categories 参数"
    
    print("  ✓ AIGenerator 接口正确")
    
    print("\n✓ 协调器集成建议选项测试通过")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("开始运行建议选项功能测试套件")
    print("="*60)
    
    tests = [
        ("建议选项提示词构建", test_category_guidance_building),
        ("建议选项关键词验证", test_category_keywords),
        ("带建议选项的用例生成", test_generate_with_categories),
        ("模板用例结构验证", test_template_cases_structure),
        ("建议选项参数传递", test_categories_parameter_passing),
        ("协调器集成建议选项", test_coordinator_integration),
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
        print("\n💡 提示: 这些测试验证了建议选项的核心功能")
        print("   完整的端到端测试需要:")
        print("   - 在Streamlit应用中选择建议选项")
        print("   - 验证生成的用例是否符合建议选项要求")
        print("   - 检查AI生成的用例是否包含相关内容")
    else:
        print(f"\n⚠ {failed} 个测试失败")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
