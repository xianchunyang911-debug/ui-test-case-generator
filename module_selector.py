#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块选择器UI组件
管理模块选择状态和UI渲染
"""

import streamlit as st
from typing import List
from module import Module
from session_state_utils import SessionStateManager


class ModuleSelector:
    """模块选择器类"""
    
    def __init__(self):
        """初始化选择器"""
        self._init_session_state()
    
    def _init_session_state(self):
        """
        初始化Session State
        确保所有必需的状态都已初始化
        """
        SessionStateManager.init_session_state()
    
    def render_module_list(self, modules: List[Module]) -> None:
        """
        渲染模块选择列表
        
        Args:
            modules: 模块列表
        """
        if not modules:
            st.warning("未识别到任何模块")
            return
        
        # 显示模块总数
        st.markdown(f"📋 识别到 **{len(modules)}** 个模块")
        
        # 快捷操作按钮
        self._render_action_buttons()
        
        st.divider()
        
        # 搜索框
        search_keyword = self._render_search_box()
        
        # 过滤模块
        filtered_modules = self._filter_modules(modules, search_keyword)
        
        if not filtered_modules:
            st.info("没有匹配的模块")
            return
        
        # 获取当前选中的模块ID集合
        selected_ids = SessionStateManager.get_selected_module_ids()
        
        # 使用容器为模块列表添加视觉边界
        with st.container(border=True):
            st.markdown("### 📦 模块列表")
            
            for module in filtered_modules:
                # 为每个模块创建唯一的key
                checkbox_key = f"module_checkbox_{module.id}"
                
                # 检查模块是否被选中
                is_selected = module.id in selected_ids
                
                # 创建复选框 - 使用更好的列布局
                col1, col2 = st.columns([0.06, 0.94])
                
                with col1:
                    # 使用checkbox，并通过on_change回调更新状态
                    checked = st.checkbox(
                        label="",
                        value=is_selected,
                        key=checkbox_key,
                        label_visibility="collapsed",
                        on_change=self._on_module_toggle,
                        args=(module.id,)
                    )
                
                with col2:
                    # 显示模块信息 - 高亮显示选中的模块
                    if is_selected:
                        module_info = f"✅ **{module.name}**"
                    else:
                        module_info = f"**{module.name}**"
                    
                    if module.description:
                        module_info += f" - {module.description}"
                    if module.type:
                        module_info += f" `{module.type}`"
                    
                    st.markdown(module_info)
        
        # 显示选中数量
        st.divider()
        selected_count = len(selected_ids)
        total_count = len(modules)
        
        # 使用颜色标识选择状态
        if selected_count == 0:
            st.warning(f"⚠️ 已选择: **{selected_count}/{total_count}** 个模块")
        elif selected_count == total_count:
            st.success(f"✅ 已选择: **{selected_count}/{total_count}** 个模块（全选）")
        else:
            st.info(f"📊 已选择: **{selected_count}/{total_count}** 个模块")
    
    def _render_action_buttons(self):
        """渲染快捷操作按钮"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ 全选", use_container_width=True,
                        help="选中所有模块"):
                SessionStateManager.select_all_modules()
                st.rerun()
        
        with col2:
            if st.button("❌ 全不选", use_container_width=True,
                        help="取消选中所有模块"):
                SessionStateManager.deselect_all_modules()
                st.rerun()
        
        with col3:
            if st.button("🔄 重新识别", use_container_width=True,
                        help="清除当前识别结果，返回上传页面重新识别"):
                SessionStateManager.clear_recognition_data()
                st.rerun()
    
    def _render_search_box(self) -> str:
        """
        渲染搜索框
        
        Returns:
            搜索关键词
        """
        search_keyword = st.text_input(
            "🔍 搜索模块",
            placeholder="输入模块名称或描述进行搜索...",
            help="支持按模块名称和描述搜索"
        )
        return search_keyword.strip()
    
    def _filter_modules(self, modules: List[Module], keyword: str) -> List[Module]:
        """
        根据搜索关键词过滤模块
        
        Args:
            modules: 模块列表
            keyword: 搜索关键词
            
        Returns:
            过滤后的模块列表
        """
        if not keyword:
            return modules
        
        keyword_lower = keyword.lower()
        filtered = []
        
        for module in modules:
            # 在名称和描述中搜索
            if (keyword_lower in module.name.lower() or 
                keyword_lower in module.description.lower()):
                filtered.append(module)
        
        return filtered
    
    def _on_module_toggle(self, module_id: str):
        """
        模块复选框切换回调
        
        Args:
            module_id: 模块ID
        """
        SessionStateManager.toggle_module_selection(module_id)
    
    def render_suggested_categories(self) -> None:
        """渲染建议选项"""
        st.divider()
        
        # 使用容器为建议选项添加视觉边界
        with st.container(border=True):
            st.markdown("### 🎯 建议选项")
            st.markdown("💡 选择以下选项可以让AI生成更有针对性的测试用例")
            
            # 获取当前建议选项状态
            categories = SessionStateManager.get_suggested_categories()
            
            # 建议选项说明
            category_descriptions = {
                '全局页面': '包含导航、头部、底部等通用组件的测试',
                '场景流程': '包含多步骤操作流程的测试',
                '异常场景': '包含错误处理、边界条件的测试',
                '上下游验证': '包含数据流转、接口调用的测试'
            }
            
            # 使用两列布局优化建议选项显示
            col1, col2 = st.columns(2)
            
            items = list(category_descriptions.items())
            for idx, (category_name, description) in enumerate(items):
                checkbox_key = f"category_{category_name}"
                is_selected = categories.get(category_name, False)
                
                # 交替放置在两列中
                target_col = col1 if idx % 2 == 0 else col2
                
                with target_col:
                    checked = st.checkbox(
                        label=f"**{category_name}**",
                        value=is_selected,
                        key=checkbox_key,
                        on_change=self._on_category_toggle,
                        args=(category_name,),
                        help=description
                    )
    
    def _on_category_toggle(self, category_name: str):
        """
        建议选项复选框切换回调
        
        Args:
            category_name: 建议选项名称
        """
        categories = SessionStateManager.get_suggested_categories()
        current_value = categories.get(category_name, False)
        SessionStateManager.set_suggested_category(category_name, not current_value)
    
    def get_selected_modules(self) -> List[Module]:
        """
        获取用户选中的模块
        
        Returns:
            选中的Module对象列表
        """
        all_modules = SessionStateManager.get_modules()
        selected_ids = SessionStateManager.get_selected_module_ids()
        
        return [module for module in all_modules if module.id in selected_ids]
    
    def get_selected_categories(self) -> List[str]:
        """
        获取用户选中的建议选项
        
        Returns:
            选中的建议选项名称列表
        """
        return SessionStateManager.get_selected_categories()
