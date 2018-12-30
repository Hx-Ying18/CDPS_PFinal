from setuptools import setup

setup(
    name='CDPS-QUIZ',
    version='1.0',
    py_modules=['hello'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [ console_scripts]
        deploy=deploy:cli
    '''
)