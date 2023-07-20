# Use the official Nginx image as the base image
FROM nginx:latest

# Copy the contents of the html_website folder to the default Nginx web root
COPY *.html /usr/share/nginx/html

# Expose port 80 to allow incoming HTTP requests
EXPOSE 80

# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]