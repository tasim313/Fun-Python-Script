# Install missing dependencies
apt-get update && apt-get install -y libgl1
# Run the server
gunicorn -w 4 -b 0.0.0.0:8000 app:app
