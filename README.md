# nospammail
AU Hack 2017 project

## Install
```
mkvirtualenv --python=$(which python3) nospammail
pip install -r requirements.txt
createdb nospammail
sudo -u postgres createuser -W nospammail
python manage.py migrate
python manage.py runserver
```



