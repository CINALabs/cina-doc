# admin-dapp - Technical Architecture Document

## 1. Overview

`admin-dapp` is a Single Page Application (SPA) built on Vue.js 3, serving as the on-chain management dashboard for the WRMB Protocol. Its technology selection is modern, the code structure is clear, and it aims to provide a stable and efficient operating interface for protocol administrators.

## 2. Tech Stack

*   **Core Framework:** [Vue.js 3](https://vuejs.org/) (using Composition API)
*   **Language:** [TypeScript](https://www.typescriptlang.org/)
*   **Build Tool:** [Vite](https://vitejs.dev/)
*   **Routing:** [Vue Router](https://router.vuejs.org/)
*   **State Management:** [Pinia](https://pinia.vuejs.org/) - The official state management library for Vue.js, providing type-safe, modular state storage.
*   **UI Library:** [Naive UI](https://www.naiveui.com/) - A feature-rich, high-performance Vue 3 component library.
*   **Blockchain Interaction:**
    *   **[Ethers.js](https://ethers.io/) v6:** Core blockchain interaction library used for creating contract instances, calling methods, and communicating with Ethereum nodes.
    *   **[Web3Modal](https://web3modal.com/) / [WalletConnect](https://walletconnect.com/):** Used to implement wallet connection functionality, supporting multiple wallet types (like MetaMask, WalletConnect).

## 3. Project Structure

The project adopts a typical Vue 3 + Vite project structure.

```
src/
├── App.vue       # Root component
├── main.ts       # App entry file, initializes Vue, Pinia, Router, etc.
├── assets/       # Static assets
├── components/   # Reusable generic Vue components
├── contracts/    # Core logic for blockchain interaction
│   ├── config.ts # **Key File**: Manages addresses and ABIs for all contracts
│   └── index.ts  # Utility functions for getting contract instances
├── router/       # Vue Router configuration
├── stores/       # Pinia state stores
├── views/        # Page-level components, corresponding to each route
└── ...           # Other utils and type definitions
```

## 4. Core Architecture & Data Flow

### 4.1. State Management (Pinia)

Pinia (`src/stores/`) plays a central role in the application, managing global shared state, mainly including:
*   **Wallet & Connection State:** Stores the current connected wallet Provider, Signer, user address, and Chain ID.
*   **Contract Instances:** Caches created Ethers.js contract instances to avoid duplicate creation.
*   **Global Loading State:** Manages global loading indicators.

### 4.2. Routing (Vue Router)

Vue Router (`src/router/index.ts`) is responsible for defining the page structure of the application. Each route maps to a page-level component in the `views` directory and defines metadata like page title via the `meta` field for dynamic rendering of navigation and breadcrumbs.

### 4.3. Blockchain Interaction Model

The blockchain interaction flow of `admin-dapp` is clear and modular, serving as the cornerstone of the entire application.

**Data Flow:**

1.  **Configuration Layer (`src/contracts/config.ts`):**
    *   This file is the "Source of Truth" for blockchain interaction.
    *   The `CONTRACT_ADDRESSES` object reads from environment variables (`.env`) and stores addresses of all protocol contracts on different networks (like Sepolia, Mainnet).
    *   The `CONTRACT_ABI_MAP` object hardcodes the ABIs (Application Binary Interface) of all relevant contracts.
    *   This centralized management of addresses and ABIs makes updating contract versions or supporting new networks very simple.

2.  **Encapsulation Layer (`src/contracts/index.ts`):**
    *   This file provides a utility function, e.g., `getContract(contractName)`.
    *   This function retrieves the current `signer` or `provider` from the Pinia store, then combines it with the address and ABI provided in `config.ts` to create an interactable contract instance using `new ethers.Contract(address, abi, signer)`.

3.  **View/Logic Layer (`src/views/**/*.vue`):**
    *   When a page component (like `ActiveLiquidity.vue`) needs to interact with a contract, it calls `getContract('ActiveLiquidityAMO')` to get the contract instance.
    *   Methods in the component (like `handleExecuteArbitrage`) call methods on that contract instance, e.g., `await contract.executeArbitrage()`.
    *   Method calls return a Transaction object, and the component can listen to the transaction status (pending, success, failure) and update the UI accordingly (e.g., show loading state, send success notification).

**Example Code Flow:**
```typescript
// In a Vue component inside <script setup>

import { getContract } from '@/contracts';
import { useWalletStore } from '@/stores/wallet'; // Example Pinia store

const walletStore = useWalletStore();

async function handleUpdateParameters() {
  if (!walletStore.signer) {
    // Prompt user to connect wallet
    return;
  }

  // 1. Get contract instance (already connected to the user's signer)
  const amoContract = getContract('ActiveLiquidityAMO', walletStore.signer);

  try {
    // 2. Call the contract method
    const tx = await amoContract.updateParameters(...); // Pass new parameters

    // 3. Wait for transaction to be mined and update UI
    console.log('Transaction sent:', tx.hash);
    await tx.wait();
    console.log('Transaction confirmed!');
    // Show success notification
  } catch (error) {
    // Handle error
    console.error('Transaction failed:', error);
  }
}
```
This layered, clear architecture makes `admin-dapp` a robust and easy-to-maintain management tool.
