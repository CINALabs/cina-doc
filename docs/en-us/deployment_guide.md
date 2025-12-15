# CINA Documentation Site Deployment Guide

This guide details how to run the CINA Docsify documentation site locally and deploy it to **GitHub Pages**.

## 1. Local Run & Preview

Before deploying, it is recommended to run the site locally to preview changes.

### Prerequisites
*   [Node.js](https://nodejs.org/) installed.

### Steps
1.  **Install Docsify CLI** (if not already installed):
    ```bash
    npm i docsify-cli -g
    ```

2.  **Start the Local Server**:
    Open your terminal in the project root (`d:/zWenbo/AI/CINA`) and run:
    ```bash
    docsify serve docs
    ```

3.  **Access the Site**:
    Open your browser and navigate to `http://localhost:3000`.

---

## 2. Deploy to GitHub Pages

### Step 1: Prepare the Documentation
Ensure your `docs/` directory is ready.
*   **`.nojekyll` File**: Ensure an empty file named `.nojekyll` exists in the `docs/` directory to prevent GitHub from ignoring files starting with `_` (like `_sidebar.md`).

### Step 2: Push to GitHub
1.  Commit all changes and push to your remote repository:
    ```bash
    git add .
    git commit -m "chore: update documentation"
    git push origin main
    ```

### Step 3: Enable GitHub Pages
1.  Go to your repository on **GitHub.com**.
2.  Click on **Settings** -> **Pages** (sidebar).
3.  Under **Build and deployment**:
    *   **Source**: Select **Deploy from a branch**.
4.  Under **Branch**:
    *   Select your branch (e.g., `main`).
    *   Select the folder **`/docs`** (Crucial step!).
5.  Click **Save**.

### Step 4: Verification
Wait for the deployment to finish, then visit the link provided by GitHub (e.g., `https://CINALabs.github.io/CINA/`).
