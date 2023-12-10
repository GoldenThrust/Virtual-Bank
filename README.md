# Virtual Bank Web Application and API

## Introduction

Welcome to the Virtual Bank project! This web application and API were created to provide developers with a platform for simulating banking transactions. Whether you're testing e-commerce websites or exploring payment integrations, our project allows you to experiment without using real bank APIs. Built on Django, it offers a range of functionalities tailored for transaction simulation.

- [**Live Demo**](http://www.virtualbank.tech/)
- [**Final Project Blog Article**](#)
- **Author:** Adeniji Olajide ([LinkedIn](https://www.linkedin.com/in/olajide-adeniji-0286a32a2/)) ([Twitter](https://twitter.com/Goldenthrust3))

![Virtual Bank](screenshot/virtualbank-homepage.gif)

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
