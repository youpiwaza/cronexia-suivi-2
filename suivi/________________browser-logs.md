2. How Enable Gzip Compression in Nginx
On servers using Nginx, gzip compression cannot be activated automatically, so you have to enable gzip compression manually.

You need to add the following code into the /etc/nginx/nginx.conf to enable gzip in Nginx servers. Do not add anywhere. You should add it inside the http {} section.

gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_buffers 16 8k;
gzip_http_version 1.1;
gzip_types image/svg+xml text/plain text/html text/xml text/css text/javascript application/xml application/xhtml+xml application/rss+xml application/javascript application/x-javascript application/x-font-ttf application/vnd.ms-fontobject font/opentype font/ttf font/eot font/otf;
After adding the gzip compression lines, save and close the config file and restart NGINX with the command.

sudo service nginx restart
