import socket  # Import the socket module to get network information
import logging  # Import logging module for log tracing
from flask import Flask, render_template, request  # Import Flask, render_template, and request from Flask

# Initialize the Flask application
app = Flask(__name__)

# Set up logging configuration
logging.basicConfig(level=logging.INFO)  # Log everything from INFO level upwards
logging.info("App started")  # Log when the app starts

def get_container_metadata():
    """Fetch container metadata like hostname, IP, and container ID."""
    try:
        # Get the hostname of the container (machine name)
        hostname = socket.gethostname()

        # Get the IP address associated with the hostname
        ip_address = socket.gethostbyname(hostname)

        # Read container ID from cgroup (Docker system information)
        with open("/proc/self/cgroup", "r") as f:
            lines = f.readlines()  # Read all lines in the cgroup file
            # Extract the container ID from the last line
            container_id = lines[-1].strip().split("/")[-1][:12]  # First 12 characters are the container ID
        logging.info(f"Container metadata retrieved: Hostname={hostname}, IP={ip_address}, Container ID={container_id}")
    except Exception as e:
        # In case of an error, log the error and set metadata values to "N/A"
        logging.error(f"Error retrieving container metadata: {e}")
        hostname, ip_address, container_id = "N/A", "N/A", "N/A"

    # Return a dictionary containing the container metadata
    return {"hostname": hostname, "ip": ip_address, "container_id": container_id}

@app.before_request
def log_request():
    """Log when a request is received."""
    logging.info(f"Received {request.method} request for {request.path}")

@app.route("/", methods=["GET", "POST"])
def index():
    """Main route that handles GET and POST requests."""
    result = None  # Initialize result as None
    if request.method == "POST":  # Check if the form was submitted via POST
        try:
            # Attempt to get the numbers from the form and convert them to floats
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            logging.info(f"Valid input: num1={num1}, num2={num2}")  # Log valid input
            result = num1 + num2  # Perform the addition
            logging.info(f"Calculation completed: {num1} + {num2} = {result}")  # Log the result
        except ValueError:
            # If input is not a valid number, log the error
            logging.error("Invalid input received")
            result = "Invalid input"  # Display error message on UI
    
    elif request.method == "GET":
        num1 = request.args.get("num1")  # Get the 'num1' query parameter from the URL
        num2 = request.args.get("num2")  # Get the 'num2' query parameter from the URL
        if num1 and num2:
            try:
                num1 = float(num1)  # Convert num1 to float
                num2 = float(num2)  # Convert num2 to float
                result = num1 + num2  # Perform the addition
                logging.info(f"Valid input (GET): num1={num1}, num2={num2}")  # Log valid input
                logging.info(f"Calculation completed (GET): {num1} + {num2} = {result}")  # Log the result
            except ValueError:
                # If input is not a valid number, log the error
                logging.error("Invalid input received (GET)")
    
    # Get container metadata and log it
    metadata = get_container_metadata()

    # Render the HTML page and pass the result and metadata to the template
    return render_template("index.html", result=result, metadata=metadata)

@app.after_request
def log_response(response):
    """Log after the request is completed and a response is sent."""
    logging.info(f"Request to {request.path} completed with status {response.status}")
    return response

@app.errorhandler(Exception)
def handle_error(e):
    """Log any unhandled errors."""
    logging.error(f"An error occurred: {e}")
    return "Internal Server Error", 500

if __name__ == "__main__":
    # Run the Flask app on 0.0.0.0 (accessible from outside the container)
    app.run(host="0.0.0.0", port=5000)