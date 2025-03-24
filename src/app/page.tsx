'use client';

import { useState } from 'react';
import CompanyForm from './components/CompanyForm';

interface Template {
  name: string;
  description: string;
  url: string;
  features: string[];
}

interface TemplateResults {
  templates: Template[];
}

export default function Home() {
  const [templates, setTemplates] = useState<Template[]>([]);

  const handleFormSubmit = async (data: TemplateResults) => {
    setTemplates(data.templates);
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-900 to-black text-white">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl md:text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            Find Your Perfect Website Template
          </h1>
          <p className="text-xl text-white max-w-2xl mx-auto">
            Tell us about your company, and we&apos;ll find the best website templates that match your needs
          </p>
        </div>

        <div className="mb-16">
          <CompanyForm onSubmit={handleFormSubmit} />
        </div>

        {templates.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {templates.map((template, index) => (
              <div
                key={index}
                className="bg-white/10 backdrop-blur-sm rounded-lg p-6 shadow-lg hover:shadow-xl transition-shadow"
              >
                <h3 className="text-xl font-semibold mb-3 text-white">{template.name}</h3>
                <p className="text-white/90 mb-4">{template.description}</p>
                <div className="mb-4">
                  <h4 className="text-sm font-medium text-white mb-2">Features:</h4>
                  <ul className="list-disc list-inside text-white/90">
                    {template.features.map((feature, featureIndex) => (
                      <li key={featureIndex}>{feature}</li>
                    ))}
                  </ul>
                </div>
                <a
                  href={template.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
                >
                  View Template
                </a>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
