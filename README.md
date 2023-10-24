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

Register a new user by providing their email, username, and password. Upon successful registration, the API will return a refresh and access token.

Request:

```json
{
  "email": "user@example.com",
  "first name": "exampleFirstName",
  "last name": "exampleLastName",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "",
  "refresh_token": ""
}
```
