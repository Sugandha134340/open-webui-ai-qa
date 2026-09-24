from playwright.sync_api import sync_playwright


BASE_URL = "http://localhost:3000"


def test_invalid_login_keeps_user_on_auth_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        signin_requests = []

        def capture_request(request):
            if "/api/v1/auths/signin" in request.url:
                signin_requests.append(request)

        page.on("request", capture_request)

        page.goto(f"{BASE_URL}/auth?redirect=%2F")
        page.wait_for_load_state("networkidle")

        page.locator('input[name="email"]').fill(
            "qa-invalid@example.com"
        )
        page.locator('input[name="password"]').fill(
            "invalid-password"
        )

        page.locator('button[type="submit"]').click()

        page.wait_for_timeout(1000)

        assert page.url.endswith(
            "/auth?redirect=%2F"
        )

        assert len(signin_requests) == 1

        assert signin_requests[0].method == "POST"

        browser.close()