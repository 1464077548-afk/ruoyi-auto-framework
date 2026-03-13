#!/usr/bin/env python3
"""
用户角色管理工作流测试
"""

import pytest
from playwright.sync_api import Page
from src.web.pages.login_page import LoginPage
from src.web.pages.home_page import HomePage
from src.core.utils.data_loader import DataLoader
from src.core.utils.data_generator import DataGenerator

class TestUserRoleWorkflow:
    """用户角色管理工作流测试"""
    
    def setup_method(self):
        """设置"""
        self.data_loader = DataLoader()
        self.data_generator = DataGenerator()
        self.test_data = {
            "username": "admin",
            "password": "admin123",
            "test_role_name": f"测试角色_{self.data_generator.random_string(6)}",
            "test_role_name_updated": f"测试角色_{self.data_generator.random_string(6)}_updated",
            "test_user_name": f"测试用户_{self.data_generator.random_string(6)}",
            "test_user_password": "123456",
            "test_user_realname": f"测试用户_{self.data_generator.random_string(4)}"
        }
    
    def test_user_role_workflow(self, page: Page, login_page: LoginPage, home_page: HomePage):
        """测试用户角色管理工作流"""
        # 1. 打开登录页面
        login_page.navigate()
        
        # 2. 执行登录操作
        login_page.login(
            self.test_data["username"],
            self.test_data["password"]
        )
        
        # 3. 验证登录成功
        assert "index" in page.url, "登录失败"
        
        # 4. 导航到角色管理页面
        home_page.navigate_to_role_management()
        
        # 5. 创建新角色
        page.click("button:has-text('新增')")
        page.fill("input[placeholder*='角色名称']", self.test_data["test_role_name"])
        page.fill("input[placeholder*='角色权限字符串']", f"role_{self.data_generator.random_string(8)}")
        page.click("button:has-text('确 定')")
        
        # 6. 验证角色创建成功
        assert "新增成功" in page.text_content(".el-message__content"), "角色创建失败"
        
        # 7. 搜索新创建的角色
        page.fill("input[placeholder*='角色名称']", self.test_data["test_role_name"])
        page.click("button:has-text('搜索')")
        
        # 8. 编辑角色
        page.click(f".el-table__body tbody tr:has-text('{self.test_data['test_role_name']}') button:has-text('修改')")
        page.fill("input[placeholder*='角色名称']", self.test_data["test_role_name_updated"])
        page.click("button:has-text('确 定')")
        
        # 9. 验证角色编辑成功
        assert "修改成功" in page.text_content(".el-message__content"), "角色编辑失败"
        
        # 10. 导航到用户管理页面
        home_page.navigate_to_user_management()
        
        # 11. 创建新用户
        page.click("button:has-text('新增')")
        page.fill("input[placeholder*='用户名']", self.test_data["test_user_name"])
        page.fill("input[placeholder*='密码']", self.test_data["test_user_password"])
        page.fill("input[placeholder*='用户姓名']", self.test_data["test_user_realname"])
        
        # 选择角色
        page.click("input[placeholder*='选择角色']")
        page.click(f"li:has-text('{self.test_data['test_role_name_updated']}')")
        
        page.click("button:has-text('确 定')")
        
        # 12. 验证用户创建成功
        assert "新增成功" in page.text_content(".el-message__content"), "用户创建失败"
        
        # 13. 搜索新创建的用户
        page.fill("input[placeholder*='用户名']", self.test_data["test_user_name"])
        page.click("button:has-text('搜索')")
        
        # 14. 删除用户
        page.click(f".el-table__body tbody tr:has-text('{self.test_data['test_user_name']}') button:has-text('删除')")
        page.click(".el-message-box__btns button:has-text('确定')")
        
        # 15. 验证用户删除成功
        assert "删除成功" in page.text_content(".el-message__content"), "用户删除失败"
        
        # 16. 导航回角色管理页面
        home_page.navigate_to_role_management()
        
        # 17. 删除角色
        page.fill("input[placeholder*='角色名称']", self.test_data["test_role_name_updated"])
        page.click("button:has-text('搜索')")
        page.click(f".el-table__body tbody tr:has-text('{self.test_data['test_role_name_updated']}') button:has-text('删除')")
        page.click(".el-message-box__btns button:has-text('确定')")
        
        # 18. 验证角色删除成功
        assert "删除成功" in page.text_content(".el-message__content"), "角色删除失败"
        
        # 19. 退出登录
        login_page.logout()
        
        # 20. 验证退出成功
        assert "login" in page.url, "退出登录失败"