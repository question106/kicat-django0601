# 🔍 Debug Guide: Media File Upload & Serving Issues

## Problem Summary
- File uploads work locally (`manage.py runserver`)
- In production (Docker + nginx-proxy), files upload but return 404 when accessed
- **NEW ISSUE**: Quote request modal shows "오류가 발생했습니다. 다시 시도해 주세요." error when uploading files

## 🕵️ Enhanced Step-by-Step Debugging

### Step 1: Debug File Upload Errors in Production

#### Check Django Logs
```bash
# View Django application logs in production
docker logs kicat-app -f

# Or if using Docker Compose
docker-compose logs app -f
```

#### Test File Upload Directly
```bash
# SSH into the production container to test file uploads
docker exec -it kicat-app /bin/sh

# Inside container, check media directory permissions
ls -la /vol/web/media/
ls -la /vol/web/media/quotes/

# Check if Django can write to media directory
touch /vol/web/media/test_file.txt
ls -la /vol/web/media/test_file.txt
rm /vol/web/media/test_file.txt
```

#### Check File Upload Limits
```bash
# Check Django settings in production
docker exec -it kicat-app python manage.py shell

# In Django shell:
from django.conf import settings
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"FILE_UPLOAD_MAX_MEMORY_SIZE: {getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 'Not set')}")
print(f"DATA_UPLOAD_MAX_MEMORY_SIZE: {getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', 'Not set')}")
```

### Step 2: Test File Upload API Endpoint

#### Manual API Test
```bash
# Test the quote creation endpoint with curl
curl -X POST https://kicat.co.kr/quotes/create/ \
  -H "Content-Type: multipart/form-data" \
  -F "name=Test User" \
  -F "company=Test Company" \
  -F "email=test@example.com" \
  -F "phone=123-456-7890" \
  -F "service_type=1" \
  -F "message=Test message" \
  -F "file=@test_document.pdf" \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN"
```

### Step 3: Check Browser Network Tab

1. Open Browser DevTools (F12)
2. Go to Network tab
3. Try submitting the quote form
4. Look for the POST request to `/quotes/create/`
5. Check:
   - Request headers
   - Request payload
   - Response status and body
   - Any error messages

### Step 4: Common Production Issues & Solutions

#### Issue 1: Missing CSRF Token
**Symptoms**: 403 Forbidden errors
**Solution**: Ensure CSRF token is properly included in form

#### Issue 2: nginx Client Max Body Size
**Symptoms**: 413 Request Entity Too Large
**Solution**: Add to nginx configuration:
```nginx
client_max_body_size 10M;
```

#### Issue 3: Volume Permissions
**Symptoms**: Permission denied errors
**Solution**: Check Docker volume permissions:
```bash
docker exec -it kicat-app ls -la /vol/web/media/
# Should show app:app ownership
```

#### Issue 4: Missing Media Directory
**Symptoms**: Directory not found errors
**Solution**: Create media directories:
```bash
docker exec -it kicat-app mkdir -p /vol/web/media/quotes/
docker exec -it kicat-app mkdir -p /vol/web/media/prepared_quotes/
```

### Step 5: Enhanced Debugging (NEW)

#### Check Enhanced Error Logs
With the updated view, you'll now see detailed error information:
```bash
# Watch logs in real-time during file upload
docker logs kicat-app -f | grep -E "(POST data|FILES data|Content length|Error|quote)"
```

#### Test File Upload Validation
The updated view now checks:
- ✅ Service type exists
- ✅ File is present in request
- ✅ File validation passes
- ✅ Database save succeeds

## 🎯 Quick Production Test Commands

```bash
# 1. Check if the application is running
curl -I https://kicat.co.kr/

# 2. Check media directory structure
docker exec -it kicat-app find /vol/web/media -type d -ls

# 3. Check Django debug endpoint (if enabled)
curl https://kicat.co.kr/debug-media/

# 4. Test small file upload
# Create a small test file first, then use the modal to upload it

# 5. Check container resource limits
docker stats kicat-app
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