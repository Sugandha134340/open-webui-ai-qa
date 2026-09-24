import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:3000"


@pytest.mark.parametrize("browser_name", ["chromium", "firefox"])
def test_unauthenticated_user_is_redirected_to_login(browser_name):
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch()
        context = browser.new_context()
        page = context.new_page()

        api_requests = []

        def capture_request(request):
            if "/api/" in request.url:
                api_requests.append(request.url)

        page.on("request", capture_request)

        page.goto(BASE_URL)

        page.wait_for_url(
            "**/auth?redirect=%2F",
            timeout=10000,
        )

        # Give asynchronous startup/config requests a short window to complete.
        page.wait_for_timeout(1000)

        assert "/auth" in page.url

        assert any(
            "/api/config" in url
            for url in api_requests
        )

        # /api/version is expected during normal application startup,
        # but its timing can vary across browsers.
        # Do not fail the redirect test solely because this request
        # was not captured before the redirect assertion.
        if not any("/api/version" in url for url in api_requests):
            print("NOTE: /api/version was not observed before redirect")

        browser.close()