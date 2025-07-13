'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

interface Project {
  id: number;
  name: string;
  description: string;
}

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([]);

  useEffect(() => {
    const fetchProjects = async () => {
      const token = localStorage.getItem('token');
      const res = await fetch('/api/projects', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      const data = await res.json();
      setProjects(data);
    };

    fetchProjects();
  }, []);

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Projects</h1>
        <Link href="/create-project">
          <a className="bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700">
            Create Project
          </a>
        </Link>
      </div>
      <div className="bg-white shadow-md rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {projects.map((project) => (
              <tr key={project.id}>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{project.id}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{project.name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{project.description}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
