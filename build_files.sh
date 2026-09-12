# #!/bin/bash
# pip install -r requirements.txt
# python manage.py collectstatic --noinput --clear


python3.9 -m pip install -r requirements.txt --break-system-packages
python3.9 manage.py collectstatic --noinput