# Welcome to INT AI DS Course! 

## Initial Setup (Do this ONCE at the beginning of the course)

1. You've already accepted the GitHub Classroom assignment and have your own repository.

2. Clone your personal repository:

    ```
    git clone https://github.com/int-ai-ds-25-08/course-materials-YOUR_USERNAME.git
    cd course-materials-YOUR_USERNAME
    ```
   
## Set up the course upstream to receive new materials:

    git remote add upstream https://github.com/aitechinstitute/int-ai-ds-25-08-template.git
    git remote -v  # Verify you see both 'origin' (your repo) and 'upstream' (course template)

## Weekly Workflow
Before Each Class - Get New Materials:
### Fetch the latest materials from the course
    git fetch upstream
    git merge upstream/main -m "Merge week X materials"

### If there are conflicts (rare), keep your version:
    git checkout --ours .
    git add .
    git commit -m "Resolved conflicts, keeping my work"
    
## During/After Class - Save Your Work:
### Save your notes and work
    git add .
    git commit -m "My notes from week X"
    git push origin main

### Important Tips

- Your work is ALWAYS safe in your personal repository
- Never force push - if you have conflicts, ask for help
- Make commits frequently to save your progress
- Your repository is private - only you and instructors can see it

### Need Help?
- If you encounter any issues, please reach out during class or office hours.
- Use Slack or support@aitechinstitute.com.au
