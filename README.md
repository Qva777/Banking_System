# Bank Simple API

<!-- ABOUT -->
> The API will allow users to create accounts, deposit money, 
> withdraw money, and send money between accounts

<!-- END ABOUT -->

<hr>

<h2>📍How to up: </h2>

- Clone
- Set your value in `.env` file in (backend) folder, look `.env.example`
- Command to build and up:  `docker compose up --build`


# Endpoints
## User:
- **POST** `/api/login_jwt`: Login JWT
- **POST** `/api/refresh`: Refresh Token


- **POST** `/api/users`: User creation
- **GET, PUT, DELETE** `/api/users/<id>`: User detail info
- **GET** `/api/users`: List of users


- **GET** `/api/deleted_users`: List of the deleted users
- **POST** `/api/users/<id>/recover`: Recover deleted users
- **DELETE** `/api/users/<id>/hard_delete`: Hard deletion

## Account:
- **POST** `/api/create_account`: Create Account
- **POST** `/api/deposit`: Make deposit
- **POST** `/api/withdraw`: Withdrawal
- **POST** `/api/transfer`: Transfer 
