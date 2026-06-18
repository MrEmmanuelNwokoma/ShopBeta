# Update Booking

**Endpoint:** `PUT /api/v1/users`
**Description:** This endpoint allows a host to update a booking.
**Content-Type:** `application/json`


### Request Body Parameters

| Parameter               | Type   | Required | Description                                  |Example/Notes          |
|--------------------|--------|----------|----------------------------------------------|-----------------------|
| `first_name`       | string | Optional      | The first name of the user                   |`"Emmanuel"`           |
| `last_name`        | string | Optional      | The last name of the user                    |`"Nwokoma"`            |
| `phone_number`     | string | Optional      | The phone number of the user                 |`"09098765443"`        |
| `location`         | string | Optional       | The user’s location (derived from lat & lon) |

### Headers

| Name            | Required | Description                      |
|-----------------|----------|----------------------------------|
| Authorization   | Yes      | Bearer access token              |


## Response

### Success Response
- **Status Code:** `200 OK`
```json
{
    "status": "success",
    "message": "booking updated successfully",
    "user_data": {
      "first_name": "Emmanuel",
      "last_name": "Doe",
      "phonenumber": "0986544567",
      "location": "Abuja, Nigeria"
    }
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
  "detail": "An error occurred while updating user profile"
}

```
