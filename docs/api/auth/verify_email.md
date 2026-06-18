# Verify Verification Token
## Endpoint

`POST /api/v1/auth/verify-email`

## Description

This endpoint allows user to input the verification token sent via email to verify email.

## Request

This request should be made with `Content-Type: application/json` and include the following parameters:

### Form Data Parameters

| Parameter       | Type   | Required | Description                     |Example/Note
|---------------- |--------|----------|---------------------------------|-----------------------|
| `token`       | string |Yes       | Random token sent to user's email        | `"123456"` |

### Example Request Body

```json
{
  "status": "success",
  "message": "Verification successful",
  "token": "123456"
}
```


## Response

### Success Response

-  **Status Code:** `200 OK`
- **Body:** A JSON object containing the following details:

```json
{
  "message": "Verification successful"
}
```
### Error Response

#### Invalid token
- **Status Code**: `400 Bad Request`

```json
{
  "detail": "Invalid verification token"
}
```
