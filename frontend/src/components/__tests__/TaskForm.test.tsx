import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import TaskForm from '../TaskForm'
import { toast } from 'react-hot-toast'

// Mock toast
jest.mock('react-hot-toast')

describe('TaskForm', () => {
  const mockOnTaskCreated = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
    ;(global.fetch as jest.Mock).mockClear()
    localStorage.setItem('auth-token', 'mock-token')
  })

  it('renders the form with title and description inputs', () => {
    render(<TaskForm onTaskCreated={mockOnTaskCreated} />)

    expect(screen.getByLabelText(/title/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /add task/i })).toBeInTheDocument()
  })

  it('shows character counters for title and description', () => {
    render(<TaskForm onTaskCreated={mockOnTaskCreated} />)

    expect(screen.getByText('0/200')).toBeInTheDocument()
    expect(screen.getByText('0/5000')).toBeInTheDocument()
  })

  it('updates character counters as user types', async () => {
    const user = userEvent.setup()
    render(<TaskForm onTaskCreated={mockOnTaskCreated} />)

    const titleInput = screen.getByLabelText(/title/i)
    await user.type(titleInput, 'Test Task')

    await waitFor(() => {
      expect(screen.getByText('9/200')).toBeInTheDocument()
    })
  })

  it('successfully creates a task', async () => {
    const user = userEvent.setup()
    const mockTask = {
      id: '1',
      title: 'Test Task',
      description: 'Test Description',
      completed: false,
      created_at: new Date().toISOString(),
      user_id: 'user123'
    }

    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockTask,
    })

    render(<TaskForm onTaskCreated={mockOnTaskCreated} />)

    const titleInput = screen.getByLabelText(/title/i)
    const descriptionInput = screen.getByLabelText(/description/i)
    const submitButton = screen.getByRole('button', { name: /add task/i })

    await user.type(titleInput, 'Test Task')
    await user.type(descriptionInput, 'Test Description')
    await user.click(submitButton)

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/tasks',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer mock-token',
          },
          body: JSON.stringify({
            title: 'Test Task',
            description: 'Test Description',
          }),
        })
      )
    })

    await waitFor(() => {
      expect(mockOnTaskCreated).toHaveBeenCalledWith(mockTask)
      expect(toast.success).toHaveBeenCalledWith('Task created successfully!')
    })

    // Form should be cleared
    expect(titleInput).toHaveValue('')
    expect(descriptionInput).toHaveValue('')
  })

  it('shows error toast when title is empty', async () => {
    const user = userEvent.setup()
    render(<TaskForm onTaskCreated={mockOnTaskCreated} />)

    const submitButton = screen.getByRole('button', { name: /add task/i })
    await user.click(submitButton)

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith('Please enter a task title')
    })

    expect(global.fetch).not.toHaveBeenCalled()
    expect(mockOnTaskCreated).not.toHaveBeenCalled()
  })

  it('shows error toast when title exceeds 200 characters', async () => {
    const user = userEvent.setup()
    render(<TaskForm onTaskCreated={mockOnTaskCreated} />)

    const titleInput = screen.getByLabelText(/title/i)
    const longTitle = 'a'.repeat(201)

    await user.type(titleInput, longTitle)

    const submitButton = screen.getByRole('button', { name: /add task/i })
    await user.click(submitButton)

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith('Title must be 200 characters or less')
    })

    expect(global.fetch).not.toHaveBeenCalled()
  })

  it('shows error toast when description exceeds 5000 characters', async () => {
    const user = userEvent.setup()
    render(<TaskForm onTaskCreated={mockOnTaskCreated} />)

    const titleInput = screen.getByLabelText(/title/i)
    const descriptionInput = screen.getByLabelText(/description/i)
    const longDescription = 'a'.repeat(5001)

    await user.type(titleInput, 'Valid Title')
    await user.type(descriptionInput, longDescription)

    const submitButton = screen.getByRole('button', { name: /add task/i })
    await user.click(submitButton)

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith('Description must be 5000 characters or less')
    })

    expect(global.fetch).not.toHaveBeenCalled()
  })

  it('handles API errors gracefully', async () => {
    const user = userEvent.setup()
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
    })

    render(<TaskForm onTaskCreated={mockOnTaskCreated} />)

    const titleInput = screen.getByLabelText(/title/i)
    await user.type(titleInput, 'Test Task')

    const submitButton = screen.getByRole('button', { name: /add task/i })
    await user.click(submitButton)

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith('Failed to create task')
    })

    expect(mockOnTaskCreated).not.toHaveBeenCalled()
  })

  it('shows loading state while creating task', async () => {
    const user = userEvent.setup()
    let resolvePromise: (value: any) => void

    const fetchPromise = new Promise((resolve) => {
      resolvePromise = resolve
    })

    ;(global.fetch as jest.Mock).mockReturnValueOnce(fetchPromise)

    render(<TaskForm onTaskCreated={mockOnTaskCreated} />)

    const titleInput = screen.getByLabelText(/title/i)
    await user.type(titleInput, 'Test Task')

    const submitButton = screen.getByRole('button', { name: /add task/i })
    await user.click(submitButton)

    // Button should show loading state
    await waitFor(() => {
      expect(screen.getByText(/creating/i)).toBeInTheDocument()
    })

    // Resolve the promise
    resolvePromise!({
      ok: true,
      json: async () => ({
        id: '1',
        title: 'Test Task',
        completed: false,
        created_at: new Date().toISOString(),
        user_id: 'user123'
      }),
    })

    await waitFor(() => {
      expect(screen.getByText(/add task/i)).toBeInTheDocument()
    })
  })

  it('disables submit button when loading', async () => {
    const user = userEvent.setup()
    let resolvePromise: (value: any) => void

    const fetchPromise = new Promise((resolve) => {
      resolvePromise = resolve
    })

    ;(global.fetch as jest.Mock).mockReturnValueOnce(fetchPromise)

    render(<TaskForm onTaskCreated={mockOnTaskCreated} />)

    const titleInput = screen.getByLabelText(/title/i)
    await user.type(titleInput, 'Test Task')

    const submitButton = screen.getByRole('button', { name: /add task/i })
    await user.click(submitButton)

    await waitFor(() => {
      expect(submitButton).toBeDisabled()
    })

    resolvePromise!({
      ok: true,
      json: async () => ({
        id: '1',
        title: 'Test Task',
        completed: false,
        created_at: new Date().toISOString(),
        user_id: 'user123'
      }),
    })

    await waitFor(() => {
      expect(submitButton).not.toBeDisabled()
    })
  })

  it('has proper ARIA labels for accessibility', () => {
    render(<TaskForm onTaskCreated={mockOnTaskCreated} />)

    const titleInput = screen.getByLabelText(/title/i)
    const descriptionInput = screen.getByLabelText(/description/i)

    expect(titleInput).toHaveAttribute('aria-label')
    expect(descriptionInput).toHaveAttribute('aria-label')
  })
})
