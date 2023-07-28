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


logger = logging.getLogger(__name__)


def get_traceback_in_json() -> str:
    """
    Capture current exception, get its traceback and return in JSON format.
    """
    tb_list = traceback.format_exception(*sys.exc_info())
    tb_string = ''.join(tb_list)
    
    # Creating a dictionary for the traceback
    tb_dict = {
        "error": str(sys.exc_info()[1]),
        "traceback": tb_string
    }

    return json.dumps(tb_dict, indent=4)


def make_customer_log(customer_log, message) -> CustomerLog:
    customer_log.error_msg = message
    customer_log.save()

    return customer_log


class PackDataViewSet(ModelViewSet):
    serializer_class = CustomerPayloadSerializer
    queryset = CustomerLog.objects.all()

    @staticmethod
    def make_pack_request(pack_url: str, customer_id: str, customer_log: CustomerLog) -> list:  # noqa: E501
        """
        docstring
        """
        try:
            pack = requests.get(pack_url + f'?customer_id={customer_id}').json()
            if len(pack) == 0:
                make_customer_log(customer_log, f'Invalid Customer ID for the Database --- {customer_id}')  # noqa: E501
                return []

            parsed_pack = [f"{item['ingrediet']} {item['quantity']}{item['unit']}" for item in pack[0]['pack_data']]  # noqa: E501

            return parsed_pack
        except Exception:
            make_customer_log(customer_log, get_traceback_in_json())
            logger.debug(f"\nATTENTION 001 -----\n\n {get_traceback_in_json()}")
            return None

    def create(self, request, *args, **kwargs):
        # Log customer_id
        customer_id = request.data.get("customer_id")
        log_msg = 'Failed to fetch data'

        if not customer_id:
            return Response({
                'error': 'Customer ID not provided',
                'status':status.HTTP_400_BAD_REQUEST,
            })

        try:
            customer_log = CustomerLog.objects.create(customer_id=customer_id)
        except Exception:
            # Log the error
            make_customer_log(customer_log, get_traceback_in_json())
            logger.debug(f"\nATTENTION 002 -----\n\n {get_traceback_in_json()}")
            return Response({"error": log_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # noqa: E501

        # Fetch pack1 and pack2 data
        pack1_data = self.make_pack_request(config('PACK_1_API'), customer_id, customer_log)  # noqa: E501
        pack2_data = self.make_pack_request(config('PACK_1_API'), customer_id, customer_log)  # noqa: E501

        if not pack1_data or not pack2_data:
            logger.debug(f"\nATTENTION 003 -----\n\n {log_msg}")
            return Response({"error": log_msg}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # noqa: E501

        return Response({
            'id': customer_log.id,
            'customer_id': customer_log.customer_id,
            'pack1': pack1_data,
            'pack2': pack2_data,
        })
