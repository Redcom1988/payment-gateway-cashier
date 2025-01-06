import hashlib
import requests
import json

class DokuOVOPayment:
    def __init__(self):
        # These should be stored in environment variables in production
        self.CLIENT_ID = "BRN-0225-1736189694884"  # Your actual client ID
        self.SECRET_KEY = "SK-9sCrJ1kdYUJAYlsJKlqz"  # Your actual secret key
        self.BASE_URL = "https://api-sandbox.doku.com"
        self.INVOICE_NUMBER = "INV-20210115-0001"
        
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
        """Create OVO payment request"""
        endpoint = f"{self.BASE_URL}/ovo-emoney/v1/payment"
        
        # Generate checksum
        checksum = self.generate_checksum(amount, ovo_phone)
        
        # Prepare request payload
        payload = {
            "client": {
                "id": self.CLIENT_ID
            },
            "order": {
                "invoice_number": self.INVOICE_NUMBER,
                "amount": int(amount)
            },
            "ovo_info": {
                "ovo_id": ovo_phone
            },
            "security": {
                "check_sum": checksum
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Client-Id": self.CLIENT_ID  
        }
        
        try:
            response = requests.post(endpoint, json=payload, headers=headers, timeout=70)
            response_data = response.json()
            
            # Add error handling for merchant not found
            if 'error' in response_data:
                raise Exception(response_data['error']['message'])
                
            return response_data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Payment gateway error: {str(e)}")