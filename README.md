# Data Analytics Dashboard Starter Kit

## Overview

The Data Analytics Dashboard Starter Kit is an open-source project designed to provide a robust foundation for building data analytics dashboards. This project leverages [Neon](https://neon.tech/docs/introduction), a serverless Postgres solution, to store and manage data, while [Streamlit](https://docs.streamlit.io/) is used to create an interactive web-based dashboard. [Airflow (via Astronomer)](https://airflow.apache.org/docs/apache-airflow/stable/index.html) orchestrates the data ingestion and processing, automating the workflow of fetching, transforming, and loading data from external APIs into Neon.

For demonstration purposes, this kit uses cryptocurrency data fetched from the [CoinGecko API](https://docs.coingecko.com/v3.0.1/reference/introduction). However, the framework is highly adaptable and can be utilized with any type of data, making it a versatile starting point for developers.


## Project Components

### Neon PostgreSQL Database:
Neon is used as the scalable, serverless PostgreSQL database for this starter kit. It efficiently manages and stores data, making it suitable for a wide range of applications.

### Streamlit Dashboard:
Streamlit provides an intuitive, interactive dashboard for real-time data visualization. It allows users to interact with the data directly from the Neon database, showcasing how Streamlit can be used for creating engaging visualizations and interfaces.

### Airflow (via Astronomer):
Airflow handles the automation of data workflows, ensuring data is efficiently fetched, processed, and loaded into Neon. It manages both historical data loads and scheduled incremental updates, demonstrating how to maintain up-to-date data integration with external sources.

### Data Source

#### CoinGecko API:
The CoinGecko API provides real-time and historical cryptocurrency market data, including OHLC, market cap, volume, and more.

## Key Features Demonstrated in This Project

- **Smooth Integration:** Understand how to connect Neon, Streamlit, and Airflow using Python to build a unified data analytics platform.
- **Interactive Data Visualization:** Learn how to create real-time, interactive dashboards using Streamlit.
- **Automated Data Collection:** See how Airflow automates the process of fetching and processing data from external APIs.
- **Effortless Filtering and Analysis:** Experience dynamic filtering options that make it easy to analyze data through a simple interface.

## Project Structure
The project is organized into several key directories and files to ensure consistent development, deployment, and operation:

- **`astronomer/`**: This folder is designated for the Airflow cloud solution, Astronomer. Within it:
    - **`dags/`**: Contains Airflow DAGs that orchestrate the ETL processes, pulling data from external APIs and loading it into the Neon database. This directory is also packaged into a Docker image, which includes a Dockerfile for containerization.
- **`frontend/`**: Includes Streamlit app files.
    - **`app.py`**: The main Streamlit app file that defines the dashboard functionality.
    - **`requirements.txt`**: Specifies the dependencies for the Streamlit app, ensuring all necessary packages are installed.
    - A Dockerfile is used to package the Streamlit app for deployment.
- **`README.md`**: Provides an overview of the project, setup instructions, and other relevant documentation.

Additionally, in the root directory:

- **`.pre-commit-config.yaml`**: Configuration for pre-commit hooks to maintain code quality.
- **`compose.yaml`**: Defines the Docker Compose configuration for orchestrating multi-container setups.

## Environment Setup

**1. Local Environment Setup (macOS)**

<details>
  <summary>Click here to see Python environment setup</summary>

  #### Install `pyenv` and `pyenv-virtualenv`
  
  Make sure you have Homebrew installed, then run the following commands to install `pyenv` and `pyenv-virtualenv`:
  
  ```bash
  brew install pyenv
  brew install pyenv-virtualenv
  ```
  
  #### Install Python
  
  Use `pyenv` to install the desired version of Python. In this project, we are using Python 3.12.0:
  
  ```bash
  pyenv install 3.12.0
  ```
  
  #### Create a Virtual Environment
  
  Create a virtual environment named `da_kit` using `pyenv-virtualenv`:
  
  ```bash
  pyenv virtualenv 3.12.0 da_kit
  ```
  
  #### Connect the Virtual Environment to the Project Directory
  
  Navigate to your project directory and set the local Python version to the virtual environment you just created:
  
  ```bash
  pyenv local da_kit
  ```

</details>

<details>
  <summary>Click here to see Docker setup</summary>


  This project utilizes Docker Compose to run Streamlit frontend. Follow these instructions to build and start the application using Docker Compose.
  
  Ensure Docker and Docker Compose are installed on your machine. You can download and install [Docker](https://www.docker.com/products/docker-desktop/) from Docker's official website.
  
  - #### Steps to Run the Application

  1. **Navigate to the Project Directory**:
  Open a terminal and navigate to the root directory of the project where the `docker-compose.yml` file is located.
  2. **Build and Start the Containers**:
  Run the following command to build the Docker images for both the frontend and backend services and start the containers:
  
      ```bash
      bashCopy code
      docker-compose up --build
  
      ```
  
      This command will:
  
      - Build the Docker images for the `streamlit` app using its Dockerfile.
      - Start the containers and run the applications.

</details>


