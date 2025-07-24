import anthropic
import base64
import io
import re
import requests
import pandas as pd
import json
import os
from datetime import datetime
from PIL import Image
from expense_tracker import logger
from dotenv import load_dotenv
from urllib.parse import urljoin

class ReceiptProcessor:

    def __init__(self, api_key, config = None):

        #load env
        load_dotenv()
        self.LLM_API_KEY = os.getenv('CLAUDE_API_KEY')
        self.CURR_API_KEY = os.getenv('CURR_API_KEY')

        #initialize logger
        self.logger = logger

        #initialize claude
        self.client = anthropic.Anthropic(api_key)

        #configure image processing parameters
        self.config = config or {}
        
        self.max_image_size = self.config.get('max_image_size', (1024, 1024))
        self.jpg_quality = self.config.get('jpg_quality', 85)

        self.target_token_range = self.config.get('target_token_range', (30000,60000))
        self.max_token_limit = self.config.get('max_token_limit', 180000)
        
        self.supported_input_formats = self.config.get('supported_input_formats', ['.jpg', '.jpeg', '.png'])
        self.output_format ='JPEG'
        
        self.logger.info(f"ReceiptProcessor initialized with max_size={self.max_image_size}, quality={self.jpg_quality}")

    def encode_image_for_claude(self, image_path, max_size= (1024, 1024), quality = 85):
        """ Resize and encode image for Claude API to stay under token limits"""

        #Open and resize image

        with Image.open(image_path) as img:
            #convert to rgb if needed
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            #Resize and maintain aspect ratio
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

            #Save to bytes with compression
            img_byte_arr = io.BytesIO()

            save_kwargs = {"format": self.output_format, "optimize": True}

            if self.output_format.upper() == "JPEG":      
                save_kwargs["quality"] = self.jpg_quality #only add for JPEG

            img.save(img_byte_arr, **save_kwargs)
            img_byte_arr = img_byte_arr.getvalue()

            #Encode to base64
            encoded = base64.b64encode(img_byte_arr).decode('utf-8')

            estimated_tokens = len(encoded) / 3
            self.logger.info(f"image {image_path} encoded is {estimated_tokens:,.0f} tokens")

            return encoded

    def process_receipt(self, image_path):
        
        prompt = """Please analyze this receipt image and extract the following information. Return your response as valid JSON only, with no additional text.

        Required JSON structure:
        {
        "merchant_name": "string or NA if not visible",
        "amount": "number or "NA" if not visible",
        "currency: "Currency of amount or "NA" is not visible",
        "date": "ddmmyy format or NA if not visible", 
        "payment_method": "Cash or Visa or Mastercard or Paynow/Paylah or NA if not clear",
        "card_type": "last 4 digits or NA if not visible/applicable"
        }

        Additional rules:
        - Only include "currency" field in the amount if the currency is NOT SGD
        - Extract only the total amount, ignore subtotals or tax breakdowns
        - If payment method is Cash, card_type should be NA
        - If payment method is Visa or Mastercard but card digits not visible, card_type should be NA
        - Use exact format ddmmyy for dates (e.g., 150324)
        - Return numbers for amount field, not strings with currency symbols"""

        #encode and compress image for API

        try:
            encoded_image = self.encode_image_for_claude(image_path, self.max_image_size, self.jpg_quality)

            #call claude
            response = self.client.messages.create(
                model= "claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content":[
                        {
                        "type": "text", 
                        "text": prompt
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": encoded_image
                        }
                    }
                ]
            }]
        )
            response_text = response.content[0].text
            return response_text
        except Exception as e:
            self.logger.error(f"Failed to process receipt. Issue is: {e}")
            return None

    def extract_receipt_data(self, json_response):
        """Validate and clean extracted receipt data"""

        validated_data = {}

        #required_fields =['merchant_name','amount','date','payment_method','card_type']
        response_data = json.loads(json_response)

        #standardize merchant name
        validated_data['merchant_name'] = self.clean_merchant_name(response_data['merchant_name'])
        validated_data['amount'] = self.validate_amount(response_data['amount'], response_data['currency'])
        validated_data['date'] = self. validate_date_format(response_data['date'])
        validated_data['payment_method'] = response_data['payment_method']
        
        if response_data['payment_method'].lower() != 'cash':
            validated_data['card_type'] = self.validate_card_digits(response_data['card_type'])
        else:
            validated_data['card_type'] = 'NA' #cash payment
        
        return validated_data

    def validate_date_format(self, date_str):
        """Validate and standardize date format"""

        corrected_date = ''

        if date_str == 'NA':
            return 'NA'
        
        try:
            corrected_date = datetime.strptime(date_str, '%d%m%y')
            return corrected_date.strftime('%d%m%y')
        except ValueError:
            self.logger.error(f"Error formatting date {date_str}")
            return 'NA'
    
    def validate_card_digits(self, card_type):
        """Extract the last 4 digits and classify the card as DBS-V, DBS-E or Trust"""
        if card_type == 'NA':
            return 'NA'
        
        match = re.search(r'(\d{4})\b', card_type)

        if match:
            card_num = match.group(1)
        elif len(card_type) == 4 and card_type.isdigit():
            card_num = card_type
        else:
            return 'NA'
        
        if card_num == '2920':
            return "DBS-V"
        elif card_num == '5393':
            return "DBS-E"
        elif card_num =='6595':
            return "Trust"
        else:
            return "NA"

    def clean_merchant_name(self, merchant_name):
        if merchant_name == "NA":
            return 'NA'
        clean_merch_name=str(merchant_name).strip()
        clean_merch_name = re.sub(r'\s+',' ', clean_merch_name)

        return clean_merch_name 

    def validate_amount(self, amount, currency):
        
        #check if NA
        if amount == 'NA':
            return 'NA'
        
        #check if currency other than SGD. if yes, convert
        if currency == "SGD" and amount.isdigit():
            valid_amount = amount.strip()
        else:
            valid_amount = self.convert_currency(amount.strip(), currency)
        
        return valid_amount

    def convert_currency(self, amount, from_currency):
        """Convert amount from foreign currency to SGD. Assume that amount and from_currency is validated before function is called"""
        try:
            api_url =' https://v6.exchangerate-api.com/v6/'       
            path = f"{self.CURR_API_KEY}/pair/{from_currency}/SGD/{amount}" 
            full_url = urljoin(api_url, path)

            #call url
            response = requests.get(full_url, timeout=10)
            response.raise_for_status() #Check HTTP errors
            data = response.json()

            if data.get('result') == 'success':
                #process data here
                converted_amount = data['conversion_result']
            else:
                self.logger.error(f"currency API error: {data.get('error-type')}")
                converted_amount = 'NA'
        
        except Exception as e:
            self.logger.error(f"Currency conversion failed {e}")
            converted_amount = 'NA'
        
        return converted_amount
    
    

