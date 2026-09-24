from playwright.sync_api import sync_playwright


BASE_URL = "http://localhost:3000"


def test_unauthenticated_user_is_redirected_to_login():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        api_requests = []

        def capture_request(request):
            if "/api/" in request.url:
                api_requests.append(request.url)

        page.on("request", capture_request)

        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        assert "/auth" in page.url

        assert any(
            "/api/config" in url
            for url in api_requests
        )

        assert any(
            "/api/version" in url
            for url in api_requests
        )

        browser.close()