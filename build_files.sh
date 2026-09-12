# #!/bin/bash
# pip install -r requirements.txt
# python manage.py collectstatic --noinput --clear


# Example build_files.sh
python3.9 -m pip install -r requirements.txt --break-system-packages
python3.9 manage.py collectstatic --noinput