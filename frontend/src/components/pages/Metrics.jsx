'use client';

import { Dialog } from '@headlessui/react';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

const Metrics = () => {
  const dummyMetricsData = [
    // Uncomment these to test the populated state
    // {
    //   name: 'Total Sales',
    //   entities: ['Orders', 'Products'],
    //   query: 'SELECT SUM(sales) FROM orders',
    // },
    // {
    //   name: 'Active Users',
    //   entities: ['Users'],
    //   query: "SELECT COUNT(*) FROM users WHERE status = 'active'",
    // },
    // {
    //   name: 'Average Order Value',
    //   entities: ['Orders', 'Products'],
    //   query: 'SELECT AVG(order_value) FROM orders',
    // },
  ];

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedMetric, setSelectedMetric] = useState(null);

  const isMetricsEmpty = !dummyMetricsData || dummyMetricsData.length === 0;

  return (
    <>
      {/* Mobile Sidebar */}
      <Dialog open={sidebarOpen} onClose={() => setSidebarOpen(false)} className="relative z-50 lg:hidden">
        <div className="fixed inset-0 bg-gray-900/80" />
        <div className="fixed inset-0 flex">
          <Dialog.Panel className="relative flex w-full max-w-sm flex-col bg-[#FBFBFB]">
            {/* Close Button */}
            <div className="absolute top-0 right-0 flex w-16 justify-center pt-5">
              <button
                type="button"
                onClick={() => setSidebarOpen(false)}
                className="-m-2.5 p-2.5"
              >
                <span className="sr-only">Close sidebar</span>
                <XMarkIcon className="h-6 w-6 text-white" aria-hidden="true" />
              </button>
            </div>
            {/* Logo */}
            <div className="flex h-16 items-center px-6">
              <h1 className="text-lg font-bold">Metrics</h1>
            </div>
            {/* Navigation */}
            <nav className="mt-6 flex-1 px-6">
              {isMetricsEmpty ? (
                <p className="text-gray-500">No metrics available</p>
              ) : (
                <ul className="space-y-1">
                  {dummyMetricsData.map((metric) => (
                    <li key={metric.name}>
                      <button
                        onClick={() => {
                          setSelectedMetric(metric);
                          setSidebarOpen(false);
                        }}
                        className={classNames(
                          selectedMetric?.name === metric.name
                            ? 'bg-gray-100 text-black'
                            : 'text-gray-700 hover:bg-gray-100 hover:text-black',
                          'group flex w-full items-center rounded-md p-2 text-sm font-medium'
                        )}
                      >
                        {metric.name}
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </nav>
          </Dialog.Panel>
        </div>
      </Dialog>

      {/* Desktop Sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-80 lg:flex-col bg-white border-r border-gray-200">
        <div className="flex h-16 items-center px-6">
          <h1 className="text-lg font-bold">Metrics</h1>
        </div>
        <nav className="mt-6 flex-1 px-6">
          {isMetricsEmpty ? (
            <p className="text-gray-500">No metrics available</p>
          ) : (
            <ul className="space-y-1">
              {dummyMetricsData.map((metric) => (
                <li key={metric.name}>
                  <button
                    onClick={() => setSelectedMetric(metric)}
                    className={classNames(
                      selectedMetric?.name === metric.name
                        ? 'bg-gray-100 text-black'
                        : 'text-gray-700 hover:bg-gray-100 hover:text-black',
                      'group flex w-full items-center rounded-md p-2 text-sm font-medium'
                    )}
                  >
                    {metric.name}
                  </button>
                </li>
              ))}
            </ul>
          )}
        </nav>
      </div>

      {/* Main Content */}
      <div className="lg:pl-80">
        <div className="flex h-16 items-center bg-white px-4 shadow lg:hidden">
          <button
            type="button"
            onClick={() => setSidebarOpen(true)}
            className="text-gray-700"
          >
            <span className="sr-only">Open sidebar</span>
            <XMarkIcon className="h-6 w-6" aria-hidden="true" />
          </button>
          <h1 className="ml-4 text-lg font-bold">Metrics</h1>
        </div>
        <main className="p-6">
          {isMetricsEmpty ? (
            <p className="text-gray-500">No metrics available</p>
          ) : selectedMetric ? (
            <div>
              <h2 className="text-2xl font-bold mb-4">{selectedMetric.name}</h2>
              <p className="mb-2">
                <span className="font-semibold">Dependent Entities:</span>{' '}
                {selectedMetric.entities.join(', ')}
              </p>
              <p className="font-semibold mb-2">Query:</p>
              <pre className="bg-gray-100 p-4 rounded-md overflow-auto">
                {selectedMetric.query}
              </pre>
            </div>
          ) : (
            <p className="text-gray-500">
              Select a metric from the sidebar to view details.
            </p>
          )}
        </main>
      </div>
    </>
  );
};

export default Metrics;