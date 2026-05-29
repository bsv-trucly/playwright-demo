import pytest
import os
from pathlib import Path

# ── Constants ────────────────────────────────────────
ARTIFACTS_DIR = Path("test-artifacts")
ARTIFACTS_DIR.mkdir(exist_ok=True)

# ── Hook nhận biết PASS/FAIL ─────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

# ── Fixture tracing ───────────────────────────────────
@pytest.fixture(autouse=True)
def tracing(context, request):
    context.tracing.start(screenshots=True, snapshots=True)
    yield
    test_failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else False

    # ── Chọn 1 trong 2 mode bên dưới ──────────────────
    TRACING_MODE = "only-on-failure"  # ← đổi thành "on" để lưu tất cả

    if TRACING_MODE == "on":
        # Lưu trace trong mọi TH
        context.tracing.stop(
            path=str(ARTIFACTS_DIR / f"{request.node.name}.zip")
        )
    elif TRACING_MODE == "only-on-failure":
        # Chỉ lưu khi FAIL
        if test_failed:
            context.tracing.stop(
                path=str(ARTIFACTS_DIR / f"{request.node.name}.zip")
            )
        else:
            context.tracing.stop()

#config Hook:
BASE_URL = "https://bsv-nhungnguyen.github.io/"
# ── beforeAll (scope="session") ──────────────────────
@pytest.fixture(scope="session", autouse=True)
def before_all_after_all():
    # beforeAll: chạy 1 lần trước toàn bộ session
    print("\n[beforeAll] Setup môi trường test...")
    yield
    # afterAll: chạy 1 lần sau toàn bộ session
    print("\n[afterAll] Kết thúc test session - dọn dẹp môi trường.")

# ── beforeEach only ───────────────────────────────────
@pytest.fixture(scope="function")
def before_each(page):
    # beforeEach: tự động login trước mỗi test
    page.goto(BASE_URL)
    page.locator("#hk-username").fill("admin")
    page.locator("#hk-password").fill("password123")
    page.locator("#hk-btn-login").click()
    yield page
    # Không có afterEach

# ── afterEach only ────────────────────────────────────
@pytest.fixture(scope="function")
def after_each(page):
    yield page
    # afterEach: tự động xóa record sau mỗi test
    page.locator("#hk-btn-delete-1").click()

# ── beforeEach / afterEach ────────────────────────────
@pytest.fixture(scope="function")
def before_each_after_each(page):
    # beforeEach: tự động login trước mỗi test
    page.goto(BASE_URL)
    page.locator("#hk-username").fill("admin")
    page.locator("#hk-password").fill("password123")
    page.locator("#hk-btn-login").click()
    yield page
    # afterEach: tự động xóa record sau mỗi test
    page.locator("#hk-btn-delete-1").click()