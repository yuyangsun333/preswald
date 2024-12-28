'use client'

import { useState } from 'react'
import Content from "./Content";
import Sidebar from "./Sidebar";
import Topbar from "./TopBar";

import { HomeIcon, ChartBarIcon, ServerIcon, GlobeAltIcon } from "@heroicons/react/24/solid";

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon, current: true },
  { name: 'Connections', href: '/connections', icon: ServerIcon, current: false },
  { name: 'Metrics', href: '/metrics', icon: ChartBarIcon, current: false },
  { name: 'Entities', href: '/entities', icon: GlobeAltIcon, current: false },
];

const userNavigation = [
  { name: 'Your profile', href: '#' },
  { name: 'Sign out', href: '#' },
]

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
        <Topbar setSidebarOpen={setSidebarOpen} userNavigation={userNavigation} />
        <main className="py-10">
          <Content>{children}</Content>
        </main>
      </div>
    </>
  );
}