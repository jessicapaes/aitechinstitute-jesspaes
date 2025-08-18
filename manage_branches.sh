#!/bin/bash

echo "🌳 Branch Management Helper"
echo "=========================="

case "$1" in
  "status")
    echo "Current branch:"
    git branch --show-current
    echo ""
    echo "All branches:"
    git branch -a
    ;;
    
  "start-dev")
    echo "Switching to dev branch..."
    git checkout dev
    git pull origin dev
    echo "✅ Ready to develop!"
    ;;
    
  "release")
    if [ -z "$2" ]; then
      echo "❌ Usage: ./manage_branches.sh release <week_number>"
      exit 1
    fi
    WEEK=$2
    echo "Creating release branch for week $WEEK..."
    git checkout dev
    git checkout -b release-week-$WEEK
    
    # Clean notebooks
    echo "Cleaning notebooks..."
    find week_$WEEK -name "*.ipynb" -exec jupyter nbconvert --clear-output --inplace {} \; 2>/dev/null
    
    echo "✅ Release branch created!"
    echo "Next steps:"
    echo "1. Review changes: git status"
    echo "2. Commit: git add week_$WEEK && git commit -m 'Release week $WEEK'"
    echo "3. Push: git push -u origin release-week-$WEEK"
    echo "4. Create PR on GitHub"
    ;;
    
  "teach")
    DATE=$(date +%Y%m%d-%H%M)
    echo "Creating live teaching branch..."
    git checkout main
    git pull origin main
    git checkout -b live-session-$DATE
    echo "✅ Teaching branch ready: live-session-$DATE"
    echo "After class, run: ./manage_branches.sh done-teaching"
    ;;
    
  "done-teaching")
    CURRENT=$(git branch --show-current)
    if [[ $CURRENT == live-session-* ]]; then
      echo "Cleaning up teaching branch: $CURRENT"
      git checkout dev
      git branch -D $CURRENT
      echo "✅ Teaching branch deleted"
    else
      echo "❌ Not on a live-session branch"
    fi
    ;;
    
  *)
    echo "Usage:"
    echo "  ./manage_branches.sh status         - Show branch info"
    echo "  ./manage_branches.sh start-dev      - Start development"
    echo "  ./manage_branches.sh release <week> - Create release branch"
    echo "  ./manage_branches.sh teach          - Start teaching session"
    echo "  ./manage_branches.sh done-teaching  - Clean up after teaching"
    ;;
esac
