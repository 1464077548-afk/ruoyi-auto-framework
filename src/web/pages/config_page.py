from playwright.sync_api import expect
from core.base.base_page import BasePage
import time

class ConfigPage(BasePage):
    # 页面元素定位器
    ADD_BUTTON = {"role": "button", "name": "新增"}
    SEARCH_INPUT = {"css": "#app","placeholder": "*参数名称"}
    SEARCH_BUTTON = {"css": "#app","role": "button", "name": "搜索"}
    # DIALOG = {"role": "dialog"}
    # DIALOG = {"css": ".el-dialog[aria-label*='添加参数']"}
    INPUT_PARAM_NAME = {"role": "dialog", "css": "input[placeholder*='参数名称']"}
    INPUT_PARAM_KEY = {"role": "dialog", "css": "input[placeholder*='参数键名']"}
    INPUT_PARAM_VALUE = {"role": "dialog", "css": "textarea[placeholder*='参数键值']"}
    INPUT_PARAM_STATUS_DISABLE = {"role": "dialog", "css": "label:has-text('否')"}
    BUTTON_CONFIRM = {"role": "dialog", "css": "button:has-text('确 定')"}
    OPERATION_MESSAGE = {"role": "alert","css": ".el-message__content"}
    CONFIG_TABLE_ROWS = {"css": "table.el-table__body tbody tr"}
    EDIT_BUTTON = ".el-table__body tbody tr:has-text('{config_value}') button:has-text('修改')"
    EDIT_INPUT_PARAM_VALUE = {"role": "dialog", "css": "textarea[placeholder*='参数键值']"}
    EDIT_CONFIRM = {"role": "dialog", "css": "button:has-text('确 定')"}
    DELETE_BUTTON = ".el-table__body tbody tr:has-text('{config_value}') button:has-text('删除')"
    DELETE_CONFIRM = ".el-message-box button:has-text('确定')"


    def __init__(self, page):
        super().__init__(page)
    
    def navigate_to_config_management(self):
        """导航到参数设置页面"""
        # 直接通过 URL 导航到配置管理页面
        self.goto(f"{self.page.url.split('/index')[0]}/system/config")
        # 等待页面加载
        self.wait_for_load_state('networkidle',3000)
    
    def is_config_list_page_loaded(self):
        """检查参数设置页面是否加载完成"""
        # 检查 URL 是否包含配置管理路径
        try:
            print(f"Current URL: {self.page.url}")
            print(f"'config' in URL: {'config' in self.page.url}")
            return "config" in self.page.url
        except Exception as e:
            print(f"Error in is_config_list_page_loaded: {e}")
            return False
    
    def search_config(self, keyword):
        """搜索参数"""
        # 输入搜索关键词
        try:
            self.fill(self.SEARCH_INPUT, keyword)
            print(f"输入搜索关键词：{keyword}")
        except Exception as e:
            print(f"填写搜索关键词时出错：{e}")
        # 点击搜索按钮
        self.click(self.SEARCH_BUTTON)
        print(f"点击搜索按钮:{self.SEARCH_BUTTON}")
    
    def add_config(self, config_name, config_key, config_value, status="否"):
        """添加参数"""
        message ="添加参数失败"
        try:
            # 点击新增按钮
            self.click(self.ADD_BUTTON)
            print("点击新增按钮")
            # 等待模态框弹出
            print("等待模态框弹出")
            self.wait_for_load_state('networkidle',3000)   
            
            self.fill(self.INPUT_PARAM_NAME, config_name) 
            print(f"填写参数名称：{config_name}")      

            #填写参数键名
            self.fill(self.INPUT_PARAM_KEY, config_key)
            print(f"填写参数键名：{config_key}")

            #填写参数键值
            self.fill(self.INPUT_PARAM_VALUE, config_value)
            print(f"填写参数键值：{config_value}")
            
            #选择系统内置状态
            self.click(self.INPUT_PARAM_STATUS_DISABLE)
            print(f"已选择系统内置状态为{self.INPUT_PARAM_STATUS_DISABLE}")
        
            #点击保存按钮
            self.click(self.BUTTON_CONFIRM) 
            print(f"点击保存按钮：{self.BUTTON_CONFIRM}")
                      
            #等待消息出现
            self.wait_for_load_state('networkidle', 3000)
            # 获取消息
            
            # 等待操作消息出现（不指定具体文本）
            if self.wait_for_selector(self.OPERATION_MESSAGE, timeout=5000):
                message = self.get_text(self.OPERATION_MESSAGE)
                # # 获取最新的消息（最后一个）
                # locator = self._get_locator(self.OPERATION_MESSAGE)
                # count = locator.count()
                # if count > 0:
                #     message = locator.nth(count - 1).text_content().strip()
                # else:
                #     message = self.get_text(self.OPERATION_MESSAGE)
                print(f"新增操作消息：{message}")
                # 等待"新增成功"的消息从 DOM 中移除
                self.wait_for_selector(self.OPERATION_MESSAGE, state="detached")
            else:
                message = "未检测到新增操作的消息"
                print("警告：未检测到新增操作的消息")
            #等待消息框关闭
            self.wait_for_load_state('networkidle', 3000)          
        except Exception as e:
            print(f"Error in add_config: {e}")
            # 截图保存
            self.screenshot(path=f"add_config_error_{int(time.time())}.png")
            message = f"添加参数失败：{str(e)}"
        
        return message
    
    def edit_config(self, config_value, new_config_value):
        """编辑参数"""
        self.wait_for_load_state('networkidle', 3000)
        # 点击修改按钮
        edit_selector = self.EDIT_BUTTON.format(config_value=config_value)
        self.click(edit_selector)
        print(f"点击修改按钮：{edit_selector}")
        # 输入新的参数值
        self.fill(self.EDIT_INPUT_PARAM_VALUE, new_config_value)
        print(f"填写新参数键值：{new_config_value}")
        # 点击保存按钮
        edit_button = self._get_locator(self.EDIT_CONFIRM)
        print(f"查找确定按钮数：{edit_button.count()}")
        edit_button.click()
        print(f"点击保存按钮：{self.EDIT_CONFIRM}")
        # 等待消息出现
        self.wait_for_load_state('networkidle', 3000)
        # 获取消息
        message= "编辑参数失败"
        if self.wait_for_selector(self.OPERATION_MESSAGE, timeout=5000):
            message = self.get_text(self.OPERATION_MESSAGE)
            print(f"编辑成功消息：{message}")
            self.wait_for_selector(self.OPERATION_MESSAGE, state="detached")
        else:
            message = "未检测到编辑操作的消息"
            print("警告：未检测到编辑操作的消息")
        return message
    
    def delete_config(self, config_value):
        """删除参数"""
        # 点击删除按钮
        self.wait_for_load_state('networkidle', 3000)
        # 生成完整的删除按钮选择器
        delete_selector = self.DELETE_BUTTON.format(config_value=config_value)
        self.click(delete_selector)
        print(f"点击删除按钮：{delete_selector}")

        # 确认删除
        self.click(self.DELETE_CONFIRM)
        print(f"点击确认删除按钮：{self.DELETE_CONFIRM}")
        # 等待消息出现，增加等待时间
        self.wait_for_load_state('networkidle', 3000)
        # 尝试获取删除消息，使用更具体的选择器
        message = "删除失败"
        
        if self.wait_for_selector(self.OPERATION_MESSAGE, timeout=5000):
            message = self.get_text(self.OPERATION_MESSAGE)
            print(f"删除成功消息：{message}")
            self.wait_for_selector(self.OPERATION_MESSAGE, state="detached")
        else:
            message = "未检测到删除操作的消息"
            print("警告：未检测到删除操作的消息")

        return message
    
    def get_config_table_rows(self):
        """获取参数表格行"""
        return self._get_locator(self.CONFIG_TABLE_ROWS).all()