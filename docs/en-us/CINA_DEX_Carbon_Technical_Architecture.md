# CINA DEX (Carbon Protocol) Technical Architecture Document

## 1. Overview

CINA DEX Trading System Interface is a modern Single Page Application (SPA) built with React and Vite. It serves as the user interface for the Bancor Carbon Protocol, providing users with the ability to create and manage on-chain automated trading strategies.

The project's technical architecture is well-designed, adopting latest industry recommended practices, achieving type safety, componentization, and logic separation, with good maintainability and scalability.

## 2. Tech Stack

*   **Core Framework:** [React](https://react.dev/) 18, [Vite](https://vitejs.dev/)
*   **Language:** [TypeScript](https://www.typescriptlang.org/)
*   **Routing:** [TanStack Router](https://tanstack.com/router/) - A fully type-safe router library that integrates route configuration and state (including search params) into the app's type system.
*   **Server State & Caching:** [TanStack Query (React Query)](https://tanstack.com/query/) - Used for fetching, caching, and synchronizing asynchronous data (including blockchain data), greatly simplifying data fetching and loading state management.
*   **Blockchain Interaction:**
    *   **[Wagmi](https://wagmi.sh/):** Core React Hooks library for handling wallet connection, network switching, transaction signing, and contract calls, covering all direct interactions with Ethereum.
    *   **[Ethers.js](https://ethers.io/):** Used under the hood by Wagmi, providing core functions for communicating with Ethereum nodes and processing blockchain data structures.
    *   **[@bancor/carbon-sdk](https://www.npmjs.com/package/@bancor/carbon-sdk):** A key helper library for handling complex business logic of the Carbon Protocol, especially encoding user-input strategy parameters (price, budget) into data formats required for smart contract calls.
*   **UI Library:** No specific third-party component library (like Material-UI); the project uses custom CSS Modules and components to achieve a highly customized visual style.
*   **Code Generation:** [TypeChain](https://github.com/dethcrypto/TypeChain) - Used to automatically generate TypeScript type definitions from smart contract ABIs, making contract interactions fully type-safe.

## 3. Project Structure

The project follows a feature-first directory structure, clearly separating concerns at different levels.

```
src/
├── abis/         # Smart contract ABI JSON files and TypeChain generated types
├── assets/       # Static assets like images, SVGs
├── components/   # Reusable React components (Button, Modal, Chart)
│   └── strategies/ # Core components related to strategies (CreateForm, StrategyChart)
├── config/       # App config, including contract addresses for each chain
├── hooks/        # Custom React Hooks (useApproval, useCreateStrategy)
├── libs/         # Wrappers for third-party libraries and core utility functions
│   ├── queries/  # TanStack Query definitions (queries & mutations)
│   ├── routing/  # TanStack Router route tree definition
│   └── wagmi/    # Wagmi client configuration
├── pages/        # Page-level components corresponding to each route
├── services/     # External services (like analytics)
├── store/        # Global UI state management (Zustand)
├── utils/        # General utility functions
```

## 4. Core Architecture & Data Flow

### 4.1. State Management Strategy

The project adopts a hybrid state management pattern recommended for modern frontends:

*   **UI State:** Uses [Zustand](https://github.com/pmndrs/zustand) (`src/store/`) to manage global, UI-related simple state, such as currently selected fiat currency.
*   **URL State:** Uses TanStack Router to store transient, shareable form state (like price range, spread during strategy creation) in URL search parameters. This provides excellent UX, allowing users to refresh pages or share links without losing progress.
*   **Server/Blockchain State:** All asynchronous data from blockchain or backend APIs is managed by TanStack Query (`src/libs/queries/`). It handles data fetching, caching, background refreshing, and invalidation, avoiding duplicate requests and automatically managing loading and error states.

### 4.2. "Create Strategy" End-to-End Data Flow

This is the best example to understand how the app interacts with the blockchain.

1.  **UI Layer (`/pages/trade/overlapping.tsx`):**
    *   User inputs strategy parameters in `CreateOverlappingPrice` and `CreateOverlappingBudget` components.
    *   These parameters are stored in URL search parameters via callback functions.
    *   User clicks "Create" button in `CreateForm` component, triggering form `onSubmit` event.

2.  **Form Logic Layer (`CreateForm.tsx`):**
    *   `onSubmit` handler calls `createStrategy()` function.
    *   This `createStrategy` function comes from `useCreateStrategy` Hook.

3.  **Hook Logic Layer (`useCreateStrategy.ts`):**
    *   **Get Params:** Hook receives full strategy parameters (pair, buy/sell order config) from its props.
    *   **Check Approval:** Calls `useApproval` Hook to check if Carbon contract address (`spenderAddress`) has sufficient token allowance.
    *   **Initiate Approval (If needed):** If allowance is insufficient, `useApproval` Hook internally uses Wagmi's `useContractWrite` to prepare and send an `approve` transaction.
    *   **Initiate Creation (After Approval):**
        *   Calls `mutation.mutate()` function returned by `useCreateStrategyQuery` Hook.
        *   `useCreateStrategyQuery` is a wrapper around TanStack Query `useMutation`. Its core `mutationFn` is as follows:
            1.  **SDK Encoding:** Calls relevant functions from `@bancor/carbon-sdk` to convert frontend strategy parameters (e.g., `{ min: '1800', max: '1900', budget: '1000' }`) into complex bytecode required for smart contract `createStrategy` function.
            2.  **Wagmi Send Transaction:** Uses Wagmi's `useContractWrite` Hook to send the encoded transaction data to the blockchain.

4.  **Post-Transaction Handling (In `useCreateStrategy` Hook):**
    *   After transaction is sent, `onSuccess` callback is triggered.
    *   App waits for transaction confirmation (`tx.wait()`).
    *   After confirmation, it invalidates relevant TanStack Query caches (like `QueryKey.strategiesByUser`), triggering UI to automatically refetch the latest strategy list and user balances.

This flow clearly demonstrates how layers collaborate: UI components handle user input, custom Hooks encapsulate business logic and transaction state, while Wagmi and SDK handle low-level blockchain interaction details.
