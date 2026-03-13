#!/usr/bin/env python3
"""
基础页面类
"""

from typing import Optional, Dict, Any, List
from playwright.sync_api import Page, Locator, expect
import logging
import time

from src.core.utils.logger import TestLogger
from src.core.utils.screenshot_utils import ScreenshotUtils

class BasePage:
    """基础页面类"""
    
    def __init__(self, page: Page):
        """初始化"""
        self.page = page
        self.logger = TestLogger().get_logger()
        self.screenshot = ScreenshotUtils(page)
        self.base_url = "http://localhost:8081"
    
    def navigate(self, url: str):
        """导航到指定URL"""
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        self.logger.info(f"导航到: {full_url}")
        self.page.goto(full_url, wait_until="networkidle")
    
    def click(self, locator: str, timeout: int = 30000):
        """点击元素"""
        self.logger.info(f"点击元素: {locator}")
        element = self.page.locator(locator)
        element.click(timeout=timeout)
    
    def fill(self, locator: str, text: str, timeout: int = 30000):
        """填写文本"""
        self.logger.info(f"填写元素: {locator}, 文本: {text}")
        element = self.page.locator(locator)
        element.fill(text, timeout=timeout)
    
    def get_text(self, locator: str, timeout: int = 30000) -> str:
        """获取元素文本"""
        element = self.page.locator(locator)
        text = element.text_content(timeout=timeout)
        self.logger.info(f"获取元素文本: {locator} = {text}")
        return text
    
    def get_value(self, locator: str, timeout: int = 30000) -> str:
        """获取输入框值"""
        element = self.page.locator(locator)
        value = element.input_value(timeout=timeout)
        self.logger.info(f"获取输入框值: {locator} = {value}")
        return value
    
    def is_visible(self, locator: str, timeout: int = 30000) -> bool:
        """检查元素是否可见"""
        try:
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=timeout)
            self.logger.info(f"元素可见: {locator}")
            return True
        except Exception as e:
            self.logger.warning(f"元素不可见: {locator} - {str(e)}")
            return False
    
    def is_hidden(self, locator: str, timeout: int = 30000) -> bool:
        """检查元素是否隐藏"""
        try:
            element = self.page.locator(locator)
            element.wait_for(state="hidden", timeout=timeout)
            self.logger.info(f"元素隐藏: {locator}")
            return True
        except Exception as e:
            self.logger.warning(f"元素未隐藏: {locator} - {str(e)}")
            return False
    
    def wait_for_element(self, locator: str, timeout: int = 30000, state: str = "visible"):
        """等待元素"""
        self.logger.info(f"等待元素: {locator}, 状态: {state}")
        element = self.page.locator(locator)
        element.wait_for(state=state, timeout=timeout)
    
    def wait_for_navigation(self, timeout: int = 30000):
        """等待导航完成"""
        self.logger.info("等待导航完成")
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def take_screenshot(self, name: str = ""):
        """截图"""
        self.screenshot.capture(name)
    
    def switch_to_frame(self, locator: str):
        """切换到iframe"""
        self.logger.info(f"切换到iframe: {locator}")
        frame = self.page.frame_locator(locator)
        return frame
    
    def switch_to_default_content(self):
        """切换到默认内容"""
        self.logger.info("切换到默认内容")
        self.page.frame_locator("body")
    
    def scroll_to(self, locator: str):
        """滚动到元素"""
        self.logger.info(f"滚动到元素: {locator}")
        element = self.page.locator(locator)
        element.scroll_into_view_if_needed()
    
    def hover(self, locator: str):
        """悬停元素"""
        self.logger.info(f"悬停元素: {locator}")
        element = self.page.locator(locator)
        element.hover()
    
    def select_option(self, locator: str, option: str):
        """选择下拉选项"""
        self.logger.info(f"选择下拉选项: {locator}, 选项: {option}")
        element = self.page.locator(locator)
        element.select_option(option)
    
    def check(self, locator: str):
        """勾选复选框"""
        self.logger.info(f"勾选复选框: {locator}")
        element = self.page.locator(locator)
        element.check()
    
    def uncheck(self, locator: str):
        """取消勾选复选框"""
        self.logger.info(f"取消勾选复选框: {locator}")
        element = self.page.locator(locator)
        element.uncheck()
    
    def get_attribute(self, locator: str, attribute: str) -> str:
        """获取元素属性"""
        element = self.page.locator(locator)
        value = element.get_attribute(attribute)
        self.logger.info(f"获取元素属性: {locator}.{attribute} = {value}")
        return value
    
    def press(self, locator: str, key: str):
        """按键"""
        self.logger.info(f"按键: {locator} - {key}")
        element = self.page.locator(locator)
        element.press(key)
    
    def wait(self, seconds: int):
        """等待指定时间"""
        self.logger.info(f"等待 {seconds} 秒")
        time.sleep(seconds)
    
    def get_current_url(self) -> str:
        """获取当前URL"""
        url = self.page.url
        self.logger.info(f"当前URL: {url}")
        return url
    
    def get_page_title(self) -> str:
        """获取页面标题"""
        title = self.page.title()
        self.logger.info(f"页面标题: {title}")
        return title
    
    def refresh(self):
        """刷新页面"""
        self.logger.info("刷新页面")
        self.page.reload()
    
    def close(self):
        """关闭页面"""
        self.logger.info("关闭页面")
        self.page.close()