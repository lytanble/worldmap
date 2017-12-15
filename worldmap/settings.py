# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

####################### DATAVERSE_INFO_REPOSITORY_PATH
#
# For Dataverse/Worldmap communication, the following repository is required:
#
#   https://github.com/IQSS/shared-dataverse-information
#
# It may be accessed in 1 of 2 ways
# -----------------------------------------------
#
#   (1) Add to the sys.path.  In the local_settings.py:
#       (a) Add/Uncomment the code below (lines 28-31),
#           ending with the "sys.path.append" line
#       (b) Set the appropriate path for "DATAVERSE_INFO_REPOSITORY_PATH"
#   (2) or run "pip install shared_dataverse_information"
# -----------------------------------------------
"""
DATAVERSE_INFO_REPOSITORY_PATH = '/home/ubuntu/code/shared-dataverse-information'
if not os.path.isdir(DATAVERSE_INFO_REPOSITORY_PATH):
    raise Exception('Directory not found for repository "shared-dataverse-information" (https://github.com/IQSS/shared-dataverse-information)\ndirectory in settings: %s' % DATAVERSE_INFO_REPOSITORY_PATH)
sys.path.append(DATAVERSE_INFO_REPOSITORY_PATH)
"""
####################### END: DATAVERSE_INFO_REPOSITORY_PATH


# Django settings for the GeoNode project.
import os
from kombu import Queue
from geonode import __file__ as geonode_path
from worldmap import get_version
from worldmap.celeryapp import app  # flake8: noqa
#import djcelery
import dj_database_url
from distutils.util import strtobool

def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")


#
# General Django development settings
#
# GeoNode Version

VERSION = get_version()

# Defines the directory that contains the settings file as the PROJECT_ROOT
# It is used for relative settings elsewhere.
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
GEONODE_ROOT = os.path.abspath(os.path.dirname(geonode_path))

# Setting debug to true makes Django serve static media and
# present pretty error pages.
DEBUG = str2bool(os.getenv('DEBUG', 'True'))

# Set to True to load non-minified versions of (static) client dependencies
# Requires to set-up Node and tools that are required for static development
# otherwise it will raise errors for the missing non-minified dependencies
DEBUG_STATIC = str2bool(os.getenv('DEBUG_STATIC', 'False'))

# This is needed for integration tests, they require
# geonode to be listening for GeoServer auth requests.
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = 'localhost:8000'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# AUTH_IP_WHITELIST property limits access to users/groups REST endpoints
# to only whitelisted IP addresses.
#
# Empty list means 'allow all'
#
# If you need to limit 'api' REST calls to only some specific IPs
# fill the list like below:
#
# AUTH_IP_WHITELIST = ['192.168.1.158', '192.168.1.159']
AUTH_IP_WHITELIST = []

SECRET_KEY = os.getenv('SECRET_KEY', "%umia(f2e-t^*n(bphyf4g6=ng$_+&ijdu$b&f$+6a^iz9ptca")

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'sqlite:///{path}'.format(
        path=os.path.join(PROJECT_ROOT, 'development.db')
    )
)
# The FULLY QUALIFIED url to the GeoServer instance for this GeoNode.
GEOSERVER_BASE_URL = os.getenv('GEOSERVER_BASE_URL',
                               "http://localhost:8080/geoserver/")


DATASTORE_URL = os.getenv('DATASTORE_URL',
                          'postgis://worldmap:worldmap@localhost:5432/data')

DB_DATASTORE = str2bool(os.getenv('DB_DATASTORE','True'))

# SHARD DATABASES SETTINGS
SHARD_STRATEGY = 'monthly'
SHARD_PREFIX = 'wm_'
SHARD_SUFFIX = ''

# set to true to have multiple recipients in /message/create/
USER_MESSAGES_ALLOW_MULTIPLE_RECIPIENTS = False

# Defines settings for development
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600),
    'datastore': dj_database_url.parse(DATASTORE_URL, conn_max_age=600),
}

MANAGERS = ADMINS = os.getenv('ADMINS', [])

USE_CUSTOM_ORG_AUTHORIZATION = True
CUSTOM_ORG_AUTH_TEXT = 'Are you affiliated with Harvard University?'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = os.getenv('TIME_ZONE', "America/Chicago")

SITE_ID = int(os.getenv('SITE_ID', '1'))

USE_I18N = str2bool(os.getenv('USE_I18N', 'True'))
USE_L10N = str2bool(os.getenv('USE_I18N', 'True'))

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', "en-us")
# Underscore at the beginning added to represent a private variable.
# should not be used in the application.
_DEFAULT_LANGUAGES = (
    ('en', 'English'),
    ('es', 'Español'),
    ('it', 'Italiano'),
    ('fr', 'Français'),
    ('de', 'Deutsch'),
    ('el', 'Ελληνικά'),
    ('id', 'Bahasa Indonesia'),
    ('zh-cn', '中文'),
    ('ja', '日本語'),
    ('fa', 'Persian'),
    ('ar', 'Arabic'),
    ('bn', 'Bengali'),
    ('ne', 'Nepali'),
    ('sq', 'Albanian'),
    ('af', 'Afrikaans'),
    ('sw', 'Swahili'),
    ('pt', 'Portuguese'),
    ('pt-br', 'Portuguese (Brazil)'),
    ('ru', 'Russian'),
    ('vi', 'Vietnamese'),
    ('ko', '한국어'),
    ('am', 'Amharic'),
    ('km', 'Khmer'),
    ('pl', 'Polish'),
    ('sv', 'Swedish'),
    ('th', 'ไทย'),
    ('uk', 'Ukranian'),
    ('si', 'Sinhala'),
    ('ta', 'Tamil'),
    ('tl', 'Tagalog'),
)

LANGUAGES = os.getenv('LANGUAGES', _DEFAULT_LANGUAGES)

EXTRA_LANG_INFO = {
    'am': {
        'bidi': False,
        'code': 'am',
        'name': 'Amharic',
        'name_local': 'Amharic',
        },
    'tl': {
        'bidi': False,
        'code': 'tl',
        'name': 'Tagalog',
        'name_local': 'tagalog',
        },
    'ta': {
        'bidi': False,
        'code': 'ta',
        'name': 'Tamil',
        'name_local': u'tamil',
        },
    'si': {
        'bidi': False,
        'code': 'si',
        'name': 'Sinhala',
        'name_local': 'sinhala',
        },
}

AUTH_USER_MODEL = os.getenv('AUTH_USER_MODEL', 'people.Profile')

MODELTRANSLATION_LANGUAGES = ['en', ]
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_FALLBACK_LANGUAGES = ('en',)


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(PROJECT_ROOT, "uploaded"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = os.getenv('MEDIA_URL', "/uploaded/")
LOCAL_MEDIA_URL = os.getenv('LOCAL_MEDIA_URL', "/uploaded/")

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.getenv('STATIC_ROOT', os.path.join(PROJECT_ROOT, "static_root"))

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = os.getenv('STATIC_URL', "/static/")

# Additional directories which hold static files
_DEFAULT_STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
    os.path.join(GEONODE_ROOT, "static"),
]

STATICFILES_DIRS = os.getenv('STATICFILES_DIRS', _DEFAULT_STATICFILES_DIRS)

# List of finder classes that know how to find static files in
# various locations.
_DEFAULT_STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
STATICFILES_FINDERS = os.getenv('STATICFILES_FINDERS',_DEFAULT_STATICFILES_FINDERS)

# Location of translation files
_DEFAULT_LOCALE_PATHS = (
    os.path.join(PROJECT_ROOT, "locale"),
    os.path.join(GEONODE_ROOT, "locale"),
)
LOCALE_PATHS = os.getenv('LOCALE_PATHS',_DEFAULT_LOCALE_PATHS)

# Location of url mappings
ROOT_URLCONF = os.getenv('ROOT_URLCONF', 'worldmap.urls')

# Login and logout urls override
LOGIN_URL = os.getenv('LOGIN_URL', '/account/login/')
LOGOUT_URL = os.getenv('LOGOUT_URL', '/account/logout/')

# Documents application
_DEFAULT_ALLOWED_DOCUMENT_TYPES = [
    'doc', 'docx', 'gif', 'jpg', 'jpeg', 'ods', 'odt', 'odp', 'pdf', 'png',
    'ppt', 'pptx', 'rar', 'sld', 'tif', 'tiff', 'txt', 'xls', 'xlsx', 'xml',
    'zip', 'gz', 'qml'
]
ALLOWED_DOCUMENT_TYPES = os.getenv('ALLOWED_DOCUMENT_TYPES', _DEFAULT_ALLOWED_DOCUMENT_TYPES)
MAX_DOCUMENT_SIZE = int(os.getenv('MAX_DOCUMENT_SIZE ', '2'))  # MB

# DOCUMENT_TYPE_MAP and DOCUMENT_MIMETYPE_MAP update enumerations in
# documents/enumerations.py and should only
# need to be uncommented if adding other types
# to settings.ALLOWED_DOCUMENT_TYPES

# DOCUMENT_TYPE_MAP = {}
# DOCUMENT_MIMETYPE_MAP = {}

WORLDMAP_APPS = (
    # WorldMap applications
    'worldmap',
    'wm_extra',
    'worldmap.certification',
)

GEONODE_APPS = (
    # GeoNode internal apps
    'geonode.people',
    'geonode.base',
    'geonode.layers',
    'geonode.maps',
    'geonode.proxy',
    'geonode.security',
    'geonode.social',
    'geonode.catalogue',
    'geonode.documents',
    'geonode.api',
    'geonode.groups',
    'geonode.services',

    # GeoServer Apps
    # Geoserver needs to come last because
    # it's signals may rely on other apps' signals.
    'geonode.geoserver',
    'geonode.upload',
    'geonode.tasks'
)


GEONODE_CONTRIB_APPS = (
    # GeoNode Contrib Apps
    'geonode.contrib.api_basemaps',
    'geonode.contrib.metadataxsl',
    'geonode.contrib.datatables',
    #'geonode.contrib.dynamic',
    #'geonode.contrib.exif',
    #'geonode.contrib.favorite',
    #'geonode.contrib.geogig',
    #'geonode.contrib.geosites',
    #'geonode.contrib.nlp',
    #'geonode.contrib.slack',
    'geonode.contrib.createlayer',
    'geonode.contrib.datastore_shards',
    'shared_dataverse_information.dataverse_info',           # external repository: https://github.com/IQSS/shared-dataverse-information
    'shared_dataverse_information.layer_classification',     # external repository: https://github.com/IQSS/shared-dataverse-information
    'geonode.contrib.dataverse_permission_links',
    'geonode.contrib.dataverse_layer_metadata', # uses the dataverse_info repository models
    'geonode.contrib.dataverse_connect',
    'geonode.contrib.dataverse_styles',
)


# Uncomment the following line to enable contrib apps
GEONODE_APPS = GEONODE_APPS + GEONODE_CONTRIB_APPS

_DEFAULT_INSTALLED_APPS = (

    'modeltranslation',

    # Boostrap admin theme
    # 'django_admin_bootstrapped.bootstrap3',
    # 'django_admin_bootstrapped',

    # Apps bundled with Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.gis',

    # Third party apps

    # Utility
    'pagination',
    'taggit',
    'friendlytagloader',
    'geoexplorer',
    'leaflet',
    'django_extensions',
    # 'geonode-client',
    # 'overextends',
    # 'haystack',
    'autocomplete_light',
    'mptt',
    # 'modeltranslation',
    #'djcelery',
    'storages',
    'floppyforms',

    # Theme
    "pinax_theme_bootstrap_account",
    "pinax_theme_bootstrap",
    'django_forms_bootstrap',

    # Social
    'account',
    'avatar',
    'dialogos',
    'agon_ratings',
    #'notification',
    'announcements',
    'actstream',
    'user_messages',
    'tastypie',
    'polymorphic',
    'guardian',
    'oauth2_provider',
    'corsheaders',
) +  GEONODE_APPS + WORLDMAP_APPS

INSTALLED_APPS = os.getenv('INSTALLED_APPS',_DEFAULT_INSTALLED_APPS)


_DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'ERROR',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR', 'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"], "level": "ERROR", },
        "geonode": {
            "handlers": ["console"], "level": "ERROR", },
        "gsconfig.catalog": {
            "handlers": ["console"], "level": "ERROR", },
        "owslib": {
            "handlers": ["console"], "level": "ERROR", },
        "pycsw": {
            "handlers": ["console"], "level": "ERROR", },
        },
    }

LOGGING = os.getenv('LOGGING', _DEFAULT_LOGGING)

#
# Customizations to built in Django settings required by GeoNode
#

# Django automatically includes the "templates" dir in all the INSTALLED_APPS.
TEMPLATES = [
    {
        'NAME': 'GeoNode Project Templates',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_ROOT, "templates"),
            os.path.join(GEONODE_ROOT, "templates")
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.tz',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'account.context_processors.account',
                'geonode.context_processors.resource_urls',
                'geonode.geoserver.context_processors.geoserver_urls',
                'worldmap.context_processors.worldmap',
            ],
            'debug': DEBUG,
        },
    }
]



_DEFAULT_MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # The setting below makes it possible to serve different languages per
    # user depending on things like headers in HTTP requests.
    'django.middleware.locale.LocaleMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # This middleware allows to print private layers for the users that have
    # the permissions to view them.
    # It sets temporary the involved layers as public before restoring the
    # permissions.
    # Beware that for few seconds the involved layers are public there could be
    # risks.
    # 'geonode.middleware.PrintProxyMiddleware',

    # If you use SessionAuthenticationMiddleware, be sure it appears before OAuth2TokenMiddleware.
    # SessionAuthenticationMiddleware is NOT required for using django-oauth-toolkit.
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
)
MIDDLEWARE_CLASSES = os.getenv('MIDDLEWARE_CLASSES',_DEFAULT_MIDDLEWARE_CLASSES)



# Replacement of default authentication backend in order to support
# permissions per object.
_DEFAULT_AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
AUTHENTICATION_BACKENDS = os.getenv('AUTHENTICATION_BACKENDS', _DEFAULT_AUTHENTICATION_BACKENDS)

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups'
    },

    'CLIENT_ID_GENERATOR_CLASS': 'oauth2_provider.generators.ClientIdGenerator',
}

ANONYMOUS_USER_ID = os.getenv('ANONYMOUS_USER_ID','-1')
GUARDIAN_GET_INIT_ANONYMOUS_USER =os.getenv('GUARDIAN_GET_INIT_ANONYMOUS_USER','geonode.people.models.get_anonymous_user_instance')

# Whether the uplaoded resources should be public and downloadable by default or not
DEFAULT_ANONYMOUS_VIEW_PERMISSION = str2bool(os.getenv('DEFAULT_ANONYMOUS_VIEW_PERMISSION', 'True'))
DEFAULT_ANONYMOUS_DOWNLOAD_PERMISSION = str2bool(os.getenv('DEFAULT_ANONYMOUS_VIEW_PERMISSION', 'True'))

#
# Settings for default search size
#
DEFAULT_SEARCH_SIZE = int(os.getenv('DEFAULT_SEARCH_SIZE','10'))


#
# Settings for third party apps
#

# Agon Ratings
AGON_RATINGS_CATEGORY_CHOICES = {
    "maps.Map": {
        "map": "How good is this map?"
    },
    "layers.Layer": {
        "layer": "How good is this layer?"
    },
    "documents.Document": {
        "document": "How good is this document?"
    }
}

# Activity Stream
_DEFAULT_ACTSTREAM_SETTINGS = {
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': False,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

ACTSTREAM_SETTINGS = os.getenv('ACTSTREAM_SETTINGS',_DEFAULT_ACTSTREAM_SETTINGS)

# Email settings
EMAIL_ENABLE = False

if EMAIL_ENABLE:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = 'GeoNode <no-reply@geonode.org>'

# Settings for Social Apps
REGISTRATION_OPEN =  str2bool(os.getenv('REGISTRATION_OPEN', 'False'))
ACCOUNT_EMAIL_CONFIRMATION_EMAIL = str2bool(os.getenv('ACCOUNT_EMAIL_CONFIRMATION_EMAIL', 'False'))
ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = str2bool(os.getenv('ACCOUNT_EMAIL_CONFIRMATION_REQUIRED', 'False'))
ACCOUNT_APPROVAL_REQUIRED = str2bool(os.getenv('ACCOUNT_APPROVAL_REQUIRED', 'False'))
ACCOUNT_USE_AUTH_AUTHENTICATE = str2bool(os.getenv('ACCOUNT_USE_AUTH_AUTHENTICATE', 'False'))
# Email for users to contact admins.
THEME_ACCOUNT_CONTACT_EMAIL = os.getenv('THEME_ACCOUNT_CONTACT_EMAIL','admin@example.com')

#
# Test Settings
#

# Setting a custom test runner to avoid running the tests for
# some problematic 3rd party apps
TEST_RUNNER =os.getenv('TEST_RUNNER', 'django_nose.NoseTestSuiteRunner')

# Arguments for the test runner

_DEFAULT_NOSE_ARGS = [
      '--verbosity=2',
      '--cover-erase',
      '--nocapture',
      '--with-coverage',
      '--cover-package=geonode',
      '--cover-inclusive',
      '--cover-tests',
      '--detailed-errors',
      '--with-xunit',

# This is very beautiful/usable but requires: pip install rudolf
#      '--with-color',

# The settings below are useful while debugging test failures or errors

#      '--failed',
#      '--pdb-failures',
#      '--stop',
#      '--pdb',
      ]
NOSE_ARGS = os.getenv('NOSE_ARGS',_DEFAULT_NOSE_ARGS)

# this is for the gazetteer
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY',"gme-harvarduniversity1")
# this is for the basemaps
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', None)

# GOOGLE_SECRET_KEY = None

GEONAMES_USER = ''
#
# GeoNode specific settings
#

SITEURL = os.getenv('SITEURL',"http://localhost:8000/")
SITENAME = 'worldmap'

USE_QUEUE = str2bool(os.getenv('USE_QUEUE', 'False'))

DEFAULT_WORKSPACE = os.getenv('DEFAULT_WORKSPACE','geonode')
CASCADE_WORKSPACE = os.getenv('CASCADE_WORKSPACE','geonode')

OGP_URL = os.getenv('OGP_URL',"http://geodata.tufts.edu/solr/select")

# Topic Categories list should not be modified (they are ISO). In case you
# absolutely need it set to True this variable
MODIFY_TOPICCATEGORY = str2bool(os.getenv('MODIFY_TOPICCATEGORY', 'False'))

MISSING_THUMBNAIL = os.getenv('MISSING_THUMBNAIL','geonode/img/missing_thumb.png')

# Search Snippet Cache Time in Seconds
CACHE_TIME = int(os.getenv('CACHE_TIME','0'))

GEOSERVER_LOCATION = os.getenv(
    'GEOSERVER_LOCATION', 'http://localhost:8080/geoserver/'
)

GEOSERVER_PUBLIC_LOCATION = os.getenv(
    'GEOSERVER_PUBLIC_LOCATION', 'http://localhost:8080/geoserver/'
)

OGC_SERVER_DEFAULT_USER = os.getenv(
    'GEOSERVER_ADMIN_USER', 'admin'
)

OGC_SERVER_DEFAULT_PASSWORD = os.getenv(
    'GEOSERVER_ADMIN_PASSWORD', 'geoserver'
)

GEOFENCE_SECURITY_ENABLED = True

# OGC (WMS/WFS/WCS) Server Settings
# OGC (WMS/WFS/WCS) Server Settings
OGC_SERVER = {
    'default': {
        'BACKEND': 'geonode.geoserver',
        'LOCATION': GEOSERVER_LOCATION,
        'LOGIN_ENDPOINT': 'j_spring_oauth2_geonode_login',
        'LOGOUT_ENDPOINT': 'j_spring_oauth2_geonode_logout',
        # PUBLIC_LOCATION needs to be kept like this because in dev mode
        # the proxy won't work and the integration tests will fail
        # the entire block has to be overridden in the local_settings
        'PUBLIC_LOCATION': GEOSERVER_PUBLIC_LOCATION,
        'USER': OGC_SERVER_DEFAULT_USER,
        'PASSWORD': OGC_SERVER_DEFAULT_PASSWORD,
        'MAPFISH_PRINT_ENABLED': True,
        'PRINT_NG_ENABLED': True,
        'GEONODE_SECURITY_ENABLED': True,
        'GEOFENCE_SECURITY_ENABLED': GEOFENCE_SECURITY_ENABLED,
        'GEOGIG_ENABLED': False,
        'WMST_ENABLED': False,
        'BACKEND_WRITE_ENABLED': True,
        'WPS_ENABLED': False,
        'LOG_FILE': '%s/geoserver/data/logs/geoserver.log'
        % os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir)),
        # Set to name of database in DATABASES dictionary to enable
        'DATASTORE': 'datastore',
        'PG_GEOGIG': False,
        'TIMEOUT': 10  # number of seconds to allow for HTTP requests
    }
}

# Uploader Settings
_DEFAULT_UPLOADER = {
    'BACKEND': 'geonode.rest',
    'OPTIONS': {
        'TIME_ENABLED': False,
        'MOSAIC_ENABLED': False,
        'GEOGIG_ENABLED': False,
    }
}
UPLOADER = os.getenv('UPLOADER', _DEFAULT_UPLOADER)

# CSW settings
_DEFAULT_CATALOGUE = {
    'default': {
        # The underlying CSW implementation
        # default is pycsw in local mode (tied directly to GeoNode Django DB)
        'ENGINE': 'geonode.catalogue.backends.pycsw_local',
        # pycsw in non-local mode
        # 'ENGINE': 'geonode.catalogue.backends.pycsw_http',
        # GeoNetwork opensource
        # 'ENGINE': 'geonode.catalogue.backends.geonetwork',
        # deegree and others
        # 'ENGINE': 'geonode.catalogue.backends.generic',

        # The FULLY QUALIFIED base url to the CSW instance for this GeoNode
        'URL': '%scatalogue/csw' % SITEURL,
        # 'URL': 'http://localhost:8080/geonetwork/srv/en/csw',
        # 'URL': 'http://localhost:8080/deegree-csw-demo-3.0.4/services',

        # login credentials (for GeoNetwork)
        # 'USER': 'admin',
        # 'PASSWORD': 'admin',
    }
}
CATALOGUE = os.getenv('CATALOGUE',_DEFAULT_CATALOGUE)
# pycsw settings
_DEFAULT_PYSCSW = {
    # pycsw configuration
    'CONFIGURATION': {
        # uncomment / adjust to override server config system defaults
        #'server': {
        #    'maxrecords': '10',
        #    'pretty_print': 'true',
        #    'federatedcatalogues': 'http://catalog.data.gov/csw'
        #},
        'metadata:main': {
            'identification_title': 'worldmap Catalogue',
            'identification_abstract': 'GeoNode is an open source platform that facilitates the creation, sharing, ' \
            'and collaborative use of geospatial data',
            'identification_keywords': 'sdi,catalogue,discovery,metadata,GeoNode, worldmap',
            'identification_keywords_type': 'theme',
            'identification_fees': 'None',
            'identification_accessconstraints': 'None',
            'provider_name': 'Organization Name',
            'provider_url': SITEURL,
            'contact_name': 'Lastname, Firstname',
            'contact_position': 'Position Title',
            'contact_address': 'Mailing Address',
            'contact_city': 'City',
            'contact_stateorprovince': 'Administrative Area',
            'contact_postalcode': 'Zip or Postal Code',
            'contact_country': 'Country',
            'contact_phone': '+xx-xxx-xxx-xxxx',
            'contact_fax': '+xx-xxx-xxx-xxxx',
            'contact_email': 'Email Address',
            'contact_url': 'Contact URL',
            'contact_hours': 'Hours of Service',
            'contact_instructions': 'During hours of service. Off on weekends.',
            'contact_role': 'pointOfContact',
        },
        'metadata:inspire': {
            'enabled': 'true',
            'languages_supported': 'eng,gre',
            'default_language': 'eng',
            'date': 'YYYY-MM-DD',
            'gemet_keywords': 'Utility and governmental services',
            'conformity_service': 'notEvaluated',
            'contact_name': 'Organization Name',
            'contact_email': 'Email Address',
            'temp_extent': 'YYYY-MM-DD/YYYY-MM-DD',
        }
    }
}

PYCSW = os.getenv('PYCSW',_DEFAULT_PYSCSW)

# GeoNode javascript client configuration

# default map projection
# Note: If set to EPSG:4326, then only EPSG:4326 basemaps will work.
DEFAULT_MAP_CRS = os.getenv('DEFAULT_MAP_CRS',"EPSG:900913")

#GeoNode Client
GEONODE_CLIENT_LOCATION = os.getenv('GEONODE_CLIENT_LOCATION',
                                     '/static/worldmap_client/')
#GEONODE_CLIENT_LOCATION = "http://localhost:9090/"

# Where should newly created maps be focused?
DEFAULT_MAP_CENTER = (0, 0)

# How tightly zoomed should newly created maps be?
# 0 = entire world;
# maximum zoom is between 12 and 15 (for Google Maps, coverage varies by area)
DEFAULT_MAP_ZOOM = int(os.getenv('DEFAULT_MAP_ZOOM','0'))

ALT_OSM_BASEMAPS = os.environ.get('ALT_OSM_BASEMAPS', False)
CARTODB_BASEMAPS = os.environ.get('CARTODB_BASEMAPS', False)
STAMEN_BASEMAPS = os.environ.get('STAMEN_BASEMAPS', False)
THUNDERFOREST_BASEMAPS = os.environ.get('THUNDERFOREST_BASEMAPS', False)
MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN', None)
BING_API_KEY = os.environ.get('BING_API_KEY', None)

_INIT_DEFAULT_LAYER_SOURCE = {
    "ptype":"gxp_wmscsource",
    "url":"/geoserver/wms",
    "restUrl": "/gs/rest"
}



DEFAULT_LAYER_SOURCE = os.getenv('DEFAULT_LAYER_SOURCE',_INIT_DEFAULT_LAYER_SOURCE)
_DEFAULT_MAP_BASELAYERS = [
    {
        "source": {
            "ptype": "gxp_gnsource",
            "url": GEOSERVER_BASE_URL + "wms",
            "restUrl": "/gs/rest"
        }
    }, {
        "source": {"ptype": "gx_olsource"},
        "type": "OpenLayers.Layer",
        "args": ["No background"],
        "visibility": False,
        "fixed": True,
        "group": "background"
    }, {
        "source": {"ptype": "gx_olsource"},
        "type": "OpenLayers.Layer.OSM",
        "args": ["OpenStreetMap"],
        "visibility": False,
        "fixed": True,
        "group": "background"
    },
    {
        "source": {
            "ptype": "gxp_bingsource",
            "apiKey": BING_API_KEY
        },
        "name": "AerialWithLabels",
        "fixed": True,
        "visibility": False,
        "group": "background"
    },
    {
        "source": {"ptype": "gxp_mapboxsource"},
    },
    {
        "source": {"ptype": "gxp_stamensource"},
        "name": "watercolor",
        "visibility": False,
        "group": "background",
        "title": "Stamen Watercolor"
        },
    {
        "source": {"ptype": "gxp_stamensource"},
        "name": "toner",
        "visibility": False,
        "group": "background",
        "title": "Stamen Toner"
    },
    {
        "source": {
            "url": "http://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer",
            "ptype": "gxp_arcgiscachesource"},
        "group": "background",
        "name": "World Street Map",
        "visibility": False,
        "fixed": True,
        "format": "jpeg",
        "tiled" : False,
        "title": "ESRI World Street Map"
    },{
        "source": {
            "url": "http://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer",
            "ptype": "gxp_arcgiscachesource"},
        "group": "background",
        "format": "jpeg",
        "name": "World Imagery",
        "visibility": False,
        "fixed": True,
        "tiled" : False,
        "title": "ESRI World Imagery"
    },
    {
        "source": {
            "url": "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer",
            "ptype": "gxp_arcgiscachesource"},
        "group": "background",
        "name": "Light Gray Canvas Base",
        "visibility": False,
        "fixed": True,
        "format": "jpeg",
        "tiled" : False,
        "title": "ESRI Light Gray Reference"
    },
    {
        "source": {
            "url": "http://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer",
            "ptype": "gxp_arcgiscachesource"},
        "group": "background",
        "name": "Dark Gray Canvas Base",
        "visibility": False,
        "fixed": True,
        "format": "jpeg",
        "tiled" : False,
        "title": "ESRI Dark Gray Reference"
    },
    {
        "source": {
            "ptype": "gxp_googlesource"
        },
        "group": "background",
        "name": "SATELLITE",
        "visibility": False,
        "fixed": True,
    },
    {
        "source": {
            "ptype": "gxp_googlesource",
        },
        "group": "background",
        "name": "TERRAIN",
        "visibility": True,
        "fixed": True,
    }, {
        "source": {
            "ptype": "gxp_googlesource"
        },
        "group": "background",
        "name": "HYBRID",
        "visibility": False,
        "fixed": True,
    }, {
        "source": {
            "ptype": "gxp_googlesource"
        },
        "group": "background",
        "name": "ROADMAP",
        "visibility": False,
        "fixed": True,
        "group": "background"
    }
]

MAP_BASELAYERS = os.getenv('MAP_BASELAYERS',_DEFAULT_MAP_BASELAYERS)

DISPLAY_SOCIAL = strtobool(os.getenv('DISPLAY_SOCIAL', 'True'))
DISPLAY_COMMENTS = strtobool(os.getenv('DISPLAY_COMMENTS', 'True'))
DISPLAY_RATINGS = strtobool(os.getenv('DISPLAY_RATINGS', 'True'))
DISPLAY_WMS_LINKS = strtobool(os.getenv('DISPLAY_WMS_LINKS', 'True'))

_DEFAULT_SOCIAL_ORIGINS = [{
    "label":"Email",
    "url":"mailto:?subject={name}&body={url}",
    "css_class":"email"
}, {
    "label":"Facebook",
    "url":"http://www.facebook.com/sharer.php?u={url}",
    "css_class":"fb"
}, {
    "label":"Twitter",
    "url":"https://twitter.com/share?url={url}&hashtags={hashtags}",
    "css_class":"tw"
}, {
    "label":"Google +",
    "url":"https://plus.google.com/share?url={url}",
    "css_class":"gp"
}]
SOCIAL_ORIGINS = os.getenv('SOCIAL_ORIGINS',_DEFAULT_SOCIAL_ORIGINS)
#CKAN Query String Parameters names pulled from
#https://github.com/ckan/ckan/blob/2052628c4a450078d58fb26bd6dc239f3cc68c3e/ckan/logic/action/create.py#L43
CKAN_ORIGINS = [{
    "label":"Humanitarian Data Exchange (HDX)",
    "url":"https://data.hdx.rwlabs.org/dataset/new?title={name}&dataset_date={date}&notes={abstract}&caveats={caveats}",
    "css_class":"hdx"
}]
#SOCIAL_ORIGINS.extend(CKAN_ORIGINS)

# Setting TWITTER_CARD to True will enable Twitter Cards
# https://dev.twitter.com/cards/getting-started
# Be sure to replace @GeoNode with your organization or site's twitter handle.
TWITTER_CARD = str2bool(os.getenv('TWITTER_CARD', 'True'))
TWITTER_SITE = '@GeoNode'
TWITTER_HASHTAGS = ['geonode']

OPENGRAPH_ENABLED =  str2bool(os.getenv('OPENGRAPH_ENABLED', 'True'))

# Enable Licenses User Interface
# Regardless of selection, license field stil exists as a field in the Resourcebase model.
# Detail Display: above, below, never
# Metadata Options: verbose, light, never
_DEFAULT_LICENSES = {
    'ENABLED': True,
    'DETAIL': 'above',
    'METADATA': 'verbose',
}

LICENSES = os.getenv('LICENSES',_DEFAULT_LICENSES)

_DEFAULT_SRID = {
    'DETAIL': 'never',
}

SRID = os.getenv('SRID',_DEFAULT_SRID)

SESSION_SERIALIZER = os.getenv('SESSION_SERIALIZER','django.contrib.sessions.serializers.PickleSerializer')

# Require users to authenticate before using Geonode
LOCKDOWN_GEONODE = str2bool(os.getenv('LOCKDOWN_GEONODE', 'False'))

# Add additional paths (as regular expressions) that don't require
# authentication.
AUTH_EXEMPT_URLS = ('/api/o/*', '/api/roles', '/api/adminRole', '/api/users',)

# A tuple of hosts the proxy can send requests to.
PROXY_ALLOWED_HOSTS = ()

# The proxy to use when making cross origin requests.
PROXY_URL = '/proxy/?url=' if DEBUG else None

# Haystack Search Backend Configuration.  To enable, first install the following:
# - pip install django-haystack
# - pip install pyelasticsearch
# Set HAYSTACK_SEARCH to True
# Run "python manage.py rebuild_index"
HAYSTACK_SEARCH = str2bool(os.getenv('HAYSTACK_SEARCH', 'False'))
# Avoid permissions prefiltering
SKIP_PERMS_FILTER = str2bool(os.getenv('SKIP_PERMS_FILTER', 'False'))
# Update facet counts from Haystack
HAYSTACK_FACET_COUNTS = str2bool(os.getenv('HAYSTACK_FACET_COUNTS', 'False'))
# HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
#        'URL': 'http://127.0.0.1:9200/',
#        'INDEX_NAME': 'geonode',
#        },
#    }
# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# HAYSTACK_SEARCH_RESULTS_PER_PAGE = 20

# Available download formats
DOWNLOAD_FORMATS_METADATA = [
    'Atom', 'DIF', 'Dublin Core', 'ebRIM', 'FGDC', 'ISO',
]
DOWNLOAD_FORMATS_VECTOR = [
    'JPEG', 'PDF', 'PNG', 'Zipped Shapefile', 'GML 2.0', 'GML 3.1.1', 'CSV',
    'Excel', 'GeoJSON', 'KML', 'View in Google Earth', 'Tiles',
]
DOWNLOAD_FORMATS_RASTER = [
    'JPEG',
    'PDF',
    'PNG',
    'ArcGrid',
    'GeoTIFF',
    'Gtopo30',
    'ImageMosaic',
    'KML',
    'View in Google Earth',
    'Tiles',
    'GML',
    'GZIP'
]

ACCOUNT_NOTIFY_ON_PASSWORD_CHANGE = str2bool(os.getenv('ACCOUNT_NOTIFY_ON_PASSWORD_CHANGE', 'False'))

TASTYPIE_DEFAULT_FORMATS = ['json']

# gravatar settings
AUTO_GENERATE_AVATAR_SIZES = (20, 32, 80, 100, 140, 200)

# notification settings
NOTIFICATION_LANGUAGE_MODULE = os.getenv('NOTIFICATION_LANGUAGE_MODULE',"account.Account")

# Number of results per page listed in the GeoNode search pages
CLIENT_RESULTS_LIMIT = int (os.getenv('CLIENT_RESULTS_LIMIT','100'))

# Number of items returned by the apis 0 equals no limit
API_LIMIT_PER_PAGE = int(os.getenv('API_LIMIT_PER_PAGE','0'))
API_INCLUDE_REGIONS_COUNT = str2bool(os.getenv('API_INCLUDE_REGIONS_COUNT', 'False'))

_DEFAULT_LEAFLET_CONFIG = {
    'TILES': [
        # Find tiles at:
        # http://leaflet-extras.github.io/leaflet-providers/preview/

        # Stamen toner lite.
        ('Watercolor',
         'http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.png',
         'Map tiles by <a href="http://stamen.com">Stamen Design</a>, \
         <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> \
         &mdash; Map data &copy; \
         <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, \
         <a href="http://creativecommons.org/licenses/by-sa/2.0/"> \
         CC-BY-SA</a>'),
        ('Toner Lite',
         'http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png',
         'Map tiles by <a href="http://stamen.com">Stamen Design</a>, \
         <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> \
         &mdash; Map data &copy; \
         <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, \
         <a href="http://creativecommons.org/licenses/by-sa/2.0/"> \
         CC-BY-SA</a>'),
    ],
    'PLUGINS': {
        'esri-leaflet': {
            'js': 'lib/js/esri-leaflet.js',
            'auto-include': True,
        },
        'leaflet-fullscreen': {
            'css': 'lib/css/leaflet.fullscreen.css',
            'js': 'lib/js/Leaflet.fullscreen.min.js',
            'auto-include': True,
        },
        'leaflet-opacity': {
            'css': 'lib/css/Control.Opacity.css',
            'js': 'lib/js/Control.Opacity.js',
            'auto-include': True,
        },
        'leaflet-navbar': {
            'css': 'lib/css/Leaflet.NavBar.css',
            'js': 'lib/js/Leaflet.NavBar.js',
            'auto-include': True,
        },
        'leaflet-measure': {
            'css': 'lib/css/leaflet-measure.css',
            'js': 'lib/js/leaflet-measure.js',
            'auto-include': True,
        },
    },
    'SRID': 3857,
    'RESET_VIEW': False
}

LEAFLET_CONFIG = os.getenv('LEAFLET_CONFIG',_DEFAULT_LEAFLET_CONFIG)

if not DEBUG_STATIC:
    # if not DEBUG_STATIC, use minified css and js
    LEAFLET_CONFIG['PLUGINS'] = {
        'leaflet-plugins': {
            'js': 'lib/js/leaflet-plugins.min.js',
            'css': 'lib/css/leaflet-plugins.min.css',
            'auto-include': True,
        }
    }

# option to enable/disable resource unpublishing for administrators
RESOURCE_PUBLISHING = False

# Settings for EXIF contrib app
EXIF_ENABLED = False

# Settings for NLP contrib app
NLP_ENABLED = False
NLP_LOCATION_THRESHOLD = 1.0
NLP_LIBRARY_PATH = os.getenv('NLP_LIBRARY_PATH',"/opt/MITIE/mitielib")
NLP_MODEL_PATH = os.getenv('NLP_MODEL_PATH',"/opt/MITIE/MITIE-models/english/ner_model.dat")

# Settings for Slack contrib app
SLACK_ENABLED = False
SLACK_WEBHOOK_URLS = [
    "https://hooks.slack.com/services/T000/B000/XX"
]

CACHES = {
    # DUMMY CACHE FOR DEVELOPMENT
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    # MEMCACHED EXAMPLE
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    #     'LOCATION': '127.0.0.1:11211',
    #     },
    # FILECACHE EXAMPLE
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #     'LOCATION': '/tmp/django_cache',
    #     }
}

LAYER_PREVIEW_LIBRARY = os.getenv("LAYER_PREVIEW_LIBRARY","worldmap")

SERVICE_UPDATE_INTERVAL = 0


SEARCH_FILTERS = {
    'TEXT_ENABLED': True,
    'TYPE_ENABLED': True,
    'CATEGORIES_ENABLED': True,
    'OWNERS_ENABLED': True,
    'KEYWORDS_ENABLED': True,
    'H_KEYWORDS_ENABLED': True,
    'T_KEYWORDS_ENABLED': True,
    'DATE_ENABLED': True,
    'REGION_ENABLED': True,
    'EXTENT_ENABLED': True,
}

# Make Free-Text Kaywords writable from users or read-only
# - if True only admins can edit free-text kwds from admin dashboard
FREETEXT_KEYWORDS_READONLY = False

# Queue non-blocking notifications.
NOTIFICATION_QUEUE_ALL = False
PINAX_NOTIFICATIONS_QUEUE_ALL = False

BROKER_URL = "django://"
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_IGNORE_RESULT = True
CELERY_SEND_EVENTS = False
CELERY_RESULT_BACKEND = None
CELERY_TASK_RESULT_EXPIRES = 1
CELERY_DISABLE_RATE_LIMITS = True
CELERY_DEFAULT_QUEUE = "default"
CELERY_DEFAULT_EXCHANGE = "default"
CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_DEFAULT_ROUTING_KEY = "default"
CELERY_CREATE_MISSING_QUEUES = True
CELERY_IMPORTS = (
    'geonode.tasks.deletion',
    'geonode.tasks.update',
    'geonode.tasks.email'
)


CELERY_QUEUES = [
    Queue('default', routing_key='default'),
    Queue('cleanup', routing_key='cleanup'),
    Queue('update', routing_key='update'),
    Queue('email', routing_key='email'),
]


# AWS S3 Settings

S3_STATIC_ENABLED = os.environ.get('S3_STATIC_ENABLED', False)
S3_MEDIA_ENABLED = os.environ.get('S3_MEDIA_ENABLED', False)

# Required to run Sync Media to S3
AWS_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', '')

AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', '')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_S3_BUCKET_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_QUERYSTRING_AUTH = False

if S3_STATIC_ENABLED:
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATIC_URL = "https://%s/%s/" % (AWS_S3_BUCKET_DOMAIN, STATICFILES_LOCATION)

if S3_MEDIA_ENABLED:
    MEDIAFILES_LOCATION = 'media'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_BUCKET_DOMAIN, MEDIAFILES_LOCATION)

#djcelery.setup_loader()

# Load additonal basemaps, see geonode/contrib/api_basemap/README.md
# TODO: Before the 2.5 release, let's change the line below. Apparently it is
# doing a circular import, we should not need to do a import * from here.
try:
    from geonode.contrib.api_basemaps import *
except ImportError:
    pass

# Require users to authenticate before using Geonode
if LOCKDOWN_GEONODE:
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + \
        ('geonode.security.middleware.LoginRequiredMiddleware',)

#for windows users check if they didn't set GEOS and GDAL in local_settings.py
#maybe they set it as a windows environment
if os.name == 'nt':
    if not "GEOS_LIBRARY_PATH" in locals() or not "GDAL_LIBRARY_PATH" in locals():
        if os.environ.get("GEOS_LIBRARY_PATH", None) \
            and os.environ.get("GDAL_LIBRARY_PATH", None):
            GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')
            GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')
        else:
            #maybe it will be found regardless if not it will throw 500 error
            from django.contrib.gis.geos import GEOSGeometry


# define the urls after the settings are overridden
USE_GEOSERVER = 'geonode.geoserver' in INSTALLED_APPS
if USE_GEOSERVER:
    LOCAL_GEOSERVER = {
        "source": {
            "ptype": "gxp_wmscsource",
            "url": OGC_SERVER['default']['PUBLIC_LOCATION'] + "wms",
            "restUrl": "/gs/rest"
        }
    }
    baselayers = MAP_BASELAYERS
    MAP_BASELAYERS = [LOCAL_GEOSERVER]
    MAP_BASELAYERS.extend(baselayers)

    def get_user_url(u):
        from django.contrib.sites.models import Site
        s = Site.objects.get_current()
        return "http://" + s.domain + "/profiles/" + u.username


    _DEFAULT_ABSOLUTE_URL_OVERRIDES = {
        'auth.user': get_user_url
    }
    ABSOLUTE_URL_OVERRIDES = os.getenv('ABSOLUTE_URL_OVERRIDES',_DEFAULT_ABSOLUTE_URL_OVERRIDES)
    AUTH_PROFILE_MODULE = os.getenv('AUTH_PROFILE_MODULE','maps.Contact')
    REGISTRATION_OPEN =  str2bool(os.getenv('REGISTRATION_OPEN', 'True'))

    ACCOUNT_ACTIVATION_DAYS = int(os.getenv('ACCOUNT_ACTIVATION_DAYS','7'))

    # TODO: Allow overriding with an env var
    DB_DATASTORE = str2bool(os.getenv('DB_DATASTORE', 'True'))

"""
START GAZETTEER SETTINGS
"""
# Defines settings for multiple databases,
# only use if PostGIS integration enabled
USE_GAZETTEER = str2bool(os.getenv('USE_GAZETTEER', 'False'))
if USE_GAZETTEER:
    INSTALLED_APPS += ('geonode.gazetteer', )
    GAZETTEER_DB_ALIAS = "wmdata"
    GAZETTEER_FULLTEXTSEARCH = False

"""
END GAZETTEER SETTINGS
"""

# Keywords thesauri
# e.g. THESAURI = [{'name':'inspire_themes', 'required':True, 'filter':True}, {'name':'inspire_concepts', 'filter':True}, ]
# Required: (boolean, optional, default false) mandatory while editing metadata (not implemented yet)
# Filter: (boolean, optional, default false) a filter option on that thesaurus will appear in the main search page
THESAURI = []
DISABLE_SECURITY = str2bool(os.getenv('DISABLE_SECURITY', 'False'))
# WorldMap client settings
HYPERMAP_REGISTRY_URL = os.getenv('HYPERMAP_REGISTRY_URL', "http://192.168.33.15:8002")
MAPPROXY_URL = os.getenv('MAPPROXY_URL', "http://192.168.33.15:8002")
SOLR_URL = os.getenv('SOLR_URL', "http://192.168.33.15:8983/solr/hypermap/select")

# Each uploaded Layer must be approved by an Admin before becoming visible
ADMIN_MODERATE_UPLOADS = False

# If this option is enabled, Resources belonging to a Group won't be visible by others
GROUP_PRIVATE_RESOURCES = False

# If this option is enabled, Groups will become strictly Mandatory on Metadata Wizard
GROUP_MANDATORY_RESOURCES = False

ASYNC_SIGNALS_BROKER_URL = 'memory://'

# A boolean which specifies wether to display the email in user's profile
SHOW_PROFILE_EMAIL = False

MONITORING_ENABLED = False

DB_DATAVERSE_NAME = 'dataverse'
DATAVERSE_GROUP_NAME = 'dataverse'

# There are 3 ways to override GeoNode settings:
# 1. Using environment variables, if your changes to GeoNode are minimal.
# 2. Creating a downstream project, if you are doing a lot of customization.
# 3. Override settings in a local_settings.py file, legacy.
# Load more settings from a file called local_settings.py if it exists
try:
    from local_settings import *  # noqa
except ImportError:
    pass
