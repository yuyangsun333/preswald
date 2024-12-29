'use client';

import { Bars3Icon } from '@heroicons/react/20/solid';

export default function Topbar({ setSidebarOpen }) {
  return (
    <div className="sticky top-0 z-40 flex h-14 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 sm:gap-x-6 sm:px-6 lg:px-8">
      <button type="button" onClick={() => setSidebarOpen(true)} className="-m-2.5 p-2.5 text-gray-700">
        <span className="sr-only">Open sidebar</span>
        <Bars3Icon className="size-6" aria-hidden="true" />
      </button>
    </div>
  );
}
