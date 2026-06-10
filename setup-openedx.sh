#!/bin/bash

set -e

echo "=============================================="
echo "Open edX Production Setup Script"
echo "=============================================="

# Configuration
EDX_PLATFORM_DIR="edx-platform"
DOCKER_NETWORK="openedx_network"
MYSQL_ROOT_PASSWORD="rootpassword"
MYSQL_EDX_PASSWORD="edxpassword"
MONGO_ROOT_PASSWORD="mongopassword"
MONGO_EDX_PASSWORD="edxmongo"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_status "Docker and Docker Compose are installed"
}

# Clone the edx-platform repository
clone_edx_platform() {
    if [ -d "$EDX_PLATFORM_DIR" ]; then
        print_status "edx-platform directory already exists, skipping clone"
        return 0
    fi
    
    print_status "Cloning edx-platform repository..."
    if git clone https://github.com/openedx/edx-platform.git; then
        print_status "Successfully cloned edx-platform"
    else
        print_error "Failed to clone edx-platform repository"
        exit 1
    fi
}

# Remove Git files
remove_git_files() {
    print_status "Removing Git-related files..."
    cd $EDX_PLATFORM_DIR
    
    # Remove Git files and directories
    rm -rf .git .github .gitignore .gitattributes
    
    cd ..
}

# Create Docker Compose file
create_docker_compose() {
    print_status "Creating Docker Compose configuration..."
    
    cat > docker-compose.yml << EOF
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: openedx_mysql
    environment:
      MYSQL_ROOT_PASSWORD: $MYSQL_ROOT_PASSWORD
      MYSQL_DATABASE: openedx
      MYSQL_USER: openedx
      MYSQL_PASSWORD: $MYSQL_EDX_PASSWORD
    volumes:
      - mysql_data:/var/lib/mysql
      - ./config/mysql.cnf:/etc/mysql/conf.d/custom.cnf
    ports:
      - "3306:3306"
    networks:
      - $DOCKER_NETWORK
    restart: unless-stopped
    command: --default-authentication-plugin=mysql_native_password

  mongodb:
    image: mongo:7.0
    container_name: openedx_mongodb
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: $MONGO_ROOT_PASSWORD
      MONGO_INITDB_DATABASE: openedx
    volumes:
      - mongo_data:/data/db
    ports:
      - "27017:27017"
    networks:
      - $DOCKER_NETWORK
    restart: unless-stopped

  memcached:
    image: memcached:alpine
    container_name: openedx_memcached
    ports:
      - "11211:11211"
    networks:
      - $DOCKER_NETWORK
    restart: unless-stopped

  openedx:
    build:
      context: ./$EDX_PLATFORM_DIR
      dockerfile: ../Dockerfile
    container_name: openedx_app
    environment:
      - DJANGO_SETTINGS_MODULE=lms.envs.production
      - SERVICE_VARIANT=lms
      - EDX_PLATFORM_SETTINGS=production
      - MYSQL_HOST=mysql
      - MYSQL_PORT=3306
      - MYSQL_DATABASE=openedx
      - MYSQL_USER=openedx
      - MYSQL_PASSWORD=$MYSQL_EDX_PASSWORD
      - MONGO_HOST=mongodb
      - MONGO_PORT=27017
      - MONGO_USER=root
      - MONGO_PASSWORD=$MONGO_ROOT_PASSWORD
      - MEMCACHED_HOST=memcached
      - MEMCACHED_PORT=11211
    volumes:
      - ./$EDX_PLATFORM_DIR:/openedx/edx-platform
      - static_assets:/openedx/staticfiles
      - media_assets:/openedx/media
      - pip_cache:/root/.cache/pip
    ports:
      - "8000:8000"
    depends_on:
      - mysql
      - mongodb
      - memcached
    networks:
      - $DOCKER_NETWORK
    restart: unless-stopped
    command: >
      sh -c "
      echo 'Waiting for databases to be ready...' &&
      sleep 20 &&
      echo 'Running migrations...' &&
      python manage.py lms migrate --settings=production &&
      python manage.py cms migrate --settings=production &&
      echo 'Collecting static files...' &&
      python manage.py lms collectstatic --noinput --settings=production &&
      python manage.py cms collectstatic --noinput --settings=production &&
      echo 'Starting application...' &&
      gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 300 lms.wsgi:application
      "

volumes:
  mysql_data:
  mongo_data:
  static_assets:
  media_assets:
  pip_cache:

networks:
  $DOCKER_NETWORK:
    driver: bridge
EOF

    print_status "Docker Compose file created"
}

# Create Dockerfile
create_dockerfile() {
    print_status "Creating Dockerfile for Open edX..."
    
    cat > Dockerfile << EOF
FROM ubuntu:24.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHON_VERSION=3.11 \
    NODE_VERSION=18.17.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    libpq-dev \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    python3.11-venv \
    python3-pip \
    wget \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js using NVM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install 18.17.0 && nvm use 18.17.0
ENV PATH="/root/.nvm/versions/node/v18.17.0/bin:$PATH"

# Create application directory
RUN mkdir -p /openedx
WORKDIR /openedx/edx-platform

# Copy the application code
COPY . .

# Create Python virtual environment
RUN python3.11 -m venv /openedx/venv
ENV PATH="/openedx/venv/bin:$PATH"

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install -r requirements/edx/assets.txt && \
    pip install -r requirements/edx/base.txt && \
    pip install -r requirements/edx/production.txt && \
    pip install gunicorn mysqlclient

# Install frontend dependencies
RUN npm clean-install --production

# Create necessary directories
RUN mkdir -p /openedx/staticfiles /openedx/media /openedx/logs

# Set proper permissions
RUN chmod -R 755 /openedx

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/ || exit 1
EOF

    print_status "Dockerfile created"
}

# Create MySQL configuration
create_mysql_config() {
    print_status "Creating MySQL configuration..."
    
    mkdir -p config
    
    cat > config/mysql.cnf << EOF
[mysqld]
default-authentication-plugin=mysql_native_password
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
max_connections=1000
innodb_buffer_pool_size=1G

[client]
default-character-set=utf8mb4
EOF

    print_status "MySQL configuration created"
}

# Build and start the containers
start_containers() {
    print_status "Building and starting Docker containers..."
    
    # Create Docker network if it doesn't exist
    if ! docker network inspect $DOCKER_NETWORK >/dev/null 2>&1; then
        docker network create $DOCKER_NETWORK
    fi
    
    # Build and start containers
    docker-compose up --build -d
    
    print_status "Containers are starting. This may take several minutes..."
    print_status "You can check the logs with: docker-compose logs -f"
}

# Wait for application to be ready
wait_for_application() {
    print_status "Waiting for Open edX to be ready..."
    
    # Wait for the application container to be running
    while true; do
        CONTAINER_STATUS=$(docker inspect -f '{{.State.Status}}' openedx_app 2>/dev/null || echo "not found")
        if [ "$CONTAINER_STATUS" = "running" ]; then
            break
        fi
        sleep 5
    done
    
    # Wait for the application to respond
    while true; do
        if curl -f http://localhost:8000/ >/dev/null 2>&1; then
            break
        fi
        sleep 10
    done
    
    print_status "Open edX is ready!"
}

# Display completion message
show_completion() {
    echo "=============================================="
    echo "Open edX Setup Complete!"
    echo "=============================================="
    echo ""
    echo "Open edX is now running at: http://localhost:8000"
    echo ""
    echo "To stop the containers: docker-compose down"
    echo "To restart the containers: docker-compose restart"
    echo "To view logs: docker-compose logs -f"
    echo ""
    echo "Note: The first time setup may take a while"
    echo "as databases are initialized and migrations are run."
    echo ""
    echo "Default credentials:"
    echo "MySQL:"
    echo "  Root user: root / $MYSQL_ROOT_PASSWORD"
    echo "  Open edX user: openedx / $MYSQL_EDX_PASSWORD"
    echo "MongoDB:"
    echo "  Root user: root / $MONGO_ROOT_PASSWORD"
    echo "=============================================="
}

# Main execution
main() {
    print_status "Starting Open edX production setup..."
    
    # Check Docker is available
    check_docker
    
    # Clone the repository
    clone_edx_platform
    
    # Remove Git files
    remove_git_files
    
    # Create configuration files
    create_docker_compose
    create_dockerfile
    create_mysql_config
    
    # Start the containers
    start_containers
    
    # Wait for application to be ready
    wait_for_application
    
    # Display completion message
    show_completion
}

# Run the main function
main "$@"
