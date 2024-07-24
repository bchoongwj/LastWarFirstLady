# LastWarFirstLady
Automator for First Lady

Make sure to download the required libraries!

How to use:
Run this script on computer, with Last War game open to the secretary page

Description:
Script has a 3 second delay before starting to let users switch windows
For the 1st run, it will check each position at 1 minute intervals (each position has its own timer)
Upon being able to appoint someone, it will scroll to the top of the list, and appoint the next person
After that, a 5 minute timer will start for that position. Each secretary position will have its own independent timer

How it works:
Script scans for images to find and click

Shortcomings:
Script takes about 15 seconds to appoint someone in each position. Wastes about a minute for each cycle of appointment
Script could make use of icon that shows when a new person has applied instead of periodically opening each position and checking
Faster scrolling of the applicants list would be good
Missing some failsafe exception cases
