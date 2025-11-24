# CINA 官方网站 - 技术架构文档

## 1. 概述

`cina-official-website` 是一个使用 Next.js 框架构建的静态信息网站。其技术选型以性能、搜索引擎优化（SEO）和快速开发为核心。整个项目不包含任何与区块链的直接交互，是一个纯粹的前端应用。

## 2. 技术栈

*   **核心框架:** [Next.js](https://nextjs.org/) 13+ (使用 App Router)
*   **UI 框架:** [React](https://react.dev/) 18
*   **开发语言:** [TypeScript](https://www.typescriptlang.org/)
*   **样式:** CSS Modules 或 Tailwind CSS (根据 `package.json` 和组件代码确定)
*   **部署:** 作为一个标准的 Next.js 项目，它可以被部署在任何支持 Node.js 的平台，如 Vercel, Netlify 或自托管服务器。

## 3. 项目结构

项目采用了 Next.js App Router 的标准目录结构。

```
src/
├── app/                # App Router 核心目录
│   ├── page.tsx        # 网站首页 (/)
│   ├── layout.tsx      # 根布局组件
│   ├── globals.css     # 全局样式
│   └── pillars/        # “核心支柱”页面的路由组
│       └── [slug]/     # 动态路由目录
│           └── page.tsx # 动态页面组件，例如 /pillars/wrmb
├── components/         # 可复用的 React 组件 (如 Header, Footer, Card)
└── ...                 # 其他可能的目录，如 public/ (存放图片), lib/ (存放工具函数)
```

## 4. 核心架构与实现

### 4.1. 路由与页面生成

*   **App Router:** 项目使用 Next.js 最新的 App Router 模式进行路由管理。目录结构直接映射到 URL 路径。
*   **静态生成 (Static Site Generation - SSG):** 该网站被构建为一个完全静态的网站。
    *   `app/page.tsx` 定义了网站主页的内容。
    *   `app/pillars/[slug]/page.tsx` 文件通过 Next.js 的 `generateStaticParams` 函数，在**构建时**为每一个“核心支柱”（如 WRMB, sWRMB）生成一个静态的 HTML 页面。
    *   这种方式提供了最佳的加载性能和 SEO 效果，因为用户直接下载的是预先渲染好的 HTML 文件。

### 4.2. 内容管理

*   **硬编码内容:** 项目中**没有**使用任何外部的 CMS (Content Management System) 或 API 来管理内容。
*   所有的文本、图片路径、新闻文章和合作伙伴信息都直接硬编码在 React 组件（`.tsx` 文件）中。例如，`app/pillars/[slug]/page.tsx` 文件内部会包含一个类似 `PILLARS` 的常量对象，根据 URL 中的 `slug` 参数来查找并显示对应的内容。
*   **优点:** 开发流程简单、快速。
*   **缺点:** 任何内容的修改（即使是一个错别字）都需要前端开发人员修改代码、重新构建和部署整个网站。

### 4.3. 区块链交互

*   **无直接交互:** `package.json` 中**不包含**任何 Web3 相关的库，如 `ethers.js`, `web3.js`, `wagmi` 等。
*   代码中没有任何连接钱包、查询链上数据或发送交易的逻辑。
*   网站上的“发行 WRMB”等行为召唤按钮 (Call to Action) 只是简单的 HTML 链接 (`<a>` 标签)，其 `href` 属性指向一个独立的、负责处理链上交互的 DApp 应用的 URL。

## 5. 结论

`cina-official-website` 是一个技术实现非常直接的静态营销网站。其架构完全服务于其作为信息展示平台的目的。对于开发者来说，维护工作主要集中在修改 React 组件中的硬编码内容和调整 UI 样式。
