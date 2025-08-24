# 📢 GitHub Classroom Workflow Guide

This guide explains how to **fetch new course materials** and **submit your work** each week.  
Follow these steps carefully to stay up to date.

---

## 🔄 1. One-time Setup

Tell Git where to fetch the official course materials from:

```bash
git remote remove upstream
git remote add upstream https://github.com/aitechinstitute/int-ai-ds-25-08-course-materials-all-int-ai-ds-25-08-template.git
git remote -v
```

✅ You should now see:
- `origin` → your personal repo (where you push your work)  
- `upstream` → the class repo (where new materials come from)  

---

## 📥 2. Getting the Latest Course Materials (every time new content is released)

1. **First Save your work from before (if you have any)**  
   ```bash
   git add -A
   git commit -m "WIP before syncing"
   ```

2. **Bring in the latest class materials**  
   ```bash
   git pull --rebase upstream main
   ```

3. **Update your own repo**  
   ```bash
   git fetch origin
   git push origin main --force-with-lease
   ```

---

## 📝 3. Working on Assignments

- Do your coding/writing in your repo.  
- Commit regularly with clear messages:  

```bash
git add <file>
git commit -m "Finished data cleaning step"
```

---

## 📤 4. Submitting Your Work

When finished with a lab/assignment:

```bash
git push origin main
```

✅ That’s it — your repo is now submitted.

---

## 🚑 5. If Something Goes Wrong

If your repo gets messy or broken, reset to the official course repo:

```bash
git fetch upstream
git reset --hard upstream/main
git push origin main --force-with-lease
```

⚠️ Warning: this will overwrite your local work with the official version.

---

## ✅ Summary Workflow

**Each time new materials are posted:**

```
fetch upstream → rebase into main → push to origin
```

**Each time you finish work:**

```
push to origin
```

---

## 🔎 Visual Workflow

```
          ┌─────────────┐
          │  Upstream   │  (class repo, official materials)
          └──────┬──────┘
                 │
     git pull --rebase upstream main
                 │
        ┌────────▼────────┐
        │   Your Repo     │  (local copy + origin fork)
        └──────┬─────────┘
               │
        git push origin main
               │
        ┌──────▼──────┐
        │   Origin    │  (your GitHub repo for submissions)
        └─────────────┘
```

---

Happy coding 🚀
