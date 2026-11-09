# Implementation Plan

## Overview

This implementation plan addresses the main window launch bug that prevents the Business Plan Generator GUI from opening after successful authentication. The fix involves correcting the import path in `main_with_login.py`, ensuring proper callback timing in `login_gui.py`, and adding robust error handling.

## Bug Condition Analysis

**Bug Condition (C(X))**: The main window fails to launch after successful authentication
- Input triggers bug when: User completes login/signup/skip action in authentication window
- Defective behavior: `handle_login_success()` callback attempts incorrect import path
- Root cause: Import statement `from main import main` fails because `main.py` is in `src/` directory, not root

**Expected Behavior (P(result))**: After authentication, main GUI window opens immediately
- Property 1: GUI window appears after successful login
- Property 2: GUI window appears after successful signup  
- Property 3: GUI window appears after "skip login" action

**Preservation Requirements (¬C(X))**: Behaviors that must remain unchanged
- Failed login attempts should keep login window open with error message
- Failed signup attempts should keep login window open with error message
- Direct launch via `src/main.py` should continue working
- User context should be stored in `builtins.CURRENT_USER`

---

## Task Dependency Graph

```
1 (Bug Condition Exploration Test)
    ↓
2 (Preservation Property Tests)
    ↓
3 (Fix Implementation)
    ├─ 3.1 (Fix import path)
    ├─ 3.2 (Fix callback timing)
    ├─ 3.3 (Add error handling)
    ├─ 3.4 (Verify exploration test passes)
    └─ 3.5 (Verify preservation tests pass)
    ↓
4 (Manual Testing)
    ├─ 4.1 (Login flow)
    ├─ 4.2 (Signup flow)
    ├─ 4.3 (Skip login flow)
    ├─ 4.4 (Failed auth)
    ├─ 4.5 (Direct launch)
    └─ 4.6 (Window close)
    ↓
5 (Checkpoint)
```

```json
{
  "waves": [
    {
      "name": "Wave 1: Exploration Test",
      "tasks": ["1"]
    },
    {
      "name": "Wave 2: Preservation Tests",
      "tasks": ["2"]
    },
    {
      "name": "Wave 3: Implementation",
      "tasks": ["3.1", "3.2", "3.3"]
    },
    {
      "name": "Wave 4: Verification",
      "tasks": ["3.4", "3.5"]
    },
    {
      "name": "Wave 5: Manual Testing",
      "tasks": ["4.1", "4.2", "4.3", "4.4", "4.5", "4.6"]
    },
    {
      "name": "Wave 6: Checkpoint",
      "tasks": ["5"]
    }
  ]
}
```

**Critical Path**: Tasks 1 → 2 → 3.1 → 3.2 → 3.3 → 3.4 → 3.5 → 4.* → 5

**Dependencies**:
- Task 2 depends on Task 1 (exploration test must be written first)
- Task 3 depends on Tasks 1 and 2 (tests must exist before implementation)
- Tasks 3.4 and 3.5 depend on 3.1, 3.2, 3.3 (implementation must be complete before verification)
- Task 4 depends on Task 3 (fix must be implemented before manual testing)
- Task 5 depends on Task 4 (all tests must pass before checkpoint)

## Tasks

## Implementation Tasks

- [ ] 1. Write bug condition exploration test
  - **Property 1: Bug Condition** - Main Window Launch After Authentication
  - **CRITICAL**: This test MUST FAIL on unfixed code - failure confirms the bug exists
  - **DO NOT attempt to fix the test or the code when it fails**
  - **NOTE**: This test encodes the expected behavior - it will validate the fix when it passes after implementation
  - **GOAL**: Surface counterexamples that demonstrate the main window launch failure
  - **Scoped PBT Approach**: Test all three authentication flows (login, signup, skip) to ensure reproducibility
  - Create test file: `tests/test_main_window_launch.py`
  - Test that after successful login, the main GUI window launches (from Bug Condition 1.1)
  - Test that after successful signup, the main GUI window launches (from Bug Condition 1.2)
  - Test that after "skip login", the main GUI window launches (from Bug Condition 1.3)
  - Test implementation: Mock the authentication flow, trigger callback, verify GUI window creation
  - The test assertions should match the Expected Behavior (2.1, 2.2, 2.3)
  - Run test on UNFIXED code
  - **EXPECTED OUTCOME**: Test FAILS due to ImportError "No module named 'main'" (this is correct - it proves the bug exists)
  - Document counterexamples: ImportError when attempting `from main import main`
  - Mark task complete when test is written, run, and failure is documented
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3_

- [ ] 2. Write preservation property tests (BEFORE implementing fix)
  - **Property 2: Preservation** - Authentication Error Handling and Direct Launch
  - **IMPORTANT**: Follow observation-first methodology
  - Observe behavior on UNFIXED code for non-buggy cases
  - Test that failed login keeps window open with error (from Preservation 3.1)
  - Test that failed signup keeps window open with error (from Preservation 3.2)
  - Test that closing login window without action exits gracefully (from Preservation 3.3)
  - Test that direct launch via `src/main.py` works without authentication (from Preservation 3.4)
  - Test that user info is stored in `builtins.CURRENT_USER` after auth (from Preservation 3.5)
  - Test that welcome messages display correctly in console (from Preservation 3.6)
  - Write property-based tests capturing observed behavior patterns
  - Property-based testing generates many test cases for stronger guarantees
  - Run tests on UNFIXED code
  - **EXPECTED OUTCOME**: Tests PASS (this confirms baseline behavior to preserve)
  - Mark task complete when tests are written, run, and passing on unfixed code
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [ ] 3. Fix main window launch after authentication

  - [ ] 3.1 Fix import path in `main_with_login.py`
    - Change `from main import main as run_original_app` to `from src.main import main as run_original_app` (line 59)
    - Ensure the sys.path manipulation at the top of the file allows this import
    - Verify that `src/main.py` has the correct `main()` function that launches GUI
    - _Bug_Condition: isBugCondition(input) where user completes any authentication action_
    - _Expected_Behavior: After authentication, callback successfully imports and executes src.main.main()_
    - _Preservation: Failed authentication attempts must continue showing errors without launching GUI_
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4_

  - [ ] 3.2 Fix callback timing in `login_gui.py`
    - Review `_handle_login()` method in `src/auth/login_gui.py` (line 159)
    - Review `_skip_login()` method in `src/auth/login_gui.py` (line 178)
    - Ensure `self.destroy()` is called BEFORE the callback `self.on_login_success()`
    - Verify callback is executed after login window destruction completes
    - Use `self.after()` or proper event scheduling if needed to ensure GUI cleanup completes
    - _Bug_Condition: Callback timing issues may prevent main window from displaying_
    - _Expected_Behavior: Login window closes completely before main window launches_
    - _Preservation: Login window must remain open on authentication failures_
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2_

  - [ ] 3.3 Add error handling for main window launch
    - Wrap the GUI launch in `handle_login_success()` with try-except blocks
    - Catch ImportError specifically for debugging import path issues
    - Catch general Exception for other GUI launch failures
    - Display user-friendly error message if main window fails to launch
    - Log detailed error information for debugging
    - Provide fallback message suggesting direct launch via `src/main.py`
    - _Bug_Condition: Unhandled exceptions may cause silent failures_
    - _Expected_Behavior: Users see clear error messages if launch fails_
    - _Preservation: Existing error handling for authentication must be preserved_
    - _Requirements: 2.4, 3.1, 3.2, 3.3_

  - [ ] 3.4 Verify bug condition exploration test now passes
    - **Property 1: Expected Behavior** - Main Window Launch After Authentication
    - **IMPORTANT**: Re-run the SAME test from task 1 - do NOT write a new test
    - The test from task 1 encodes the expected behavior
    - When this test passes, it confirms the expected behavior is satisfied
    - Run bug condition exploration test from step 1
    - Verify all three authentication flows (login, signup, skip) successfully launch main GUI
    - Verify no ImportError occurs
    - Verify GUI window is created and visible
    - **EXPECTED OUTCOME**: Test PASSES (confirms bug is fixed)
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

  - [ ] 3.5 Verify preservation tests still pass
    - **Property 2: Preservation** - Authentication Error Handling and Direct Launch
    - **IMPORTANT**: Re-run the SAME tests from task 2 - do NOT write new tests
    - Run preservation property tests from step 2
    - Verify failed login still shows error and keeps window open
    - Verify failed signup still shows error and keeps window open
    - Verify closing without action still exits gracefully
    - Verify direct launch via `src/main.py` still works
    - Verify user context storage still works
    - Verify console messages still display correctly
    - **EXPECTED OUTCOME**: Tests PASS (confirms no regressions)
    - Confirm all tests still pass after fix (no regressions)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [ ] 4. Test all authentication flows work correctly

  - [ ] 4.1 Manual test: Login flow
    - Start application via `run_with_login.bat` or `python main_with_login.py`
    - Enter valid credentials and click "Login"
    - Verify login window closes
    - Verify main Business Plan Generator GUI window opens
    - Verify user can interact with the GUI (select mode, fill forms, etc.)
    - Verify user info is accessible if needed
    - _Requirements: 2.1, 2.2, 3.5_

  - [ ] 4.2 Manual test: Signup then login flow
    - Start application via `run_with_login.bat` or `python main_with_login.py`
    - Switch to "Sign Up" tab
    - Create new account with valid information
    - Verify success message and switch to login tab
    - Enter credentials and click "Login"
    - Verify login window closes
    - Verify main Business Plan Generator GUI window opens
    - _Requirements: 2.2, 3.2_

  - [ ] 4.3 Manual test: Skip login flow
    - Start application via `run_with_login.bat` or `python main_with_login.py`
    - Click "Continue Without Login"
    - Confirm the dialog
    - Verify login window closes
    - Verify main Business Plan Generator GUI window opens in guest mode
    - Verify application functions normally
    - _Requirements: 2.3, 3.3_

  - [ ] 4.4 Manual test: Failed authentication preserves login window
    - Start application via `run_with_login.bat` or `python main_with_login.py`
    - Enter invalid credentials
    - Click "Login"
    - Verify error message appears
    - Verify login window REMAINS OPEN
    - Verify main GUI window does NOT open
    - Try signup with existing username
    - Verify error message appears
    - Verify login window REMAINS OPEN
    - _Requirements: 3.1, 3.2_

  - [ ] 4.5 Manual test: Direct launch still works
    - Start application via `run_app.bat` or `python src/main.py`
    - Verify main Business Plan Generator GUI opens directly
    - Verify no authentication window appears
    - Verify application functions normally
    - _Requirements: 3.4_

  - [ ] 4.6 Manual test: Window close behavior
    - Start application via `run_with_login.bat` or `python main_with_login.py`
    - Close the login window using the X button without logging in
    - Verify application exits gracefully with "Login cancelled" message
    - Verify no errors or exceptions occur
    - _Requirements: 3.3_

- [ ] 5. Checkpoint - Ensure all tests pass
  - Ensure all automated tests pass (exploration test and preservation tests)
  - Ensure all manual test scenarios complete successfully
  - Verify no regressions in existing functionality
  - Document any edge cases discovered during testing
  - Ask the user if questions arise

## Notes

### Test Files Location
- Create test directory: `tests/` in project root if it doesn't exist
- Exploration test: `tests/test_main_window_launch.py`
- Preservation tests: `tests/test_auth_preservation.py`

### Key Files to Modify
- `main_with_login.py` (line 59): Fix import statement
- `src/auth/login_gui.py` (lines 159, 178): Review callback timing
- `main_with_login.py` (lines 45-65): Add error handling in `handle_login_success()`

### Testing Strategy
- **Property 1 (Bug Condition)**: Tests that authentication triggers main window launch
- **Property 2 (Preservation)**: Tests that error handling and alternative flows remain unchanged
- Manual testing validates real user workflows end-to-end

### Success Criteria
- All automated tests pass (exploration + preservation)
- All manual test scenarios complete successfully
- No regressions in authentication or direct launch workflows
- Clear error messages if any failures occur

