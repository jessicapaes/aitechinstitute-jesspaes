# INT AI DS Course — GitHub Setup Instructions

> **Welcome! 🎉**  
> This guide helps you set up your own private repository for the course. You’ll use it to pull weekly materials, run notebooks, take notes, submit work, and keep everything safely backed up.

---

## Quick Links (Videos)

- **Video 1 — Create a GitHub Account:**  
  [https://youtu.be/Vyx4KFc039s](https://youtu.be/Vyx4KFc039s)  
  [![Create a GitHub Account](https://img.youtube.com/vi/Vyx4KFc039s/hqdefault.jpg)](https://youtu.be/Vyx4KFc039s)

- **Video 2 — Set up GitHub Classroom (Student):**  
  [https://youtu.be/3Bf7ifK2Cmc](https://youtu.be/3Bf7ifK2Cmc)  
  [![Set up GitHub Classroom](https://img.youtube.com/vi/3Bf7ifK2Cmc/hqdefault.jpg)](https://youtu.be/3Bf7ifK2Cmc)

---

## Table of Contents
- [Initial Setup (Do This ONCE)](#initial-setup-do-this-once--takes--5-minutes)
  - [Step 1: Accept the GitHub Classroom Assignment](#step-1-accept-the-github-classroom-assignment)
  - [Step 2: Clone Your Repository to Your Computer](#step-2-clone-your-repository-to-your-computer)
  - [Step 3: Connect to Course Updates (One-Time Setup)](#step-3-connect-to-course-updates-one-time-setup)
  - [Step 4: Test Everything Works](#step-4-test-everything-works)
- [Weekly Workflow](#-weekly-workflow-what-youll-do-every-week)
  - [Before Each Class: Get New Materials](#before-each-class-get-new-materials)
  - [During/After Class: Save Your Work](#duringafter-class-save-your-work)
- [Repository Structure](#-your-repository-structure)
- [FAQ](#-frequently-asked-questions)
- [Troubleshooting](#-troubleshooting)
- [Pro Tips](#-pro-tips)
- [Need Help?](#-need-help)
- [Setup Checklist](#-setup-checklist)

---

## Initial Setup (Do This ONCE — Takes ~5 minutes)

### Step 1: Accept the GitHub Classroom Assignment

1. **Click the invitation link from your instructor**  
   It will look like: `https://classroom.github.com/a/XXXXXX`  
   ⚠️ Make sure you’re logged into GitHub first (create an account at https://github.com if needed).

2. **You’ll see a page like:**
```
GitHub Classroom
INT-AI-DS-25-08

Accept this assignment: course-materials

[Accept this assignment] button
```

3. **Click “Accept this assignment”.**

4. **After ~30 seconds, you’ll see confirmation:**
```
✓ You accepted the assignment, course-materials

Your assignment repository has been created:
https://github.com/int-ai-ds-25-08/course-materials-wvlt2
```

5. **Click the link to go to *your* repository.**

---

### Step 2: Clone Your Repository to Your Computer

1. On your repository page, click the green **`<> Code`** button.
2. Copy the **HTTPS** URL (example):  
   `https://github.com/int-ai-ds-25-08/course-materials-wvlt2.git`
3. Open your terminal / command prompt and run:
```bash
git clone https://github.com/int-ai-ds-25-08/course-materials-wvlt2.git
```
Example output:
```
Cloning into 'course-materials-wvlt2'...
remote: Enumerating objects: 18, done.
remote: Counting objects: 100% (18/18), done.
remote: Compressing objects: 100% (13/13), done.
Receiving objects: 100% (18/18), done.
```
4. Go into your new folder:
```bash
cd course-materials-wvlt2
```
5. Check that everything is there:
```bash
ls
```
You should see something like:
```
README.md    STUDENT_INSTRUCTIONS.md    week_0/    week_1/    week_2/ ... week_12/
```

---

### Step 3: Connect to Course Updates (One-Time Setup)

This lets you receive new materials each week.

1. **Add the course “upstream” repository:**
```bash
git remote add upstream https://github.com/aitechinstitute/int-ai-ds-25-08-course-materials-all-int-ai-ds-25-08-template.git
```
2. **Verify it worked:**
```bash
git remote -v
```
You should see **four** lines:
```
origin    https://github.com/int-ai-ds-25-08/course-materials-wvlt2.git (fetch)
origin    https://github.com/int-ai-ds-25-08/course-materials-wvlt2.git (push)
upstream  https://github.com/aitechinstitute/int-ai-ds-25-08-course-materials-all-int-ai-ds-25-08-template.git (fetch)
upstream  https://github.com/aitechinstitute/int-ai-ds-25-08-course-materials-all-int-ai-ds-25-08-template.git (push)
```
✅ If you see these 4 lines, you’re all set!

---

### Step 4: Test Everything Works

1. Open the first notebook:
```bash
jupyter notebook week_0/notebooks/introduction.ipynb
```
2. Run the first cell — you should see: **“Hello, INT AI DS!”**
3. Add a new cell with your own notes (use **Shift+Enter** to run cells).
4. Save your work (**Ctrl+S** / **Cmd+S** in Jupyter).
5. Commit and push your changes:
```bash
git add .
git commit -m "My first commit - testing setup"
git push origin main
```

---

## 📅 Weekly Workflow (What You’ll Do Every Week)

### Before Each Class: Get New Materials
```bash
# 1) Make sure you're in your repository folder
cd ~/path/to/course-materials-wvlt2

# 2) Fetch new materials from the course template
git fetch upstream

# 3) Merge them into your repository
git merge upstream/main -m "Get week X materials"
```
**Example output when new materials are available:**
```
Updating e53de45..abc1234
Fast-forward
 week_1/notebooks/lesson1.ipynb | 150 +++++++++++++++++++
 week_1/slides/lecture1.pdf     | Bin 0 -> 245632 bytes
 2 files changed, 150 insertions(+)
```

### During/After Class: Save Your Work
```bash
# 1) Save all your changes
git add .

# 2) Commit with a meaningful message
git commit -m "Week 1 notes and exercises"

# 3) Push to YOUR repository
git push origin main
```

---

## 📁 Your Repository Structure
```
course-materials-wvlt2/
├── week_0/
│   ├── notebooks/     # Jupyter notebooks for hands-on work
│   ├── slides/        # Lecture slides (PDFs)
│   ├── homework/      # Assignments
│   └── resources/     # Additional materials
├── week_1/
│   ├── notebooks/
│   ├── slides/
│   ├── homework/
│   └── resources/
├── week_2/
│   └── ... (same structure)
└── ... through week_12/
```

---

## ❓ Frequently Asked Questions

### Will my notes be overwritten when I get new materials?
**No.** Git merges the instructor’s new files into your repository. Your notes stay in your copy. (If you edit the **same** file the instructor updated, you may see a merge conflict—see below.)

### Can other students see my work?
**No.** Your repository is private. Only you and the instructor(s) can access it.

### What if I mess up and want to start fresh?
You can delete your local folder and clone again:
```bash
rm -rf course-materials-wvlt2
git clone https://github.com/int-ai-ds-25-08/course-materials-wvlt2.git
cd course-materials-wvlt2
git remote add upstream https://github.com/aitechinstitute/int-ai-ds-25-08-course-materials-all-int-ai-ds-25-08-template.git
```

### What if I see “merge conflicts”?
This is rare. If it happens and you just want to keep **your** versions:
```bash
# Keep your version of files during a merge conflict
git checkout --ours .
git add .
git commit -m "Resolved conflicts, keeping my work"
```
> Tip: Ask in class if you’re unsure—we’ll help you merge properly so you don’t lose notes.

### I forgot to save my work before getting new materials!
No problem. First commit your current work:
```bash
git add .
git commit -m "Save my work"
```
Then fetch and merge the new materials as usual.

---

## 🆘 Troubleshooting

### “Permission denied” or “Authentication failed”
- Make sure you’re logged into GitHub.
- Consider using a **Personal Access Token** instead of a password.
- Docs: https://docs.github.com/en/authentication

### “Repository not found”
- Confirm you **accepted the assignment** first.
- Make sure you’re using **your** repository URL (not the example).

### “Not a git repository”
- Ensure you’re in the right folder:
```bash
cd course-materials-YOUR_USERNAME   # e.g., course-materials-wvlt2
```

### Jupyter won’t start
- Install Jupyter: `pip install jupyter`
- Or try: `python -m notebook`

---

## 💡 Pro Tips

1. **Commit often.** Small, frequent commits are safest.
2. **Write meaningful commit messages.** (e.g., “Week 3 notes on neural networks”).
3. **Pull before you start working.** Get the latest materials first.
4. **Use Markdown cells** in notebooks for clear, structured notes.
5. **Back up by pushing.** If it’s not pushed, it’s not backed up.

---

## 📞 Need Help?

- **During class:** Ask right away—others probably have the same question.
- **Outside class:**
  - Check this guide first
  - Ask in the course discussion forum
  - Come to office hours
  - Email your instructor and include:
    - What you tried
    - The exact error message
    - A screenshot if helpful

---

## ✅ Setup Checklist

Before the next class, make sure you’ve:

- [ ] Accepted the GitHub Classroom assignment
- [ ] Cloned your repository locally
- [ ] Added the `upstream` remote
- [ ] Opened and run a notebook successfully
- [ ] Pushed at least one commit to your repository

---

*Happy coding! 🚀*
