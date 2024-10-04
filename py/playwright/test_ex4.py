from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/")
    page.get_by_label("Search", exact=True).click()
    page.frame_locator("iframe[name=\"callout\"]").get_by_label("Stay signed out").click()
    page.get_by_label("Search", exact=True).click()
    page.get_by_label("Search", exact=True).fill("sofa trending")
    page.get_by_label("Search", exact=True).click()
    page.locator("div").filter(has_text="Choose what you’re giving feedback onsofa trending colorsFood court · 387 S 1st").nth(2).click()
    page.get_by_role("button", name="What color sofa is trending").click()
    page.get_by_role("button", name="What is a timeless color for").click()
    page.get_by_role("button", name="What color sofa makes room").click()
    page.get_by_role("link", name="Sofa Color Trends – 11 Hues").click()
    page.get_by_role("img", name="An L-shaped sofa in rust tone").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
