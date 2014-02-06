import os, sys
from distutils.sysconfig import get_python_lib

plib = get_python_lib()

#Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)

#Add the path to 3rd party django application and to django itself.
sys.path.append(plib + '/django')
sys.path.append(plib + '/pubsub')

os.environ['DJANGO_SETTINGS_MODULE'] = 'pubsub.settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

