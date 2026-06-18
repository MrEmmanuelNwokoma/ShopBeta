# Set New Password

## Endpoint

`POST /api/v1/auth/set-new-password`

## Description

This endpoint updates the user’s password.

## Request

This request should be made with `Content-Type: application/json` and include the following parameters:

### Form Data Parameters

| Name        | Type   | Required | Description                                                                         |
| ----------- | ------ | -------- | ----------------------------------------------------------------------------------- |
| `new_password`  | string | Yes      | The password of the user.                                                           |


## Response

### Success Response

-  **Status Code:** `200 OK`
- **Body:** A JSON object containing the following details:

```json
{
  "status": "success",
  "message": "Password updated successfully"
}
```

### Error


#### Invalid or Expired Token

- **Status Code:** `400 Bad Request`
```json
{
  "detail": "Invalid or expired reset token"
}
```

#### Password Mismatch

- ****Status Code:** `400 Bad Request`
```json
{
  "detail": "Passwords do not match"
}
```

#### Validation Error
- **Status Code:** `422 Unprocessable Entity`

```json
{
  "detail": "Invalid input data"
}
```
