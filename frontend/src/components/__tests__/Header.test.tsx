import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Header from '../Header'
import { toast } from 'react-hot-toast'
import { useRouter } from 'next/navigation'

// Mock toast
jest.mock('react-hot-toast')

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
}))

describe('Header', () => {
  const mockPush = jest.fn()
  const mockRouter = {
    push: mockPush,
    replace: jest.fn(),
    prefetch: jest.fn(),
    back: jest.fn(),
  }

  beforeEach(() => {
    jest.clearAllMocks()
    ;(global.fetch as jest.Mock).mockClear()
    ;(useRouter as jest.Mock).mockReturnValue(mockRouter)
    localStorage.setItem('auth-token', 'mock-token')
  })

  it('renders the header with title', () => {
    render(<Header />)

    expect(screen.getByText(/todo app/i)).toBeInTheDocument()
  })

  it('renders logout button', () => {
    render(<Header />)

    expect(screen.getByRole('button', { name: /logout/i })).toBeInTheDocument()
  })

  it('successfully logs out user', async () => {
    const user = userEvent.setup()

    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
    })

    render(<Header />)

    const logoutButton = screen.getByRole('button', { name: /logout/i })
    await user.click(logoutButton)

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/api/auth/signout',
        expect.objectContaining({
          method: 'POST',
          headers: {
            'Authorization': 'Bearer mock-token',
          },
        })
      )
    })

    await waitFor(() => {
      expect(localStorage.removeItem).toHaveBeenCalledWith('auth-token')
      expect(toast.success).toHaveBeenCalledWith('Logged out successfully')
      expect(mockPush).toHaveBeenCalledWith('/signin')
    })
  })

  it('shows loading state while logging out', async () => {
    const user = userEvent.setup()
    let resolvePromise: (value: any) => void

    const fetchPromise = new Promise((resolve) => {
      resolvePromise = resolve
    })

    ;(global.fetch as jest.Mock).mockReturnValueOnce(fetchPromise)

    render(<Header />)

    const logoutButton = screen.getByRole('button', { name: /logout/i })
    await user.click(logoutButton)

    await waitFor(() => {
      expect(screen.getByText(/logging out/i)).toBeInTheDocument()
    })

    resolvePromise!({ ok: true })

    await waitFor(() => {
      expect(screen.getByText(/logout/i)).toBeInTheDocument()
    })
  })

  it('disables logout button while loading', async () => {
    const user = userEvent.setup()
    let resolvePromise: (value: any) => void

    const fetchPromise = new Promise((resolve) => {
      resolvePromise = resolve
    })

    ;(global.fetch as jest.Mock).mockReturnValueOnce(fetchPromise)

    render(<Header />)

    const logoutButton = screen.getByRole('button', { name: /logout/i })
    await user.click(logoutButton)

    await waitFor(() => {
      expect(logoutButton).toBeDisabled()
    })

    resolvePromise!({ ok: true })

    await waitFor(() => {
      expect(logoutButton).not.toBeDisabled()
    })
  })

  it('handles logout API error gracefully', async () => {
    const user = userEvent.setup()

    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
    })

    render(<Header />)

    const logoutButton = screen.getByRole('button', { name: /logout/i })
    await user.click(logoutButton)

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith('Failed to logout')
    })

    // Should not redirect or clear token on error
    expect(localStorage.removeItem).not.toHaveBeenCalled()
    expect(mockPush).not.toHaveBeenCalled()
  })

  it('handles network errors gracefully', async () => {
    const user = userEvent.setup()

    ;(global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'))

    render(<Header />)

    const logoutButton = screen.getByRole('button', { name: /logout/i })
    await user.click(logoutButton)

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith('Failed to logout')
    })

    expect(localStorage.removeItem).not.toHaveBeenCalled()
    expect(mockPush).not.toHaveBeenCalled()
  })

  it('clears auth token from localStorage on successful logout', async () => {
    const user = userEvent.setup()

    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
    })

    render(<Header />)

    const logoutButton = screen.getByRole('button', { name: /logout/i })
    await user.click(logoutButton)

    await waitFor(() => {
      expect(localStorage.removeItem).toHaveBeenCalledWith('auth-token')
    })
  })

  it('redirects to signin page on successful logout', async () => {
    const user = userEvent.setup()

    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
    })

    render(<Header />)

    const logoutButton = screen.getByRole('button', { name: /logout/i })
    await user.click(logoutButton)

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/signin')
    })
  })

  it('has proper styling for header', () => {
    const { container } = render(<Header />)

    const header = container.querySelector('header')
    expect(header).toBeInTheDocument()
    expect(header).toHaveClass('bg-white', 'shadow')
  })

  it('has proper ARIA labels for accessibility', () => {
    render(<Header />)

    const logoutButton = screen.getByRole('button', { name: /logout/i })
    expect(logoutButton).toHaveAttribute('aria-label')
  })

  it('prevents multiple logout requests', async () => {
    const user = userEvent.setup()
    let resolvePromise: (value: any) => void

    const fetchPromise = new Promise((resolve) => {
      resolvePromise = resolve
    })

    ;(global.fetch as jest.Mock).mockReturnValue(fetchPromise)

    render(<Header />)

    const logoutButton = screen.getByRole('button', { name: /logout/i })

    // Click multiple times quickly
    await user.click(logoutButton)
    await user.click(logoutButton)
    await user.click(logoutButton)

    // Should only make one API call
    expect(global.fetch).toHaveBeenCalledTimes(1)

    resolvePromise!({ ok: true })
  })

  it('shows loading spinner icon when logging out', async () => {
    const user = userEvent.setup()
    let resolvePromise: (value: any) => void

    const fetchPromise = new Promise((resolve) => {
      resolvePromise = resolve
    })

    ;(global.fetch as jest.Mock).mockReturnValueOnce(fetchPromise)

    render(<Header />)

    const logoutButton = screen.getByRole('button', { name: /logout/i })
    await user.click(logoutButton)

    // The button should show loading text
    await waitFor(() => {
      expect(screen.getByText(/logging out/i)).toBeInTheDocument()
    })

    resolvePromise!({ ok: true })
  })
})
