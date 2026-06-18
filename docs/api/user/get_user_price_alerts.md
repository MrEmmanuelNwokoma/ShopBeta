# Update Booking

**Endpoint:** `PUT /api/v1/users/me/price_alerts`
**Description:** This endpoint allows a user to retrieve their price_alerts.
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
    "message": "user price_alerts retrieved successfully",

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
  "detail": "An error occurred while retrieving user price_alerts"
}

```
