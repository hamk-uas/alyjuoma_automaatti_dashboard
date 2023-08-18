from setuptools import find_packages, setup

setup(
    name='alyjuoma_automaatti_dashboard',
    version='v0.2.2-alpha',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'mysql-connector-python==8.0.20',
        'freezegun',
        'flask-cors',
    ],
)