import sys, os
h="/home/deals490"

INTERP = h+"/venv/bin/python3"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(os.getcwd())
sys.path.append(h+"/repo")
sys.path.insert(0,h+"/venv/bin")
sys.path.insert(0,h+"/venv/lib/python3.6/site-packages")

os.environ['DJANGO_SETTINGS_MODULE'] = "commerce.settings_dreamhost"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

