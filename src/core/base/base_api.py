#!/usr/bin/env python3
"""
基础API类
"""

import requests
import logging
from typing import Optional, Dict, Any, Tuple
from requests import Response

from src.core.utils.logger import TestLogger
from src.core.utils.data_loader import DataLoader

class BaseAPI:
    """基础API类"""
    
    def __init__(self, base_url: str = "", api_prefix: str = ""):
        """初始化"""
        self.logger = TestLogger().get_logger()
        self.data_loader = DataLoader()
        
        # 加载配置
        config = self.data_loader.load_yaml("config/ruoyi_config.yaml")
        self.base_url = base_url or config.get("ruoyi", {}).get("base_url", "http://localhost:8081")
        self.api_prefix = api_prefix or config.get("ruoyi", {}).get("api", {}).get("prefix", "/prod-api")
        
        # 超时设置
        self.timeout = config.get("ruoyi", {}).get("api", {}).get("timeout", 30)
        
        # 请求头
        self.headers = config.get("ruoyi", {}).get("api", {}).get("headers", {
            "Content-Type": "application/json"
        })
        
        # 会话
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        """GET请求"""
        full_url = self._build_url(url)
        self.logger.info(f"GET请求: {full_url}")
        if params:
            self.logger.info(f"参数: {params}")
        
        try:
            response = self.session.get(full_url, params=params, timeout=self.timeout, **kwargs)
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"GET请求失败: {str(e)}")
            raise
    
    def post(self, url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        """POST请求"""
        full_url = self._build_url(url)
        self.logger.info(f"POST请求: {full_url}")
        if data:
            self.logger.info(f"表单数据: {data}")
        if json:
            self.logger.info(f"JSON数据: {json}")
        
        try:
            response = self.session.post(full_url, data=data, json=json, timeout=self.timeout, **kwargs)
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"POST请求失败: {str(e)}")
            raise
    
    def put(self, url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        """PUT请求"""
        full_url = self._build_url(url)
        self.logger.info(f"PUT请求: {full_url}")
        if data:
            self.logger.info(f"表单数据: {data}")
        if json:
            self.logger.info(f"JSON数据: {json}")
        
        try:
            response = self.session.put(full_url, data=data, json=json, timeout=self.timeout, **kwargs)
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"PUT请求失败: {str(e)}")
            raise
    
    def delete(self, url: str, **kwargs) -> Response:
        """DELETE请求"""
        full_url = self._build_url(url)
        self.logger.info(f"DELETE请求: {full_url}")
        
        try:
            response = self.session.delete(full_url, timeout=self.timeout, **kwargs)
            self._log_response(response)
            return response
        except Exception as e:
            self.logger.error(f"DELETE请求失败: {str(e)}")
            raise
    
    def _build_url(self, url: str) -> str:
        """构建完整URL"""
        if url.startswith("http://") or url.startswith("https://"):
            return url
        
        if url.startswith("/"):
            url = url[1:]
        
        if self.api_prefix and not url.startswith(self.api_prefix[1:]):
            return f"{self.base_url}{self.api_prefix}/{url}"
        
        return f"{self.base_url}/{url}"
    
    def _log_response(self, response: Response):
        """记录响应"""
        self.logger.info(f"响应状态码: {response.status_code}")
        
        try:
            response_json = response.json()
            self.logger.info(f"响应数据: {response_json}")
        except Exception:
            self.logger.info(f"响应内容: {response.text[:500]}...")
    
    def set_token(self, token: str):
        """设置token"""
        self.headers["Authorization"] = f"Bearer {token}"
        self.session.headers.update(self.headers)
        self.logger.info("Token已设置")
    
    def get_token(self) -> Optional[str]:
        """获取token"""
        return self.headers.get("Authorization", "").replace("Bearer ", "")
    
    def assert_status_code(self, response: Response, expected_status: int):
        """断言状态码"""
        assert response.status_code == expected_status, f"状态码错误: 期望 {expected_status}, 实际 {response.status_code}"
        self.logger.info(f"状态码断言成功: {expected_status}")
    
    def assert_json(self, response: Response, expected: Dict[str, Any]):
        """断言JSON响应"""
        try:
            response_json = response.json()
            for key, value in expected.items():
                assert key in response_json, f"响应中缺少键: {key}"
                assert response_json[key] == value, f"值不匹配: {key} 期望 {value}, 实际 {response_json[key]}"
            self.logger.info("JSON响应断言成功")
        except Exception as e:
            self.logger.error(f"JSON响应断言失败: {str(e)}")
            raise
    
    def assert_contains(self, response: Response, expected: str):
        """断言响应包含"""
        assert expected in response.text, f"响应中不包含: {expected}"
        self.logger.info(f"响应包含断言成功: {expected}")
    
    def close(self):
        """关闭会话"""
        self.session.close()
        self.logger.info("会话已关闭")