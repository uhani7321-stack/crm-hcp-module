import React from 'react';

const MainLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-[#F9FAFB] font-sans text-gray-800">
      <main className="max-w-[1400px] mx-auto p-6">
        <h1 className="text-xl font-semibold mb-6">Log HCP Interaction</h1>
        {children}
      </main>
    </div>
  );
};

export default MainLayout;
