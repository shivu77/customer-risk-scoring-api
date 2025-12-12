# API Documentation

## Base URL
`http://127.0.0.1:8000`

## Schemas

### CustomerCreate
```
{
  "name": "string (min length 2)",
  "age": "int (18-80)",
  "income": "float (>=0)",
  "activity_score": "int (0-100)"
}
```

### CustomerResponse
```
{
  "id": "int",
  "name": "string",
  "age": "int",
  "income": "float",
  "activity_score": "int",
  "created_at": "ISO datetime"
}
```

### RiskScoreCreate
```
{
  "customer_id": "int (>0)",
  "age": "int (18-80)",
  "income": "float (>=0)",
  "activity_score": "int (0-100)"
}
```

### RiskScoreResponse
```
{
  "id": "int",
  "customer_id": "int",
  "final_score": "int",
  "explanation": "string",
  "created_at": "ISO datetime"
}
```

## Endpoints

### POST /customer/add
- Request
```
curl -X POST http://127.0.0.1:8000/customer/add \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Rahul",
    "age":28,
    "income":45000,
    "activity_score":62
  }'
```
- Success Response
```
{
  "id": 1,
  "name": "Rahul",
  "age": 28,
  "income": 45000.0,
  "activity_score": 62,
  "created_at": "2025-12-12T10:00:00Z"
}
```

### GET /customer/{id}
- Request
```
curl http://127.0.0.1:8000/customer/1
```
- Not Found
```
{
  "status": "error",
  "detail": "Customer not found"
}
```

### POST /risk/score
- Request
```
curl -X POST http://127.0.0.1:8000/risk/score \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "age": 28,
    "income": 45000,
    "activity_score": 62
  }'
```
- Success Response
```
{
  "id": 1,
  "customer_id": 1,
  "final_score": 40,
  "explanation": "Age contributed 10 points (moderate risk). Income added 15 points (low income). Activity score added 15 points (moderate activity). Final score = 40.",
  "created_at": "2025-12-12T10:02:00Z"
}
```

### GET /risk/{customer_id}
- Request
```
curl http://127.0.0.1:8000/risk/1
```
- Success Response
```
[
  {
    "id": 1,
    "customer_id": 1,
    "final_score": 40,
    "explanation": "Age contributed 10 points (moderate risk). Income added 15 points (low income). Activity score added 15 points (moderate activity). Final score = 40.",
    "created_at": "2025-12-12T10:02:00Z"
  }
]
```

## Error Codes
- 404: `{"status":"error","detail":"Customer not found"}`
- 422: `{"status":"validation_error","errors":[...]}` (input validation)
- 500: `{"status":"error","detail":"Internal server error"}`

