from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demo.playwright.dev/todomvc/")
    page.goto("https://demo.playwright.dev/todomvc/#/")
    page.get_by_placeholder("What needs to be done?").click()
    page.get_by_placeholder("What needs to be done?").click()
    page.get_by_placeholder("What needs to be done?").fill("run the test")
    page.get_by_placeholder("What needs to be done?").press("Enter")
    page.get_by_placeholder("What needs to be done?").fill("pick up kid")
    page.get_by_placeholder("What needs to be done?").press("Enter")
    page.goto("https://www.google.com/")
    page.get_by_label("Search", exact=True).click()
    page.get_by_label("Search", exact=True).fill("sofa trending")
    page.get_by_role("link", name="9 Sofa Trends for 2024 That").click()
    page.get_by_role("link", name="living room", exact=True).click()
    page.get_by_role("img", name="Small modern living room with").click()
    page.get_by_role("img", name="Small modern living room with").click()
    page.get_by_role("button", name="Close").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
