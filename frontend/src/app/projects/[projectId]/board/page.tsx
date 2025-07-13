'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { socket } from '@/lib/socket';

interface Ticket {
  id: number;
  title: string;
}

interface Column {
  id: number;
  name: string;
  tickets: Ticket[];
}

interface Board {
  id: number;
  name: string;
  columns: Column[];
}

export default function BoardPage() {
  const [board, setBoard] = useState<Board | null>(null);
  const params = useParams();
  const { projectId } = params;

  useEffect(() => {
    if (projectId) {
      fetchBoard();
    }

    socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    socket.on('ticket_update', (updatedTicket) => {
      // Update the board state with the new ticket data
      setBoard((prevBoard) => {
        if (!prevBoard) return prevBoard;
        const newColumns = prevBoard.columns.map((column) => {
          const newTickets = column.tickets.map((ticket) => {
            if (ticket.id === updatedTicket.id) {
              return updatedTicket;
            }
            return ticket;
          });
          return { ...column, tickets: newTickets };
        });
        return { ...prevBoard, columns: newColumns } as Board;
      });
    });

    return () => {
      socket.off('connect');
      socket.off('ticket_update');
    };
  }, [projectId]);

  const fetchBoard = async () => {
    const token = localStorage.getItem('token');
    const res = await fetch(`/api/projects/${projectId}/boards`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    const data = await res.json();
    setBoard(data[0]);
  };

  const onDragEnd = (result: any) => {
    // ... (drag and drop logic)
  };

  if (!board) {
    return <div>Loading...</div>;
  }

  return (
    <DragDropContext onDragEnd={onDragEnd}>
      <></>
      {/* ... (board rendering logic) */}
    </DragDropContext>
  );
}