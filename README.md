# Virtual Bank API

## Introduction

The Virtual Bank API and web application are designed as a comprehensive solution for developers and learners who need a safe and controlled environment to simulate banking transactions. Whether you’re an aspiring developer exploring the intricacies of APIs, a tester validating the robustness of e-commerce platforms, or a professional working on complex payment gateway integrations, Virtual Bank offers a versatile platform tailored to meet these needs.

Built on the powerful Django framework, Virtual Bank not only facilitates the simulation of transactions but also provides an extensive range of features, including account management, transaction histories, and user authentication. This makes it an ideal tool for educational purposes, development, and testing scenarios where using real bank APIs would be impractical or risky.

By leveraging Virtual Bank, developers can experiment freely, test different use cases, and gain hands-on experience with financial transactions all without the constraints or concerns of working with real banking systems. Whether you are building the next big fintech application or just beginning your journey in API development, Virtual Bank is here to support your learning and development needs.

![Virtual Bank Dasboard Screenshot](sample/sample.png)
# Table of Contents
- [Virtual Bank API](#virtual-bank-api)
  - [Introduction](#introduction)
- [Table of Contents](#table-of-contents)
  - [Use Cases](#use-cases)
  - [Installation](#installation)
    - [Using Docker (Recommended)](#using-docker-recommended)
    - [Docker Repository Overview](#docker-repository-overview)
      - [Repository Details](#repository-details)
      - [Image Features](#image-features)
      - [Image Tags](#image-tags)
      - [Using the Docker Image](#using-the-docker-image)
      - [Image Architecture](#image-architecture)
    - [Running Both API and Client Web Interface](#running-both-api-and-client-web-interface)
    - [Local Installation](#local-installation)
    - [Local Database Configuration:](#local-database-configuration)
    - [Neon Database Configuration (for Deployment)](#neon-database-configuration-for-deployment)
  - [Authentication (JWT and Cookies)](#authentication-jwt-and-cookies)
  - [Usage](#usage)
    - [Running the Development Server](#running-the-development-server)
    - [Create User](#create-user)
    - [Obtain JWT Token](#obtain-jwt-token)
    - [Create Account (using JWT token)](#create-account-using-jwt-token)
  - [WebSocket Integration](#websocket-integration)
  - [Project Status](#project-status)
  - [API Documentation](#api-documentation)
    - [Overview](#overview)
    - [Authentication](#authentication)
    - [Endpoints](#endpoints)
      - [**Admin Endpoints**](#admin-endpoints)
        - [Users Management](#users-management)
        - [Accounts Management](#accounts-management)
        - [Notifications Management](#notifications-management)
        - [Transactions Management](#transactions-management)
      - [**Public Endpoints**](#public-endpoints)
        - [Authentication](#authentication-1)
        - [Accounts](#accounts)
        - [Debit Cards](#debit-cards)
        - [Deposits](#deposits)
        - [Notifications](#notifications)
        - [Transactions](#transactions)
        - [Transfers](#transfers)
  - [Contributing](#contributing)
  - [Licensing](#licensing)
  - [Contact](#contact)



## Use Cases

Here are some potential ways the Virtual Bank API can be used, implemented, or integrated:

1. **Personal Finance Management Apps**: Integrate with personal finance tools to help users track expenses, incomes, and transfers between accounts.

2. **Banking as a Service (BaaS)**: Offer the API as a BaaS platform, enabling developers to build financial services apps with a ready-made backend.

3. **Integration with Payment Gateways**: Connect with external payment processors like PayPal, Stripe, or Flutterwave to enable deposits and withdrawals between virtual and real-world accounts.

4. **Mobile Banking Applications**: Extend the API to support a mobile app that allows users to manage accounts, perform real-time transactions, and view account history.

5. **E-Commerce Platforms**: Integrate with e-commerce platforms to handle transactions for payments, refunds, or wallet top-ups, enabling seamless online shopping experiences.

6. **Fintech APIs**: Implement as part of a larger fintech platform, allowing companies to offer bank-like services without building a full banking infrastructure.

7. **Integration with Analytics Tools**: Use the API with business analytics tools to generate reports and visualizations of transaction data, helping businesses track cash flow and financial health.

8. **Customizable Corporate Banking Solutions**: Enable businesses to manage internal funds, process payroll, or allocate budgets to departments using the API.

9. **Educational Tools**: Implement as a tool for teaching financial literacy, using the API to simulate real-world banking scenarios.

10. **API Gateway for Multiple Banking Services**: Integrate the Virtual Bank API with other banking APIs to create a unified platform for users to manage multiple accounts and services.

11. **Multi-Currency Support**: Enhance to support multiple currencies and use in a global financial application where users can hold and exchange different currencies.

12. **Blockchain Integration**: Integrate with blockchain technologies to create secure, decentralized banking solutions, allowing for blockchain-based transfers and transactions.

13. **Microloan Platforms**: Adapt or Enhance the API to enable peer-to-peer lending services, where users can request loans, track repayments, and manage interest rates.

14. **Digital Wallets for E-learning Platforms**: Integrate with e-learning platforms to offer students a digital wallet for course payments, scholarships, or reward systems.

## Installation

### Using Docker (Recommended)

The easiest way to get started with Virtual Bank is using Docker:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GoldenThrust/Virtual-Bank.git
   cd Virtual-Bank
   ```

2. **Use the Official Docker Image**:
   ```bash
   docker pull goldenthrust/virtual-bank
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your preferred settings.

4. **Start the Docker containers**:
   ```bash
   docker-compose up -d
   ```
   This will start PostgreSQL, Redis, and the Virtual Bank API server.

   **Troubleshooting Docker Connectivity Issues**:
   
   If you're experiencing network issues when trying to pull Docker images:
   
   a. **Configure alternative DNS**:
      ```powershell
      # For Windows
      mkdir -p .docker
      @'
      {
        "dns": ["8.8.8.8", "8.8.4.4"]
      }
      '@ | Out-File -FilePath .docker\config.json -Encoding utf8
      ```

### Docker Repository Overview

The Virtual Bank project provides an official Docker image available on Docker Hub to make deployment and testing easier for everyone.

#### Repository Details

- **Docker Hub Repository**: [goldenthrust/virtual-bank](https://hub.docker.com/r/goldenthrust/virtual-bank)
- **Latest Image**: `goldenthrust/virtual-bank:latest`

#### Image Features

- **All-in-One Solution**: Contains both API backend and client web frontend
- **Pre-configured**: Ready to connect to PostgreSQL and Redis
- **Environment Variables**: Fully customizable through environment variables
- **Production-Ready**: Optimized for both development and production use
- **Documentation**: Includes Swagger API documentation

#### Image Tags

- `latest`: Always points to the most recent stable release
- `x.y.z` (e.g., `1.0.0`): Version-specific tags for reproducible deployments

#### Using the Docker Image

The image can be used in various ways:

1. **Basic Usage**:
   ```bash
   docker run -p 8030:8030 -p 8040:8040 goldenthrust/virtual-bank
   ```

2. **With Environment Variables**:
   ```bash
   docker run -p 8030:8030 -p 8040:8040 \
     -e DB_HOST=my-postgres \
     -e DB_NAME=virtualbank \
     -e REDIS_HOST=my-redis \
     goldenthrust/virtual-bank
   ```

3. **With Docker Compose** (recommended):
   ```yaml
   # Sample docker-compose.yml snippet
   services:
     api:
       image: goldenthrust/virtual-bank
       ports:
         - "8030:8030"
       environment:
         - DB_HOST=db
         - REDIS_HOST=redis
       # ...other configuration
   ```

#### Image Architecture

The Docker image is based on Python 3.12 and includes:
- Django REST framework for the API
- Django for the client web application
- PostgreSQL client libraries
- Redis client libraries
- All required Python dependencies

### Running Both API and Client Web Interface

To run both the API backend and the client web frontend in Docker:

1. **Use the helper script**:
   
   **For Linux/macOS**:
   ```bash
   chmod +x start_app.sh
   ./start_app.sh
   ```
   
   **For Windows**:
   ```powershell
   .\start_app.ps1
   ```

2. **Or manually with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Access the applications**:
   - API: http://localhost:8030/api/
   - API Documentation: http://localhost:8030/swagger/
   - API Admin Interface: http://localhost:8030/admin/
   - Client Web Interface: http://localhost:8040/

4. **Create superusers** (optional):
   ```bash
   # For API
   docker-compose exec api python manage.py createsuperuser
   
   # For client web app
   docker-compose exec client python manage.py createsuperuser
   ```

5. **View logs**:
   ```bash
   # View logs for all services
   docker-compose logs -f
   
   # View logs for specific service
   docker-compose logs -f api
   docker-compose logs -f client
   ```

### Local Installation

To set up the Virtual Bank project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GoldenThrust/virtual-bank.git
   cd virtual-bank
   ```

2. **Create and activate a Python virtual environment:**

    #### For Linux (Ubuntu):
    Install the necessary packages, create and activate the virtual environment:
    ```bash
    sudo apt install python3.10-venv
    python3 -m venv venv
    source venv/bin/activate
    ```
    ### For macOS:
    Install Python 3 if not already installed (you can use Homebrew to install it), then create and activate the virtual environment:

    ``` bash
    python -m venv venv
    source venv/bin/activate
    ```
    
    If you don’t have Homebrew installed, you can install it by running:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    brew install python
    ```
    ### For Windows:
    Open the command prompt (or PowerShell) as an administrator.
    Run the following commands to create and activate the virtual environment:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
    Install pip (if necessary) and upgrade it:
    For all platforms (Linux, macOS, Windows):

    ```bash
    python -m pip install --upgrade pip
    ```

    Install project dependencies:
    Inside the activated virtual environment, run:

    ```bash
    python -m pip install -r requirements.txt
    ```
    ---
    **or**
    ---
    Run the installation script:
    ### For Linux/macOS:
    Make the installation script executable and run it:

    ```bash
    chmod +x install.sh
    ./install.sh
    ```

    ### For Windows:
    You may need to run the script manually if .sh files are not supported:

    ```bash
    bash install.sh
    ```

3. **Redis Setup for Django Channels**
   Register on Redis Cloud: Go to [Redis.io](https://redis.io) and register for a free Redis Cloud account. After registration, create a new Redis database instance and retrieve the connection URL.

   This URL will be used to configure Redis in your Django project.

   Add the Redis URL to your .env file: After setting up your Redis Cloud account, add the Redis connection URL to your .env file:

   ```ini
   REDIS_URL=redis://your_redis_cloud_url:6379
   ```

4. **Rename `.env-example` file in the root directory and edit environment variables**:
   ```ini
   DEV=TRUE
   SECRET_KEY=b309e3c3f0f6d3fb71a62617c100f59bb166a585b6b124d2
   JWT_KEY=00276c14dc8d8b2990a4b20024278907eccb2feec2a02eb8

   DB_USER=postgres
   DB_PASSWORD=*******
   DB_NAME=virtual_bank
   DB_HOST=localhost
   DB_PORT=5432

   PGHOST='example.us-east-2.aws.neon.tech'
   PGDATABASE='virtualbank'
   PGUSER='vb_owner'
   PGPASSWORD='*********'

   REDIS_URL=redis://your_redis_cloud_url:6379
   ```

   ### Local Database Configuration:
   - Default Configuration (PostgreSQL):
        - Configure your PostgreSQL database by creating a user with the provided credentials (DB_USER and DB_PASSWORD).
        If you need help setting up PostgreSQL, you can refer to the [official documentation](https://www.postgresql.org/docs/current/tutorial-start.html).
    - Other Databases:
        - For different databases, refer to the [Django documentation](https://docs.djangoproject.com/en/5.0/ref/databases/) on database setup.
   ```ini
   # .env file for local PostgreSQL
   DB_USER=your_db_username
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=virtualbank
   ```

   ### Neon Database Configuration (for Deployment)
   Neon is a cloud-native serverless Postgres solution that allows you to easily deploy scalable PostgreSQL databases. The Virtual Bank API project uses PostgreSQL for data management, and leveraging Neon for deployment provides a robust, cloud-based infrastructure with features like autoscaling, backups, and connection pooling.

   Steps to Set Up Neon PostgreSQL for Your Virtual Bank Project:
   - **Create an Account on Neon**:
   Visit [Neon.tech](https://neon.tech) and register for a free account. Neon offers a free tier, which is perfect for development and testing purposes.
   Once your account is created, you can access the Neon dashboard, where you'll be able to create and manage your PostgreSQL instances.
   
   - **Create a PostgreSQL Instance**:
   From the Neon dashboard, click on the button to create a new PostgreSQL instance.
   You can configure the database with any specifications needed, such as the region (e.g., us-east-2), scaling preferences, and performance options.
   After creating the instance, Neon will provide you with the connection details, including the host, database name, user, and password. Keep these details secure, as they will be used in your application to connect to the remote PostgreSQL database.
   Configure Your .env File: After setting up the PostgreSQL instance on Neon, you'll need to configure the connection information in your project's .env file. The .env file stores environment variables, which provide your Django application with the necessary credentials to connect to Neon.

   Here's an example of the necessary configuration:

   ```ini
   # .env file for Neon PostgreSQL
   DB_HOST='example.us-east-2.aws.neon.tech'  # The host address of your Neon database
   DB_NAME='virtualbank'                  # The name of your PostgreSQL database
   DB_USER='vb_owner'                         # The PostgreSQL user with access to the database
   DB_PASSWORD='your_password_here'           # The password for the database user
   ```
   - **DB_HOST**: The host address provided by Neon for your PostgreSQL instance.
   - **DB_NAME**: The name of the database you created (e.g., virtualbank).
   - **DB_USER**: The username associated with your PostgreSQL instance. Typically, this is the owner of the database (e.g., vb_owner).
   - **DB_PASSWORD**: The password that was set during the creation of the PostgreSQL instance.

   Modify Django Database Settings: In your Django settings.py file, you will need to use the above environment variables to configure the connection to Neon PostgreSQL. Modify your DATABASES configuration like this:
   
   ```python
   # For Neon PostgreSQL (deployment)
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql',
      'NAME': os.getenv('DB_NAME'),
      'USER': os.getenv('DB_USER'),
      'PASSWORD': os.getenv('DB_PASSWORD'),
      'HOST':  os.getenv('DB_HOST'),
      'PORT':  os.getenv('DB_PORT'),
      'OPTIONS': {
        'sslmode': 'require',
      },
    }
  }
   ```
1. **Run migrations**:
   ```bash
   cd api/
   python manage.py makemigrations
   python manage.py migrate
   ```

   **Clients**:
   ```bash
   cd clients/
   python manage.py makemigrations
   ```

2. **Start the development server**:
   **API**:
   ```bash
   cd api/
   python manage.py runserver
   ```

   **Clients**:
   ```bash
   cd clients/
   python manage.py runserver 8040
   ```

   Access the application in your browser at [http://localhost:8030/](http://localhost:8030/) or [http://localhost:8040/](http://localhost:8040/) for clients.

## Authentication (JWT and Cookies)

The Virtual Bank API uses JWT (JSON Web Token) for authentication. After logging in, you will receive a token that must be passed in all subsequent requests.

**Authorization Header**:
Include the JWT token in the Authorization header for all requests:
```http
Authorization: Bearer <your_token>
```

**As a Cookie**:
Alternatively, you can pass the JWT token as a Cookie:
```http
Cookie: jwt=<your_token>
```

## Usage

### Running the Development Server

To start the development server, navigate to the corresponding directories and run the following commands.

**For API**:
```bash
cd api/
python manage.py runserver
```

**For Clients**:
```bash
cd clients/
python manage.py runserver 8040
```

### Create User

To create a new user, use the following `curl` command:
```bash
curl -X POST http://localhost:8030/api/users/create/ \
-H 'Content-Type: application/json' \
-d '{
    "username": "max_miller",
    "password": "maxm1234",
    "first_name": "Max",
    "last_name": "Miller",
    "email": "max.miller@example.com",
    "address": "606 Oakwood Dr",
    "city": "Mountainview",
    "state": "CO",
    "country": "USA",
    "date_of_birth": "1998-01-22",
    "phone_number": "+199999999999"
}'
```

### Obtain JWT Token

After creating a user, obtain the JWT token by logging in:
```bash
curl -X POST http://localhost:8030/api/users/login/ \
-H 'Content-Type: application/json' \
-d '{
    "username": "max_miller",
    "password": "maxm1234"
}'
```

The response will contain the access token, which you can use for authenticated requests:
```json
{
    "access": "your_jwt_access_token",
    "refresh": "your_jwt_refresh_token"
}
```

### Create Account (using JWT token)

To create an account, use the JWT token obtained from the login step. Include the token in the Authorization header:
```bash
curl -X POST http://localhost:8030/api/accounts/create/ \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer your_jwt_access_token' \
-d '{
    "name": "Biznumd",
    "account_type": "CURRENT",
    "balance": 7500,
    "currency": "USD"
}'
```

Make sure to replace `your_jwt_access_token` with the actual token you received during login.

## WebSocket Integration

The API also supports WebSocket connections for real-time transaction and notification updates using Django Channels. Whenever a transaction is saved, a Django signal triggers a WebSocket event, providing instant updates to connected clients.

**Endpoint**: `/ws/socket/`

**Example Frontend WebSocket Listener**:
```javascript
const socket = new WebSocket("ws://localhost:8030/ws/socket/");

socket.addEventListener("message", (e) => {
  const data = JSON.parse(e.data);

  console.log(data.content, data.event);
  
  if (data.event === "transaction") {
  } else if (data.event === "notification") {
  }
});
```

## Project Status

The API is mostly finished, and I am currently working on the frontend. It is now possible to make transfers and deposits on the frontend with real-time updates and chart visualization of transactions.

![Virtual Bank Dashboard](sample/sample.gif)

## API Documentation

### Overview
This API provides endpoints for managing users, accounts, debit cards, deposits, notifications, transactions, transfers, and more. It includes both public and admin-only endpoints.

### Authentication
This API uses Both Basic and JWT (JSON Web Token) for authentication. The following endpoints are related to authentication:
 - Login: /auth/login/
 - Refresh Token: /auth/refresh/
 - Logout: /auth/logout/
After obtaining the token via login, include the JWT token in the Authorization header for all requests as follows:
Authorization: Bearer <your_token>
Or send the token has cookie


### Endpoints

#### **Admin Endpoints**

##### Users Management
- **List Users**  
  - **Endpoint:** `GET /admin/users/`
  - **Description:** Create a users or returns a list of all users (admin only).
  - **Authorization:** Bearer Token (Admin)
  - **Method:** GET, POST
  - **Request Body:** 
  ```json
  {
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string",
    "email": "user@example.com",
    "address": "string",
    "city": "string",
    "state": "string",
    "country": "string",
    "date_of_birth": "2019-08-24T14:15:22Z",
    "phone_number": -9223372036854776000,
    "date_joined": "2019-08-24T14:15:22Z"
  }
  ```

- **User Detail**  
  - **Endpoint:** `GET /admin/users/{id}/`
  - **Description:** Retrieves, delete, or update details of a specific user by their `id` (admin only).
  - **Authorization:** Bearer Token (Admin)
  - **Method:** GET, PUT, DELETE
  - **Request Body:** 
  ```json
  {
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string",
    "email": "user@example.com",
    "address": "string",
    "city": "string",
    "state": "string",
    "country": "string",
    "date_of_birth": "2019-08-24T14:15:22Z",
    "phone_number": -9223372036854776000,
    "date_joined": "2019-08-24T14:15:22Z"
  }
  ```

##### Accounts Management
- **List Accounts**  
  - **Endpoint:** `GET /admin/accounts/`
  - **Description:** Create Account or returns a list of all accounts (admin only).
  - **Authorization:** Bearer Token (Admin)
  - **Method:** GET, POST
  - **Request Body:** 
  ```json
  {
    "name": "string",
    "account_type": "SAVINGS",
    "balance": "string",
    "currency": "USD"
  }
  ```

- **Account Detail**  
  - **Endpoint:** `GET /admin/accounts/{id}/`
  - **Description:** Retrieves details of a specific account by its `id` (admin only).
  - **Authorization:** Bearer Token (Admin)
  - **Method:** GET, PUT, DELETE
  - **Request Body:** 
  ```json
  {
    "name": "string",
    "account_type": "SAVINGS",
    "balance": "string",
    "currency": "USD"
  }
  ```

##### Notifications Management
- **List Notifications**  
  - **Endpoint:** `GET /admin/notifications/`
  - **Description:** Create Notifications or returns a list of all notifications (admin only).
  - **Authorization:** Bearer Token (Admin)
  - **Method:** GET, POST
  - **Request Body:** 
  ```json
  {
    "user": 0,
    "notification_type": "USER_NOTIFICATION",
    "content": "string",
    "status": "READ"
  }
  ```

- **Notification Detail**  
  - **Endpoint:** `GET /admin/notifications/{id}/`
  - **Description:** Retrieves, delete, or update details of a specific notification by its `id` (admin only).
  - **Authorization:** Bearer Token (Admin)
  - **Method:** GET, PUT, DELETE
  - **Request Body:** 
  ```json
  {
    "user": 0,
    "notification_type": "USER_NOTIFICATION",
    "content": "string",
    "status": "READ"
  }
  ```

##### Transactions Management
- **List Transactions**  
  - **Endpoint:** `GET /admin/transactions/`
  - **Description:** create or returns a list of all transactions (admin only).
  - **Authorization:** Bearer Token (Admin)
  - **Method:** GET, POST
  - **Request Body:** 
  ```json
  {
    "transaction_type": "DEPOSIT",
    "amount_sent": "string",
    "amount_received": "string",
    "currency_sent": "USD",
    "currency_received": "USD",
    "description": "string",
    "rate": "string",
    "account": 0,
    "payer": 0,
    "payee": 0
  }
  ```

- **Transaction Detail**  
  - **Endpoint:** `GET /admin/transactions/{id}/`
  - **Description:** Retrieves, delete, or update details of a specific transaction by its `id` (admin only).
  - **Authorization:** Bearer Token (Admin)
  - **Method:** GET, PUT, DELETE
  - **Request Body:** 
  - **Request Body:** 
  ```json
  {
    "transaction_type": "DEPOSIT",
    "amount_sent": "string",
    "amount_received": "string",
    "currency_sent": "USD",
    "currency_received": "USD",
    "description": "string",
    "rate": "string",
    "account": 0,
    "payer": 0,
    "payee": 0
  }
  ```

---

#### **Public Endpoints**

##### Authentication
- **Verify Token**  
  - **Endpoint:** `POST /auth/token/verify/`
  - **Description:** Verifies the provided JWT token.
  - **Method:** POST
  - **Request Body:** 
  ```json
  {
    "token": "jwt_access_token"
  }
  ```

- **Register User** 
  Note: profile_picture can be  
  - **Endpoint:** `POST /auth/register/`
  - **Description:** Registers a new user.
  - **Method:** POST
  - **Request Body:** 
  ```json
  {
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string",
    "email": "user@example.com",
    "address": "string",
    "city": "string",
    "state": "string",
    "country": "string",
    "profile_picture": "image_file",
    "date_of_birth": "2019-08-24T14:15:22Z",
    "phone_number": -9223372036854776000,
    "date_joined": "2019-08-24T14:15:22Z"
  }
  ```
  - Notes:
      The profile_picture field is optional. If included, it should be uploaded as an image file in the form-data.

      For file uploads, ensure that your server is configured to handle multipart/form-data and save the uploaded files properly.

      If profile_picture is omitted, the user will be registered without a profile picture.
  
  - Handling File Uploads:
      As URL: Provide the URL of the image in the profile_picture field.
      
      As Base64 String: Provide the base64-encoded image string in the profile_picture field.
      
      As File Upload: Use multipart/form-data to include the file in the profile_picture field.


- **Update User**  
  - **Endpoint:** `PUT /auth/update/`
  - **Description:** Updates user information.
  - **Method:** PUT
  - **Request Body:** 
  ```json
  {
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "password": "string",
    "email": "user@example.com",
    "address": "string",
    "city": "string",
    "state": "string",
    "country": "string",
    "date_of_birth": "2019-08-24T14:15:22Z",
    "phone_number": -9223372036854776000,
    "date_joined": "2019-08-24T14:15:22Z"
  }
  ```

- **Verify User**  
  - **Endpoint:** `GET /auth/verify/`
  - **Description:** Retrieves the currently authenticated user's information.
  - **Method:** GET

- **Login**  
  - **Endpoint:** `POST /auth/login/`
  - **Description:** Logs in a user and returns a JWT token.
  - **Method:** POST
  - **Request Body:** 
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

- **Refresh Token**  
  - **Endpoint:** `POST /auth/token/refresh/`
  - **Description:** Refreshes the JWT token.
  - **Method:** POST'
  - **Request Body:** 
  ```json
  {
    "refresh": "jwt_refresh_token"
  }
  ```

- **Logout**  
  - **Endpoint:** `GET /auth/logout/`
  - **Description:** Logs out the user and invalidates the JWT token.
  - **Method:** GET

##### Accounts
- **List User Accounts**  
  - **Endpoint:** `GET /accounts/`
  - **Description:** Returns a list of all accounts associated with the authenticated user.
  - **Method:** GET

- **Create Account**  
  - **Endpoint:** `POST /accounts/create/`
  - **Description:** Creates a new account for the authenticated user.
  - **Method:** POST
  - **Request Body:** 
  ```json
  {
    "name": "string",
    "account_type": "SAVINGS | CURRENT",
    "balance": "string",
    "currency": "USD"
  }
  ```

- **Account Detail**  
  - **Endpoint:** `GET /accounts/{account_number}/`
  - **Description:** Retrieves details of a specific account by its `account_number`.
  - **Method:** GET

##### Debit Cards
- **List User Debit Cards**  
  - **Endpoint:** `GET /debit-cards/`
  - **Description:** Returns a list of all debit cards associated with the authenticated user.
  - **Method:** GET

- **Debit Card Detail**  
  - **Endpoint:** `GET /debit-cards/{card_number}/`
  - **Description:** Retrieves details of a specific debit card by its `card_number`.
  - **Method:** GET

- **List Debit Card Transactions**  
  - **Endpoint:** `GET /debit-cards/transactions/`
  - **Description:** Returns a list of transactions for the authenticated user's debit cards.
  - **Method:** GET
  - **Query Parameters:**:
    `role` (optional): The role of the authenticated user in the transaction (`payer`, `payee`).
    `account_number` (optional): Filters the transactions based on the specified account number.
    `page` (optional): The page number to retrieve. Defaults to 1 (the first page).
    `size` (optional): The number of results to return per page. Defaults to 100.


- **Debit Card Transaction Detail**  
  - **Endpoint:** `GET /debit-cards/transactions/{transaction_id}/`
  - **Description:** Retrieves details of a specific debit card transaction by its `transaction_identifier`.
  - **Method:** GET

- **Make Payment**  
  - **Endpoint:** `POST /debit-cards/payment/`
  - **Description:** Makes a payment using a debit card.
  - **Method:** POST
  - **Request Body:** 
  ```json
  {
      "amount": 0,
      "payee_account_number": 100000000,
      "card_number": 1000000000,
      "cvv": 100,
      "expiration_date": "22/08",
      "description": "string",
  }
  ```

##### Deposits
- **List User Deposits**  
  - **Endpoint:** `GET /deposits/`
  - **Description:** Returns a list of all deposits made by the authenticated user.
  - **Method:** GET

- **Create Deposit**  
  - **Endpoint:** `POST /deposits/create/`
  - **Description:** Creates a new deposit for the authenticated user.
  - **Method:** POST
  - **Request Body:** 
  ```json
  {
      "amount": 0,
      "account_number": 10000000000,
      "description": "string",
  }
  ```
  - **Query Parameters:**:
    `account_number` (optional): Filters the transactions based on the specified account number.
    `page` (optional): The page number to retrieve. Defaults to 1 (the first page).
    `size` (optional): The number of results to return per page. Defaults to 100.


- **Deposit Detail**  
  - **Endpoint:** `GET /deposits/{deposit_id}/`
  - **Description:** Retrieves details of a specific deposit by its **`deposit_id`**.
  - **Method:** GET

##### Notifications

- **List User Notifications**  
  - **Endpoint:** `GET /notifications/`
  - **Description:** Returns a list of notifications for the authenticated user.
  - **Method:** GET
  - **Query Parameters:**:
    `type` (optional): The type of notification to return. `user | account | transaction | security`
    `page` (optional): The page number to retrieve. Defaults to 1 (the first page).
    `size` (optional): The number of results to return per page. Defaults to 100.


- **Notification Detail**  
  - **Endpoint:** `GET /notifications/{id}/`
  - **Description:** Retrieves a specific notification by its `id`.
  - **Method:** GET

##### Transactions
- **List Transaction History**  
  - **Endpoint:** `GET /transactions/`
  - **Description:** Returns the transaction history for the authenticated user.
  - **Method:** GET
  - **Query Parameters:**:
    `role` (optional): The role of the authenticated user in the transaction (`payer`, `payee`).
    `account_number` (optional): Filters the transactions based on the specified account number.
    `page` (optional): The page number to retrieve. Defaults to 1 (the first page).
    `size` (optional): The number of results to return per page. Defaults to 100.


- **Transaction Detail**  
  - **Endpoint:** `GET /transactions/{transaction_id}/`
  - **Description:** Retrieves details of a specific transaction by its `transaction_identifier`.
  - **Method:** GET

##### Transfers
- **List User Transfers**  
  - **Endpoint:** `GET /transfers/`
  - **Description:** Returns a list of all transfers made by the authenticated user.
  - **Method:** GET
  - **Query Parameters:**:
    `role` (optional): The role of the authenticated user in the transaction (`payer`, `payee`).
    `account_number` (optional): Filters the transactions based on the specified account number.
    `page` (optional): The page number to retrieve. Defaults to 1 (the first page).
    `size` (optional): The number of results to return per page. Defaults to 100.


- **Create Transfer**  
  - **Endpoint:** `POST /transfers/create/`
  - **Description:** Creates a new transfer for the authenticated user.
  - **Method:** POST
  - **Request Body:** 
  ```json
  {
    "amount": 0,
    "payer_account_number": 100000000,
    "payee_account_number": 100000000,
    "description": "string"
  }
  ```

- **Transfer Detail**  
  - **Endpoint:** `GET /transfers/{transfer_id}/`
  - **Description:** Retrieves details of a specific transfer by its `transfer_identifier`.
  - **Method:** GET

## Contributing
Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: ``` git checkout -b feature/new-feature  ```
3. Make your changes and commit them: ``` git commit -m 'Add new feature' ```.
4. Push to the branch: ``` git push origin feature/new-feature ```.
5. Submit a pull request.

## Licensing
The Virtual Bank project is licensed under the MIT License, ensuring open-source availability and contributions from the community.

## Contact
For any inquiries or support, please contact Adeniji Olajide at [adenijiolajid01@gmail.com](mailto:adenijiolajid01@gmail.com).
