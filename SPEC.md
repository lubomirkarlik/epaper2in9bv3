# EPaper29BV3 API Documentation

## Overview
The EPaper29BV3 is an advanced electronic paper display that provides low power consumption and high visibility.

## API Endpoints

### Get Display Status

**Endpoint:** `GET /api/display/status`

**Description:** Retrieves the current status of the display.

**Response:**
```json
{
  "status": "active",
  "brightness": 75
}
```

### Update Display Content

**Endpoint:** `POST /api/display/content`

**Description:** Updates the content displayed on the screen.

**Request Body:**
```json
{
  "content": "Hello World!"
}
```

**Response:**
```json
{
  "message": "Content updated successfully"
}
```

## Conclusion
This API allows for easy interaction with the EPaper29BV3 display, ensuring that content can be updated and monitored effectively.