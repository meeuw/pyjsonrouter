from setuptools import setup

def read(filename):
    with open(filename) as f:
        return f.read()

setup(
    name = "pyjsonrouter",
    version = "0.1",
    author = "Dick Marinus",
    author_email = "dick@mrns.nl",
    description = ("Minimal wsgi router from JSON configuration file"),
    license = "GPL-3",
    keyworkds = "wsgi framework router json",
    url = "http://packages.python.org/pyjsonrouter",
    packages = ["pyjsonrouter"],
    long_description=read('README'),
    classifiers=[
        "Environment :: Web Environment",
    ]
)
