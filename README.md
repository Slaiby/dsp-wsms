## Loan Eligibility Prediction 🚀
 
This repository contains the source code and documentation for a comprehensive Loan Eligibility Prediction Web Application and Monitoring System. The system includes components for making predictions, visualizing past predictions, model serving via an API, data ingestion with quality validation, scheduled predictions, and monitoring dashboards.
 
## Components ✨
The project comprises various components:
- **Web Application**:
Prediction Page: Allows users to make single or multiple predictions through a form or CSV file upload. Relies on a model API service for predictions.
Past Predictions Page: Enables users to view past predictions, with options to filter by date range and prediction source.
- **Model Service (API)**:
Provides endpoints for making predictions and retrieving past predictions, including the features used. Utilizes a PostgreSQL database for storing predictions and data quality issues.
- **Database**:
Utilizes PostgreSQL for storing model predictions and data quality problems.
 
- **Data Ingestion Job**:
Simulates continuous data flow by ingesting new data at regular intervals, validating data quality, saving data issues, and generating reports.
- **Prediction Job**:
Executes scheduled predictions on ingested data at regular intervals.
- **Monitoring Dashboards**:
Ingested Data Monitoring Dashboard: Helps the data operations team monitor ingested data problems.
Data Drift and Prediction Issues Dashboard: Aids ML engineers and data scientists in detecting model or application issues.
 
## Getting Started 🛠
 
This guide will help you set up the project locally for development and testing.
 
 
 
### Installing 🔧
 
Step-by-step guide to setting up your development environment:
 
1. **Clone the repository**: `git clone repo-url`
2. **Install the requirements**: `pip install -r requirements.txt`
 
### Environment Configuration
 
Important steps to correctly set up your environment, including creating a `.env` file with the correct PostgreSQL database connection details.
 
#### Resolving PostgreSQL Connection Issues
 
To resolve database connection issues like the `psycopg2.OperationalError: FATAL: role "root_user" does not exist`:
 
1. **Create the Role**: If `root_user` is your intended database user, create this role in PostgreSQL with:
   ```sql
   CREATE ROLE root_user WITH LOGIN PASSWORD 'your_password';
 
Replace 'your_password' with a secure password.
 
Grant Permissions: Grant necessary permissions to root_user, for instance:
 
```ALTER ROLE root_user CREATEDB;```
Adjust based on your project's requirements.
 
Verify Role: Use \du in PostgreSQL to list all roles and check that root_user is present with correct permissions.
 
Update Connection String: Make sure the .env file or application's database connection details correctly reference root_user and the password.
 
Restart PostgreSQL Service: Apply configurations by restarting the PostgreSQL service, typically with:
```sudo service postgresql restart```
 
Troubleshoot: If issues persist, recheck connection parameters including database name, host, port, and credentials for errors or typos.
has context menu