# Virtual Bank Web Application and API

## Introduction

Welcome to the Virtual Bank project! This web application and API were created to provide developers with a platform for simulating banking transactions. Whether you're testing e-commerce websites or exploring payment integrations, our project allows you to experiment without using real bank APIs. Built on Django, it offers a range of functionalities tailored for transaction simulation.

- [**Website**](http://www.virtualbank.tech/)
- **Author:** Adeniji Olajide 
  - [LinkedIn](https://www.linkedin.com/in/olajide-adeniji-0286a32a2/)
  - [Twitter](https://twitter.com/Goldenthrust3)
- [**Final Project Blog Article**](Pending)

![Virtual Bank](./screenshot/virtualbank-homepage.gif)

## Installation

To set up the Virtual Bank project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/virtual-bank.git
   cd virtual-bank
   ```
2. Run the installation script:
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
3. Create a .env file in the root directory and add the following environment variables:
    ```dotenv
    # .env file
    DB_USER=your_db_username
    DB_PASSWORD=your_db_password
    ```

4. Configure your database:
    - Default Configuration (PostgreSQL):
        - Configure your PostgreSQL database by creating a user with the provided credentials (DB_USER and DB_PASSWORD).
        If you need help setting up PostgreSQL, you can refer to the [official documentation](https://www.postgresql.org/docs/current/tutorial-start.html).
    - Other Databases:
        - For different databases, refer to the [Django documentation](https://docs.djangoproject.com/en/5.0/ref/databases/) on database setup.

4. Run migrations
    - API
    ```bash
    cd api/
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

    - Clients
    ```bash
    cd clients/
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```
5. Start the development server:
    - API
    ```bash
    cd api/
    python manage.py runserver
    ```

    - clients
    ```bash
    cd clients/
    python manage.py runserver
    ```
    Access the application in your browser at http://localhost:8000/.

## Usage

### Running the Development Server

To start the development server:

- **API:**
  - Navigate to the API directory:
    ```bash
    cd api/
    python manage.py runserver
    ```

    **Create User:**
    ```bash
    curl -X POST http://localhost/api/v1/users/create/ -H 'Content-Type: application/json;' -d '{
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
        "phone_number": "+199999999999",
    }'
    ```

    **Generate Authorization Key:**
    ```bash
    cd helper
    python3 authorizationkey.py
    # Output: username:password
    # Input: max_miller:maxm1234
    # Output Authorization Key: bWF4X21pbGxlcjptYXhtMTIzNA==
    ```

    **Create Account:**
    ```bash
    curl -X POST http://localhost/api/v1/accounts/create/ -H 'Content-Type: application/json; Authorization: Basic bWF4X21pbGxlcjptYXhtMTIzNA==' -d '{
        "name": "Biznumd",
        "account_type": "CURRENT",
        "balance": 7500,
        "currency": "USD"
    }'
    ```

- **Clients:**
  - Navigate to the Clients directory:
    ```bash
    cd clients/
    python3 manage.py runserver
    ```

Once the servers are running, access the application in your browser at http://localhost:8000/.

Additionally, the application is accessible on the official website - [Virtual Bank](http://www.virtualbank.tech).


## API Endpoints
The Virtual Bank API provides several endpoints for handling transactions.

### Users

#### User List (Admin Only)
- **Endpoint:** `/api/v1/users/`
- **Description:** Retrieves a list of users.
- **Method:** GET, POST
- **Authorization:** Basic base64(username:password)
- **Body:**
       ```json           
            {
                "username": "your_username",
                "password": "your_password",
                "first_name": "your_first_name",
                "last_name": "your_last_name",
                "email": "your_email",
                "address": "your_address",
                "city": "your_city",
                "state": "your_state",
                "country": "your_country",
                "date_of_birth": "your_date_of_birth",
                "phone_number": "your_phone_number",
            },
        ```

#### User Detail (Admin Only)
- **Endpoint:** `/api/v1/users/<int:pk>/`
- **Description:** Retrieves details of a specific user.
- **Method:** GET, PUT, DELETE
- **Authorization:** Basic base64(username:password)

#### User Creation 
- **Endpoint:** `/api/v1/users/create/`
- **Description:** Creates a new user.
- **Method:** POST
- **Authorization:** None (No authentication required)
- **Body:**

#### User Update
- **Endpoint:** `/api/v1/users/update/`
- **Description:** Updates user information.
- **Method:** PUT
- **Authorization:** Basic base64(username:password)

#### User Info
- **Endpoint:** `/api/v1/users/info/`
- **Description:** Retrieves user information.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### User List 
- **Endpoint:** `/api/v1/users/lists/`
- **Description:** Retrieves a list of users.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

### Accounts

#### Accounts List (Admin Only)
- **Endpoint:** `/api/v1/accounts/`
- **Description:** Retrieves a list of accounts.
- **Method:** GET, POST
- **Authorization:** Basic base64(username:password)
- **Body:**

#### Account Detail (Admin Only)
- **Endpoint:** `/api/v1/accounts/<int:pk>/`
- **Description:** Retrieves details of a specific account.
- **Method:** GET, PUT, DELETE
- **Authorization:** Basic base64(username:password)

#### Accounts List 
- **Endpoint:** `/api/v1/accounts/lists/`
- **Description:** Retrieves accounts associated with current users.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### Account Creation 
- **Endpoint:** `/api/v1/accounts/create/`
- **Description:** Creates a new account.
- **Method:** POST
- **Authorization:** Basic base64(username:password)
- **Body:**

#### Account Details 
- **Endpoint:** `/api/v1/accounts/details/<int:number>/`
- **Description:** Retrieves details of a specific account.
- **Method:** GET, PUT, DELETE
- **Authorization:** Basic base64(username:password)

### Debit Cards

#### Debit Cards List (Admin Only)
- **Endpoint:** `/api/v1/debit_cards/`
- **Description:** Retrieves a list of debit cards.
- **Method:** GET, POST
- **Authorization:** Basic base64(username:password)
- **Body:**

#### Debit Card Detail (Admin Only)
- **Endpoint:** `/api/v1/debit_cards/<int:pk>/`
- **Description:** Retrieves details of a specific debit card.
- **Method:** GET, PUT, DELETE
- **Authorization:** Basic base64(username:password)

#### Debit Cards List 
- **Endpoint:** `/api/v1/debit_cards/lists/`
- **Description:** Retrieves debit cards associated with current users.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### Debit Card Transactions (Admin Only)
- **Endpoint:** `/api/v1/debit_cards_transactions/`
- **Description:** Retrieves transactions related to debit cards.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### Debit Card Transactions Detail (Admin Only)
- **Endpoint:** `/api/v1/debit_cards_transactions/<int:pk>`
- **Description:** Retrieves details of a specific debit card transaction.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### Debit Cards List 
- **Endpoint:** `/api/v1/debit_cards/lists/`
- **Description:** Retrieves debit cards associated with current users.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### Debit Card Details 
- **Endpoint:** `/api/v1/debit_cards/details/<int:number>/`
- **Description:** Retrieves details of a specific debit card.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### Debit Card Transactions List 
- **Endpoint:** `/api/v1/debit_cards_transactions/lists/`
- **Description:** Retrieves transactions related to debit cards.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### Debit Card Transaction Details 
- **Endpoint:** `/api/v1/debit_cards_transactions/details/<uuid:identifier>/`
- **Description:** Retrieves details of a specific debit card transaction.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### Debit Card Receive Payment 
- **Endpoint:** `/api/v1/debit_cards/receive_payment/`
- **Description:** Processes payment receipts for debit cards.
- **Method:** POST
- **Authorization:** Basic base64(username:password)
- **Body:**

### Deposits

#### Deposits List (Admin Only)
- **Endpoint:** `/api/v1/deposits/`
- **Description:** Retrieves a list of deposits.
- **Method:** GET, POST
- **Authorization:** Basic base64(username:password)
- **Body:**

#### Deposit Detail (Admin Only)
- **Endpoint:** `/api/v1/deposits/<int:pk>/`
- **Description:** Retrieves details of a specific deposit.
- **Method:** GET, PUT, DELETE
- **Authorization:** Basic base64(username:password)

#### Deposit Creation 
- **Endpoint:** `/api/v1/deposits/create/`
- **Description:** Creates a new deposit.
- **Method:** POST
- **Authorization:** Basic base64(username:password)
- **Body:**

#### User Deposits List 
- **Endpoint:** `/api/v1/deposits/lists/`
- **Description:** Retrieves deposits associated with current users.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### User Deposit Details 
- **Endpoint:** `/api/v1/deposits/details/<uuid:identifier>/`
- **Description:** Retrieves details of a specific user deposit.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

### Merchants

#### Merchants List (Admin Only)
- **Endpoint:** `/api/v1/merchants/`
- **Description:** Retrieves a list of merchants.
- **Method:** GET, POST
- **Authorization:** Basic base64(username:password)
- **Body:**

#### Merchant Detail (Admin Only)
- **Endpoint:** `/api/v1/merchants/<int:pk>/`
- **Description:** Retrieves details of a specific merchant.
- **Method:** GET, PUT, DELETE
- **Authorization:** Basic base64(username:password)

#### Merchant Creation 
- **Endpoint:** `/api/v1/merchants/create/`
- **Description:** Creates a new merchant.
- **Method:** POST
- **Authorization:** Basic base64(username:password)
- **Body:**

#### Merchant Details 
- **Endpoint:** `/api/v1/merchants/details/`
- **Description:** Retrieves details of a merchant.
- **Method:** GET, PUT, DELETE
- **Authorization:** Basic base64(username:password)

### Notifications

#### Notifications List (Admin Only)
- **Endpoint:** `/api/v1/notifications/`
- **Description:** Retrieves a list of notifications.
- **Method:** GET, POST
- **Authorization:** Basic base64(username:password)
- **Body:**

#### Notification Detail (Admin Only)
- **Endpoint:** `/api/v1/notifications/<int:pk>/`
- **Description:** Retrieves details of a specific notification.
- **Method:** GET, PUT, DELETE
- **Authorization:** Basic base64(username:password)

#### User Notifications List 
- **Endpoint:** `/api/v1/notifications/lists/`
- **Description:** Retrieves notifications associated with current users.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### User Notification Detail 
- **Endpoint:** `/api/v1/notifications/details/<int:notification_number>/`
- **Description:** Retrieves details of a specific user notification.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

### Transactions

#### Transactions List (Admin Only)
- **Endpoint:** `/api/v1/transactions/`
- **Description:** Retrieves a list of transactions.
- **Method:** GET, POST
- **Authorization:** Basic base64(username:password)
- **Body:**

#### Transaction Detail (Admin Only)
- **Endpoint:** `/api/v1/transactions/<int:pk>/`
- **Description:** Retrieves details of a specific transaction.
- **Method:** GET, PUT, DELETE
- **Authorization:** Basic base64(username:password)

#### Transaction History 
- **Endpoint:** `/api/v1/transactions/history/`
- **Description:** Retrieves transaction history.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### User Transaction Detail 
- **Endpoint:** `/api/v1/transactions/history/<uuid:identifier>/`
- **Description:** Retrieves details of a specific user transaction.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

### Transfers

#### Transfers List (Admin Only)
- **Endpoint:** `/api/v1/transfers/`
- **Description:** Retrieves a list of transfers.
- **Method:** GET, POST
- **Authorization:** Basic base64(username:password)
- **Body:**

#### Transfer Detail (Admin Only)
- **Endpoint:** `/api/v1/transfers/<int:pk>/`
- **Description:** Retrieves details of a specific transfer.
- **Method:** GET, PUT, DELETE
- **Authorization:** Basic base64(username:password)

#### Transfer Creation 
- **Endpoint:** `/api/v1/transfers/create/`
- **Description:** Creates a new transfer.
- **Method:** POST
- **Authorization:** Basic base64(username:password)
- **Body:**

#### User Transfer List 
- **Endpoint:** `/api/v1/transfers/lists/`
- **Description:** Retrieves transfers associated with current users.
- **Method:** GET
- **Authorization:** Basic base64(username:password)

#### User Transfer Details 
- **Endpoint:** `/api/v1/transfers/details/<uuid:identifier>/`
- **Description:** Retrieves details of a specific user transfer.
- **Method:** GET
- **Authorization:** Basic base64(username:password)


## Contributing
Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: ``` git checkout -b feature/new-feature  ```
3. Make your changes and commit them: ``` git commit -m 'Add new feature' ```.
4. Push to the branch: ``` git push origin feature/new-feature ```.
5. Submit a pull request.

## Related Projects

Explore other related projects that offer real-world payment solutions:

- [Stripe API](https://stripe.com/docs/development/): The official Stripe API. A widely-used payment gateway for handling real transactions securely.
- [PayPal Developer](https://developer.paypal.com/): PayPal's official checkout SDK for integrating PayPal payments into your applications.

These projects provide robust and secure payment solutions that go beyond dummy data, suitable for real-world applications and e-commerce platforms.


## How the project come to live
> This section is under construction. Stay tuned for insights into the project's inception, development challenges, and interesting anecdotes!

## Note
**Please Note**: This README is a work in progress. It may undergo changes or become more comprehensive over time as the project evolves.

## Licensing
The Virtual Bank project is licensed under the MIT License, ensuring open-source availability and contributions from the community.
