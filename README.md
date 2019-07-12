# cut-release

Python script to help QA team or anyone to cut the release branch off of the default branch. This project is mainly for the person who handles the Release activity. Instead of repeating the tasks or commands each time, isn't it better to automate the same? 

This project assumes you have set up the SSH access to your Public/Private GitHub. The goal is to just create a separate release branch out of the default branch and push to the default branch, so that the QA team can work off the release branch and rest of the developers can work on development branch. This is mainly useful when your application has multiple sub-projects or teams and you as a QA person want to have a release branch cut out so that the other development work doesn't affect your testing.

Below actions are automated:

1. Clone the repo
2. Create a Release Branch
3. Push the branch to the origin
4. Collect the issues/JIRAs that are scheduled to go out with the release
5. Delete the repo

*Note:* The reason for deleting the repo at the end is to make sure we are not storing stuff on the CI servers (Yes, a CI server! You can schedule a cron job to cut the release branch for you based on your requirement!)
