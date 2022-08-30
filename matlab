# nginx configuration

server {
	listen 8585 default_server;
	listen [::]:8585 default_server;

	root /var/www/html;

	index index.html;

	server_name _;

	location ~ ^/([0-9]+) {
		proxy_set_header Host '127.0.0.1';
		proxy_pass http://127.0.0.1:$1;
	}

	location / {
		include proxy_params;
		proxy_pass http://unix:/tmp/matlabhub.sock;
	}
}

