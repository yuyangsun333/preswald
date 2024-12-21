'use client'

import { useState } from 'react'
import Content from "./Content";
import Sidebar from "./Sidebar";
import Topbar from "./TopBar";

import {
  HomeIcon,
} from '@heroicons/react/24/outline'

const navigation = [
  { name: 'Dashboard', href: '#', icon: HomeIcon, current: true },
]

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
      <div className="lg:pl-72">
        <Topbar setSidebarOpen={setSidebarOpen} userNavigation={userNavigation} />
        <main className="py-10">
          <Content>{children}</Content>
        </main>
      </div>
    </>
  );
}