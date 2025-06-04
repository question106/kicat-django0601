# 🔍 Debug Guide: Media File Upload & Serving Issues

## Problem Summary
- File uploads work locally (`manage.py runserver`)
- In production (Docker + nginx-proxy), files upload but return 404 when accessed
- **NEW ISSUE**: Quote request modal shows "오류가 발생했습니다. 다시 시도해 주세요." error when uploading files
- **DISCOVERY**: Files ARE being uploaded (visible in admin), but nginx can't serve them

## 🕵️ Enhanced Step-by-Step Debugging

### ⚠️ **URGENT: Volume Mapping Issue Detected**

From your nginx logs, I can see:
```bash
[error] open() "/vol/web/media/quotes/translation_material_GvoTFxs.pdf" failed (2: No such file or directory)
```

**This means nginx-proxy can't see the files that Django is saving!**

### Step 1: Check Volume Mapping Issue

#### Test 1: Check if Django App Can See Its Own Files
```bash
# Check files in Django container
docker exec -it kicat-app ls -la /vol/web/media/quotes/

# Check if files exist after upload
docker exec -it kicat-app find /vol/web/media -name "*.pdf" -ls
```

#### Test 2: Check if nginx-proxy Can See Media Files
```bash
# Check if nginx-proxy container can see the media files
docker exec -it nginx-proxy ls -la /vol/web/media/quotes/ 2>/dev/null || echo "nginx-proxy CANNOT see media files"

# Check nginx-proxy volume mounts
docker inspect nginx-proxy | grep -A 20 "Mounts"
```

#### Test 3: Check Volume Configuration
```bash
# List all volumes
docker volume ls | grep media

# Check volume details
docker volume inspect kicat-production_media-files
```

### Step 2: Fix Volume Mapping

The issue is that **nginx-proxy and Django app don't share the same volume**. Here are the solutions:

#### Solution A: Let Django Serve Media Files (Recommended)
Since Django is already serving static files, let it handle media too:

**No nginx configuration needed** - Django will serve media files directly through the app.

#### Solution B: Fix nginx-proxy Volume Mapping (Advanced)
If you want nginx to serve media files directly:

1. **Update proxy-stack to mount media volume:**
```yaml
# In portainer-setup/proxy-stack/docker-compose.yml
volumes:
  - kicat-production_media-files:/vol/web/media:ro  # Add this line
```

2. **Redeploy proxy stack** with the new volume mapping

### Step 3: Check JavaScript Cache Issue

#### Force Cache Reload
1. **Hard refresh** in browser: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
2. **Clear browser cache** for your domain
3. **Check if new JavaScript loads** - the file upload UI should now change when you select a file

### Step 4: Test Both Fixes

#### Test File Upload UI
1. Upload a file in the quote modal
2. **UI should change** to show file name and size
3. Form should submit successfully

#### Test Media File Access
1. Upload a file via quote modal
2. Go to admin panel and click the file link
3. **File should download/display** instead of 404 error

## 🎯 Quick Production Test Commands

```bash
# 1. Check if Django can see uploaded files
docker exec -it kicat-app ls -la /vol/web/media/quotes/

# 2. Check if nginx-proxy can see the same files
docker exec -it nginx-proxy ls -la /vol/web/media/quotes/ || echo "Volume not mounted"

# 3. Upload a test file and check immediately
# (Upload via modal, then run):
docker exec -it kicat-app ls -la /vol/web/media/quotes/ | tail -1

# 4. Test media URL directly
curl -I https://kicat.graceed.co.uk/media/quotes/[FILENAME]
```

## 🔧 Enhanced Error Messages

The updated Django view now provides specific error messages:
- **"Service type is required"** - Missing service_type field
- **"Invalid service type"** - service_type ID doesn't exist
- **"File upload is required"** - No file in request
- **"Validation failed: [details]"** - Django model validation errors
- **"Server error: [details]"** - Unexpected server errors

## 🚀 Next Steps After Debugging

1. **Deploy Enhanced Debug Version**: The updated code includes better error handling
2. **Test File Upload**: Try uploading a small file and check the specific error message
3. **Check Logs**: Monitor Docker logs for detailed error information
4. **Fix Based on Specific Error**: Use the enhanced error messages to identify the exact issue

## 🎯 Expected Results After Volume Fix

1. **JavaScript Cache Fixed**: File upload UI will show selected file name and change appearance
2. **Volume Mapping Fixed**: nginx will be able to serve media files OR Django will serve them directly
3. **File Upload Works**: Both upload and file access will work properly
4. **404 Errors Gone**: Clicking file links in admin will download/display files correctly

## 🕵️ Step-by-Step Debugging

### Step 1: Check if Files Are Actually Uploaded

#### Test Upload in Development
```bash
# Start local development
docker-compose up

# Upload a file through the modal
# Check if file appears in: data/web/media/quotes/
ls -la data/web/media/quotes/
```

#### Test Upload in Production
```bash
# Deploy to production (after fixes)
# Upload a file through the modal
# Check container media directory:
docker exec kicat-app ls -la /vol/web/media/quotes/
```

### Step 2: Test Media URL Access

#### Check Django URLs
```bash
# In production container:
docker exec -it kicat-app sh

# Test Django media serving:
curl http://localhost:8000/media/quotes/filename.jpg
curl http://localhost:8000/debug-media/

# Check file permissions:
ls -la /vol/web/media/quotes/
stat /vol/web/media/quotes/filename.jpg
```

#### Check External Access
```bash
# Test from outside container:
curl -I https://kicat.co.kr/media/quotes/filename.jpg
curl -I https://kicat.co.kr/debug-media/
```

### Step 3: Check Volume Mappings

#### Verify Volume Mounting
```bash
# Check if volumes are properly mounted:
docker volume ls | grep kicat
docker volume inspect kicat-production_media-files

# Check if nginx-proxy can see the files:
docker exec nginx-proxy ls -la /vol/web/media/ 2>/dev/null || echo "nginx-proxy can't see media files"
```

### Step 4: Check Django Settings

#### Verify Settings in Production
```bash
# In production container:
docker exec -it kicat-app sh
python manage.py shell

# In Django shell:
from django.conf import settings
print("MEDIA_URL:", settings.MEDIA_URL)
print("MEDIA_ROOT:", settings.MEDIA_ROOT)
print("DEBUG:", settings.DEBUG)

import os
print("MEDIA_ROOT exists:", os.path.exists(settings.MEDIA_ROOT))
print("MEDIA_ROOT writable:", os.access(settings.MEDIA_ROOT, os.W_OK))
```

## 🛠️ Common Solutions

### Solution 1: Force Django to Serve Media in Production
**File: `app/app/settings.py`**
```python
# Add this at the end of settings.py
SERVE_MEDIA_IN_PRODUCTION = True
```

**File: `app/app/urls.py`**
```python
# Always serve media files (current fix applied)
urlpatterns += static(
    settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT,
)
```

### Solution 2: Fix File Permissions
```bash
# In Dockerfile, ensure proper permissions:
RUN mkdir -p /vol/web/media && \
    chown -R app:app /vol && \
    chmod -R 755 /vol
```

### Solution 3: Update nginx-proxy Configuration
**For Direct nginx Serving (Advanced):**

Create `portainer-setup/nginx-media-fix.sh`:
```bash
#!/bin/bash
# After both stacks are deployed, run this script

# Mount media volume to nginx-proxy
docker volume create nginx-media
docker run --rm -v kicat-production_media-files:/source -v nginx-media:/dest alpine sh -c "cp -a /source/. /dest/"

# Update nginx-proxy to mount media volume
docker stop nginx-proxy
docker run -d \
  --name nginx-proxy \
  -p 80:80 -p 443:443 \
  -v /var/run/docker.sock:/tmp/docker.sock:ro \
  -v nginx-proxy_nginx-certs:/etc/nginx/certs \
  -v nginx-proxy_nginx-vhost:/etc/nginx/vhost.d \
  -v nginx-proxy_nginx-html:/usr/share/nginx/html \
  -v nginx-media:/vol/web/media:ro \
  --network proxy-network \
  nginxproxy/nginx-proxy:alpine
```

## 🧪 Test Cases

### Test Case 1: File Upload
1. Go to your site
2. Open quote request modal
3. Upload a small image file
4. Submit form
5. Check if file exists in media directory

### Test Case 2: Direct URL Access
1. Upload a file (get filename from admin or database)
2. Try accessing: `https://your-domain.com/media/quotes/filename.ext`
3. Should return the file, not 404

### Test Case 3: Debug Endpoint
1. Visit: `https://your-domain.com/debug-media/`
2. Should show media directory contents
3. Verify uploaded files are listed

## 📋 Quick Fix Checklist

- [ ] Fixed volume mappings in portainer configs
- [ ] Django serves media files in production
- [ ] File permissions correct in Docker
- [ ] Upload works (files appear in container)
- [ ] Direct media URL access works
- [ ] nginx-proxy forwards requests properly

## 🚀 Expected Results After Fix

1. **File Upload**: ✅ Files saved to `/vol/web/media/quotes/`
2. **URL Access**: ✅ `https://domain.com/media/quotes/file.jpg` returns file
3. **Debug Page**: ✅ Shows uploaded files
4. **Quote Modal**: ✅ File upload and submission works
5. **Admin Panel**: ✅ Can see uploaded files

## 📞 If Still Not Working

If media files still don't work after these fixes:

1. **Check container logs**: `docker logs kicat-app`
2. **Check nginx-proxy logs**: `docker logs nginx-proxy`
3. **Verify file upload in Django admin**: Upload via admin panel and test URL
4. **Test with simple HTML form**: Bypass AJAX to isolate the issue

The most likely fix is that Django now serves media files in production mode, which should resolve the 404 errors. 