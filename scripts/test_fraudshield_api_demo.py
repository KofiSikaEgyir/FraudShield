# =====================================================
# FraudShield API Demo Test Script
# Purpose: Test prediction, SMS simulation, history,
#          high-risk logs, and summary endpoints
# =====================================================

import json
import requests


BASE_URL = "http://127.0.0.1:8000"


def print_section(title: str):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def pretty_print_response(response):
    print(f"Status Code: {response.status_code}")

    try:
        data = response.json()
        print(json.dumps(data, indent=4))
    except Exception:
        print(response.text)


def test_health_endpoint():
    print_section("1. Testing Health Endpoint")

    response = requests.get(f"{BASE_URL}/health")
    pretty_print_response(response)


def test_high_risk_prediction():
    print_section("2. Testing High-Risk Fraud Prediction with SMS Simulation")

    payload = {
        "customer_phone": "0240000001",
        "type": "TRANSFER",
        "amount": 250000,
        "oldbalanceOrg": 250000,
        "newbalanceOrig": 0
    }

    response = requests.post(f"{BASE_URL}/predict/", json=payload)

    print("Request Payload:")
    print(json.dumps(payload, indent=4))

    print()
    print("API Response:")
    pretty_print_response(response)


def test_low_risk_prediction():
    print_section("3. Testing Low-Risk Prediction with No SMS Required")

    payload = {
        "customer_phone": "0240000002",
        "type": "PAYMENT",
        "amount": 100,
        "oldbalanceOrg": 5000,
        "newbalanceOrig": 4900
    }

    response = requests.post(f"{BASE_URL}/predict/", json=payload)

    print("Request Payload:")
    print(json.dumps(payload, indent=4))

    print()
    print("API Response:")
    pretty_print_response(response)


def test_prediction_history():
    print_section("4. Testing Prediction History Endpoint")

    response = requests.get(f"{BASE_URL}/predict/history?limit=5")
    pretty_print_response(response)


def test_high_risk_logs():
    print_section("5. Testing High-Risk Logs Endpoint")

    response = requests.get(f"{BASE_URL}/predict/high-risk?limit=5")
    pretty_print_response(response)


def test_prediction_summary():
    print_section("6. Testing Prediction Summary Endpoint")

    response = requests.get(f"{BASE_URL}/predict/summary")
    pretty_print_response(response)


def run_demo_tests():
    print_section("FraudShield API Demo Test Started")

    print(
        "Make sure the FastAPI server is already running at "
        "http://127.0.0.1:8000"
    )

    test_health_endpoint()
    test_high_risk_prediction()
    test_low_risk_prediction()
    test_prediction_history()
    test_high_risk_logs()
    test_prediction_summary()

    print_section("FraudShield API Demo Test Completed")


if __name__ == "__main__":
    run_demo_tests()