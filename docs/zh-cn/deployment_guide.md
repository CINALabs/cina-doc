# CINA 文档站点部署指南

本指南详细说明了如何在本地运行 CINA Docsify 文档站点以及将其部署到 **GitHub Pages**。

## 1. 本地运行与预览

在部署之前，建议在本地运行站点以预览更改。

### 前置条件
*   已安装 [Node.js](https://nodejs.org/)。

### 步骤
1.  **安装 Docsify CLI** (如果尚未安装):
    ```bash
    npm i docsify-cli -g
    ```

2.  **启动本地服务器**:
    在项目根目录 (`d:/zWenbo/AI/CINA`) 打开终端并运行:
    ```bash
    docsify serve docs
    ```

3.  **访问站点**:
    打开浏览器并访问 `http://localhost:3000`。

---

## 2. 部署到 GitHub Pages

### 第一步：准备文档
确保 `docs/` 目录已准备就绪。
*   **`.nojekyll` 文件**: 确保 `docs/` 目录下存在一个名为 `.nojekyll` 的空文件，以防止 GitHub 忽略以 `_` 开头的文件（如 `_sidebar.md`）。

### 第二步：推送到 GitHub
1.  提交所有更改并推送到远程仓库:
    ```bash
    git add .
    git commit -m "chore: update documentation"
    git push origin main
    ```

### 第三步：启用 GitHub Pages
1.  在 **GitHub.com** 上进入你的仓库。
2.  点击 **Settings** (设置) -> **Pages** (侧边栏)。
3.  在 **Build and deployment** (构建与部署) 下:
    *   **Source**: 选择 **Deploy from a branch**。
4.  在 **Branch** 下:
    *   选择你的分支 (例如 `main`)。
    *   选择文件夹 **`/docs`** (关键步骤！)。
5.  点击 **Save** (保存)。

### 第四步：验证
等待部署完成后，访问 GitHub 提供的链接 (例如 `https://CINALabs.github.io/CINA/`)。
