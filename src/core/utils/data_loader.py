#!/usr/bin/env python3
"""
数据加载工具
"""

import yaml
import csv
import os
from typing import Dict, List, Any

class DataLoader:
    """数据加载类"""
    
    def __init__(self):
        """初始化"""
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    def load_yaml(self, file_path: str) -> Dict[str, Any]:
        """加载YAML文件"""
        full_path = self._get_full_path(file_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return data or {}
        except Exception as e:
            print(f"加载YAML文件失败: {full_path} - {str(e)}")
            return {}
    
    def load_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """加载CSV文件"""
        full_path = self._get_full_path(file_path)
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            return data
        except Exception as e:
            print(f"加载CSV文件失败: {full_path} - {str(e)}")
            return []
    
    def save_yaml(self, file_path: str, data: Dict[str, Any]):
        """保存YAML文件"""
        full_path = self._get_full_path(file_path)
        
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            print(f"YAML文件已保存: {full_path}")
        except Exception as e:
            print(f"保存YAML文件失败: {full_path} - {str(e)}")
    
    def save_csv(self, file_path: str, data: List[Dict[str, Any]]):
        """保存CSV文件"""
        full_path = self._get_full_path(file_path)
        
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            if data:
                fieldnames = data[0].keys()
                with open(full_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(data)
                print(f"CSV文件已保存: {full_path}")
        except Exception as e:
            print(f"保存CSV文件失败: {full_path} - {str(e)}")
    
    def _get_full_path(self, file_path: str) -> str:
        """获取完整路径"""
        if os.path.isabs(file_path):
            return file_path
        return os.path.join(self.base_dir, file_path)
    
    def get_test_data(self, test_name: str, env: str = "dev") -> Dict[str, Any]:
        """获取测试数据"""
        # 加载环境配置
        env_config = self.load_yaml("config/test_env.yaml")
        current_env = env_config.get("current_env", env)
        env_data = env_config.get("environments", {}).get(current_env, {})
        
        # 加载通用数据
        common_data = self.load_yaml("data/yaml/common_data.yaml")
        
        # 加载测试特定数据
        test_data = {}
        test_data_file = f"data/yaml/{test_name}_data.yaml"
        if os.path.exists(self._get_full_path(test_data_file)):
            test_data = self.load_yaml(test_data_file)
        
        # 合并数据
        merged_data = {
            **common_data,
            **env_data,
            **test_data
        }
        
        return merged_data
    
    def get_login_data(self) -> Dict[str, Any]:
        """获取登录数据"""
        return self.load_yaml("data/yaml/auth/login_data.yaml")
    
    def get_user_data(self) -> Dict[str, Any]:
        """获取用户数据"""
        return self.load_yaml("data/yaml/system/user_data.yaml")
    
    def get_menu_data(self) -> Dict[str, Any]:
        """获取菜单数据"""
        return self.load_yaml("data/yaml/system/menu_data.yaml")