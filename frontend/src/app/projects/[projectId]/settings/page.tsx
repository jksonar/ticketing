import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';

export default function ProjectSettingsPage() {
  const [project, setProject] = useState(null);
  const [message, setMessage] = useState('');
  const params = useParams();
  const { projectId } = params;

  useEffect(() => {
    const fetchProject = async () => {
      const response = await fetch(`/api/projects/${projectId}/settings`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      const data = await response.json();
      if (response.ok) {
        setProject(data);
      } else {
        setMessage(data.detail);
      }
    };
    fetchProject();
  }, [projectId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await fetch(`/api/projects/${projectId}/settings`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(project),
    });
    const data = await response.json();
    if (response.ok) {
      setMessage('Project updated successfully');
    } else {
      setMessage(data.detail);
    }
  };

  if (!project) return <div>Loading...</div>;

  return (
    <div>
      <h1>Project Settings</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={project.name}
          onChange={(e) => setProject({ ...project, name: e.target.value })}
          placeholder="Project name"
        />
        <textarea
          value={project.description}
          onChange={(e) => setProject({ ...project, description: e.target.value })}
          placeholder="Project description"
        />
        <button type="submit">Update</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}
