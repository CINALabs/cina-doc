# CINA 生态系统：整体技术架构总结

## 1. 概述

CINA 生态系统的技术架构呈现出“多仓库、多协议、多技术栈”的特点。它并非一个单体应用，而是一个由多个独立的、通过智能合约和经济模型相互关联的微服务式项目群。

其架构设计的核心思想是**关注点分离**：不同的代码仓库承载不同的业务目标，并为其选择了最适合的技术栈。

## 2. 技术栈总结

生态系统内主要使用了两大类技术栈：

### a. 智能合约
*   **语言:** Solidity (`^0.8.x`)
*   **框架:**
    *   **Foundry:** 用于需要高强度测试和性能优化的核心模块，如 `v4-pool-amo`。
    *   **Hardhat:** 用于功能复杂、需要与前端和脚本进行大量交互的协议，如 `CINA-protocol-contracts`。
    *   项目普遍采用 **Foundry + Hardhat** 的混合模式，兼顾了开发效率和测试覆盖率。
*   **核心设计模式:**
    *   **可升级合约 (UUPS):** 核心业务逻辑合约（如 AMO）普遍采用 UUPS 代理模式，以便于未来迭代升级。
    *   **钻石标准 (EIP-2535):** CINA/f(x) 协议采用了钻石标准，通过“切面 (Facet)”合约实现了极高的模块化和可扩展性。

### b. 前端应用
*   **框架:**
    *   **Vue.js 3 (Composition API):** 主要用于内部管理工具和功能相对直接的 DApp，如 `admin-dapp`, `digital-fund`, `wrmb-dapp`。其开发效率高，生态成熟。
    *   **React / Next.js:** 主要用于需要 SEO、功能复杂或面向更广泛公众的应用，如 `cina-official-website` (营销官网) 和 `CINA-Dex-trading-system-interface` (专业交易平台)。
*   **状态管理:**
    *   **Pinia:** 在 Vue.js 项目中作为首选。
    *   **TanStack Query (React Query) + Zustand/Context:** 在 React 项目中用于分离服务端缓存状态和客户端 UI 状态。
*   **区块链交互:**
    *   **Ethers.js:** 在 Vue.js 项目中被直接用于和合约交互。
    *   **Wagmi:** 在 React 项目中作为首选，它提供了强大的 Hooks，极大地简化了钱包连接、交易发送和链上数据读取的逻辑。

### c. 后端服务
*   **语言:** Go
*   **框架:** Gin
*   **数据库:** MySQL + GORM
*   **架构:** 典型的分层架构（API -> Service -> DAO）。

## 3. 代码库关系与技术交互图

下图展示了各个代码仓库在技术层面的交互关系。

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

    %% 交互关系
    D1 & D2 -- "ethers.js" --> P1
    D3 -- "wagmi" --> P4
    D4 -- "ethers.js" --> P1
    D5 -- "ethers.js" --> P5
    
    P3 -- "imports & calls" --> P1
    P3 -- "imports & calls" --> P2
    
    %% 样式
    classDef fe fill:#117A65,stroke:#fff,color:#fff;
    classDef sc fill:#1F618D,stroke:#fff,color:#fff;
    classDef be fill:#9A7D0A,stroke:#fff,color:#fff;
    class D1,D2,D3,D4,D5 fe;
    class P1,P2,P3,P4,P5 sc;
    class B1 be;
```

## 4. 各仓库技术定位总结

| 仓库名称                               | 技术定位                                                     | 核心技术栈                                       |
| -------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------ |
| **`CINA-protocol-contracts`**          | CINA/f(x) 稳定币协议的核心合约                               | Solidity, Hardhat, Foundry, EIP-2535             |
| **`WRMB-protocol-contracts`**          | WRMB 储蓄与收益协议的核心合约                                | Solidity, Hardhat                                |
| **`v4-pool-amo`**                      | 连接 WRMB 和 CINA 协议的算法市场操作 (AMO) 模块              | Solidity, Foundry, Uniswap v4 Hooks              |
| **`ETHShanghai-2025`**                 | CINA/f(x) 协议的闪电贷杠杆功能演示                           | Solidity, Hardhat, Next.js, Wagmi                |
| **`wrmb-dapp`**                        | WRMB 协议的全功能主 DApp                                     | Vue.js, Ethers.js                                |
| **`wrap-dapp`**                        | WRMB 协议的轻量级封装/解封装工具 DApp                        | Vue.js, Ethers.js                                |
| **`admin-dapp`**                       | WRMB 协议的内部管理后台                                      | Vue.js, Pinia, Ethers.js                         |
| **`CINA-Dex-trading-system-interface`** | Bancor Carbon 协议的专业交易策略前端                         | React, Next.js, TanStack (Router/Query), Wagmi   |
| **`cina-official-website`**            | 生态系统的静态营销官网                                       | React, Next.js                                   |
| **`digital-fund`**                     | 数字基金管理后台前端 (后端未知)                              | Vue.js, Pinia, Ethers.js                         |
| **`digital-fund-backend`**             | NFT 市场 API 后端 (与 `digital-fund` 前端无关)               | Go, Gin, GORM, MySQL                             |

## 5. 整体架构结论

CINA 生态系统的技术架构是现代化的、模块化的，并根据每个组件的具体需求精心选择了合适的技术。

*   **合约层**展现了对行业最新标准（如 EIP-2535, Uniswap v4 Hooks）的深入理解和应用。
*   **前端层**根据应用的复杂度和目标受众，灵活选用了 Vue 和 React 两大主流框架。
*   **协议间的交互**主要通过链上智能合约直接调用来实现，清晰、透明且去信任。

这种架构模式虽然在初次理解时较为复杂，但为整个生态系统的长期扩展、迭代和维护奠定了坚实的基础。
