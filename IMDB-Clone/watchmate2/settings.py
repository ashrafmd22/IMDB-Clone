"""
Django settings for watchmate2 project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4*hsl=ujg9e!)uco4r9j0ff*t!^qboeo@rbs0zq!0e(xvw8l0*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'watchlist_app',
    'rest_framework.authtoken', #ye likha h for token authentication ye likhne se ek table ban jaaygi for tokens
    'django_filters',#django filter use krne ke liye likha h 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'watchmate2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'watchmate2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# permission ke liye likhna h ye 
# dekh tu permission tu do way se laga skta h pehle uss particular view m 
# usse object level permission kehte h to sirf usi m permission lgegi 
# and dusra setting m lagayga to sabme lag jaaygi
# dekh mene setting m ISAUTHENTICATED laga diya to ye sari classes pr lag gaya h 
REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
#    'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.BasicAuthentication',
        
#     ],
'DEFAULT_AUTHENTICATION_CLASSES': [
       'rest_framework.authentication.TokenAuthentication',
    # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        
   ],
#    'DEFAULT_THROTTLE_CLASSES': [
#        'rest_framework.throttling.AnonRateThrottle',
#        'rest_framework.throttling.UserRateThrottle',
#    ], #dekh throttle se number of request control kr skta h like yaha setting m tune mention kiya throttle
#  anon=1 mtlb jisne login nhi kiya wo bas ek rewuest bhej skta h ek din m and jisne login kiya h wo 3 request
#    bhej skta h ek din m chahe wo koi bhi url aceess kre becoz setting m throttle mention krne se poore
#    view m lag jaata h
   'DEFAULT_THROTTLE_RATES': {
       'anon': '5/day',
       'user': '10/day',
       'review-create': '1/day',#jaha bhi review-create wala throttling scope use krega waha tu bas 1 hi request
    #    send kr skta h only on url pr bas ek hit milegi 
       'review-list': '10/day', #jaha bhi ye scope use hoga waha 10 hit milegi us url pr mtlb uss function pr
       'review-detail':'2/day', #jaha bhi ye review-detail wala scope use hoga us function ko bas 2 bar hi 
    #    hit kr skta h 
   },
#    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
#     'PAGE_SIZE': 5 #dekh pagination likhne se se ek data bht pages m divide hojata h like yaha pr setting m likhne se saare 
    # view pr lg jaayga ye pagination mtlb sab ke data divide honge aur ek page pr 5 hi data dikhegnge  
    # agar tujhe kisi particular view m bas lagana h ke iska data dive ho aur kisi ka data divide na ho 
    # custom pagination likh and usse alag se likh and usse uss view m mention krde jisme tu pagination lagana chahta h 
#DEKH AGAR TU CHAHTA H ke teri web api har koi access na krle to tu simple neeche wali line likh in rest framework to tujhe bas json data
# dikhega jb bhi tu web api dekhega mtlb jb tu url browser m daalega to tujhe api nhi dikhegi bas json data dikhega 
    'DEFAULT_RENDERER_CLASSES':('rest_framework.renderers.JSONRenderer',),

 } 
# token authentication use krne ke liye hame ek to rest framework m mention krna hota h and installed apps 
# m bhi mention krna hota h   
# dekh smjh agar setting m mention krega authentication yaa permission waala to wo poore 
# function pr lg jaayga and haa permission batata h tum kya likh skte ho update kr skte ho use kr skte 
# and authentication batata h ke aap login ho yaa nhi mtlb login hoge tbhi use kr skte h otherwise nhi

# dekh jb bhi tu refresh token se access token generate krega to sirf access token milega but tu chaahe
# to ye kr skta h ke jb bhi access token mile to refresh bhi new mile , tu bht kuchh aur kr skta h like 
# refresh tokem ka access token ka time bada skta h and all site pr jaa jwt ki and dekhle 
# SIMPLE_JWT ={
#     # 'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
#     # 'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
#     'ROTATE_REFRESH_TOKENS': True, #isse tujhe new refresh token milega new access token ke sth
#     # 'BLACKLIST_AFTER_ROTATION': True,
#     # 'ALGORITHM': 'HS256',
#}