'use client'

import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { getInitials, formatDateTime, getPriorityColor, getStatusColor } from '@/lib/utils'
import { Ticket, Clock, User, Plus } from 'lucide-react'

interface TicketItem {
  id: number
  title: string
  description: string
  status: string
  priority: string
  created_at: string
  updated_at: string
  owner: {
    id: number
    username: string
    email: string
  }
}

export function RecentTickets() {
  const { data: tickets, isLoading, error } = useQuery({
    queryKey: ['recent-tickets'],
    queryFn: async () => {
      const response = await axios.get('/api/tickets?limit=5&sort=updated_at')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <div className="space-y-3">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="h-16 bg-gray-200 rounded-md"></div>
          </div>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-muted-foreground">Failed to load tickets</p>
        <Button variant="outline" className="mt-2" onClick={() => window.location.reload()}>
          Try Again
        </Button>
      </div>
    )
  }

  if (!tickets || tickets.length === 0) {
    return (
      <div className="text-center py-8">
        <Ticket className="mx-auto h-12 w-12 text-muted-foreground" />
        <h3 className="mt-2 text-sm font-semibold text-gray-900">No tickets</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          Get started by creating a new ticket.
        </p>
        <div className="mt-6">
          <Button asChild>
            <Link href="/create-ticket">
              <Plus className="mr-2 h-4 w-4" />
              New Ticket
            </Link>
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {tickets.map((ticket: TicketItem) => (
        <Card key={ticket.id} className="hover:shadow-md transition-shadow">
          <CardContent className="p-4">
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-1">
                  <Link
                    href={`/tickets/${ticket.id}`}
                    className="text-sm font-medium text-gray-900 hover:text-primary truncate"
                  >
                    {ticket.title}
                  </Link>
                </div>
                <p className="text-xs text-muted-foreground line-clamp-2 mb-2">
                  {ticket.description || 'No description'}
                </p>
                <div className="flex items-center space-x-2">
                  <Badge 
                    variant="secondary" 
                    className={`text-xs ${getStatusColor(ticket.status)}`}
                  >
                    {ticket.status}
                  </Badge>
                  <Badge 
                    variant="outline" 
                    className={`text-xs ${getPriorityColor(ticket.priority)}`}
                  >
                    {ticket.priority}
                  </Badge>
                </div>
                <div className="flex items-center mt-2 space-x-4 text-xs text-muted-foreground">
                  <div className="flex items-center">
                    <Clock className="mr-1 h-3 w-3" />
                    {formatDateTime(ticket.updated_at)}
                  </div>
                  {ticket.owner && (
                    <div className="flex items-center">
                      <User className="mr-1 h-3 w-3" />
                      {ticket.owner.username}
                    </div>
                  )}
                </div>
              </div>
              {ticket.owner && (
                <div className="ml-2">
                  <Avatar className="h-6 w-6">
                    <AvatarFallback className="text-xs">
                      {getInitials(ticket.owner.username)}
                    </AvatarFallback>
                  </Avatar>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
      
      <div className="pt-2">
        <Button variant="outline" asChild className="w-full">
          <Link href="/tickets">
            View All Tickets
          </Link>
        </Button>
      </div>
    </div>
  )
}