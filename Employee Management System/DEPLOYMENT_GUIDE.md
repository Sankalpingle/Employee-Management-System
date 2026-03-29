# 🚀 Deployment Guide - Employee Management System

## Production Checklist

- [ ] Update database credentials
- [ ] Change JWT secret key
- [ ] Enable HTTPS
- [ ] Set Flask debug mode to False
- [ ] Configure CORS properly
- [ ] Set up error logging
- [ ] Backup database
- [ ] Test all features
- [ ] Configure firewall
- [ ] Set up monitoring

---

## Deployment Options

### Option 1: Heroku Deployment

**Prerequisites:**
- Heroku account
- Heroku CLI installed
- GitHub repository

**Steps:**

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Add Heroku config:
```bash
heroku create your-app-name
heroku config:set JWT_SECRET_KEY=your-secret-key
heroku config:set MYSQL_HOST=your-mysql-host
heroku config:set MYSQL_USER=your-username
heroku config:set MYSQL_PASSWORD=your-password
heroku config:set MYSQL_DB=employee_management
```

3. Deploy:
```bash
git push heroku main
```

---

### Option 2: AWS EC2 Deployment

**Prerequisites:**
- AWS account
- EC2 instance running Ubuntu 20.04
- SSH access

**Steps:**

1. SSH into instance:
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

2. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv mysql-server
```

3. Clone repository:
```bash
git clone your-repo-url
cd employee-management
```

4. Setup virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

5. Configure MySQL:
```bash
sudo mysql -u root
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'strong_password';
mysql> FLUSH PRIVILEGES;
```

6. Run database setup:
```bash
mysql -u root -p employee_management < database.sql
```

7. Configure app.py with environment variables
```python
import os
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
```

8. Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

9. Setup Nginx reverse proxy:
```bash
sudo apt install nginx
# Configure /etc/nginx/sites-available/default
```

---

### Option 3: Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV FLASK_DEBUG=False

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      MYSQL_HOST: db
      MYSQL_USER: root
      MYSQL_PASSWORD: password
      MYSQL_DB: employee_management
    depends_on:
      - db

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: employee_management
    volumes:
      - ./database.sql:/docker-entrypoint-initdb.d/init.sql
      - dbdata:/var/lib/mysql

volumes:
  dbdata:
```

Run with:
```bash
docker-compose up -d
```

---

### Option 4: DigitalOcean App Platform

1. Create `app.yaml`:
```yaml
name: employee-management
services:
- name: api
  github:
    branch: main
    repo: your-repo
  http_port: 5000
  source_dir: ./
  envs:
  - key: MYSQL_HOST
    value: ${db.MYSQL_HOST}
  - key: MYSQL_USER
    value: root
  - key: JWT_SECRET_KEY
    scope: RUN_AND_BUILD_TIME
    value: ${JWT_SECRET_KEY}

databases:
- name: db
  engine: MYSQL
  version: "8"
```

2. Connect GitHub repository to DigitalOcean
3. Deploy from dashboard

---

## Environment Variables

Create `.env` file:
```env
# Flask
FLASK_ENV=production
FLASK_DEBUG=False

# Database
MYSQL_HOST=your-mysql-host
MYSQL_USER=your-username
MYSQL_PASSWORD=your-secure-password
MYSQL_DB=employee_management

# Security
JWT_SECRET_KEY=generate-a-random-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=2592000

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
```

Load in app.py:
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
```

---

## Security Hardening

### 1. HTTPS/SSL Setup

Using Let's Encrypt with Certbot:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

Nginx configuration:
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:5000;
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### 2. CORS Configuration

Update app.py:
```python
from flask_cors import CORS

CORS(app, origins=['https://yourdomain.com'])
```

### 3. Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    pass
```

### 4. CSRF Protection

```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
```

### 5. SQL Injection Prevention

Already using parameterized queries ✓

### 6. Authentication Security

```python
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
```

---

## Performance Optimization

### 1. Database Indexing

Already configured in database.sql ✓

### 2. Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/analytics/dashboard')
@cache.cached(timeout=3600)
def get_dashboard_analytics():
    pass
```

### 3. Pagination

```python
@app.route('/api/employees', methods=['GET'])
def get_employees():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = "SELECT * FROM employees LIMIT %s OFFSET %s"
    params = [per_page, (page-1)*per_page]
```

---

## Monitoring & Logging

### 1. Application Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('app.log', 
                                       maxBytes=10240000, 
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### 2. Error Tracking

```python
@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(f"Unhandled exception: {error}")
    return jsonify({'message': 'Internal server error'}), 500
```

### 3. Monitoring Tools

- **New Relic**: APM monitoring
- **Sentry**: Error tracking
- **DataDog**: Infrastructure monitoring
- **CloudWatch**: AWS logging

---

## Backup Strategy

### Automated MySQL Backups

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u root -p$MYSQL_PASSWORD employee_management > backup_$DATE.sql
```

Schedule with cron:
```bash
0 2 * * * /home/ubuntu/backup.sh
```

---

## Database Migration to Production

```bash
# Export current database
mysqldump -u root -p employee_management > prod_backup.sql

# Import to production
mysql -u root -p -h prod-server.com < prod_backup.sql
```

---

## Rollback Procedure

1. Keep previous version in git
2. Maintain database backups
3. Have rollback script ready:

```bash
#!/bin/bash
# rollback.sh
git checkout previous-version
systemctl restart employee-management
mysql < previous-backup.sql
```

---

## Maintenance

### Regular Tasks

- [ ] Update Python packages monthly
- [ ] Review logs weekly
- [ ] Backup database daily
- [ ] Monitor server resources
- [ ] Update SSL certificates (before expiry)
- [ ] Security patches as available

### Performance Check

Monitor:
- API response times (target: <200ms)
- Database query performance
- CPU/Memory usage
- Error rates
- User concurrent sessions

---

## Cost Estimation (AWS)

- **EC2 t2.micro**: $10/month
- **RDS MySQL**: $15/month
- **ELB**: $16/month
- **Data transfer**: ~$5/month
- **Total**: ~$46/month

---

## Support & Maintenance

For production support:
- Set up uptime monitoring
- Configure alerts
- Have incident response plan
- Document runbooks
- Regular security audits

---

**Version:** 1.0.0
**Last Updated:** 2024
