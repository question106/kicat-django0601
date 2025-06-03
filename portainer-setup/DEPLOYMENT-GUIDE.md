# 🚀 Production Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ **Step 1: Prepare Your Repository**

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for production deployment"
   git push origin main
   ```

2. **Make repository public or set up access token for private repos**

3. **Verify your GitHub repository URL:**
   - Example: `https://github.com/YOUR-USERNAME/kicat-django0601.git`

### ✅ **Step 2: VPS Prerequisites**

Ensure your VPS has:
- ✅ **Portainer running** (you already have this)
- ✅ **Docker installed**
- ✅ **Domain DNS configured** (A records pointing to VPS IP)

### ✅ **Step 3: Network Setup**

**On your VPS, create the proxy network:**
```bash
docker network create proxy-network
```

## 🛠️ Deployment Steps

### **Step 1: Deploy Global Nginx Proxy (One Time Only)**

1. **Go to Portainer UI** → **Stacks** → **Add Stack**
2. **Name:** `nginx-proxy`
3. **Copy this configuration:**

```yaml
version: '3.8'

services:
  nginx-proxy:
    image: nginxproxy/nginx-proxy:alpine
    container_name: nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro
      - nginx-certs:/etc/nginx/certs
      - nginx-vhost:/etc/nginx/vhost.d
      - nginx-html:/usr/share/nginx/html
    restart: unless-stopped
    networks:
      - proxy-network

  letsencrypt:
    image: nginxproxy/acme-companion
    container_name: nginx-proxy-acme
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - nginx-certs:/etc/nginx/certs
      - nginx-vhost:/etc/nginx/vhost.d
      - nginx-html:/usr/share/nginx/html
      - acme-state:/etc/acme.sh
    environment:
      - DEFAULT_EMAIL=admin@kicat.co.kr  # 👈 CHANGE THIS
    depends_on:
      - nginx-proxy
    restart: unless-stopped
    networks:
      - proxy-network

volumes:
  nginx-certs:
  nginx-vhost:
  nginx-html:
  acme-state:

networks:
  proxy-network:
    external: true
```

4. **Deploy the stack**

### **Step 2: Deploy Your Django Application**

1. **Go to Portainer UI** → **Stacks** → **Add Stack**
2. **Name:** `kicat-production`
3. **Copy configuration from:** `portainer-setup/kicat-production/docker-compose.yml`
4. **⚠️ IMPORTANT: Update these values:**

```yaml
environment:
  # Domain configuration
  - VIRTUAL_HOST=your-domain.com,www.your-domain.com       # 👈 CHANGE THIS
  - LETSENCRYPT_HOST=your-domain.com,www.your-domain.com   # 👈 CHANGE THIS
  - LETSENCRYPT_EMAIL=your-email@domain.com                # 👈 CHANGE THIS
  
  # Security
  - SECRET_KEY=generate-a-super-secure-key-here             # 👈 GENERATE NEW
  - ALLOWED_HOSTS=your-domain.com,www.your-domain.com      # 👈 CHANGE THIS
  - DB_PASS=create-secure-database-password                # 👈 CHANGE THIS

build:
  context: https://github.com/YOUR-USERNAME/kicat-django0601.git  # 👈 CHANGE THIS
```

5. **Deploy the stack**

## 🔧 Configuration Details

### **🔑 Generate Django Secret Key:**
```python
# Run this in Python:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### **🌐 DNS Configuration:**
Set these A records in your domain provider:
```
your-domain.com        A    YOUR_VPS_IP_ADDRESS
www.your-domain.com    A    YOUR_VPS_IP_ADDRESS
```

### **📊 Environment Variables Reference:**

| Variable | Example | Purpose |
|----------|---------|---------|
| `VIRTUAL_HOST` | `kicat.co.kr,www.kicat.co.kr` | Domains for nginx routing |
| `LETSENCRYPT_HOST` | `kicat.co.kr,www.kicat.co.kr` | Domains for SSL certificates |
| `LETSENCRYPT_EMAIL` | `admin@kicat.co.kr` | Let's Encrypt contact email |
| `SECRET_KEY` | `django-insecure-xyz123...` | Django secret key |
| `ALLOWED_HOSTS` | `kicat.co.kr,www.kicat.co.kr` | Django allowed hosts |
| `DB_PASS` | `secure_password_123` | Database password |

## 📝 Post-Deployment Steps

### **Step 1: Verify Deployment**

1. **Check containers are running:**
   - Go to **Containers** in Portainer
   - Verify `kicat-app` and `kicat-db` are running

2. **Check your website:**
   - Visit `https://your-domain.com`
   - Should show your Django site with SSL certificate

### **Step 2: Create Django Superuser**

1. **In Portainer** → **Containers** → Click `kicat-app`
2. **Console** → Connect as `app` user
3. **Run:**
   ```bash
   python manage.py createsuperuser
   ```

### **Step 3: Load Initial Data (if needed)**

```bash
# In container console:
python manage.py loaddata your_fixtures.json
```

## 🔍 Troubleshooting

### **Container not starting:**
1. Check **Logs** in Portainer
2. Common issues:
   - Wrong GitHub URL
   - Missing environment variables
   - Database connection issues

### **SSL not working:**
1. Verify DNS is pointing to VPS
2. Check Let's Encrypt logs
3. Ensure email is correct

### **500 Error:**
1. Check Django logs in container
2. Verify `ALLOWED_HOSTS` setting
3. Check database connection

## 🎯 Quick Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Domain DNS configured
- [ ] Proxy network created
- [ ] Global nginx-proxy deployed
- [ ] Environment variables updated
- [ ] GitHub URL updated in stack
- [ ] Stack deployed successfully
- [ ] Website accessible with SSL
- [ ] Django admin accessible
- [ ] Superuser created

## 🚀 Next Steps After Deployment

1. **Monitor:** Use Portainer to monitor containers
2. **Backup:** Set up database backups
3. **Scale:** Add more sites using the same pattern
4. **Update:** Redeploy by updating the stack

**Your Django application should now be live with automatic SSL! 🎉** 