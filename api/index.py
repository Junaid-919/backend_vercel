import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pms.settings")

<<<<<<< HEAD
app = get_wsgi_application()   # 👈 MUST be named `app`
=======
app = get_wsgi_application()   # 👈 MUST be named `app`
>>>>>>> 47c1e98 (Initial commit jan23)
