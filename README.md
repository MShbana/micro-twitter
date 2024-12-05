# Micro-Twitter Project

A Django-based micro social media application with Django, DRF, PostgreSQL, Redis, and Celery.

## Setup & Installation

### Prerequisites
- Docker.
- Docker Compose.

### Steps to Set Up Locally

1. **Clone the repository**:
    ```
    git clone git@github.com:MShbana/micro-twitter.git
    cd micro-twitter
    ```

2. **In the project's root directory, copy server_variables.env.example as server_variables.env**:

    ```
    cp server_variables.env.example server_variables.env
    ```

    - Replace `SECRET_KEY` with a secure key. The rest of the values can be kept as is for local development.
    - *Important Note*: In real projects, server_variables.env.example will contain placeholders for the values.

3. **Build and start the containers**:

    `docker compose up -d --build`

4. **Run migrations**:

    `docker compose exec server python manage.py migrate`

### Creating SuperUser:
- To create a superuser, to access the Django Admin Dashboard: `docker-compose exec server python manage.py createsuperuser`.

### Accessing the Django Admin Dashboard:
- You can access the dashboard through: `"http://localhost:8000/admin"`.

### Running Tests:
- To run tests:`docker-compose exec server python manage.py test`

### Generating a Coverage Report:
- To create Covarege Report: `docker compose exec server coverage report -m`

### API Documentation:
- `http://localhost:8000/api/docs/redoc/`
- `http://localhost:8000/api/docs/swagger/`

### API Testing:
- A postman collection with the name `MicroTwitterByMohamedShabana.json` was shared via the email.
