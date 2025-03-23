import socket  # Import the socket module to get network information
from flask import Flask, render_template, request  # Import Flask, render_template, and request from Flask

app = Flask(__name__)  # Initialize the Flask application

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
    except Exception:
        # In case of an error, set the metadata values to "N/A"
        hostname, ip_address, container_id = "N/A", "N/A", "N/A"

    # Return a dictionary containing the container metadata
    return {"hostname": hostname, "ip": ip_address, "container_id": container_id}

@app.route("/", methods=["GET", "POST"])
def index():
    result = None  # Initialize result to None
    if request.method == "POST":  # Check if the form was submitted via POST
        try:
            # Attempt to get the numbers from the form and convert them to floats
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            result = num1 + num2  # Add the numbers if valid
        except ValueError:
            result = "Invalid input"  # If input is not a valid number, show error message

    # Get container metadata by calling the get_container_metadata function
    metadata = get_container_metadata()

    # Render the HTML page and pass the result and metadata to the template
    return render_template("index.html", result=result, metadata=metadata)

if __name__ == "__main__":
    # Run the Flask app on 0.0.0.0 (accessible from outside the container)
    app.run(host="0.0.0.0", port=5000)
    