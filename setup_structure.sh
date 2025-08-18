#!/bin/bash

# Create folders for week_00 to week_12 (13 weeks total)
for i in {00..12}
do
    echo "Creating week_$i folders..."
    mkdir -p "week_$i/slides"
    mkdir -p "week_$i/notebooks"
    mkdir -p "week_$i/resources"
    mkdir -p "week_$i/homework"
    
    # Create empty .gitkeep files so git tracks empty folders
    touch "week_$i/slides/.gitkeep"
    touch "week_$i/notebooks/.gitkeep"
    touch "week_$i/resources/.gitkeep"
    touch "week_$i/homework/.gitkeep"
done

# Create README
echo "# INT AI DS Course Materials 2025-08" > README.md
echo "Course materials for International AI & Data Science program" >> README.md

# Create .gitignore for Jupyter files
cat > .gitignore << 'GITIGNORE'
*.ipynb_checkpoints
.ipynb_checkpoints/
*-checkpoint.ipynb
.DS_Store
__pycache__/
*.pyc
GITIGNORE

echo "✅ Course structure created successfully!"
echo "📁 Created week_00 to week_12 with slides, notebooks, resources, and homework folders"
