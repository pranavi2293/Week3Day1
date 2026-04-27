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

# def test_SEC_ERR_004_no_500_errors():
#     """Verify: Server should not return 500 for invalid input"""
    
#     # deliberately bad payloads
#     test_payloads = [
#         {},  # empty input
#         {'username': '', 'password': ''},  # empty values
#         {'username': None, 'password': None},  # null values
#         {'user': 'admin'},  # missing fields
#         "invalid_string_payload"  # wrong type
#     ]

#     for payload in test_payloads:
#         try:
#             response = requests.post(f"{BASE_URL}/login", data=payload)
#             assert response.status_code in [400, 401], \
#                 f"CRITICAL: Server returned {response.status_code} instead of 400/401"
#         except Exception as e:
#             assert False, f"CRITICAL: Server crashed with exception: {str(e)}"