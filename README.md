#  NGL Django Project Setup Guide

This is a Django-based project. Follow the steps below to set up your environment, install dependencies, and access the different apps.

## 1. Set Up the Python Environment

Ensure that your Python environment is already set up for this project. If you're using a virtual environment, activate it first:

- **On Windows**:

```bash
venv\Scripts\activate
```

- **On macOS/Linux**:

```bash
source venv/bin/activate
```

If you don't have a virtual environment, create one using:

```bash
python -m venv venv
```

Then, activate it as shown above.

## 2. Install Dependencies

Once your virtual environment is activated, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all the necessary libraries specified in the `requirements.txt` file.

## 3. Migrate the Database

After installing the dependencies, you need to apply database migrations to set up the database schema based on the models defined in the Django project.

```bash
python manage.py migrate
```

## 4. Run the Development Server

To start the development server, use the following command:

```bash
python manage.py runserver
```

The development server will start, and you can access the app in your web browser.

- Default URL which is app1: [http://localhost:8000] and for app2:(http://localhost:8000/app2/login)

## 5. Access the Apps

- **App 1**: You can access the main app (app1) at:

  ```plaintext
  http://localhost:8000
  ```

- **App 2 (Admin)**: To access the Django admin interface (app2), go to:

  ```plaintext
  http://localhost:8000/app2/login
  ```

  Log in using the credentials you have sign up with a different emal.

## 6. Additional Information

- If you make changes to models or settings, remember to run the migration commands:

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

- To stop the development server, press `CTRL+C` in the terminal.
