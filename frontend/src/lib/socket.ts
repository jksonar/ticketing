import { io } from 'socket.io-client';

const URL = process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'ws://localhost:8000/ws';

export const socket = io(URL, {
  transports: ['websocket'],
});
