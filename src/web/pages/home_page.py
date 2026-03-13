#!/usr/bin/env python3
"""
首页
"""

from playwright.sync_api import Page
from src.core.base.base_page import BasePage

class HomePage(BasePage):
    """首页"""
    
    def __init__(self, page: Page):
        """初始化"""
        super().__init__(page)
        self.url = "/index"
    
    def navigate(self):
        """导航到首页"""
        super().navigate(self.url)
    
    def get_welcome_message(self) -> str:
        """获取欢迎信息"""
        return self.get_text(".welcome-message")
    
    def navigate_to_menu(self, menu_path: str):
        """导航到菜单"""
        # 菜单路径格式: "系统管理 > 用户管理"
        menu_items = menu_path.split(" > ")
        
        for item in menu_items:
            # 点击菜单项
            self.click(f"span:has-text('{item}')")
            # 等待页面加载
            self.wait(1)
    
    def navigate_to_user_management(self):
        """导航到用户管理"""
        self.navigate_to_menu("系统管理 > 用户管理")
    
    def navigate_to_role_management(self):
        """导航到角色管理"""
        self.navigate_to_menu("系统管理 > 角色管理")
    
    def navigate_to_menu_management(self):
        """导航到菜单管理"""
        self.navigate_to_menu("系统管理 > 菜单管理")
    
    def navigate_to_dept_management(self):
        """导航到部门管理"""
        self.navigate_to_menu("系统管理 > 部门管理")
    
    def navigate_to_config_management(self):
        """导航到配置管理"""
        self.navigate_to_menu("系统管理 > 参数设置")
    
    def navigate_to_dict_management(self):
        """导航到字典管理"""
        self.navigate_to_menu("系统管理 > 字典管理")
    
    def navigate_to_log_management(self):
        """导航到日志管理"""
        self.navigate_to_menu("系统管理 > 日志管理")
    
    def navigate_to_notice_management(self):
        """导航到通知管理"""
        self.navigate_to_menu("系统管理 > 通知管理")
    
    def get_current_menu(self) -> str:
        """获取当前菜单"""
        return self.get_text(".el-breadcrumb__item:last-child")
    
    def logout(self):
        """退出登录"""
        # 点击用户头像
        self.click(".user-avatar")
        
        # 点击退出按钮
        self.click("button:has-text('退出登录')")
        
        # 确认退出
        self.click(".el-message-box__btns button:has-text('确定')")