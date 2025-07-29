--Installation Instructions--

1. Clone the repository:

(in gitbash)

git clone https://github.com/nilesclancy/script-aid-api-nc.git (or use the ssh url)
cd script-aid-api-nc

2. (Optional) Create and activate a virtual environment:

(in gitbash)

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install required packages:

(in gitbash)

pip install -r requirements.txt

4. Apply migrations:

(in gitbash)

python manage.py migrate

5. (Optional) Create a superuser (admin account):

(in gitbash)

python manage.py createsuperuser

6. Start the development server:

(in gitbash)

python manage.py runserver

The backend API should now be available at:

http://127.0.0.1:8000/api/

--API Features--

/api/register — Register new users

/api/login — Obtain authentication token

/api/upload — Upload transcript with title + content

/api/transcripts — View all user transcripts

/api/parsed — Parse a transcript for keywords and context

/api/files — View/export saved parsed files

All endpoints (except register/login) require Authorization: Token <your-token>

--Frontend Check--

To use this API with the ScriptAid React frontend, clone and run script-aid-client-nc.

Make sure this API runs on:

http://127.0.0.1:8000
