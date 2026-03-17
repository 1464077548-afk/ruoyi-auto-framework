from core.base.base_page import BasePage

class LogPage(BasePage):
    """日志管理页面"""
    OPER_LOG_URL = "{base_url}/system/log/operlog"
    LOGIN_LOG_URL = "{base_url}/system/log/logininfor"
    # 页面元素定位器
    SYSTEM_MANAGEMENT_MENU = "text=系统管理"
    OPER_LOG_MENU = "//a[contains(@href, '/operlog') and contains(text(), '操作日志')]"
    LOGIN_LOG_MENU = "//a[contains(@href, '/loginlog') and contains(text(), '登录日志')]"
    LOG_LIST_TITLE = ".card-title"
    #操作日志
    OPER_LOG_SEARCH_INPUT = {"role": "textbox", "name": "请输入操作人员"}   
    SEARCH_BUTTON = {"role": "button", "name": "搜索"}
    OPER_DETAIL_BUTTON = {"role": "button", "name": "详情"}
    
    #登录日志
    LOGIN_LOG_SEARCH_INPUT = {"role": "textbox", "name": "请输入用户名称"}
    
    EXPORT_BUTTON = {"role": "button", "name": "导出"}
    LOG_TABLE = ".el-table"

    #操作日志表格
    LOG_TABLE_ROWS = ".el-table__body tbody tr"
    
    def navigate_to_oper_log_management(self, base_url):
        """导航到操作日志页面"""
        # 首先尝试强制关闭任何可能存在的模态框
        try:
            print("强制关闭现有模态框...")
            # 直接使用 JavaScript 关闭所有模态框
            self.page.evaluate("""
                // 关闭 Element UI 模态框
                const dialogs = document.querySelectorAll('.el-dialog__wrapper');
                dialogs.forEach(dialog => {
                    dialog.style.display = 'none';
                });
                // 关闭 layui 模态框
                const layuiLayers = document.querySelectorAll('.layui-layer');
                layuiLayers.forEach(layer => {
                    layer.style.display = 'none';
                });
                // 关闭 bootstrap 模态框
                const bootstrapModals = document.querySelectorAll('.modal');
                bootstrapModals.forEach(modal => {
                    modal.style.display = 'none';
                });
            """)
            print("成功强制关闭所有模态框")
        except Exception as e:
            print(f"强制关闭模态框失败：{e}")

        # 打印当前 URL
        print(f"当前 URL: {self.page.url}")
        
        # 构建操作日志页面 URL
        operlog_url = self.OPER_LOG_URL.format(base_url=base_url)
        print(f"操作日志页面 URL: {operlog_url}")

        try:
            # 首先尝试直接导航到操作日志页面
            print("尝试直接导航到操作日志页面")
            self.page.goto(operlog_url)
            # 等待页面加载
            self.wait_for_load_state("networkidle")
            print(f"直接导航后 URL: {self.page.url}")
        except Exception as e:
            print(f"直接导航失败：{e}")
            print("尝试通过菜单导航到操作日志页面")
            # 点击系统管理菜单
            if self.is_visible(self.SYSTEM_MANAGEMENT_MENU):
                print("系统管理菜单项可见")
                print("点击系统管理菜单")
                self.click(self.SYSTEM_MANAGEMENT_MENU)
                # 等待菜单展开
                self.page.wait_for_timeout(1000)
                
                # 点击操作日志菜单
                if self.is_visible(self.OPER_LOG_MENU):
                    print("操作日志菜单项可见")
                    print("点击操作日志菜单")
                    self.click(self.OPER_LOG_MENU)
                    # 等待页面加载
                    self.wait_for_load_state("networkidle")
                    print(f"菜单导航后 URL: {self.page.url}")
                else:
                    print("操作日志菜单项不可见，再次尝试直接导航")
                    print(f"直接导航到操作日志页面：{operlog_url}")
                    self.page.goto(operlog_url)
                    # 等待页面加载
                    self.wait_for_load_state("networkidle")
                    print(f"再次直接导航后 URL: {self.page.url}")
            else:
                print("系统管理菜单项不可见，再次尝试直接导航")
                print(f"直接导航到操作日志页面：{operlog_url}")
                self.page.goto(operlog_url)
                # 等待页面加载
                self.wait_for_load_state("networkidle")
                print(f"再次直接导航后 URL: {self.page.url}")

    
    def is_log_list_page_loaded(self, log_type=None):
        """
        检查日志列表页面是否加载完成
        
        Args:
            log_type: 日志类型
            
        Returns:
            bool: 页面是否加载完成
        """
        # 检查 URL 是否包含日志管理路径
        try:
            current_url = self.page.url
            print(f"当前 URL: {current_url}")
            return '/log' in current_url or '/operlog' in current_url or '/loginlog' in current_url
        except:
            return False

    def navigate_to_login_log_management(self, base_url):
        """
        导航到登录日志页面
        
        Returns:
            self: 页面对象
        """
        self.page.goto(self.LOGIN_LOG_URL.format(base_url=base_url))
        self.wait_for_load_state("networkidle")
        print(f"当前 URL: {self.page.url}")



    def search_oper_log(self, keyword):
        """
        搜索操作日志
        
        Args:
            keyword: 搜索关键字
        """
        print(f"开始搜索日志：{keyword}")
        
        self.fill(self.OPER_LOG_SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
    
    def export_oper_log(self):
        """导出操作日志"""
        # 点击导出按钮
        self.click(self.EXPORT_BUTTON)
        self.wait_for_load_state("networkidle")

    def search_login_log(self, keyword):
        """
        搜索登录日志
        
        Args:
            keyword: 搜索关键字
        """
        print(f"开始搜索日志：{keyword}")
        
        self.fill(self.LOGIN_LOG_SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    def export_login_log(self):
        """导出登录日志"""
        # 点击导出按钮
        self.click(self.EXPORT_BUTTON)
        
        # 等待导出操作
        self.wait_for_load_state("networkidle")
        
    def get_log_table_rows(self):
        """获取操作日志表格行"""
        return self._get_locator(self.LOG_TABLE_ROWS).count()
    
    def get_log_rows(self):
        """获取日志表格行（兼容方法）"""
        return self.get_log_table_rows()