# 📚 COMPLETE GitHub Setup Guide - Start Here!  
**INT AI DS Course**

Welcome to our first class! Let's set up everything from scratch. Follow these steps in order.

---

## 📝 PART 1: Before You Begin (One-Time Setup)

### ✅ Prerequisites Checklist
- [ ] 🐍 Install Python ([Download Anaconda](https://www.anaconda.com/products/individual))
- [ ] 🔧 Install Git ([Download Git](https://git-scm.com/downloads))
- [ ] 🐙 Create a GitHub account ([Sign up here](https://github.com/signup))
- [ ] 🌐 Log into GitHub in your browser

---

## 🚀 PART 2: Initial Setup (Do This NOW - ~5 minutes)

### Step 1: Accept the GitHub Classroom Assignment
1. Click this link: [GitHub Classroom Assignment](https://classroom.github.com/a/5rVSv69f)
2. Click **"Accept this assignment"**
3. Wait ~30 seconds for your repository to be created
4. You’ll see:  
   `Your repository has been created: course-materials-all-YOUR_USERNAME`
5. Click that link to view your repository

---

### Step 2: Clone Your Repository
Open your terminal/command prompt and run:
```bash
# Clone your personal repository (replace YOUR_USERNAME)
git clone https://github.com/int-ai-ds-25-08/course-materials-all-YOUR_USERNAME.git

# Navigate into the folder
cd course-materials-all-YOUR_USERNAME

# Verify location
pwd
# Should show: .../course-materials-all-YOUR_USERNAME
```

---

### Step 3: Connect to Course Materials
```bash
# Add the course template as "upstream"
git remote add upstream https://github.com/aitechinstitute/int-ai-ds-25-08-template.git

# Verify both remotes are set up
git remote -v
```

Expected output:
```
origin    https://github.com/int-ai-ds-25-08/course-materials-all-YOUR_USERNAME.git (fetch)
origin    https://github.com/int-ai-ds-25-08/course-materials-all-YOUR_USERNAME.git (push)
upstream  https://github.com/aitechinstitute/int-ai-ds-25-08-template.git (fetch)
upstream  https://github.com/aitechinstitute/int-ai-ds-25-08-template.git (push)
```

---

### Step 4: Get Week 0 Materials (First-Time Special Command)
```bash
# Fetch the materials
git fetch upstream

# FIRST TIME ONLY - need special flag
git merge upstream/main --allow-unrelated-histories -m "Get week 0 materials"
```

⚠️ **If you see merge conflicts:**
```bash
git checkout --theirs .
git add .
git commit -m "Accept all course materials"
git push origin main
```

---

### Step 5: Verify Everything Works
```bash
# Check notebooks
ls week_0/notebooks/
# Should show 11 notebook files

# Check slides
ls week_0/slides/
# Should show Week-00_premier-slides.pptx

# Open Jupyter
jupyter notebook week_0/notebooks/00_lab_01_system_setup.ipynb
```

---

## 📅 PART 3: Your Weekly Routine (Starting Week 1)

### ⏰ Before Each Class (Tue/Thu)
```bash
# 1. Go to your repo
cd ~/path/to/course-materials-all-YOUR_USERNAME

# 2. Save your work
git add .
git commit -m "Save my work"

# 3. Get new materials
git fetch upstream
git merge upstream/main -m "Get week X materials"
```
> Note: From Week 1 onwards, you **don’t** need `--allow-unrelated-histories`.

---

### 📝 During/After Class
```bash
# Save your notes and exercises
git add .
git commit -m "Week X class notes and exercises"
git push origin main
```

---

## 🔧 PART 4: Troubleshooting Guide

### ❌ Problem: `command not found: git`  
✅ Solution: Install Git → [Download here](https://git-scm.com/downloads)

---

### ❌ Problem: `command not found: jupyter`  
✅ Solution: Install Jupyter:
```bash
pip install jupyter
# or
conda install jupyter
```

---

### ❌ Problem: "repository not found"  
✅ Solution:
1. Accept the assignment first  
2. Use **your** username, not the example  
3. Ensure you’re logged into GitHub  

---

### ❌ Problem: "Permission denied (publickey)"  
✅ Solution: Use HTTPS, not SSH.  
Clone should start with `https://`, not `git@`.

---

### ❌ Problem: "fatal: refusing to merge unrelated histories"  
✅ Solution: First time only:
```bash
git merge upstream/main --allow-unrelated-histories
```

---

### ❌ Problem: "upstream does not appear to be a git repository"  
✅ Solution:
```bash
git remote add upstream https://github.com/aitechinstitute/int-ai-ds-25-08-template.git
```

---

### ❌ Problem: Merge conflicts  
✅ Solution: Accept all instructor materials:
```bash
git checkout --theirs .
git add .
git commit -m "Resolved conflicts"
```

---

## 🔄 PART 5: Complete Reset (If Everything Breaks)

```bash
# 1. Delete broken repo
rm -rf course-materials-all-YOUR_USERNAME

# 2. Clone fresh
git clone https://github.com/int-ai-ds-25-08/course-materials-all-YOUR_USERNAME.git
cd course-materials-all-YOUR_USERNAME

# 3. Add upstream
git remote add upstream https://github.com/aitechinstitute/int-ai-ds-25-08-template.git

# 4. Get materials (special flag)
git fetch upstream
git merge upstream/main --allow-unrelated-histories

# 5. If conflicts, accept all
git checkout --theirs .
git add .
git commit -m "Fresh setup complete"
git push origin main
```

---

## ✅ PART 6: Success Checklist

Before class starts, confirm you:
- [ ] 🎓 Accepted the GitHub Classroom assignment
- [ ] 💻 Cloned your repository locally
- [ ] 🔗 Added upstream remote (`git remote -v`)
- [ ] 📂 Merged Week 0 materials successfully
- [ ] 📑 See 11 notebooks in `week_0/notebooks/`
- [ ] 🚀 Can open Jupyter notebooks

---

## 💬 PART 7: Getting Help

**Before Class**  
- 💬 Slack: `#int-ai-ds-25-08` (post your error message)  
- 📧 Email: support@aitechinstitute.com.au  

**15 minutes before class (4:15 PM AWST)**  
- 🔗 Live setup help: [Google Meet Link](https://meet.google.com/cbu-hczs-sab)  

**During Class**  
- 🙋 Ask immediately—others likely have the same question!  

---

## 📍 Important Reminders
- ⏰ **Class Time:** 4:30 PM AWST (6:30 PM AEST)  
- 🔗 **Class Link:** [Google Meet](https://meet.google.com/cbu-hczs-sab)  
- 🎯 **Today’s Focus:** System setup + Git workflow  
- 💻 **Bring:** Laptop with Python, Git, GitHub ready  

⚠️ **Note:** The `--allow-unrelated-histories` flag is only needed today.  
From Week 1 onwards, just use:
```bash
git merge upstream/main
```

---

See you in class!  
**– Amir**

---

**P.S.** If you’re stuck, join at 4:15 PM AWST for personal help. We’ll ensure everyone is ready before class content begins!
