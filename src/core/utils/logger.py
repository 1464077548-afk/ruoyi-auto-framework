#!/usr/bin/env python3
"""
日志工具
"""

import logging
import os
from datetime import datetime

class TestLogger:
    """测试日志类"""
    
    def __init__(self):
        """初始化"""
        self.log_dir = "logs"
        self._ensure_log_dir()
        self.log_file = os.path.join(self.log_dir, f"ruoyi_test.log")
    
    def _ensure_log_dir(self):
        """确保日志目录存在"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def get_logger(self, name: str = "test_logger") -> logging.Logger:
        """获取日志器"""
        logger = logging.getLogger(name)
        
        # 避免重复添加处理器
        if not logger.handlers:
            # 设置日志级别
            logger.setLevel(logging.INFO)
            
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # 文件处理器
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(logging.INFO)
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def get_error_logger(self, name: str = "error_logger") -> logging.Logger:
        """获取错误日志器"""
        logger = logging.getLogger(name)
        
        if not logger.handlers:
            logger.setLevel(logging.ERROR)
            
            # 错误日志文件
            error_log_file = os.path.join(self.log_dir, f"error_{datetime.now().strftime('%Y%m%d')}.log")
            
            file_handler = logging.FileHandler(error_log_file, encoding='utf-8')
            file_handler.setLevel(logging.ERROR)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def clear_old_logs(self, days: int = 7):
        """清理旧日志"""
        import time
        current_time = time.time()
        
        for file in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, file)
            if os.path.isfile(file_path):
                file_time = os.path.getmtime(file_path)
                if (current_time - file_time) > (days * 24 * 3600):
                    os.remove(file_path)
                    print(f"已删除旧日志: {file}")

# 全局日志实例
test_logger = TestLogger().get_logger()
error_logger = TestLogger().get_error_logger()