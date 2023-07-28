import requests
import traceback
import sys
import logging
import json
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import status

from decouple import config

from .models import CustomerLog
from .serializers import CustomerPayloadSerializer


# Getting the logger instance for the current module
logger = logging.getLogger(__name__)


def get_traceback_in_json() -> str:
    """
    Capture the current exception, extract its traceback and return in a 
    formatted JSON string.
    
    Returns:
        str: Formatted traceback in JSON.
    """
    tb_list = traceback.format_exception(*sys.exc_info())
    tb_string = ''.join(tb_list)
    
    # Constructing a dictionary for traceback details
    tb_dict = {
        "error": str(sys.exc_info()[1]),
        "traceback": tb_string
    }

    return json.dumps(tb_dict, indent=4)


def make_customer_log(customer_log, message) -> CustomerLog:
    """
    Log the error message for a given customer.

    Parameters:
    - customer_log (CustomerLog): The log entry for the customer.
    - message (str): The error message to log.

    Returns:
    - CustomerLog: The updated log entry with the error message.
    """
    customer_log.error_msg = message
    customer_log.save()

    return customer_log


class PackDataViewSet(ModelViewSet):
    serializer_class = CustomerPayloadSerializer
    queryset = CustomerLog.objects.all()

    @staticmethod
    def make_pack_request(pack_url: str, customer_id: str, customer_log: CustomerLog) -> list:  # noqa: E501
        """
        Make a request to the pack API and parse the response.

        Parameters:
        - pack_url (str): The URL of the pack API.
        - customer_id (str): The ID of the customer.
        - customer_log (CustomerLog): The log entry for the customer.

        Returns:
        - list: Parsed pack data or empty list if an error occurs.
        """
        try:
            pack = requests.get(pack_url + f'?customer_id={customer_id}').json()
            if len(pack) == 0:
                make_customer_log(customer_log, f'Invalid Customer ID for the Database --- {customer_id}')  # noqa: E501
                return []

            # Parsing the pack data from the API response
            parsed_pack = [f"{item['ingredient']} {item['quantity']}{item['unit']}" for item in pack[0]['pack_data']]  # noqa: E501
            return parsed_pack
        except Exception:
            # TODO: We can handle exceptions specfically here rather than capturing each

            make_customer_log(customer_log, get_traceback_in_json())
            logger.debug(f"\nATTENTION 001 -----\n\n {get_traceback_in_json()}")
            return None

    def create(self, request, *args, **kwargs):
        """
        Create a new customer log entry and fetch the respective packs for the customer.

        Accepts a request containing the customer ID and fetches pack data 
        for the customer.

        Parameters:
        - request (Request): The API request.

        Returns:
        - Response: API response containing pack data or error message.
        """
        # Extracting customer_id from request payload
        customer_id = request.data.get("customer_id")
        log_msg = 'Failed to fetch data'

        # Validating the provided customer_id
        if not customer_id:
            return Response({
                'error': 'Customer ID not provided',
                'status':status.HTTP_400_BAD_REQUEST,
            })

        try:
            # Logging the customer_id
            customer_log = CustomerLog.objects.create(customer_id=customer_id)
        except Exception:
            # TODO: Same specific exception handling can also be done here

            make_customer_log(customer_log, get_traceback_in_json())
            logger.debug(f"\nATTENTION 002 -----\n\n {get_traceback_in_json()}")
            return Response({"error": log_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # noqa: E501

        # Fetching pack data using the helper function
        pack1_data = self.make_pack_request(config('PACK_1_API'), customer_id, customer_log)  # noqa: E501
        pack2_data = self.make_pack_request(config('PACK_2_API'), customer_id, customer_log)  # noqa: E501

        if not pack1_data or not pack2_data:
            logger.debug(f"\nATTENTION 003 -----\n\n {log_msg}")
            return Response({"error": log_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # noqa: E501

        return Response({
            'id': customer_log.id,
            'customer_id': customer_log.customer_id,
            'pack1': pack1_data,
            'pack2': pack2_data,
        }, status=status.HTTP_200_OK)
