# Unit tests

In order to run test.py, you must have an account on the scihub.copernicus website (https://scihub.copernicus.eu/dhus/#/home). You will find the registration steps at https://scihub.copernicus.eu/userguide/SelfRegistration.

When it is done, you can type the following command, replacing YourUsername and YourPassword:

pytest test.py -v --username YourUsername --password YourPassword

Make sure the folder in which you are running test.py also contains the conftest.py file.
