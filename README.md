# Lenme Task

## Project README

### Configuration Details

#### Prerequisites
- Python 3.8+
- Django 3.2+
- Django REST Framework
- Django Celery Beat
- Simple JWT
- DRF Spectacular

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Sameh-Elsherbiny/lenme-task.git
    cd lenme
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```sh
    python manage.py migrate
    ```

5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```
7. Install Redis:
    ```sh
    sudo apt-get update
    sudo apt-get install redis-server
    sudo systemctl enable redis-server.service
    ```

### Running Celery

1. Start the Celery worker:
    ```sh
    celery -A <your_project_name> worker --loglevel=info
    ```

2. Start the Celery Beat scheduler:
    ```sh
    celery -A <your_project_name> beat --loglevel=info
    ```

### Endpoints and Models

#### Endpoints

The project includes the following endpoints:

**Authentication:**
- `POST /api/token/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token

**Core:**
- `GET /core/`: Core app endpoints

**Loan:**
- `POST /loan/submitofferview/`: Submit a loan offer

#### Swagger Documentation

You can view the API documentation using Swagger by navigating to `/swagger/` in your browser.

### Models

#### Core Models

**User:**
- Custom user model with fields like email, password, etc.

**Account:**
- Represents user accounts with fields like balance, user, etc.

#### Loan Models

**Loan:**
- Represents a loan with fields like amount, interest_rate, borrower, etc.

**Offer:**
- Represents a loan offer with fields like amount, lender, loan, etc.

### Sample Code

#### Serializer Example

```python
from django.utils.translation import gettext as _
from rest_framework import serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError(_("Name must contain only letters."))
        return value
```

Test Example
```
def test_submit_offer_insufficient_balance(self):
    # Reduce lender's balance to below loan amount
    self.lender_account.balance = 1000
    self.lender_account.save()

    # Log in as the lender
    response = self.client.post('/api/token/', {'email': 'lender@email.com', 'password': 'testpassword'})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    token = response.data['access']
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    # Submit the loan offer
    response = self.client.post('/loan/submitofferview/', self.offer_data)

    # Verify the response
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('Insufficient balance', response.data['non_field_errors'][0])

```

end test

Database Schema
Core Models
User

id: Primary Key
email: Email Field
password: CharField
Account

id: Primary Key
balance: DecimalField
user: ForeignKey to User
Loan Models
Loan

id: Primary Key
amount: DecimalField
interest_rate: DecimalField
borrower: ForeignKey to User
Offer

id: Primary Key
amount: DecimalField
lender: ForeignKey to User
loan: ForeignKey to Loan

