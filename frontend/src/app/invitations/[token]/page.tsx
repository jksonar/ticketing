import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';

export default function AcceptInvitationPage() {
  const [message, setMessage] = useState('');
  const params = useParams();
  const { token } = params;

  useEffect(() => {
    const acceptInvitation = async () => {
      if (token) {
        const response = await fetch(`/api/invitations/${token}`,
        {
        headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
      }
        );
        const data = await response.json();
        setMessage(data.message || data.detail);
      }
    };
    acceptInvitation();
  }, [token]);

  return (
    <div>
      <h1>Accepting Invitation</h1>
      <p>{message}</p>
    </div>
  );
}
