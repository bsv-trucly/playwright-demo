from playwright.sync_api import expect

class CreatePage:
    def __init__(self, page):
        self.page = page

    def verify_title_displayed(self):
        expect(
            self.page.get_by_text("新規アカウント追加")
        ).to_be_visible()