# Ecommerce API Documentation

This documentation provides an overview of the Ecommerce API built using Django Rest Framework. The API is designed to support various e-commerce operations, including product management, order processing, user authentication, and more.

## Table of Contents

- [Authentication](#authentication)
- [Users](#users)
- [Products](#products)
- [Orders](#orders)
- [Payments](#payments)
- [Categories](#categories)
- [Reviews](#reviews)

## Authentication

The Ecommerce API uses token-based authentication. To access protected endpoints, clients need to include a valid token in the `Authorization` header of their requests.

### Registration

**Endpoint:** `POST /api/auth/register/`

Register a new user by providing their email, username, and password.

Request:

```json
{
  "email": "user@example.com",
  "first_name": "exampleFirstName",
  "last_name": "exampleLastName",
  "password": "password123"
}
```

Response:

```json
{
  "email": "user@example.com",
  "first_name": "exampleFirstName",
  "last_name": "exampleLastName",
  "id": 1
}
```

### Login

**Endpoint:** `POST /api/auth/login/`

logs in a user by providing their email and password. Upon login success, the API will return an access token and user details.

Request:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "ciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJlbWFpbCI6Im",
  "user": {
    "email": "user@example.com",
    "first_name": "exampleFirstName",
    "last_name": "exampleLastName",
    "id": "2"
  }
}
```
