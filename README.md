
# Artificial Heirlooms

A Django-based e-commerce platform for selling traditional handicrafts


## Features

- Dynamic Product Management: Add and manage products.
- Login with Google account
- Elegant look


## Awaken the Application Locally

1. Create a virtual environment and activate it
```bash
 python -m venv <your_venv_name>
 cd <your_venv_name>
 .\Scripts\activate
```
2. Clone the repository:
```bash
 git clone https://github.com/Pyisoe-Thame/artificial_heirlooms.git
```
3. Install the required packages
```bash
 pip install -r requirements.txt
```
4. Update Project Settings
Open the settings.py file in the project directory and make the following changes for production:
- Set DEBUG = False.
- Add your domain or IP address to ALLOWED_HOSTS:
```bash
ALLOWED_HOSTS = ['127.0.0.1', '<your_ip_address>', '<your_domain>']
```
5. Collect Static Files
```bash
python manage.py collectstatic
```
6. Run the server
```bash
 cd artificial_heirlooms
 python -m manage.py runserver
```
7. Enjoy the show!
## Google Login
To achieve login with google replace
```
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'
```
at lines __165__ and __166__ of __\project\settings.py__
with your actual Google OAuth2 key and Google OAuth2 Secret.

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/)


## Support

For support, email pyisoethame@gmail.com or just leave the comment under this project.

