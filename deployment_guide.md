# CINA Documentation Site Deployment Guide

This guide details how to deploy the CINA Docsify documentation site to **GitHub Pages**.

## Prerequisites

1.  **GitHub Account**: You must have a GitHub account.
2.  **Git Installed**: You must have Git installed on your local machine.
3.  **Project Repository**: The project must be a Git repository.

## Step 1: Prepare the Documentation

Ensure your `docs/` directory is ready for deployment.

1.  **Verify `index.html`**: Ensure `docs/index.html` is correctly configured (already done).
2.  **Bypass Jekyll**: GitHub Pages uses Jekyll by default, which ignores files starting with `_` (like `_sidebar.md`). To prevent this, we must create an empty file named `.nojekyll` in the `docs/` directory.
    *   *Note: This file has already been created for you.*

## Step 2: Push to GitHub

1.  Open your terminal in the project root (`d:/zWenbo/AI/CINA`).
2.  Add all changes to Git:
    ```bash
    git add .
    ```
3.  Commit the changes:
    ```bash
    git commit -m "feat: setup docsify documentation site"
    ```
4.  Push to your GitHub repository:
    ```bash
    git push origin main
    ```
    *(Replace `main` with your branch name if different)*

## Step 3: Enable GitHub Pages

1.  Go to your repository on **GitHub.com**.
2.  Click on **Settings** (top right tab).
3.  In the left sidebar, click on **Pages** (under the "Code and automation" section).
4.  Under **Build and deployment**:
    *   **Source**: Select **Deploy from a branch**.
5.  Under **Branch**:
    *   Select your branch (e.g., `main` or `master`).
    *   Select the folder **`/docs`** (this is crucial!).
6.  Click **Save**.

## Step 4: Verification

1.  After saving, GitHub will start a deployment workflow. Wait for a minute or two.
2.  Refresh the Pages settings page. You should see a message at the top: "Your site is live at..." with a link.
3.  Click the link to visit your documentation site.
4.  **Verify Features**:
    *   **Bilingual Support**: Check if switching languages works.
    *   **Dark Mode**: Click the toggle button (usually bottom right or top right) to check Dark/Light mode.
    *   **Mermaid Diagrams**: Navigate to "Product Architecture" to ensure diagrams render.

## Troubleshooting

*   **404 Errors**: If you get a 404 error, ensure you selected the `/docs` folder in Step 3, not the root `/`.
*   **Missing Sidebar**: If the sidebar is missing, ensure the `.nojekyll` file exists in the `docs/` folder.
*   **Diagrams not rendering**: Ensure the Mermaid script is loaded in `index.html`.

## Custom Domain (Optional)

If you have a custom domain (e.g., `docs.cina.io`):
1.  In the **Pages** settings, enter your custom domain in the **Custom domain** field.
2.  Configure your DNS provider (CNAME record) to point to your GitHub Pages URL.
