'use client';

import { Dialog, DialogBackdrop, DialogPanel, TransitionChild } from '@headlessui/react';
import { XMarkIcon, Cog6ToothIcon } from '@heroicons/react/24/outline';

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

export default function Sidebar({ sidebarOpen, setSidebarOpen, navigation }) {
  return (
    <>
      {/* Mobile Sidebar */}
      <Dialog open={sidebarOpen} onClose={() => setSidebarOpen(false)} className="relative z-50 lg:hidden">
        <DialogBackdrop className="fixed inset-0 bg-gray-900/80 transition-opacity duration-300 ease-linear" />
        <div className="fixed inset-0 flex">
          <DialogPanel className="relative mr-16 flex w-full max-w-xs flex-1 transform transition duration-300 ease-in-out">
            <TransitionChild>
              <div className="absolute left-full top-0 flex w-16 justify-center pt-5">
                <button type="button" onClick={() => setSidebarOpen(false)} className="-m-2.5 p-2.5">
                  <span className="sr-only">Close sidebar</span>
                  <XMarkIcon aria-hidden="true" className="size-6 text-white" />
                </button>
              </div>
            </TransitionChild>
            <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-white px-6 pb-4">
              <div className="flex h-16 shrink-0 items-center">
                <img
                  src="logo.png"
                  alt="Your Company"
                  className="h-14 w-auto"
                />
              </div>
              <nav className="flex flex-1 flex-col">
                <ul className="flex flex-1 flex-col gap-y-7">
                  {/* Navigation Items */}
                  <li>
                    <ul className="-mx-2 space-y-1">
                      {navigation.map((item) => (
                        <li key={item.name}>
                          <a
                            href={item.href}
                            className={classNames(
                              item.current
                                ? 'bg-gray-50 text-blue-600'
                                : 'text-gray-700 hover:bg-gray-50 hover:text-blue-600',
                              'group flex gap-x-3 rounded-md p-2 text-sm/6 font-medium'
                            )}
                          >
                            <item.icon
                              aria-hidden="true"
                              className={classNames(
                                item.current ? 'text-blue-600' : 'text-gray-400 group-hover:text-blue-600',
                                'size-6 shrink-0'
                              )}
                            />
                            {item.name}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </li>
                  {/* Settings */}
                  <li className="mt-auto">
                    <a
                      href="#"
                      className="group -mx-2 flex gap-x-3 rounded-md p-2 text-sm/6 font-semibold text-gray-700 hover:bg-gray-50 hover:text-blue-600"
                    >
                      <Cog6ToothIcon
                        aria-hidden="true"
                        className="size-6 shrink-0 text-gray-400 group-hover:text-blue-600"
                      />
                      Settings
                    </a>
                  </li>
                </ul>
              </nav>
            </div>
          </DialogPanel>
        </div>
      </Dialog>

      {/* Desktop Sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-[17.188rem] lg:max-w-[21.875rem] lg:min-w-[15.625rem] lg:flex-col">
        <div className="flex grow flex-col gap-y-5 overflow-y-auto border-r border-gray-200  border-[#eeeff1] bg-[#FBFBFB] px-6 pb-4">
          <div className="flex h-16 shrink-0 items-center">
            <img
              src="logo.png"
              alt="Your Company"
              className="h-14 w-auto"
            />
          </div>
          <nav className="flex flex-1 flex-col">
            {/* Navigation and Teams */}
            <ul className="flex flex-1 flex-col gap-y-7">
              {/* Same structure as above */}
              <li>
                <ul className="-mx-2 space-y-1">
                  {navigation.map((item) => (
                    <li key={item.name}>
                      <a
                        href={item.href}
                        className={classNames(
                          item.current
                            ? 'bg-gray-100 text-black'
                            : 'text-gray-700 hover:text-black hover:bg-sidebar-link-hover',
                          'group flex gap-x-3 rounded-md p-2 text-sm/6 font-semibold'
                        )}
                      >
                        <item.icon
                          aria-hidden="true"
                          className={classNames(
                            item.current ? 'text-amber-600' : 'text-gray-400 group-hover:text-amber-600',
                            'size-6 shrink-0'
                          )}
                        />
                        {item.name}
                      </a>
                    </li>
                  ))}
                </ul>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </>
  );
}
