'use client';

import { useState } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';

export default function MobileSidebarController({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen">
      <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
      <div className="flex">
        <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
}