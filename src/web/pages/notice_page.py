from core.base.base_page import BasePage

class NoticePage(BasePage):
    """通知管理页面"""
    # 通知管理页面 URL
    NOTICE_URL = "{base_url}/system/notice"
    

    #=================新增================#
    ADD_BUTTON = "button:has-text('新增')"
    ADD_NOTICE_DIALOG={"role": "dialog", "name": "添加公告"}
    ADD_NOTICE_TITLE_INPUT = {"role": "dialog", "name": "添加公告","placeholder": "*公告标题"}
    ADD_NOTICE_TYPE_SELECT = {"role": "dialog", "name": "添加公告", "css": ".el-select"}
    ADD_NOTICE_TYPE_OPTION = {"role":"listitem"}
    ADD_NOTICE_CONTENT_INPUT = {"role": "dialog", "name": "添加公告", "css": ".ql-editor[data-placeholder='请输入内容']"}
    ADD_NOTICE_STATUS_RADIO = {"role": "radio", "name": "正常"}
    SAVE_BUTTON = {"role": "button", "name": "确 定"}

    OPER_MESSAGE = {"css": ".el-message__content"}

    #=================搜索================#
    SEARCH_INPUT = {"role": "textbox", "name": "请输入公告标题"}
    SEARCH_BUTTON = {"role": "button", "name": "搜索"}

    #=================表格================#
    SEARCH_TABLE = ".el-table__body tbody tr"

    #=================编辑================#
    EDIT_BUTTON = ".el-table__body tbody tr:has-text('{notice_title}') button:has-text('修改')"
    EDIT_NOTICE_DIALOG={"role": "dialog", "name": "修改公告"}
    EDIT_NOTICE_TITLE_INPUT = {"role": "dialog", "name": "修改公告","placeholder": "公告标题"}
    EDIT_SAVE_BUTTON = {"role": "dialog", "name": "修改公告", "css": "button:has-text('确 定')"}
    #=================删除================#
    DELETE_BUTTON = ".el-table__body tbody tr:has-text('{notice_title}') button:has-text('删除')"
    # 删除确认弹窗
    CONFIRM_DELETE_MODAL = {"role": "dialog", "name": "系统提示"}
    CONFIRM_DELETE_BUTTON =".el-message-box button:has-text('确定')"



    CONFIRM_BUTTON = "button:has-text('确定')"
    
    def __init__(self, page):
        """
        初始化通知管理页面
        
        Args:
            page: Playwright 页面对象
        """
        super().__init__(page)
    
    def navigate_to_notice_management(self, base_url):
        """导航到通知管理页面"""
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
        
        # 导航到通知管理页面
        self.page.goto(self.NOTICE_URL.format(base_url=base_url))
        self.wait_for_load_state("networkidle")
        return self.page.url
    
    def is_notice_list_page_loaded(self):
        """检查通知公告列表页面是否加载完成"""
        # 检查 URL 是否包含通知公告路径
        try:
            current_url = self.page.url
            return '/notice' in current_url or '/system/notice' in current_url
        except:
            return False
    
    def search_notice(self, keyword):
        """搜索通知公告"""
        print(f"开始搜索通知：{keyword}")
        
        # 输入公告标题
        self.fill(self.SEARCH_INPUT, keyword)
        
        # 点击搜索按钮
        self.click(self.SEARCH_BUTTON)
        
        # 等待搜索结果
        self.page.wait_for_timeout(2000)
        
        # 直接获取表格行数
        row_count = self.get_notice_table_rows(self.SEARCH_TABLE)
        
        print(f"搜索完成：{keyword}, 找到 {row_count} 条记录")
  
        return row_count
    
    def add_notice(self, notice_title, notice_content, notice_type, status="正常"):
        """添加通知公告"""
        # 点击新增按钮
        self.click(self.ADD_BUTTON)
        
        # 等待模态框出现
        self.wait_for_selector(self.ADD_NOTICE_DIALOG)
        
        # 填写通知信息
        try:
            # 填写公告标题
            self.fill(self.ADD_NOTICE_TITLE_INPUT, notice_title)
            # 选择公告类型
            print(f"选择公告类型：{notice_type}")
            
            # 先点击选择器输入框来展开下拉列表
            print("点击公告类型选择器...")
            self.click(self.ADD_NOTICE_TYPE_SELECT)
            
            # 等待下拉列表出现
            print("等待下拉列表出现...")
            self.wait_for_load_state("networkidle")
            
            
            # 尝试点击对应的选项
            self._get_locator(self.ADD_NOTICE_TYPE_OPTION).filter(has_text=notice_type).click()
    
            
            # 填写公告内容
            print("填写公告内容...")
            self.fill(self.ADD_NOTICE_CONTENT_INPUT, notice_content)
            
            # 选择状态
            print("选择状态...")
            self.click(self.ADD_NOTICE_STATUS_RADIO)
            
            # 点击保存按钮
            print("点击保存按钮...")
            self.click(self.SAVE_BUTTON)

            #获取操作消息
            if self.wait_for_selector(self.OPER_MESSAGE, timeout=5000):
                message = self.get_text(self.OPER_MESSAGE)
                print(f"获取操作消息：{message}")
                return message
        except Exception as e:
            print(f"填写通知信息失败：{e}")
            return "填写通知信息失败"
        
    
    def edit_notice(self, old_notice_title, new_notice_title):
        """编辑通知公告"""
        # 点击编辑按钮
        self.click(self.EDIT_BUTTON.format(notice_title=old_notice_title))
        
        
        # 等待模态框出现
        self.wait_for_selector(self.EDIT_NOTICE_DIALOG)
        
        # 输入新的公告标题
        self.fill(self.EDIT_NOTICE_TITLE_INPUT, new_notice_title)
        
        # 点击保存按钮
        self.click(self.EDIT_SAVE_BUTTON)
   
        # 等待操作结果
        message = "修改通知公告失败"
        if self.wait_for_selector(self.OPER_MESSAGE):
            message = self.get_text(self.OPER_MESSAGE)
            print(f"获取修改操作消息：{message}")      
        return message
    
    def delete_notice(self, notice_title):
        """删除通知公告"""
        # 点击删除按钮
        self.click(self.DELETE_BUTTON.format(notice_title=notice_title))
        
        # 等待确认弹窗出现
        self.wait_for_selector(self.CONFIRM_DELETE_MODAL)
        
        # 确认删除
        self.click(self.CONFIRM_DELETE_BUTTON)
        
        # 等待操作结果
        message = "删除通知公告失败"
        if self.wait_for_selector(self.OPER_MESSAGE, timeout=5000):
            message = self.get_text(self.OPER_MESSAGE)
        
        return message
    
    def get_notice_table_rows(self, table_selector):
        """获取通知公告表格行"""
        return self.page.locator(table_selector).count()
