
# Flask Blog Application with CRUD Functionality

This Flask web application provides CRUD (Create, Read, Update, Delete) endpoints for managing articles in a small blog site. 
The application supports both HTML and JSON responses based on the Headers. Content is formatted in HTML, and the solution includes the ability to upload images alongside articles.

Additionally, users can perform the following actions:
- Register an account
- Login and Logout
- Update their profile information
- Search for posts
- Manage your own posts


## Getting Started

1. **Clone the Repository**

    ```bash
    git clone https://github.com/erickkpina/vroom-assessment.git
    cd vroom-assessment
    ```

2. **Setup Virtual Environment (Optional but recommended)**

    Create and activate a virtual environment to isolate the project dependencies.

    
    ### Using venv
    ```bash
    python -m venv venv
    ```
    ### Activate the virtual environment (Windows)
    ```bash
    venv\Scripts\activate
    ```
    ### Activate the virtual environment (Mac/Linux)
    ```bash
    source venv/bin/activate
    ```

3. **Install Dependencies**

    Install the required Python packages listed in `requirements.txt`.

    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize Database with SQLAlchemy**

    Initialize database tables using Flask-Migrate with SQLAlchemy.

    ```bash
    flask db init  # Initialize migrations (if not done)
    flask db migrate -m "Initial migration"  # Create migration files
    flask db upgrade  # Apply migrations to the database
    ```

6. **Running the Application**

    Start the Flask development server.

    ```bash
    flask run
    ```

    The application will be accessible at `http://127.0.0.1:5000` by default.

7. **Access the Application**

    Open a web browser and navigate to `http://127.0.0.1:5000` to access the Flask application.
