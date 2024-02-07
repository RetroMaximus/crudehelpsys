# crudehelpsys/setup.py

from setuptools import setup, find_packages

setup(
    name='crudehelpsys',
    version='1.0.0',
    description='Simplifying command-line applications! '
                  'Developed by the cRUDEcREW, this script acts as a robust backbone, offering a '
                  'straightforward solution for command execution and help requests in your Python projects.'
                  'cRUDE Help Sys has a user-friendly approach that facilitates seamless command initiation through '
                  'a dynamic system that allows the import and execution of custom commands stored outside '
                  'the script,eliminating the need for constant modification. Ease of use is '
                  'highlighted by its interactive console input listener, This enables users to effortlessly navigate '
                  'and execute commands for simplicity and efficiency. cRUDE Help Sys simplifies command-line application '
                  'development, offering a hassle-free experience for developers and users alike.   '
                  'Welcome to a world where command-line operations become a breeze - welcome to cRUDE Help Sys! ',
    author='Reginald (Scr1ptAl1as) Finley',
    author_email='reggieretro@gmail.com',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here
	    # Core Python packages do not need to be included here.
    ],
    entry_points={
        'console_scripts': [
            'crudehelpsys = crudehelpsys.chs:main',
        ],
    },
)