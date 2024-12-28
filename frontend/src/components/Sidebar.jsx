'use client';

import { Dialog } from '@headlessui/react';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { Link, useLocation } from 'react-router-dom';

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

export default function Sidebar({ sidebarOpen, setSidebarOpen, navigation }) {
  const location = useLocation();

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
              <img src="logo.png" alt="Your Company" className="h-14 w-auto" />
            </div>
            {/* Navigation */}
            <nav className="mt-6 flex-1 px-6">
              <ul className="space-y-1">
                {navigation.map((item) => (
                  <li key={item.name}>
                    <Link
                      to={item.href}
                      className={classNames(
                        location.pathname === item.href
                          ? 'bg-gray-50 text-blue-600'
                          : 'text-gray-700 hover:bg-gray-50 hover:text-blue-600',
                        'group flex items-center gap-x-3 rounded-md p-2 text-sm font-medium'
                      )}
                    >
                      <item.icon
                        className={classNames(
                          location.pathname === item.href
                            ? 'text-blue-600'
                            : 'text-gray-400 group-hover:text-blue-600',
                          'h-6 w-6'
                        )}
                        aria-hidden="true"
                      />
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </nav>
          </Dialog.Panel>
        </div>
      </Dialog>

      {/* Desktop Sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-80 lg:flex-col bg-[#FBFBFB] border-r border-gray-200">
        <div className="flex h-16 items-center px-6">
          <img src="logo.png" alt="Your Company" className="h-14 w-auto" />
        </div>
        <nav className="mt-6 flex-1 px-6">
          <ul className="space-y-1">
            {navigation.map((item) => (
              <li key={item.name}>
                <Link
                  to={item.href}
                  className={classNames(
                    location.pathname === item.href
                      ? 'bg-gray-100 text-black'
                      : 'text-gray-700 hover:bg-gray-100 hover:text-black',
                    'group flex items-center gap-x-3 rounded-md p-2 text-sm font-medium'
                  )}
                >
                  <item.icon
                    className={classNames(
                      location.pathname === item.href
                        ? 'text-amber-600'
                        : 'text-gray-400 group-hover:text-amber-600',
                      'h-6 w-6'
                    )}
                    aria-hidden="true"
                  />
                  {item.name}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </>
  );
}