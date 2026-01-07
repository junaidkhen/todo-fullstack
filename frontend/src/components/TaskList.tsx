'use client';

import { useState, useEffect, useMemo } from 'react';
import toast from 'react-hot-toast';
import TaskItem from './TaskItem';
import SearchAndFilters from './SearchAndFilters';
import { fetchTasks, updateTask, deleteTask, toggleTaskCompletion } from '@/lib/api';

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

export default function TaskListClient() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState({
    title: '',
    description: '',
    priority: 'Medium',
    category: '',
    due_date: '',
  });
  const [loadingStates, setLoadingStates] = useState<Record<number, boolean>>({});

  // Filter and sort states
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [priorityFilter, setPriorityFilter] = useState('all');
  const [sortBy, setSortBy] = useState('newest');

  // Fetch tasks on component mount
  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    setLoading(true);
    try {
      const response = await fetchTasks();
      if (response.data) {
        setTasks(response.data);
      } else {
        toast.error(response.error || 'Failed to load tasks');
      }
    } catch (error) {
      toast.error('Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  const setTaskLoading = (taskId: number, isLoading: boolean) => {
    setLoadingStates(prev => ({
      ...prev,
      [taskId]: isLoading,
    }));
  };

  const handleToggle = async (taskId: number) => {
    if (loadingStates[taskId]) return;

    setTaskLoading(taskId, true);

    try {
      const response = await toggleTaskCompletion(taskId);
      if (response.data) {
        toast.success(response.data.completed ? 'Task completed!' : 'Task marked as incomplete');
        // Update the task in the local state
        setTasks(prev => prev.map(task =>
          task.id === taskId ? { ...task, completed: response.data.completed } : task
        ));
      } else {
        toast.error(response.error || 'Failed to update task');
      }
    } catch (error) {
      toast.error('Error updating task');
    } finally {
      setTaskLoading(taskId, false);
    }
  };

  const handleDelete = async (taskId: number) => {
    if (loadingStates[taskId]) return;

    // Confirm deletion
    if (!confirm('Are you sure you want to delete this task?')) {
      return;
    }

    setTaskLoading(taskId, true);

    try {
      const response = await deleteTask(taskId);
      if (response.data || !response.error) {
        toast.success('Task deleted successfully');
        // Remove the task from the local state
        setTasks(prev => prev.filter(task => task.id !== taskId));
      } else {
        toast.error(response.error || 'Failed to delete task');
      }
    } catch (error) {
      toast.error('Error deleting task');
    } finally {
      setTaskLoading(taskId, false);
    }
  };

  const startEditing = (task: Task) => {
    setEditingTaskId(task.id);
    setEditForm({
      title: task.title,
      description: task.description || '',
      priority: task.priority || 'Medium',
      category: task.category || '',
      due_date: task.due_date ? task.due_date.split('T')[0] : '',
    });
  };

  const handleEdit = async (taskId: number) => {
    if (loadingStates[taskId]) return;

    if (!editForm.title.trim()) {
      toast.error('Title is required');
      return;
    }

    setTaskLoading(taskId, true);

    try {
      const response = await updateTask(taskId, {
        title: editForm.title,
        description: editForm.description || null,
        priority: editForm.priority,
        category: editForm.category || null,
        due_date: editForm.due_date || null,
      });

      if (response.data) {
        const updatedTask = response.data;
        setEditingTaskId(null);
        toast.success('Task updated successfully');
        // Update the task in the local state
        setTasks(prev => prev.map(task =>
          task.id === taskId ? updatedTask : task
        ));
      } else {
        toast.error(response.error || 'Failed to update task');
      }
    } catch (error) {
      toast.error('Error updating task');
    } finally {
      setTaskLoading(taskId, false);
    }
  };

  const cancelEdit = () => {
    setEditingTaskId(null);
  };

  // Filter and sort tasks
  const filteredAndSortedTasks = useMemo(() => {
    let filtered = tasks;

    // Apply search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (task) =>
          task.title.toLowerCase().includes(query) ||
          (task.description && task.description.toLowerCase().includes(query))
      );
    }

    // Apply status filter
    if (statusFilter === 'active') {
      filtered = filtered.filter((task) => !task.completed);
    } else if (statusFilter === 'completed') {
      filtered = filtered.filter((task) => task.completed);
    }

    // Apply category filter
    if (categoryFilter !== 'all') {
      filtered = filtered.filter((task) => task.category === categoryFilter);
    }

    // Apply priority filter
    if (priorityFilter !== 'all') {
      filtered = filtered.filter((task) => task.priority === priorityFilter);
    }

    // Apply sorting
    const sorted = [...filtered];
    switch (sortBy) {
      case 'newest':
        sorted.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        break;
      case 'oldest':
        sorted.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());
        break;
      case 'title':
        sorted.sort((a, b) => a.title.localeCompare(b.title));
        break;
      case 'title-desc':
        sorted.sort((a, b) => b.title.localeCompare(a.title));
        break;
      case 'dueDate':
        sorted.sort((a, b) => {
          if (!a.due_date) return 1;
          if (!b.due_date) return -1;
          return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
        });
        break;
      case 'priority':
        const priorityOrder = { High: 0, Medium: 1, Low: 2 };
        sorted.sort((a, b) => {
          const aPriority = priorityOrder[a.priority as keyof typeof priorityOrder] ?? 3;
          const bPriority = priorityOrder[b.priority as keyof typeof priorityOrder] ?? 3;
          return aPriority - bPriority;
        });
        break;
    }

    return sorted;
  }, [tasks, searchQuery, statusFilter, categoryFilter, priorityFilter, sortBy]);

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-teal-500 mb-4"></div>
        <h3 className="text-sm font-medium text-gray-900">Loading tasks...</h3>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Search and Filters */}
      <SearchAndFilters
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
        statusFilter={statusFilter}
        onStatusChange={setStatusFilter}
        categoryFilter={categoryFilter}
        onCategoryChange={setCategoryFilter}
        priorityFilter={priorityFilter}
        onPriorityChange={setPriorityFilter}
        sortBy={sortBy}
        onSortChange={setSortBy}
      />

      {/* Task List */}
      <div className="space-y-3" role="list" aria-label="Task list">
        {filteredAndSortedTasks.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-xl border border-gray-200">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">
              {tasks.length === 0 ? 'No tasks yet' : 'No tasks found'}
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              {tasks.length === 0
                ? 'Get started by creating a new task.'
                : 'Try adjusting your filters or search query.'}
            </p>
          </div>
        ) : editingTaskId !== null ? (
          // Edit Modal Overlay
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl shadow-xl max-w-lg w-full p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Edit Task</h3>
              <div className="space-y-4">
                <div>
                  <label htmlFor={`edit-title-${editingTaskId}`} className="block text-sm font-medium text-gray-700 mb-1">
                    Title *
                  </label>
                  <input
                    id={`edit-title-${editingTaskId}`}
                    type="text"
                    value={editForm.title}
                    onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault();
                        handleEdit(editingTaskId);
                      } else if (e.key === 'Escape') {
                        cancelEdit();
                      }
                    }}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                    placeholder="Task title"
                    aria-required="true"
                  />
                </div>
                <div>
                  <label htmlFor={`edit-description-${editingTaskId}`} className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    id={`edit-description-${editingTaskId}`}
                    value={editForm.description}
                    onChange={(e) => setEditForm({ ...editForm, description: e.target.value })}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                    placeholder="Task description (optional)"
                    rows={3}
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor={`edit-priority-${editingTaskId}`} className="block text-sm font-medium text-gray-700 mb-1">
                      Priority
                    </label>
                    <select
                      id={`edit-priority-${editingTaskId}`}
                      value={editForm.priority}
                      onChange={(e) => setEditForm({ ...editForm, priority: e.target.value })}
                      className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                      disabled={loadingStates[editingTaskId]}
                    >
                      <option value="Low">Low</option>
                      <option value="Medium">Medium</option>
                      <option value="High">High</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor={`edit-category-${editingTaskId}`} className="block text-sm font-medium text-gray-700 mb-1">
                      Category
                    </label>
                    <select
                      id={`edit-category-${editingTaskId}`}
                      value={editForm.category}
                      onChange={(e) => setEditForm({ ...editForm, category: e.target.value })}
                      className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                      disabled={loadingStates[editingTaskId]}
                    >
                      <option value="">None</option>
                      <option value="Work">Work</option>
                      <option value="Personal">Personal</option>
                      <option value="Health">Health</option>
                      <option value="Shopping">Shopping</option>
                      <option value="Finance">Finance</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label htmlFor={`edit-due-date-${editingTaskId}`} className="block text-sm font-medium text-gray-700 mb-1">
                    Due Date
                  </label>
                  <input
                    type="date"
                    id={`edit-due-date-${editingTaskId}`}
                    value={editForm.due_date}
                    onChange={(e) => setEditForm({ ...editForm, due_date: e.target.value })}
                    className="block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                    disabled={loadingStates[editingTaskId]}
                  />
                </div>

                <div className="flex justify-end gap-3 pt-4">
                  <button
                    onClick={cancelEdit}
                    disabled={loadingStates[editingTaskId]}
                    className="px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    aria-label="Cancel editing"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={() => handleEdit(editingTaskId)}
                    disabled={loadingStates[editingTaskId]}
                    className="px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-teal-500 hover:bg-teal-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    aria-label="Save edited task"
                  >
                    {loadingStates[editingTaskId] ? (
                      <>
                        <svg
                          className="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline"
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                        >
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Saving...
                      </>
                    ) : (
                      'Save Changes'
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : null}

        {filteredAndSortedTasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onToggle={handleToggle}
            onDelete={handleDelete}
            onEdit={startEditing}
            isLoading={loadingStates[task.id] || false}
          />
        ))}
      </div>
    </div>
  );
}