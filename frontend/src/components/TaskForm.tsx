'use client';

import { useState } from 'react';
import toast from 'react-hot-toast';
import { createTask } from '@/lib/api';

export default function TaskForm() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      toast.error('Title is required');
      return;
    }

    if (title.length > 200) {
      toast.error('Title must be 200 characters or less');
      return;
    }

    if (description.length > 1000) {
      toast.error('Description must be 1000 characters or less');
      return;
    }

    setLoading(true);

    try {
      const response = await createTask({
        title: title.trim(),
        description: description || null,
      });

      if (response.data) {
        setTitle('');
        setDescription('');
        toast.success('Task created successfully!');
        // Trigger a refresh of the task list in the parent component
        window.location.reload();
      } else {
        toast.error(response.error || 'Failed to create task');
      }
    } catch (err) {
      toast.error('An error occurred while creating the task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow sm:rounded-lg p-6" role="form" aria-label="Create new task form">
      <h2 className="text-lg font-medium text-gray-900 mb-4" id="form-heading">Add New Task</h2>
      <form onSubmit={handleSubmit} className="space-y-4" aria-labelledby="form-heading">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700">
            Title *
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="What needs to be done?"
            maxLength={200}
            required
            aria-required="true"
            aria-describedby="title-help"
            disabled={loading}
          />
          <p id="title-help" className="mt-1 text-xs text-gray-500">
            Required. Maximum 200 characters. ({title.length}/200)
          </p>
        </div>
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700">
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
            className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="Add details (optional)"
            maxLength={1000}
            aria-describedby="description-help"
            disabled={loading}
          />
          <p id="description-help" className="mt-1 text-xs text-gray-500">
            Optional. Maximum 1000 characters. ({description.length}/1000)
          </p>
        </div>
        <div>
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            aria-label="Create new task"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Creating...
              </>
            ) : (
              <>
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Add Task
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}