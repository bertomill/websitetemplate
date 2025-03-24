from http.server import BaseHTTPRequestHandler
import json
from typing import List, Optional
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

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

def search_templates_with_ai(company_info):
    """
    Use OpenAI with web search to find relevant website templates
    """
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError("OpenAI API key not found in environment variables")

    prompt = f"""
    Find modern website templates suitable for a {company_info['industry']} company.
    The company name is {company_info['name']}, and they target {company_info['target_audience']}.
    Company description: {company_info['description']}.
    Please search for actual, real website templates that would be perfect for this business.
    Focus on templates from reputable sources like ThemeForest, Template Monster, or similar platforms.
    Return specific template URLs and detailed descriptions.
    """

    try:
        response = client.responses.create(
            model="gpt-4o",
            tools=[{
                "type": "web_search_preview",
                "search_context_size": "medium"
            }],
            input=prompt
        )

        # Extract URLs and descriptions from the response
        message = next(item for item in response if item["type"] == "message")
        content = message["content"][0]
        text = content["text"]
        annotations = content.get("annotations", [])

        # Parse the response into our template format
        templates = []
        urls = {ann["url"]: ann["title"] for ann in annotations if ann["type"] == "url_citation"}
        
        # Extract template information from the AI response
        for url, title in urls.items():
            templates.append({
                "name": title,
                "description": "AI-recommended template for your business",
                "url": url,
                "features": ["Modern Design", "Mobile Responsive", "Easy Customization"]
            })

        if not templates:
            raise ValueError("No templates found in AI response")

        return {"templates": templates}
    except Exception as e:
        print(f"Error in AI search: {str(e)}")
        # Fallback to mock data if AI search fails
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
                
                # Get template suggestions using AI and web search
                result = search_templates_with_ai(company_info)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(result).encode('utf-8'))
            else:
                raise ValueError("Empty request body")
                
        except Exception as e:
            print(f"Error handling request: {str(e)}")  # Add server-side logging
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_message = {"error": str(e)}
            self.wfile.write(json.dumps(error_message).encode('utf-8')) 