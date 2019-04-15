import pytest
import pandas as pd
import sys

sys.path.append('..')

import src.leiden_permit_scraper as permit


### FIXTURES

@pytest.fixture
def address():
    return 'street23'


@pytest.fixture
def zip_code():
    return '1234AB'


@pytest.fixture
def address_zipcode(address, zip_code):
    return address + zip_code


@pytest.fixture
def permit_df(address_zipcode):
    return pd.DataFrame(data=[address_zipcode], columns=['LocatiePostcode'])


@pytest.fixture
def target_permit_df(address, zip_code):
    data = [(zip_code, zip_code[:4], address)]
    columns = ['postcode6', 'postcode4', 'adres']
    return pd.DataFrame(data=data, columns=columns)


### TESTS

def test_get_zip_code_nozip(address):
    assert permit.get_zip_code(address) == ''


def test_get_zip_code(address_zipcode, zip_code):
    assert zip_code == permit.get_zip_code(address_zipcode)


def test_get_address_nozip(address):
    assert permit.get_address(address) == address


def test_get_address(address_zipcode, address):
    assert permit.get_address(address_zipcode) == address


def test_parse_permits(permit_df, target_permit_df):
    assert target_permit_df.equals(permit.parse_permits(permit_df))
