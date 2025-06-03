# Django Multi-Site Deployment with Portainer

## 🚀 Overview
This project uses **Portainer** for easy deployment and management of multiple Django websites on a single VPS with automatic SSL certificates.

## 📁 Project Structure
```
kicat-django0601/
├── app/                     # Your Django application code
├── portainer-setup/         # Portainer deployment configurations
│   ├── proxy-stack/         # Global nginx-proxy stack (deploy once)
│   ├── site1-stack/         # Template for individual sites
│   ├── SETUP-INSTRUCTIONS.md
│   ├── DEPLOYMENT-METHODS.md
│   └── ADDING-NEW-SITES.md
├── Dockerfile              # Production Docker image
├── requirements.txt        # Python dependencies
└── docker-compose.yml     # Development environment
```

## 🛠️ Quick Start

### 1. Development (Local)
```bash
docker-compose up --build
```
Access: http://localhost:8000

### 2. Production (Portainer)
1. **Deploy Global Proxy** (once): Use `portainer-setup/proxy-stack/docker-compose.yml`
2. **Deploy Sites**: Create new stacks using `portainer-setup/site1-stack/docker-compose.yml` as template
3. **Configure DNS**: Point domains to your VPS IP

## 📚 Documentation
- **[Setup Instructions](portainer-setup/SETUP-INSTRUCTIONS.md)** - Complete setup guide
- **[Deployment Methods](portainer-setup/DEPLOYMENT-METHODS.md)** - How to deploy your code
- **[Adding New Sites](portainer-setup/ADDING-NEW-SITES.md)** - Scale to multiple websites

## 🔑 Key Features
- ✅ **Multiple Domains**: site1.com, site2.com, site3.com, etc.
- ✅ **Automatic SSL**: Let's Encrypt certificates
- ✅ **Easy Management**: Portainer web interface
- ✅ **Complete Isolation**: Each site has its own database and volumes
- ✅ **Auto-Discovery**: nginx-proxy automatically routes traffic

## 🌐 Architecture
```
Internet → nginx-proxy → [site1.com] → Django App 1
                      → [site2.com] → Django App 2
                      → [site3.com] → Django App 3
```

## 🚀 Deployment Workflow
1. **Push code** to Git repository
2. **Create stack** in Portainer
3. **Configure domain** in environment variables
4. **Deploy** - SSL and routing handled automatically!

---
**Perfect for hosting multiple client websites on a single VPS! 🎯**