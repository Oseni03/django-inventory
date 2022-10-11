from setuptools import setup, find_packages
import shop

with open('README.md', 'r') as fh:
    long_description = fh.read()

REQUIREMENTS = [
    'Django>=4.0',
    'django-htmx>=1.12',
    'mptt',
]

DIR = ["src"]

CLASSIFIERS = [
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Framework :: Django',
    'Framework :: Django :: 4.0',
    'Framework :: Django :: 4.1',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]

setup(
    author="Oseni Ayomide Daniel",
    author_email="oseniayomide57@gmail.com",
    maintainer="Oseni Ayomide Daniel",
    maintainer_email="oseniayomide57@gmail.com",
    name="django-ecomstore-inventory",
    version=src.inventory.__version__,
    description="An ecommerce inventory Django app.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Oseni03/django-inventory',
    license='MIT License',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=['tests', 'docs']),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    package_data={"inventory": ["templates/inventory", "static/inventory"]},
    package_dir=DIR,
    where="src",
)
