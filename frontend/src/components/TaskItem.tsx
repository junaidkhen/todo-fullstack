'use client';

import { useState } from 'react';

interface Task {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  priority?: string | null;
  category?: string | null;
  due_date?: string | null;
  created_at: string;
  updated_at: string;
}

// Helper function to get priority badge colors
const getPriorityColor = (priority: string | null | undefined) => {
  switch (priority?.toLowerCase()) {
    case 'high':
      return 'bg-red-100 text-red-700';
    case 'medium':
      return 'bg-amber-100 text-amber-700';
    case 'low':
      return 'bg-teal-100 text-teal-700';
    default:
      return 'bg-gray-100 text-gray-700';
  }
};

// Helper function to get category icon
const getCategoryIcon = (category: string | null | undefined) => {
  switch (category?.toLowerCase()) {
    case 'work':
      return (
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
      );
    case 'health':
      return (
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
      );
    case 'shopping':
      return (
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      );
    case 'finance':
      return (
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      );
    default:
      return (
        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
        </svg>
      );
  }
};

// Helper function to format due date
const formatDueDate = (dateString: string | null | undefined) => {
  if (!dateString) return null;

  const date = new Date(dateString);
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);

  // Reset time parts for comparison
  today.setHours(0, 0, 0, 0);
  tomorrow.setHours(0, 0, 0, 0);
  date.setHours(0, 0, 0, 0);

  if (date.getTime() === today.getTime()) {
    return 'Today';
  } else if (date.getTime() === tomorrow.getTime()) {
    return 'Tomorrow';
  } else {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  }
};

interface TaskItemProps {
  task: Task;
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
  onEdit: (task: Task) => void;
  isLoading?: boolean;
}

export default function TaskItem({ task, onToggle, onDelete, onEdit, isLoading = false }: TaskItemProps) {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <div
      className={`bg-white rounded-xl border border-gray-200 p-4 hover:shadow-md transition-all ${
        task.completed ? 'opacity-60' : ''
      } ${isLoading ? 'opacity-50 pointer-events-none' : ''}`}
      role="listitem"
      aria-label={`Task: ${task.title}`}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <button
          onClick={() => onToggle(task.id)}
          disabled={isLoading}
          className={`flex-shrink-0 mt-0.5 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
            task.completed
              ? 'bg-teal-500 border-teal-500'
              : 'border-gray-300 hover:border-teal-500'
          } disabled:opacity-50 disabled:cursor-not-allowed`}
          aria-label={task.completed ? "Mark task as incomplete" : "Mark task as complete"}
        >
          {task.completed && (
            <svg className="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
            </svg>
          )}
        </button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1 min-w-0">
              <h3
                className={`text-base font-medium ${
                  task.completed ? 'line-through text-gray-500' : 'text-gray-900'
                }`}
              >
                {task.title}
              </h3>

              {/* Badges Row */}
              <div className="flex flex-wrap items-center gap-2 mt-2">
                {/* Priority Badge */}
                {task.priority && (
                  <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium ${getPriorityColor(task.priority)}`}>
                    {task.priority}
                  </span>
                )}

                {/* Category Badge */}
                {task.category && (
                  <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs bg-blue-100 text-blue-700">
                    {getCategoryIcon(task.category)}
                    <span className="ml-1.5">{task.category}</span>
                  </span>
                )}

                {/* Due Date Badge */}
                {task.due_date && (
                  <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs bg-gray-100 text-gray-600">
                    <svg className="w-3.5 h-3.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {formatDueDate(task.due_date)}
                  </span>
                )}
              </div>

              {/* Show Details Toggle */}
              {task.description && (
                <button
                  onClick={() => setShowDetails(!showDetails)}
                  className="inline-flex items-center text-xs text-gray-500 hover:text-teal-600 mt-2 focus:outline-none"
                >
                  <svg
                    className={`w-4 h-4 mr-1 transition-transform ${showDetails ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                  {showDetails ? 'Hide details' : 'Show details'}
                </button>
              )}

              {/* Details Section */}
              {showDetails && task.description && (
                <div className="mt-3 text-sm text-gray-600 p-3 bg-gray-50 rounded-lg">
                  {task.description}
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-2 flex-shrink-0">
              <button
                onClick={() => onEdit(task)}
                disabled={isLoading}
                className="p-2 text-gray-400 hover:text-teal-600 hover:bg-teal-50 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                aria-label={`Edit task: ${task.title}`}
                title="Edit task"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
              </button>
              <button
                onClick={() => onDelete(task.id)}
                disabled={isLoading}
                className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                aria-label={`Delete task: ${task.title}`}
                title="Delete task"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}