# Main Window Launch Fix Bugfix Design

## Overview

The bug prevents the main application window from launching after successful authentication. When a user logs in or continues as guest through the login GUI, the main window should appear but doesn't. The issue has two root causes: (1) an incorrect import path in `main_with_login.py` that tries to import from `main` but should import from `src.main`, and (2) the callback execution timing where the login window is destroyed before the callback can properly launch the main window. The fix will correct the import path and ensure proper callback execution after window destruction.

## Glossary

- **Bug_Condition (C)**: The condition that triggers the bug - when authentication completes successfully (login or guest mode) and the callback should launch the main window
- **Property (P)**: The desired behavior when authentication completes - the main window should launch and be visible to the user
- **Preservation**: Existing authentication UI behavior (login/signup flow, error handling, skip login) that must remain unchanged by the fix
- **handle_login_success**: The callback function in `main_with_login.py` that is invoked after successful authentication to launch the main app
- **show_login**: The function in `login_gui.py` that displays the login window and accepts an `on_success` callback
- **on_login_success**: The callback parameter passed to the LoginWindow class that should be executed after authentication

## Bug Details

### Bug Condition

The bug manifests when a user successfully authenticates (either by logging in or continuing as guest) and the login window closes. The `handle_login_success` callback is either not being executed properly due to window destruction timing, or the import of the main application fails due to an incorrect module path, or both.

**Formal Specification:**
```
FUNCTION isBugCondition(input)
  INPUT: input of type AuthenticationEvent
  OUTPUT: boolean
  
  RETURN (input.authenticationSuccessful == true)
         AND (input.loginWindowDestroyed == true)
         AND (input.callbackProvided == handle_login_success)
         AND NOT mainWindowLaunched()
END FUNCTION
```

### Examples

- **Successful Login**: User enters valid credentials, clicks "Login", sees success message, login window closes, but main window never appears
- **Continue as Guest**: User clicks "Continue Without Login", confirms the dialog, login window closes, but main window never appears  
- **Successful Signup then Login**: User creates account, switches to login tab, logs in successfully, sees welcome message, login window closes, but main window never appears
- **Edge Case - Window Close**: User logs in successfully but closes the window during the success message - main window should still launch after window destruction completes

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- Login form validation and error messages must continue to work exactly as before
- Signup form validation and account creation must remain unchanged
- "Continue Without Login" confirmation dialog must remain unchanged
- Authentication manager integration (login/signup/remember me) must remain unchanged
- Success/error message boxes must continue to display as before
- Window centering and UI layout must remain unchanged
- Tab switching between Login and Sign Up must remain unchanged

**Scope:**
All inputs that do NOT involve the successful completion of authentication should be completely unaffected by this fix. This includes:
- Failed login attempts (wrong password, non-existent user)
- Failed signup attempts (validation errors, duplicate username)
- User canceling the "Continue Without Login" dialog
- Window close events before authentication completion
- All authentication UI interactions and validations

## Hypothesized Root Cause

Based on the bug description, the most likely issues are:

1. **Incorrect Import Path**: The `main_with_login.py` file attempts to import with `from main import main as run_original_app` but the correct path should be `from src.main import main as run_original_app` since main.py is located in the src directory, not the root directory

2. **Callback Execution Timing**: The `LoginWindow.destroy()` method is called before the callback executes, which may cause the callback to fail or not execute at all due to the window's event loop terminating

3. **Callback Not Invoked After Destroy**: The callback is passed to the window but when `self.destroy()` is called in `_handle_login` and `_skip_login`, the callback is invoked immediately after, but the window destruction may interfere with the callback's ability to create new windows

4. **Missing Error Handling**: If the import fails, there's no visible error message to the user - the application silently fails to launch

## Correctness Properties

Property 1: Bug Condition - Main Window Launches After Authentication

_For any_ authentication event where the user successfully completes authentication (login or guest mode) and the login window is destroyed, the fixed code SHALL successfully import the main application module and launch the main GUI window, making it visible to the user.

**Validates: Requirements 2.1, 2.2**

Property 2: Preservation - Authentication UI Behavior

_For any_ user interaction that does NOT result in successful authentication completion (failed logins, failed signups, canceled dialogs, validation errors), the fixed code SHALL produce exactly the same behavior as the original code, preserving all existing authentication UI functionality, error handling, and validation.

**Validates: Requirements 3.1, 3.2, 3.3**

## Fix Implementation

### Changes Required

Assuming our root cause analysis is correct:

**File**: `main_with_login.py`

**Function**: `handle_login_success` and the import statement within it

**Specific Changes**:
1. **Fix Import Path**: Change the import statement from `from main import main as run_original_app` to `from src.main import main as run_original_app`
   - This corrects the module path to match the actual file structure where main.py is in the src directory
   - The try-except block should catch ImportError and provide a clear error message

2. **Use after_idle for Callback Execution**: Modify the callback invocation in `login_gui.py` to use `self.after_idle()` before destroying the window
   - This ensures the callback is scheduled on the event queue before window destruction
   - Prevents race conditions between window destruction and callback execution

3. **Alternative: Delay Destroy Call**: Instead of calling `self.destroy()` immediately, schedule it after the callback
   - Use `self.after(100, self.destroy)` to give callback time to execute
   - This ensures callback completes before window cleanup

4. **Add Error Handling**: Wrap the main app launch in better error handling
   - Display error message if import fails
   - Show traceback for debugging purposes
   - Provide clear user feedback instead of silent failure

5. **Store Callback Result**: Ensure the callback is properly invoked after window is closed
   - Move callback invocation to happen after `self.destroy()` completes
   - Or use `self.quit()` instead of `self.destroy()` to exit mainloop without destroying window immediately

## Testing Strategy

### Validation Approach

The testing strategy follows a two-phase approach: first, surface counterexamples that demonstrate the bug on unfixed code, then verify the fix works correctly and preserves existing behavior.

### Exploratory Bug Condition Checking

**Goal**: Surface counterexamples that demonstrate the bug BEFORE implementing the fix. Confirm or refute the root cause analysis. If we refute, we will need to re-hypothesize.

**Test Plan**: Write automated tests that simulate successful authentication scenarios and verify that the main window actually launches. Run these tests on the UNFIXED code to observe failures and understand the root cause.

**Test Cases**:
1. **Successful Login Test**: Simulate valid login credentials, submit login form, verify main window appears (will fail on unfixed code - import error or callback not executing)
2. **Guest Mode Test**: Simulate clicking "Continue Without Login" and confirming dialog, verify main window appears (will fail on unfixed code)
3. **Import Path Test**: Attempt to import `from main import main` and verify it fails with ImportError, then attempt `from src.main import main` and verify it succeeds (will demonstrate the import path issue)
4. **Callback Timing Test**: Monitor callback execution during window destroy event to see if callback is invoked (may reveal timing issue on unfixed code)

**Expected Counterexamples**:
- ImportError: "No module named 'main'" when trying to import the main application
- Main window never appears after authentication success message
- Possible causes: incorrect import path, callback not executing after destroy, window destruction preventing new window creation

### Fix Checking

**Goal**: Verify that for all inputs where the bug condition holds, the fixed function produces the expected behavior.

**Pseudocode:**
```
FOR ALL input WHERE isBugCondition(input) DO
  result := authenticateAndLaunch_fixed(input)
  ASSERT mainWindowLaunched(result)
  ASSERT mainWindowVisible(result)
END FOR
```

### Preservation Checking

**Goal**: Verify that for all inputs where the bug condition does NOT hold, the fixed function produces the same result as the original function.

**Pseudocode:**
```
FOR ALL input WHERE NOT isBugCondition(input) DO
  ASSERT authenticateAndLaunch_original(input) = authenticateAndLaunch_fixed(input)
END FOR
```

**Testing Approach**: Property-based testing is recommended for preservation checking because:
- It generates many test cases automatically across the input domain (invalid credentials, validation errors, edge cases)
- It catches edge cases that manual unit tests might miss (special characters, empty fields, SQL injection attempts)
- It provides strong guarantees that behavior is unchanged for all authentication failure paths

**Test Plan**: Observe behavior on UNFIXED code first for authentication failures and UI interactions, then write property-based tests capturing that behavior.

**Test Cases**:
1. **Failed Login Preservation**: Observe that incorrect credentials show error message on unfixed code, then write test to verify this continues after fix
2. **Failed Signup Preservation**: Observe that validation errors (weak password, invalid email, duplicate username) show appropriate errors on unfixed code, then write test to verify this continues after fix
3. **Cancel Dialog Preservation**: Observe that canceling "Continue Without Login" dialog keeps login window open on unfixed code, then write test to verify this continues after fix
4. **UI Interaction Preservation**: Observe that tab switching, form field validation, and visual feedback work correctly on unfixed code, then write tests to verify this continues after fix

### Unit Tests

- Test import path correction - verify `from src.main import main` works correctly
- Test callback execution after window destroy - verify callback is invoked
- Test main window launches with valid user object
- Test main window launches with None user object (guest mode)
- Test error handling when import fails
- Test that success messages display before window closes

### Property-Based Tests

- Generate random valid authentication scenarios (different usernames, login vs guest) and verify main window always launches
- Generate random invalid authentication inputs (wrong passwords, validation failures) and verify authentication UI behavior is preserved
- Test across many window state transitions to ensure callback always executes correctly

### Integration Tests

- Test full authentication flow: open login window → enter credentials → click login → verify success message → verify login window closes → verify main window appears
- Test guest flow: open login window → click continue without login → confirm dialog → verify login window closes → verify main window appears  
- Test that authenticated user data is properly passed to main application through `builtins.CURRENT_USER`
- Test switching between tabs, signup, then login, then main window launch
