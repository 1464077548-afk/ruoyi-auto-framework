from core.base.base_page import BasePage

class DictPage(BasePage):
    """字典管理页面"""
    
    # 页面元素定位器
    SYSTEM_MANAGEMENT_MENU = {"role":"menubar","name":"系统管理"}
    DICT_MANAGEMENT_MENU = {"role":"menuitem","name":"字典管理"}
    DICT_LIST_TITLE = {"role":"heading","name":"字典列表"}
    TOOLBAR = {"role":"toolbar"}
    DICT_TABLE = {"role":"table"}
       # 页面元素定位器
    ADD_BUTTON = {"css": "#app button:has-text('新增')"}
    SEARCH_INPUT = {"css": "#app","placeholder": "*字典类型"}
    DICT_NAME_INPUT = {"css": "#app","placeholder": "*字典名称"}
    SEARCH_BUTTON = {"css": "#app","role": "button", "name": "搜索"}
    # DIALOG = {"role": "dialog"}
    DIALOG = {"role": "dialog", "name": "添加字典类型"}
    INPUT_DICT_NAME = {"role": "dialog", "css": "input[placeholder*='字典名称']"}
    INPUT_DICT_KEY = {"role": "dialog", "css": "input[placeholder*='字典类型']"}
    INPUT_DICT_STATUS = {"role": "dialog", "css": "label:has-text('正常')"}
    BUTTON_CONFIRM = {"css": ".el-dialog[aria-label*='添加字典类型'] button:has-text('确 定')"}

    DICT_DATA_DIALOG = {"role": "dialog", "name": "添加字典数据"}
    INPUT_DICT_DATA_LABEL = {"css": ".el-dialog[aria-label*='添加字典数据'] input[placeholder*='数据标签']"}
    INPUT_DICT_DATA_VALUE = {"css": ".el-dialog[aria-label*='添加字典数据'] input[placeholder*='数据键值']"}
    INPUT_DICT_DATA_SORT = {"css": ".el-dialog[aria-label*='添加字典数据'] .el-input-number--medium"}
    DICT_DATA_CONFIRM = {"css": ".el-dialog[aria-label*='添加字典数据'] button:has-text('确 定')"}
    OPERATION_MESSAGE = {"css": ".el-message__content"}
    DICT_TABLE_ROWS = {"css": ".el-table__body tbody tr"}
    ENTER_DICT_DATA_BUTTON = ".el-table__body tbody tr:has-text('{dict_type}') a:has-text('{dict_type}')"
    EDIT_BUTTON = ".el-table__body tbody tr:has-text('{dict_type}') button:has-text('修改')"
    DICT_DATA_EDIT_DIALOG = {"role": "dialog", "name": "修改字典数据"}
    SEARCH_DICT_DATA_LABEL = {"role": "textbox", "name": "请输入字典标签"}
    EDIT_DICT_DATA_LABEL = {"css": ".el-dialog[aria-label*='修改字典数据'] input[placeholder*='数据标签']"}
    EDIT_DICT_DATA_VALUE = {"css": ".el-dialog[aria-label*='修改字典数据'] input[placeholder*='数据键值']"}
    EDIT_DICT_DATA_SORT = {"css": ".el-dialog[aria-label*='修改字典数据'] .el-input-number--medium"}
    EDIT_INPUT_VALUE = {"role": "dialog", "css": "textarea[placeholder*='数据键值']"}
    EDIT_DICT_DATA_CONFIRM = {"css": ".el-dialog[aria-label*='修改字典数据'] button:has-text('确 定')"}
    DELETE_BUTTON = ".el-table__body tbody tr:has-text('{dict_type}') button:has-text('删除')"
    DELETE_CONFIRM = ".el-message-box button:has-text('确定')"

    
    def __init__(self, page):
        """
        初始化字典管理页面
        
        Args:
            page: Playwright 页面对象
        """
        super().__init__(page)
    
    def navigate_to_dict_management(self, base_url):
        """导航到字典管理页面"""
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
        
        # 直接导航到字典管理页面
        try:
            dict_url =base_url + '/system/dict'
            # 确保 URL 格式正确
            if '//system/dict' in dict_url:
                dict_url = dict_url.replace('//system/dict', '/system/dict')
            
            print(f"直接导航到字典管理页面：{dict_url}")
            self.page.goto(dict_url)
            # 等待页面加载
            self.page.wait_for_load_state('networkidle', timeout=10000)
            print("成功导航到字典管理页面")
        except Exception as e:
            print(f"直接导航到字典管理页面失败：{e}")
            
            # 如果直接导航失败，尝试通过菜单导航
            try:
                # 点击系统管理菜单
                if self.is_visible(self.SYSTEM_MANAGEMENT_MENU):
                    self.click(self.SYSTEM_MANAGEMENT_MENU)
                    # 等待菜单展开
                    self.page.wait_for_timeout(1000)
                
                # 尝试使用多种定位器点击字典管理菜单
                dict_selectors = [
                    self.DICT_MANAGEMENT_MENU,
                    "a:has-text('字典管理')",
                    "li:has-text('字典管理')",
                    "[href*='/dict']"
                ]
                
                clicked = False
                for selector in dict_selectors:
                    try:
                        if self.is_visible(selector):
                            self.click(selector)
                            clicked = True
                            print(f"成功点击字典管理菜单：{selector}")
                            break
                    except Exception as e:
                        print(f"尝试点击字典管理菜单 {selector} 失败：{e}")
            except Exception as e:
                print(f"通过菜单导航到字典管理页面失败：{e}")
        
        # 等待页面加载
        self.page.wait_for_timeout(3000)
        # 等待 URL 包含 dict
        try:
            self.page.wait_for_url("**/dict", timeout=10000)
        except Exception as e:
            print(f"等待字典管理页面 URL 失败：{e}")
    
    def is_dict_list_page_loaded(self):
        """检查字典列表页面是否加载完成"""
        # 检查 URL 是否包含 dict 或 system/dict
        try:
            current_url = self.page.url
            return '/dict' in current_url or '/system/dict' in current_url
        except Exception as e:
            print(f"检查 URL 失败：{e}")
            # 检查页面元素
            try:
                return (self.is_visible(self.DICT_LIST_TITLE) or
                        self.is_visible(self.TOOLBAR) or
                        self.is_visible(self.DICT_TABLE))
            except Exception as e:
                print(f"检查页面元素失败：{e}")
                return False
    
    def search_dict(self, locator, keyword):
        """搜索字典"""
        if self.is_visible(locator):
            print(f"使用选择器 {locator} 填写搜索关键字")
            self.fill(locator, keyword)
        #点击搜索
        self.click(self.SEARCH_BUTTON)
        print(f"使用选择器 {self.SEARCH_BUTTON} 点击搜索按钮")

        # 等待搜索结果
        self.wait_for_load_state('networkidle', timeout=10000)
        print(f"搜索完成：{keyword}")

    def search_dict_data(self, keyword):
        """搜索字典数据"""
        self.search_dict(self.SEARCH_DICT_DATA_LABEL, keyword)
        # 等待搜索结果
        self.wait_for_selector(self.DICT_TABLE_ROWS, timeout=10000)
        dict_rows = self.get_data_rows(self.DICT_TABLE_ROWS)
        print(f"搜索字典数据结果：{dict_rows} 条")
        return dict_rows
        
    def add_dict_type(self, dict_type, dict_name):
        """添加字典类型"""
        # 点击新增按钮
        try:
            self.click(self.ADD_BUTTON)
            print(f"成功点击新增按钮{self.ADD_BUTTON}")
        
            # 等待模态框出现
            
            self.wait_for_selector(self.DIALOG, timeout=10000)

            
            # 输入字典信息    
            self.fill(self.INPUT_DICT_NAME, dict_name)
            self.fill(self.INPUT_DICT_KEY, dict_type)
            self.click(self.INPUT_DICT_STATUS)
            
            # 点击保存按钮
            self.click(self.BUTTON_CONFIRM)
            print(f"成功点击确认按钮，新增字典类型：{dict_type} - {dict_name}")
        
        
            # 等待操作结果
            if self.wait_for_selector(self.OPERATION_MESSAGE, timeout=10000):
                message = self.get_text(self.OPERATION_MESSAGE)
                print(f"获取操作结果：{message}")
                #等待 alert 从 dom 移除
                self.wait_for_selector(self.OPERATION_MESSAGE, state="detached")
                return message
        except Exception as e:
            print(f"获取操作结果失败：{e}")
            return "添加字典类型失败"
    
    def add_dict_data(self, dict_value, dict_label, dict_sort="100", status="0"):
        """添加字典数据"""
        # 点击新增按钮

        try:
            self.click(self.ADD_BUTTON)            
        # 等待模态框出现
            self.wait_for_selector(self.DICT_DATA_DIALOG, timeout=10000)
        # 输入字典数据信息
        
            self.fill(self.INPUT_DICT_DATA_LABEL, dict_label)
            print(f"填写数据标签：{dict_label}")
            self.fill(self.INPUT_DICT_DATA_VALUE, dict_value)
            print(f"填写数据键值：{dict_value}")
            # self.fill(self.INPUT_DICT_DATA_SORT, dict_sort)
            
            # 选择状态
            
            # 点击保存按钮
            self.click(self.DICT_DATA_CONFIRM)
            print(f"点击确认按钮，新增字典数据：dict_label：{dict_label} - dict_value：{dict_value}")

            # 等待操作结果
            if self.wait_for_selector(self.OPERATION_MESSAGE, timeout=10000):
                message = self.get_text(self.OPERATION_MESSAGE)
                print(f"获取操作结果：{message}")
                #等待 alert 从 dom 移除
                self.wait_for_selector(self.OPERATION_MESSAGE, state="detached")
                return message
        except Exception as e:
            print(f"获取操作结果失败：{e}")
            return "添加字典数据失败"
        return "添加字典数据失败"
    
    def enter_dict_data_management(self, dict_type):
        """进入字典数据管理"""
        try:
            # 搜索字典类型
            self.search_dict(self.SEARCH_INPUT, dict_type)
            
            # 点击字典数据按钮
            self.click(self.ENTER_DICT_DATA_BUTTON.format(dict_type=dict_type))
            print(f"点击字典类型按钮：{dict_type}")
            # 等待字典数据页面加载
            self.page.wait_for_timeout(2000)
        except Exception as e:
            print(f"进入字典数据管理失败：{e}")
    
    def edit_dict_data(self, old_dict_label, new_dict_label):
        """修改字典数据"""
        try:
            # 搜索字典数据
            self.search_dict(self.SEARCH_DICT_DATA_LABEL, old_dict_label)
            
            # 点击修改按钮
            self.click(self.EDIT_BUTTON.format(dict_type=old_dict_label))
            
            # 等待模态框出现
            self.wait_for_selector(self.DICT_DATA_EDIT_DIALOG, timeout=10000)
                
            # 修改字典数据信息
            self.fill(self.EDIT_DICT_DATA_LABEL, new_dict_label)
                
            # 点击保存按钮
            self.click(self.EDIT_DICT_DATA_CONFIRM)
                         
            # 等待操作结果
            if self.wait_for_selector(self.OPERATION_MESSAGE, timeout=10000):
                message = self.get_text(self.OPERATION_MESSAGE)
                print(f"获取操作结果：{message}")
                #等待 alert 从 dom 移除
                self.wait_for_selector(self.OPERATION_MESSAGE, state="detached")
                return message
        except Exception as e:
            print(f"修改字典数据失败：{e}")
            return "修改字典数据失败"
        return "修改字典数据失败"
    
    
    def delete_dict_data(self, dict_label):
        """删除字典数据"""
        try:
            # 搜索字典数据
            self.search_dict(self.SEARCH_DICT_DATA_LABEL, dict_label)         
            # 点击删除按钮
            self.click(self.DELETE_BUTTON.format(dict_type=dict_label))

                
            # 等待确认对话框
            self.wait_for_selector(self.DELETE_CONFIRM)       
            # 点击确认按钮
            self.click(self.DELETE_CONFIRM)
                
            # 等待操作结果
            if self.wait_for_selector(self.OPERATION_MESSAGE, timeout=10000):
                message = self.get_text(self.OPERATION_MESSAGE)
                print(f"获取操作结果：{message}")