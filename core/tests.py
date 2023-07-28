from django.test import TestCase
from core.models import CustomerLog
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.exceptions import ValidationError
from core.serializers import CustomerPayloadSerializer


class CustomerLogModelTest(TestCase):

    def test_customer_log_creation(self):
        log = CustomerLog.objects.create(customer_id="12345", error_msg="Some error")
        self.assertEqual(log.customer_id, "12345")
        self.assertEqual(log.error_msg, "Some error")


class PackDataViewSetTest(APITestCase):

    def test_create_without_customer_id(self):
        url = reverse('core:pack-list')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Customer ID not provided")

    def test_create_with_valid_customer_id(self):
        url = reverse('core:pack-list')
        response = self.client.post(url, {"customer_id": "101"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("pack1" in response.data)
        self.assertTrue("pack2" in response.data)


class CustomerPayloadSerializerTest(TestCase):

    def test_valid_data(self):
        valid_data = {"customer_id": "12345"}
        serializer = CustomerPayloadSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_data_missing_customer_id(self):
        invalid_data = {}
        serializer = CustomerPayloadSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
