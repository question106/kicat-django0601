# Portainer Multi-Site Setup Guide

## Overview
This setup allows you to host multiple websites using Portainer with automatic SSL certificates and easy management through the web interface.

## Architecture
- **Global Nginx Proxy**: Handles all incoming traffic and routes to the correct site
- **Individual Site Stacks**: Each website runs as a separate stack
- **Automatic SSL**: Let's Encrypt certificates managed automatically
- **Isolated Databases**: Each site has its own database

## Step-by-Step Setup

### Step 1: Create the Proxy Network

First, create a network that all sites will use to communicate with the proxy:

```bash
docker network create proxy-network
```

### Step 2: Deploy the Global Proxy Stack

1. **In Portainer Web UI:**
   - Go to **Stacks** → **Add Stack**
   - Name: `nginx-proxy`
   - Copy the content from `proxy-stack/docker-compose.yml`
   - **Important**: Change `your-email@example.com` to your real email
   - Deploy the stack

### Step 3: Deploy Your First Site

1. **In Portainer Web UI:**
   - Go to **Stacks** → **Add Stack**
   - Name: `site1` (or your site name)
   - Copy the content from `site1-stack/docker-compose.yml`
   - **Update these values:**
     - `VIRTUAL_HOST`: Your actual domain (e.g., `mysite.com,www.mysite.com`)
     - `LETSENCRYPT_HOST`: Same as VIRTUAL_HOST
     - `LETSENCRYPT_EMAIL`: Your email for SSL certificates
     - `SECRET_KEY`: Generate a new Django secret key
     - `ALLOWED_HOSTS`: Your domain names
     - `DB_PASS`: Choose a secure database password
   - Deploy the stack

### Step 4: Add More Sites

For each additional site:
1. Create a new stack in Portainer
2. Use the same docker-compose structure as site1
3. Change:
   - Container names (site2-app, site2-db, etc.)
   - Domain names in VIRTUAL_HOST
   - Database credentials
   - Volume names to avoid conflicts

## Key Benefits of This Approach

✅ **Easy Management**: All sites managed through Portainer UI
✅ **Automatic SSL**: Let's Encrypt certificates auto-renewed
✅ **Domain-based Routing**: Nginx automatically routes based on domain
✅ **Isolated**: Each site has its own database and volumes
✅ **Scalable**: Easy to add/remove sites
✅ **No Manual Nginx Config**: Everything handled automatically

## Environment Variables Explained

### For the Proxy (nginx-proxy):
- **VIRTUAL_HOST**: Domain names that should route to this container
- **VIRTUAL_PORT**: Port inside the container (usually 8000 for Django)
- **LETSENCRYPT_HOST**: Domains to get SSL certificates for
- **LETSENCRYPT_EMAIL**: Email for Let's Encrypt registration

### DNS Requirements
Make sure your domain's A records point to your VPS IP:
```
site1.yourdomain.com    A    YOUR_VPS_IP
www.site1.yourdomain.com A   YOUR_VPS_IP
```

## Monitoring and Logs

In Portainer, you can:
- View logs for each container
- Monitor resource usage
- Restart individual services
- Update containers easily

## Troubleshooting

1. **Site not accessible**: Check domain DNS settings
2. **SSL not working**: Verify email in LETSENCRYPT_EMAIL
3. **Database connection issues**: Check DB_HOST matches service name
4. **Proxy not routing**: Ensure containers are on proxy-network

## Example: Adding a Second Site

```yaml
# site2-stack/docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    container_name: site2-app
    environment:
      - VIRTUAL_HOST=site2.yourdomain.com,www.site2.yourdomain.com
      - VIRTUAL_PORT=8000
      - LETSENCRYPT_HOST=site2.yourdomain.com,www.site2.yourdomain.com
      # ... other environment variables
    networks:
      - proxy-network
      - site2-internal
```

This approach is much easier than manual nginx configuration and perfect for Portainer users! 