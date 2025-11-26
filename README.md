# FastAPI MongoDB Authentication Project

A FastAPI application with MongoDB database and FastAPI-Users for authentication.

## Features

- User registration and authentication
- JWT token-based authentication
- MongoDB database with Beanie ODM
- Protected routes
- User profile management
- Automatic API documentation

## Setup

### Prerequisites

- Python 3.8+
- MongoDB (local installation or MongoDB Atlas)

### Installation

1. Clone or create the project directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   copy .env.example .env
   ```
   Edit the `.env` file with your configuration.

4. Make sure MongoDB is running on your system or update the connection string for MongoDB Atlas.

### Running the Application

```bash
uvicorn main:app --reload
```

The application will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative API docs: `http://localhost:8000/redoc`

## Authentication Endpoints

### Register a new user
- **POST** `/auth/register`
- Body:
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```

### Login
- **POST** `/auth/jwt/login`
- Body (form data):
  ```
  username: user@example.com
  password: password123
  ```
- Returns a JWT token

### Logout
- **POST** `/auth/jwt/logout`
- Requires authentication

## Protected Routes

### Get user profile
- **GET** `/api/user-profile`
- Requires authentication

### Protected route example
- **GET** `/api/protected-route`
- Requires authentication

### User management
- **GET** `/users/me` - Get current user info
- **PATCH** `/users/me` - Update current user
- **DELETE** `/users/me` - Delete current user

## Project Structure

```
├── main.py          # FastAPI application and route setup
├── models.py        # User model and database models
├── schemas.py       # Pydantic schemas for API
├── auth.py          # Authentication configuration
├── database.py      # Database connection and initialization
├── config.py        # Application configuration
├── routes.py        # Custom API routes
├── requirements.txt # Python dependencies
└── .env.example     # Environment variables template
```

## Environment Variables

- `MONGODB_URL`: MongoDB connection string
- `DATABASE_NAME`: Database name
- `SECRET_KEY`: Secret key for JWT tokens (change in production!)

## Usage Example

1. Start the application
2. Register a new user via `/auth/register`
3. Login via `/auth/jwt/login` to get a JWT token
4. Use the token in the Authorization header: `Bearer <your-token>`
5. Access protected routes like `/api/protected-route`

## MongoDB Collections

The application will automatically create the following collections:
- `users`: Stores user information and authentication data
