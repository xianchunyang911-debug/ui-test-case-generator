#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试建议选项作为独立模块生成
"""

from ai_generator import AIGenerator
from test_case_coordinator import TestCaseCoordinator

# 创建生成器和协调器
generator = AIGenerator()
coordinator = TestCaseCoordinator(ai_generator=generator)

# 测试生成建议选项模块
print('=== 测试建议选项作为独立模块 ===\n')

categories = ['全局页面', '场景流程', '异常场景', '上下游验证']
category_cases = coordinator._generate_category_modules(categories)

print(f'总共生成 {len(category_cases)} 个用例\n')

# 按模块分组统计
modules = {}
for case in category_cases:
    module = case['页面/模块']
    if module not in modules:
        modules[module] = []
    modules[module].append(case)

print('各模块用例数量:')
for module, cases in modules.items():
    print(f'  {module}: {len(cases)} 个用例')

print('\n各模块的用例列表:')
for module, cases in modules.items():
    print(f'\n【{module}】')
    for i, case in enumerate(cases, 1):
        print(f'  {i}. {case["检查点"]} - {case["设计原则"]}')

print('\n✅ 测试完成！')
print('\n说明：')
print('- 每个建议选项都生成了独立的模块')
print('- 在"在线检验"中可以看到这些模块')
print('- 可以分别对每个模块进行检验')
