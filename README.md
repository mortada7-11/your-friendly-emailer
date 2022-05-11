# your-friendly-emailer


this will be a script for sending HTML emails in bulk using SMTP and MIME.

<h3>Notice :</h3>
As it stands right now, the script only support Gmail accounts.
Since it support only Username/Password pair login, you are required to allow less secure apps in your account :
      1. Go to your Google account settings.
      2. Search for "Less secure apps" in the search box.
      3. Turn "Allow less secure apps" on.

<h2>option 1: Sending a single email</h2>
You will provide the recipient, subject, message, HTML file path when it prompt you.

<h2>option 2: Sending multiple emails</h2>
You will provide the subject, message, HTML file path, CSV file path when it prompt you.
The CSV scheme is configured as '''email,fullname'''.
