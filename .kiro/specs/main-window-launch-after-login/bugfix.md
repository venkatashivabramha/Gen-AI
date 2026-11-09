# Bugfix Requirements Document

## Introduction

After successful login or signup in the authentication window (`main_with_login.py`), the main Business Plan Generator GUI window fails to open. Users see the success message ("Welcome back, username!") and the login window closes, but the main application window does not appear. The process either exits silently or hangs, preventing users from accessing the business plan generation functionality.

This bug affects all users attempting to use the application through the `main_with_login.py` entry point, making the authentication wrapper effectively non-functional.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN user successfully logs in through the authentication window THEN the login window closes but the main Business Plan Generator GUI window does not appear

1.2 WHEN user successfully signs up and logs in through the authentication window THEN the login window closes but the main Business Plan Generator GUI window does not appear

1.3 WHEN user selects "Continue Without Login" and confirms THEN the login window closes but the main Business Plan Generator GUI window does not appear

1.4 WHEN `handle_login_success()` callback executes in `main_with_login.py` THEN the system fails to launch the main GUI due to incorrect import path for `src/main.py`

### Expected Behavior (Correct)

2.1 WHEN user successfully logs in through the authentication window THEN the system SHALL close the login window and immediately open the main Business Plan Generator GUI window

2.2 WHEN user successfully signs up and logs in through the authentication window THEN the system SHALL close the login window and immediately open the main Business Plan Generator GUI window with the authenticated user context

2.3 WHEN user selects "Continue Without Login" and confirms THEN the system SHALL close the login window and immediately open the main Business Plan Generator GUI window in guest mode

2.4 WHEN `handle_login_success()` callback executes in `main_with_login.py` THEN the system SHALL correctly import and execute the main application entry point from `src/main.py`

### Unchanged Behavior (Regression Prevention)

3.1 WHEN user enters invalid credentials in the login window THEN the system SHALL CONTINUE TO display "Login Failed" error message without closing the login window

3.2 WHEN user attempts to sign up with existing username or email THEN the system SHALL CONTINUE TO display "Signup Failed" error message without closing the login window

3.3 WHEN user closes the login window without logging in or signing up THEN the system SHALL CONTINUE TO exit gracefully with "Login cancelled. Exiting..." message

3.4 WHEN the main application is launched directly via `src/main.py` without authentication THEN the system SHALL CONTINUE TO function normally and display the Business Plan Generator GUI

3.5 WHEN user successfully authenticates THEN the system SHALL CONTINUE TO store user info in `builtins.CURRENT_USER` for access by the main application

3.6 WHEN user successfully authenticates THEN the system SHALL CONTINUE TO display welcome messages in the console with username and email information
