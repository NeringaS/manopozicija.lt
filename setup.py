from setuptools import setup, find_packages

setup(
    name='manoseimas-pylab-lt',
    version='0.1a1',
    license='AGPLv3+',
    packages=find_packages(),
    install_requires=[
        'django',
        'django-nose',
        'django-compressor',
        'django-libsass',
        'django-debug-toolbar',
        'django-extensions',
        'django-webtest',
        'django-autoslug',
        'django-allauth',
        'factory_boy',
        'fake-factory',
        'unidecode',
        'markdown',
        'yattag',
        'psycopg2',
        'mock',
        'docutils',
        'exportrecipe',
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ],
)
