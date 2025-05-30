import DealList from './components/DealList';

import { Outlet } from 'react-router-dom'

export default function App() {
  return (
    <div className="h-screen w-screen flex">
      <div className="w-1/4 bg-gray-100 p-4 overflow-y-auto">
        <DealList />
      </div>
      <div className="w-3/4 p-6 overflow-y-auto">
        <Outlet />
      </div>
    </div>
  );
}