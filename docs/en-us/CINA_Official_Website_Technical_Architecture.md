# CINA Official Website - Technical Architecture Document

## 1. Overview

`cina-official-website` is a static information website built using the Next.js framework. Its technology selection focuses on performance, Search Engine Optimization (SEO), and rapid development. The entire project does not contain any direct interaction with the blockchain and is a pure frontend application.

## 2. Tech Stack

*   **Core Framework:** [Next.js](https://nextjs.org/) 13+ (using App Router)
*   **UI Framework:** [React](https://react.dev/) 18
*   **Language:** [TypeScript](https://www.typescriptlang.org/)
*   **Styling:** CSS Modules or Tailwind CSS (determined by `package.json` and component code)
*   **Deployment:** As a standard Next.js project, it can be deployed on any platform supporting Node.js, such as Vercel, Netlify, or self-hosted servers.

## 3. Project Structure

The project adopts the standard directory structure of Next.js App Router.

```
src/
├── app/                # App Router core directory
│   ├── page.tsx        # Homepage (/)
│   ├── layout.tsx      # Root layout component
│   ├── globals.css     # Global styles
│   └── pillars/        # Route group for "Core Pillars" pages
│       └── [slug]/     # Dynamic route directory
│           └── page.tsx # Dynamic page component, e.g., /pillars/wrmb
├── components/         # Reusable React components (like Header, Footer, Card)
└── ...                 # Other possible directories, like public/ (images), lib/ (utils)
```

## 4. Core Architecture & Implementation

### 4.1. Routing & Page Generation

*   **App Router:** The project uses Next.js's latest App Router mode for routing management. The directory structure maps directly to URL paths.
*   **Static Site Generation (SSG):** The website is built as a fully static site.
    *   `app/page.tsx` defines the content of the homepage.
    *   `app/pillars/[slug]/page.tsx` uses Next.js's `generateStaticParams` function to generate a static HTML page for each "Core Pillar" (like WRMB, sWRMB) at **build time**.
    *   This approach provides the best loading performance and SEO results because users download pre-rendered HTML files directly.

### 4.2. Content Management

*   **Hardcoded Content:** The project does **not** use any external CMS (Content Management System) or API to manage content.
*   All text, image paths, news articles, and partner information are directly hardcoded in React components (`.tsx` files). For example, `app/pillars/[slug]/page.tsx` contains a constant object like `PILLARS` internally, looking up and displaying corresponding content based on the `slug` parameter in the URL.
*   **Pros:** Simple and fast development process.
*   **Cons:** Any content modification (even a typo) requires frontend developers to modify code, rebuild, and deploy the entire website.

### 4.3. Blockchain Interaction

*   **No Direct Interaction:** `package.json` does **not** contain any Web3-related libraries, such as `ethers.js`, `web3.js`, `wagmi`, etc.
*   There is no logic in the code for connecting wallets, querying on-chain data, or sending transactions.
*   Call to Action (CTA) buttons on the website, such as "Mint WRMB", are simply HTML links (`<a>` tags) whose `href` attribute points to the URL of an independent DApp application responsible for handling on-chain interactions.

## 5. Conclusion

`cina-official-website` is a static marketing website with a very straightforward technical implementation. Its architecture fully serves its purpose as an information display platform. For developers, maintenance work mainly focuses on modifying hardcoded content in React components and adjusting UI styles.
