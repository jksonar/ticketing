'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';

interface Comment {
  id: number;
  content: string;
  author: { username: string };
  created_at: string;
}

interface Ticket {
  id: number;
  title: string;
  description: string;
  status: string;
  priority: string;
  comments: Comment[];
}

export default function TicketDetails() {
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [newComment, setNewComment] = useState('');
  const params = useParams();
  const { ticketId } = params;

  useEffect(() => {
    if (ticketId) {
      fetchTicket();
    }
  }, [ticketId]);

  const fetchTicket = async () => {
    const token = localStorage.getItem('token');
    const res = await fetch(`/api/tickets/${ticketId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    const data = await res.json();
    setTicket(data);
  };

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const res = await fetch(`/api/tickets/${ticketId}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ content: newComment, ticket_id: ticketId }),
    });

    if (res.ok) {
      fetchTicket();
      setNewComment('');
    }
  };

  if (!ticket) {
    return <div>Loading...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">{ticket.title}</h1>
      <div className="bg-white shadow-md rounded-lg p-4">
        <p className="text-gray-700">{ticket.description}</p>
        <div className="mt-4">
          <span className="font-bold">Status:</span> {ticket.status}
        </div>
        <div>
          <span className="font-bold">Priority:</span> {ticket.priority}
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-bold mb-4">Comments</h2>
        <div className="space-y-4">
          {ticket.comments.map((comment) => (
            <div key={comment.id} className="bg-gray-100 p-4 rounded-lg">
              <p className="font-bold">{comment.author.username}</p>
              <p>{comment.content}</p>
              <p className="text-xs text-gray-500">{new Date(comment.created_at).toLocaleString()}</p>
            </div>
          ))}
        </div>

        <form onSubmit={handleCommentSubmit} className="mt-4">
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            className="w-full border p-2 rounded-md"
            placeholder="Add a comment..."
            required
          ></textarea>
          <button type="submit" className="mt-2 bg-indigo-600 text-white py-2 px-4 rounded-md">
            Add Comment
          </button>
        </form>
      </div>
    </div>
  );
}
