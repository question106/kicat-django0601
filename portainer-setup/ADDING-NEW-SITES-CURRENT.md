# Adding New Sites to Your Current NPM Setup

## 🎯 Current Architecture

Your setup uses **Nginx Proxy Manager (NPM)** instead of nginx-proxy:

```
📁 Your Active Stacks:
├── npm-stack           ✅ (Handles routing & SSL - ports 80, 443, 8081)
└── kicat-production    ✅ (Your main Django site)
```

## 🚀 Adding a New Site (2-Step Process)

### **Step 1: Create New Stack in Portainer**

1. **Go to Portainer** → **Stacks** → **Add Stack**
2. **Name**: `newsite-production` (or any unique name)
3. **Build method**: Repository/Git
4. **Repository URL**: `https://github.com/YOUR-USERNAME/YOUR-NEW-REPO.git`
5. **Compose path**: `docker-compose.yml` (or wherever you put it)
6. **Environment Variables**:
   ```
   SECRET_KEY=your_generated_secret_key
   DB_PASSWORD=unique_password_for_this_site
   MAILJET_API_KEY=your_mailjet_key (if needed)
   MAILJET_API_SECRET=your_mailjet_secret (if needed)
   ADMIN_EMAILS=admin@newsite.com
   ```
7. **Deploy the stack**

### **Step 2: Configure Domain in NPM**

1. **Go to NPM Admin Panel**: `http://YOUR_VPS_IP:8081`
2. **Proxy Hosts** → **Add Proxy Host**
3. **Configure**:
   ```
   Domain Names: newsite.com, www.newsite.com
   Scheme: http
   Forward Hostname/IP: newsite-app
   Forward Port: 8000
   
   ✅ Block Common Exploits
   ✅ Websockets Support
   ```
4. **SSL Tab**:
   ```
   ✅ Request a new SSL Certificate
   ✅ Force SSL
   ✅ HTTP/2 Support
   Email: your-email@example.com
   ```
5. **Save**

## 📝 Docker-Compose Template for New Sites

```yaml
version: '3.8'

services:
  app:
    build:
      context: https://github.com/YOUR-USERNAME/YOUR-NEW-REPO.git
      dockerfile: Dockerfile
    container_name: newsite-app  # Change this
    volumes:
      - newsite-static:/vol/web/static
      - newsite-media:/vol/web/media
    environment:
      - DEBUG=0
      - SECRET_KEY=${SECRET_KEY}
      - ALLOWED_HOSTS=newsite.com www.newsite.com  # Your domains
      - DB_HOST=db
      - DB_NAME=newsite_production  # Unique DB name
      - DB_USER=postgres
      - DB_PASSWORD=${DB_PASSWORD}  # Unique password
    depends_on:
      - db
    restart: unless-stopped
    expose:
      - "8000"
    networks:
      - proxy-network  # This connects to NPM
      - newsite-internal

  db:
    image: postgres:13-alpine
    container_name: newsite-db  # Change this
    volumes:
      - newsite-postgres:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=newsite_production  # Match above
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=${DB_PASSWORD}  # Match above
    restart: unless-stopped
    networks:
      - newsite-internal

volumes:
  newsite-static:    # Change these
  newsite-media:     # Change these
  newsite-postgres:  # Change these

networks:
  proxy-network:
    external: true  # This is created by npm-stack
  newsite-internal:
    driver: bridge
```

## 🔧 What to Change for Each New Site

| Setting | Example 1 | Example 2 | Example 3 |
|---------|-----------|-----------|-----------|
| **Stack Name** | `site1-production` | `site2-production` | `blog-production` |
| **Container Names** | `site1-app`, `site1-db` | `site2-app`, `site2-db` | `blog-app`, `blog-db` |
| **Domains** | `site1.com` | `site2.com` | `blog.mycompany.com` |
| **Database** | `site1_production` | `site2_production` | `blog_production` |
| **Volume Names** | `site1-static`, `site1-postgres` | `site2-static`, `site2-postgres` | `blog-static`, `blog-postgres` |
| **Network** | `site1-internal` | `site2-internal` | `blog-internal` |
| **GitHub Repo** | `username/site1-repo.git` | `username/site2-repo.git` | `username/blog-repo.git` |

## 🎯 Key Differences from Old nginx-proxy Method

| Old Method (nginx-proxy) | Current Method (NPM) |
|--------------------------|----------------------|
| ❌ Environment variables: `VIRTUAL_HOST`, `LETSENCRYPT_HOST` | ✅ No special environment variables needed |
| ❌ Manual nginx config files | ✅ Web UI configuration |
| ❌ nginx-proxy container autodiscovery | ✅ Manual proxy host creation in NPM |
| ❌ Limited SSL options | ✅ Full Let's Encrypt integration |

## 📊 Your Portainer Dashboard Will Look Like:

```
📁 Stacks
├── npm-stack              (Global proxy - already deployed)
├── kicat-production       (kicat.co.kr)
├── newsite-production     (newsite.com)
├── blog-production        (blog.company.com)
└── shop-production        (shop.company.com)
```

## 🔍 Troubleshooting

### **Container not accessible from NPM:**
- Ensure container is connected to `proxy-network`
- Check container name matches NPM configuration
- Verify container is running on port 8000

### **SSL certificate issues:**
- Verify domain DNS points to VPS IP
- Check email address in NPM
- Wait 2-3 minutes for Let's Encrypt

### **Database connection issues:**
- Ensure unique database names and passwords
- Check environment variables match

## ✅ Benefits of Your Current NPM Setup

✅ **Web UI**: Easy management through browser
✅ **Full SSL Control**: Advanced Let's Encrypt options  
✅ **Real-time Monitoring**: See proxy stats and logs
✅ **Advanced Features**: Rate limiting, custom headers, etc.
✅ **Backup/Restore**: Export/import proxy configurations
✅ **Multiple Certificates**: Different SSL providers support

## 🚀 Quick Checklist for New Sites

- [ ] Code pushed to GitHub repository
- [ ] Docker-compose.yml created with unique names
- [ ] Stack deployed in Portainer
- [ ] Container running and healthy
- [ ] Domain DNS pointing to VPS IP
- [ ] Proxy host created in NPM (YOUR_VPS_IP:8081)
- [ ] SSL certificate obtained
- [ ] Website accessible with HTTPS

Your new site will be live with automatic SSL! 🎉 