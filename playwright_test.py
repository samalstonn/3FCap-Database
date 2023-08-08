from __future__ import print_function
import time
from playwright.sync_api import Playwright, sync_playwright, expect
from rauth import OAuth1Service
import webbrowser
from mongo_test import update
import logins


base_url = "https://api.etrade.com"


def portfolio_data(session):
    """
    This function will return the portfolio data
    """
    url = base_url + "/v1/accounts/list.json"

    # Make API call for GET request
    response = session.get(url, header_auth=True).json()

    account = response["AccountListResponse"]["Accounts"]["Account"][0]

    url = base_url + "/v1/accounts/" + account["accountIdKey"] + "/portfolio.json"

    # Make API call for GET request
    response = session.get(url, header_auth=True)
    return response.json()


def use_playwright(playwright: Playwright, authorize_url):
    """
    This function will use playwright to get the verification code
    """
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(authorize_url)
    page.get_by_label("User ID", exact=True).click()
    page.get_by_label("User ID", exact=True).fill(logins.etrade_username)
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill(logins.etrade_password)
    page.get_by_role("button", name="Log on").click()
    page.get_by_role("button", name="Accept").click()
    return page.get_by_role("textbox").text_content()


def oauth():
    """Allows user authorization for the sample application with OAuth 1"""
    etrade = OAuth1Service(
        name="etrade",
        consumer_key=logins.consumer_key,
        consumer_secret=logins.consumer_secret,
        request_token_url="https://api.etrade.com/oauth/request_token",
        access_token_url="https://api.etrade.com/oauth/access_token",
        authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
        base_url="https://api.etrade.com",
    )

    # Step 1: Get OAuth 1 request token and secret
    request_token, request_token_secret = etrade.get_request_token(
        params={"oauth_callback": "oob", "format": "json"}
    )

    # Step 2: Go through the authentication flow. Login to E*TRADE.
    # After you login, the page will provide a verification code to enter.
    authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)

    # with sync_playwright() as playwright:
    #     (n := use_playwright(playwright, authorize_url))
    # print(n)
    # webbrowser.open(authorize_url)
    # text_content = input("Enter verification code: ")

    # # Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
    # session = etrade.get_auth_session(
    #     request_token, request_token_secret, params={"oauth_verifier": text_content}
    # )
    while True:
        time.sleep(5)
        update()


if __name__ == "__main__":
    oauth()
