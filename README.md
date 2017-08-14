# Softwear QA/Build Engineer Assessment

This is an assessment for the QA Build engineer position at Softwear, BV. Please clone this repository and install the dependencies to begin. Open the tests/test_application.py and add additional test cases. If you are not familiar with py.test review the documentation available at https://docs.pytest.org/en/latest/contents.html. If you are unsure how to write python test cases, then start the webserver and write Selenium test cases instead.

# Application Synopsis

This is a mock sales application built using Flask and Sqlite3. The endpoints provided return either HTML or JSON. There are a few endpoints exposed:

* /
* /get_sales
* /get-receipt/<id>
* /add-sale

When the server is running, open your browser and go to: http://127.0.0.1:5000/add-sale

# Requirements

* Python 3
* pip

# Installation

Use the following steps to setup the environment.

```
# Create a Python virtual environment called env
$ python3 -m venv env
# Activate the virtual environment (Windows: env/bin/activate.bat)
$ source env/bin/activate
# Use Python pip to install the requirements
$ pip install -r requirements.txt
````

# Running the tests

Use the following command to run the test cases. Additional test cases can be added to the file tests/test_application.py. Some examples are already in this file.

```
$ py.test tests/
```

# Starting the server

If you wish to write tests using Selenium, then start the server with this command. The application will be available at http://127.0.0.1:5000/

```
$ python main.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
