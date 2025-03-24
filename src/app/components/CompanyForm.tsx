'use client';

import { useState } from 'react';

interface FormData {
  name: string;
  industry: string;
  description: string;
  target_audience: string;
}

interface TemplateResults {
  templates: Array<{
    name: string;
    description: string;
    url: string;
    features: string[];
  }>;
}

interface CompanyFormProps {
  onSubmit: (data: TemplateResults) => void;
}

export default function CompanyForm({ onSubmit }: CompanyFormProps) {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    industry: '',
    description: '',
    target_audience: '',
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/search-templates', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch templates');
      }

      const data = await response.json();
      onSubmit(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto p-6 bg-white/10 backdrop-blur-sm rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-white">Tell us about your company</h2>
      
      {error && (
        <div className="mb-4 p-4 bg-red-500/20 text-red-200 rounded-md border border-red-500/30">
          {error}
        </div>
      )}
      
      <div className="space-y-4">
        <div>
          <label htmlFor="name" className="block text-sm font-medium text-white mb-1">
            Company Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md bg-white/5 border-white/10 text-white placeholder-white/50 focus:border-blue-500 focus:ring-blue-500"
            disabled={isLoading}
            placeholder="Enter your company name"
          />
        </div>

        <div>
          <label htmlFor="industry" className="block text-sm font-medium text-white mb-1">
            Industry
          </label>
          <input
            type="text"
            id="industry"
            name="industry"
            value={formData.industry}
            onChange={handleChange}
            required
            className="mt-1 block w-full rounded-md bg-white/5 border-white/10 text-white placeholder-white/50 focus:border-blue-500 focus:ring-blue-500"
            disabled={isLoading}
            placeholder="e.g. Technology, Healthcare, Education"
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-white mb-1">
            Company Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={4}
            className="mt-1 block w-full rounded-md bg-white/5 border-white/10 text-white placeholder-white/50 focus:border-blue-500 focus:ring-blue-500"
            disabled={isLoading}
            placeholder="Describe what your company does"
          />
        </div>

        <div>
          <label htmlFor="target_audience" className="block text-sm font-medium text-white mb-1">
            Target Audience
          </label>
          <input
            type="text"
            id="target_audience"
            name="target_audience"
            value={formData.target_audience}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md bg-white/5 border-white/10 text-white placeholder-white/50 focus:border-blue-500 focus:ring-blue-500"
            disabled={isLoading}
            placeholder="Who are your customers?"
          />
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className={`w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors ${
            isLoading ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {isLoading ? 'Finding Templates...' : 'Find Templates'}
        </button>
      </div>
    </form>
  );
} 