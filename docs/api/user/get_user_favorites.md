# Update Booking

**Endpoint:** `PUT /api/v1/users/me/favorites`
**Description:** This endpoint allows a suer to retrieve their favorite products.
**Content-Type:** `application/json`



## Headers

| Name            | Required | Description                      |
|-----------------|----------|----------------------------------|
| Authorization   | Yes      | Bearer access token              |


## Response

### Success Response
- **Status Code:** `200 OK`
```json
{
    "status": "success",
    "message": "user favorites retrieved successfully",

}
```

### Error Response

#### Unauthorized

- **Status Code:** `401 Unauthorized`
```json
{
  "detail": "Could not validate credentials"
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
- **Status Code:** `500 Internal Server Error`
```json
{
  "detail": "An error occurred while retrieving user favorites"
}

```
