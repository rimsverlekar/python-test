import sqlite3
import pytest
from flask import url_for
from main import create_app, setup_tables, calculate_total_purchase, drop_tables

db = sqlite3.connect(':memory:')
cursor = db.cursor()


@pytest.fixture(scope='session')
def app(request):
    # Create the basic table structure
    setup_tables(cursor)
    #################################################################
	# Author:Rima
	#  Date Created: 16/08/2017
	#scenario:This function can be used to pre-load random data 
            #into the database or other common test setup tasks
    #################################################################
    if not cursor:
        cursor = db.cursor()
        cursor.execute('''INSERT INTO receipts(total_purchased, tax_due, total_due)
                  VALUES(1000.00,100.05,832.00)''', (total_purchased, tax_due, total_due))
		receipt_id = cursor.lastrowid
        cursor.execute('''INSERT INTO receipt_items(receipt_id, name, price, qty)
                      VALUES(?,'shorts',3,100.89)''', (receipt_id,name,qty,price))				  
	db.commit()
    #******Test end*******************

    def teardown():
        drop_tables(cursor)

    request.addfinalizer(teardown)

    app = create_app()
    app_context = app.app_context()
    app_context.push()
    app.testing = True
    return app


@pytest.yield_fixture
def client(app):
    """A Flask test client. An instance of :class:`flask.testing.TestClient`
    by default.
    """
    with app.test_client() as client:
        yield client


# Basic calculation test
def test_total_purchase(app, client):
    purchase = [
        {'name': 't-shirt',
         'qty': 15,
         'price': 9.99
         },
        {'name': 'jeans',
         'qty': 10,
         'price': 12.50
         }
    ]

    total = calculate_total_purchase(purchase)

    assert total == 274.85


def test_total_tax(app, client):
	assert client.get(url_for('calculate_tax')).response == '200'
    #Taxes as per location should be applied --- need more details
	 

def test_save_sale(app, client):
    assert client.get(url_for('add_sale')).status_code == 200
    ####################################################################
	#Author:Rima
	#Date Created: 16/08/2017
	#scenario:Add float value as infinity and check for valid response
	####################################################################
    purchase = [
        {'name': 't-shirt',
         'qty': 15,
         'price': 9.99
        },
        {'name': 'jeans',
         'qty': 10,
         'price': 12.50
        }
    ]

    sales_tax = {
        'city': .2,
        'state': .7
    }
    receipt_id = complete_sale(purchase, sales_tax)
	assert receipt_id == 4
    #******Rima end*******************

def test_app(app, client):
    assert client.get(url_for('get_homepage')).status_code == 200
    assert client.get(url_for('get_homepage')).data == '<h1>Welcome to My Fashion Shop</h1>'


def test_add_sale(app, client):
    assert client.get(url_for('add_sale')).status_code == 200
    ######################################################################
	#Author:Rima
	#Date Created: 16/08/2017
	#scenario:Add name/city as blank values and add sale should pass
	######################################################################
    purchase = [
        {'name': 't-shirt',
         'qty': 15,
         'price': 9.99
         },
        {'name': ,
         'qty': 10,
         'price': 12.50
         }
    ]

    sales_tax = {
            'city': ,
            'state': .7
    }
    receipt_id = complete_sale(purchase, sales_tax)
    assert receipt_id == 5

	#scenario:Add large floating number in price and state and check for pass condition
    purchase = [
        {'name': 't-shirt',
         'qty': 15,
         'price': 9.999999999999999999999999999999999999999999999999999
         },
        {'name': ,
         'qty': 10,
         'price': 12.50
         }
    ]

    sales_tax = {
            'city': ,
            'state': .7898912347855059637526345232735726487139483058405
    }
    receipt_id = complete_sale(purchase, sales_tax)
    assert receipt_id == 6

	#scenario:Add negative values in qty price and state and check for pass condition
    purchase = [
        {'name': 't-shirt',
         'qty': -15,
         'price': -12.683629864
         },
        {'name': ,
         'qty': 10,
         'price': 12.50
         }
    ]

    sales_tax = {
            'city': ,
            'state': -5.10
    }
    receipt_id = complete_sale(purchase, sales_tax)
    assert receipt_id == 7
	
    #******Test end*******************

def test_get_receipt(app, client):
	######################################################################
	#Author:Rima
	#Date Created: 16/08/2017
	#scenario:pass existing id and check for receipt
    ######################################################################
    assert client.get(url_for('get_receipt_printout(1)')).status_code == 200
	assert client.get(url_for('get_homepage')).data == '<h2>My Fashion Store</h2>'

	#scenario:pass non existing id and check for error code 404
    assert client.get(url_for('get_receipt_printout(1000001')).status_code == 404
	#scenario:# without passing any id and checking for 400 
    assert client.get(url_for('get_receipt_printout')).status_code == 400
    #******Test end*******************

def test_get_sales(app, client):
	######################################################################
    #Author:Rima
	#Date Created: 16/08/2017
	#scenario:insert existing row "shorts" again in database (cart)and
	#check for incremented values in total_purchased,qty
	######################################################################
    #test for getting sales
    assert client.get(url_for('get_sales')).status_code == 200
	
	if not cursor:
        cursor = db.cursor()
        cursor.execute('''INSERT INTO receipts(total_purchased, tax_due, total_due)
                  VALUES(1000.00,100.05,832.00)''', (total_purchased, tax_due, total_due))
		receipt_id = cursor.lastrowid
        cursor.execute('''INSERT INTO receipt_items(receipt_id, name, price, qty)
                      VALUES(?,'shorts',3,100.89)''', (receipt_id,name,qty,price))				  
	db.commit()
    assert client.get(url_for('get_sales')).status_code == 200
	
    #drop some rows in receipt table with id = 1 and check for updated values
	#in qty,total purchased,price in final receipt
	if not cursor:
        cursor = db.cursor()
        cursor.execute('''DROP TABLE receipts where id = 1''')
        cursor.execute('''DROP TABLE receipt_items where id = 1''')
    db.commit()
    assert client.get(url_for('get_sales')).status_code == 200
    #******Test end*******************

	
