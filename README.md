
# Artificial Heirlooms

A Django-based e-commerce platform for selling traditional handicrafts


## Features

- Dynamic Product Management: Add and manage products.
- Login with Google account
- Elegant look


## Deployment

1. Create a virtual environment and activate it
```bash
 python -m venv <your_venv_name>
 cd <your_venv_name>
 .\Scripts\activate
```
2. Clone the repository:
```bash
 git clone https://github.com/Pyisoe-Thame/artificial_hierlooms
```
3. Install the required packages
```bash
 pip install -r requirements.txt
```
4. Run the server
```bash
 cd artificial_heirlooms
 python -m manage.py runserver
```
5. Enjoy the show!
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

