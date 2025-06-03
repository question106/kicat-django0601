#!/bin/bash

# Setup script to configure nginx-proxy for media file serving
# Run this after deploying both proxy-stack and kicat-production

echo "Setting up nginx media configuration..."

# Create nginx configuration for media files
docker exec nginx-proxy sh -c 'cat > /etc/nginx/vhost.d/kicat.co.kr << EOF
# Media files configuration for kicat.co.kr
location /media/ {
    alias /vol/web/media/;
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}
EOF'

docker exec nginx-proxy sh -c 'cat > /etc/nginx/vhost.d/www.kicat.co.kr << EOF
# Media files configuration for www.kicat.co.kr
location /media/ {
    alias /vol/web/media/;
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}
EOF'

docker exec nginx-proxy sh -c 'cat > /etc/nginx/vhost.d/kicat.graceed.co.uk << EOF
# Media files configuration for kicat.graceed.co.uk
location /media/ {
    alias /vol/web/media/;
    expires 1y;
    add_header Cache-Control "public, immutable";
    access_log off;
}
EOF'

# Reload nginx configuration
echo "Reloading nginx configuration..."
docker exec nginx-proxy nginx -s reload

echo "✅ nginx media configuration complete!"
echo "Test with: curl -I http://kicat.graceed.co.uk/media/quotes/견적서_샘플.jpg" 