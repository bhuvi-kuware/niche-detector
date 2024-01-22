import argparse
import sys
import google.api_core
from google.api_core import protobuf_helpers
from google.ads.googleads.errors import GoogleAdsException
from ga_runner import create_client, handleGoogleAdsException

def get_resource_name(client_token , customer_id):
    create_client(client_token)