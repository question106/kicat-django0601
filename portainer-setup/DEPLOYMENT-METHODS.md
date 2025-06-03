# How to Deploy Your Project Files with Portainer

## The Problem
The `docker-compose.yml` file only defines **services** (containers, networks, volumes). Your actual **project files** (Python code, templates, static files) need to be deployed separately.

## Method 1: Git Repository + Build (Recommended)

### Option A: Public Repository
```yaml
services:
  app:
    image: your-username/your-project:latest  # Pre-built image
    # OR
    build:
      context: https://github.com/your-username/your-project.git
      dockerfile: Dockerfile
```

### Option B: Private Repository with Access Token
```yaml
services:
  app:
    build:
      context: https://github.com/your-username/private-repo.git
      dockerfile: Dockerfile
      args:
        - GITHUB_TOKEN=your_personal_access_token
```

## Method 2: Portainer Git Repository Deployment

Portainer can pull your code directly from Git:

1. **In Portainer:**
   - Go to **Stacks** → **Add Stack**
   - Choose **Repository** tab
   - Enter your Git repository URL
   - Specify the docker-compose.yml path
   - Deploy

## Method 3: Build Image Locally, Push to Registry

### Steps:
1. **Build locally:**
   ```bash
   docker build -t your-username/your-project:v1.0 .
   docker push your-username/your-project:v1.0
   ```

2. **Use in docker-compose.yml:**
   ```yaml
   services:
     app:
       image: your-username/your-project:v1.0
   ```

## Method 4: Volume Mounting (Development Only)

**WARNING**: Only for development, not production!

```yaml
services:
  app:
    image: python:3.9
    volumes:
      - /path/to/your/project:/app  # Mount host directory
    working_dir: /app
    command: python manage.py runserver 0.0.0.0:8000
```

## Recommended Workflow for Production

### Step 1: Prepare Your Project
```dockerfile
# Dockerfile
FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Step 2: Push to Git Repository
```bash
git add .
git commit -m "Deploy version"
git push origin main
```

### Step 3: Deploy in Portainer
```yaml
# In Portainer Stack
services:
  app:
    build:
      context: https://github.com/your-username/your-project.git
      dockerfile: Dockerfile
    environment:
      - VIRTUAL_HOST=yoursite.com
      # ... other environment variables
```

## Complete Example: Django Project Deployment

### Your Project Structure:
```
your-django-project/
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── myproject/
│   ├── settings.py
│   └── ...
└── myapp/
    ├── models.py
    └── ...
```

### Dockerfile:
```dockerfile
FROM python:3.9-alpine

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### In Portainer Stack:
```yaml
version: '3.8'
services:
  app:
    build:
      context: https://github.com/your-username/your-django-project.git
      dockerfile: Dockerfile
    environment:
      - VIRTUAL_HOST=yoursite.com,www.yoursite.com
      - VIRTUAL_PORT=8000
      # ... other environment variables
```

## Which Method Should You Use?

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Git + Build** | Production | Automatic, version controlled | Requires Git setup |
| **Pre-built Images** | Production | Fast deployment | Manual building |
| **Portainer Git** | Both | Easy setup | Limited customization |
| **Volume Mounting** | Development only | Quick changes | Not secure for production |

## For Your Setup:
1. **Put your Django project in a Git repository**
2. **Add a Dockerfile to your project**
3. **Use the Git URL in your Portainer stack**
4. **Portainer will automatically pull and build your code**

This way, every time you update your code and push to Git, you can redeploy the stack in Portainer to get the latest version! 