import google.api_core
from google.api_core import protobuf_helpers
from google.ads.googleads.errors import GoogleAdsException
from ga_runner import create_client, handleGoogleAdsException

def search_accounts(token, term, customer_id):
    try:
        client = create_client(token)
        ga_service = client.get_service("GoogleAdsService")
        if term.isdigit() and len(term) == 10:
            query = f''' SELECT customer_client.id, customer_client.resource_name, customer_client.descriptive_name FROM customer_client WHERE customer_client.id = '{term}' '''
        else:
            query = f''' SELECT customer_client.id, customer_client.resource_name, customer_client.descriptive_name FROM customer_client WHERE customer_client.descriptive_name LIKE '%{term}%' '''
        response = ga_service.search_stream(customer_id=customer_id, query=query)
        rows = []
        try:
            for batch in response:               
                for row in batch.results:
                    child_row = {}
                    child_row["text"] = f"{row.customer_client.descriptive_name} ({row.customer_client.id})"
                    child_row["id"] = row.customer_client.id
                    rows.append(child_row)
        except GoogleAdsException as ex:
            handleGoogleAdsException(ex)
        return rows
    except GoogleAdsException as ex:
        handleGoogleAdsException(ex)