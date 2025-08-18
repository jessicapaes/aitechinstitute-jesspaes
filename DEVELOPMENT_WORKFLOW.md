# Development Workflow

## Branches
- `main`: Clean, student-ready materials (NEVER develop here)
- `dev`: All development happens here
- `live-*`: Temporary branches for teaching (never push)

## Weekly Development Cycle

### Monday-Thursday: Develop
```bash
git checkout dev
# Create materials
git add .
git commit -m "Develop week X"
git push origin dev
Friday: Release
bash# On dev: clean notebooks
jupyter nbconvert --clear-output --inplace week_X/**/*.ipynb
git commit -am "Clean week X"
git push origin dev

# Release to main
git checkout main
git checkout dev -- week_X/
git commit -m "Release week X"
git push origin main
git checkout dev
During Class: Teach
bashgit checkout main
git checkout -b live-session-X
# Teach (don't push)
git checkout dev
git branch -D live-session-X
Future Semesters

Main branch has all clean materials
Just clone and teach
Update dev for improvements
