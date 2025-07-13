import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: string | Date) {
  return new Intl.DateTimeFormat("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  }).format(new Date(date))
}

export function formatDateTime(date: string | Date) {
  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(date))
}

export function getInitials(name: string) {
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2)
}

export function getPriorityColor(priority: string) {
  switch (priority.toLowerCase()) {
    case "high":
      return "text-red-600 bg-red-50"
    case "medium":
      return "text-yellow-600 bg-yellow-50"
    case "low":
      return "text-green-600 bg-green-50"
    default:
      return "text-gray-600 bg-gray-50"
  }
}

export function getStatusColor(status: string) {
  switch (status.toLowerCase()) {
    case "open":
      return "text-blue-600 bg-blue-50"
    case "in-progress":
      return "text-yellow-600 bg-yellow-50"
    case "done":
      return "text-green-600 bg-green-50"
    case "closed":
      return "text-gray-600 bg-gray-50"
    default:
      return "text-gray-600 bg-gray-50"
  }
}