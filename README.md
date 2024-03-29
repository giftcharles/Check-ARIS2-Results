# Check ARIS2 Results
Periodically check for results update published on the ARIS website for any given account/student


# How to use

1. Create `credentials.py` file.
2. Add three variables, `__username__`, `__password__`, `__headless__` and `__waittime__`.
3. The `__username__` variable takes your ARIS2 ID as a value, the `__password__` variable obviously takes your password, the `__waittime__` variable takes an integer that defines the amount of time to wait between each check, specified in seconds and the `__headless__` variable takes a `0` or a `1`, when set to `0` it will show the automated browser while checking for results and it will not show it when set to `1`, if you do not set it the default is `1`.
4. Use `0` as a value for `__waittime__` to make the script wait at a random interval between 12 and 24 hours until the next check.
5. Run `ARIS2Results.py` to start the checks.

When the script finds your results they will be automatically downloaded into `full_results.html`.

# Requirements

1. Python 3.x
2. Chromedriver
3. Chrome Browser
