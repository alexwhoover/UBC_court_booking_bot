# UBC_court_booking_bot
An automated bot to book UBC tennis courts when they open.

# Libraries
This bot's web automation has been built using the Playwright library.
Browser fingerprint injection with browserforge.
Realistic mouse movement with python_ghost_cursor (Python 3.12 or earlier only)

# Notes
Must log-in to UBC CWL beforehand on chrome browser, accept 2FA with DUO, then choose "This is my device." This should ensure that process can be completely automated without a DUO push notification.
