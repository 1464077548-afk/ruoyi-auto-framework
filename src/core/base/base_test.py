#!/usr/bin/env python3
"""
基础测试类
"""

import pytest
import logging
import allure
from typing import Optional, Dict, Any
from datetime import datetime

from src.core.utils.logger import TestLogger
from src.core.utils.screenshot_utils import ScreenshotUtils
from src.core.utils.data_loader import DataLoader

class BaseTest:
    """基础测试类"""
    
    def __init__(self):
        """初始化"""
        self.logger = TestLogger().get_logger()
        self.screenshot = ScreenshotUtils()
        self.data_loader = DataLoader()
        self.test_data = {}
    
    @pytest.fixture(autouse=True)
    def setup_test(self, request):
        """测试前置"""
        test_name = request.node.name
        self.logger.info(f"=== 开始执行测试方法 {test_name} ===")
        
        # 加载测试数据
        self.load_test_data()
        
        yield
        
        # 测试后置
        self.teardown_test()
        self.logger.info(f"=== 测试方法 {test_name} 执行完成 ===")
    
    def load_test_data(self):
        """加载测试数据"""
        pass
    
    def teardown_test(self):
        """测试后置"""
        pass
    
    def get_test_data(self, key: str, default: Any = None) -> Any:
        """获取测试数据"""
        return self.test_data.get(key, default)
    
    def assert_equal(self, actual: Any, expected: Any, message: str = ""):
        """断言相等"""
        try:
            assert actual == expected, message
            self.logger.info(f"断言成功: {message}")
        except AssertionError as e:
            self.logger.error(f"断言失败: {message}")
            self.logger.error(f"实际值: {actual}")
            self.logger.error(f"期望值: {expected}")
            raise
    
    def assert_contains(self, actual: str, expected: str, message: str = ""):
        """断言包含"""
        try:
            assert expected in actual, message
            self.logger.info(f"断言成功: {message}")
        except AssertionError as e:
            self.logger.error(f"断言失败: {message}")
            self.logger.error(f"实际值: {actual}")
            self.logger.error(f"期望值: {expected}")
            raise
    
    def assert_true(self, condition: bool, message: str = ""):
        """断言为真"""
        try:
            assert condition, message
            self.logger.info(f"断言成功: {message}")
        except AssertionError as e:
            self.logger.error(f"断言失败: {message}")
            raise
    
    def assert_false(self, condition: bool, message: str = ""):
        """断言为假"""
        try:
            assert not condition, message
            self.logger.info(f"断言成功: {message}")
        except AssertionError as e:
            self.logger.error(f"断言失败: {message}")
            raise
    
    def capture_screenshot(self, name: str = ""):
        """捕获截图"""
        try:
            screenshot_name = name or f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.screenshot.capture(screenshot_name)
            self.logger.info(f"截图已保存: {screenshot_name}")
        except Exception as e:
            self.logger.error(f"截图失败: {str(e)}")
    
    def log_step(self, step: str, details: str = ""):
        """记录测试步骤"""
        self.logger.info(f"步骤: {step}")
        if details:
            self.logger.info(f"详情: {details}")
    
    def log_test_data(self, data: Dict[str, Any]):
        """记录测试数据"""
        self.logger.info("测试数据:")
        for key, value in data.items():
            if key == 'password':
                value = '*****'
            self.logger.info(f"  {key}: {value}")
    
    def handle_exception(self, e: Exception, message: str = ""):
        """处理异常"""
        self.logger.error(f"{message}: {str(e)}")
        self.capture_screenshot(f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        raise