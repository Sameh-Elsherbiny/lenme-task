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
    git clone <repository-url>
    cd <repository-directory>
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
