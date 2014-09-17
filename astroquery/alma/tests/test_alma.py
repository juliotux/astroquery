# Licensed under a 3-clause BSD style license - see LICENSE.rst
import os
from astropy.tests.helper import pytest

from .. import Alma
from ...utils.testing_tools import MockResponse

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def data_path(filename):
    return os.path.join(DATA_DIR, filename)

DATA_FILES = {'GET': {'http://almascience.org/aq/search.votable':
                      'sgra_query.xml',
                     },
              'POST': {}
              }

def alma_request(request_type, url, **kwargs):
    with open(data_path(DATA_FILES[request_type][url]), 'rb') as f:
        response = MockResponse(content=f.read(), url=url)
    return response

def _get_dataarchive_url(*args):
    return 'http://almascience.eso.org'

def test_SgrAstar(monkeypatch):
    # Local caching prevents a remote query here

    monkeypatch.setattr(Alma, '_get_dataarchive_url', _get_dataarchive_url)
    alma = Alma()

    # monkeypatch instructions from https://pytest.org/latest/monkeypatch.html
    monkeypatch.setattr(alma, '_request', alma_request)
    # set up local cache path to prevent remote query
    alma.cache_location = DATA_DIR

    # the failure should occur here
    result = alma.query_object('Sgr A*')

    # test that max_results = 50
    assert len(result) == 82
    assert b'2011.0.00217.S' in result['Project_code']
