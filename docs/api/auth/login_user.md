# Login

## Endpoint

`POST /api/v1/auth/login`

## Description

This endpoint handles user authentication using different authentication strategies (local, Google, or Facebook)... and logs the activity for the user

## Request

The request should be made with `Content-Type: multipart/form-data` and include the following parameters:

### Form Data Parameters

| Name        | Type   | Required | Description                                                                         |
| ----------- | ------ | -------- | ----------------------------------------------------------------------------------- |
| `username`  | string | Yes      | The email or phone number of the user.                                                              |
| `password`  | string | Yes      | The password of the user.                                                           |


## Response

### Success Response

- **Status Code:** `200 OK`
- **Body:** A JSON object containing the following keys:

```json
{
  "status": "success",
  "message": "login successful",
  "access_token": "string",
  "refresh_token": "string",
  "token_type": "Bearer"
}
```

### Error
```json
{
  "detail": "Invalid credentials"
}
```