# Website Template Finder

A Next.js application with Python runtime that helps users find the perfect website template based on their company information.

## Features

- Modern, responsive UI built with Next.js and Tailwind CSS
- Python backend using Vercel's serverless functions
- Intelligent template matching based on company information
- Real-time form validation and error handling
- Loading states and user feedback

## Tech Stack

- **Frontend**:
  - Next.js 14
  - TypeScript
  - Tailwind CSS
  - React

- **Backend**:
  - Python 3.12
  - FastAPI (via Vercel's Python runtime)
  - Pydantic for data validation
  - BeautifulSoup4 for web scraping

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.12
- Vercel CLI (optional, for local development)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bertomill/websitetemplate.git
   cd websitetemplate
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Set up Python environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Development

1. Start the Next.js development server:
   ```bash
   npm run dev
   ```

2. The application will be available at `http://localhost:3000`

### Deployment

This project is designed to be deployed on Vercel. The Python backend will automatically be deployed as serverless functions.

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Deploy!

## Project Structure

```
websitetemplate/
├── api/                    # Python backend API endpoints
│   └── search-templates.py # Main API endpoint
├── src/                    # Next.js frontend
│   └── app/               # App router components
│       └── components/    # Reusable components
├── requirements.txt       # Python dependencies
└── Pipfile               # Python version and dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
