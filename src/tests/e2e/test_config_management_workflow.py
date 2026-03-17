import pytest
from src.core.base.base_playwright_test import BasePlaywrightTest
from src.core.utils.data_loader import DataLoader
from src.web.pages.login_page import LoginPage
from src.web.pages.config_page import ConfigPage

class TestConfigManagementWorkflow(BasePlaywrightTest):
    """测试配置管理业务流"""
    
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.integration
    def test_config_management_workflow(self, page, test_config, env_config, base_url, test_logger):
        """测试完整的配置管理业务流：登录→创建配置→搜索配置→编辑配置→删除配置→验证"""
        # 从 YAML 文件加载并处理测试数据
        config_test_cases = DataLoader.get_test_cases('config', 'config_data', 'config_test_cases')
        
        # 使用第一个测试用例（成功案例）
        config_test_case = config_test_cases[0]
        
        test_config_name = config_test_case.get('config_name', f"测试配置_{DataLoader._replace_placeholders('{{random_string(6)}}')}")
        test_config_key = config_test_case.get('config_key', f"test_config_{DataLoader._replace_placeholders('{{random_string(6)}}')}")
        test_config_value = config_test_case.get('config_value', f"test_value_{DataLoader._replace_placeholders('{{random_string(6)}}')}")
        test_config_value_updated = f"{test_config_value}_updated"
        
        # 记录测试数据
        test_data = {
            "username": "admin",
            "password": "admin123",
            "test_config_name": test_config_name,
            "test_config_key": test_config_key,
            "test_config_value": test_config_value,
            "test_config_value_updated": test_config_value_updated
        }
        self.log_test_data(test_data)
        
        # 创建页面对象
        login_page = LoginPage(page, base_url)
        config_page = ConfigPage(page)
        
        try:
            # 1. 登录系统
            self.log_test_step("1. 打开登录页面")
            login_page.open("login")
            
            self.log_test_step("2. 执行登录操作", f"用户名：{test_data['username']}, 密码：*****")
            login_page.login(test_data["username"], test_data["password"], "1234")
            
            self.log_test_step("3. 验证登录成功")
            self.assert_login_success(login_page)
            
            # 2. 导航到配置管理页面
            self.log_test_step("4. 导航到配置管理页面")
            config_page.navigate_to_config_management()
            assert config_page.is_config_list_page_loaded(), "配置管理页面加载失败"
            
            # 3. 创建新配置
            self.log_test_step("5. 创建新配置")
            add_message = config_page.add_config(
                config_name=test_config_name,
                config_key=test_config_key,
                config_value=test_config_value,
                status="否"
            )
            self.log_test_step("6. 验证配置创建成功")
            assert "成功" in add_message, f"添加配置失败：{add_message}"

            
            # 4. 搜索新创建的配置
            self.log_test_step("7. 搜索新创建的配置")
            config_page.search_config(test_config_name)
            config_rows = config_page.get_config_table_rows()
            assert len(config_rows) > 0, "搜索配置失败"

            
            # 5. 编辑配置
            self.log_test_step("8. 编辑配置")
            modify_message = config_page.edit_config(test_config_value, test_config_value_updated)
            self.log_test_step("9. 验证配置编辑成功")
            assert "成功" in modify_message, f"编辑配置失败：{modify_message}"
            
            # 6. 搜索编辑后的配置
            self.log_test_step("10. 搜索编辑后的配置")
            config_page.search_config(test_config_name)
            config_rows = config_page.get_config_table_rows()
            assert len(config_rows) > 0, "搜索编辑后的配置失败"
            
            # 7. 删除配置
            self.log_test_step("11. 删除配置")
            message = config_page.delete_config(test_config_name)
            self.log_test_step("12. 验证配置删除成功")
            assert "成功" in message, "删除配置失败"
            
            # 8. 验证配置已删除
            self.log_test_step("13. 验证配置已删除")
            config_page.search_config(test_config_name)
            config_rows = config_page.get_config_table_rows()
            assert len(config_rows) == 0, "配置删除失败"
            
            # 9. 退出登录
            self.log_test_step("14. 执行退出登录")
            login_page.logout()
            
        except Exception as e:
            self.take_screenshot_on_failure("test_config_management_workflow")
            test_logger.error(f"测试失败：{str(e)}")
            raise
        finally:
            self.clean_cache()