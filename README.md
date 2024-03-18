# ___ZNAKAPP___
##  Overview
**Znakapp** is a project designed to remove watermarks from real estate listings. It is built using the Python web framework **Django 4.2**, integrates **Tailwind CSS** for styling.
**Supported Websites:**
Znakapp works seamlessly with real estate listings from the following websites:
- [kn.kz](https://kn.kz)
- [krisha.kz](https://krisha.kz)
- [kz.m2bomber.com](https://kz.m2bomber.com)
- [nedvizhimostpro.kz](https://nedvizhimostpro.kz)
- [olx.kz](https://olx.kz)
## Features
- **Django Web Framework:** The project is developed with Django, providing a robust and scalable foundation for web applications.

- **Tailwind CSS Styling:** Tailwind CSS is utilized for a modern and responsive user interface design.
## Requirements
Ensure you have the following dependencies installed before running the project:
+ ***Python 3.8 (Important, as some dependencies may not install correctly)***
+ (Other dependencies from requirements.txt)
```bash
pip install -r requirements.txt
```
## Installation
Follow these steps to install and run Znakapp:
1. **Clone the Znakapp repository:**
```bash 
git clone https://github.com/Delete101/znakapp.git
cd znakapp
```
2. **Create a virtual environment:**<br>
+ For Linux and MacOS:
```bash
python3 -m venv venv
```
+ For Windows:
```bash
python -m venv venv
```
3. **Activate a virtual environment:**
+ For Linux and MacOS:
```bash
source venv/bin/activate
```
+ For Windows:
```bash
venv\Scripts\activate
```
4. **Install Torch separately:**
```bash
pip install torch==2.0.1
```
5. **Install dependencies (excluding detectron2):**
```bash
pip install -r requirements.txt
```
6. **Install detectron2**
```bash
pip install -e git+https://github.com/facebookresearch/detectron2.git@94113be6e12db36b8c7601e13747587f19ec92fe#egg=detectron2
```
7. **Perform migrations:**
```bash
python manage.py migrate
```
7. **Create a superuser (admin) for the Django admin interface:**<br>
+ For Linux or MacOS:
```bash
python3 manage.py createsuperuser
```
+ For Windows:
```bash
python manage.py createsuperuser
```
  - When you enter the command, you will be prompted to enter the username, email address, and password for the superuser.
  - The username may contain letters, numbers, and the characters @/./+/-/_. It should not contain spaces.
  - After that, you will be prompted to enter the password. Please note that the characters you type for the password will not be displayed in the console.
8.   **Run the Django development server:**

```bash
python manage.py runserver
``` 
## For Linux And MacOS
```bash
git clone https://github.com/Delete101/znakapp.git
cd znakapp
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install torch==2.0.1
pip install -r requirements.txt
pip install -e git+https://github.com/facebookresearch/detectron2.git@94113be6e12db36b8c7601e13747587f19ec92fe#egg=detectron2
python manage.py migrate
# Please note that the characters you type for the password will not be displayed in the console.
python3 manage.py createsuperuser
python manage.py runserver
```
## For Windows
```bash
git clone https://github.com/Delete101/znakapp.git
cd znakapp
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install torch==2.0.1
pip install -r requirements.txt
pip install -e git+https://github.com/facebookresearch/detectron2.git@94113be6e12db36b8c7601e13747587f19ec92fe#egg=detectron2
python manage.py migrate
# Please note that the characters you type for the password will not be displayed in the console.
python manage.py createsuperuser
python manage.py runserver
```
  **Visit http://127.0.0.1:8000 in your web browser to access the application.**
## **Usage**
1. **Login to Your Account:**
Before using Znakapp, log in to your account using the credentials created during the superuser (admin) creation process. Click the "Login" button at the top right and enter the username and password you specified when creating the superuser.
1. **Upload announcement of the sale of real estate link:**
Inside your profile, find the option to upload the link to the real estate listings containing watermarks.
1. **Click the "Download" Button:**
After uploading the link, press the "Download" button to initiate the watermark removal process.
1. **View and Download the Watermark-Free Image:**
Once the process is complete, view and download the watermark-free image generated by Znakapp.

By following these steps, you can effectively utilize Znakapp to remove watermarks.