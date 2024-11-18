# **File and Folder Management System**

This backend system allows users to create and manage folders and files, ensuring each user has a root folder to organize their content. The system supports hierarchical folder structures and offers full CRUD functionality for both files and folders and listing capabilities.

### Prerequisites

1. Python (version 3.8 or higher)
2. MySQL database server
3. Django (version 3.x or higher)

## Installation

1. **Create Project folder**
   Clone the repo
   git clone https://github.com/Babutmcdb/django-file-management.git

2. **Create a virtual environment and install dependencies**:

   ```bash
   virtualenv "your env name"
   "your env name"\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure MySQL Database**:

   - Create a new MySQL database.
   - Update the `DATABASES` setting in `settings.py` with your MySQL configuration:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'your_db_name',
             'USER': 'your_db_user',
             'PASSWORD': 'your_db_password',
             'HOST': 'localhost',
             'PORT': '3306',
         }
     }
     ```

4. **Apply Migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Server**:

   ```bash
   python manage.py runserver
   ```

7. **Access the Application**:
   - Open `http://127.0.0.1:8000` in your browser.
   - Login as an admin at `http://127.0.0.1:8000/admin`.

## Usage

- **File Management**:
  - Admins can create and manage users with specific access permissions.

## Project Structure

- **models.py**: Contains the `Entry` model for folder and file access..
- **views.py**: Contains views for folder and file creation, listing, updating, and deleting.
- **urls.py**: Configures the routes for file management.

## API Endpoints

Method - Endpoint- Description
Get - /api/list/ - List all folder and files
Post - /api/create/ - Creates a file or folder
Post - /api/move/ - Edit a file or folder
Post - /api/rename/ - Rename a file or folder
Post - /api/delete/ - Delete a file or folder

This is a basic file management system. Feel free to customize and extend it for your own needs.
