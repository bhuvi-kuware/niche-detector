import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from ga_runner import create_client, handleGoogleAdsException

def get_account_keywords(client_token,customer_id,login_customer_id):
    client = create_client(client_token,login_customer_id)
    ga_service = client.get_service("GoogleAdsService")
    query = """
       SELECT campaign.id, campaign.name , ad_group.id, ad_group.name,  ad_group_criterion.criterion_id ,  ad_group_criterion.keyword.text  , ad_group_criterion.keyword.match_type FROM keyword_view WHERE campaign.advertising_channel_type='SEARCH'  AND ad_group_criterion.status IN ('ENABLED','PAUSED')"""
    print(query)
    # Issues a search request using streaming.
    stream = ga_service.search_stream(customer_id=customer_id, query=query)
    
    accountKeywords = []
    for batch in stream:
        for row in batch.results:
            if(row.ad_group_criterion.keyword.text!=''):
                accountKeywords.append(row.ad_group_criterion.keyword.text)
    return accountKeywords