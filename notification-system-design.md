# Notification System Design

---

## Stage 1: API Design

### Core Features
- Fetch notifications
- Create notification
- Delete notification

---

### Get Notifications
GET /api/notifications

Headers:
Authorization: Bearer <token>

Response:
{
  "notifications": [
    {
      "id": "1",
      "type": "Placement",
      "message": "You are shortlisted",
      "timestamp": "2026-01-01T10:00:00Z"
    }
  ]
}

---

### Create Notification
POST /api/notifications

Body:
{
  "userId": "101",
  "type": "Event",
  "message": "Hackathon tomorrow"
}

---

### Delete Notification
DELETE /api/notifications/{id}

---

### Real-Time Notifications
Use WebSockets to push notifications instantly to users.

---

## Stage 2: Database Design

### Choice
PostgreSQL (reliable and structured)

---

### Table: notifications
- id (UUID)
- user_id (string)
- type (Event, Result, Placement)
- message (text)
- timestamp (datetime)

---

### Problems at Scale
- Large dataset → slow queries  
- High read load  

---

### Solutions
- Index on user_id and timestamp  
- Pagination  
- Caching (Redis)  

---

### Sample Query
SELECT * FROM notifications
WHERE user_id = '101'
ORDER BY timestamp DESC;

---

## Stage 3: Query Optimization

### Given Query
SELECT * FROM notifications
WHERE student_id = 1042
ORDER BY timestamp DESC;

---

### Issues
- No index → full table scan  
- Sorting large data  

---

### Fix
Create index:
(student_id, timestamp DESC)

---

### Indexing Every Column?
Not good:
- Slows writes  
- Uses extra memory  

---

### Placement Query
SELECT DISTINCT user_id
FROM notifications
WHERE type = 'Placement'
AND timestamp >= NOW() - INTERVAL '7 days';

---

## Stage 4: Performance

### Problem
Fetching notifications on every page load overloads DB

---

### Solutions
- Redis caching  
- Pagination  
- Lazy loading  
- WebSockets (push updates)

---

### Tradeoffs
- Cache → fast but may be stale  
- WebSockets → real-time but complex  

---

## Stage 5: Scalable Notification Sending

### Problem in Given Approach
- Sequential (slow)  
- No retry mechanism  
- Failure breaks flow  
- Not scalable  

---

### Improved Approach
Use queue-based async processing

---

### Flow
Request → Queue → Worker → Email + DB + Push

---

### Pseudocode

function notify_all(student_ids, message):
    for id in student_ids:
        push_to_queue({id, message})

worker():
    while queue not empty:
        task = get_task()

        try:
            save_to_db(task)
            send_email(task)
            push_to_app(task)
        except:
            retry(task)

---

### Key Points
- Async processing  
- Retry mechanism  
- Independent operations  

---

## Stage 6: Priority Notifications

### Idea
Sort notifications based on:
- Type weight (Placement > Result > Event)
- Latest timestamp

---

### Code (Python)

import requests

URL = "http://20.207.122.201/evaluation-service/notifications"
TOKEN = "YOUR_TOKEN"

weights = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

def get_notifications():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    res = requests.get(URL, headers=headers)
    return res.json()["notifications"]

def get_top_notifications():
    data = get_notifications()

    sorted_data = sorted(
        data,
        key=lambda x: (weights[x["type"]], x["timestamp"]),
        reverse=True
    )

    top10 = sorted_data[:10]

    for n in top10:
        print(n)

if __name__ == "__main__":
    get_top_notifications()

---

### Screenshot Instructions
Run:
python your_file.py

Take screenshot when:
- Top 10 notifications are printed
- Full output visible in terminal

---

### Optimization
Maintain top 10 using a min-heap instead of sorting full list each time.