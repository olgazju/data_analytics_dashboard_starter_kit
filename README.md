# Data Analytics Dashboard Starter Kit

## Overview

The Data Analytics Dashboard Starter Kit is an open-source project designed to provide a robust foundation for building data analytics dashboards. This project leverages [Neon](https://neon.tech/docs/introduction), a serverless Postgres solution, to store and manage data, while [Streamlit](https://docs.streamlit.io/) is used to create an interactive web-based dashboard. [Airflow (via Astronomer)](https://airflow.apache.org/docs/apache-airflow/stable/index.html) orchestrates the data ingestion and processing, automating the workflow of fetching, transforming, and loading data from external APIs into Neon.

This setup is ideal for individuals who may not have extensive experience with backend or frontend development but wish to quickly build a proof of concept (POC) or a functional data dashboard. All that's needed is a basic understanding of Python.

For demonstration purposes, this kit uses cryptocurrency data fetched from the [CoinGecko API](https://docs.coingecko.com/v3.0.1/reference/introduction). However, the framework is highly adaptable and can be utilized with any type of data, making it a versatile starting point for developers.

<img width="1512" alt="image" src="https://github.com/user-attachments/assets/3115250e-54fd-4e01-8455-0dcf82aadf43">

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
    - **`requirements.txt`**: Specifies the dependencies for the Airflow dags image.
    - A **Dockerfile** is used to package the Airflow dags for deployment.
- **`frontend/`**: Includes Streamlit app files.
    - **`app.py`**: The main Streamlit app file that defines the dashboard functionality.
    - **`requirements.txt`**: Specifies the dependencies for the Streamlit app, ensuring all necessary packages are installed.
    - A **Dockerfile** is used to package the Streamlit app for deployment.
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

<details>
  <summary>Click here to see how to use CoinGecko API with a free demo account</summary>
    
  #### To use the CoinGecko API with a free demo account, follow these steps:
    
  - Create a Free Demo Account: Sign up for a free demo account on CoinGecko by following the instructions in the User Guide.
  - Generate an API Key: After creating your account, generate an API key that you will use to make requests to the CoinGecko API. This API key is unique to your account and should be kept secure.
  - Keep Your API Key Safe: Ensure that you do not push your API key to GitHub or share it publicly. This is your secret token, and exposing it could lead to unauthorized access to your account.

  Here’s a code example demonstrating how to use the CoinGecko API to fetch OHLC data (OHLC data represents the Open, High, Low, and Close prices of an asset within a specific time period) for bitcoin for 30 days:

  ```Python
    import requests
    import pandas as pd
    import os
    
    def fetch_ohlc_data(coin_id, api_key, days=30, vs_currency='usd'):
        base_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
        headers = {
            "x-cg-demo-api-key": api_key
        }
        params = {
            "vs_currency": vs_currency,
            "days": days
        }
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            ohlc_df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close'])
            ohlc_df['date'] = pd.to_datetime(ohlc_df['timestamp'], unit='ms')
            return ohlc_df
        else:
            print(f"Failed to fetch data for {coin_id}: {response.status_code}")
            return pd.DataFrame()
    
    coin_id = 'bitcoin'
    api_key = os.getenv("COIN_TOKEN")  # Replace with your actual API key
    ohlc_data = fetch_ohlc_data(coin_id, api_key)
    
    print(ohlc_data.head())
  ```   

    
</details>

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

<details>
  <summary>Click here to see Astronomer setup</summary>

#### Astronomer Setup:

1. Create an Account: Follow [this link](https://www.astronomer.io/docs/astro/first-dag-onboarding) to create an account in Astro.
2. Set Up Organization and Workspace: After signing up, create your Organization and Workspace within Astro.
3. Set Up Astro Deployment: Once your workspace is ready, set up your Astro Deployment. This will allow you to run your Airflow DAGs.

   <img width="1248" alt="image" src="https://github.com/user-attachments/assets/f99514c3-6536-4304-89e1-0c30036eef27">
   
5. Access Environment Tab: Click on your deployment to access the **Environment** tab.
6. Create Secrets: In the **Environment** tab, create a secret for the CoinGecko API token and a connection to your Neon database. These secrets will be used in the Airflow DAG to authenticate and connect to the necessary services (An Airflow DAG (Directed Acyclic Graph) is a collection of tasks organized to run in a specific order, used to automate data workflows.)
    - **CoinGecko API Token**: This token is needed to authenticate API requests to CoinGecko. Don't forget to click on Secret checkbox.

      <img width="1285" alt="image" src="https://github.com/user-attachments/assets/38e0c2e0-88a1-42ad-95e1-7ad9b95d2817">

    - **Neon Database Connection**: This connection string will allow Airflow to interact with your Neon database.

      <img width="674" alt="image" src="https://github.com/user-attachments/assets/f880e6e6-c2b0-467b-91c1-974d8867644f">

    From the deployment page, you can also click on the "Open Airflow" button to access the real Airflow UI.

</details>

<details>
  <summary>Click here to see how to deploy dags image</summary>
    
  #### How to Deploy Dags Image:
  
  1. Navigate to the `astronomer` folder in your project directory.
  2. Use the command `astro login` to authenticate your Astronomer account.
  3. After successful login, deploy your DAGs by running the command `astro deploy`.
  4. You will be prompted to choose your Astro Deployment. Select the appropriate one from the list.
  5. Once selected, the deployment process will start (you will see DEPLOYING status).

  ![image](https://github.com/user-attachments/assets/3241b5a6-189d-47be-a60b-86ee74e5337d)

   Wait for it to complete, and your DAGs will be deployed to Astronomer.

  <img width="1287" alt="image" src="https://github.com/user-attachments/assets/c9c8fa5d-ae8b-4aef-b8be-b53de6d4ff71">

  For more detailed instructions, refer to the [Astronomer documentation on deploying DAGs](https://www.astronomer.io/docs/astro/deploy-dags).
</details>

**5. Setup Streamlit (Deployment)**

<details>
  <summary>Click here to see Streamlit setup</summary>

  #### Streamlit Setup:

  Create a `frontend/.streamlit/secrets.toml` file to store sensitive information, such as your connection details to Neon. This file helps keep your secrets secure when deploying your Streamlit app. For more details on how to manage secrets in Streamlit, refer to the official documentation [here](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management).

Streamlit utilizes the `secrets.toml` file to configure connections to databases like PostgreSQL, as demonstrated in the Streamlit [tutorial](https://docs.streamlit.io/develop/tutorials/databases/postgresql). To set up the connection, create a `secrets.toml` file with the following structure:

  ```toml
  [connections.postgresql]
  dialect = "postgresql"
  host = "ep-holy-band-a5en4z0k.us-east-2.aws.neon.tech"
  port = "5432"
  database = "da_db"
  username = "da_db_owner"
  password = "****"
  [token]
  coin_token = "****"
  ```

Also CoingGecko API token was added as a secret.

</details>  

<details>
  <summary>Click here to see Streamlit Deployment</summary>

  #### Streamlit Deployment:

  Follow this link to create an account on the Streamlit public cloud: [Streamlit Account Creation](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/create-your-account#step-1-primary-identity). Once your account is set up, click on "Create a new app," and you will be prompted to connect to your GitHub account. Connect your GitHub account and select the public repository containing your Streamlit app. After you have linked the repository, Streamlit will automatically start the deployment process. Wait for the deployment to complete, and your Data Analytics Dashboard will be live and accessible through a provided URL.
  
  To securely manage your app's secrets, such as API keys or database connection strings, follow the instructions here: [Streamlit Secrets Management](https://chatgpt.com/c/8a4b0249-d6dc-45b3-bf95-c8bb7acfc079#:~:text=Streamlit%20Secrets%20Management). If you have frontend/.streamlit/secrets.toml in your project you can just copy its content.

  Following the link https://share.streamlit.io/, you can see a list of all your deployed Streamlit apps. This interface allows you to manage your apps, view their status, and update them as needed. It provides a centralized place to track and interact with your deployed projects.

  <img width="1495" alt="image" src="https://github.com/user-attachments/assets/eea9f064-0046-44c0-9e2e-e9dba2f9a642">

</details>

## How to Use the Data Analytics Dashboard Starter Kit*

1. **Run the Historical DAG**: Start by running the historical data load DAG in Airflow (Astronomer). This will fetch OHLC (Open, High, Low, Close) data for the selected cryptocurrencies and load it into the Neon database.

<img width="1510" alt="image" src="https://github.com/user-attachments/assets/5621eeb1-7dc1-4b72-8a37-f68aa5be5f5c">


   
2. **Verify Data in Neon**: Once the DAG has completed, you can verify that the data has been successfully ingested by running a simple SQL query in Neon. Check the data to ensure it includes the OHLC values for the coins you are tracking.

<img width="1033" alt="image" src="https://github.com/user-attachments/assets/e93b870f-3ada-426f-959a-cccf9447c5be">


3. **View the Dashboard**: With the data loaded into Neon, navigate to your deployed Streamlit app using the provided link. Use the dashboard to visualize the cryptocurrency data, apply date filters, and observe the various metrics displayed. The dashboard shows metrics like market cap, current price, and 24-hour price change with visual indicators (arrows) for changes.

Note: For simplicity, this starter kit currently includes only 12 cryptocurrencies and a few select metrics to demonstrate functionality. However, it can be easily extended to support more coins and additional metrics as needed.
