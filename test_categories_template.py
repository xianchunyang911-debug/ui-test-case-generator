#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试建议选项的模板生成功能
"""

from ai_generator import AIGenerator

# 测试模板生成（不使用AI）
generator = AIGenerator()

# 测试不带建议选项
print('=== 测试1: 不带建议选项 ===')
cases1 = generator._template_cases('测试模块')
print(f'生成用例数: {len(cases1)}')

# 测试带建议选项
print('\n=== 测试2: 带全部建议选项 ===')
categories = ['全局页面', '场景流程', '异常场景', '上下游验证']
cases2 = generator._template_cases('测试模块', categories)
print(f'生成用例数: {len(cases2)}')

# 显示额外生成的用例
print('\n额外生成的用例:')
for i, case in enumerate(cases2[len(cases1):], 1):
    print(f'{i}. {case["检查点"]} - {case["设计原则"]}')

print('\n=== 测试3: 只选择部分建议选项 ===')
categories3 = ['全局页面', '异常场景']
cases3 = generator._template_cases('测试模块', categories3)
print(f'生成用例数: {len(cases3)}')
print('额外生成的用例:')
for i, case in enumerate(cases3[len(cases1):], 1):
    print(f'{i}. {case["检查点"]} - {case["设计原则"]}')

print('\n✅ 测试完成！')
