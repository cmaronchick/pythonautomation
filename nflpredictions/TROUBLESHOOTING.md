# predictions-scraper.py Troubleshooting Guide

## Overview
This document describes the improvements made to fix hanging issues in `predictions-scraper.py` and related scraper modules.

## Problems Identified

1. **Short timeout values**: WebDriverWait timeouts were set to only 2 seconds, causing premature failures
2. **No page load timeouts**: Driver instances didn't have explicit page load timeout protection
3. **Inadequate error handling**: Many driver.get() calls lacked timeout exception handling
4. **Improper driver cleanup**: Using driver.close() instead of driver.quit() left processes hanging
5. **Global driver instances**: Some scrapers used global drivers that weren't properly managed
6. **No error isolation**: Failures in one scraper would stop all subsequent scrapers

## Solutions Implemented

### 1. Increased Timeout Values
- Changed all `WebDriverWait(driver, timeout=2)` to `WebDriverWait(driver, timeout=10)`
- Added `driver.set_page_load_timeout(35)` to all driver instances
- This gives pages adequate time to load without hanging indefinitely

### 2. Enhanced Error Handling
- Added try-except blocks around all `driver.get()` calls in main script
- Added TimeoutException and WebDriverException catching
- Added individual try-except blocks for each scraper function call
- Errors are logged but don't stop the entire process

### 3. Proper Driver Cleanup
- Changed all `driver.close()` to `driver.quit()` across all modules
- Added finally block to ensure CSV writing happens even on errors
- Ensured drivers are quit in both success and exception paths

### 4. Fixed Global Driver Issues
- Removed global driver instance in scraper_usatoday.py
- Each scraper function now creates and manages its own driver

### 5. Error Logging
- Added print statements identifying which scraper is being executed
- Errors are appended to the errors array with source identification
- Failed scrapers don't prevent other scrapers from running

## Files Modified

1. `predictions-scraper.py` - Main script with comprehensive error handling
2. `scraper_espn.py` - Timeout improvements
3. `scraper_nfl.py` - Timeout improvements
4. `scraper_dratings.py` - Timeout improvements
5. `scraper_usatoday.py` - Fixed global driver, timeout improvements
6. `scraper_clutchpoints.py` - Timeout improvements
7. `scraper_oddsshark.py` - Timeout improvements
8. `scraper_oddstrader.py` - Timeout improvements
9. `scraper_nflspinzone.py` - Timeout improvements
10. `scraper_sbr.py` - Timeout improvements
11. `scraper_copilot.py` - Timeout improvements
12. `scraper_rotowire.py` - Timeout improvements

## Usage

Run the script as before:
```bash
python predictions-scraper.py <week_number> <year> <season>
```

Example:
```bash
python predictions-scraper.py 16 2025 reg
```

## Monitoring

When running the script, you should see:
1. Progress messages for each scraper: "Fetching ESPN data...", etc.
2. Error messages if a scraper fails (but script continues)
3. Final CSV output with all successful predictions

## What to Watch For

### Normal Behavior
- Some scrapers may take 10-30 seconds to complete
- Error messages for specific scrapers that fail
- CSV file is created even if some scrapers fail
- Script completes within a reasonable time (< 10 minutes typically)

### Problematic Behavior
- Script hangs for more than 2-3 minutes on a single scraper
- No progress messages being printed
- Chrome/ChromeDriver processes accumulating in the background
- Memory usage steadily increasing

## If Hangs Still Occur

1. **Check which scraper is hanging**: Look at the last printed message
2. **Verify ChromeDriver**: Ensure ChromeDriver is compatible with your Chrome version
3. **Check network connectivity**: Some websites may be slow or unreachable
4. **Increase timeout values**: If consistently timing out, increase from 35s to 60s
5. **Run individual scrapers**: Test problematic scrapers in isolation
6. **Check website changes**: Websites may have changed structure, breaking the scraper

## Testing Individual Scrapers

Each scraper module can be run independently:
```bash
python scraper_espn.py <week_number>
python scraper_nfl.py <week_number>
# etc.
```

## Additional Improvements Considered

For future enhancements, consider:
1. Adding a timeout decorator that works with Selenium operations
2. Implementing retry logic for failed scrapers
3. Adding parallel execution with proper process management
4. Creating a configuration file for timeout values
5. Adding health checks for websites before scraping
6. Implementing better logging with timestamps and log levels
