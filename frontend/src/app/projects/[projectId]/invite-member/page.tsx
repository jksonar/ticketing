import { useState } from 'react';
import { useParams } from 'next/navigation';

export default function InviteMemberPage() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const params = useParams();
  const { projectId } = params;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await fetch('/api/invitations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify({ email, project_id: projectId }),
    });
    const data = await response.json();
    setMessage(data.message || data.detail);
  };

  return (
    <div>
      <h1>Invite Member</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter email to invite"
          required
        />
        <button type="submit">Invite</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}
