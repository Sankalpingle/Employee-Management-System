# Employee Management System - API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication

All endpoints require JWT token in header (except `/register` and `/login`):

```javascript
headers: {
  'Authorization': 'Bearer YOUR_TOKEN_HERE'
}
```

---

## 🔐 Authentication Endpoints

### Register User
**POST** `/register`

Request:
```json
{
  "email": "user@company.com",
  "password": "securepassword123"
}
```

Response (201):
```json
{
  "message": "User registered successfully"
}
```

---

### Login
**POST** `/login`

Request:
```json
{
  "email": "user@company.com",
  "password": "securepassword123"
}
```

Response (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1
}
```

Store the `access_token` and use it for subsequent requests.

---

## 👥 Employee Endpoints

### Get All Employees (with filters)
**GET** `/employees?search=&department=IT&status=Active`

Query Parameters (all optional):
- `search` - Search by name, email, or position
- `department` - Filter by department
- `status` - Filter by status (Active/Inactive)

Response (200):
```json
[
  {
    "id": 1,
    "name": "Rajesh Kumar",
    "email": "rajesh@company.com",
    "phone": "9876543210",
    "position": "Senior Developer",
    "department": "IT",
    "salary": 85000,
    "status": "Active",
    "hire_date": "2022-01-15"
  }
]
```

Example with cURL:
```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:5000/api/employees?department=IT&status=Active"
```

Example with JavaScript:
```javascript
const response = await fetch(
  'http://localhost:5000/api/employees?department=IT',
  {
    headers: {'Authorization': `Bearer ${token}`}
  }
);
const employees = await response.json();
```

---

### Get Single Employee
**GET** `/employees/{id}`

Response (200):
```json
{
  "id": 1,
  "name": "Rajesh Kumar",
  "email": "rajesh@company.com",
  "phone": "9876543210",
  "position": "Senior Developer",
  "department": "IT",
  "salary": 85000,
  "status": "Active",
  "hire_date": "2022-01-15"
}
```

---

### Create Employee
**POST** `/employees`

Request:
```json
{
  "name": "New Employee",
  "email": "newemp@company.com",
  "phone": "9876543220",
  "position": "Developer",
  "department": "IT",
  "salary": 75000
}
```

Response (201):
```json
{
  "message": "Employee created successfully",
  "id": 11
}
```

Required fields:
- name (string)
- email (string, unique)
- phone (string)
- position (string)
- department (string)
- salary (number)

---

### Update Employee
**PUT** `/employees/{id}`

Request (send only fields to update):
```json
{
  "salary": 90000,
  "position": "Senior Developer",
  "status": "Active"
}
```

Response (200):
```json
{
  "message": "Employee updated successfully"
}
```

---

### Delete Employee
**DELETE** `/employees/{id}`

Response (200):
```json
{
  "message": "Employee deleted successfully"
}
```

---

## 📊 Analytics Endpoints

### Get Dashboard Statistics
**GET** `/analytics/dashboard`

Response (200):
```json
{
  "total_employees": 10,
  "active_employees": 9,
  "avg_salary": 78500.50,
  "departments": [
    {
      "name": "IT",
      "count": 4
    },
    {
      "name": "HR",
      "count": 1
    }
  ],
  "top_paid": [
    {
      "name": "Priya Singh",
      "position": "Product Manager",
      "salary": 95000
    }
  ]
}
```

---

## 📥 Export Endpoints

### Export to CSV
**GET** `/employees/export/csv`

Response: Binary CSV file download

---

## ✅ Health Check

**GET** `/health`

Response (200):
```json
{
  "status": "ok"
}
```

---

## 📋 Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Server Error |

---

## 🔍 Common API Calls

### Search for employees in IT department
```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:5000/api/employees?department=IT&search=developer"
```

### Create multiple employees
```javascript
const employees = [
  {name: "John", email: "john@company.com", ...},
  {name: "Jane", email: "jane@company.com", ...}
];

for (const emp of employees) {
  await fetch('http://localhost:5000/api/employees', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(emp)
  });
}
```

### Get statistics
```javascript
const stats = await fetch(
  'http://localhost:5000/api/analytics/dashboard',
  {headers: {'Authorization': `Bearer ${token}`}}
).then(r => r.json());

console.log(`Total: ${stats.total_employees}`);
console.log(`Average Salary: ₹${stats.avg_salary}`);
```

---

## 🚨 Error Responses

### Missing Authentication
```json
{
  "message": "Unauthorized"
}
```

### Duplicate Email
```json
{
  "message": "Email already exists"
}
```

### Not Found
```json
{
  "message": "Employee not found"
}
```

---

## 💡 Tips

1. **Token Management**: Store token in `localStorage` for persistence
2. **Error Handling**: Always check response status
3. **Search**: Search works with partial matches
4. **Filters**: Multiple filters work together (AND logic)
5. **Performance**: Use filters instead of loading all employees

---

## 🧪 Testing with Postman

1. **Create Collection**: "Employee Management"
2. **Set Base URL**: `http://localhost:5000/api`
3. **Register**: POST to `/register` with email/password
4. **Login**: POST to `/login` get the token
5. **Set Environment Variable**: `{{token}}` = response.access_token
6. **Use in Headers**: `Authorization: Bearer {{token}}`

---

## 📚 Full Example Workflow

```javascript
// 1. Register
const regRes = await fetch('http://localhost:5000/api/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'user@company.com',
    password: 'password123'
  })
});

// 2. Login
const loginRes = await fetch('http://localhost:5000/api/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'user@company.com',
    password: 'password123'
  })
});
const { access_token } = await loginRes.json();

// 3. Create Employee
const empRes = await fetch('http://localhost:5000/api/employees', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@company.com',
    phone: '9876543210',
    position: 'Developer',
    department: 'IT',
    salary: 75000
  })
});

// 4. Get Dashboard Stats
const statsRes = await fetch('http://localhost:5000/api/analytics/dashboard', {
  headers: {'Authorization': `Bearer ${access_token}`}
});
const stats = await statsRes.json();
console.log(stats);
```

---

**Last Updated:** 2024
**Version:** 1.0.0
