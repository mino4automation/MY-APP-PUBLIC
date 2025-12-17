# Flask Container Demo App

A simple Flask application designed to demonstrate container metadata retrieval and basic request handling.

## Features
- **Arithmetic Calculator**: Adds two numbers via UI or API.
- **System Metadata**: Displays Container ID, Hostname, and IP Address.
- **Docker Ready**: Includes `Dockerfile` and `docker-compose.yml` for easy deployment.

## Getting Started

### Prerequisites
- Python 3.x
- Docker (optional)

### Local Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```
   The app will start at `http://localhost:5000`.

### Docker Setup

1. **Build and Run**
   ```bash
   docker-compose up --build
   ```

## API Usage

### `GET /`
Returns the main page.
- **Parameters**:
    - `num1` (optional): First number.
    - `num2` (optional): Second number.
- **Example**: `http://localhost:5000/?num1=5&num2=10`

### `POST /`
Submits the form to calculate the sum.
- **Form Data**:
    - `num1`: First number.
    - `num2`: Second number.
