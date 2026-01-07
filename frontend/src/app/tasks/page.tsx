'use client';

import { useState, useEffect } from 'react';
import { redirect } from 'next/navigation';
import Header from '@/components/Header';
import TaskListClient from '@/components/TaskList';
import TaskFormModal from '@/components/TaskFormModal';
import StatsCard from '@/components/StatsCard';
import { fetchTasks } from '@/lib/api';

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

export default function TasksPage() {
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  // Load tasks for stats
  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    setLoading(true);
    try {
      const response = await fetchTasks();
      if (response.data) {
        setTasks(response.data);
      }
    } catch (error) {
      console.error('Failed to load tasks', error);
    } finally {
      setLoading(false);
    }
  };

  // Calculate stats
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter((task) => task.completed).length;
  const activeTasks = totalTasks - completedTasks;

  // Calculate overdue tasks (tasks with due_date in the past and not completed)
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const overdueTasks = tasks.filter((task) => {
    if (!task.due_date || task.completed) return false;
    const dueDate = new Date(task.due_date);
    dueDate.setHours(0, 0, 0, 0);
    return dueDate < today;
  }).length;

  const handleTaskCreated = () => {
    setShowTaskForm(false);
    loadTasks(); // Refresh tasks
  };

  return (
    <>
      <Header onAddTask={() => setShowTaskForm(true)} />
      <main className="min-h-screen bg-gray-50 py-8" role="main">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Stats Dashboard */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <StatsCard label="Total Tasks" value={totalTasks} />
            <StatsCard label="Completed" value={completedTasks} />
            <StatsCard label="Active" value={activeTasks} />
            <StatsCard label="Overdue" value={overdueTasks} />
          </div>

          {/* Task List */}
          <TaskListClient key={tasks.length} />
        </div>
      </main>

      {/* Task Form Modal */}
      {showTaskForm && (
        <TaskFormModal
          onClose={() => setShowTaskForm(false)}
          onTaskCreated={handleTaskCreated}
        />
      )}
    </>
  );
}