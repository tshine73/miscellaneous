import requests
from google_auth_oauthlib.flow import Flow


def oauth_test():
    scopes = ["https://www.googleapis.com/auth/datastudio"]

    flow = Flow.from_client_secrets_file(
        "client_secret_sandbox_oauth2_web_test.json",
        scopes=scopes,
        redirect_uri="http://localhost:5000"
    )
    # auth_url, __ = flow.authorization_url(access_type='offline',include_granted_scopes='true',prompt='consent')
    auth_url, __ = flow.authorization_url()
    print('Please go to this URL: {}'.format(auth_url))

    # The user will get an authorization code. This code is used to get the access token
    code = input('Enter the authorization code: ')
    token = flow.fetch_token(code=code)
    print(token)
    access_token = token["access_token"]

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    url = f"https://datastudio.googleapis.com/v1/assets:search?assetTypes=REPORT"
    permissions = requests.get(url, headers=headers)
    print(permissions.text)


if __name__ == "__main__":
    oauth_test(
