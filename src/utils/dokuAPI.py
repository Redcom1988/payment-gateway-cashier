from datetime import datetime
import hashlib
import requests
import json

class DokuOVOPayment:
    def __init__(self):
        # These should be stored in environment variables in production
        self.CLIENT_ID = "BRN-0225-1736189694884"  # Your actual client ID
        self.SECRET_KEY = "SK-ZyDaNSqcYkWnUZoFpI1y"  # Your actual secret key
        self.BASE_URL = "https://api-sandbox.doku.com"
        self.INVOICE_NUMBER = "INV-20210115-0002"
        
    def generate_checksum(self, amount, ovo_id):
        """
        Generate checksum for Doku OVO payment
        Format: sha256(order.amount + client.id + order.invoice_number + ovo_info.ovo_id + secret_key)
        """
        # Ensure amount is formatted without decimals
        amount_str = str(int(amount))
        
        # Concatenate values in the correct order
        raw = f"{amount_str}{self.CLIENT_ID}{self.INVOICE_NUMBER}{ovo_id}{self.SECRET_KEY}"
        print(f"Raw checksum string: {raw}")  # Debug print
        
        # Generate SHA-256 hash
        checksum = hashlib.sha256(raw.encode('utf-8')).hexdigest()
        print(f"Generated checksum: {checksum}")  # Debug print
        return checksum
    
    def create_payment(self, amount, ovo_phone):
        try:
            # Get current UTC timestamp
            current_time = datetime.utcnow()
            request_timestamp = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            request_id = f"REQ-{current_time.strftime('%Y%m%d%H%M%S')}"
            
            # Generate checksum
            amount_str = str(int(amount))
            raw = f"{amount_str}{self.CLIENT_ID}{self.INVOICE_NUMBER}{ovo_phone}{self.SECRET_KEY}"
            checksum = hashlib.sha256(raw.encode()).hexdigest()
            
            print("\nRequest Components:")
            print(f"Amount: {amount_str}")
            print(f"Client ID: {self.CLIENT_ID}")
            print(f"Invoice: {self.INVOICE_NUMBER}")
            print(f"Phone: {ovo_phone}")
            print(f"Timestamp: {request_timestamp}")
            print(f"Request ID: {request_id}")
            print(f"Checksum: {checksum}")
            
            # Prepare headers with all possible required fields
            headers = {
                "Content-Type": "application/json",
                "Client-Id": self.CLIENT_ID,
                "Request-Id": request_id,
                "Request-Timestamp": request_timestamp,
                "Request-Target": "/ovo-emoney/v1/payment"
            }
            
            # Prepare payload with consistent formatting
            payload = {
                "client": {
                    "id": self.CLIENT_ID
                },
                "order": {
                    "invoice_number": self.INVOICE_NUMBER,
                    "amount": int(amount)
                },
                "ovo_info": {
                    "ovo_id": str(ovo_phone)
                },
                "security": {
                    "check_sum": checksum
                }
            }
            
            endpoint = f"{self.BASE_URL}/ovo-emoney/v1/payment"
            
            print("\nRequest Details:")
            print(f"Endpoint: {endpoint}")
            print(f"Headers: {json.dumps(headers, indent=2)}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(endpoint, json=payload, headers=headers)
            
            print(f"\nResponse Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Body: {response.text}")
            
            if response.status_code != 200:
                response_data = response.json()
                if 'error' in response_data:
                    print("\nError Details:")
                    print(f"Message: {response_data['error']['message']}")
                    print(f"Our Checksum: {checksum}")
                    if 'security' in response_data:
                        print(f"Their Checksum: {response_data['security']['check_sum']}")
                    print(f"Match?: {checksum == response_data['security']['check_sum']}")
                raise Exception(f"API returned status code {response.status_code}: {response.text}")
                
            return response.json()
            
        except Exception as e:
            raise Exception(f"Payment gateway error: {str(e)}")