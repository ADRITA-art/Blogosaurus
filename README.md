# Blogosaurus

Welcome to **Blogosaurus**, a Flask-based blogging platform! 🚀

Blogosaurus allows users to create, edit, view, and delete blog posts with ease. It also includes robust user authentication and authorization features using JWT (JSON Web Tokens).

---

## 🌟 Features

- **🔒 User Authentication**: Sign up, log in, and log out functionality with secure password hashing.
- **🛡️ JWT Authorization**: Protect routes and ensure secure access to user-specific data.
- **📝 Blog Management**: Create, edit, view, and delete blog posts.
- **📊 Dashboard**: View all blogs created by the logged-in user.
- **🔗 RESTful API**: JSON-based API endpoints for seamless integration.
- **🌐 CORS Support**: Cross-Origin Resource Sharing enabled for API access.

---

## 📂 Project Structure

```
blogosaurus/
├── app/
│   ├── __init__.py          # App factory and initialization
│   ├── models.py            # Database models for User and Blog
│   ├── routes/
│   │   ├── __init__.py      # Route initialization
│   │   ├── auth_routes.py   # Authentication routes
│   │   ├── blog_routes.py   # Blog management routes
│   ├── templates/           # HTML templates for the frontend
│   ├── static/              # Static files (CSS, JS, images)
├── instance/
│   ├── config.py            # Instance-specific configuration
│   ├── site.db              # SQLite database
├── config.py                # Default configuration
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── .gitignore               # Git ignore rules
```

---

## 🚀 Quick Start

### 1️⃣ Prerequisites

- Python 3.10 or higher
- A virtual environment (recommended)
- SQLite (default database)

### 2️⃣ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/blogosaurus.git
   cd blogosaurus
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory and add the following:
   ```
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///instance/site.db
   ```

5. **Initialize the database**:
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

6. **Run the application**:
   ```bash
   python run.py
   ```

7. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 📡 API Endpoints

### 🔑 Authentication

- **POST** `/signup`: Register a new user.
- **POST** `/login`: Log in and receive a JWT token.
- **GET** `/logout`: Log out the user.

### 📝 Blog Management

- **GET** `/`: View all blogs.
- **GET** `/dashboard`: View blogs created by the logged-in user.
- **POST** `/create`: Create a new blog post.
- **GET/PUT** `/edit/<int:id>`: View or update a specific blog post.
- **DELETE** `/delete/<int:id>`: Delete a specific blog post.
- **GET** `/blog/<int:id>`: View a specific blog post.

---

## 🛠️ Technologies Used

- **Flask**: Web framework
- **Flask-SQLAlchemy**: ORM for database management
- **Flask-Login**: User session management
- **Flask-JWT-Extended**: JWT-based authentication
- **Flask-CORS**: Cross-Origin Resource Sharing
- **SQLite**: Lightweight database

---

## 🤝 Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your branch.
4. Submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.

---

## 📧 Contact

For any questions or feedback, feel free to reach out at [your-email@example.com](mailto:your-email@example.com).