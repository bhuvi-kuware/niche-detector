import argparse
import sys
import google.api_core
from google.api_core import protobuf_helpers
from google.ads.googleads.errors import GoogleAdsException
from ga_runner import create_client, handleGoogleAdsException
from customers.get_resource_name import get_resource_name


def link_manager_to_client(client_token,manager_token, manager_customer_id,customer_id,parent_customer_client_id):
    manager_client = create_client(manager_token)
    result = False
    try: 
        # Before Extend an invitation to the client.
        customer_client_link_service = manager_client.get_service("CustomerClientLinkService")
        
        # Extend an invitation to the client while authenticating as the manager.
        client_link_operation = manager_client.get_type("CustomerClientLinkOperation")
        client_link = client_link_operation.create
        client_link.client_customer = customer_client_link_service.customer_path(customer_id)
        client_link.status = manager_client.enums.ManagerLinkStatusEnum.PENDING

        response = customer_client_link_service.mutate_customer_client_link(
            customer_id=manager_customer_id, operation=client_link_operation
        )
        resource_name = response.result.resource_name
        print("Resource Name")
        print(resource_name)
    except GoogleAdsException as ex:
        for error in ex.failure.errors:
            error_message = error.message
            if(error_message=="Client is already invited by this manager."):
                print("Client is already invited by this manager")
                return False
               ## resource_name = get_resource_name(customer_id)
            if(error_message=="Client is already managed in hierarchy."):
                print("Client is already managed in hierarchy")
                return True
        try:
             # Find the manager_link_id of the link we just created, so we can construct
            # the resource name for the link from the client side. Note that since we
            # are filtering by resource_name, a unique identifier, only one
            # customer_client_link resource will be returned in the response
            query = f'''
            SELECT
                customer_client_link.manager_link_id
            FROM
                customer_client_link
            WHERE
                customer_client_link.resource_name = "{resource_name}"'''

            ga_service = manager_client.get_service("GoogleAdsService")

            response = ga_service.search(
                customer_id=manager_customer_id, query=query
            )

            # Since the googleads_service.search method returns an iterator we need
            # to initialize an iteration in order to retrieve results, even though
            # we know the query will only return a single row.
            for row in response.results:
                manager_link_id = row.customer_client_link.manager_link_id
                print(manager_link_id)

        except GoogleAdsException as ex:
            print("Came in Error")
            handleGoogleAdsException(ex)
        try:
            # Accepting the invitation as a client that we have received from manager
            client = create_client(client_token,parent_customer_client_id)
            customer_manager_link_service = client.get_service(
                "CustomerManagerLinkService"
            )
            manager_link_operation = client.get_type("CustomerManagerLinkOperation")
            manager_link = manager_link_operation.update
            manager_link.resource_name = (
                customer_manager_link_service.customer_manager_link_path(
                    customer_id,
                    manager_customer_id,
                    manager_link_id,
                )
            )

            manager_link.status = client.enums.ManagerLinkStatusEnum.ACTIVE
            client.copy_from(
                manager_link_operation.update_mask,
                protobuf_helpers.field_mask(None, manager_link._pb),
            )

            response = customer_manager_link_service.mutate_customer_manager_link(customer_id=customer_id, operations=[manager_link_operation])
            print("Client accepted invitation with resource_name: " f'"{response.results[0].resource_name}"')
            result = True
            return result
        except GoogleAdsException as ex:
            print("Came in Error3")
            handleGoogleAdsException(ex)
    
