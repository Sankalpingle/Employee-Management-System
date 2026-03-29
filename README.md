# Employee Management System (EMS)

A complete web-based Employee Management System with modern GUI, user authentication, CRUD operations, analytics, and data export capabilities.

## 📋 Features

✅ **User Authentication** - Secure registration and login with JWT tokens
✅ **Employee CRUD Operations** - Create, read, update, and delete employees
✅ **Search & Filter** - Search by name, email, position; filter by department and status
✅ **Dashboard & Analytics** - Total employees, active count, average salary, department distribution, top earners
✅ **Data Export** - Export employee list to CSV
✅ **Modern UI** - Responsive design, dark theme, smooth animations
✅ **REST API** - Complete API documentation included

## 🛠️ Tech Stack

**Backend:** Python 3.8+, Flask, Flask-JWT-Extended, MySQL
**Frontend:** HTML5, CSS3, Vanilla JavaScript
**Database:** MySQL 5.7+

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.8+
- MySQL Server 5.7+
- pip

### Setup Steps

1. **Database Setup**
   ```bash
   mysql -u root -p < database.sql
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database**
   Edit `app.py` lines 10-15:
   ```python
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = 'your_password'  # ← Change this
   ```

4. **Run Application**
   ```bash
   python app.py
   ```

5. **Access Application**
   Open http://localhost:5000 in your browser

### Create Account & Login
- Click "Register" to create new account
- Enter email and password
- Login with your credentials

## 📁 Project Files

```
├── app.py                    # Flask backend (12KB)
├── index.html                # Complete frontend GUI (34KB)
├── database.sql              # MySQL schema + sample data (2.3KB)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── QUICK_START.md            # Quick setup guide
├── API_DOCUMENTATION.md      # Complete API reference
├── DEPLOYMENT_GUIDE.md       # Production deployment
└── .env.example              # Environment template
```

## 📊 Database Schema

**Users Table**
- id (Primary Key)
- email (Unique)
- password (Hashed)
- created_at

**Employees Table**
- id (Primary Key)
- name
- email (Unique)
- phone
- position
- department
- salary
- status (Active/Inactive)
- hire_date
- created_at, updated_at

Sample data includes 10 employees across IT, HR, Finance, Sales, and Marketing departments.

## 🔐 Security Features

- **Password Hashing** - Werkzeug secure hashing
- **JWT Authentication** - Token-based access control
- **Input Validation** - Server-side validation
- **SQL Injection Prevention** - Parameterized queries
- **Secure Headers** - HTTP security headers

## 🎯 Features in Detail

### Dashboard
- Total employees count
- Active employees count
- Average salary calculation
- Department distribution chart
- Top 5 highest paid employees

### Employees Management
- View all employees in responsive table
- Add new employee with form
- Edit existing employee details
- Delete employees
- Real-time search
- Filter by department
- Filter by status

### Data Export
- Export all employees to CSV
- Open in Excel or any spreadsheet
- Includes all employee information

## 📱 Responsive Design

- **Desktop** - Full feature set, optimized layout
- **Tablet** - Adjusted table, touch-friendly buttons
- **Mobile** - Single column, optimized for small screens

## 🔌 API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login and get token

### Employees
- `GET /api/employees` - Get all employees (with search/filter)
- `POST /api/employees` - Create employee
- `GET /api/employees/<id>` - Get single employee
- `PUT /api/employees/<id>` - Update employee
- `DELETE /api/employees/<id>` - Delete employee

### Analytics
- `GET /api/analytics/dashboard` - Get statistics

### Export
- `GET /api/employees/export/csv` - Export to CSV

See `API_DOCUMENTATION.md` for complete details.

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| MySQL connection error | Ensure MySQL is running, check credentials |
| Port 5000 in use | Use different port in app.py |
| Module not found | Run `pip install -r requirements.txt` |
| Can't login | Try registering a new account |

## 📝 Configuration

### Database Credentials
Edit in `app.py`:
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'employee_management'
```

### JWT Secret Key
```python
app.config['JWT_SECRET_KEY'] = 'change-this-in-production'
```

## 🎨 Customization

### Change Colors
Edit CSS variables in `index.html`:
```css
:root {
    --primary: #6366f1;
    --secondary: #ec4899;
    --success: #10b981;
    --danger: #ef4444;
}
```

### Add Departments
Edit filter options and database records.

### Modify Fields
Add new columns to employees table and update forms.

## 📈 Performance

- Database indexes on department, status, hire_date
- Optimized queries with filters
- Client-side search performance
- Responsive table design

## 🚀 Deployment

For production deployment, see `DEPLOYMENT_GUIDE.md` for:
- Heroku deployment
- AWS EC2 setup
- Docker containerization
- Security hardening
- SSL/HTTPS configuration
- Performance optimization

## 📚 Documentation

- `README.md` - Project overview (this file)
- `QUICK_START.md` - 5-minute setup guide
- `API_DOCUMENTATION.md` - Complete API reference
- `DEPLOYMENT_GUIDE.md` - Production deployment guide

## 💡 Tips

1. **Change JWT secret in production**
2. **Use strong MySQL password**
3. **Enable HTTPS**
4. **Regular database backups**
5. **Monitor error logs**
6. **Update dependencies regularly**

## 🤝 Support

For issues:
1. Check troubleshooting section
2. Verify prerequisites installed
3. Check MySQL is running
4. Review Flask/browser console for errors
5. Check API_DOCUMENTATION for endpoint details

## 📄 License

Free to use for educational and commercial purposes.

## 📊 File Sizes

- app.py: 12 KB
- index.html: 34 KB
- database.sql: 2.3 KB
- API_DOCUMENTATION.md: 6.7 KB
- DEPLOYMENT_GUIDE.md: 8.4 KB
- Others: < 3 KB each

**Total Project Size: ~70 KB** (extremely lightweight)

## ✨ Highlights

✓ **Zero Dependencies GUI** - Pure HTML/CSS/JavaScript (no framework)
✓ **Complete Solution** - Backend, frontend, database included
✓ **Production Ready** - Security, validation, error handling
✓ **Well Documented** - Multiple guides and API documentation
✓ **Easy to Deploy** - Multiple deployment options
✓ **Customizable** - Easy to modify and extend
✓ **Lightweight** - All files fit in ~70KB

## 🎓 Learning Value

Great for learning:
- Flask backend development
- RESTful API design
- JWT authentication
- MySQL database design
- Frontend form handling
- Data export functionality
- Responsive web design

---

**Version:** 1.0.0
**Status:** Production Ready ✅
**Last Updated:** 2024

Start building employee management solutions today! 🎉
