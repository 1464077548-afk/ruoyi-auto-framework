#!/usr/bin/env python3
"""
运行测试脚本
"""

import subprocess
import sys

def run_test():
    """运行测试"""
    # 运行所有测试
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "src/tests", "-v"],
        capture_output=True,
        text=True
    )
    
    print("测试结果:")
    print(result.stdout)
    
    if result.stderr:
        print("错误信息:")
        print(result.stderr)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_test())