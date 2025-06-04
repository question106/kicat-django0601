#!/bin/bash

echo "=== KICAT PRODUCTION DIAGNOSTIC SCRIPT ==="
echo "Running at: $(date)"
echo

echo "=== 1. DOCKER CONTAINERS STATUS ==="
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo

echo "=== 2. DOCKER NETWORKS ==="
docker network ls
echo

echo "=== 3. DOCKER VOLUMES ==="
docker volume ls | grep kicat
echo

echo "=== 4. CHECK NGINX-PROXY LOGS (last 20 lines) ==="
docker logs --tail 20 nginx-proxy 2>/dev/null || echo "nginx-proxy container not found or not accessible"
echo

echo "=== 5. CHECK KICAT-APP LOGS (last 20 lines) ==="
docker logs --tail 20 kicat-app 2>/dev/null || echo "kicat-app container not found or not accessible"
echo

echo "=== 6. CHECK KICAT-DB LOGS (last 10 lines) ==="
docker logs --tail 10 kicat-db 2>/dev/null || echo "kicat-db container not found or not accessible"
echo

echo "=== 7. STATIC FILES IN KICAT-APP CONTAINER ==="
echo "Checking if static files exist in app container:"
docker exec kicat-app ls -la /vol/web/static/ 2>/dev/null || echo "Cannot access /vol/web/static/ in kicat-app"
echo
echo "Checking if main.js exists:"
docker exec kicat-app ls -la /vol/web/static/js/main.js 2>/dev/null || echo "main.js not found in kicat-app"
echo

echo "=== 8. STATIC FILES IN NGINX-PROXY CONTAINER ==="
echo "Checking if static files are accessible to nginx:"
docker exec nginx-proxy ls -la /vol/web/static/ 2>/dev/null || echo "Cannot access /vol/web/static/ in nginx-proxy"
echo
echo "Checking if main.js is accessible to nginx:"
docker exec nginx-proxy ls -la /vol/web/static/js/main.js 2>/dev/null || echo "main.js not accessible to nginx-proxy"
echo

echo "=== 9. VOLUME MOUNT INFORMATION ==="
echo "kicat-app volume mounts:"
docker inspect kicat-app | grep -A 10 -B 2 "Mounts" 2>/dev/null || echo "Cannot inspect kicat-app"
echo
echo "nginx-proxy volume mounts:"
docker inspect nginx-proxy | grep -A 10 -B 2 "Mounts" 2>/dev/null || echo "Cannot inspect nginx-proxy"
echo

echo "=== 10. PORTAINER STACK STATUS ==="
echo "Running stacks:"
docker stack ls 2>/dev/null || echo "No Docker Swarm stacks found"
echo

echo "=== 11. NGINX CONFIGURATION ==="
echo "Checking nginx config in proxy container:"
docker exec nginx-proxy cat /etc/nginx/conf.d/default.conf 2>/dev/null | head -20 || echo "Cannot access nginx config"
echo

echo "=== 12. NETWORK CONNECTIVITY TEST ==="
echo "Testing connection from nginx-proxy to kicat-app:"
docker exec nginx-proxy wget -q --spider http://kicat-app:8000/ 2>/dev/null && echo "✓ nginx-proxy can reach kicat-app" || echo "✗ nginx-proxy cannot reach kicat-app"
echo

echo "=== DIAGNOSTIC COMPLETE ==="
echo "Please share this output to help diagnose the issue." 