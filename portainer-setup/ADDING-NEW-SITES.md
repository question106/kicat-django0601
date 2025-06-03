# Adding New Sites to Your Portainer Setup

## The Process: Each Site = New Stack

When you want to add a new website, you create a **completely separate stack** in Portainer. The global proxy automatically discovers and routes traffic to the new site.

## Example: Adding site2.com

### Step 1: Create New Stack in Portainer

1. **Go to Portainer Web UI**
2. **Stacks** → **Add Stack**
3. **Name**: `site2-mycompany` (or any unique name)
4. **Use this docker-compose.yml content:**

```yaml
version: '3.8'

services:
  # Your Django App for site2.com
  app:
    build:
      context: https://github.com/your-username/site2-project.git
      dockerfile: Dockerfile
    container_name: site2-app
    volumes:
      - site2-static:/vol/web/static
      - site2-media:/vol/web/media
    environment:
      # Domain configuration for site2.com
      - VIRTUAL_HOST=site2.com,www.site2.com
      - VIRTUAL_PORT=8000
      - LETSENCRYPT_HOST=site2.com,www.site2.com
      - LETSENCRYPT_EMAIL=your-email@example.com
      
      # Django settings for site2
      - DEBUG=0
      - SECRET_KEY=different-secret-key-for-site2
      - ALLOWED_HOSTS=site2.com,www.site2.com
      - DB_HOST=db
      - DB_NAME=site2_db
      - DB_USER=postgres
      - DB_PASS=different-password-for-site2
    depends_on:
      - db
    restart: unless-stopped
    networks:
      - proxy-network
      - site2-internal

  # Database for site2.com
  db:
    image: postgres:13-alpine
    container_name: site2-db
    volumes:
      - site2-postgres:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=site2_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=different-password-for-site2
    restart: unless-stopped
    networks:
      - site2-internal

volumes:
  site2-static:
  site2-media:
  site2-postgres:

networks:
  proxy-network:
    external: true
  site2-internal:
    driver: bridge
```

### Step 2: Deploy the Stack

5. **Click "Deploy the stack"**
6. **Wait for deployment to complete**

### Step 3: Configure DNS

Point your domain to your VPS:
```
site2.com      A    YOUR_VPS_IP
www.site2.com  A    YOUR_VPS_IP
```

## That's It! 🎉

The nginx-proxy automatically:
- **Detects** the new container
- **Configures** routing for site2.com
- **Obtains** SSL certificate
- **Routes** traffic to the correct site

## Adding site3.com, site4.com, etc.

Just repeat the process with different values:

### For site3.com:
```yaml
# Change these values:
container_name: site3-app
- VIRTUAL_HOST=site3.com,www.site3.com
- LETSENCRYPT_HOST=site3.com,www.site3.com
# Different database credentials
# Different volume names (site3-static, site3-postgres, etc.)
```

## Important: What to Change for Each New Site

| Setting | Example for site2.com | Example for site3.com |
|---------|----------------------|----------------------|
| **Stack Name** | `site2-mycompany` | `site3-mycompany` |
| **Container Names** | `site2-app`, `site2-db` | `site3-app`, `site3-db` |
| **Domain** | `site2.com` | `site3.com` |
| **Database Name** | `site2_db` | `site3_db` |
| **Database Password** | `site2-password` | `site3-password` |
| **Secret Key** | `site2-secret` | `site3-secret` |
| **Volume Names** | `site2-static`, `site2-postgres` | `site3-static`, `site3-postgres` |
| **Network Names** | `site2-internal` | `site3-internal` |
| **Git Repository** | `your-username/site2-project.git` | `your-username/site3-project.git` |

## Your Portainer Dashboard Will Look Like:

```
📁 Stacks
├── nginx-proxy          (Global proxy - deploy once)
├── site1-mycompany      (site1.com)
├── site2-mycompany      (site2.com)  
├── site3-mycompany      (site3.com)
└── site4-mycompany      (site4.com)
```

## Benefits of This Approach

✅ **Complete Isolation**: Each site has its own database, volumes, secrets
✅ **Independent Updates**: Update one site without affecting others
✅ **Easy Management**: Each site is a separate stack in Portainer
✅ **Automatic Discovery**: Proxy automatically detects new sites
✅ **Individual Scaling**: Scale each site independently
✅ **Easy Removal**: Delete a site by removing its stack

## Quick Template for New Sites

Save this template and just change the highlighted values:

```yaml
version: '3.8'
services:
  app:
    build:
      context: https://github.com/YOUR-USERNAME/NEW-SITE-REPO.git
    container_name: SITENAME-app
    environment:
      - VIRTUAL_HOST=YOURDOMAIN.com,www.YOURDOMAIN.com
      - LETSENCRYPT_HOST=YOURDOMAIN.com,www.YOURDOMAIN.com
      - ALLOWED_HOSTS=YOURDOMAIN.com,www.YOURDOMAIN.com
      - SECRET_KEY=UNIQUE-SECRET-KEY
      - DB_PASS=UNIQUE-DB-PASSWORD
    networks:
      - proxy-network
      - SITENAME-internal
  db:
    image: postgres:13-alpine
    container_name: SITENAME-db
    environment:
      - POSTGRES_PASSWORD=SAME-UNIQUE-DB-PASSWORD
    networks:
      - SITENAME-internal
volumes:
  SITENAME-static:
  SITENAME-postgres:
networks:
  proxy-network:
    external: true
  SITENAME-internal:
```

## No Need to Touch:
- ❌ The global nginx-proxy stack
- ❌ Any existing site configurations  
- ❌ Server nginx configuration
- ❌ DNS for existing sites

Just create new stacks for new sites! 🚀 