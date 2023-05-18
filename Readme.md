## Indian Recruiter Spam Filter

### An unfinished project to filter emails from Indian spammers

Recruiters in India search the internet, collecting email addresses associated with the CVs/resumes/web pages of software developers. Then, when they have a requirement for a job, they email all the emails with that requirement. Your resume might clearly state that you are only interested in Java positions in East London, and not mention the Python programming language, but you will receive a dozen emails from different recruiters about a Python position in Plano, Texas.

The purpose of this Python program, classify.py, is to generate a JavaScript program which automatically moves emails from Indian spammers to a folder called "IndianRecruiterSpam".

It uses lists of Indian names and phrases taken from Indian spam emails, such as "below mention details", and uses the rule

#### If there are two or more Indian names and one or more Indian phrases, OR there are two or more phrases and one or more Indian names, it's spam, so move it to folder IndianRecruiterSpam (you have to create this "label" in your own GMail)

The Python program classify.py generates JavaScript program MessageView.js, which, when integrated into GMail using InboxSDK, 

https://inboxsdk.github.io/inboxsdk-docs/

is supposed to interrogate all incoming emails, and if they are Indian recruiter spam, move them into folder IndianRecruiterSpam. 


##### Problems include:

- the difficulty of importing files into JavaScript programs, eg. names.csv, the list of Indian names

- the work of creating a realistic 'test set'
-- it should be possible to give the program a long list of emails which are not spam, another list which is spam, watch how it classifies incoming emails, and when it makes a mistake, add the misclassified email to one of the lists, and it will learn

- complexity of some phrases, e.g. "hiring on w2 ui developer position". This should be
"hiring on %s position", where anything can be substituted for %s.

- the difficulty of writing ML code in JavaScript. It would take far too long, and wouldn't perform. The code for detecting that an email from "John Walters" is Indian recruiter spam has to be written in Python. It is possible to include Python code in a page with JavaScript in it, but I haven't found out how to incorporate it into this GMail app program. 

See https://pyscript.net/alpha/pyscript.js

- as a result, I had to write Python to do the Machine Learning, then translate what it learned into JavaScript, then produce a JavaScript file, which can be loaded into Chrome via chrome://extensions/ https://developer.chrome.com/docs/extensions/mv3/getstarted/ and InboxSDK https://inboxsdk.github.io/inboxsdk-docs/

- currently, all classify.py does is 
-- test itself by finding how many of data/spam* are wrongly classified as not spam, and how many of data/not-spam* are wrongly classified as spam
-- insert the latest list of Indian names and phrases I have copied from recruiter emails into the JavaScript file, which reports how many of these names and phrases occur in the email, if you open GMail in Chrome, choose View..Developer..JavaScript Console from the Chrome menu, and click on an email  

- the program specifically targets Indian recruiters. The fact that literally every one of the spam recruiter emails I recieve every day is from someone with an Indian name, is irrelevant to the kind of people who look for prejudice everywhere. This program is nothing to do with prejudice. 

- worst of all, Google has changed the way Extensions, or Plugins, work. InboxSDK depends on updating itself from its own website every time it is used. Most of the code for InboxSDK is in this site. But the latest version of Chrome Extensions demands that your Extension uses manifest.json version 3, which makes it impossible for the extension to use this remote code. This code uses version 2. 

https://stackoverflow.com/questions/72360336/latest-beta-version-of-inboxsdk-library-which-supports-chrome-manifest-v3-is-not

### Installation

The JavaScript Extension only works in Chrome. Go to chrome://extensions/ and choose "Load unpacked". A dialog will appear. Choose the folder where you downloaded this code, and hit "Select". Now open another tab, and enter "mail.google.com".

From the top menu in your browser, choose "View...Developer...JavaScript Console".

Choose an email from your Inbox. Watch the JavaScript Console to see how the program is classifying it.

### Python Machine Learning 

classify.py reads files from the data/ folder. The files whose names begin 'spam' are spam, and those which begin 'not-spam' are not spam. It is supposed to adjust its algorithm when it falsely classifies spam as not spam, or vice-versa. It is then supposed to translate what it has learned into JavaScript. The Python program reads messageView.js.template, and creates messageView.js, which must be loaded into Chrome using the Extension Manager (see above).

classify.py runs under Python 3.9+

