import socket  # Import the socket module to get network information like hostname and IP
import logging  # Import logging module to track events and errors in the application
from flask import Flask, render_template, request  # Import Flask for the web app, render_template for HTML, and request for handling inputs

# Initialize the Flask application
app = Flask(__name__)  # Create a new Flask web application instance

# Set up logging configuration
logging.basicConfig(level=logging.INFO)  # Configure logging to show all messages at INFO level and above
logging.info("App started")  # Log a message indicating the application has successfully started

def get_container_metadata():
    """Fetch container metadata like hostname, IP, and container ID."""
    try:
        # Get the hostname of the container (machine name)
        hostname = socket.gethostname()  # Call the socket library to retrieve the current machine's hostname

        # Get the IP address associated with the hostname
        ip_address = socket.gethostbyname(hostname)  # Resolve the hostname to an IP address using the socket library

        # Read container ID from cgroup (Docker system information)
        with open("/proc/self/cgroup", "r") as f:  # Open the cgroup file which contains container details
            lines = f.readlines()  # Read all lines from the file into a list
            # Extract the container ID from the last line
            container_id = lines[-1].strip().split("/")[-1][:12]  # Parse the last line to find the container ID and take the first 12 characters
        logging.info(f"Container metadata retrieved: Hostname={hostname}, IP={ip_address}, Container ID={container_id}")  # Log the retrieved metadata
    except Exception as e:
        # In case of an error, log the error and set metadata values to "N/A"
        logging.error(f"Error retrieving container metadata: {e}")  # Log the specific error that occurred
        hostname, ip_address, container_id = "N/A", "N/A", "N/A"  # Set default values if retrieval fails

    # Return a dictionary containing the container metadata
    return {"hostname": hostname, "ip": ip_address, "container_id": container_id}  # Return the data as a dictionary

@app.before_request
def log_request():
    """Log when a request is received."""
    logging.info(f"Received {request.method} request for {request.path}")  # Log the HTTP method (GET/POST) and the path requested

@app.route("/", methods=["GET", "POST"])
def index():
    """Main route that handles GET and POST requests."""
    result = None  # Initialize result variable as None to store calculation output later
    if request.method == "POST":  # Check if the user submitted data via a POST request (e.g., clicking a button)
        try:
            # Attempt to get the numbers from the form and convert them to floats
            num1 = float(request.form["num1"])  # Get 'num1' from the form data and convert it to a decimal number
            num2 = float(request.form["num2"])  # Get 'num2' from the form data and convert it to a decimal number
            logging.info(f"Valid input: num1={num1}, num2={num2}")  # Log the valid numbers received from the user
            result = num1 + num2  # Add the two numbers together
            logging.info(f"Calculation completed: {num1} + {num2} = {result}")  # Log the result of the addition
        except ValueError:
            # If input is not a valid number, log the error
            logging.error("Invalid input received")  # Log that the input could not be converted to numbers
            result = "Invalid input"  # Set the result to an error message to show the user
    
    elif request.method == "GET":  # Check if the request is a GET request (e.g., loading the page or using URL parameters)
        num1 = request.args.get("num1")  # Try to get 'num1' from the URL query parameters
        num2 = request.args.get("num2")  # Try to get 'num2' from the URL query parameters
        if num1 and num2:  # Check if both numbers were provided in the URL
            try:
                num1 = float(num1)  # Convert 'num1' string to a float
                num2 = float(num2)  # Convert 'num2' string to a float
                result = num1 + num2  # Add the two numbers together
                logging.info(f"Valid input (GET): num1={num1}, num2={num2}")  # Log the valid inputs from the URL
                logging.info(f"Calculation completed (GET): {num1} + {num2} = {result}")  # Log the calculation result
            except ValueError:
                # If input is not a valid number, log the error
                logging.error("Invalid input received (GET)")  # Log that the URL parameters were invalid
    
    # Get container metadata and log it
    metadata = get_container_metadata()  # Call the helper function to get system info (hostname, IP, ID)

    # Render the HTML page and pass the result and metadata to the template
    return render_template("index.html", result=result, metadata=metadata)  # Send data to 'index.html' to display to the user

@app.after_request
def log_response(response):
    """Log after the request is completed and a response is sent."""
    logging.info(f"Request to {request.path} completed with status {response.status}")  # Log the status code sent back to the user
    return response  # Return the response object to be sent to the client

@app.errorhandler(Exception)
def handle_error(e):
    """Log any unhandled errors."""
    logging.error(f"An error occurred: {e}")  # Log any unexpected errors that crash the app
    return "Internal Server Error", 500  # Return a generic error message and a 500 status code

if __name__ == "__main__":
    # Run the Flask app on 0.0.0.0 (accessible from outside the container)
    app.run(host="0.0.0.0", port=5000)  # Start the web server, listening on all network interfaces at port 5000
