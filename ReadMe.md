Chapters - Portfolio Backend

This project is a FastAPI-based backend for an Chapters - AI Portal Portfolio backend. It provides APIs for managing administrators, users, projects, project feedback and etc.

## Features

- User authentication and authorization (JWT-based)
- Role-based access control (Admin and User roles)
- MongoDB integration using Beanie ODM

## Technology Stack

- Python 3.7+
- FastAPI
- MongoDB
- Beanie ODM
- PyJWT

## Project Structure

```
.
├── app.py
├── main.py
├── .env
├── auth/
│   ├── jwt_bearer.py
│   └── jwt_handler.py
├── config/
│   └── config.py
├── database/
│   └── ..
├── models/
│   ├── ..
├── routes/
│   ├── ..
├── schemas/
│   ├── ..
└── requirements.txt
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone Tharuka-Wijethunga/Chapters-Portfolio-Back-end
   cd Chapters-Portfolio-Back-end
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your MongoDB URI:
   ```
   MONGODB_URI=your_mongodb_uri_here
   MONGODB_DB=your_database_name
   ```

5. Initialize the admin users by running:
   ```
   python initialize_admin.py
   ```

## Running the Application

To run the application, use the following command:

```
python main.py
```

The API will be available at `http://localhost:8080`.

API Documentation : `http://localhost:8080/docs`.