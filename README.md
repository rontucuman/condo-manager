# condo-manager

python -m venv venv  
.\venv\Scripts\activate  
python -m pip install -r .\requirements.txt  
python manage.py makemigrations  
python manage.py migrate  
python manage.py createsuperuser  
python manage.py runserver  