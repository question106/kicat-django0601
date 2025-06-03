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

## 🛠️ Deployment Steps

### **Step 1: Deploy Global Nginx Proxy (First Time Only)**

1. **Go to Portainer UI** → **Stacks** → **Add Stack**
2. **Name:** `nginx-proxy`
3. **Build method:** Upload
4. **Upload:** `portainer-setup/proxy-stack/docker-compose.yml`
5. **Deploy the stack**

> ✅ **Note:** The proxy stack will automatically create the `proxy-network` that your sites will use.

### **Step 2: Deploy Your Django Application**

1. **Go to Portainer UI** → **Stacks** → **Add Stack**
2. **Name:** `kicat-production`
3. **Build method:** Git Repository
4. **Repository URL:** `https://github.com/question106/kicat-django0601.git`
5. **Compose path:** `portainer-setup/kicat-production/docker-compose.yml`
6. **Environment Variables:**
   ```
   DJANGO_SECRET_KEY=your_generated_key
   DB_PASSWORD=your_generated_key
   ```
7. **Deploy the stack**

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