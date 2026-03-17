import pytest
from src.core.base.base_playwright_test import BasePlaywrightTest
from src.web.pages.login_page import LoginPage
from src.web.pages.log_page import LogPage

class TestLogManagementWorkflow(BasePlaywrightTest):
    """测试日志管理业务流"""
    
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.integration
    def test_log_management_workflow(self, page, test_config, env_config, base_url, test_logger):
        """测试完整的日志管理业务流：登录→访问操作日志→搜索操作日志→导出操作日志→访问登录日志→搜索登录日志→导出登录日志"""
        # 记录测试数据
        test_data = {
            "username": "admin",
            "password": "admin123",
            "search_keyword": "admin"
        }
        self.log_test_data(test_data)
        
        # 创建页面对象
        login_page = LoginPage(self.page, self.base_url)
        log_page = LogPage(self.page)
        
        try:
            # 1. 登录系统
            self.log_test_step("1. 打开登录页面")
            login_page.open("login")
            
            self.log_test_step("2. 执行登录操作", f"用户名：{test_data['username']}, 密码：*****")
            login_page.login(test_data["username"], test_data["password"], "1234")
            
            self.log_test_step("3. 验证登录成功")
            self.assert_login_success(login_page)
            
            # 2. 导航到操作日志页面
            self.log_test_step("4. 导航到操作日志页面")
            log_page.navigate_to_oper_log_management(base_url)
            assert log_page.is_log_list_page_loaded("oper"), "操作日志页面加载失败"
            
            # 3. 搜索操作日志
            self.log_test_step("5. 搜索操作日志")
            log_page.search_oper_log(test_data["search_keyword"])
            log_rows = log_page.get_log_table_rows()
            assert log_rows > 0, "搜索结果为空"
            self.log_test_step("验证搜索结果", f"找到 {log_rows} 条操作日志")
            
            
            # 4. 导出操作日志
            self.log_test_step("7. 导出操作日志")
            log_page.export_oper_log()
            self.log_test_step("8. 验证操作日志导出成功")
            #TODO: 验证导出文件是否存在且正确
            
            # 5. 导航到登录日志页面
            self.log_test_step("9. 导航到登录日志页面")
            log_page.navigate_to_login_log_management(base_url)
            assert log_page.is_log_list_page_loaded("login"), "登录日志页面加载失败"
            
            # 6. 搜索登录日志
            self.log_test_step("10. 搜索登录日志")
            log_page.search_login_log(test_data["search_keyword"])
            log_rows = log_page.get_log_table_rows()
            assert log_rows > 0, "搜索结果为空"
            self.log_test_step("11. 验证搜索结果", f"找到 {log_rows} 条登录日志")
            
            # 7. 导出登录日志
            self.log_test_step("12. 导出登录日志")
            log_page.export_login_log()
            self.log_test_step("13. 验证登录日志导出成功")
            #TODO: 验证导出文件是否存在且正确
            
            # 8. 退出登录
            self.log_test_step("14. 执行退出登录")
            login_page.logout()
            
        except Exception as e:
            self.take_screenshot_on_failure("test_log_management_workflow")
            self.logger.error(f"测试失败：{str(e)}")
            raise
        finally:
            self.clean_cache()