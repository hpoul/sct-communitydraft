# Django settings for community project.

# You should not modify anything in this file,
# but in settings_local.py

import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
# SCT library path.
LIB_PATH = os.path.join(ROOT_PATH,'..','..','communitytools', 'sphenecoll')

from django.conf.urls.defaults import *

DEBUG = True
TEMPLATE_DEBUG = True

# The following settings should be customized in settings_local.py !!!

ADMINS = (
    ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS


DATABASE_ENGINE = 'postgresql'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'djangotest'             # Or path to database file if using sqlite3.
DATABASE_USER = 'django'             # Not used with sqlite3.
DATABASE_PASSWORD = 'test'         # Not used with sqlite3.
DATABASE_HOST = '127.0.0.1'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

SPH_SETTINGS = { 'wiki_rss_url' : '/feeds/wiki/',
                 }

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Vienna'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT_PATH,'..','static')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=6&cv@*svpas38mz%h-5j7*&61zhkiuej%17@$hrf#$!37qylx'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
#    'sphene.sphboard.middleware.PerformanceMiddleware',
#    'sphene.community.middleware.PsycoMiddleware',
    'sphene.community.middleware.ThreadLocals',
    'sphene.community.middleware.GroupMiddleware',
    'sphene.community.middleware.MultiHostMiddleware',
#    'sphene.community.middleware.StatsMiddleware',
    'sphene.community.middleware.LastModified',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'sphene.community.middleware.PermissionDeniedMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'sphene.community.context_processors.navigation',
)


ROOT_URLCONF = 'community.urls'

SPH_HOST_MIDDLEWARE_URLCONF_MAPPING = {
    'community.spacecombat2.net': { 'groupName': 'SpaceCombat2' },
    'community.spacecombat2.com': { 'groupName': 'SpaceCombat2' },
    '127.0.0.1:8000': { 'groupName': 'SpaceCombat2' },
}

SPH_HOST_MIDDLEWARE_URLCONF_MAP = {
    '127.0.0.1:8000': { 'urlconf': 'urlconfs.community_urls',
                        'params': { 'groupName': 'example' }
                        },
    r'^(?P<groupName>\w+).localhost.*$': { 'urlconf': 'urlconfs.community_urls', },
}

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, 'templates'),
    os.path.join(ROOT_PATH, '..', 'sitetemplates'),

    os.path.join(LIB_PATH, 'templates'),

)

import sys
sys.path.append(ROOT_PATH)
sys.path.append(LIB_PATH)



INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.flatpages',

    'django.contrib.admin',
    'django.contrib.sitemaps',
    
    'sphene.community',
    'sphene.sphboard',
    'sphene.sphwiki',

)

try:
    # settings_local overwrites a few settings from here, and has to define SECRET_KEY
    from settings_local import *
except:
    print "Warning - Unable to import settings_local"
