# Django Application Integration with exsited-python SDK
## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Steps to Integrate the SDK](#steps-to-integrate-the-sdk)
  - [1. Activate your virtual environment](#1-activate-your-virtual-environment)
  - [2. Install required packages](#2-install-required-packages)
  - [3. Move to the djangoSDK directory](#3-move-to-the-djangoSDK-directory)
  - [4. Make a package for commonData](#4-make-a-package-for-commonData)
  - [5. Update Database Credentials](#5-update-database-credentials)
  - [6. Run the Django Application](#6-run-the-Django-Application)
- [Conclusion](#conclusion)


## Overview

This guide outlines the steps required to integrate the "exsited-python SDK" into your Django project. By following this guide, you'll install necessary "dependencies," set up a "virtual environment," configure "database credentials," and run the "project."

## Prerequisites

Ensure the following are installed on your system:
- Python 3.12
- MySQl
- Django 5.0.6
- django-mysqlclient


##  Clone the Repository

First, clone the Django SDK project repository from GitHub & navigate into the directory:

```bash
git clone https://github.com/exsited/django_sdk_project.git

# navigate into the directory
cd exsited_django_example

```

## Steps to Integrate the SDK

### 1. Activate your virtual environment

Activate virtual environment by - 

```bash
# Install "virtualenv" if not already installed
pip install virtualenv

# Create a "virtual environment"
python -m venv venv

# Activate the "virtual environment" (Windows)
venv\Scripts\activate
```

```bash
#if you face any error, try with this- 
.\venv\Scripts\activate
```

```bash
# For Linux/Mac, use: 
source venv/bin/activate
```

### 2. Install required packages

Install these packages -

```bash
pip install django djangorestframework mysqlclient exsited
```

### 3. Move to the djangoSDK directory

Navigate to the djangoSDK directory:

```bash
cd djangoSDK
```
### 4. Make a package for commonData

Make a package under your root project named "common" and inside that create a python file named "common_data" manually or by using following command:

```bash
mkdir common
touch common/__init__.py
touch common/common_data.py


```
navigate to `djangoSDK/common/common_data.py` update the following credentials with your details:

```python
from exsited.exsited.auth.dto.token_dto import RequestTokenDTO

class CommonData:

    @staticmethod
    def get_request_token_dto():
        return RequestTokenDTO(
            clientId = 	"[YOUR_CLIENT_ID]",
            clientSecret = "[YOUR_CLIENT_SECRET]",
            redirectUri = "[YOUR_REDIRECT_URI]",
            ExsitedUrl = "[YOUR_EXSITED_SERVER_URL]"
        )
```


### 5. Update Database Credentials

Next, go to `djangoSDK/service/utils.py` and update the database credentials:

```python
def connect_to_db():
    return MySQLdb.connect(
        host="[YOUR_HOST]",          # Your Database host
        user="[YOUR_USERNAME]",      # Your Database username
        passwd="[YOUR_PASSWORD]",    # Your Database password
        db="[YOUR_DATABASE_NAME]"    # Your Database name
    )
```

### 6. Run the Django Application

Finally, navigate to the "djangoSDK" directory and run the Django development server:

```bash
python manage.py runserver
```

## Conclusion

By following these steps, you should be able to successfully integrate the exsited-python SDK into your Django project. If you encounter any issues, ensure your environment is set up correctly, and all dependencies are properly installed.
