# Data Analytics Dashboard Starter Kit

## Overview

The Data Analytics Dashboard Starter Kit is an open-source project designed to provide a robust foundation for building data analytics dashboards. This project leverages [Neon](https://neon.tech/docs/introduction), a serverless Postgres solution, to store and manage data, while [Streamlit](https://docs.streamlit.io/) is used to create an interactive web-based dashboard. [Airflow (via Astronomer)](https://airflow.apache.org/docs/apache-airflow/stable/index.html) orchestrates the data ingestion and processing, automating the workflow of fetching, transforming, and loading data from external APIs into Neon.

This setup is ideal for individuals who may not have extensive experience with backend or frontend development but wish to quickly build a proof of concept (POC) or a functional data dashboard. All that's needed is a basic understanding of Python.

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

## Pricing Tiers for Technologies

Here's a breakdown of the pricing models for each technology used in the Data Analytics Dashboard Starter Kit:

| Technology          | Pricing Tier                | Description                                                                                                             |
|---------------------|-----------------------------|-------------------------------------------------------------------------------------------------------------------------|
| **Neon**            | Free                        | $0/month. Includes 0.5 GiB storage, 24/7 database at 0.25 CU, Autoscaling up to 2 CU, 1 project, 10 branches. [More info](https://console.neon.tech/app/billing#plans). |
| **Astronomer (Airflow)** | Free Trial                | 14-day trial with $300 in credits. Includes 1 Workspace, 1 Deployment, up to 5 workers per worker queue, A5, A10, or A20 workers. [More info](https://www.astronomer.io/docs/astro/trial). |
| **CoinGecko API**   | Free Demo (Beta)            | Free tier with 10K API calls per month and some limitations. [More info](https://www.coingecko.com/en/api/pricing).    |
| **Streamlit Cloud** | Free                        | Free to deploy, manage, and share your apps with the world, directly from Streamlit.                                    |


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

To get started with the Data Analytics Dashboard Starter Kit, you can either clone or fork the repository from GitHub. Use the following command to clone the repository:

```bash
git clone https://github.com/olgazju/data_analytics_dashboard_starter_kit.git
```

After cloning, navigate to the root folder of the project:

```bash
cd data_analytics_dashboard_starter_kit
```

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
  
  Set the local Python version to the virtual environment you just created:
  
  ```bash
  pyenv local da_kit
  ```

</details>

<details>
  <summary>Click here to see Docker setup</summary>

  #### Steps to Run the Application

  1. Ensure Docker and Docker Compose are installed on your machine. You can download and install [Docker](https://www.docker.com/products/docker-desktop/) from Docker's official website.
  2. Navigate to the Project Directory: Open a terminal and navigate to the root directory of the project where the `compose.yaml` file is located.
  3. Run the following command to build the Docker image for the frontend app and start the containers:
  
      ```bash
      docker-compose up --build
  
      ```
  
      This command will:
  
      - Build the Docker image for the `streamlit` app using its Dockerfile.
      - Start the containers and run the applications.
   4. Open a web browser and go to `http://localhost:8501`. This will take you to the Streamlit application interface.

</details>

<details>
  <summary>Click here to see more about the .env local file</summary>

  Remember to create a `.env` file in the root folder using `touch .env`. This file is excluded from GitHub, so it's safe to store your sensitive information here. If you want to test access to Neon or other services locally, you can keep secrets such as the Neon connection string or the CoinGecko API token in this file.

  Example of what you might include in your `.env` file:
  ```
    NEON_DB_URL=your_neon_connection_string 
    COIN_API_TOKEN=your_coin_api_token
  ```
</details>

**2. Setup CoingGecko API usage**

**3. Setup Neon Database**

<details>
  <summary>Click here to see Neon setup</summary>

#### Neon Setup:

- Create an Account: Visit the [Neon website](https://neon.tech/docs/get-started-with-neon/signing-up) and follow the instructions to create a new account. The free tier allows you to have one project with 0.5 GiB storage.
- Project Dashboard: Once your account is created, you will be able to access the Neon project dashboard. This dashboard allows you to manage your database projects. Below is a screenshot of what the project dashboard looks like.

    <img width="1280" alt="image" src="https://github.com/user-attachments/assets/c6e5851b-6c06-43b2-add3-20aaaa2dde0b">

- Connection Link and Database Management: By clicking on your project, you can view the project dashboard. From here, you can obtain the connection link to your database and create new databases if needed. This connection link will be used later to connect your Streamlit app and Airflow instance to the Neon database.

    <img width="1279" alt="image" src="https://github.com/user-attachments/assets/14106837-d97b-4fa2-834c-ad4e6dff7c50">

As shown in the screenshot, the actual connection link is:

```
postgresql://da_db_owner:*******@ep-holy-band-a5en4z0k.us-east-2.aws.neon.tech/da_db?sslmode=require
```

- ep-holy-band-a5en4z0k.us-east-2.aws.neon.tech is the host.
- da_db is the database name.
- da_db_owner is the user.
- The password is the hidden part after the :.

This connection link will be used in different parts of this kit to connect your applications to the Neon database.

</details>

**4. Setup Astronomer Airflow**

deployment
connection in deployment
secret in deployment

**5. Setup Streamlit (Deployment)**

conneciton to NEON
secrets


