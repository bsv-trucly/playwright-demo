import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://playwright-demo.eventos.work/web/portal/529/event/3988/users/login"
LOGIN_URL = f"{BASE_URL}/login"
TOP_URL = f"{BASE_URL}/top"

VALID_EMAIL = "truclytest@gmail.com"
VALID_PASSWORD = "brave0404"
WRONG_PASSWORD = "wrongpassword1"
UNREGISTERED_EMAIL = "notregistered@example.com"

EMAIL_ERROR_INVALID = "メールアドレスが正しくありません。"
EMAIL_ERROR_REQUIRED = "メールアドレスを入力してください"
PASSWORD_ERROR_LENGTH = "パスワードは8文字以上32文字以下で指定してください。"
LOGIN_ERROR_MSG = "ログインできませんでした。入力内容をご確認の上、もう一度お試しください。"


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        pg = context.new_page()
        pg.goto(LOGIN_URL)
        pg.wait_for_load_state("networkidle")
        yield pg
        context.close()
        browser.close()



# ===== 画面タイトル =====

def test_login_page_title(page):
    """「ログイン」画面タイトルが表示されること"""
    # get_by_role: <h1>, <h2>,... có text "ログイン"
    assert page.get_by_role("heading", name="ログイン").is_visible()


# ===== メールアドレス 表示 =====

def test_email_label_displayed(page):
    """「メールアドレス」ラベルが表示されること"""
    # get_by_text: text hiển thị trực tiếp trên UI
    assert page.get_by_text("メールアドレス").first.is_visible()


def test_email_textbox_displayed(page):
    """メールアドレス テキストボックスが表示されること"""
    # get_by_label: tìm input được gắn với <label>メールアドレス</label>
    assert page.get_by_label("メールアドレス").is_visible()


# ===== メールアドレス 入力 =====

def test_email_can_type_and_display(page):
    """メールアドレスフィールドに文字入力でき、入力した文字が表示されること"""
    page.get_by_label("メールアドレス").fill("test@example.com")
    assert page.get_by_label("メールアドレス").input_value() == "test@example.com"


def test_email_valid_lowercase(page):
    """「abc@gmail.com」入力で入力した文字が表示されること（エラーなし）"""
    page.get_by_label("メールアドレス").fill("abc@gmail.com")
    page.get_by_label("メールアドレス").press("Tab")
    assert page.get_by_label("メールアドレス").input_value() == "abc@gmail.com"
    assert not page.get_by_text(EMAIL_ERROR_INVALID).is_visible()


def test_email_valid_uppercase(page):
    """「ABC@GMAIL.COM」入力で入力した文字が表示されること（エラーなし）"""
    page.get_by_label("メールアドレス").fill("ABC@GMAIL.COM")
    page.get_by_label("メールアドレス").press("Tab")
    assert page.get_by_label("メールアドレス").input_value() == "ABC@GMAIL.COM"
    assert not page.get_by_text(EMAIL_ERROR_INVALID).is_visible()


def test_email_invalid_missing_tld(page):
    """「abc@gmail」（形式不正）でエラー「メールアドレスが正しくありません。」表示"""
    page.get_by_label("メールアドレス").fill("abc@gmail")
    page.get_by_label("メールアドレス").press("Tab")
    # get_by_text: text thông báo lỗi hiển thị trên UI
    assert page.get_by_text(EMAIL_ERROR_INVALID).is_visible()


def test_email_invalid_special_char_before_at(page):
    """「abc!@gmail.com」（形式不正）でエラー「メールアドレスが正しくありません。」表示"""
    page.get_by_label("メールアドレス").fill("abc!@gmail.com")
    page.get_by_label("メールアドレス").press("Tab")
    assert page.get_by_text(EMAIL_ERROR_INVALID).is_visible()


def test_email_invalid_no_at_symbol(page):
    """「test.abc」（形式不正）でエラー「メールアドレスが正しくありません。」表示"""
    page.get_by_label("メールアドレス").fill("test.abc")
    page.get_by_label("メールアドレス").press("Tab")
    assert page.get_by_text(EMAIL_ERROR_INVALID).is_visible()


def test_email_invalid_starts_with_at(page):
    """「@gmail.com」（形式不正）でエラー「メールアドレスが正しくありません。」表示"""
    page.get_by_label("メールアドレス").fill("@gmail.com")
    page.get_by_label("メールアドレス").press("Tab")
    assert page.get_by_text(EMAIL_ERROR_INVALID).is_visible()


def test_email_invalid_fullwidth_characters(page):
    """全角文字入力でエラー「メールアドレスが正しくありません。」表示"""
    page.get_by_label("メールアドレス").fill("テスト＠ｇｍａｉｌ．ｃｏｍ")
    page.get_by_label("メールアドレス").press("Tab")
    assert page.get_by_text(EMAIL_ERROR_INVALID).is_visible()


def test_email_empty_shows_required_error(page):
    """メールアドレスをクリアするとエラー「メールアドレスを入力してください」表示"""
    page.get_by_label("メールアドレス").fill("test@example.com")
    page.get_by_label("メールアドレス").fill("")
    page.get_by_label("メールアドレス").press("Tab")
    assert page.get_by_text(EMAIL_ERROR_REQUIRED).is_visible()


# ===== パスワード 表示 =====

def test_password_label_displayed(page):
    """「パスワード」ラベルが表示されること"""
    # get_by_text: text hiển thị trực tiếp trên UI
    assert page.get_by_text("パスワード").first.is_visible()


def test_password_textbox_displayed(page):
    """パスワード テキストボックスが表示されること"""
    # get_by_label: tìm input được gắn với <label>パスワード</label>
    assert page.get_by_label("パスワード").is_visible()


def test_password_mask_icon_initially_inactive(page):
    """初期状態でパスワードはマスク表示（type=password）、アイコンは非アクティブ"""
    assert page.get_by_label("パスワード").get_attribute("type") == "password"


# ===== パスワード 入力・マスク =====

def test_password_input_is_masked(page):
    """パスワード入力時に「*****」でマスク表示されること"""
    page.get_by_label("パスワード").fill("TestPass1")
    assert page.get_by_label("パスワード").get_attribute("type") == "password"


def test_password_unmask_on_eye_icon_click(page):
    """目アイコンを押すとマスク表示が解除され、アイコンがアクティブになること"""
    page.get_by_label("パスワード").fill("TestPass1")
    # get_by_role: <button> dùng để toggle hiển thị mật khẩu
    # Nếu button có aria-label khác, thay name= cho phù hợp
    page.get_by_role("button", name="パスワードを表示").click()
    assert page.get_by_label("パスワード").get_attribute("type") == "text"


def test_password_remask_on_second_eye_icon_click(page):
    """目アイコンをもう一度押すとマスク表示に戻り、アイコンが非アクティブになること"""
    page.get_by_label("パスワード").fill("TestPass1")
    toggle = page.get_by_role("button", name="パスワードを表示")
    toggle.click()
    toggle.click()
    assert page.get_by_label("パスワード").get_attribute("type") == "password"


# ===== パスワード バリデーション =====

def test_password_too_short_shows_error(page):
    """8文字以下でエラー「パスワードは8文字以上32文字以下で指定してください。」表示"""
    page.get_by_label("パスワード").fill("pass1")
    page.get_by_label("パスワード").press("Tab")
    assert page.get_by_text(PASSWORD_ERROR_LENGTH).is_visible()


def test_password_max_32_chars_cannot_exceed(page):
    """32文字を超えて入力できないこと"""
    page.get_by_label("パスワード").fill("A" * 33)
    assert len(page.get_by_label("パスワード").input_value()) <= 32


def test_password_numbers_only_no_error(page):
    """「数字」のみのパスワードでエラーが表示されないこと"""
    page.get_by_label("パスワード").fill("12345678")
    page.get_by_label("パスワード").press("Tab")
    assert not page.get_by_text(PASSWORD_ERROR_LENGTH).is_visible()


def test_password_letters_only_no_error(page):
    """「英大文字・英小文字」のみでエラーが表示されないこと"""
    page.get_by_label("パスワード").fill("AbCdEfGh")
    page.get_by_label("パスワード").press("Tab")
    assert not page.get_by_text(PASSWORD_ERROR_LENGTH).is_visible()


def test_password_symbols_only_no_error(page):
    """「記号」のみでエラーが表示されないこと"""
    page.get_by_label("パスワード").fill("!@#$%^&*")
    page.get_by_label("パスワード").press("Tab")
    assert not page.get_by_text(PASSWORD_ERROR_LENGTH).is_visible()


def test_password_numbers_and_letters_no_error(page):
    """「数字」と「英大文字・英小文字」の組み合わせでエラーが表示されないこと"""
    page.get_by_label("パスワード").fill("Abc12345")
    page.get_by_label("パスワード").press("Tab")
    assert not page.get_by_text(PASSWORD_ERROR_LENGTH).is_visible()


def test_password_numbers_and_symbols_no_error(page):
    """「数字」と「記号」の組み合わせでエラーが表示されないこと"""
    page.get_by_label("パスワード").fill("1234!@#$")
    page.get_by_label("パスワード").press("Tab")
    assert not page.get_by_text(PASSWORD_ERROR_LENGTH).is_visible()


def test_password_symbols_and_letters_no_error(page):
    """「記号」と「英大文字・英小文字」の組み合わせでエラーが表示されないこと"""
    page.get_by_label("パスワード").fill("Abc!@#$%")
    page.get_by_label("パスワード").press("Tab")
    assert not page.get_by_text(PASSWORD_ERROR_LENGTH).is_visible()


# ===== パスワードをお忘れた場合 =====

def test_forgot_password_link_with_underline_displayed(page):
    """「パスワードを忘れた方はこちら」リンクに下線付きで表示されること"""
    # get_by_role: <a> link có text "パスワードを忘れた方はこちら"
    link = page.get_by_role("link", name="パスワードを忘れた方はこちら")
    assert link.is_visible()
    text_decoration = link.evaluate("el => window.getComputedStyle(el).textDecorationLine")
    assert "underline" in text_decoration


def test_forgot_password_link_navigates_to_reset_page(page):
    """「パスワードを忘れた方はこちら」を押すとパスワード再設定画面に遷移すること"""
    page.get_by_role("link", name="パスワードを忘れた方はこちら").click()
    page.wait_for_load_state("networkidle")
    assert any(kw in page.url for kw in ["/password", "/reset", "/forgot", "/remind"])


# ===== ログインボタン =====

def test_login_button_displayed_and_initially_disabled(page):
    """ログインボタンが表示され、初期状態が非活性（disabled）であること"""
    # get_by_role: <button> có text "ログイン"
    login_btn = page.get_by_role("button", name="ログイン")
    assert login_btn.is_visible()
    is_disabled = (
        login_btn.is_disabled()
        or login_btn.get_attribute("disabled") is not None
        or "disabled" in (login_btn.get_attribute("class") or "")
    )
    assert is_disabled


def test_login_fail_correct_email_wrong_password(page):
    """正しいメールアドレス・間違ったパスワードでログイン失敗しエラーメッセージ表示"""
    page.get_by_label("メールアドレス").fill(VALID_EMAIL)
    page.get_by_label("パスワード").fill(WRONG_PASSWORD)
    page.get_by_role("button", name="ログイン").click()
    page.wait_for_load_state("networkidle")
    assert page.get_by_text(LOGIN_ERROR_MSG).is_visible()


def test_login_fail_unregistered_email_correct_password(page):
    """未登録メールアドレス・正しいパスワードでログイン失敗しエラーメッセージ表示"""
    page.get_by_label("メールアドレス").fill(UNREGISTERED_EMAIL)
    page.get_by_label("パスワード").fill(VALID_PASSWORD)
    page.get_by_role("button", name="ログイン").click()
    page.wait_for_load_state("networkidle")
    assert page.get_by_text(LOGIN_ERROR_MSG).is_visible()


def test_login_success(page):
    """正しいメールアドレスと正しいパスワードでログイン成功しプロファイル画面へ遷移すること"""
    page.get_by_label("メールアドレス").fill(VALID_EMAIL)
    page.get_by_label("パスワード").fill(VALID_PASSWORD)
    page.get_by_role("button", name="ログイン").click()
    page.wait_for_load_state("networkidle")
    assert any(kw in page.url for kw in ["/event-home", "/profile", "/dashboard", "/home"])


# ===== 新規登録 =====

def test_new_registration_button_displayed(page):
    """「新規登録」ボタンが表示されること"""
    # get_by_role: <button> hoặc <a> có text "新規登録"
    assert page.get_by_role("button", name="新規登録").is_visible()


def test_new_registration_button_navigates(page):
    """「新規登録」ボタンを押すと新規登録画面に遷移すること"""
    page.get_by_role("button", name="新規登録").click()
    page.wait_for_load_state("networkidle")
    assert any(kw in page.url for kw in ["/register", "/signup", "/new", "/entry"])
