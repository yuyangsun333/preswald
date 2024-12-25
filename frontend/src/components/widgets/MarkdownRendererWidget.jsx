import React from 'react';
import ReactMarkdown from 'react-markdown';

const MarkdownRendererWidget = ({ markdown, value, error }) => {
  const content = markdown || value || '';

  if (error) {
    return (
      <div className="text-red-600 p-4">
        Error: {error}
      </div>
    );
  }

  return (
    <div className="prose prose-sm max-w-none">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
};

export default MarkdownRendererWidget;
