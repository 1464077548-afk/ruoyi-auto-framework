#!/usr/bin/env python3
"""
E2E测试配置
"""

import pytest
from playwright.sync_api import sync_playwright
from src.web.pages.login_page import LoginPage
from src.web.pages.home_page import HomePage
from src.core.utils.data_loader import DataLoader

@pytest.fixture(scope="session")
def playwright():
    """Playwright fixture"""
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright):
    """浏览器fixture"""
    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=50
    )
    yield browser
    browser.close()

@pytest.fixture(scope="session")
def context(browser):
    """上下文fixture"""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080}
    )
    yield context
    context.close()

@pytest.fixture(scope="function")
def page(context):
    """页面fixture"""
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="function")
def login_page(page):
    """登录页面fixture"""
    return LoginPage(page)

@pytest.fixture(scope="function")
def home_page(page):
    """首页fixture"""
    return HomePage(page)

@pytest.fixture(scope="function")
def logged_in_page(page, login_page):
    """已登录页面fixture"""
    # 加载登录数据
    data_loader = DataLoader()
    login_data = data_loader.get_login_data()
    valid_login = login_data.get("login", {}).get("valid", {})
    
    # 登录
    login_page.navigate()
    login_page.login(
        valid_login.get("username", "admin"),
        valid_login.get("password", "admin123")
    )
    
    # 等待登录成功
    login_page.wait_for_navigation()
    
    yield page
    
    # 退出登录
    try:
        login_page.logout()
    except Exception:
        pass