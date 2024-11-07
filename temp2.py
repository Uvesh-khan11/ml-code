# paypal integration code check


import requests
from requests.auth import HTTPBasicAuth
import requests

# # Replace with your client ID and secret
# client_id = 'ASA9DDunHLvYUWqK2rlrU0rw55o9Q5KL1CDx6awUXGTIxuM4PlnsI341ZQzt6c7zyxz7sTIaZ4SF_b8J'
# secret = 'EBFj9-vwvDLHXvIcRt-dICHDDAYG0Z9r8WOu5iJ-5lbZKq3ItTj7BP472y-trOvahn-wX1twaKXVDh4O'

# auth_url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
# headers = {
#     'Accept': 'application/json',
#     'Accept-Language': 'en_US',
# }
# data = {
#     'grant_type': 'client_credentials'
# }

# response = requests.post(auth_url, headers=headers, data=data, auth=HTTPBasicAuth(client_id, secret))
# access_token = response.json().get('access_token')
# print("Access Token:", access_token)

token = 'A21AALFdJQCrggsU-oYLBDvlba5OjCfynWE0UNvfx7ajwxCN6e_BmWHhPA5SjOCA4obD8LHFBiaVlwq05YZxUA39W-3tXPcnw'

# import json


# # {'id': '5BK88685L49775816', 'status': 'CREATED', 'links': [{'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/5BK88685L49775816', 'rel': 'self', 'method': 'GET'}, {'href': 'https://www.sandbox.paypal.com/checkoutnow?token=5BK88685L49775816', 'rel': 'approve', 'method': 'GET'}, {'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/5BK88685L49775816', 'rel': 'update', 'method': 'PATCH'}, {'href': 'https://api.sandbox.paypal.com/v2/checkout/orders/5BK88685L49775816/capture', 'rel': 'capture', 'method': 'POST'}]}
# # https://www.sandbox.paypal.com/checkoutnow?token=5BK88685L49775816


# # Function to create a PayPal order
# def create_paypal_order(token):
#     # Step 1: Create PayPal Order
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {token}',
#     }

#     # Data for the order
#     data = {
#         "intent": "CAPTURE",
#         "purchase_units": [{
#             "reference_id": "YOUR_REFERENCE_ID",  # Unique ID for your order
#             "amount": {
#                 "currency_code": "USD",
#                 "value": "100.00"  # Amount to be charged
#             }
#         }],
#         "application_context": {
#             "return_url": "http://localhost:8000/return",  # URL to return to after approval
#             "cancel_url": "http://localhost:8000/cancel"   # URL to return to if canceled
#         }
#     }

#     # Make the request to create the order
#     response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, json=data)

#     # Check the response
#     if response.status_code == 201:
#         order_data = response.json()
#         print("Order created successfully:", order_data)

#         # Get the approval URL to redirect the user
#         approve_url = next(link['href'] for link in order_data['links'] if link['rel'] == 'approve')
#         print("Redirect the user to:", approve_url)

#         return approve_url, order_data['id']  # Return approval URL and order ID
#     else:
#         print("Error creating order:", response.status_code, response.json())
#         return None, None

# # Function to capture payment
# def capture_payment(order_id):
#     # Step 2: Capture Payment
#     capture_headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {token}"
#     }

#     # Capture the payment using the order ID
#     capture_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
#     capture_response = requests.post(capture_url, headers=capture_headers)

#     # Check if capture was successful
#     if capture_response.status_code == 201:
#         capture_data = capture_response.json()
#         print("Payment captured successfully:", capture_data)
#     else:
#         print("Error capturing payment:", capture_response.status_code, capture_response.json())

# # Example flow
# if __name__ == "__main__":
#     # Create order
#     approve_url, order_id = create_paypal_order(token)

#     if approve_url and order_id:
#         # Simulate user approval; in real application, redirect user to approve_url
#         print("User should approve payment at:", approve_url)

#         # Simulate the return from PayPal
#         # After user approves, they will be redirected back to your return URL
#         # You should call the capture_payment function here
#         # For example:
#         # capture_payment(order_id)

#         # Uncomment the next line to actually capture the payment
#         # capture_payment(order_id)