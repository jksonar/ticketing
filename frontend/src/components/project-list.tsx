'use client'

import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { getInitials, formatDate } from '@/lib/utils'
import { FolderOpen, Users, Calendar, Plus } from 'lucide-react'

interface Project {
  id: number
  name: string
  description: string
  created_at: string
  users: Array<{
    id: number
    username: string
    email: string
  }>
}

export function ProjectList() {
  const { data: projects, isLoading, error } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const response = await axios.get('/api/projects')
      return response.data
    },
  })

  if (isLoading) {
    return (
      <div className="space-y-3">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="h-20 bg-gray-200 rounded-md"></div>
          </div>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-muted-foreground">Failed to load projects</p>
        <Button variant="outline" className="mt-2" onClick={() => window.location.reload()}>
          Try Again
        </Button>
      </div>
    )
  }

  if (!projects || projects.length === 0) {
    return (
      <div className="text-center py-8">
        <FolderOpen className="mx-auto h-12 w-12 text-muted-foreground" />
        <h3 className="mt-2 text-sm font-semibold text-gray-900">No projects</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          Get started by creating a new project.
        </p>
        <div className="mt-6">
          <Button asChild>
            <Link href="/create-project">
              <Plus className="mr-2 h-4 w-4" />
              New Project
            </Link>
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {projects.map((project: Project) => (
        <Card key={project.id} className="hover:shadow-md transition-shadow">
          <CardContent className="p-4">
            <div className="flex items-start justify-between">
              <div className="flex-1 min-w-0">
                <Link
                  href={`/projects/${project.id}`}
                  className="text-sm font-medium text-gray-900 hover:text-primary"
                >
                  {project.name}
                </Link>
                <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
                  {project.description || 'No description'}
                </p>
                <div className="flex items-center mt-2 space-x-4 text-xs text-muted-foreground">
                  <div className="flex items-center">
                    <Calendar className="mr-1 h-3 w-3" />
                    {formatDate(project.created_at)}
                  </div>
                  <div className="flex items-center">
                    <Users className="mr-1 h-3 w-3" />
                    {project.users?.length || 0} members
                  </div>
                </div>
              </div>
              <div className="flex -space-x-1 ml-2">
                {project.users?.slice(0, 3).map((user) => (
                  <Avatar key={user.id} className="h-6 w-6 border-2 border-white">
                    <AvatarFallback className="text-xs">
                      {getInitials(user.username)}
                    </AvatarFallback>
                  </Avatar>
                ))}
                {project.users?.length > 3 && (
                  <div className="h-6 w-6 rounded-full bg-gray-100 border-2 border-white flex items-center justify-center">
                    <span className="text-xs text-gray-600">
                      +{project.users.length - 3}
                    </span>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
      
      <div className="pt-2">
        <Button variant="outline" asChild className="w-full">
          <Link href="/projects">
            View All Projects
          </Link>
        </Button>
      </div>
    </div>
  )
}