#!/bin/bash
# ----------------------------------------------------------------------
# AUTO SETUP AND RUN SCRIPT for Django Ledger (via Docker Compose)
# https://github.com/arrobalytics/django-ledger
# ----------------------------------------------------------------------

# --- Configuration ---
REPO_URL="https://github.com/arrobalytics/django-ledger.git"
PROJECT_DIR="django-ledger"
SERVICE_NAME="web" # Service name for the Django container

# --- Functions ---

# Function to clean up containers and resources
cleanup() {
    echo -e "\n\n🚨 Shutting down Django Ledger project..."
    if [ -d "$PROJECT_DIR" ]; then
        cd "$PROJECT_DIR"
        # Stop and remove all containers, networks, and volumes
        docker-compose down --volumes
        cd ..
    fi
    echo -e "✅ Project shut down and containers/volumes removed."
    echo "The source files remain in the '$PROJECT_DIR' directory."
    exit 0
}

# Trap Ctrl+C (SIGINT) and SIGTERM (kill command) signals to run cleanup
trap cleanup SIGINT SIGTERM

# --- Main Script Execution ---

echo "Starting automatic setup for Django Ledger..."
echo "This script requires **Git, Docker, and Docker Compose** to be installed."
echo "----------------------------------------------------------------------"

# 1. Clone the repository if it doesn't exist
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Cloning repository: $REPO_URL"
    git clone "$REPO_URL"
    if [ $? -ne 0 ]; then
        echo "❌ Error: Git clone failed. Check your network or Git installation."
        exit 1
    fi
else
    echo "Repository already exists in '$PROJECT_DIR'. Skipping clone."
fi

# Change to the project directory
cd "$PROJECT_DIR"
if [ $? -ne 0 ]; then
    echo "❌ Error: Could not change directory to '$PROJECT_DIR'."
    exit 1
fi

# 2. Build and start services (detached mode)
echo -e "\nBuilding Docker images and starting services..."
docker-compose up --build -d
if [ $? -ne 0 ]; then
    echo "❌ Error: Docker Compose failed to build or start services. Check your Docker installation."
    cleanup
fi

# 3. Wait for database to be ready (a simple wait)
echo "Waiting 15 seconds for the database to initialize..."
sleep 15

# 4. Run database migrations
echo -e "\nApplying Django database migrations..."
docker-compose exec $SERVICE_NAME python manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Error: Database migrations failed."
    cleanup
fi

# 5. Output Access Instructions
echo -e "\n----------------------------------------------------------------------"
echo "🎉 Setup Complete! Django Ledger is running."
echo "----------------------------------------------------------------------"
echo "1. Create an **Admin/Superuser** account by running this command:"
echo -e "   docker-compose exec $SERVICE_NAME python manage.py createsuperuser"
echo ""
echo "2. Access the application in your web browser at: **http://127.0.0.1:8000**"
echo "----------------------------------------------------------------------"

# 6. Keep the script running until the user terminates it
echo "The project will now run in the background."
echo "Press **Ctrl+C** to stop the project and clean up Docker resources."

# Infinite loop to keep the script running, waiting for trap signal
while true; do
    sleep 5
done
