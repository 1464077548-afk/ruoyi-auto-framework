#!/usr/bin/env python3
"""
运行测试并生成报告
"""

import subprocess
import sys
import os

def run_test_with_report():
    """运行测试并生成报告"""
    # 运行测试
    test_result = subprocess.run(
        [sys.executable, "-m", "pytest", "src/tests", "-v", "--alluredir=allure-results"],
        capture_output=True,
        text=True
    )
    
    print("测试结果:")
    print(test_result.stdout)
    
    if test_result.stderr:
        print("错误信息:")
        print(test_result.stderr)
    
    # 生成Allure报告
    if os.system("allure generate allure-results -o allure-report --clean") == 0:
        print("\nAllure报告已生成，请运行 'allure open allure-report' 查看报告")
    else:
        print("\n生成Allure报告失败，请确保已安装allure-commandline")
    
    return test_result.returncode

if __name__ == "__main__":
    sys.exit(run_test_with_report())