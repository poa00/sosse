# Copyright 2022-2024 Laurent Defert
#
#  This file is part of SOSSE.
#
# SOSSE is free software: you can redistribute it and/or modify it under the terms of the GNU Affero
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# SOSSE is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with SOSSE.
# If not, see <https://www.gnu.org/licenses/>.

"""
Django settings for SOSSE project.

Generated by 'django-admin startproject' using Django 2.2.25.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from .conf import Conf

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'django_filters',
    'se.apps.SEConfig',
    'se.apps.SEAdminConfig',
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

ROOT_URLCONF = 'sosse.urls'

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

TEST_RUNNER = 'sosse.test_runner.SuiteRunner'

WSGI_APPLICATION = 'sosse.wsgi.application'

X_FRAME_OPTIONS = 'SAMEORIGIN'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

CONN_MAX_AGE = None

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PERMISSION_CLASSES': ['se.rest_permissions.LoginRequiredPermission'],
    'PAGE_SIZE': 100
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
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

SOSSE_LANGDETECT_TO_POSTGRES = {
    'ar': {
        'name': 'arabic',
        'flag': 'العربية'
    },
    'da': {
        'name': 'danish',
        'flag': '🇩🇰'
    },
    'nl': {
        'name': 'dutch',
        'flag': '🇳🇱'
    },
    'en': {
        'name': 'english',
        'flag': '🇬🇧'
    },
    'fi': {
        'name': 'finnish',
        'flag': '🇫🇮'
    },
    'fr': {
        'name': 'french',
        'flag': '🇫🇷'
    },
    'de': {
        'name': 'german',
        'flag': '🇩🇪'
    },
    'el': {
        'name': 'greek',
        'flag': '🇬🇷'
    },
    'hu': {
        'name': 'hungarian',
        'flag': '🇭🇺'
    },
    'id': {
        'name': 'indonesian',
        'flag': '🇮🇩'
    },
    'ga': {
        'name': 'irish',
        'flag': '🇮🇪'
    },
    'it': {
        'name': 'italian',
        'flag': '🇮🇹'
    },
    'ne': {
        'name': 'nepali',
        'flag': '🇳🇵'
    },
    'no': {
        'name': 'norwegian',
        'flag': '🇳🇴'
    },
    'pt': {
        'name': 'portuguese',
        'flag': '🇵🇹'
    },
    'ro': {
        'name': 'romanian',
        'flag': '🇷🇴'
    },
    'ru': {
        'name': 'russian',
        'flag': '🇷🇺'
    },
    'es': {
        'name': 'spanish',
        'flag': '🇪🇸'
    },
    'sv': {
        'name': 'swedish',
        'flag': '🇸🇪'
    },
    'ta': {
        'name': 'tamil',
        'flag': 'தமிழ்'
    },
    'tr': {
        'name': 'turkish',
        'flag': '🇹🇷'
    },

    # Not supported by Postgres, but support by langdetect
    'af': {
        'name': 'afrikaans',
    },
    'bg': {
        'name': 'bulgarian',
        'flag': '🇧🇬'
    },
    'bn': {
        'name': 'bengali',
        'flag': '🇧🇩'
    },
    'ca': {
        'name': 'catalan',
        'flag': '🏴󠁥󠁳󠁣󠁴󠁿'
    },
    'cs': {
        'name': 'czech',
        'flag': '🇨🇿'
    },
    'cy': {
        'name': 'welsh',
        'flag': '🏴󠁧󠁢󠁷󠁬󠁳󠁿'
    },
    'et': {
        'name': 'estonian',
        'flag': '🇪🇪'
    },
    'fa': {
        'name': 'persian',
        'flag': '🇮🇷'
    },
    'gu': {
        'name': 'gujarati',
        'flag': '🇮🇳'
    },
    'he': {
        'name': 'hebrew',
        'flag': '🇮🇱'
    },
    'hi': {
        'name': 'hindi',
        'flag': '🇮🇳'
    },
    'hr': {
        'name': 'croatian',
        'flag': '🇭🇷'
    },
    'ja': {
        'name': 'japanese',
        'flag': '🇯🇵'
    },
    'kn': {
        'name': 'kannada',
        'flag': '🇮🇳'
    },
    'ko': {
        'name': 'korean',
        'flag': '🇰🇷'
    },
    'lt': {
        'name': 'lithuanian',
        'flag': '🇱🇹'
    },
    'lv': {
        'name': 'latvian',
        'flag': '🇱🇻'
    },
    'mk': {
        'name': 'macedonian',
        'flag': '🇲🇰'
    },
    'ml': {
        'name': 'malayalam',
        'flag': '🇮🇳'
    },
    'mr': {
        'name': 'marathi',
        'flag': '🇮🇳'
    },
    'pa': {
        'name': 'punjabi',
        'flag': '🇵🇰'
    },
    'pl': {
        'name': 'polish',
        'flag': '🇵🇱'
    },
    'sk': {
        'name': 'slovak',
        'flag': '🇸🇰   '
    },
    'sl': {
        'name': 'slovenian',
        'flag': '🇸🇮'
    },
    'so': {
        'name': 'shona',
        'flag': '🇿🇼'
    },
    'sq': {
        'name': 'albanian',
        'flag': '🇦🇱'
    },
    'sw': {
        'name': 'swahili'
    },
    'te': {
        'name': 'telugu',
        'flag': '🇮🇳'
    },
    'th': {
        'name': 'thai',
        'flag': '🇹🇭'
    },
    'tl': {
        'name': 'tagalog',
        'flag': '🇵🇭'
    },
    'uk': {
        'name': 'ukrainian',
        'flag': '🇺🇦'
    },
    'ur': {
        'name': 'urdu'
    },
    'vi': {
        'name': 'vietnamese',
        'flag': '🇻🇳'
    },
    'zh-cn': {
        'name': 'chinese',
        'flag': '🇨🇳'
    },
    'zh-tw': {
        'name': 'chinese',
        'flag': '🇹🇼'
    }
}

globals().update(Conf.get())

SOSSE_VERSION_TAG = '0.dev5'
SOSSE_VERSION_COMMIT = ''

SPECTACULAR_SETTINGS = {
    'TITLE': 'Sosse',
    'DESCRIPTION': 'Selenium based Open Source Search Engine',
    'VERSION': SOSSE_VERSION_TAG,
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': '/static/swagger'
}
