# 🚀 Quick Start Guide - Employee Management System

## 5-Minute Setup

### Step 1: Database Setup (2 minutes)
```bash
mysql -u root -p < database.sql
```
**Password:** Enter your MySQL root password

### Step 2: Install Dependencies (2 minutes)
```bash
pip install -r requirements.txt
```

### Step 3: Update Database Credentials
Edit `app.py` line 10-15:
```python
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'  # ← Change this
app.config['MYSQL_DB'] = 'employee_management'
```

### Step 4: Run the Application (1 minute)
```bash
python app.py
```

✅ **Done!** Open: http://localhost:5000

---

## 🔓 Test Login

Create your own account:
1. Click "Register"
2. Enter email and password
3. Click "Register"
4. Login with your credentials

**OR** Test with existing data:
- Employees are pre-populated in database
- Create any new account to access them

---

## 📱 Default Dashboard Features

```
✓ Dashboard - View analytics and statistics
✓ Employees - CRUD operations
✓ Search - Find by name, email, position
✓ Filter - Department & Status filters
✓ Export - Download as CSV
✓ Responsive - Works on mobile too
```

---

## ⚡ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Ctrl+Shift+C | Open Chrome DevTools |
| F5 | Refresh page |
| Ctrl+K | Focus search |

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| MySQL connection error | Check MySQL is running, verify credentials |
| Port 5000 in use | `lsof -i :5000` or use different port |
| Module not found | Run `pip install -r requirements.txt` |
| Can't login | Try registering a new account first |

---

## 📂 Project Structure

```
.
├── app.py                 # Flask backend
├── index.html            # Frontend (GUI)
├── database.sql          # Database schema
├── requirements.txt      # Python dependencies
├── README.md             # Full documentation
└── .env.example          # Configuration template
```

---

## 🎯 Next Steps

1. ✅ Application is running
2. 📊 Explore Dashboard
3. 👥 Add some employees
4. 🔍 Try search & filters
5. 📥 Export to CSV
6. 🎨 Customize colors (if needed)

---

## 💡 Pro Tips

```javascript
// Access API directly from console:
const token = localStorage.getItem('token');
fetch('http://localhost:5000/api/employees', {
  headers: {'Authorization': `Bearer ${token}`}
}).then(r => r.json()).then(console.log)
```

---

## 🆘 Need Help?

1. Check README.md for detailed guide
2. Review browser console (F12) for errors
3. Check Flask terminal for backend errors
4. Verify MySQL is running: `mysql -u root -p`

---

**Happy coding! 🎉**
