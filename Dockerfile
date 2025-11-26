# Use a lightweight and stable NGINX base image
FROM nginx:stable-alpine

# Remove the default NGINX configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom NGINX configuration into the image
COPY nginx.conf /etc/nginx/conf.d/nginx.conf

# Copy the static website files into the default web root directory
COPY /static/index.html /usr/share/nginx/html/index.html

# Expose port 80
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]