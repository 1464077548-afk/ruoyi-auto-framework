#!/usr/bin/env python3
"""
配置管理工作流测试
"""

import pytest
from playwright.sync_api import Page
from src.web.pages.login_page import LoginPage
from src.web.pages.home_page import HomePage
from src.core.utils.data_loader import DataLoader
from src.core.utils.data_generator import DataGenerator

class TestConfigManagementWorkflow:
    """配置管理工作流测试"""
    
    def setup_method(self):
        """设置"""
        self.data_loader = DataLoader()
        self.data_generator = DataGenerator()
        self.test_data = {
            "username": "admin",
            "password": "admin123",
            "test_config_name": f"测试参数_{self.data_generator.random_string(6)}",
            "test_config_key": f"test_config_{self.data_generator.random_string(8)}",
            "test_config_value": f"test_value_{self.data_generator.random_string(8)}",
            "test_config_value_updated": f"test_value_{self.data_generator.random_string(8)}_updated"
        }
    
    def test_config_management_workflow(self, page: Page, login_page: LoginPage, home_page: HomePage):
        """测试配置管理工作流"""
        # 1. 打开登录页面
        login_page.navigate()
        
        # 2. 执行登录操作
        login_page.login(
            self.test_data["username"],
            self.test_data["password"]
        )
        
        # 3. 验证登录成功
        assert "index" in page.url, "登录失败"
        
        # 4. 导航到配置管理页面
        home_page.navigate_to_config_management()
        
        # 5. 创建新配置
        page.click("button:has-text('新增')")
        page.fill("input[placeholder*='参数名称']", self.test_data["test_config_name"])
        page.fill("input[placeholder*='参数键名']", self.test_data["test_config_key"])
        page.fill("textarea[placeholder*='参数键值']", self.test_data["test_config_value"])
        page.click("label:has-text('否')")  # 非系统内置
        page.click("button:has-text('确 定')")
        
        # 6. 验证配置创建成功
        assert "新增成功" in page.text_content(".el-message__content"), "配置创建失败"
        
        # 7. 搜索新创建的配置
        page.fill("input[placeholder*='参数名称']", self.test_data["test_config_name"])
        page.click("button:has-text('搜索')")
        
        # 8. 编辑配置
        page.click(f".el-table__body tbody tr:has-text('{self.test_data['test_config_value']}') button:has-text('修改')")
        page.fill("textarea[placeholder*='参数键值']", self.test_data["test_config_value_updated"])
        page.click("button:has-text('确 定')")
        
        # 9. 验证配置编辑成功
        assert "修改成功" in page.text_content(".el-message__content"), "配置编辑失败"
        
        # 10. 搜索编辑后的配置
        page.fill("input[placeholder*='参数名称']", self.test_data["test_config_name"])
        page.click("button:has-text('搜索')")
        
        # 11. 删除配置
        page.click(f".el-table__body tbody tr:has-text('{self.test_data['test_config_name']}') button:has-text('删除')")
        page.click(".el-message-box__btns button:has-text('确定')")
        
        # 12. 验证配置删除成功
        assert "删除成功" in page.text_content(".el-message__content"), "配置删除失败"
        
        # 13. 退出登录
        login_page.logout()
        
        # 14. 验证退出成功
        assert "login" in page.url, "退出登录失败"