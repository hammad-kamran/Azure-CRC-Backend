import pytest
from unittest.mock import patch, MagicMock
import azure.functions as func
import json
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file for testing
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from function_app import http_triggerham

@pytest.fixture
def mock_request():
    req = MagicMock(spec=func.HttpRequest)
    req.params = {}
    req.get_json.return_value = {}
    return req

@patch('function_app.container')
def test_http_triggerham_with_name(mock_container, mock_request, monkeypatch):
    # Load environment variables for testing
    monkeypatch.setenv("COSMOSDB_ENDPOINT", os.getenv("COSMOSDB_ENDPOINT"))
    monkeypatch.setenv("COSMOSDB_KEY", os.getenv("COSMOSDB_KEY"))
    
    response = http_triggerham(mock_request)
    
    assert response.status_code == 200
    data = json.loads(response.get_body())
    assert data['message'] == "Hello, Hammad. Your name has been added to the database."
    assert data['visitor_count'] == 1

@patch('function_app.container')
def test_http_triggerham_without_name(mock_container, mock_request):
    mock_container.read_item.return_value = {'count': 0}
    
    response = http_triggerham(mock_request)
    
    assert response.status_code == 200
    data = json.loads(response.get_body())
    assert data['message'] == "This HTTP triggered function executed successfully."
    assert data['visitor_count'] == 1
