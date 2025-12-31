# API Documentation - Instagram Automation Pro

## Base URL
- Development: `http://localhost:8000`
- Production: `https://api.yourdomain.com`

## Authentication

All protected endpoints require JWT token in header:
```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Authentication Endpoints

#### POST /api/auth/login
User login
```json
Request:
{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "access_token": "jwt_token",
  "token_type": "bearer",
  "user_id": "user_id"
}
```

### Rules Management Endpoints

#### GET /api/rules
Get all automation rules
```json
Response:
{
  "rules": [
    {
      "id": "rule_id",
      "rule_name": "Lead Generation",
      "keywords": ["interested", "price", "buy"],
      "comment_reply": "Thanks for your interest!",
      "toggle": {
        "comment_only": false,
        "send_dm": true,
        "dm_message": "Hey, here's what you asked for..."
      },
      "is_active": true,
      "created_at": "2025-01-01T12:00:00Z"
    }
  ]
}
```

#### POST /api/rules
Create new automation rule
```json
Request:
{
  "rule_name": "Lead Generation",
  "keywords": ["interested", "price"],
  "comment_reply": "Thanks for your interest! 👇",
  "toggle": {
    "comment_only": false,
    "send_dm": true,
    "dm_message": "Check out our details..."
  },
  "is_active": true
}

Response:
{
  "id": "rule_id",
  "message": "Rule created successfully"
}
```

#### GET /api/rules/{rule_id}
Get specific rule
```json
Response:
{
  "id": "rule_id",
  "rule_name": "Lead Generation",
  "keywords": ["interested"],
  "comment_reply": "Thanks for your interest!",
  "toggle": {
    "comment_only": false,
    "send_dm": true,
    "dm_message": "Here's more info..."
  },
  "is_active": true,
  "created_at": "2025-01-01T12:00:00Z"
}
```

#### PUT /api/rules/{rule_id}
Update rule (including toggles)
```json
Request:
{
  "rule_name": "Updated Rule Name",
  "toggle": {
    "comment_only": true,
    "send_dm": false
  }
}

Response:
{
  "id": "rule_id",
  "message": "Rule updated successfully"
}
```

#### DELETE /api/rules/{rule_id}
Delete rule
```json
Response:
{
  "message": "Rule deleted successfully"
}
```

## Toggle Feature Logic

### How Toggles Work

Every rule has two toggles:

**1. comment_only** (boolean)
- `true` = Only reply to comment, don't send DM
- `false` = Proceed with DM check

**2. send_dm** (boolean)
- `true` = Send DM to commenter
- `false` = Don't send DM

### Processing Logic

```
Comment received
    ↓
Always reply to comment ✓
    ↓
Check: comment_only = true?
    ├─ YES → Stop (don't check send_dm)
    └─ NO → Continue
        ↓
    Check: send_dm = true?
        ├─ YES → Send DM ✓
        └─ NO → Stop
```