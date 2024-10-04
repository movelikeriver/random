from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/")
    page.frame_locator("iframe[name=\"callout\"]").get_by_label("Stay signed out").click()
    page.get_by_label("Search", exact=True).click()
    page.get_by_label("Search", exact=True).fill("sofa trending")
    page.get_by_role("button", name="What is the current trend in").click()
    page.get_by_role("button", name="What is the trend in sofa").click()
    page.get_by_role("link", name="4 Living Room Sofa Trends for").click()
    page.get_by_role("button", name="Do Not Sell My Personal").click()
    page.get_by_role("heading", name="Strictly Necessary Cookies").click()
    page.get_by_role("button", name="Confirm My Choices").click()
    page.get_by_role("button", name="close dialog").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
