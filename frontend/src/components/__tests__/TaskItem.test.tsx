import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import TaskItem from '../TaskItem'
import { toast } from 'react-hot-toast'

// Mock toast
jest.mock('react-hot-toast')

describe('TaskItem', () => {
  const mockTask = {
    id: 'task-1',
    title: 'Test Task',
    description: 'Test Description',
    completed: false,
    created_at: new Date('2026-01-01').toISOString(),
    user_id: 'user123'
  }

  const mockOnUpdate = jest.fn()
  const mockOnDelete = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders task title and description', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    expect(screen.getByText('Test Task')).toBeInTheDocument()
    expect(screen.getByText('Test Description')).toBeInTheDocument()
  })

  it('renders task without description', () => {
    const taskWithoutDesc = { ...mockTask, description: undefined }
    render(
      <TaskItem
        task={taskWithoutDesc}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    expect(screen.getByText('Test Task')).toBeInTheDocument()
    expect(screen.queryByText('Test Description')).not.toBeInTheDocument()
  })

  it('truncates long descriptions with ellipsis', () => {
    const longDescription = 'a'.repeat(150)
    const taskWithLongDesc = { ...mockTask, description: longDescription }

    render(
      <TaskItem
        task={taskWithLongDesc}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    const descriptionElement = screen.getByText(/aaa/i)
    expect(descriptionElement.textContent).toHaveLength(104) // 100 chars + "..."
  })

  it('shows completed status badge for completed tasks', () => {
    const completedTask = { ...mockTask, completed: true }
    render(
      <TaskItem
        task={completedTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    expect(screen.getByText('Completed')).toBeInTheDocument()
  })

  it('shows pending status badge for incomplete tasks', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    expect(screen.getByText('Pending')).toBeInTheDocument()
  })

  it('applies strike-through style to completed task title', () => {
    const completedTask = { ...mockTask, completed: true }
    render(
      <TaskItem
        task={completedTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    const titleElement = screen.getByText('Test Task')
    expect(titleElement).toHaveClass('line-through')
  })

  it('calls onUpdate when checkbox is clicked', async () => {
    const user = userEvent.setup()
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    const checkbox = screen.getByRole('checkbox')
    await user.click(checkbox)

    expect(mockOnUpdate).toHaveBeenCalledWith(mockTask.id, true)
  })

  it('checkbox reflects task completion status', () => {
    const { rerender } = render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    const checkbox = screen.getByRole('checkbox') as HTMLInputElement
    expect(checkbox.checked).toBe(false)

    const completedTask = { ...mockTask, completed: true }
    rerender(
      <TaskItem
        task={completedTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    expect(checkbox.checked).toBe(true)
  })

  it('shows edit button', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    expect(screen.getByRole('button', { name: /edit/i })).toBeInTheDocument()
  })

  it('shows delete button', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    expect(screen.getByRole('button', { name: /delete/i })).toBeInTheDocument()
  })

  it('calls onDelete when delete button is clicked', async () => {
    const user = userEvent.setup()
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    const deleteButton = screen.getByRole('button', { name: /delete/i })
    await user.click(deleteButton)

    expect(mockOnDelete).toHaveBeenCalledWith(mockTask.id)
  })

  it('disables all controls when isLoading is true', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        isLoading={true}
      />
    )

    const checkbox = screen.getByRole('checkbox')
    const editButton = screen.getByRole('button', { name: /edit/i })
    const deleteButton = screen.getByRole('button', { name: /delete/i })

    expect(checkbox).toBeDisabled()
    expect(editButton).toBeDisabled()
    expect(deleteButton).toBeDisabled()
  })

  it('applies reduced opacity when loading', () => {
    const { container } = render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
        isLoading={true}
      />
    )

    const taskCard = container.firstChild as HTMLElement
    expect(taskCard).toHaveClass('opacity-50')
  })

  it('displays formatted creation date', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    // Should display a formatted date (exact format may vary)
    expect(screen.getByText(/created/i)).toBeInTheDocument()
  })

  it('has proper ARIA labels for accessibility', () => {
    render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    const checkbox = screen.getByRole('checkbox')
    const editButton = screen.getByRole('button', { name: /edit/i })
    const deleteButton = screen.getByRole('button', { name: /delete/i })

    expect(checkbox).toHaveAttribute('aria-label')
    expect(editButton).toHaveAttribute('aria-label')
    expect(deleteButton).toHaveAttribute('aria-label')
  })

  it('checkbox has correct aria-label based on completion status', () => {
    const { rerender } = render(
      <TaskItem
        task={mockTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    const checkbox = screen.getByRole('checkbox')
    expect(checkbox).toHaveAttribute('aria-label', expect.stringContaining('Mark'))

    const completedTask = { ...mockTask, completed: true }
    rerender(
      <TaskItem
        task={completedTask}
        onUpdate={mockOnUpdate}
        onDelete={mockOnDelete}
      />
    )

    expect(checkbox).toHaveAttribute('aria-label', expect.stringContaining('Unmark'))
  })
})
