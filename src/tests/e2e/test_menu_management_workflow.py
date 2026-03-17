import pytest
from src.core.base.base_playwright_test import BasePlaywrightTest
from src.core.utils.data_loader import DataLoader
from src.web.pages.login_page import LoginPage
from src.web.pages.menu_page import MenuPage

class TestMenuManagementWorkflow(BasePlaywrightTest):
    """测试菜单管理业务流"""
    
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.integration
    def test_menu_management_workflow(self, page, test_config, env_config, base_url, test_logger):
        """测试完整的菜单管理业务流：登录→创建菜单→编辑菜单→搜索菜单→删除菜单→验证"""
        # 从 YAML 文件加载并处理测试数据
        menu_test_cases = DataLoader.get_test_cases('system', 'menu_data', 'menu_test_cases')
        
        # 使用第一个测试用例（成功案例）
        menu_test_case = menu_test_cases[0]
        
        test_menu_name = menu_test_case.get('menu_name', f"测试菜单_{DataLoader._replace_placeholders('{{random_string(6)}}')}")
        test_menu_name_updated = f"{test_menu_name}_updated"
        test_menu_order = menu_test_case.get('menu_order', "100")
        test_menu_path = menu_test_case.get('menu_path', f"test_{DataLoader._replace_placeholders('{{random_string(6)}}')}")
        test_menu_component = menu_test_case.get('menu_component', f"Test{DataLoader._replace_placeholders('{{random_string(6)}}')}")
        test_menu_permission = menu_test_case.get('menu_permission', f"test:{DataLoader._replace_placeholders('{{random_string(6)}}')}:list")
        
        # 记录测试数据
        test_data = {
            "username": "admin",
            "password": "admin123",
            "test_menu_name": test_menu_name,
            "test_menu_name_updated": test_menu_name_updated,
            "test_menu_path": test_menu_path,
            "test_menu_component": test_menu_component,
            "test_menu_permission": test_menu_permission,
            "test_menu_order": test_menu_order
        }
        self.log_test_data(test_data)
        
        # 创建页面对象
        login_page = LoginPage(self.page, self.base_url)
        menu_page = MenuPage(self.page)
        
        try:
            # 1. 登录系统
            self.log_test_step("1. 打开登录页面")
            login_page.open("login")
            
            self.log_test_step("2. 执行登录操作", f"用户名：{test_data['username']}, 密码：*****")
            login_page.login(test_data["username"], test_data["password"], "1234")
            
            self.log_test_step("3. 验证登录成功")
            self.assert_login_success(login_page)
            
            # 2. 导航到菜单管理页面
            self.log_test_step("4. 导航到菜单管理页面")
            menu_page.navigate_to_menu_management(base_url)
            assert menu_page.is_menu_list_page_loaded(), "菜单管理页面加载失败"
            
            # 3. 创建新菜单
            self.log_test_step("5. 创建新菜单")
            menu_result = menu_page.add_menu(
                menu_name=test_menu_name,
                menu_path=test_menu_path,
                menu_order=test_menu_order,
                menu_component=test_menu_component,
                menu_permission=test_menu_permission,
                menu_icon="el-icon-menu",
                status="0"
            )
            self.log_test_step("6. 验证菜单创建成功", f"结果：{menu_result}")
            assert "成功" in menu_result
            
            # 4. 搜索新创建的菜单
            self.log_test_step("7. 搜索新创建的菜单")
            menu_rows = menu_page.search_menu(test_menu_name)       
            assert menu_rows > 0, "搜索菜单失败"
            
            # 5. 编辑菜单
            self.log_test_step("8. 编辑菜单")
            edit_result = menu_page.edit_menu(
                old_menu_name=test_menu_name,
                new_menu_name=test_menu_name_updated,
            )
            self.log_test_step("9. 验证菜单编辑成功", f"结果：{edit_result}")
            assert "成功" in edit_result
            
            # 6. 搜索编辑后的菜单
            self.log_test_step("10. 搜索编辑后的菜单")
            menu_rows = menu_page.search_menu(test_menu_name_updated)
            
            assert menu_rows > 0, "搜索编辑后的菜单失败"
            
            # 7. 删除菜单
            self.log_test_step("11. 删除菜单")
            delete_result = menu_page.delete_menu(test_menu_name_updated)
            self.log_test_step("12. 验证菜单删除成功", f"结果：{delete_result}")
            assert "成功" in delete_result
            
            # 8. 验证菜单已删除
            self.log_test_step("13. 验证菜单已删除")
            menu_rows =menu_page.search_menu(test_menu_name_updated)
            assert menu_rows == 0, "菜单删除失败"
            
            # 9. 退出登录
            self.log_test_step("14. 执行退出登录")
            login_page.logout()
            
        except Exception as e:
            self.take_screenshot_on_failure("test_menu_management_workflow")
            self.logger.error(f"测试失败：{str(e)}")
            raise
        finally:
            self.clean_cache()