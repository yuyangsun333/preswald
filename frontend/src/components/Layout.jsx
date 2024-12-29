'use client'

import { useState } from 'react'
import Content from "./Content";
import Sidebar from "./Sidebar";
import Topbar from "./TopBar";

import { HomeIcon, ChartBarIcon, MagnifyingGlassIcon, ServerIcon, GlobeAltIcon, ClockIcon, DocumentTextIcon } from "@heroicons/react/24/solid";

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon, current: true },
  { name: 'Queries', href: '/queries', icon: MagnifyingGlassIcon, current: false },
  { name: 'Metrics', href: '/metrics', icon: ChartBarIcon, current: false },
  { name: 'Schedules', href: '/schedules', icon: ClockIcon, current: false },  
  { name: 'Connections', href: '/connections', icon: ServerIcon, current: false },
  { name: 'Entities', href: '/entities', icon: GlobeAltIcon, current: false },
  { name: 'Definitions', href: '/definitions', icon: DocumentTextIcon, current: false },
];

export default function Example({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <>
      <Sidebar
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
        navigation={navigation}
      />
      <div className="lg:pl-80">
        <Topbar setSidebarOpen={setSidebarOpen} />
        <main>
          <Content>{children}</Content>
        </main>
      </div>
    </>
  );
}