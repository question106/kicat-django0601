# Database Configuration in Production

## 🗄️ How Databases Work in Production

In the Portainer approach, **each site gets its own dedicated PostgreSQL database container**. This provides complete isolation between sites.

## 📋 Database Configuration Details

### **In Production Stack (`site1-stack/docker-compose.yml`):**

```yaml
services:
  # Your Django App
  app:
    environment:
      - DB_HOST=db                    # 👈 Points to database service
      - DB_NAME=site1_db             # 👈 Database name
      - DB_USER=postgres             # 👈 Database user
      - DB_PASS=your-db-password     # 👈 Database password
    depends_on:
      - db                           # 👈 Waits for database to start

  # Database for this site
  db:                                # 👈 DATABASE SERVICE
    image: postgres:13-alpine        # 👈 PostgreSQL container
    container_name: site1-db
    volumes:
      - postgres-data:/var/lib/postgresql/data  # 👈 Persistent storage
    environment:
      - POSTGRES_DB=site1_db         # 👈 Creates database
      - POSTGRES_USER=postgres       # 👈 Creates user
      - POSTGRES_PASSWORD=your-db-password     # 👈 Sets password
    networks:
      - site1-internal               # 👈 Private network

volumes:
  postgres-data:                     # 👈 Persistent database storage
```

## 🏗️ Database Architecture

### **Each Site = Isolated Database:**

```
📁 Portainer Stacks:
├── nginx-proxy (Global)
├── site1-stack
│   ├── site1-app (Django)
│   └── site1-db (PostgreSQL)    # 👈 Dedicated database
├── site2-stack  
│   ├── site2-app (Django)
│   └── site2-db (PostgreSQL)    # 👈 Different database
└── site3-stack
    ├── site3-app (Django)
    └── site3-db (PostgreSQL)    # 👈 Another database
```

## ⚙️ When Database Gets Configured

### **1. Stack Deployment Time:**
When you deploy the stack in Portainer:

1. **PostgreSQL container starts**
2. **Database is created** automatically (`POSTGRES_DB=site1_db`)
3. **User is created** (`POSTGRES_USER=postgres`)  
4. **Password is set** (`POSTGRES_PASSWORD=your-password`)
5. **Django connects** using environment variables

### **2. First Django Start:**
When Django container starts:

1. **Waits for database** (`depends_on: db`)
2. **Connects to database** using `DB_HOST=db`
3. **Runs migrations** (if configured in entrypoint)
4. **Creates Django tables**

## 🔧 Database Configuration Steps

### **Step 1: Set Database Credentials**
In your Portainer stack, customize these values:

```yaml
environment:
  # Django app settings
  - DB_HOST=db
  - DB_NAME=site1_db              # 👈 Change for each site
  - DB_USER=postgres
  - DB_PASS=secure-password-123   # 👈 Use strong password

# Database container settings
db:
  environment:
    - POSTGRES_DB=site1_db        # 👈 Must match Django setting
    - POSTGRES_USER=postgres      # 👈 Must match Django setting  
    - POSTGRES_PASSWORD=secure-password-123  # 👈 Must match Django setting
```

### **Step 2: Database Isolation**
Each site has its own:

- **Database container** (`site1-db`, `site2-db`, etc.)
- **Database name** (`site1_db`, `site2_db`, etc.)
- **Storage volume** (`site1-postgres`, `site2-postgres`, etc.)
- **Network** (`site1-internal`, `site2-internal`, etc.)

### **Step 3: Data Persistence**
Database data is stored in Docker volumes:

```yaml
volumes:
  postgres-data:          # 👈 Data survives container restarts
```

## 🚀 Complete Example: site2.com

```yaml
version: '3.8'
services:
  app:
    container_name: site2-app
    environment:
      - VIRTUAL_HOST=site2.com,www.site2.com
      - DB_HOST=db
      - DB_NAME=site2_db           # 👈 Different database
      - DB_USER=postgres
      - DB_PASS=different-password # 👈 Different password
    depends_on:
      - db
    networks:
      - proxy-network
      - site2-internal             # 👈 Different network

  db:
    image: postgres:13-alpine
    container_name: site2-db       # 👈 Different container
    volumes:
      - site2-postgres:/var/lib/postgresql/data  # 👈 Different volume
    environment:
      - POSTGRES_DB=site2_db       # 👈 Different database
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=different-password     # 👈 Different password
    networks:
      - site2-internal             # 👈 Different network

volumes:
  site2-postgres:                  # 👈 Different volume
networks:
  site2-internal:                  # 👈 Different network
```

## 💡 Key Benefits

### **Complete Database Isolation:**
- ✅ **No data mixing** between sites
- ✅ **Independent backups** per site
- ✅ **Different passwords** for security
- ✅ **Separate storage** volumes

### **Easy Management:**
- ✅ **Scale databases** independently
- ✅ **Backup specific sites** easily
- ✅ **Update one site** without affecting others
- ✅ **Monitor per-site** database usage

## 🔍 Database Access

### **For Development/Debugging:**
You can connect to any site's database:

```bash
# Connect to site1 database
docker exec -it site1-db psql -U postgres -d site1_db

# Connect to site2 database  
docker exec -it site2-db psql -U postgres -d site2_db
```

### **From Django App:**
Django automatically connects using the environment variables:

```python
# Django settings.py (automatically configured)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),     # site1_db
        'USER': os.environ.get('DB_USER'),     # postgres
        'PASSWORD': os.environ.get('DB_PASS'), # your-password
        'HOST': os.environ.get('DB_HOST'),     # db
        'PORT': '5432',
    }
}
```

## 📝 Summary

**Database Configuration Happens:**
1. **✅ Automatically** when you deploy the stack
2. **✅ Per-site isolation** - each site gets its own database
3. **✅ Environment variables** handle the connection
4. **✅ Persistent storage** - data survives container restarts

**You don't need to manually configure databases** - it's all handled by the docker-compose.yml configuration! 