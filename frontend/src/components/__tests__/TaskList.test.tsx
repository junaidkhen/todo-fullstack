import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import TaskList from '../TaskList'
import { toast } from 'react-hot-toast'

// Mock toast
jest.mock('react-hot-toast')

// Mock TaskItem component to simplify testing
jest.mock('../TaskItem', () => {
  return function MockTaskItem({ task, onUpdate, onDelete, isLoading }: any) {
    return (
      <div data-testid={`task-${task.id}`}>
        <span>{task.title}</span>
        <button onClick={() => onUpdate(task.id, !task.completed)}>Toggle</button>
        <button onClick={() => onDelete(task.id)}>Delete</button>
        {isLoading && <span>Loading...</span>}
      </div>
    )
  }
})

describe('TaskList', () => {
  const mockTasks = [
    {
      id: 'task-1',
      title: 'Task 1',
      description: 'Description 1',
      completed: false,
      created_at: new Date().toISOString(),
      user_id: 'user123'
    },
    {
      id: 'task-2',
      title: 'Task 2',
      description: 'Description 2',
      completed: true,
      created_at: new Date().toISOString(),
      user_id: 'user123'
    },
    {
      id: 'task-3',
      title: 'Task 3',
      description: 'Description 3',
      completed: false,
      created_at: new Date().toISOString(),
      user_id: 'user123'
    }
  ]

  beforeEach(() => {
    jest.clearAllMocks()
    ;(global.fetch as jest.Mock).mockClear()
    localStorage.setItem('auth-token', 'mock-token')
  })

  it('renders empty state when no tasks', () => {
    render(<TaskList tasks={[]} onTasksChange={jest.fn()} />)

    expect(screen.getByText(/no tasks yet/i)).toBeInTheDocument()
  })

  it('renders all tasks', () => {
    render(<TaskList tasks={mockTasks} onTasksChange={jest.fn()} />)

    expect(screen.getByTestId('task-task-1')).toBeInTheDocument()
    expect(screen.getByTestId('task-task-2')).toBeInTheDocument()
    expect(screen.getByTestId('task-task-3')).toBeInTheDocument()
  })

  it('displays correct task count summary', () => {
    render(<TaskList tasks={mockTasks} onTasksChange={jest.fn()} />)

    expect(screen.getByText(/2 pending/i)).toBeInTheDocument()
    expect(screen.getByText(/1 completed/i)).toBeInTheDocument()
  })

  it('successfully toggles task completion', async () => {
    const user = userEvent.setup()
    const mockOnTasksChange = jest.fn()
    const updatedTask = { ...mockTasks[0], completed: true }

    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => updatedTask,
    })

    render(<TaskList tasks={mockTasks} onTasksChange={mockOnTasksChange} />)

    const toggleButton = screen.getAllByText('Toggle')[0]
    await user.click(toggleButton)

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/tasks/task-1/toggle',
        expect.objectContaining({
          method: 'PATCH',
          headers: {
            'Authorization': 'Bearer mock-token',
          },
        })
      )
    })

    await waitFor(() => {
      expect(toast.success).toHaveBeenCalledWith('Task completed!')
      expect(mockOnTasksChange).toHaveBeenCalled()
    })
  })

  it('shows different toast message when unmarking task', async () => {
    const user = userEvent.setup()
    const mockOnTasksChange = jest.fn()
    const completedTask = mockTasks[1]
    const updatedTask = { ...completedTask, completed: false }

    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => updatedTask,
    })

    render(<TaskList tasks={mockTasks} onTasksChange={mockOnTasksChange} />)

    const toggleButton = screen.getAllByText('Toggle')[1]
    await user.click(toggleButton)

    await waitFor(() => {
      expect(toast.success).toHaveBeenCalledWith('Task marked as pending')
    })
  })

  it('performs optimistic update when toggling task', async () => {
    const user = userEvent.setup()
    const mockOnTasksChange = jest.fn()
    let resolvePromise: (value: any) => void

    const fetchPromise = new Promise((resolve) => {
      resolvePromise = resolve
    })

    ;(global.fetch as jest.Mock).mockReturnValueOnce(fetchPromise)

    render(<TaskList tasks={mockTasks} onTasksChange={mockOnTasksChange} />)

    const toggleButton = screen.getAllByText('Toggle')[0]
    await user.click(toggleButton)

    // Should show loading state immediately (optimistic update)
    await waitFor(() => {
      expect(screen.getAllByText('Loading...').length).toBeGreaterThan(0)
    })

    // Resolve the promise
    resolvePromise!({
      ok: true,
      json: async () => ({ ...mockTasks[0], completed: true }),
    })

    await waitFor(() => {
      expect(mockOnTasksChange).toHaveBeenCalled()
    })
  })

  it('rolls back optimistic update on toggle error', async () => {
    const user = userEvent.setup()
    const mockOnTasksChange = jest.fn()

    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
    })

    render(<TaskList tasks={mockTasks} onTasksChange={mockOnTasksChange} />)

    const toggleButton = screen.getAllByText('Toggle')[0]
    await user.click(toggleButton)

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith('Failed to update task')
    })

    // Should not call onTasksChange on error (rollback)
    expect(mockOnTasksChange).not.toHaveBeenCalled()
  })

  it('successfully deletes a task', async () => {
    const user = userEvent.setup()
    const mockOnTasksChange = jest.fn()

    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
    })

    // Mock window.confirm
    window.confirm = jest.fn(() => true)

    render(<TaskList tasks={mockTasks} onTasksChange={mockOnTasksChange} />)

    const deleteButton = screen.getAllByText('Delete')[0]
    await user.click(deleteButton)

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/tasks/task-1',
        expect.objectContaining({
          method: 'DELETE',
          headers: {
            'Authorization': 'Bearer mock-token',
          },
        })
      )
    })

    await waitFor(() => {
      expect(toast.success).toHaveBeenCalledWith('Task deleted successfully')
      expect(mockOnTasksChange).toHaveBeenCalled()
    })
  })

  it('does not delete task if confirmation is cancelled', async () => {
    const user = userEvent.setup()
    const mockOnTasksChange = jest.fn()

    window.confirm = jest.fn(() => false)

    render(<TaskList tasks={mockTasks} onTasksChange={mockOnTasksChange} />)

    const deleteButton = screen.getAllByText('Delete')[0]
    await user.click(deleteButton)

    expect(global.fetch).not.toHaveBeenCalled()
    expect(mockOnTasksChange).not.toHaveBeenCalled()
  })

  it('performs optimistic delete', async () => {
    const user = userEvent.setup()
    const mockOnTasksChange = jest.fn()
    let resolvePromise: (value: any) => void

    const fetchPromise = new Promise((resolve) => {
      resolvePromise = resolve
    })

    ;(global.fetch as jest.Mock).mockReturnValueOnce(fetchPromise)
    window.confirm = jest.fn(() => true)

    render(<TaskList tasks={mockTasks} onTasksChange={mockOnTasksChange} />)

    const deleteButton = screen.getAllByText('Delete')[0]
    await user.click(deleteButton)

    // Optimistic delete - onTasksChange should be called immediately
    await waitFor(() => {
      expect(mockOnTasksChange).toHaveBeenCalled()
    })

    resolvePromise!({ ok: true })
  })

  it('rolls back optimistic delete on error', async () => {
    const user = userEvent.setup()
    const mockOnTasksChange = jest.fn()

    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
    })
    window.confirm = jest.fn(() => true)

    render(<TaskList tasks={mockTasks} onTasksChange={mockOnTasksChange} />)

    const deleteButton = screen.getAllByText('Delete')[0]
    await user.click(deleteButton)

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith('Failed to delete task')
    })

    // Should call onTasksChange twice - once for optimistic, once for rollback
    await waitFor(() => {
      expect(mockOnTasksChange).toHaveBeenCalledTimes(2)
    })
  })

  it('handles network errors gracefully', async () => {
    const user = userEvent.setup()
    const mockOnTasksChange = jest.fn()

    ;(global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'))

    render(<TaskList tasks={mockTasks} onTasksChange={mockOnTasksChange} />)

    const toggleButton = screen.getAllByText('Toggle')[0]
    await user.click(toggleButton)

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith('Failed to update task')
    })
  })

  it('prevents multiple simultaneous operations on same task', async () => {
    const user = userEvent.setup()
    const mockOnTasksChange = jest.fn()
    let resolvePromise: (value: any) => void

    const fetchPromise = new Promise((resolve) => {
      resolvePromise = resolve
    })

    ;(global.fetch as jest.Mock).mockReturnValue(fetchPromise)

    render(<TaskList tasks={mockTasks} onTasksChange={mockOnTasksChange} />)

    const toggleButton = screen.getAllByText('Toggle')[0]

    // Click multiple times quickly
    await user.click(toggleButton)
    await user.click(toggleButton)
    await user.click(toggleButton)

    // Should only make one API call
    expect(global.fetch).toHaveBeenCalledTimes(1)

    resolvePromise!({
      ok: true,
      json: async () => ({ ...mockTasks[0], completed: true }),
    })
  })

  it('has proper ARIA labels for accessibility', () => {
    render(<TaskList tasks={mockTasks} onTasksChange={jest.fn()} />)

    const taskListContainer = screen.getByRole('list', { hidden: true })
    expect(taskListContainer).toBeInTheDocument()
  })

  it('displays tasks in correct order', () => {
    render(<TaskList tasks={mockTasks} onTasksChange={jest.fn()} />)

    const taskElements = screen.getAllByTestId(/task-/)
    expect(taskElements[0]).toHaveAttribute('data-testid', 'task-task-1')
    expect(taskElements[1]).toHaveAttribute('data-testid', 'task-task-2')
    expect(taskElements[2]).toHaveAttribute('data-testid', 'task-task-3')
  })
})
