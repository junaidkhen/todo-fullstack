# End-to-End Test Scenarios

**Purpose**: Manual E2E testing checklist for full user journey validation
**Date**: 2026-01-03
**Feature**: 002-fullstack-todo-web

---

## Test Environment Setup

### Prerequisites
- [ ] Backend server running on http://localhost:8000
- [ ] Frontend server running on http://localhost:3000
- [ ] Database initialized (SQLite or PostgreSQL)
- [ ] Test browsers: Chrome, Firefox, Safari, Edge (latest versions)
- [ ] Network tools ready (DevTools, Network tab)

---

## Test Scenario 1: New User Signup & First Task

**Objective**: Verify complete user onboarding flow

### Steps:
1. **Navigate to App**
   - [ ] Open http://localhost:3000
   - [ ] Verify landing page loads
   - [ ] Check for signup/signin links

2. **Sign Up**
   - [ ] Click "Sign Up" link
   - [ ] Enter email: `testuser1@example.com`
   - [ ] Enter password: `TestPass123!`
   - [ ] Submit form
   - [ ] Verify redirect to `/tasks` page
   - [ ] Check for auth token in browser storage (DevTools → Application → Local Storage)

3. **Create First Task**
   - [ ] Verify empty state message appears ("No tasks yet")
   - [ ] Fill title: "Buy groceries"
   - [ ] Fill description: "Milk, eggs, bread"
   - [ ] Click "Add Task" button
   - [ ] Verify loading spinner appears briefly
   - [ ] Verify success toast notification
   - [ ] Verify task appears in list
   - [ ] Verify task shows as "pending" (not completed)

### Expected Results:
- ✅ User successfully creates account
- ✅ Auth token stored in localStorage
- ✅ First task created and visible
- ✅ Toast notifications work

---

## Test Scenario 2: Task Management (CRUD Operations)

**Objective**: Test all task operations

### Setup:
- [ ] User logged in with at least 1 existing task

### Steps:

#### 2.1: Create Multiple Tasks
- [ ] Create task: "Call dentist" (title only, no description)
- [ ] Create task: "Write report" with description "Q4 summary"
- [ ] Create task with long title (190 characters) - should succeed
- [ ] Try to create task with title > 200 chars - should show error toast
- [ ] Try to submit empty title - should show validation error
- [ ] Verify all valid tasks appear in list

#### 2.2: View Task Details
- [ ] Verify task list shows titles
- [ ] Verify descriptions truncated at 100 characters with "..."
- [ ] Verify "Created" timestamps display correctly
- [ ] Verify pending/completed status indicators

#### 2.3: Toggle Task Completion
- [ ] Click checkbox on "Buy groceries" task
- [ ] Verify optimistic update (checkbox changes immediately)
- [ ] Verify success toast appears
- [ ] Verify task shows "Completed" badge
- [ ] Verify title has strike-through styling
- [ ] Click checkbox again to mark incomplete
- [ ] Verify task returns to pending state

#### 2.4: Edit Task
- [ ] Click "Edit" button on a task
- [ ] Verify form appears with current values
- [ ] Change title to "Buy groceries - UPDATED"
- [ ] Change description
- [ ] Press Enter to save (keyboard shortcut)
- [ ] Verify loading spinner on Save button
- [ ] Verify success toast
- [ ] Verify changes appear in task list
- [ ] Edit another task and press Escape to cancel
- [ ] Verify task not changed

#### 2.5: Delete Task
- [ ] Click "Delete" button on a task
- [ ] Verify confirmation dialog appears
- [ ] Cancel deletion
- [ ] Verify task still exists
- [ ] Click "Delete" again and confirm
- [ ] Verify optimistic update (task removed immediately)
- [ ] Verify success toast
- [ ] Verify task no longer in list

### Expected Results:
- ✅ All CRUD operations work correctly
- ✅ Optimistic UI updates feel instant
- ✅ Loading states prevent duplicate actions
- ✅ Toast notifications provide feedback
- ✅ Keyboard shortcuts work (Enter, Escape)

---

## Test Scenario 3: Multi-User Isolation

**Objective**: Verify users cannot access each other's data

### Setup:
- [ ] Two different browsers or incognito windows

### Steps:

#### 3.1: Create Two Users
- **Browser 1 (User A)**:
  - [ ] Sign up as `usera@test.com` / `PasswordA123!`
  - [ ] Create task: "User A Task 1"
  - [ ] Create task: "User A Task 2"
  - [ ] Note task IDs from Network tab (DevTools)

- **Browser 2 (User B)**:
  - [ ] Sign up as `userb@test.com` / `PasswordB123!`
  - [ ] Create task: "User B Task 1"

#### 3.2: Verify Isolation
- **Browser 1 (User A)**:
  - [ ] Verify task list shows only "User A Task 1" and "User A Task 2"
  - [ ] Verify count shows "2 pending, 0 completed"
  - [ ] No "User B" tasks visible

- **Browser 2 (User B)**:
  - [ ] Verify task list shows only "User B Task 1"
  - [ ] Verify count shows "1 pending, 0 completed"
  - [ ] No "User A" tasks visible

#### 3.3: Attempt Cross-User Access (Security Test)
- **Browser 2 (User B)**:
  - [ ] Try to manually access User A's task using DevTools:
    ```javascript
    // In browser console
    fetch('/api/tasks/<user_a_task_id>', {
      headers: { 'Authorization': 'Bearer ' + localStorage.getItem('auth-token') }
    }).then(r => r.json()).then(console.log)
    ```
  - [ ] Verify response is 404 (not 403 - prevents enumeration)
  - [ ] Try to delete User A's task via API
  - [ ] Verify 404 response
  - [ ] Verify User A's tasks still exist in Browser 1

### Expected Results:
- ✅ Complete data isolation between users
- ✅ Cannot access other users' tasks even with known IDs
- ✅ Error responses don't leak information (404 for all unauthorized)

---

## Test Scenario 4: Authentication & Session Management

**Objective**: Test auth flows and token handling

### Steps:

#### 4.1: Logout
- [ ] User logged in with tasks visible
- [ ] Click "Logout" button in header
- [ ] Verify loading spinner on logout button
- [ ] Verify success toast
- [ ] Verify redirect to `/signin`
- [ ] Verify auth token removed from localStorage
- [ ] Try to navigate to `/tasks` manually
- [ ] Verify redirect back to `/signin` (middleware works)

#### 4.2: Sign In (Existing User)
- [ ] On signin page, enter credentials
- [ ] Submit form
- [ ] Verify redirect to `/tasks`
- [ ] Verify previous tasks still visible
- [ ] Verify auth token in localStorage

#### 4.3: Token Expiration (Manual Test)
- [ ] Sign in successfully
- [ ] In DevTools console, manually expire token:
  ```javascript
  localStorage.setItem('auth-token', 'expired.invalid.token')
  ```
- [ ] Refresh page or make API call
- [ ] Verify error toast: "Session expired"
- [ ] Verify redirect to signin
- [ ] Sign in again
- [ ] Verify can access tasks again

#### 4.4: Invalid Credentials
- [ ] Try to sign in with wrong password
- [ ] Verify error message (no sensitive info leak)
- [ ] Try to sign up with existing email
- [ ] Verify appropriate error message

### Expected Results:
- ✅ Logout clears session completely
- ✅ Protected routes redirect to signin when unauthenticated
- ✅ Token expiration handled gracefully
- ✅ Invalid credentials show friendly errors

---

## Test Scenario 5: UI/UX Polish & Accessibility

**Objective**: Test Phase 6 improvements

### Steps:

#### 5.1: Loading States
- [ ] Throttle network to "Slow 3G" in DevTools
- [ ] Create a task
- [ ] Verify loading spinner on submit button
- [ ] Verify button shows "Creating..." text
- [ ] Verify button is disabled during operation
- [ ] Toggle a task
- [ ] Verify checkbox disabled briefly
- [ ] Verify task opacity changes during operation

#### 5.2: Toast Notifications
- [ ] Create task - verify green success toast (top-right)
- [ ] Complete task - verify "Task completed!" toast
- [ ] Delete task - verify "Task deleted successfully" toast
- [ ] Try to create task with empty title - verify red error toast
- [ ] Logout - verify "Logged out successfully" toast
- [ ] Verify toasts auto-dismiss after 2-4 seconds

#### 5.3: Optimistic Updates
- [ ] Throttle network to "Slow 3G"
- [ ] Toggle task completion
- [ ] Verify UI updates IMMEDIATELY (before server response)
- [ ] Simulate network error (DevTools → offline)
- [ ] Try to delete task
- [ ] Verify task removed immediately
- [ ] When network fails, verify task reappears (rollback)
- [ ] Verify error toast shown

#### 5.4: Accessibility (Keyboard Navigation)
- [ ] Use only keyboard (no mouse):
  - [ ] Tab through all interactive elements
  - [ ] Verify focus indicators visible on all elements
  - [ ] Press Enter on "Add Task" button
  - [ ] Tab to checkbox, press Space to toggle
  - [ ] Tab to Edit button, press Enter
  - [ ] Press Escape to cancel edit
  - [ ] Tab to Delete button, press Enter

#### 5.5: Accessibility (Screen Reader)
- [ ] Enable screen reader (VoiceOver on Mac, NVDA on Windows)
- [ ] Navigate task list
- [ ] Verify task titles announced
- [ ] Verify checkbox states announced ("checked" / "unchecked")
- [ ] Verify button labels descriptive ("Delete task: Buy groceries")
- [ ] Verify form labels associated with inputs

### Expected Results:
- ✅ All loading states work correctly
- ✅ Toast notifications provide clear feedback
- ✅ Optimistic updates with rollback work
- ✅ Full keyboard navigation possible
- ✅ Screen reader can understand all elements

---

## Test Scenario 6: Edge Cases & Error Handling

**Objective**: Test unusual scenarios and error conditions

### Steps:

#### 6.1: Empty States
- [ ] New user with no tasks - verify empty state message
- [ ] Create task, then delete all tasks - verify empty state reappears

#### 6.2: Long Content
- [ ] Create task with title exactly 200 characters - should succeed
- [ ] Create task with description exactly 5000 characters - should succeed
- [ ] Verify long description truncated with "..." in list view

#### 6.3: Special Characters
- [ ] Create task with title: `<script>alert('xss')</script>`
- [ ] Verify HTML not executed (XSS prevented)
- [ ] Create task with emojis: "🎉 Party planning 🎊"
- [ ] Verify emojis display correctly

#### 6.4: Network Failures
- [ ] Go offline (DevTools → Network → Offline)
- [ ] Try to create task
- [ ] Verify error toast appears
- [ ] Go back online
- [ ] Retry operation - should succeed

#### 6.5: Concurrent Editing
- [ ] Edit task in one window
- [ ] Delete same task in another window
- [ ] Verify graceful error handling

### Expected Results:
- ✅ Empty states handled correctly
- ✅ Long content truncated appropriately
- ✅ XSS attacks prevented
- ✅ Network errors handled gracefully

---

## Test Scenario 7: Cross-Browser & Responsive Testing

**Objective**: Verify compatibility across browsers and devices

### Browsers to Test:
- [ ] **Chrome** (latest): All features work
- [ ] **Firefox** (latest): All features work
- [ ] **Safari** (latest): All features work
- [ ] **Edge** (latest): All features work

### Responsive Design:
- [ ] **Mobile (375px)**:
  - [ ] Layout adapts to small screen
  - [ ] All buttons accessible
  - [ ] Forms usable on mobile
  - [ ] Touch targets adequate size

- [ ] **Tablet (768px)**:
  - [ ] Layout optimal for tablet
  - [ ] Multi-column if appropriate

- [ ] **Desktop (1920px)**:
  - [ ] Content centered and max-width constrained
  - [ ] No excessive whitespace

### Expected Results:
- ✅ All browsers show consistent behavior
- ✅ Responsive design works on all screen sizes

---

## Test Scenario 8: Performance

**Objective**: Verify performance meets requirements

### Steps:

#### 8.1: Page Load
- [ ] Clear cache
- [ ] Load `/tasks` page
- [ ] Verify initial load < 2 seconds (with 100 tasks)
- [ ] Check Network tab: minimize requests, no errors

#### 8.2: Task Operations
- [ ] Create task - verify completes < 1 second
- [ ] Toggle task - verify completes < 1 second
- [ ] Delete task - verify completes < 1 second

#### 8.3: Large Dataset
- [ ] Create 100 tasks (use API or loop)
- [ ] Verify list still loads < 2 seconds
- [ ] Verify scrolling smooth
- [ ] Verify operations still fast

### Expected Results:
- ✅ Page loads meet performance targets
- ✅ Operations feel instant with optimistic updates
- ✅ App remains responsive with large dataset

---

## Critical Bugs Checklist

**Must-Fix Issues** (block release if found):
- [ ] User can access another user's tasks
- [ ] Auth tokens leaked in console or visible in UI
- [ ] XSS vulnerability (script execution)
- [ ] SQL injection possible
- [ ] Data loss on error (no rollback)
- [ ] App crashes or shows error page
- [ ] Cannot sign up or sign in
- [ ] Cannot create or view tasks

**Should-Fix Issues** (fix if time permits):
- [ ] Confusing error messages
- [ ] Slow performance (> 2 seconds)
- [ ] Missing accessibility features
- [ ] Poor mobile experience

---

## Test Execution Log

| Scenario | Date | Tester | Browser | Status | Notes |
|----------|------|--------|---------|--------|-------|
| 1 - Signup | | | | ⏳ PENDING | |
| 2 - CRUD | | | | ⏳ PENDING | |
| 3 - Isolation | | | | ⏳ PENDING | |
| 4 - Auth | | | | ⏳ PENDING | |
| 5 - UX | | | | ⏳ PENDING | |
| 6 - Edge Cases | | | | ⏳ PENDING | |
| 7 - Cross-Browser | | | | ⏳ PENDING | |
| 8 - Performance | | | | ⏳ PENDING | |

---

## Automated Test Coverage Summary

**Backend Tests**:
- Unit tests: ✅ Models, JWT validation
- Integration tests: ✅ All API endpoints
- Multi-user tests: ✅ Data isolation

**Frontend Tests**:
- Component tests: ⏳ To be implemented

**Total E2E Manual Tests**: 8 scenarios, ~100 test steps

---

**CHECKPOINT 7 Requirements**:
- ✅ All backend tests written and passing
- ✅ Multi-user isolation verified
- ⏳ E2E scenarios documented (this file)
- ⏳ Manual testing in progress

**Next Steps**:
1. Run pytest for backend tests
2. Execute E2E manual tests
3. Document results in log table above
4. Fix any critical bugs found
5. Mark CHECKPOINT 7 as complete
