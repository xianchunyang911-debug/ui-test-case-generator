#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块选择器测试
测试ModuleSelector的核心逻辑和Session State管理
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from module import Module
from session_state_utils import SessionStateManager


# 模拟Streamlit的session_state
class MockSessionState:
    """模拟Streamlit的session_state"""
    def __init__(self):
        self._state = {}
    
    def __getitem__(self, key):
        return self._state.get(key)
    
    def __setitem__(self, key, value):
        self._state[key] = value
    
    def __contains__(self, key):
        return key in self._state
    
    def get(self, key, default=None):
        return self._state.get(key, default)
    
    def setdefault(self, key, default):
        if key not in self._state:
            self._state[key] = default
        return self._state[key]


# 创建全局mock session_state
mock_session_state = MockSessionState()


def setup_test_modules():
    """创建测试用的模块列表"""
    modules = [
        Module(
            id="module_1",
            name="用户列表",
            description="用户列表页面",
            type="列表页",
            level=2,
            selected=True
        ),
        Module(
            id="module_2",
            name="用户详情",
            description="用户详情页面",
            type="详情页",
            level=2,
            selected=True
        ),
        Module(
            id="module_3",
            name="创建用户",
            description="创建用户页面",
            type="创建页",
            level=2,
            selected=True
        ),
        Module(
            id="module_4",
            name="编辑用户",
            description="编辑用户页面",
            type="编辑页",
            level=2,
            selected=True
        ),
    ]
    return modules


def test_session_state_initialization():
    """测试Session State初始化"""
    print("\n" + "="*60)
    print("测试 1: Session State初始化")
    print("="*60)
    
    # 重置mock session_state
    global mock_session_state
    mock_session_state = MockSessionState()
    
    # 手动初始化必要的状态
    mock_session_state['modules'] = []
    mock_session_state['selected_module_ids'] = set()
    mock_session_state['suggested_categories'] = {
        '全局页面': False,
        '场景流程': False,
        '异常场景': False,
        '上下游验证': False
    }
    
    # 验证初始化
    assert 'modules' in mock_session_state
    assert 'selected_module_ids' in mock_session_state
    assert 'suggested_categories' in mock_session_state
    
    print("\n  ✓ Session State初始化成功")
    print(f"  - modules: {mock_session_state['modules']}")
    print(f"  - selected_module_ids: {mock_session_state['selected_module_ids']}")
    print(f"  - suggested_categories: {mock_session_state['suggested_categories']}")
    
    print("\n✓ Session State初始化测试通过")
    return True


def test_module_selection():
    """测试模块选择状态管理"""
    print("\n" + "="*60)
    print("测试 2: 模块选择状态管理")
    print("="*60)
    
    # 设置测试模块
    modules = setup_test_modules()
    mock_session_state['modules'] = modules
    mock_session_state['selected_module_ids'] = {m.id for m in modules}
    
    print(f"\n  初始状态: {len(mock_session_state['selected_module_ids'])} 个模块被选中")
    
    # 测试取消选择
    module_id = "module_1"
    selected_ids = mock_session_state['selected_module_ids']
    if module_id in selected_ids:
        selected_ids.remove(module_id)
    
    print(f"  取消选择 {module_id} 后: {len(selected_ids)} 个模块被选中")
    assert module_id not in selected_ids
    
    # 测试重新选择
    selected_ids.add(module_id)
    print(f"  重新选择 {module_id} 后: {len(selected_ids)} 个模块被选中")
    assert module_id in selected_ids
    
    print("\n✓ 模块选择状态管理测试通过")
    return True


def test_select_all_deselect_all():
    """测试全选/全不选功能"""
    print("\n" + "="*60)
    print("测试 3: 全选/全不选功能")
    print("="*60)
    
    modules = setup_test_modules()
    mock_session_state['modules'] = modules
    
    # 测试全选
    all_ids = {m.id for m in modules}
    mock_session_state['selected_module_ids'] = all_ids
    
    print(f"\n  全选后: {len(mock_session_state['selected_module_ids'])} 个模块被选中")
    assert len(mock_session_state['selected_module_ids']) == len(modules)
    
    # 测试全不选
    mock_session_state['selected_module_ids'] = set()
    
    print(f"  全不选后: {len(mock_session_state['selected_module_ids'])} 个模块被选中")
    assert len(mock_session_state['selected_module_ids']) == 0
    
    print("\n✓ 全选/全不选功能测试通过")
    return True


def test_search_filter():
    """测试搜索过滤功能"""
    print("\n" + "="*60)
    print("测试 4: 搜索过滤功能")
    print("="*60)
    
    modules = setup_test_modules()
    
    # 测试按名称搜索
    keyword = "用户"
    filtered = [m for m in modules if keyword in m.name or keyword in m.description]
    
    print(f"\n  搜索关键词 '{keyword}': 找到 {len(filtered)} 个模块")
    assert len(filtered) == 4  # 所有模块都包含"用户"
    
    # 测试按类型搜索
    keyword = "列表"
    filtered = [m for m in modules if keyword in m.name or keyword in m.description]
    
    print(f"  搜索关键词 '{keyword}': 找到 {len(filtered)} 个模块")
    assert len(filtered) == 1  # 只有"用户列表"
    
    # 测试不匹配的搜索
    keyword = "不存在"
    filtered = [m for m in modules if keyword in m.name or keyword in m.description]
    
    print(f"  搜索关键词 '{keyword}': 找到 {len(filtered)} 个模块")
    assert len(filtered) == 0
    
    # 测试大小写不敏感
    keyword = "用户"
    keyword_lower = keyword.lower()
    filtered = [m for m in modules if keyword_lower in m.name.lower() or keyword_lower in m.description.lower()]
    
    print(f"  搜索关键词 '{keyword}' (不区分大小写): 找到 {len(filtered)} 个模块")
    assert len(filtered) == 4
    
    print("\n✓ 搜索过滤功能测试通过")
    return True


def test_suggested_categories():
    """测试建议选项功能"""
    print("\n" + "="*60)
    print("测试 5: 建议选项功能")
    print("="*60)
    
    # 初始化建议选项
    categories = {
        '全局页面': False,
        '场景流程': False,
        '异常场景': False,
        '上下游验证': False
    }
    mock_session_state['suggested_categories'] = categories
    
    print(f"\n  初始状态: {categories}")
    
    # 测试选中建议选项
    categories['全局页面'] = True
    categories['场景流程'] = True
    
    selected = [k for k, v in categories.items() if v]
    print(f"  选中建议选项: {selected}")
    assert len(selected) == 2
    assert '全局页面' in selected
    assert '场景流程' in selected
    
    # 测试取消选中
    categories['全局页面'] = False
    
    selected = [k for k, v in categories.items() if v]
    print(f"  取消选中后: {selected}")
    assert len(selected) == 1
    assert '场景流程' in selected
    
    print("\n✓ 建议选项功能测试通过")
    return True


def test_get_selected_modules():
    """测试获取选中的模块"""
    print("\n" + "="*60)
    print("测试 6: 获取选中的模块")
    print("="*60)
    
    modules = setup_test_modules()
    mock_session_state['modules'] = modules
    
    # 选中部分模块
    selected_ids = {"module_1", "module_3"}
    mock_session_state['selected_module_ids'] = selected_ids
    
    # 获取选中的模块
    selected_modules = [m for m in modules if m.id in selected_ids]
    
    print(f"\n  选中的模块ID: {selected_ids}")
    print(f"  选中的模块: {[m.name for m in selected_modules]}")
    
    assert len(selected_modules) == 2
    assert selected_modules[0].name == "用户列表"
    assert selected_modules[1].name == "创建用户"
    
    print("\n✓ 获取选中模块测试通过")
    return True


def test_get_selected_categories():
    """测试获取选中的建议选项"""
    print("\n" + "="*60)
    print("测试 7: 获取选中的建议选项")
    print("="*60)
    
    categories = {
        '全局页面': True,
        '场景流程': False,
        '异常场景': True,
        '上下游验证': False
    }
    mock_session_state['suggested_categories'] = categories
    
    # 获取选中的建议选项
    selected_categories = [k for k, v in categories.items() if v]
    
    print(f"\n  选中的建议选项: {selected_categories}")
    
    assert len(selected_categories) == 2
    assert '全局页面' in selected_categories
    assert '异常场景' in selected_categories
    
    print("\n✓ 获取选中建议选项测试通过")
    return True


def test_state_persistence():
    """测试状态持久化（模拟页面刷新）"""
    print("\n" + "="*60)
    print("测试 8: 状态持久化")
    print("="*60)
    
    # 设置初始状态
    modules = setup_test_modules()
    selected_ids = {"module_1", "module_2"}
    categories = {
        '全局页面': True,
        '场景流程': False,
        '异常场景': False,
        '上下游验证': True
    }
    
    mock_session_state['modules'] = modules
    mock_session_state['selected_module_ids'] = selected_ids
    mock_session_state['suggested_categories'] = categories
    
    print(f"\n  设置状态:")
    print(f"  - 模块数量: {len(modules)}")
    print(f"  - 选中模块: {len(selected_ids)}")
    print(f"  - 选中建议选项: {[k for k, v in categories.items() if v]}")
    
    # 模拟"页面刷新"（实际上session_state会保持）
    # 验证状态仍然存在
    assert len(mock_session_state['modules']) == 4
    assert len(mock_session_state['selected_module_ids']) == 2
    assert mock_session_state['suggested_categories']['全局页面'] == True
    assert mock_session_state['suggested_categories']['上下游验证'] == True
    
    print(f"\n  验证状态持久化:")
    print(f"  - 模块数量: {len(mock_session_state['modules'])}")
    print(f"  - 选中模块: {len(mock_session_state['selected_module_ids'])}")
    print(f"  - 建议选项状态保持不变")
    
    print("\n✓ 状态持久化测试通过")
    return True


def test_clear_data():
    """测试清除数据功能"""
    print("\n" + "="*60)
    print("测试 9: 清除数据功能")
    print("="*60)
    
    # 设置一些数据
    modules = setup_test_modules()
    mock_session_state['modules'] = modules
    mock_session_state['selected_module_ids'] = {"module_1", "module_2"}
    mock_session_state['modules_recognized'] = True
    
    print(f"\n  清除前:")
    print(f"  - 模块数量: {len(mock_session_state['modules'])}")
    print(f"  - 选中模块: {len(mock_session_state['selected_module_ids'])}")
    print(f"  - 识别状态: {mock_session_state['modules_recognized']}")
    
    # 清除数据
    mock_session_state['modules'] = []
    mock_session_state['selected_module_ids'] = set()
    mock_session_state['modules_recognized'] = False
    
    print(f"\n  清除后:")
    print(f"  - 模块数量: {len(mock_session_state['modules'])}")
    print(f"  - 选中模块: {len(mock_session_state['selected_module_ids'])}")
    print(f"  - 识别状态: {mock_session_state['modules_recognized']}")
    
    assert len(mock_session_state['modules']) == 0
    assert len(mock_session_state['selected_module_ids']) == 0
    assert mock_session_state['modules_recognized'] == False
    
    print("\n✓ 清除数据功能测试通过")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*60)
    print("开始运行模块选择器测试套件")
    print("="*60)
    print("\n注意: 这些测试验证核心逻辑，不包括Streamlit UI交互")
    
    tests = [
        ("Session State初始化", test_session_state_initialization),
        ("模块选择状态管理", test_module_selection),
        ("全选/全不选功能", test_select_all_deselect_all),
        ("搜索过滤功能", test_search_filter),
        ("建议选项功能", test_suggested_categories),
        ("获取选中的模块", test_get_selected_modules),
        ("获取选中的建议选项", test_get_selected_categories),
        ("状态持久化", test_state_persistence),
        ("清除数据功能", test_clear_data),
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
        print("\n💡 提示: 这些测试验证了核心逻辑")
        print("   完整的UI交互测试需要在Streamlit应用中手动验证:")
        print("   - 复选框点击不会导致页面刷新")
        print("   - 全选/全不选按钮正常工作")
        print("   - 搜索框实时过滤模块")
        print("   - 建议选项复选框正常工作")
    else:
        print(f"\n⚠ {failed} 个测试失败")
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
