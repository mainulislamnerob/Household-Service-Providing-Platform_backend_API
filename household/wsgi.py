import os
from django.core.wsgi import get_wsgi_application

# Vercel imports this module; set settings here
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'household.settings')

# Expose BOTH names:
# - `application` for Django/gunicorn (local/prod servers)
# - `app` for Vercel's python function loader (matches your friend's pattern)
application = get_wsgi_application()
app = application
