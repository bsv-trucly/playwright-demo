import pytest
from playwright.sync_api import sync_playwright

def test_login_success():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://playwright-demo.eventos.work/console/login")
        page.fill("#mail_address", "trucly@bravesoft.com.vn")
        page.fill("#password", "brave0404")
        page.click("#login_button")
        page.wait_for_url("https://playwright-demo.eventos.work/console/event-home")
        
        assert page.url == "https://playwright-demo.eventos.work/console/event-home"
        
        browser.close()


