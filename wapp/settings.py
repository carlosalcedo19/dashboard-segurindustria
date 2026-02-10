
from django.urls import reverse_lazy
from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-e)0xx#g)wo*uqr!jqjhx)e!#n0kr=fk$f6lo*ri@z-m(z4m7au'

DEBUG = False

ALLOWED_HOSTS = [ ".onrender.com",]



BASE_APPS = [
    "unfold", 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'apps.users.apps.UsersConfig',
    'apps.base.apps.BaseConfig',
    'apps.crm',
    'apps.client',
    'apps.maintenance',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

#DATABASES = {
#    'default': {
#        'ENGINE': os.getenv('DATABASE_ENGINE'),
#          'NAME': os.getenv('DATABASE_NAME'),
#          'USER': os.getenv('DATABASE_USER'),
#          'PASSWORD': os.getenv('DATABASE_PASSWORD'),
#          'HOST': os.getenv('DATABASE_HOST'),
#          'PORT': int(os.getenv('DATABASE_PORT')),
#          'CONN_MAX_AGE': 300
#      }
#  }


UNFOLD = {
    
    "SITE_TITLE": "Segurindustria CRM Cloud",
    "SITE_HEADER": "Segurindustria CRM ",
    "SITE_URL": "/admin",
    "LOGIN": {
         "image": "https://cdn-img.segurindustria.pe/wp-content/uploads/2024/02/Bg-ProductosDestacados-Nosotros-Mobile.webp",
         #"redirect_after": lambda r: reverse_lazy("admin:project_project_changelist"),
    },
    "COLORS": {
          "primary": {
                "50": "239 243 255",
                "100": "224 231 255",
                "200": "199 210 254",
                "300": "165 180 252",
                "400": "129 149 247",
                "500": "64 104 237",
                "600": "55 90 210",
                "700": "46 76 182",
                "800": "37 62 154",
                "900": "28 48 126",
                "950": "17 29 77"
            }
    },
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Autenticación y autorización",
                "separator": False,
                "items": [
                    {
                        "title": "Usuarios",
                        "icon": "person",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                    {
                        "title": "Permisos",
                        "icon": "lock",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    }
                    
                ],
            },
            {
                "title": "CRM",
                "separator": True,
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": "/admin/crm/lead/dashboard/", 
                    },
                    {
                        "title": "Clientes",
                        "icon": "family_restroom",
                        "link": reverse_lazy("admin:client_client_changelist"),
                    },   
                    {
                        "title": "Leads",
                        "icon": "balcony",
                        "link": reverse_lazy("admin:crm_lead_changelist"),
                    }, 
                ],
            },
            {
                "title": "Mantenimiento",
                "separator": True,
                "items": [
                    {
                        "title": "Canales de Venta",
                        "icon": "settings_account_box",
                        "link": reverse_lazy("admin:maintenance_channel_changelist"),
                    },   
                    {
                        "title": "Productos",
                        "icon": "balcony",
                        "link": reverse_lazy("admin:maintenance_product_changelist"),
                    }, 
                ],
            },
        ]
    }
}

ROOT_URLCONF = 'wapp.urls'
ICON_EDIT_URL = '/static/admin/img/visible.png'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-pe'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/



STATIC_ROOT = os.getenv('STATIC_ROOT')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
