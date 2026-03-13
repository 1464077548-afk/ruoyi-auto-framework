#!/usr/bin/env python3
"""
登录页面
"""

from playwright.sync_api import Page
from src.core.base.base_page import BasePage

class LoginPage(BasePage):
    """登录页面"""
    
    def __init__(self, page: Page):
        """初始化"""
        super().__init__(page)
        self.url = "/login"
    
    def navigate(self):
        """导航到登录页面"""
        super().navigate(self.url)
    
    def login(self, username: str, password: str, code: str = ""):
        """登录"""
        # 输入用户名
        self.fill("input[placeholder='账号']", username)
        
        # 输入密码
        self.fill("input[placeholder='密码']", password)
        
        # 输入验证码
        if code:
            self.fill("input[placeholder='验证码']", code)
        
        # 点击登录按钮
        self.click("button:has-text('登 录')")
    
    def get_error_message(self) -> str:
        """获取错误信息"""
        return self.get_text(".el-message__content")
    
    def is_logged_in(self) -> bool:
        """检查是否登录成功"""
        return self.is_visible("#app")
    
    def logout(self):
        """退出登录"""
        # 点击用户头像
        self.click(".user-avatar")
        
        # 点击退出按钮
        self.click("button:has-text('退出登录')")
        
        # 确认退出
        self.click(".el-message-box__btns button:has-text('确定')")
    
    def is_logout_success(self) -> bool:
        """检查是否退出成功"""
        return self.is_visible("input[placeholder='账号']")