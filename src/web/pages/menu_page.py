from core.base.base_page import BasePage

class MenuPage(BasePage):
    """菜单管理页面"""
    MENU_URL = "/system/menu"
    # 页面元素定位器
    SYSTEM_MANAGEMENT_MENU = "text=系统管理"
    MENU_MANAGEMENT_MENU = "//a[contains(@href, '/menu') and contains(text(), '菜单管理')]"
    MENU_LIST_TITLE = ".card-title"
    TOOLBAR = "#toolbar"

    #新增菜单
    ADD_MENU_BUTTON = {"role": "button", "name": "新增"}
    MENU_ADD_MODAL = {"role": "dialog", "name": "添加菜单"}
    MENU_NAME_INPUT = {"role": "dialog", "name": "添加菜单","placeholder": "*菜单名称"}
    MENU_PATH_INPUT = {"role": "dialog", "name": "添加菜单","placeholder": "*路由地址"}
    MENU_ORDER_INPUT = {"role": "spinbutton"}
    SAVE_BUTTON = {"role": "dialog", "name": "添加菜单","css":"button:has-text('确 定')"}

    #搜索菜单
    SEARCH_INPUT = {"role": "textbox", "name": "菜单名称"}
    SEARCH_BUTTON = {"role": "button", "name": "搜索"}

    #菜单表格
    MENU_TABLE_ROWS = ".el-table__body tbody tr"
    MENU_NAME_TABLE_ROW = ".el-table__body tbody tr:has-text('{menu_name}')"

    #编辑菜单 
    EDIT_MENU_BUTTON = ".el-table__body tbody tr:has-text('{menu_name}') button:has-text('修改')"
    #编辑菜单弹窗
    EDIT_MENU_MODAL = {"role": "dialog", "name": "修改菜单"}
    EDIT_MENU_NAME_INPUT = {"role": "dialog", "name": "修改菜单","placeholder": "*菜单名称"}
    EDIT_MENU_SAVE_BUTTON = {"role": "dialog", "name": "修改菜单","css":"button:has-text('确 定')"}
    #删除菜单
    DELETE_MENU_BUTTON = ".el-table__body tbody tr:has-text('{menu_name}') button:has-text('删除')"
    #删除菜单弹窗
    DELETE_MENU_MODAL = {"role": "dialog", "name": "系统提示"}
    DELETE_MENU_CONFIRM_BUTTON =".el-message-box button:has-text('确定')"



    SUCCESS_MESSAGE = ".el-message__content"

    
   
    
    
    def __init__(self, page):
        """
        初始化菜单管理页面
        
        Args:
            page: Playwright 页面对象
        """
        super().__init__(page)
    
    def navigate_to_menu_management(self, base_url):
        """
        导航到菜单管理页面
        
        Returns:
            self: 页面对象
        """
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
        
        # 导航到菜单管理页面
        self.page.goto(base_url + self.MENU_URL)
        self.wait_for_load_state("networkidle")
        return self
    
    def is_menu_list_page_loaded(self):
        """
        判断菜单列表页面是否加载完成
        
        Returns:
            bool: 页面是否加载完成
        """
        # 检查 URL 是否包含 menu 或 system/menu
        current_url = self.page.url
        if '/menu' in current_url or '/system/menu' in current_url:
            return True
        
        # 检查页面元素
        try:
            return (self.is_visible(self.MENU_LIST_TITLE) or
                    self.is_visible(self.TOOLBAR) or
                    self.is_visible(self.MENU_TABLE_ROWS))
        except Exception as e:
            print(f"检查页面元素失败：{e}")
            return False
    
    def search_menu(self, keyword):
        """
        搜索菜单
        
        Args:
            keyword: 搜索关键字
            
        Returns:
            int: 匹配的菜单行数
        """
        
        self.fill(self.SEARCH_INPUT, keyword)
        
        self.click(self.SEARCH_BUTTON)
        
        # 等待搜索结果
        self.wait_for_selector(self.MENU_TABLE_ROWS)

        # 获取包含关键字的行
        menu_rows = self.get_menu_rows(self.MENU_NAME_TABLE_ROW.format(menu_name=keyword))
        
        return menu_rows
    
    def add_menu(self, menu_name, menu_path, menu_order, menu_component, menu_permission="", menu_icon="", menu_sort="100", menu_type="M", parent_id="0", status="0"):
        """
        添加菜单
        
        Args:
            menu_name: 菜单名称
            menu_path: 菜单路径
            menu_order: 菜单排序
            menu_component: 组件路径
            menu_permission: 菜单权限
            menu_icon: 菜单图标
            menu_type: 菜单类型
            parent_id: 父菜单 ID
            status: 状态
            
        Returns:
            str: 操作结果信息
        """
        # 点击添加按钮
        self.click_first_element(self.ADD_MENU_BUTTON)
        
        self.wait_for_selector(self.MENU_ADD_MODAL)
        # 填写菜单信息
        try:
            # #1. 选择上级菜单
            # self.fill(self.MENU_ADD_MODAL + " input[name='menuName']", menu_name)

            # #2. 选择菜单类型
            # self.fill(self.MENU_ADD_MODAL + " input[name='menuType']", menu_type)
            # self.fill(self.MENU_ADD_MODAL + " input[name='parentIds']", parent_id)
            #3.填写菜单名称
            self.fill(self.MENU_NAME_INPUT, menu_name)
            #4.填写显示排序
            self.fill(self.MENU_ORDER_INPUT, menu_sort)
            #5.输入路由地址
            self.fill(self.MENU_PATH_INPUT, menu_path)
            #点击确定保存
            self.click(self.SAVE_BUTTON)
            # 等待操作结果
            self.wait_for_selector(self.SUCCESS_MESSAGE)
            message = self.get_text(self.SUCCESS_MESSAGE)
            #等待 alert 移出 dom
            self.wait_for_selector(self.SUCCESS_MESSAGE, state="detach")
    
            return message
        except Exception as e:
            print(f"填写菜单信息失败：{e}")
            return f"操作失败：{str(e)}"
    
    def edit_menu(self, old_menu_name, new_menu_name):
        """
        编辑菜单
        
        Args:
            new_name: 新的菜单名称
            
        Returns:
            str: 操作结果信息
        """
        # 找到第一个菜单的编辑按钮
        edit_buttons = self.click(self.EDIT_MENU_BUTTON.format(menu_name=old_menu_name))
        
        
        # 等待模态框出现
        self.wait_for_selector(self.EDIT_MENU_MODAL)
            
        # 修改菜单名称
        self.fill(self.EDIT_MENU_NAME_INPUT, new_menu_name)
            
        # 点击保存按钮
        self.click(self.EDIT_MENU_SAVE_BUTTON)
            
        # 等待操作结果
        self.wait_for_selector(self.SUCCESS_MESSAGE)
        message = self.get_text(self.SUCCESS_MESSAGE)
        #等待 alert 移出 dom
        self.wait_for_selector(self.SUCCESS_MESSAGE, state="detach")
            
        return message
        
    def delete_menu(self, menu_name):
        """
        删除菜单
        
        Args:
            menu_name: 菜单名称
            
        Returns:
            str: 操作结果信息
        """
        # 找到删除按钮并点击
        try:
            self.click(self.DELETE_MENU_BUTTON.format(menu_name=menu_name))
        
            # 等待确认对话框
            self.wait_for_selector(self.DELETE_MENU_MODAL)
                
            # 点击确认按钮
            self.click(self.DELETE_MENU_CONFIRM_BUTTON)
                
            # 等待操作结果
            self.wait_for_selector(self.SUCCESS_MESSAGE)
            message = self.get_text(self.SUCCESS_MESSAGE)
                
            self.wait_for_selector(self.SUCCESS_MESSAGE, state="detach")
            # 等待表格更新
            self.wait_for_load_state("networkidle")
            return message
        except Exception as e:
            print(f"删除菜单失败：{e}")
            return f"操作失败：{str(e)}"
    
    def get_menu_rows(self, table_selector):
        """
        获取菜单表格行
        
        Returns:
            locator: 菜单行定位器
        """
        return self._get_locator(table_selector).count()