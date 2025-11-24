# CINA Protocol Technical Architecture Document

## 1. Overview

The CINA Protocol is a Solidity-based smart contract system for issuing and managing the decentralized stablecoin FxUSD. The protocol is a fork of f(x) protocol, and its technical core is the implementation of a highly scalable lending and liquidation engine.

The key goals of its architectural design are **Efficiency** and **Scalability**. By adopting a concentrated liquidity mechanism similar to Uniswap V3 to manage debt positions, it drastically reduces Gas consumption and computational complexity under high load (large number of users and positions).

## 2. Tech Stack

*   **Smart Contract Language:** Solidity (`^0.8.26`)
*   **Development & Testing Frameworks:**
    *   **Hardhat:** Used for compilation, deployment, testing, and scripting.
    *   **Foundry:** Used for unit testing and fuzzing of contracts.
    *   The project adopts a hybrid framework mode, combining the advantages of both.
*   **Core Dependencies:**
    *   **Ethers.js:** Client library for interacting with contracts.
    *   **OpenZeppelin Contracts:** Widely uses its secure contract components (such as `Ownable`, `ERC721`).
    *   **TypeChain:** Used to generate TypeScript type definitions for smart contracts, enhancing development experience and safety.

## 3. Core Architecture

The protocol's architecture can be divided into three layers: **Interface Layer (Facets)**, **Logic Hub (PoolManager)**, and **Core Engine (Pools)**.

```mermaid
graph TD
    subgraph User Interaction
        User
    end

    subgraph Protocol Contracts
        A[Diamond Proxy / Router] --- B{PoolManager};
        subgraph Facets (EIP-2535)
            F1[PositionFacet]
            F2[FxUSDFacet]
            F3[SavingFacet]
        end
        B --- C1[WETH Pool];
        B --- C2[stETH Pool];
        B --- C3[...other Pools];
        C1 -- inherits from --> D{BasePool};
        D -- contains --> E[PositionLogic];
        E -- inherits from --> F[TickLogic];
    end

    subgraph Stability Module
        PK[PegKeeper]
    end

    subgraph External Dependencies
        PO[Price Oracle]
        CP[Curve Pool]
    end

    User --> A;
    A -- delegates calls to --> F1;
    A -- delegates calls to --> F2;
    A -- delegates calls to --> F3;
    F1 -- calls --> B;
    F2 -- calls --> B;
    B -- uses --> PO;
    PK -- monitors --> CP;
    PK -- controls --> B;
```

### 3.1. Interface Layer: Diamond Proxy (EIP-2535)

The entry point of the protocol is a proxy contract following the EIP-2535 Diamond Standard. This pattern provides extremely high flexibility and upgradeability.

*   **Function:** All user requests (such as opening positions, repayment) are sent to this single address proxy contract.
*   **Facets:** Specific business logic is split into different implementation contracts called "Facets" (located in `contracts/periphery/facets/`). For example, `PositionOperateFlashLoanFacetV2.sol` specifically handles position-related operations.
*   **Delegatecall:** The Diamond Proxy routes user requests to the corresponding Facet contract via `delegatecall` for execution, while keeping storage and state within the context of the proxy contract. This allows the protocol to independently upgrade, add, or remove a functional module without interrupting service or migrating data.

### 3.2. Logic Hub: `PoolManager.sol`

`PoolManager` is the core coordinator of the entire system.

*   **Role:** It does not directly handle the logic of specific assets but acts as a registry and state machine.
*   **Function:**
    *   **Pool Registration (`registerPool`):** Registers and manages all collateral pools.
    *   **Operation Routing (`operate`):** Receives instructions from the Interface Layer (Facets) and dispatches them to the correct pool for processing.
    *   **Global State Management:** Responsible for protocol-level state, such as fees, toggle controls, etc.
    *   **Liquidation Coordination:** Coordinates the liquidation process in conjunction with `PegKeeper`.

### 3.3. Stability Module: `PegKeeper.sol`

`PegKeeper` is an autonomously running contract responsible for maintaining the price peg of FxUSD.

*   **Price Monitoring:** It continuously obtains the price of FxUSD in secondary markets like Curve via an external oracle.
*   **Circuit Breaker Mechanism:**
    *   When the FxUSD price falls below the peg threshold, it calls `PoolManager` to pause new borrowing, preventing FxUSD oversupply.
    *   When the price recovers, it automatically re-enables borrowing.
*   **Arbitrage Incentive:** It controls a special redemption mechanism that allows arbitrage when the price de-pegs, thereby using market forces to restore the peg.

## 4. Core Engine: Tick-based Position Management

This is the most innovative part of the protocol, located in each specific Pool implementation, with its core logic in `PositionLogic.sol` and `TickLogic.sol`.

### 4.1. Concept: Concentrated Liquidity for Debt

The system transforms the debt management problem into a concentrated liquidity problem similar to Uniswap V3.

*   **Tick:** The system defines a large number of discrete "Ticks", each representing a specific "Debt/Collateral Ratio".
*   **Aggregation:** All positions with similar health status are aggregated onto the same Tick. The system only needs to track the total collateral and total debt of each Tick, without caring about individual positions.

### 4.2. `PositionLogic.sol`: Share Mechanism

*   **Share Conversion:** User assets (collateral and debt) are internally converted into "Shares". Two indices, `collIndex` and `debtIndex`, change with the accumulation of interest and yield.
    *   `Actual Assets = Shares * Current Index`
*   **Position NFT:** Each user position is represented by an NFT, whose `PositionInfo` struct stores the user's shares (`colls`, `debts`) and a key pointer `nodeId`.

### 4.3. `TickLogic.sol`: Tree Structure & Lazy Update

*   **`tickTreeData`:** A core mapping storing all nodes of the tree structure. Each node (`TickTreeNode`) represents a historical `tick` state, containing the total shares under that state, as well as a pointer to the parent node and ratio adjustment coefficients (`collRatio`, `debtRatio`).
*   **`tickBitmap`:** A bitmap used for extremely fast lookup of which `tick` currently has debt, crucial for the liquidation process.

#### **Workflow Details:**

1.  **Open Position (`_addPositionToTick`):**
    *   Calculate the corresponding `tick` based on the user's debt/collateral ratio.
    *   Get or create the node (`TickTreeNode`) for that `tick`.
    *   Add the user's collateral shares and debt shares to the total shares of that node.
    *   User's `PositionInfo.nodeId` points to that node.

2.  **Liquidation (`_liquidateTick`):**
    *   When a `tick` becomes unhealthy overall due to price changes, a liquidator triggers liquidation for that `tick`.
    *   Liquidation reduces the total shares of the corresponding tree node.
    *   **Key Step:** After liquidation, the remaining shares are moved to a new, healthier `tick`. Meanwhile, the system updates the metadata of the old node, pointing its `parent` pointer to the node corresponding to this new `tick`, and recording the share reduction ratio (`collRatio`, `debtRatio`) caused by this liquidation. **This is the process of forming the tree chain.**

3.  **Lazy Update (`_getAndUpdatePosition`):**
    *   When a user interacts with their position, the protocol does not know how many indirect liquidations the position has undergone since the last interaction.
    *   At this point, the protocol calls `_getRootNode`, traversing from the user position's `nodeId` up along the `parent` pointers to the root node.
    *   During traversal, it accumulates the `collRatio` and `debtRatio` of all nodes on the path.
    *   Finally, applying this accumulated ratio to the user's initial shares calculates the user's current "real" collateral and debt amounts. This process implements "lazy update" of state, greatly improving system efficiency.

## 5. Summary

The CINA Protocol constructs a decentralized stablecoin system that is efficient, scalable, and robust through an innovative **Tick-based** debt management mechanism, combined with a flexible **Diamond Proxy** architecture and an autonomous **Peg Stability Module**. Its core advantage lies in the ability to manage massive user positions at extremely low cost, providing a powerful financial infrastructure for the DeFi ecosystem.
