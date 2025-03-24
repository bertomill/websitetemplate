from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from typing import List, Optional

# Create a FastAPI app
app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing) to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the data model for company information
class CompanyInfo(BaseModel):
    name: str
    industry: str
    description: Optional[str] = None
    target_audience: Optional[str] = None

# Define the response model for templates
class Template(BaseModel):
    name: str
    description: str
    url: str
    features: List[str]

@app.post("/api/search-templates")
async def search_templates(company_info: CompanyInfo):
    try:
        # This is a simplified example. In a real application, you would:
        # 1. Use more sophisticated web scraping
        # 2. Implement proper error handling
        # 3. Add rate limiting
        # 4. Use proper API keys and authentication
        
        # For demonstration, we'll return some mock data
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
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 