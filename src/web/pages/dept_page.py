from core.base.base_page import BasePage

class DeptPage(BasePage):
    """部门管理页面"""
    
    # 页面元素定位器
    SYSTEM_MANAGEMENT_MENU = "//a[contains(@href, '/system') and contains(text(), '系统管理')]"
    DEPT_MANAGEMENT_MENU = "//a[contains(@href, '/dept') and contains(text(), '部门管理')]"
    DEPT_LIST_TITLE = ".card-title"
    TOOLBAR = "#toolbar"
    DEPT_TABLE = ".table"
    SEARCH_INPUT = "#app input[placeholder*='部门名称']"
    SEARCH_BUTTON = {"role": "button", "name": "搜索"}
    ADD_DEPT_BUTTON = "button.el-button--primary:has-text('新增')"
    DEPT_ADD_MODAL = {"role": "dialog", "name": "添加部门"}
    DEPT_EDIT_MODAL = {"role": "dialog", "name": "修改部门"}
    DEPT_NAME_INPUT = {"role": "dialog", "placeholder": "*部门名称"}
    DEPT_PARENT_SELECT = {"css": ".vue-treeselect__control"}
    DEPT_PARENT_OPTION = ".vue-treeselect__menu .vue-treeselect__option-arrow-container"
    DEPT_PARENT_OPTION_PARENTS = ".vue-treeselect__option-arrow"
    DEPT_NAME_OPTION = ".vue-treeselect__label:has-text('{parent_name}')"
    
    DEPT_PHONE_INPUT = {"role": "dialog", "placeholder": "*联系电话"}
    DEPT_EMAIL_INPUT = {"role": "dialog", "placeholder": "*邮箱"}
    DEPT_LEADER_INPUT = {"role": "dialog", "placeholder": "*负责人"}
    DEPT_STATUS_RADIOS = {"role": "radio", "name": "正常"}
    ORDER_NUM_INPUT = {"role": "spinbutton"}

    EDIT_BUTTON = ".el-table__body tbody tr:has-text('{old_dept_name}') button:has-text('修改')"
    DELETE_BUTTON = ".el-table__body tbody tr:has-text('{dept_name}') button:has-text('删除')"
    DELETE_CONFIRM = ".el-message-box button:has-text('确定')"
    SAVE_BUTTON = {"role": "dialog", "css": "button:has-text('确 定')"}
    SUCCESS_MESSAGE = ".el-message--success"
    
    def __init__(self, page):
        """
        初始化部门管理页面
        
        Args:
            page: Playwright 页面对象
        """
        super().__init__(page)
    
    def navigate_to_dept_management(self):
        """
        导航到部门管理页面
        
        Returns:
            self: 页面对象
        """
        # 尝试直接导航到部门管理页面
        try:
            dept_url = f"{self.page.url.split('/index')[0]}/system/dept"
            self.page.goto(dept_url)
            print(f"直接导航到部门管理页面：{dept_url}")
        except Exception as e:
            print(f"直接导航到部门管理页面失败：{e}")
            
            # 如果直接导航失败，尝试通过菜单导航
            try:
                # 点击系统管理菜单
                if self.is_visible(self.SYSTEM_MANAGEMENT_MENU):
                    self.click(self.SYSTEM_MANAGEMENT_MENU)
                    # 等待菜单展开
                    self.page.wait_for_timeout(1000)
                
                # 点击部门管理菜单
                if self.is_visible(self.DEPT_MANAGEMENT_MENU):
                    self.click(self.DEPT_MANAGEMENT_MENU)
            except Exception as e:
                print(f"通过菜单导航到部门管理页面失败：{e}")
        
        # 等待页面加载
        self.page.wait_for_timeout(3000)
        # 等待页面加载完成
        try:
            self.page.wait_for_load_state('networkidle', timeout=10000)
        except Exception as e:
            print(f"等待页面加载完成失败：{e}")
        
        return self
    
    def is_dept_list_page_loaded(self):
        """
        判断部门列表页面是否加载完成
        
        Returns:
            bool: 页面是否加载完成
        """
        # 检查 URL 是否包含 dept 或 system/dept
        current_url = self.page.url
        if '/dept' in current_url or '/system/dept' in current_url:
            return True
        
        # 检查页面元素
        try:
            return (self.is_visible(self.DEPT_LIST_TITLE) or
                    self.is_visible(self.TOOLBAR) or
                    self.is_visible(self.DEPT_TABLE))
        except Exception as e:
            print(f"检查页面元素失败：{e}")
            return False
    
    def search_dept(self, keyword):
        """
        搜索部门
        
        Args:
            keyword: 搜索关键字
            
        Returns:
            self: 页面对象
        """
        try:
            # 定位搜索输入框
            if self.is_visible(self.SEARCH_INPUT):
                self.fill(self.SEARCH_INPUT, keyword)
                print(f"填写搜索关键字：{keyword}")
            
            # 点击搜索按钮
            if self.is_visible(self.SEARCH_BUTTON):
                self.click(self.SEARCH_BUTTON)
                print("点击搜索按钮")
            
            # 等待搜索结果
            self.page.wait_for_timeout(2000)
            # 等待表格加载
            self.wait_for_load_state('networkidle', timeout=5000)
            print("等待搜索结果加载完成")
        except Exception as e:
            print(f"搜索部门时出错：{e}")
        
        return self
    
    def add_dept(self, dept_name, order_num="100", leader="", phone="", email="", parent_id="0", status="0", parent_name=""):
        """
        添加部门
        
        Args:
            dept_name: 部门名称
            order_num: 排序
            leader: 负责人
            phone: 联系电话
            email: 邮箱
            parent_id: 父部门 ID
            status: 状态
            parent_name: 父部门名称（可选）
            
        Returns:
            str: 操作结果信息
        """
        # 点击添加按钮
        self.click(self.ADD_DEPT_BUTTON)
        print(f"点击添加按钮：{self.ADD_DEPT_BUTTON}")
        
        # 等待模态框出现
        self.wait_for_selector(self.DEPT_ADD_MODAL)
        
        # 填写部门信息
        self.fill(self.DEPT_NAME_INPUT, dept_name)
        print(f"填写部门名称：{dept_name}")
        self.fill(self.ORDER_NUM_INPUT, order_num)
        print(f"填写排序：{order_num}") 

        if leader:
            self.fill(self.DEPT_LEADER_INPUT, leader)
            print(f"填写负责人：{leader}")
        if phone:
            self.fill(self.DEPT_PHONE_INPUT, phone)
            print(f"填写联系电话：{phone}")
        if email:
            self.fill(self.DEPT_EMAIL_INPUT, email)
            print(f"填写邮箱：{email}")
        
        # 选择父部门
        try:
            # 确保部门选择器可见
            if self.is_visible(self.DEPT_PARENT_SELECT):
                # 点击部门选择器
                self.click(self.DEPT_PARENT_SELECT)
                print(f"点击部门选择器：{self.DEPT_PARENT_SELECT}")
                
                # 获取下拉菜单中的所有选项

                options = self._get_locator(self.DEPT_PARENT_OPTION)
                options_count = options.count()
                print(f"找到 {options_count} 个根部门选项")
                # 遍历展开所有根部门选项
                if options_count > 0:
                    for i in range(options_count):
                        options.nth(i).click()
                        print(f"展开根部门选项 {i+1}: {options.nth(i).text_content()}")
                        dept_name_selector=self.DEPT_NAME_OPTION.format(parent_name=parent_name)
                        if self.is_visible(dept_name_selector):
                            self.click(dept_name_selector)
                            print(f"成功选择部门：{parent_name}")
                            break
                        else:
                            print(f"根目录下未找到部门：{parent_name}，尝试展开根目录下的子目录，并查找部门")
                            #检查根节点下是否还有父部门箭头
                            parents = self._get_locator(self.DEPT_PARENT_OPTION_PARENTS)
                            if parents.count() > 0:
                                print(f"找到 {parents.count()} 个父部门箭头")
                                # 遍历展开所有父部门选项
                                for j in range(parents.count()):
                                    parent = parents.nth(j)
                                    parent.click(force=True)
                                    print(f"点击子目录：{j},{parent.text_content()}")
                                    if self.is_visible(self.DEPT_NAME_OPTION.format(parent_name=parent_name)):
                                        self.click(self.DEPT_NAME_OPTION.format(parent_name=parent_name))
                                        print(f"成功选择部门：{parent_name}")
                                        break
                                    else:
                                        print(f"子目录下未找到部门：{parent_name}")
                            else:
                                print(f"根目录无子目录，也未找到部门：{parent_name}")
            
            else:
                print("父部门选择器不可见，跳过选择")
        except Exception as e:
            print(f"选择父部门时出错：{e}")
            # 如果选择父部门失败，继续执行其他操作
        
        # 选择状态
        self.click(self.DEPT_STATUS_RADIOS)
        print(f"选择状态：{status}")
        
        # 点击保存按钮
        self.click(self.SAVE_BUTTON)
        print(f"点击保存按钮：{self.SAVE_BUTTON}")
        
        # 等待操作结果
        if self.wait_for_selector(self.SUCCESS_MESSAGE):
            message = self.get_text(self.SUCCESS_MESSAGE)
            print(f"添加成功消息：{message}")
            #等待 alert 从 DOM 移除
            self.wait_for_selector(self.SUCCESS_MESSAGE, state="detached")
        else:
            message = "未检测到添加成功消息"
            print(f"警告：未检测到添加成功消息：{message}")
        
        return message
    
    def edit_dept(self, old_dept_name,  new_name=""):
        """
        编辑部门
        
        Args:
            old_dept_name: 旧的部门名称
            new_name: 新的部门名称
            
        Returns:
            str: 操作结果信息
        """
        # 找到第一个部门的编辑按钮
        edit_selector = self.EDIT_BUTTON.format(old_dept_name=old_dept_name)
        self.click(edit_selector)
        print(f"点击编辑按钮：{edit_selector}")
            
        # 等待模态框出现
        self.wait_for_selector(self.DEPT_EDIT_MODAL)
            
        # 修改部门信息
        if new_name:
            self.fill(self.DEPT_NAME_INPUT, new_name)
            print(f"填写新部门名称：{new_name}")
            
            # 点击保存按钮
            self.click(self.SAVE_BUTTON)
            print(f"点击保存按钮：{self.SAVE_BUTTON}")
            
            # 等待操作结果
            if self.wait_for_selector(self.SUCCESS_MESSAGE):
                message = self.get_text(self.SUCCESS_MESSAGE)
                print(f"编辑成功消息：{message}")
                #等待 alert 从 DOM 移除
                self.wait_for_selector(self.SUCCESS_MESSAGE, state="detached")
            else:
                message = "未检测到编辑成功消息"
                print(f"警告：未检测到编辑成功消息：{message}")
            
            return message
        
        return None
    
    def delete_dept(self, dept_name):
        """
        删除部门
        
        Args:
            dept_name: 部门名称
            
        Returns:
            str: 操作结果信息
        """
        # 搜索部门
        self.search_dept(dept_name)
        
        # 找到删除按钮并点击
        delete_selector = self.DELETE_BUTTON.format(dept_name=dept_name)