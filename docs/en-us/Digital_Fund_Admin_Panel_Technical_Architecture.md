# Digital Fund Admin Panel - Technical Architecture Document

## 1. Overview

`digital-fund` is a Single Page Application (SPA) built on Vue.js 3, serving as the internal management interface for the "Digital Fund". Its technical architecture is similar to `admin-dapp`, adopting the mainstream tech stack in the Vue 3 ecosystem, aiming to provide a responsive, stable, and easy-to-maintain management tool.

## 2. Tech Stack

*   **Core Framework:** [Vue.js 3](https://vuejs.org/) (using Composition API)
*   **Language:** [TypeScript](https://www.typescriptlang.org/)
*   **Build Tool:** [Vite](https://vitejs.dev/)
*   **Routing:** [Vue Router](https://router.vuejs.org/)
*   **State Management:** [Pinia](https://pinia.vuejs.org/)
*   **UI Library:** No large third-party component library used; adopts a custom component pattern.
*   **Blockchain Interaction:** [Ethers.js](https://ethers.io/) v6

## 3. Project Structure

The project follows a typical Vue 3 + Vite project structure, very similar to `admin-dapp`.

```
src/
├── App.vue       # Root component
├── main.ts       # App entry
├── assets/       # Static assets
├── components/   # Reusable generic Vue components
├── config/       # App configuration, mainly blockchain network RPC addresses
├── router/       # Vue Router configuration
├── stores/       # Pinia state stores
├── views/        # Page-level components
└── ...
```

## 4. Core Architecture & Data Flow

### 4.1. Routing (Vue Router)

The `src/router/index.ts` file defines all pages and corresponding access paths of the application. This is the key entry point for understanding application functionality. The route configuration reveals the core business modules of the application, including:

*   `/dashboard`
*   `/nav-management` (NAV Management)
*   `/mint-management` (Mint Request Management)
*   `/burn-management` (Burn Request Management)
*   `/blacklist-management` (Blacklist Management)
*   `/contract-management` (Contract Management)

### 4.2. State Management (Pinia)

Pinia (`src/stores/`) is used to manage global state shared across components or pages.
*   **`walletStore` (Example):** A typical store used to store user wallet connection information, such as `provider`, `signer`, user address, and Chain ID.
*   **Data Caching:** Pinia stores can also be used to cache data fetched from the blockchain or backend API to avoid duplicate requests.

### 4.3. Data Interaction Model

The functions of `digital-fund` (like "Request Management") strongly suggest it adopts a **Frontend-Backend-Blockchain** hybrid interaction model.

#### 4.3.1. Interaction with Backend API (Inferred)

*   **Purpose:** Handle business processes requiring off-chain storage, approval, and processing. For example, when an investor submits a "Mint Request", the request needs to be persisted for admins to view and approve.
*   **Flow (Inferred):**
    1.  Frontend page (like `MintManagement.vue`) sends an HTTP request (e.g., `POST /api/mint-requests`) to the backend API via `fetch` or `axios`.
    2.  Backend service receives the request and creates a new mint request record in the database with status "Pending".
    3.  Admin refreshes the frontend interface; frontend gets the list of all pending requests via `GET /api/mint-requests` from the backend and displays them.
    4.  Admin clicks "Approve" button; frontend sends `POST /api/mint-requests/{id}/approve`.
*   **Status:** **The `digital-fund-backend` repository in this project is NOT the backend for this panel.** The real backend service is **unknown** within the current analysis scope.

#### 4.3.2. Direct Interaction with Blockchain

*   **Purpose:** Execute final admin operations that need to be on-chain.
*   **Flow:**
    1.  **Get Contract Instance:** The app creates an interactable contract object via a utility function (similar to `getContract(contractName)`), using `ethers.js`, the `signer` stored in Pinia store, and pre-configured contract address and ABI.
    2.  **Call Method:** When an admin approves a request and needs to execute an on-chain operation (e.g., minting tokens for a user), the frontend calls the corresponding method on the contract instance, like `await fundContract.mint(recipientAddress, amount)`.
    3.  **Transaction Processing:** Frontend listens to the transaction lifecycle (sent, confirmed, failed) and provides real-time status feedback to the user.
*   **Configuration:** Blockchain-related configurations, such as RPC node addresses, are located in `src/config/index.ts`.

## 5. Conclusion

`digital-fund` is a Vue.js frontend application with a clear architecture, serving as an internal management tool for the Digital Fund. It is technically very similar to `admin-dapp`. Its complete business process relies on a currently unknown backend service to handle off-chain approval flows, combined with Ethers.js to interact directly with smart contracts to execute final on-chain management operations.
