'use client';

import { useState, useRef } from 'react';
import { XMarkIcon, PlayIcon } from '@heroicons/react/24/outline';
import 'tailwindcss/tailwind.css';

const Queries = () => {
  const [query, setQuery] = useState('');
  const [queryResult, setQueryResult] = useState(null);
  const [activeQuery, setActiveQuery] = useState('My first shared query');
  const [resultHeight, setResultHeight] = useState(300); // Default height for resizable results

  const savedQueries = [
    // { name: 'My first shared query', content: "SELECT country_code, COUNT(*) FROM city GROUP BY 1 LIMIT 10;" },
    // { name: 'Sample Queries', content: 'SELECT * FROM sample_table;' },
    // { name: 'test', content: 'SELECT NOW();' },
  ];

  const executeQuery = () => {
    // Simulate query execution
    if (query.trim() === '') {
      setQueryResult({ error: 'Query cannot be empty' });
      return;
    }

    // Dummy data for query results
    setQueryResult({
      success: true,
      data: [
        { country_code: 'BLZ', count: 2 },
        { country_code: 'BGD', count: 24 },
        { country_code: 'ITA', count: 58 },
        { country_code: 'OMN', count: 5 },
      ],
    });
  };

  const handleResize = (e) => {
    const newHeight = Math.max(100, window.innerHeight - e.clientY);
    setResultHeight(newHeight);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-gray-200 overflow-y-auto">
        <div className="p-4 border-b">
          <h2 className="text-md">History</h2>
        </div>
        <ul className="space-y-2 p-4">
          {savedQueries.map((item) => (
            <li key={item.name}>
              <button
                onClick={() => {
                  setActiveQuery(item.name);
                  setQuery(item.content);
                }}
                className={`w-full text-left p-2 rounded-lg ${
                  activeQuery === item.name
                    ? 'bg-amber-100 text-amber-600'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                {item.name}
              </button>
            </li>
          ))}
        </ul>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="flex justify-between items-center h-14 px-6">
          <h1 className="text-md">{activeQuery}</h1>
          <button
            onClick={executeQuery}
            className="flex items-center px-2 py-2 bg-amber-600 text-sm text-white rounded-lg hover:bg-amber-700"
          >
            <PlayIcon className="w-5 h-5 mr-2" />
            Run Query
          </button>
        </div>

        {/* Query Editor */}
        <div className="flex-1 overflow-y-auto p-6">
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full h-full border border-gray-300 rounded-lg p-4 text-sm font-mono bg-gray-100 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
            placeholder="Write your SQL query here..."
          ></textarea>
        </div>

        {/* Resizable Divider */}
        <div
          className="h-2 bg-gray-300 cursor-row-resize"
          onMouseDown={(e) => {
            e.preventDefault();
            document.addEventListener('mousemove', handleResize);
            document.addEventListener('mouseup', () => {
              document.removeEventListener('mousemove', handleResize);
            });
          }}
        ></div>

        {/* Query Results */}
        <div
          className="bg-white p-6 border-t overflow-y-auto"
          style={{ height: `${resultHeight}px` }}
        >
          <h2 className="text-md font-semibold mb-4">Results</h2>
          {queryResult ? (
            queryResult.error ? (
              <p className="text-red-600">{queryResult.error}</p>
            ) : (
              <table className="w-full border-collapse border border-gray-300">
                <thead>
                  <tr className="bg-gray-100">
                    {Object.keys(queryResult.data[0]).map((key) => (
                      <th
                        key={key}
                        className="px-4 py-2 text-left text-sm font-medium text-gray-900 border border-gray-300"
                      >
                        {key}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {queryResult.data.map((row, index) => (
                    <tr
                      key={index}
                      className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}
                    >
                      {Object.values(row).map((value, i) => (
                        <td
                          key={i}
                          className="px-4 py-2 text-sm text-gray-900 border border-gray-300"
                        >
                          {value}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            )
          ) : (
            <p className="text-gray-500">Run a query to see results.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Queries;