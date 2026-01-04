To utilize this:
* Install Python from python.org
* Download the chromedriver file from here: https://googlechromelabs.github.io/chrome-for-testing/#stable
** You'll need to download the appropriate type based on your computer and processor (Macs are USUALLY x64, FWIW)

Create a new folder on your computer and copy the chromedriver file there

Open a Terminal and navigate to that folder

Install the dependencies for the script using pip: pip install selenium docx csv
* If you ever hit an error that say Module Not Found or something, you should be able to add it using this same command; you just need to update the module name.

In your terminal, run "python bloodworks-web-scraper.py"
* The end date is 30 days from today by default. If you want to specify the date instead, add the date in the MM/DD/YYYY format, e.g. "python bloodworks-web-scraper.py 11/30/2025"

This will create a word doc for you and you can post to Slack accordingly. I have noticed that Slack has a 4000 character limit, so you have to do it in a few posts.
