from http.server import BaseHTTPRequestHandler
import json
from typing import List, Optional
import os

# Define our data models
class CompanyInfo(BaseModel):
    name: str
    industry: str
    description: Optional[str] = None
    target_audience: Optional[str] = None

class Template(BaseModel):
    name: str
    description: str
    url: str
    features: List[str]

def get_templates_for_company(company_info):
    """
    This function would normally search for templates based on the company info.
    For now, we'll return mock data.
    """
    return {
        "templates": [
            {
                "name": "Modern Business Template",
                "description": f"Perfect for {company_info['industry']} companies targeting {company_info['target_audience']}",
                "url": "https://example.com/template1",
                "features": ["Responsive Design", "Contact Form", "About Section", "Product Showcase"]
            },
            {
                "name": "Professional Portfolio",
                "description": "Showcase your products and services with this elegant design",
                "url": "https://example.com/template2",
                "features": ["Gallery", "Testimonials", "Services Section", "Team Profiles"]
            },
            {
                "name": "E-commerce Ready",
                "description": "Start selling online with this complete e-commerce solution",
                "url": "https://example.com/template3",
                "features": ["Shopping Cart", "Product Catalog", "Secure Checkout", "Inventory Management"]
            }
        ]
    }

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                company_info = json.loads(post_data.decode('utf-8'))
                
                # Get template suggestions
                result = get_templates_for_company(company_info)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(result).encode('utf-8'))
            else:
                raise ValueError("Empty request body")
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_message = {"error": str(e)}
            self.wfile.write(json.dumps(error_message).encode('utf-8')) 