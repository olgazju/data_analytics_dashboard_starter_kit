# Data Analytics Dashboard Starter Kit
An easy-to-use Data Analytics Dashboard Starter Kit with FastAPI, Neon, Airflow, and Streamlit. Designed to help developers get started with Neon and quickly integrate, process, and visualize data for building analytics applications.


### **Project Architecture Overview**

1. **Airflow**:
    - **Role**: Orchestrates data workflows. Airflow will handle tasks like extracting data from various sources (APIs, databases, flat files), transforming the data using Python scripts or SQL, and loading it into the Neon database.
    - **Tasks**:
        - **Extract**: Pull data from various sources such as APIs, CSV files, or other databases.
        - **Transform**: Clean and preprocess the data using Python scripts, Pandas, or SQL transformations.
        - **Load**: Insert the transformed data into Neon using the SQLAlchemy library or directly through a connection to Neon.
2. **Neon (Postgres Database)**:
    - **Role**: Serves as the main data storage. Neon will store the transformed data that Airflow loads. It will handle data querying and provide the necessary data for visualization.
    - **Functionality**: Supports scalability, automated backups, and point-in-time recovery, making it a reliable choice for storing business-critical data.
3. **FastAPI**:
    - **Role**: Acts as the backend API server that interfaces with the Neon database using SQLAlchemy. It exposes endpoints for querying, processing, and serving data to the visualization layer.
    - **Integration with SQLAlchemy**:
        - FastAPI uses SQLAlchemy to handle database operations, including querying, inserting, updating, and deleting data from Neon. This provides a robust and efficient way to manage interactions with the database.
4. **Streamlit**:
    - **Role**: Provides the user interface for data visualization. Streamlit will consume data from FastAPI and offer interactive dashboards for exploring and analyzing the data.
    - **Functionality**:
        - Display tables, charts, and graphs.
        - Allow users to interact with the data through filters and query options.
        - Provide insights and analytics through customizable visual elements.

### **Data Flow and Interaction**

1. **Data Source to Airflow**: Airflow pulls data from external sources, which could be APIs, CSV files, databases, or cloud storage.
2. **Airflow to Neon**: Airflow processes and transforms the data, then loads it into the Neon database.
3. **Neon to FastAPI**: FastAPI queries Neon for data based on user requests or pre-defined analytics needs.
4. **FastAPI to Streamlit**: FastAPI sends the processed data to Streamlit, which then visualizes it in the dashboard for end-users.


## Project Setup

Follow these steps to set up the Python environment for the project:

### 1. Install `pyenv` and `pyenv-virtualenv`

Make sure you have Homebrew installed, then run the following commands to install `pyenv` and `pyenv-virtualenv`:

```bash
brew install pyenv
brew install pyenv-virtualenv
```

### 2. Install Python

Use `pyenv` to install the desired version of Python. In this project, we are using Python 3.12.0:

```bash
pyenv install 3.12.0
```

### 3. Create a Virtual Environment

Create a virtual environment named `da_kit` using `pyenv-virtualenv`:

```bash
pyenv virtualenv 3.12.0 da_kit
```

### 4. Connect the Virtual Environment to the Project Directory

Navigate to your project directory and set the local Python version to the virtual environment you just created:

```bash
pyenv local da_kit
```

## Running the Application with Docker Compose

This project utilizes Docker Compose to run both the Streamlit frontend and the FastAPI backend services. Follow these instructions to build and start the application using Docker Compose.

### Prerequisites

- Ensure Docker and Docker Compose are installed on your machine. You can download and install Docker from Docker's official website.

### Steps to Run the Application

1. **Navigate to the Project Directory**:
Open a terminal and navigate to the root directory of the project where the `docker-compose.yml` file is located.
2. **Build and Start the Containers**:
Run the following command to build the Docker images for both the frontend and backend services and start the containers:

    ```bash
    bashCopy code
    docker-compose up --build

    ```

    This command will:

    - Build the Docker images for the `streamlit` and `fastapi` services using their respective Dockerfiles.
    - Start the containers and run the applications.
3. **Access the Applications**:
    - **Streamlit Frontend**: Open a web browser and go to `http://localhost:8501`. This will take you to the Streamlit application interface.
    - **FastAPI Backend**: The FastAPI backend is accessible at `http://localhost:8000`. You can view the API documentation generated by FastAPI at `http://localhost:8000/docs`.
