from http.server import BaseHTTPRequestHandler
import json
from typing import List, Optional
from pydantic import BaseModel

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

def search_templates(company_info: CompanyInfo):
    # This is a simplified example. In a real application, you would:
    # 1. Use more sophisticated web scraping
    # 2. Implement proper error handling
    # 3. Add rate limiting
    # 4. Use proper API keys and authentication
    
    templates = [
        Template(
            name="Modern Business Template",
            description="A clean, professional template perfect for business websites",
            url="https://example.com/template1",
            features=["Responsive Design", "Contact Form", "About Section"]
        ),
        Template(
            name="E-commerce Starter",
            description="Complete e-commerce solution with product management",
            url="https://example.com/template2",
            features=["Product Catalog", "Shopping Cart", "Payment Integration"]
        ),
        Template(
            name="Portfolio Showcase",
            description="Showcase your work with this elegant portfolio template",
            url="https://example.com/template3",
            features=["Project Gallery", "Client Testimonials", "Blog Section"]
        )
    ]
    
    return {"templates": templates}

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            # Parse the request data into our CompanyInfo model
            company_info = CompanyInfo(**request_data)
            
            # Get templates
            result = search_templates(company_info)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            
        except Exception as e:
            # Handle errors
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
    
    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers() 