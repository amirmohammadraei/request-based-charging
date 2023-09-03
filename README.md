# Request-Based Charging Platform

The Request-Based Charging Platform is a web application built with Python and Django that offers a pay-as-you-go payment model for users. Users are charged based on the number of requests they make within a given month. This README provides step-by-step instructions on setting up and running the project.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Project Setup](#project-setup)
  - [1. Prerequisites](#1-prerequisites)
  - [2. Clone the Repository](#2-clone-the-repository)
  - [3. Create a Virtual Environment](#3-create-a-virtual-environment)
  - [4. Install Dependencies](#4-install-dependencies)
  - [5. Database Configuration](#5-database-configuration)
  - [6. Apply Migrations](#6-apply-migrations)
- [Running the Development Server](#running-the-development-server)
- [API Endpoints](#api-endpoints)
- [Testing with Postman](#testing-with-postman)
- [Contributing](#contributing)
- [License](#license)

## Technologies Used

- Python
- Django
- Django REST framework
- PostgreSQL (database)
- Postman (for testing)
- Git (for version control)

## Project Setup

### 1. Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.x
- pip (Python package manager)
- PostgreSQL (with a user and database for the project)

### 2. Clone the Repository

Clone the project repository to your local machine:

```shell
git clone https://github.com/your-username/request-based-charging.git
```

### 3. Create a Virtual Environment

Navigate to the project directory and create a virtual environment:

```shell
cd request-based-charging
python -m venv venv
```

### 4. Install Dependencies

Activate the virtual environment and install project dependencies:

```shell
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
pip install -r requirements.txt
```

### 5. Database Configuration

Configure the database settings in the `settings.py` file:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your-database-name',
        'USER': 'your-database-username',
        'PASSWORD': 'your-database-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. Apply Migrations

Apply database migrations to create the necessary tables:

```shell
python manage.py makemigrations
python manage.py migrate
```

## Running the Development Server

Start the development server:

```shell
python manage.py runserver
```

The application should now be accessible at `http://127.0.0.1:8000/`.

## API Endpoints

1. **User Registration:** `POST /api/register/`
   - Register a new user with a unique username and email.

2. **User Login:** `POST /api/login/`
   - Authenticate and obtain an API token.

3. **Create Request:** `POST /api/create-request/`
   - Create a new request associated with the authenticated user.

4. **Get User Requests:** `GET /api/user-requests/`
   - Retrieve all requests made by the authenticated user.

5. **Current Month Cost:** `GET /api/current-month-cost/`
   - Get the total cost for the current month for the authenticated user.

## Testing with Postman

To test the API endpoints, you can use Postman. Import the provided Postman collection (`request-based-charging.postman_collection.json`) into Postman and use it to send requests to the API endpoints.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your fork.
5. Create a pull request to the main repository.
