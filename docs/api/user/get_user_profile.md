# Get User Profile

## Endpoint
`GET /api/v1/users/me`

---

## Description
This endpoint returns the currently authenticated user based on the provided
Bearer access token.



## Authentication
This endpoint requires **OAuth2 Bearer Token authentication**.

Include the access token in the request header:

---

## Request Parameters

### Headers

| Name            | Required | Description                      |
|-----------------|----------|----------------------------------|
| Authorization   | Yes      | Bearer access token              |

---

## Response

### Success Response

- **Status Code:** `200 OK`
- **Body:** A JSON object containing the following details:

```json
{
  "status": "success",
  "message": "User's profile retrieved successfully",
  "data": {
    "id": "uuid",
    "name": "John Doe",
    "phone_number": "+2348012345678",
    "location": "Lagos",
    "role": "user",
    "is_verified": true,
    "created_at": "2026-01-01T12:00:00Z"
  }
}
```
### Error Response
#### Unauthorized

- **Status Code:** `401 Unauthorized`
```json
{
  "detail": "Could not validate token"
}
```

#### Token Expired or Invalid

- **Status Code:** `401 Unauthorized`

```json
{
  "detail": "Invalid or expired token"
}
```

#### User Not Found 
- **Status Code:** `404 Not Found`
```json
{
  "detail": "User not found"
}
```