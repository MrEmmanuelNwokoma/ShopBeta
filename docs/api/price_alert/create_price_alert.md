# Create Favorite

## Endpoint: `POST /api/v1/favorites/`


---

## Description

This endpoint allows users to add a store's product to their favorites.

---

## Request

The request should be made with `Content-Type: application/json` and include the following parameters:

---
### Headers

| Name            | Required | Description                      |
|-----------------|----------|----------------------------------|
| Authorization   | Yes      | Bearer access token              |

### Request Body Parameters

| Parameter          | Type     | Required | Description                                  |Example/Notes          |
|--------------------|----------|----------|----------------------------------------------|-----------------------|
| `store_product_id`       | string   | Yes      | The id of the store_product                         |`"uuid1234"`               |
| `target_price`       | Decimal   | Yes      | The target price for the product                         |`"2500.00"`               |



### Example Request Body

```json
{
  "store_product_id": "uuid1234",
  "target_price": "2500.00"
}
```
## Response

### Success Response

- **Status Code:** `200 OK`
- **Body:** A JSON object containing the newly created price alert:

```json
{
  "status": "success",
  "message": "Price alert created successfully"
}
```

### Error Response


#### Alert Already Exists Error
- **Status Code**: `409 Conflict`

```json
{
  "detail": "Alert already exists"
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
