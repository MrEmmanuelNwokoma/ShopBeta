# Register User

## Endpoint: `POST /api/v1/auth/`


# Register Guest User

## Endpoint

`POST /api/v1/auth/`

---

## Description

This endpoint handles user registration using the local authentication strategy.
It validates user input, ensures password confirmation matches, creates a new
user account,persists the user data in the database and logs the activity for that user.

---

## Request

The request should be made with `Content-Type: application/json` and include the following parameters:

---

### Request Body Parameters

| Parameter          | Type     | Required | Description                                  |Example/Notes          |
|--------------------|----------|----------|----------------------------------------------|-----------------------|
| `name`       | string   | Yes      | The name of the user                         |`"user"`               |
| `email`            | Emailstr | Yes      | The email of the user                        |`"user@gmail.com"`     |
| `password`         | string   | Yes      | The password of the user                     |`"strongpassword"` |



### Example Request Body

```json
{
  "status": "success",
  "message": "Guest user registered successfully",
  "name": "John",
  "email": "John@gmail.com",
  "password": "strongpassword"
}
```
## Response

### Success Response

- **Status Code:** `200 OK`
- **Body:** A JSON object containing the newly created user details:

```json
{
  "id": "string",
  "name": "string",
  "phone_number": "string",
  "location": "string",
  "is_active": true
}
```

### Error Response


#### User Already Exists Error
- **Status Code**: `409 Conflict`

```json
{
  "detail": "User already exists"
}
```

#### Validation Error
- **Status Code**: `422 Unprocessed Entity`
```json
{
  "detail": "Invalid input data"
}
```
#### Internal Server Error
- **Status Code**: `500 Internal Server Error`
```json
{
  "detail": "An unexpected error occured"
}
```
