from setuptools import setup
setup(
    name = 'task-tracker',
    version = '0.1',
    packages = ['src'],
    entry_points = {
        'console_scripts': [
            'task-tracker = src.__main__:main'
        ]
    }
)