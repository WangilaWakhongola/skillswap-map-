# SkillSwap-Map API Documentation

## Base URL
- Development: `http://localhost:8000/api`
- Production: `https://api.skillswap-map.com/api`

## Authentication

All endpoints (except auth and public endpoints) require JWT token in the header:

```
Authorization: Bearer <your_jwt_token>
```

### Get JWT Token

**Endpoint:** `POST /auth/login/`

**Request:**
```json
{
  "username": "john_doe",
  "password": "password123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Register New User

**Endpoint:** `POST /auth/register/`

**Request:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123",
  "password2": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

## User Endpoints

### List Users

**Endpoint:** `GET /users/`

**Query Parameters:**
- `search`: Search by name or username
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)
- `ordering`: Sort field (e.g., `-rating`, `username`)

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "bio": "I love teaching programming",
      "avatar": "https://...",
      "rating": 4.8,
      "total_reviews": 12,
      "total_exchanges": 23,
      "latitude": 40.7128,
      "longitude": -74.0060,
      "city": "New York",
      "country": "USA"
    }
  ]
}
```

### Get User Profile

**Endpoint:** `GET /users/{id}/`

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "I love teaching programming",
  "avatar": "https://...",
  "rating": 4.8,
  "total_reviews": 12,
  "total_exchanges": 23,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "city": "New York",
  "country": "USA",
  "skills": [...],
  "followers_count": 45,
  "following_count": 32
}
```

### Update User Profile

**Endpoint:** `PUT /users/{id}/`

**Request:**
```json
{
  "bio": "Updated bio",
  "city": "San Francisco",
  "country": "USA",
  "avatar": "<binary_data>"
}
```

### Get User's Skills

**Endpoint:** `GET /users/{id}/skills/`

**Response:**
```json
{
  "count": 5,
  "results": [...]
}
```

---

## Skill Endpoints

### List Skills

**Endpoint:** `GET /skills/`

**Query Parameters:**
- `category`: Filter by category ID
- `skill_type`: Filter by type (offer/request)
- `search`: Search by title or description
- `expertise_level`: Filter by level
- `available_online`: Boolean (true/false)
- `latitude`: User latitude (for distance filtering)
- `longitude`: User longitude
- `max_distance_km`: Maximum distance
- `ordering`: Sort field (e.g., `-rating`, `created_at`)

**Response:**
```json
{
  "count": 150,
  "results": [
    {
      "id": 1,
      "user": {
        "id": 1,
        "username": "john_doe",
        "avatar": "https://..."
      },
      "category": "Programming",
      "title": "Learn Python Basics",
      "description": "I can teach you Python fundamentals",
      "skill_type": "offer",
      "expertise_level": "expert",
      "exchange_type": "barter",
      "price_per_hour": null,
      "image": "https://...",
      "available_online": true,
      "average_rating": 4.9,
      "total_exchanges": 15,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Create Skill

**Endpoint:** `POST /skills/`

**Request:**
```json
{
  "category": 1,
  "title": "Learn Python Basics",
  "description": "I can teach you Python fundamentals",
  "skill_type": "offer",
  "expertise_level": "expert",
  "experience_years": 5,
  "exchange_type": "barter",
  "available_online": true,
  "available_in_person": true,
  "max_distance_km": 50,
  "start_time": "08:00:00",
  "end_time": "20:00:00"
}
```

### Get Skill Details

**Endpoint:** `GET /skills/{id}/`

### Update Skill

**Endpoint:** `PUT /skills/{id}/`

### Delete Skill

**Endpoint:** `DELETE /skills/{id}/`

### Like/Unlike Skill

**Endpoint:** `POST /skills/{id}/like/`

**Response:**
```json
{
  "liked": true,
  "likes_count": 45
}
```

---

## Exchange Endpoints

### List Exchanges

**Endpoint:** `GET /exchanges/`

**Query Parameters:**
- `status`: Filter by status (proposed/accepted/in_progress/completed)
- `search`: Search by title

**Response:**
```json
{
  "count": 25,
  "results": [
    {
      "id": 1,
      "initiator": {
        "id": 1,
        "username": "john_doe"
      },
      "recipient": {
        "id": 2,
        "username": "jane_smith"
      },
      "initiator_skill": {
        "id": 1,
        "title": "Learn Python"
      },
      "recipient_skill": {
        "id": 5,
        "title": "Learn Spanish"
      },
      "status": "accepted",
      "title": "Exchange: Python for Spanish",
      "proposed_date": "2024-01-20T14:00:00Z",
      "confirmed_date": "2024-01-18T10:00:00Z",
      "exchange_location": "Coffee Shop",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Create Exchange Proposal

**Endpoint:** `POST /exchanges/`

**Request:**
```json
{
  "recipient": 2,
  "initiator_skill": 1,
  "recipient_skill": 5,
  "title": "Exchange: Python for Spanish",
  "description": "Let's exchange skills",
  "proposed_date": "2024-01-20T14:00:00Z",
  "duration_hours": 1.0,
  "exchange_location": "Coffee Shop",
  "is_online": false
}
```

### Get Exchange Details

**Endpoint:** `GET /exchanges/{id}/`

### Update Exchange Status

**Endpoint:** `PUT /exchanges/{id}/`

**Request:**
```json
{
  "status": "accepted"
}
```

### Accept Exchange

**Endpoint:** `POST /exchanges/{id}/accept/`

### Complete Exchange

**Endpoint:** `POST /exchanges/{id}/complete/`

### Cancel Exchange

**Endpoint:** `POST /exchanges/{id}/cancel/`

---

## Messaging Endpoints

### List Conversations

**Endpoint:** `GET /messages/conversations/`

**Response:**
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "user1": {...},
      "user2": {...},
      "last_message": "See you tomorrow!",
      "user1_unread_count": 0,
      "user2_unread_count": 2,
      "updated_at": "2024-01-18T15:30:00Z"
    }
  ]
}
```

### Get Conversation Messages

**Endpoint:** `GET /messages/conversations/{conversation_id}/messages/`

**Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "sender": {...},
      "recipient": {...},
      "content": "Hi, are you available tomorrow?",
      "is_read": true,
      "created_at": "2024-01-18T14:00:00Z"
    }
  ]
}
```

### Send Message

**Endpoint:** `POST /messages/send/`

**Request:**
```json
{
  "recipient": 2,
  "content": "Hi, I'm interested in your skill",
  "exchange": 1
}
```

### Get Notifications

**Endpoint:** `GET /notifications/`

**Query Parameters:**
- `is_read`: Filter by read status (true/false)

**Response:**
```json
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "notification_type": "exchange_proposed",
      "title": "New Exchange Proposal",
      "message": "John Doe proposed an exchange",
      "is_read": false,
      "created_at": "2024-01-18T14:00:00Z"
    }
  ]
}
```

### Mark Notification as Read

**Endpoint:** `POST /notifications/{id}/mark_as_read/`

---

## Location Endpoints

### Update User Location

**Endpoint:** `PUT /location/update/`

**Request:**
```json
{
  "latitude": 40.7128,
  "longitude": -74.0060,
  "address": "123 Main St, New York, NY 10001"
}
```

### Find Nearby Skills

**Endpoint:** `GET /location/nearby/`

**Query Parameters:**
- `latitude`: User latitude
- `longitude`: User longitude
- `radius_km`: Search radius (default: 50)
- `category`: Filter by skill category

**Response:**
```json
{
  "count": 12,
  "results": [...]
}
```

---

## Skill Categories Endpoints

### List Categories

**Endpoint:** `GET /skill-categories/`

**Response:**
```json
{
  "count": 15,
  "results": [
    {
      "id": 1,
      "name": "Programming",
      "slug": "programming",
      "icon": "fa-code",
      "color": "#3B82F6"
    }
  ]
}
```

---

## Reviews Endpoints

### Create Review

**Endpoint:** `POST /reviews/`

**Request:**
```json
{
  "reviewed_user": 2,
  "exchange": 1,
  "rating": 5,
  "title": "Excellent teacher!",
  "comment": "John was very patient and explained everything clearly",
  "would_exchange_again": true,
  "communication_rating": 5,
  "reliability_rating": 5,
  "skill_quality_rating": 5
}
```

### Get User Reviews

**Endpoint:** `GET /users/{id}/reviews/`

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Error message",
  "status_code": 400,
  "details": {
    "field_name": ["Error message for this field"]
  }
}
```

### Common Status Codes

- `200`: Success
- `201`: Created
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Server Error

---

## Rate Limiting

API requests are rate-limited to prevent abuse:
- Anonymous users: 100 requests per hour
- Authenticated users: 1000 requests per hour

Rate limit headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642340400
```

---

## WebSocket Endpoints (Real-Time)

### Chat Messages
```
ws://localhost:8000/ws/chat/{exchange_id}/
```

### Notifications
```
ws://localhost:8000/ws/notifications/
```

---

## Pagination

List endpoints support pagination:

```json
{
  "count": 150,
  "next": "http://localhost:8000/api/skills/?page=2",
  "previous": null,
  "results": [...]
}
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

---

## Filtering & Searching

Example filter requests:

```bash
# Get active skills in programming category
GET /skills/?category=1&is_active=true

# Search for Python skills
GET /skills/?search=python

# Filter by expertise level
GET /skills/?expertise_level=expert

# Combine filters
GET /skills/?category=1&expertise_level=advanced&search=python
```

---

## Support

- 📧 API Support: api-support@skillswap-map.com
- 📖 Full Documentation: https://docs.skillswap-map.com
- 🐛 Report Issues: https://github.com/skillswap-map/api/issues
