# Request Verification Token

## Endpoint
`POST /api/v1/auth/resend-verification-token`

---

### Description
This endpoint allows user to request a verification token.  
A reset token is generated and sent to the user’s registered email.

---

## Request

**Content-Type:** `application/json`

## Form Data Parameters

| Name  | Type     | Required | Description                     |
|-------|----------|----------|---------------------------------|
| email | Emailstr | Yes      | Registered email address        |

---

## Example Request

```json
{
  "status": "success",
  "message": "Token sent successfully",
  "email": "user@example.com"
}
```

##  Response

### Success Response

-**Status Code:** `200 OK`
- **Body:** A JSON object containing the following keys:

```json
{
  "message": "Token sent successfully"
}
```

### Error Response

#### User Not Found

- **Status Code:** `404 Not Found`

```json
{
  "detail": "User not found"
}
```

#### Validation Error

- **Status Code:** `422 Unprocessable Entity`

```json
{
  "detail": "Invalid email format"
}
```

