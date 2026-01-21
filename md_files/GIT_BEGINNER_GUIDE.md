# 🎓 Beginner's Guide to Your Git Branches

This guide explains the specific branches in your **Tabsirah** project based on your screenshot.

---

## 1. Local vs. Remote (Where is it stored?)

Imagine **Git** is a save system for your code.

| **Term** | **Analogy** | **Location** | **Explanation** |
| :--- | :--- | :--- | :--- |
| **Local** | **Your House** | Your C: Drive | These are the files on your computer. You can edit them without internet. Shown as just `master`, `main`, etc. |
| **Remote (origin)** | **The Cloud** | GitHub Servers | "Origin" is just a nickname for your specific GitHub repository. It's a backup accessible by others. |
| **origin/...** | **Last Letter from Home** | Your C: Drive | When you see `origin/master`, it's a *read-only memory* on your computer of what the files *looked like* on GitHub the last time you connected. |

> **Analogy:** `origin/master` is like a photo of your friend's house. You can look at it on your phone (Local), but you can't rearrange their furniture (Remote) until you go there (Push).

---

## 2. Your 3 Specific Branches

You have three parallel timelines (branches). Here is what each one is for:

### 🛠️ `master` (Current Active Branch)
*   **What is it?**: Currently, this is your **"Hotfix / Live"** branch. It has the latest UI fixes (colored letters).
*   **When to use**: You are using it right now.
*   **Why is it here?**: It seems to be a legacy default branch that got updated with recent fixes.
*   **Status**: ⭐️ **Most Up-To-Date**

### 🧪 `develop` (The Workbench)
*   **What is it?**: This is your **"Laboratory"**. It contains extra tools (`src/` scripts) that are too messy for the final app.
*   **When to use**: **Recommended for daily work.** You should merge your `master` fixes into this.
*   **Why is it here?**: To keep your heavy tools (training scripts) separate from the lightweight app.

### 📦 `main` (The Showroom)
*   **What is it?**: This is the **"Production Product"**. It is clean, strict, and only contains the finished app code.
*   **When to use**: **NEVER edit this directly.** Only merge into it when you are ready to publish/deploy to the internet.
*   **Why is it here?**: To ship a clean version of the app to your users (via Render).

---

## 3. Visual Flow

```mermaid
graph TD
    subgraph "Your Computer (Local)"
        master[🛠️ master] -->|Merge fixes| develop[🧪 develop]
        develop -->|Merge final version| main[📦 main]
    end
    
    subgraph "GitHub (Remote)"
        main -->|Push (Upload)| origin_main[☁️ origin/main]
        master -->|Push (Upload)| origin_master[☁️ origin/master]
    end

    style master fill:#ff9,stroke:#333,stroke-width:2px,color:black
    style develop fill:#9f9,stroke:#333,stroke-width:2px,color:black
    style main fill:#99f,stroke:#333,stroke-width:2px,color:black
```

---

## 4. Summary: What should I do?

1.  **Right Now**: You are on `master` (see the checkmark `✓` in your screenshot). This is fine! It has your latest work.
2.  **Next Step**: You should probably "push" your work to save it to GitHub.
    *   Command: `git push origin master`
    *   *Translation: "Upload my local 'master' branch to the 'origin' (GitHub) server."*

I hope this clears things up! Git can be confusing, but thinking of it as **timelines** helps.
