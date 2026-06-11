from playwright.sync_api import sync_playwright, expect

BASE_URL = "https://bsv-nhungnguyen.github.io/"

## Frames & Iframes
def test_Case1(page):
    page.goto(BASE_URL)
    frame = page.frame_locator("#demo-iframe")
    frame.get_by_placeholder("Enter your name").fill("Truc")
    frame.get_by_role("button", name="Submit").click()
    expect(frame.get_by_text("Success: Hello Truc!")).to_be_visible()

def test_Case2(page):
    page.goto(BASE_URL)
    page.get_by_role("button",name="Load Nested Frames (A → B → C)").click()
    frame_a = page.frame_locator("#iframe-A")
    expect(frame_a.get_by_text("Iframe A")).to_be_visible()
    frame_a.get_by_role("button",name="Click button").click()
    expect(frame_a.get_by_text("Iframe A Clicked!")).to_be_visible()
    frame_a.get_by_role("button",name="Open Iframe B").click()
    expect(frame_a.get_by_text("Iframe B")).to_be_visible()

def test_Case3(page):
    page.goto(BASE_URL)
    page.get_by_role("button",name="Load Nested Frames (A → B → C)").click()
    frame_a = page.frame_locator("#iframe-A")
    frame_a.get_by_role("button",name="Open Iframe B").click()
    frame_b =frame_a.frame_locator("#iframe-B")
    expect(frame_b.get_by_text("Iframe B")).to_be_visible()
    expect(frame_b.get_by_role("button", name="Click button")).to_be_visible()
    expect(frame_b.get_by_role("button", name="Open Iframe C")).to_be_visible()

def test_Case4(page):
    page.goto(BASE_URL)
    page.get_by_role("button",name="Load Nested Frames (A → B → C)").click()
    frame_a = page.frame_locator("#iframe-A")
    frame_a.get_by_role("button",name="Open Iframe B").click()
    frame_b =frame_a.frame_locator("#iframe-B")
    frame_b.get_by_role("button", name="Open Iframe C").click()
    frame_c =frame_b.frame_locator("#iframe-C")
    expect(frame_c.get_by_text("Iframe C")).to_be_visible()
    expect(frame_c.get_by_role("button",name ="Click button")).to_be_visible()

def test_Case5(page):
    page.goto(BASE_URL)
    page.get_by_role("button", name="Load Nested Frames (A → B → C)").click()
    frame_a = page.frame_locator("#iframe-A")
    frame_a.get_by_role("button",name="Open Iframe B").click()
    frame_b =frame_a.frame_locator("#iframe-B")
    frame_b.get_by_role("button", name="Open Iframe C").click()
    frame_c =frame_b.frame_locator("#iframe-C")
    frame_c.get_by_role("button", name="Click button").click()
    expect(frame_c.get_by_text("Iframe C Clicked!")).to_be_visible()

## Windows & Popups
def test_Case6(page, context):
    page.goto(BASE_URL)
    with context.expect_page() as new_page_info:
     page.get_by_role("button", name=("Open New Tab (playwright.dev)")).click()
    new_page = new_page_info.value
    new_page.wait_for_load_state()
    new_page.get_by_role("link", name="Get started").click()
    expect(new_page.get_by_role("heading", name="Installation")).to_be_visible()

def test_Case7(page, context):
    page.goto(BASE_URL)
    with context.expect_page() as popup_info:
     page.get_by_role("button", name=("Open Popup Window")).click()
    popup = popup_info.value
    popup.wait_for_load_state()
    expect(popup.get_by_role("heading", name="Popup Activated")).to_be_visible()

def test_Case8(page):
    page.goto(BASE_URL)
    page.get_by_role("button", name="Open In-page Moda").click()
    expect(page.get_by_role("heading", name="Secure Confirmation")).to_be_visible()

def test_Case9(page):
    page.goto(BASE_URL)
    page.get_by_role("button", name="Open In-page Modal").click()
    page.get_by_placeholder("Enter code (e.g. 1234)").fill("Truc")
    page.locator("#modal-overlay").get_by_role("button", name="Confirm").click()
    expect(page.get_by_text("✓ Verified: Truc")).to_be_visible()

def test_Case10(page):
   page.goto(BASE_URL)
   page.get_by_role("button", name="Open In-page Modal").click()
   page.get_by_placeholder("Enter code (e.g. 1234)").fill("Truc")
   page.locator("#modal-overlay").get_by_role("button", name="Cancel").click()
   expect(page.get_by_text("✓ Verified: Truc")).not_to_be_visible()

##Dialogs
def test_Case11(page):
   page.goto(BASE_URL)
   dialog_message = []
   page.on("dialog", lambda dialog: (
        dialog_message.append(dialog.message),
        dialog.accept()))
   page.get_by_role("button", name="Trigger Alert").click()
   assert dialog_message[0] == "This is a browser alert!"

def test_Case12(page):
   page.goto(BASE_URL)
   page.on("dialog", lambda dialog: dialog.accept())
   page.get_by_role("button", name="Trigger Alert").click()
   expect(page.get_by_role("button", name="Trigger Alert")).to_be_visible()

def test_Case13(page):
   page.goto(BASE_URL)
   dialog_message = []
   page.on("dialog", lambda dialog:(dialog_message.append(dialog.message),dialog.accept()))
   page.get_by_role("button", name="Trigger Confirm").click()
   assert dialog_message[0] == "Continue?"

def test_Case14(page):
   page.goto(BASE_URL)
   page.on("dialog", lambda dialog:dialog.accept())
   page.get_by_role("button", name="Trigger Confirm").click()
   expect(page.get_by_text("Confirmed")).to_be_visible()

def test_Case15(page):
   page.goto(BASE_URL)
   page.on("dialog", lambda dialog:dialog.dismiss())
   page.get_by_role("button", name="Trigger Confirm").click()
   expect(page.get_by_text("Cancelled")).to_be_visible()

def test_Case16(page):
   page.goto(BASE_URL)
   page.on("dialog", lambda dialog:dialog.accept("Truc nè!"))
   page.get_by_role("button", name="Trigger Prompt").click()
   expect(page.get_by_text("Truc nè!")).to_be_visible()

def test_Case17(page):
   page.goto(BASE_URL)
   page.on("dialog", lambda dialog:dialog.dismiss())
   page.get_by_role("button", name="Trigger Prompt").click()
   expect(page.get_by_text("Dismissed")).to_be_visible()

##Visual Regressions

# Case 18: Chụp trong mọi trường hợp → đổi config thành --screenshot=on
def test_Case18(page):
    page.goto(BASE_URL)
    page.get_by_role("button", name="Normal State").click()
    expect(page.get_by_text("System Normal")).to_be_visible()
    page.screenshot(path="test-results/test_Case18.png", full_page=True)


# Case 19: Chỉ chụp khi FAIL, test PASS → đổi config thành ----screenshot=only-on-failure
def test_Case19(page):
    page.goto(BASE_URL)
    page.get_by_role("button", name="Normal State").click()
    expect(page.get_by_text("System Normal")).to_be_visible()
    page.locator("#section-screenshot").page.screenshot(path="test-results/test_Case19.png")


# Case 20: Chỉ chụp khi FAIL, test FAIL → đổi config thành ----screenshot=only-on-failure
def test_Case20(page):
    page.goto(BASE_URL)
    page.get_by_role("button", name="Failure State").click()
    expect(page.get_by_text("System Normal")).to_be_visible()

# Case 21: Quay video trong mọi trường hợp
# Config pytest.ini: --video=on
def test_Case21(page):
    page.goto(BASE_URL)
    page.get_by_role("button", name="Play Sequence").click()
    expect(page.get_by_text("Sequence complete!")).to_be_visible(timeout=30000)


# Case 22: Chỉ quay trong TH failed — test PASS nên không có video
# Config pytest.ini: --video=retain-on-failure
def test_Case22(page):
    page.goto(BASE_URL)
    page.get_by_role("button", name="Play Sequence").click()
    expect(page.get_by_text("Sequence complete!")).to_be_visible(timeout=50000)


# Case 23: Chỉ quay trong TH failed — test FAIL nên có video
# Config pytest.ini: --video=retain-on-failure
def test_Case23(page):
    page.goto(BASE_URL)
    page.get_by_role("button", name="Play Sequence").click()
    expect(page.get_by_text("Sequence complete!")).to_be_visible(timeout=1000)

# Case 24: Trace trong mọi TH — test PASS → có trace
def test_Case24(page):
    page.goto(BASE_URL)
    page.get_by_placeholder("Developer Name").fill("Truc")
    page.get_by_placeholder("dev@example.com").fill("truclytest@gmail.com")
    page.get_by_role("button", name="Submit Form").click()
    expect(page.get_by_text("Submitted: Truc")).to_be_visible()
    
# Case 25: Trace trong TH Failed  → sửa config only-on-failure
def test_Case25(page):
    page.goto(BASE_URL)
    page.get_by_placeholder("Developer Name").fill("")
    page.get_by_placeholder("dev@example.com").fill("")
    page.get_by_role("button", name="Submit Form").click()
    expect(page.get_by_text("Submitted: Truc")).to_be_visible()

# Case 26: Trace trong TH Failed  → sửa config only-on-failure
def test_Case26(page):
    page.goto(BASE_URL)
    page.get_by_placeholder("Developer Name").fill("Truc")
    page.get_by_placeholder("dev@example.com").fill("truclytest@gmail.com")
    page.get_by_role("button", name="Submit Form").click()
    expect(page.get_by_text("Submitted: Truc")).to_be_visible()

##Hook
# Case 27: beforeAll
def test_Case27(page):
    page.goto(BASE_URL)
    expect(page.get_by_role("heading", name ="Playwright test 08.05.2026")).to_be_visible()
    # In thông báo để verify beforeAll đã chạy
    print("\n[beforeAll] Setup môi trường test đã chạy")

# Case 28: afterAll
def test_Case28(page):
    page.goto(BASE_URL)
    expect(page.get_by_role("heading", name ="Playwright test 08.05.2026")).to_be_visible()
    # In thông báo để verify beforeAll đã chạy
    print("\n[beforeAll] Setup môi trường test đã chạy")

# Case 29: beforeEach — tự động login trước test
def test_Case29(before_each):
    page = before_each
    page.get_by_placeholder("e.g. Fix login bug").fill("Fix login bug")
    page.get_by_label("Category").select_option("bug")
    page.get_by_role("button", name="Create Record").click()
    expect(page.get_by_role("cell", name="Fix login bug")).to_be_visible()

# Case 30: beforeEach after_each
def test_Case30(before_each_after_each):
    page = before_each_after_each
    page.get_by_placeholder("e.g. Fix login bug").fill("Truc test")
    page.get_by_label("Category").select_option("Task")
    page.get_by_role("button", name="Create Record").click()
    expect(page.get_by_role("cell", name="Truc test")).to_be_visible()