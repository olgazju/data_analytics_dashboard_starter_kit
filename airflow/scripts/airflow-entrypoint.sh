#!/usr/bin/env bash

set -e

if [ "$1" == "init" ]; then
    # Check if migrations have already been applied
    if [ ! -f /opt/airflow/init-completed ]; then
        echo "Running database migrations..."
        airflow db migrate
        echo "Database migrations completed."

        echo "Creating default connections..."
        airflow connections create-default-connections

        # Create an admin user if it doesn't exist
        if ! airflow users list | grep -q 'admin'; then
            echo "Creating admin user..."
            airflow users create -r Admin -u admin -e admin@admin.com -f admin -l admin -p admin
        fi

        # Create a marker file to indicate that initialization is complete
        touch /opt/airflow/init-completed
    else
        echo "Initialization already completed. Skipping migrations."
    fi

    # Exit after initialization
    exit 0
fi

# Run the passed command (e.g., scheduler or webserver)
exec airflow "$@"
