try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='BirdsWatcher',
    version='1.0',
    packages=['vag'],
    url='https://birdswatcher-vag.rhcloud.com/',
    license='',
    author='Luiza Utsch',
    author_email='',
    description='',
    install_requires=
    [
        'Flask>=0.12',
        'Flask-OAuthlib>=0.9.3',
    ]
)
