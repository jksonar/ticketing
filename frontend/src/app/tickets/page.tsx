'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Ticket {
  id: number;
  title: string;
  description: string;
  status: string;
  priority: string;
}

export default function Tickets() {
  const [tickets, setTickets] = useState<Ticket[]>([]);

  useEffect(() => {
    const fetchTickets = async () => {
      const res = await fetch('/api/tickets?project_id=1'); // Hardcoded project_id for now
      const data = await res.json();
      setTickets(data);
    };

    fetchTickets();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Tickets</h1>
        <Link href="/create-ticket">
          <a className="bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700">
            Create Ticket
          </a>
        </Link>
      </div>
      <div className="bg-white shadow-md rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {tickets.map((ticket) => (
              <tr key={ticket.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{ticket.id}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{ticket.title}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{ticket.status}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{ticket.priority}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}