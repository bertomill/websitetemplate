from flask import Flask, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

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

@app.route('/api/search-templates', methods=['POST', 'OPTIONS'])
def search_templates():
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    try:
        company_info = request.json
        if not company_info:
            raise ValueError("Empty request body")

        result = search_templates_with_ai(company_info)
        
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        error_response = jsonify({'error': str(e)})
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        error_response.status_code = 500
        return error_response 