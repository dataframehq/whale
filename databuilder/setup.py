import setuptools
from setuptools import find_packages

setuptools.setup(
    name='whalebuilder',
    version='1.0.0b0',
    author='Robert Yi',
    author_email='robert@ryi.me',
    description="A pared-down metadata scraper + SQL runner.",
    url='https://github.com/dataframehq/whale',
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=[
        'amundsen-databuilder>=2.0.0',
        'pyhocon>=0.3.42',
        'tabulate',
        'pyaml',
        'google-api-python-client',
        'SQLAlchemy>=1.3.19'
    ],
    include_package_data=True,
)
