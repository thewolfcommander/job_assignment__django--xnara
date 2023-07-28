# Django API 


# Project development plan

| Section | Overview | Actionable Steps |
| --- | --- | --- |
| Initialization | Set up the base Django project. | 1\. Create new Django project.<br> 2. Navigate to project directory.<br> 3. Start a new Django app. |
| Package Installation | Install necessary libraries. | 1\. Install Django Rest Framework, Swagger for DRF, and `requests`. |
| App Configuration | Add necessary configurations for app. | 1\. Update `INSTALLED_APPS` in `settings.py`.<br> 2. Add necessary configurations for `REST_FRAMEWORK`. |
| Model Development | Create models for logging customer ID and errors. | 1\. Define the logging model `CustomerLog`. |
| API Development | Develop the main API functionality. | 1\. Define serializer for input payload.<br> 2. Create viewset for API that fetches pack data, combines it and logs any errors. |
| Swagger Integration | Set up Swagger for API documentation. | 1\. Configure Swagger/OpenAPI in `urls.py`.<br> 2. Add path for Swagger UI. |
| Exception & Logging | Ensure robust error handling and logging. | 1\. Directly log customer ID and errors in the view method. |
| Testing & Review | Test API and review for any issues. | 1\. Review code structure and logic.<br> 2. Run database migrations.<br> 3. Start the server and test API using Postman/Swagger. |


# Sample API Response

![Alt text](image.png)