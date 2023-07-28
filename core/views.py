import requests
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import status

from decouple import config

from .models import CustomerLog
from .serializers import CustomerPayloadSerializer

class PackDataViewSet(ModelViewSet):
    serializer_class = CustomerPayloadSerializer

    def create(self, request, *args, **kwargs):
        # Log customer_id
        customer_id = request.data.get("customer_id")
        customer_log = CustomerLog.objects.create(customer_id=customer_id)

        try:
            # Fetch pack1 and pack2 data
            pack1 = requests.get(config('PACK_1_API')).json()
            pack2 = requests.get(config('PACK_2_API')).json()
            
            combined_data = [{"pack": f"{item['ingredient']} {item['quantity']}{item['unit']}"} for item in pack1 + pack2]  # noqa: E501

            return Response(combined_data)

        except Exception as e:
            # Log the error
            customer_log.error_msg=str(e)
            return Response({"error": "Failed to fetch data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # noqa: E501
