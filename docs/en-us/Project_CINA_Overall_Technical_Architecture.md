# CINA Ecosystem: Overall Technical Architecture Summary

## 1. Overview

The technical architecture of the CINA ecosystem features "Multi-Repository, Multi-Protocol, Multi-Tech Stack". It is not a monolithic application but a cluster of microservice-style projects composed of multiple independent protocols interconnected through smart contracts and economic models.

The core philosophy of its architectural design is **Separation of Concerns**: different code repositories carry different business objectives and have selected the most suitable technology stacks for them.

## 2. Tech Stack Summary

Two main categories of technology stacks are primarily used within the ecosystem:

### a. Smart Contracts
*   **Language:** Solidity (`^0.8.x`)
*   **Frameworks:**
    *   **Foundry:** Used for core modules requiring high-intensity testing and performance optimization, such as `v4-pool-amo`.
    *   **Hardhat:** Used for protocols with complex functionality requiring extensive interaction with frontends and scripts, such as `CINA-protocol-contracts`.
    *   The project generally adopts a **Foundry + Hardhat** hybrid mode, balancing development efficiency and test coverage.
*   **Core Design Patterns:**
    *   **Upgradeable Contracts (UUPS):** Core business logic contracts (like AMO) generally adopt the UUPS proxy pattern to facilitate future iterative upgrades.
    *   **Diamond Standard (EIP-2535):** The CINA/f(x) Protocol adopts the Diamond Standard, achieving extremely high modularity and extensibility through "Facet" contracts.

### b. Frontend Applications
*   **Frameworks:**
    *   **Vue.js 3 (Composition API):** Mainly used for internal management tools and relatively straightforward DApps, such as `admin-dapp`, `digital-fund`, `wrmb-dapp`. High development efficiency and mature ecosystem.
    *   **React / Next.js:** Mainly used for applications requiring SEO, complex functionality, or facing a broader public, such as `cina-official-website` (Marketing Site) and `CINA-Dex-trading-system-interface` (Pro Trading Platform).
*   **State Management:**
    *   **Pinia:** Preferred in Vue.js projects.
    *   **TanStack Query (React Query) + Zustand/Context:** Used in React projects to separate server-side cache state and client-side UI state.
*   **Blockchain Interaction:**
    *   **Ethers.js:** Used directly for contract interaction in Vue.js projects.
    *   **Wagmi:** Preferred in React projects, providing powerful Hooks that greatly simplify wallet connection, transaction sending, and on-chain data reading logic.

### c. Backend Services
*   **Language:** Go
*   **Framework:** Gin
*   **Database:** MySQL + GORM
*   **Architecture:** Typical layered architecture (API -> Service -> DAO).

## 3. Codebase Relationships & Technical Interaction Diagram

The diagram below shows the interaction relationships of various code repositories at the technical level.

```mermaid
graph LR
    subgraph Frontend
        D1[wrmb-dapp]
        D2[wrap-dapp]
        D3[CINA-Dex-trading-system-interface]
        D4[admin-dapp]
        D5[digital-fund]
    end

    subgraph Smart Contracts
        P1[WRMB-protocol-contracts]
        P2[CINA-protocol-contracts]
        P3[v4-pool-amo]
        P4[Bancor Carbon Contracts]
        P5[Unknown Fund Contracts]
    end
    
    subgraph Backend_Services
        B1[digital-fund-backend (NFT API)]
    end

    %% Interactions
    D1 & D2 -- "ethers.js" --> P1
    D3 -- "wagmi" --> P4
    D4 -- "ethers.js" --> P1
    D5 -- "ethers.js" --> P5
    
    P3 -- "imports & calls" --> P1
    P3 -- "imports & calls" --> P2
    
    %% Styles
    classDef fe fill:#117A65,stroke:#fff,color:#fff;
    classDef sc fill:#1F618D,stroke:#fff,color:#fff;
    classDef be fill:#9A7D0A,stroke:#fff,color:#fff;
    class D1,D2,D3,D4,D5 fe;
    class P1,P2,P3,P4,P5 sc;
    class B1 be;
```

## 4. Repository Technical Positioning Summary

| Repository Name | Technical Positioning | Core Tech Stack |
| :--- | :--- | :--- |
| **`CINA-protocol-contracts`** | Core contracts of CINA/f(x) Stablecoin Protocol | Solidity, Hardhat, Foundry, EIP-2535 |
| **`WRMB-protocol-contracts`** | Core contracts of WRMB Savings & Yield Protocol | Solidity, Hardhat |
| **`v4-pool-amo`** | Algo Market Operations (AMO) module connecting WRMB and CINA | Solidity, Foundry, Uniswap v4 Hooks |
| **`ETHShanghai-2025`** | Flash loan leverage demo for CINA/f(x) Protocol | Solidity, Hardhat, Next.js, Wagmi |
| **`wrmb-dapp`** | Full-featured main DApp for WRMB Protocol | Vue.js, Ethers.js |
| **`wrap-dapp`** | Lightweight Wrap/Unwrap tool DApp for WRMB Protocol | Vue.js, Ethers.js |
| **`admin-dapp`** | Internal admin dashboard for WRMB Protocol | Vue.js, Pinia, Ethers.js |
| **`CINA-Dex-trading-system-interface`** | Pro trading strategy frontend for Bancor Carbon Protocol | React, Next.js, TanStack (Router/Query), Wagmi |
| **`cina-official-website`** | Static marketing website for the ecosystem | React, Next.js |
| **`digital-fund`** | Digital Fund Admin Panel Frontend (Backend unknown) | Vue.js, Pinia, Ethers.js |
| **`digital-fund-backend`** | NFT Marketplace API Backend (Unrelated to `digital-fund` frontend) | Go, Gin, GORM, MySQL |

## 5. Overall Architecture Conclusion

The technical architecture of the CINA ecosystem is modern, modular, and carefully selected for the specific needs of each component.

*   **Contract Layer** demonstrates a deep understanding and application of the latest industry standards (e.g., EIP-2535, Uniswap v4 Hooks).
*   **Frontend Layer** flexibly selects between Vue and React, two mainstream frameworks, based on application complexity and target audience.
*   **Inter-protocol Interaction** is mainly achieved through direct on-chain smart contract calls, which is clear, transparent, and trustless.

Although this architectural pattern is complex to understand initially, it lays a solid foundation for the long-term expansion, iteration, and maintenance of the entire ecosystem.
