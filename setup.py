from setuptools import find_packages, setup

setup(
    name='alyjuoma_automaatti_dashboard',
    version='v0.1.1-alpha',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'mysql-connector-python',
        'freezegun'
    ],
)