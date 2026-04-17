# API Documentation

## Endpoints

### GET /api/example

- **Description**: Retrieve example data.
- **Responses**:
  - `200 OK`: Returns a list of examples.
  - `404 Not Found`: If no examples are found.

### POST /api/example

- **Description**: Create a new example.
- **Request Body**:
  - `name`: String, required.
  - `value`: Number, required.
- **Responses**:
  - `201 Created`: Returns the created example.
  - `400 Bad Request`: If required fields are missing.

## Error Codes

- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error
