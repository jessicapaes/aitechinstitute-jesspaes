# Branch Workflow for INT AI DS Course

## Quick Reference

| Branch | Purpose | Commands |
|--------|---------|----------|
| `dev` | Development | `./manage_branches.sh start-dev` |
| `release-week-X` | Clean for release | `./manage_branches.sh release X` |
| `main` | Student materials | Never work here directly |
| `live-session-DATE` | Teaching | `./manage_branches.sh teach` |

## Full Workflow

### 📝 Monday-Thursday: Development
```bash
./manage_branches.sh start-dev
# Create/edit materials in week_X/
git add .
git commit -m "Develop week X materials"
git push origin dev
📦 Friday: Release
./manage_branches.sh release 0  # For week 0
git add week_0/
git commit -m "Release week 0 materials"
git push -u origin release-week-0
# Go to GitHub and create PR
🎓 Class Time: Teaching
./manage_branches.sh teach
# Teach with Jupyter
./manage_branches.sh done-teaching
Emergency Commands
If something goes wrong:
# Check where you are
git status
git branch

# Get back to safety
git checkout dev

# Discard all local changes
git reset --hard HEAD

# Sync with remote
git pull origin dev
Branch Rules

NEVER commit directly to main
ALWAYS develop on dev
ALWAYS clean notebooks before release
ALWAYS delete live-session branches after class
ALWAYS use PRs to merge to main

Testing the Workflow

Check current status: ./manage_branches.sh status
Practice creating a release: ./manage_branches.sh release 0
Practice teaching setup: ./manage_branches.sh teach
