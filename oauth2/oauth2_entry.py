#
#    Copyright 2019 Google LLC
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        https://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import google.oauth2.credentials
import google_auth_oauthlib.flow
import os
import sys
import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import googleapiclient
from googleapiclient import sample_tools
from googleapiclient.http import build_http

from google.oauth2 import service_account

# credentials.authorize()


def oauth_test():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # creds = credentials
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists("token.json"):
    #   creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #   if creds and creds.expired and creds.refresh_token:
    #     creds.refresh(Request())
    #   else:
    #     flow = InstalledAppFlow.from_client_secrets_file(
    #         "credentials.json", SCOPES
    #     )
    #     creds = flow.run_local_server(port=0)
    #   # Save the credentials for the next run
    #   with open("token.json", "w") as token:
    #     token.write(creds.to_json())


# MyBusinessAccount, flags = sample_tools.init([],
#                                                  "mybusinessaccountmanagement",
#                                                  "v1", __doc__, __file__,
#                                                  scope="https://www.googleapis.com/auth/business.manage"
#                                                  )
#
# request = MyBusinessAccount.accounts().list(filter='type=LOCATION_GROUP', pageToken="")
# response = request.execute()
# print(response)


    scopes = ["https://www.googleapis.com/auth/datastudio"]
    # scopes = ["https://www.googleapis.com/auth/cloud-platform"]

    # url = f"https://accounts.google.com/o/oauth2/v2/auth?scope=https://www.googleapis.com/auth/userinfo.profile&access_type=offline&include_granted_scopes=true&response_type=code&state=state_parameter_passthrough_value&redirect_uri=https://localhost&client_id=42418434834-vuu7uikj67nvara22e4afvslniu8slul.apps.googleusercontent.com"
    # permissions = requests.get(url)
    # permissions.text


    flow = Flow.from_client_secrets_file(
        "client_secret_sandbox_oauth2_web_test.json",
        scopes=scopes,
        redirect_uri="http://localhost:5000"
    )
    # auth_url, __ = flow.authorization_url(access_type='offline',include_granted_scopes='true',prompt='consent')
    auth_url, __ = flow.authorization_url()
    print('Please go to this URL: {}'.format(auth_url))
    # The user will get an authorization code. This code is used to get the
    # access token.
    code = input('Enter the authorization code: ')
    token = flow.fetch_token(code=code)
    print(token)
    access_token = token["access_token"]
    print(access_token)

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    url = f"https://datastudio.googleapis.com/v1/assets:search?assetTypes=REPORT"
    permissions = requests.get(url, headers=headers)
    print(permissions.text)

    # Call the Gmail API
    # service = build("gmail", "v1")
    # # results = service.users().labels().list().execute()
    # # labels = results.get("labels", [])
    # query = "is:unread"
    # results = service.users().messages().list(userId="me", q=query).execute()
    # print(results)

def service_account_test():
    scopes = ["https://www.googleapis.com/auth/datastudio"]

    credential = service_account.Credentials.from_service_account_file("random-hello-1245721-7758d81e95f1.json", scopes=scopes)

    delegated_credentials = credential.with_subject('mfgwsdata@bu.microfusion.tw')

    # delegated_credentials = credential.with_subject('admin@bu.microfusion.tw')

    delegated_credentials.refresh(Request())

    access_token = delegated_credentials.token


    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    url = f"https://datastudio.googleapis.com/v1/assets:search?assetTypes=REPORT"
    permissions = requests.get(url, headers=headers)
    print(permissions.text)

    assetName = "1ba98210-7846-4a37-adc3-00eb1ea48e8c"
    url = f"https://datastudio.googleapis.com/v1/assets/{assetName}/permissions:addMembers"
    body = {
        "role": "VIEWER",
        "members": [
            "user:steven.fanchiang@nextlink.com.tw"
        ]
    }
    permissions = requests.post(url, headers=headers, json=body)
    print(permissions)

if __name__ == "__main__":
    oauth_test()
    # service_account_test()