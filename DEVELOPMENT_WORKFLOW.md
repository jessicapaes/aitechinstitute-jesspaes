# INT AI DS Course - Complete Instructor & TA Guide

## 🎯 Overview
This guide covers the complete workflow for managing course materials using our 4-branch system.

## 🌳 Branch Structure

| Branch Type | Purpose | Who Uses | Lifetime |
|------------|---------|----------|----------|
| `main` | Clean materials students pull | Students | Forever |
| `dev` | Development workspace | Instructors/TAs | Forever |
| `release-week-X` | Quality check before release | Instructors/TAs | Temporary (few hours) |
| `live-session-DATE` | Live teaching demos | Instructor | Temporary (2-3 hours) |

## 📋 Initial Setup (One Time Only)

### For Instructors/TAs:
```bash
# 1. Clone the repository
git clone https://github.com/aitechinstitute/int-ai-ds-25-08-template.git
cd int-ai-ds-25-08-template

# 2. Set up dev branch locally
git checkout dev
git pull origin dev

# 3. Verify you have the helper script
ls manage_branches.sh
# If missing, get it from dev branch:
git checkout dev -- manage_branches.sh
chmod +x manage_branches.sh

# 4. Test the setup
./manage_branches.sh status
```

## 📅 Weekly Workflow

### Friday-Monday: Development Phase

**Instructor/TA develops new materials:**

```bash
# 1. Start development session (Friday afternoon)
./manage_branches.sh start-dev
# OR manually:
git checkout dev
git pull origin dev

# 2. Create/modify materials for the upcoming week
# Example for Week 1:
cd week_1/notebooks/
# Create new notebook, edit existing ones, add slides, etc.

# 3. Save your work frequently
git add .
git commit -m "Develop Week 1: Data Analysis fundamentals"
git push origin dev

# 4. Continue developing through the weekend
# Make as many commits as needed - dev can be messy!
```

### Monday: Release Phase (Before Class)

**Instructor reviews and releases materials:**

```bash
# 1. Monday morning - Ensure all development is complete
git checkout dev
git pull origin dev
git status  # Should be clean

# 2. Create release branch
./manage_branches.sh release 1
# OR manually:
git checkout -b release-week-1

# 3. Clean all notebooks (removes output)
find week_1 -name "*.ipynb" -exec jupyter nbconvert --clear-output --inplace {} \;

# 4. Review what will be released
git status
git diff HEAD week_1/

# 5. Commit cleaned materials
git add week_1/
git commit -m "Release: Week 1 materials - Data Analysis"

# 6. Push release branch
git push -u origin release-week-1

# 7. Create Pull Request on GitHub
echo "Create PR at: https://github.com/aitechinstitute/int-ai-ds-25-08-template/compare/main...release-week-1"
```

### Creating & Merging the Pull Request

**On GitHub (Monday morning):**

1. Go to: https://github.com/aitechinstitute/int-ai-ds-25-08-template
2. Click "Compare & pull request" for `release-week-1`
3. Review the changes:
   - ✅ Check all notebooks have no output
   - ✅ Verify no solutions are visible
   - ✅ Ensure no personal/sensitive data
4. Set PR title: "Release Week 1: Data Analysis"
5. Add description:
   ```markdown
   ## Week 1 Release
   
   ### Contents:
   - [ ] Lecture notebooks (3 files)
   - [ ] Homework assignment
   - [ ] Slides PDF
   
   ### Checklist:
   - [ ] All notebooks cleaned
   - [ ] No solution code visible
   - [ ] Tested all code cells
   - [ ] Ready for students
   ```
6. Click "Merge pull request"
7. Click "Confirm merge"
8. Delete the release branch (GitHub will prompt)

**Back in terminal:**
```bash
# 8. Clean up local branch
git checkout main
git pull origin main
git checkout dev
git branch -d release-week-1

# 9. Notify students (optional)
echo "✅ Week 1 materials are now available! Run 'git fetch upstream && git merge upstream/main'"
```

### Class Days (Tuesday/Wednesday/Thursday): Live Teaching

**Instructor during class:**

```bash
# 1. Before class starts (5 mins before)
./manage_branches.sh teach
# This creates: live-session-20250819-1400

# 2. Verify you're on teaching branch
git branch --show-current
# Should show: live-session-[date-time]

# 3. Open Jupyter for teaching
jupyter notebook week_1/notebooks/

# During class you can:
# - Run all cells (outputs visible only to you)
# - Add new cells with examples
# - Modify code to show variations
# - Add debug print statements
# - Create new example files
# - Make mistakes and fix them live!

# 4. After class ends
./manage_branches.sh done-teaching
# OR manually:
git checkout dev
git branch -D live-session-20250819-1400
```

## 🔄 Daily Quick Commands

### Start Development (Friday)
```bash
cd ~/path/to/int-ai-ds-25-08-template
./manage_branches.sh status
./manage_branches.sh start-dev
```

### During Weekend Development
```bash
# Check what you've changed
git status
git diff

# Save work in progress
git add .
git commit -m "WIP: Week 2 materials"
git push origin dev
```

### Monday Morning Release
```bash
# Create release branch
./manage_branches.sh release [week_number]

# Clean and push
find week_X -name "*.ipynb" -exec jupyter nbconvert --clear-output --inplace {} \;
git add week_X/
git commit -m "Release: Week X materials"
git push origin release-week-X

# Create PR on GitHub and merge
```

### Before Teaching (Tue/Wed/Thu)
```bash
# Make sure you have latest materials
git checkout main
git pull origin main

# Create teaching branch
./manage_branches.sh teach
```

## 🚨 Troubleshooting

### "I need more time to develop"
```bash
# If it's Monday and materials aren't ready:
# Option 1: Release partial materials
git checkout dev
git checkout -b release-week-X-partial
# Add only completed materials
git add week_X/notebooks/intro.ipynb week_X/slides/
git commit -m "Release: Week X partial materials"
# Create PR and merge

# Option 2: Postpone release
# Notify students that materials will be available later
# Continue on dev, release Monday afternoon/evening
```

### "I accidentally committed to main"
```bash
# Move the commit to dev
git checkout main
git log -1  # Note the commit hash
git checkout dev
git cherry-pick [commit-hash]
git push origin dev

# Remove from main
git checkout main
git reset --hard HEAD~1
git push origin main --force-with-lease
```

### "I forgot to clean notebooks before PR"
```bash
# On the release branch
git checkout release-week-X
find week_X -name "*.ipynb" -exec jupyter nbconvert --clear-output --inplace {} \;
git add .
git commit --amend --no-edit
git push origin release-week-X --force-with-lease
```

### "Need emergency fix after Monday release"
```bash
# Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix-week-1-typo

# Make the fix
# edit week_1/notebooks/lesson.ipynb

# Clean and commit
jupyter nbconvert --clear-output --inplace week_1/notebooks/lesson.ipynb
git add week_1/notebooks/lesson.ipynb
git commit -m "Fix: Typo in week 1 lesson"
git push origin hotfix-week-1-typo

# Create PR: hotfix-week-1-typo → main
# Merge immediately
```

## 📊 Weekly Schedule & Checklist

### Weekly Timeline
- **Friday afternoon**: Start developing next week's materials
- **Weekend**: Continue development
- **Monday morning**: Release materials via PR
- **Monday afternoon**: Students pull new materials
- **Tuesday-Thursday**: Teach using live branches

### For Instructor:
- [ ] **Friday PM**: Start developing on `dev`
- [ ] **Saturday/Sunday**: Complete materials development
- [ ] **Monday AM (before noon)**: Create release branch
- [ ] **Monday AM**: Clean notebooks
- [ ] **Monday AM**: Create & merge PR
- [ ] **Monday PM**: Verify students can pull
- [ ] **Tue/Wed/Thu**: Use `live-session` branch for teaching
- [ ] **After each class**: Delete `live-session` branch

### For Teaching Assistant:
- [ ] **Weekend**: Review materials on `dev` branch
- [ ] **Sunday**: Test all code cells work
- [ ] **Sunday**: Check homework solutions (keep separate)
- [ ] **Monday AM**: Review PR before merge
- [ ] **Monday PM**: Help students with git issues
- [ ] **Week-long**: Monitor GitHub Classroom submissions

## 🎯 Key Rules - NEVER BREAK THESE

1. **NEVER commit directly to `main`** - Always use PR
2. **NEVER push a `live-session` branch** - Always delete after class
3. **ALWAYS clean notebooks before release** - No output in student materials
4. **ALWAYS release Monday morning** - Students need materials before Tuesday class
5. **ALWAYS use dev for development** - Keep experiments off main

## 📞 Student Support

When students have issues, they should run:
```bash
# Monday afternoon - Get latest materials
git fetch upstream
git merge upstream/main

# If merge conflicts:
git stash
git fetch upstream
git reset --hard upstream/main
git stash pop  # To restore their work
```

## 🔗 Quick Links

- **Repository**: https://github.com/aitechinstitute/int-ai-ds-25-08-template
- **GitHub Classroom**: https://classroom.github.com/classrooms/215336669-int-ai-ds-25-08
- **Create PR**: https://github.com/aitechinstitute/int-ai-ds-25-08-template/pulls
- **Check PRs**: https://github.com/aitechinstitute/int-ai-ds-25-08-template/pulls

## 📝 Example: Complete Week 2 Cycle

```bash
# Friday 3pm: Start development
./manage_branches.sh start-dev
cd week_2/notebooks/
jupyter notebook  # Create pandas_basics.ipynb
git add .
git commit -m "Add pandas basics notebook"
git push origin dev

# Saturday: Add more content
# Create homework, add slides, etc.
git add week_2/
git commit -m "Add week 2 homework and slides"
git push origin dev

# Sunday: Final touches
# Review, test, polish
git add week_2/
git commit -m "Complete week 2 materials"
git push origin dev

# Monday 9am: Release
./manage_branches.sh release 2
git add week_2/
git commit -m "Release: Week 2 - Pandas and Data Manipulation"
git push origin release-week-2

# Go to GitHub, create PR, merge by 10am

# Tuesday 2pm: Teach
./manage_branches.sh teach
jupyter notebook week_2/notebooks/pandas_basics.ipynb
# After class:
./manage_branches.sh done-teaching

# Friday: Start Week 3 development...
```

## 🚀 Quick Start for This Week

```bash
# If today is Friday/Weekend - Start developing:
./manage_branches.sh start-dev
# Develop Week X materials

# If today is Monday - Release:
./manage_branches.sh release X
# Clean, commit, push, PR, merge

# If today is Tue/Wed/Thu - Teach:
./manage_branches.sh teach
# After class:
./manage_branches.sh done-teaching
```
