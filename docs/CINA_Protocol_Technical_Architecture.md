# CINA 协议技术架构文档

## 1. 概述

CINA 协议是一套基于 Solidity 的智能合约系统，用于发行和管理去中心化稳定币 FxUSD。该协议是 f(x) protocol 的一个分叉，其技术核心是实现了一个高度可扩展的借贷和清算引擎。

其架构设计的关键目标是**效率**和**可扩展性**，通过采用类似 Uniswap V3 的集中流动性机制来管理债务头寸，极大地降低了在高负载下（大量用户和头寸）的 Gas 消耗和计算复杂度。

## 2. 技术栈

*   **智能合约语言:** Solidity (`^0.8.26`)
*   **开发与测试框架:**
    *   **Hardhat:** 用于编译、部署、测试和脚本编写。
    *   **Foundry:** 用于合约的单元测试和模糊测试。
    *   项目采用了混合框架的模式，结合了两者的优点。
*   **核心依赖:**
    *   **Ethers.js:** 用于与合约进行交互的客户端库。
    *   **OpenZeppelin Contracts:** 广泛使用了其安全合约组件（如 `Ownable`, `ERC721`）。
    *   **TypeChain:** 用于为智能合约生成 TypeScript 类型定义，增强了开发体验和安全性。

## 3. 核心架构

协议的架构可以分为三层：**接口层 (Facets)**、**逻辑中枢 (PoolManager)** 和 **核心引擎 (Pools)**。

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

### 3.1. 接口层: 钻石代理 (EIP-2535)

协议的入口点是一个遵循 EIP-2535 钻石标准的代理合约。这种模式提供了极高的灵活性和可升级性。

*   **功能:** 用户的所-有请求（如开仓、还款）都发送到这个单一地址的代理合约。
*   **Facets (切面):** 具体的业务逻辑被拆分到不同的实现合约中，称为“切面”（位于 `contracts/periphery/facets/`）。例如，`PositionOperateFlashLoanFacetV2.sol` 专门处理与头寸相关的操作。
*   **Delegatecall:** 钻石代理通过 `delegatecall` 将用户的请求路由到对应的切面合约来执行，同时保持了存储和状态在代理合约的上下文中。这使得协议可以在不中断服务或迁移数据的情况下，独立地升级、添加或移除某个功能模块。

### 3.2. 逻辑中枢: `PoolManager.sol`

`PoolManager` 是整个系统的核心协调者。

*   **角色:** 它不直接处理具体资产的逻辑，而是作为一个注册中心和状态机。
*   **功能:**
    *   **池注册 (`registerPool`):** 注册和管理所有抵押品资金池（Pool）。
    *   **操作路由 (`operate`):** 接收来自接口层（Facets）的指令，并将其分派到正确的资金池进行处理。
    *   **全局状态管理:** 负责协议级别的状态，如手续费、开关控制等。
    *   **清算协调:** 协调清算流程，与 `PegKeeper` 配合。

### 3.3. 稳定模块: `PegKeeper.sol`

`PegKeeper` 是一个自主运行的合约，负责维持 FxUSD 的价格锚定。

*   **价格监控:** 它通过一个外部预言机持续获取 FxUSD 在 Curve 等二级市场的价格。
*   **断路器机制:**
    *   当 FxUSD 价格低于锚定阈值时，它会调用 `PoolManager` 暂停新的借款，防止 FxUSD 供应过剩。
    *   当价格恢复时，它会自动重新开启借款功能。
*   **套利激励:** 它控制着一个特殊的赎回机制，允许在价格脱钩时进行套利，从而利用市场力量恢复锚定。

## 4. 核心引擎: 基于 Tick 的头寸管理

这是协议最具创新性的部分，位于每个具体的资金池（Pool）实现中，其核心逻辑在 `PositionLogic.sol` 和 `TickLogic.sol` 中。

### 4.1. 概念: 债务的集中流动性

该系统将债务管理问题转化为一个类似于 Uniswap V3 的集中流动性问题。

*   **Tick (刻度):** 系统定义了大量离散的“刻度”，每个刻度代表一个特定的“债务/抵押品比率”。
*   **聚合:** 所有健康状况相似的头寸被聚合到同一个刻度上。系统只需跟踪每个刻度的总抵押品和总债务，而无需关心单个头寸。

### 4.2. `PositionLogic.sol`: 份额机制

*   **份额转换:** 用户的资产（抵押品和债务）在内部被转换为“份额”（Shares）。`collIndex` 和 `debtIndex` 两个指数会随着利息和收益的累积而变化。
    *   `实际资产 = 份额 * 当前指数`
*   **头寸 NFT:** 每个用户头寸由一个 NFT 代表，其 `PositionInfo` 结构体中存储着用户的份额 (`colls`, `debts`) 和一个关键的指针 `nodeId`。

### 4.3. `TickLogic.sol`: 树状结构与懒更新

*   **`tickTreeData`:** 一个核心的映射，存储着树状结构的所有节点。每个节点 (`TickTreeNode`) 代表一个历史上的 `tick` 状态，包含该状态下的总份额、以及指向父节点的指针和比例调整系数 (`collRatio`, `debtRatio`)。
*   **`tickBitmap`:** 一个位图，用于极速查找当前哪个 `tick` 上存在债务，对于清算流程至关重要。

#### **工作流程详解:**

1.  **开仓 (`_addPositionToTick`):**
    *   根据用户的债务/抵押品比率计算出对应的 `tick`。
    *   获取或创建该 `tick` 的节点 (`TickTreeNode`)。
    *   将用户的抵押品份额和债务份额累加到该节点的总份额上。
    *   用户的 `PositionInfo.nodeId` 指向该节点。

2.  **清算 (`_liquidateTick`):**
    *   当某个 `tick` 因价格变动而整体变为不健康时，清算人触发对该 `tick` 的清算。
    *   清算会减少该 `tick` 对应的树节点的总份额。
    *   **关键步骤:** 清算后，剩余的份额会被移动到一个新的、更健康的 `tick` 上。同时，系统会更新旧节点的元数据，使其 `parent` 指针指向这个新 `tick` 对应的节点，并记录下因本次清算导致的份额缩减比例 (`collRatio`, `debtRatio`)。**这就是树状链条的形成过程。**

3.  **懒更新 (`_getAndUpdatePosition`):**
    *   当用户与其头寸交互时，协议并不知道该头寸自上次交互以来经历了多少次间接的清算。
    *   此时，协议会调用 `_getRootNode`，从用户头寸的 `nodeId` 开始，沿着 `parent` 指针一路向上遍历到根节点。
    *   在遍历过程中，它会累积路径上所有节点的 `collRatio` 和 `debtRatio`。
    *   最终，将这个累积的比例应用到用户最初的份额上，就能计算出用户当前“真实”的抵押品和债务数量。这个过程实现了状态的“懒更新”，极大地提高了系统效率。

## 5. 总结

CINA 协议通过创新的 **Tick-based** 债务管理机制，结合灵活的**钻石代理**架构和自主的**锚定稳定模块**，构建了一个既高效、可扩展又稳健的去中心化稳定币系统。其核心优势在于能够以极低的成本管理海量用户头寸，为 DeFi 生态系统提供了一个强大的金融基础设施。
