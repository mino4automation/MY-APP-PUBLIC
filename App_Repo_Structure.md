# Application Repository Structure

This document explains what each file and folder in this project does, including hidden system folders.

## 📂 Root Folders

### `templates/`
**The Design Folder**. Contains the HTML files for the web pages.
-   **`index.html`**: The main interface of our calculator app.

### `.venv/`
**The Virtual Environment**. This is a self-contained "box" where Python installs the specific libraries for this project, keeping them separate from your computer's main Python.
-   **`Scripts/`** (Windows) or `bin/` (Mac/Linux): Contains executable files like `python.exe` and `pip.exe` specifically for this environment.
-   **`Lib/`**: Contains the actual code for the installed libraries (like `Flask`).
-   **`Include/`**: Contains C header files for Python packages (usually for advanced use).
-   **`pyvenv.cfg`**: A configuration file that points to the main Python installation being used.

### `.git/`
**The History Vault**. This hidden folder is where Git stores every version of your code.
-   **`hooks/`**: Scripts that run automatically before/comitting or pushing (e.g., to check for errors).
-   **`info/`**: Local configuration file often used for referencing excludes.
-   **`logs/`**: Records of changes made to references (bracnhes/tags).
-   **`objects/`**: The massive database of all your file contents, compressed and hashed.
-   **`refs/`**: Pointers to commit objects (branches like `main` and tags).
-   **`config`**: Local settings for this repository (like remote URL).
-   **`HEAD`**: A pointer to the current branch you are working on.

## 📄 Root Files

### `app.py`
**The Brain**. The main Python script that runs the Flask server, handles calculations, and fetches system metadata.

### `requirements.txt`
**The Shopping List**. Lists required Python packages (e.g., `Flask`) so they can be installed with `pip install -r requirements.txt`.

### `Dockerfile`
**The Blueprint**. Instructions for Docker to build a self-contained image of this application.

### `docker-compose.yml`
**The Manager**. A configuration file to easily run the container with settings like port mapping (5000:5000) and specific restart policies.

### `README.md`
**The Manual**. General instructions on how to use, install, and run the project.

### `CONTRIBUTING.md`
**The Rules**. Guidelines for developers, including coding standards and workflow steps.

### `.gitignore`
**The Ignore List**. Tells Git which files to intentionally skip (like `.venv` or `__pycache__`).
