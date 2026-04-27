import requests
import pytest

BASE_URL = "http://127.0.0.1:5000"

def test_SEC_AUTH_001_sql_injection():
    """Verify: Input Validation"""
    payload = {'username': "admin' --", 'password': 'any'}
    response = requests.post(f"{BASE_URL}/login", data=payload)
    
    # Secure code uses '?' placeholders, so this injection will fail (401).
    assert response.status_code == 401, "CRITICAL: SQL Injection bypass detected!"

def test_SEC_LOG_002_error_leakage():
    """Verify : Secure by Default"""
    payload = {'username': "'", 'password': '123'}
    response = requests.post(f"{BASE_URL}/login", data=payload)
    
    forbidden_terms = ["sqlite3", "OperationalError", "SELECT * FROM"]
    for term in forbidden_terms:
        assert term not in response.text, f"POLICY VIOLATION: Technical leak found: {term}"

def test_SEC_PRIV_003_data_minimization():
    """Verify: Principle of Least Privilege"""
    # Note: Ensure 'admin' with 'password123' exists in your users.db for this to pass!
    payload = {'username': 'admin', 'password': 'password123'}
    response = requests.post(f"{BASE_URL}/login", data=payload)
    
    if response.status_code == 200:
        data = response.json()
        assert 'ssn' not in data, "COMPLIANCE FAILURE: SSN exposed in login response!"
    else:
        pytest.skip("Login failed; cannot verify data minimization. Check if user exists in DB.")