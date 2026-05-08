import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def page():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    yield page
    browser.close()
    p.stop()

@pytest.fixture
def access_to_create_page(page):
    # login
    page.goto("https://admin.odakyu.bravesoft.vn", wait_until="networkidle")
    page.get_by_placeholder("メールアドレス").fill("kimtran@bravesoft.com.vn")
    page.get_by_placeholder("パスワード").fill("brave0404")
    page.get_by_role("button", name="ログイン").click()

    # vào trang create
    page.goto("https://admin.odakyu.bravesoft.vn/account-management")
    return page