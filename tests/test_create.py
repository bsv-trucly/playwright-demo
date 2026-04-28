from playwright.sync_api import sync_playwright, expect

# =====================
# SETUP CHUNG
# =====================
BASE_URL = "https://admin.odakyu.bravesoft.vn"
EMAIL = "kimtran@bravesoft.com.vn"
PASSWORD = "brave0404"
CREATE_URL = "https://admin.odakyu.bravesoft.vn/account-management"


# =====================
# HÀM DÙNG CHUNG
# =====================
def open_create_form():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # login
    page.goto(BASE_URL)
    page.locator("input[name='email']").fill(EMAIL)
    page.locator("input[name='password']").fill(PASSWORD)
    page.locator("button.login-button").click()
    page.wait_for_load_state("networkidle")

    # vào trang create
    page.goto(CREATE_URL)
    page.wait_for_load_state("networkidle")

    # click button 新規追加
    page.locator("button.common-submit-btn").click()

    return page, browser, p


# =====================
# TEST CASES
# =====================

# Case 1: Kiểm tra title hiển thị đúng
def test_case_01_title_display_correctly():
    page, browser, p = open_create_form()

    expect(page.get_by_text("新規アカウント追加")).to_be_visible()

    browser.close()
    p.stop()

# Case 2: Kiểm tra URL
def test_case_02_VerifyURL():
    page, browser, p = open_create_form()
    expect(page).to_have_url("https://admin.odakyu.bravesoft.vn/account-management")


# Case 3: Kiểm tra label アカウント名
def test_case_03_label_account_name_displayed():
    page, browser, p = open_create_form()

    expect(page.locator("div.label-title").filter(has_text="アカウント名")).to_be_visible()
    expect(page.locator(".required-mark").first).to_be_visible()
    expect(page.get_by_text("255文字以内")).to_be_visible()

    browser.close()
    p.stop()

# Case 4: Kiểm tra có nhập được text vào textbox アカウント名
def test_case_04_VerifyAccountNameTextboxAcceptsInput():
    page, browser, p = open_create_form()

    page.locator("input[name='userName']").fill("チュック")
    expect( page.locator("input[name='userName']")).to_have_value("チュック")

# Case 5: Kiểm tra label メールアドレス
def test_case_05_VerifylabelMailadress():
    page, browser, p = open_create_form()

    expect(page.locator("div.label-title").filter(has_text="メールアドレス")).to_be_visible()
    expect(page.locator(".required-mark").first).to_be_visible()

# Case 6: Kiểm tra nhập mail vào textbox Mailaddress
def test_case_06_VerifyMailaddressTextboxAcceptsInput():
    page, browser, p = open_create_form()

    page.locator("input[name='email']").fill("trucly@bravesoft.com.vn")
    expect(page.locator("input[name='email']")).to_have_value("trucly@bravesoft.com.vn")

# Case 7: Kiểm tra hiển thị label パスワード
def test_case_07_VerifyLabelパスワード():
    page, browser, p = open_create_form()

    expect(page.locator("div.label-title").filter(has_text="パスワード")).to_be_visible()
    expect(page.locator(".required-mark").first).to_be_visible()
    expect(page.get_by_text("（半角英数字 8文字以上32文字以内）")).to_be_visible()

# Case 8: Kiêm tra placeholder của textbox パスワード
def test_case_08_Verifytextboxパスワードplaceholder():
    page, browser, p = open_create_form()

    expect(page.locator("input[name='password']")).to_have_attribute("placeholder","**********")

# Case 9: Kiểm tra khi input vào textbox パスワード
def test_case_09_VerifyPasswordFieldMasksInput():
    page, browser, p = open_create_form()

    page.locator("input[name='password']").fill("brave0404")
    expect(page.locator("input[name='password']")).to_have_value("brave0404")
    expect(page.locator("input[name='password']")).to_have_attribute("type", "password")

# Case 10: Kiểm tra hiển thị selectbox 権限
def test_case_10_VerifyAuthoritySelectbox():
    page, browser, p = open_create_form()

    expect(page.locator("div.label-title").filter(has_text="権限")).to_be_visible()
    expect(page.locator(".required-mark").first).to_be_visible()
    expect(page.get_by_role("combobox").nth(0)).to_be_visible()
    expect(page.get_by_role("combobox").nth(1)).to_have_attribute("aria-expanded", "false")

# Case 11: Kiểm tra chọn マスター管理者 trong selectbox 権限
def test_case_11_VerifySelectMasterAdmin():
    page, browser, p = open_create_form()

    page.locator(".modify-account-modal").wait_for(state="visible")
    page.get_by_role("combobox").nth(1).click()
    page.get_by_role("option", name="マスター管理者").click()
    expect(page.get_by_role("combobox").nth(1)).to_contain_text("マスター管理者")

# Case 12: Kiểm tra chọn テナント管理者 trong selectbox 権限
def test_case_12_VerifySelectMasterAdmin():
    page, browser, p = open_create_form()

    page.locator(".modify-account-modal").wait_for(state="visible")
    page.get_by_role("combobox").nth(1).click()
    page.get_by_role("option", name="テナント管理者").click()
    expect(page.get_by_role("combobox").nth(1)).to_contain_text("テナント管理者")

# Case 13: Kiểm tra chỉ chọn được 1 option trong selectbox 権限
def test_case_13_VerifySelectOnlyOneOption():
    page, browser, p = open_create_form()

    page.locator(".modify-account-modal").wait_for(state="visible")
    page.get_by_role("combobox").nth(1).click()
    page.get_by_role("option", name="マスター管理者").click()
    page.get_by_role("combobox").nth(1).click()
    page.get_by_role("option", name="テナント管理者").click()
    expect(page.get_by_role("combobox").nth(1)).to_contain_text("テナント管理者")
    expect(page.get_by_role("combobox").nth(1)).not_to_contain_text("マスター管理者")

# Case 14: Kiểm tra hiển thị label チケット組成時のポイント付与パラメータの変更権限
def test_case_14_VerifyLabelTicketPermission():
    page, browser, p = open_create_form()

    page.locator(".modify-account-modal").wait_for(state="visible")

    page.get_by_role("combobox").nth(1).click()
    page.get_by_role("option", name="テナント管理者").click()

    expect(page.get_by_text("チケット組成時のポイント付与パラメータの変更権限")).to_be_visible()
    expect(page.get_by_text("有")).to_be_visible()
    expect(page.get_by_text("無")).to_be_visible()

    browser.close()
    p.stop()


# Case 15: Kiểm tra chọn 有
def test_case_15_VerifySelectYes():
    page, browser, p = open_create_form()

    page.locator(".modify-account-modal").wait_for(state="visible")

    page.get_by_role("combobox").nth(1).click()
    page.get_by_role("option", name="テナント管理者").click()
    page.get_by_text("有").click()

    expect(page.get_by_role("radio", name="有")).to_be_checked()

    browser.close()
    p.stop()


# Case 16: Kiểm tra chọn 無
def test_case_16_VerifySelectNo():
    page, browser, p = open_create_form()

    page.locator(".modify-account-modal").wait_for(state="visible")

    page.get_by_role("combobox").nth(1).click()
    page.get_by_role("option", name="テナント管理者").click()
    page.get_by_text("無").click()

    expect(page.get_by_role("radio", name="無")).to_be_checked()

    browser.close()
    p.stop()


# Case 17: Kiểm tra chỉ chọn được 1 option 有 hoặc 無
def test_case_17_VerifySelectOnlyOneRadio():
    page, browser, p = open_create_form()

    page.locator(".modify-account-modal").wait_for(state="visible")

    page.get_by_role("combobox").nth(1).click()
    page.get_by_role("option", name="テナント管理者").click()
    page.get_by_text("有").click()
    page.get_by_text("無").click()

    expect(page.get_by_role("radio", name="無")).to_be_checked()
    expect(page.get_by_role("radio", name="有")).not_to_be_checked()

    browser.close()
    p.stop()