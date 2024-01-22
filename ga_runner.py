from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from flask import Flask, redirect, session, request

REFRESH_ERROR = "INVALID REFRESH TOKEN"
def create_client(token,login_customer_id=0):
    try:
        credentials = {
            "developer_token": "CkoqdicTC0N7WVWdwDRw9A",
            "client_id": "380632208728-u3sci89kmmpshkp5c79hifpu850ga2i5.apps.googleusercontent.com",
            "client_secret": "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",
            "refresh_token": token,
            "use_proto_plus": "true"
            }
        if(login_customer_id!=0):
            credentials['login_customer_id'] = login_customer_id
        print(credentials)
        googleads_client = GoogleAdsClient.load_from_dict(credentials, version="v14")
        return googleads_client

    except: 
        raise ValueError(REFRESH_ERROR)

def handleGoogleAdsException(ex: GoogleAdsException):
    print(
        f'Request with ID "{ex.request_id}" failed with status '
        f'"{ex.error.code().name}" and includes the following errors:'
    )
    for error in ex.failure.errors:
        print(f'\tError with message "{error.message}".')
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f"\t\tOn field: {field_path_element.field_name}")