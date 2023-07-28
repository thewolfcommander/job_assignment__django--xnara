from django.db import models


class CustomerLog(models.Model):
    customer_id = models.CharField(max_length=255)
    request_time = models.DateTimeField(auto_now_add=True)
    error_msg = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"Customer --- {self.customer_id} (Request time -- {self.request_time})"