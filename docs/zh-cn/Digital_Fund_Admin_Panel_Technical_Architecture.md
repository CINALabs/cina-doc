# 数字基金管理后台 - 技术架构文档

## 1. 概述

`digital-fund` 是一个基于 Vue.js 3 构建的单页应用（SPA），作为“数字基金”的内部管理界面。其技术架构与 `admin-dapp` 类似，采用了 Vue 3 生态系统中的主流技术栈，旨在提供一个响应式、稳定且易于维护的管理工具。

## 2. 技术栈

*   **核心框架:** [Vue.js 3](https://vuejs.org/) (使用 Composition API)
*   **开发语言:** [TypeScript](https://www.typescriptlang.org/)
*   **构建工具:** [Vite](https://vitejs.dev/)
*   **路由管理:** [Vue Router](https://router.vuejs.org/)
*   **状态管理:** [Pinia](https://pinia.vuejs.org/)
*   **UI 组件库:** 未使用大型第三方组件库，采用了自定义组件的模式。
*   **区块链交互:** [Ethers.js](https://ethers.io/) v6

## 3. 项目结构

项目遵循典型的 Vue 3 + Vite 项目结构，与 `admin-dapp` 的结构非常相似。

```
src/
├── App.vue       # 根组件
├── main.ts       # 应用入口
├── assets/       # 静态资源
├── components/   # 可复用的通用 Vue 组件
├── config/       # 应用配置，主要是区块链网络 RPC 地址
├── router/       # Vue Router 的路由配置文件
├── stores/       # Pinia 的状态存储模块
├── views/        # 页面级组件
└── ...
```

## 4. 核心架构与数据流

### 4.1. 路由 (Vue Router)

`src/router/index.ts` 文件定义了应用的所有页面和对应的访问路径。这是理解应用功能的关键入口。路由配置揭示了该应用的核心业务模块，包括：

*   `/dashboard`
*   `/nav-management` (资产净值管理)
*   `/mint-management` (铸造请求管理)
*   `/burn-management` (销毁请求管理)
*   `/blacklist-management` (黑名单管理)
*   `/contract-management` (合约管理)

### 4.2. 状态管理 (Pinia)

Pinia (`src/stores/`) 用于管理需要跨组件或跨页面共享的全局状态。
*   **`walletStore` (示例):** 一个典型的 store，用于存储用户的钱包连接信息，如 `provider`, `signer`, 用户地址和链 ID。
*   **数据缓存:** Pinia store 也可用于缓存从区块链或后端 API 获取的数据，以避免重复请求。

### 4.3. 数据交互模型

`digital-fund` 的功能（如“请求管理”）强烈暗示其采用了**前端-后端-区块链**的混合交互模型。

#### 4.3.1. 与后端 API 的交互 (推测)

*   **目的:** 处理需要链下存储、审批和处理的业务流程。例如，当一个投资者提交“铸造请求”时，该请求需要被持久化存储以便管理员查看和审批。
*   **流程 (推测):**
    1.  前端页面（如 `MintManagement.vue`）通过 `fetch` 或 `axios` 向后端 API 发送一个 HTTP 请求（例如 `POST /api/mint-requests`）。
    2.  后端服务接收请求，在数据库中创建一条新的铸造请求记录，状态为“待处理”。
    3.  管理员在前端界面刷新，前端向后端 `GET /api/mint-requests` 获取所有待处理的请求列表并展示。
    4.  管理员点击“批准”按钮，前端发送 `POST /api/mint-requests/{id}/approve`。
*   **现状:** **本项目的 `digital-fund-backend` 仓库并非此后台的后端。** 真正的后端服务在当前分析范围内是**未知**的。

#### 4.3.2. 与区块链的直接交互

*   **目的:** 执行最终的、需要上链的管理员操作。
*   **流程:**
    1.  **获取合约实例:** 应用通过一个工具函数（类似于 `getContract(contractName)`），使用 `ethers.js`、Pinia store 中存储的 `signer`、以及预先配置好的合约地址和 ABI，来创建一个可交互的合约对象。
    2.  **调用方法:** 当管理员批准一个请求并需要执行链上操作时（例如，为用户铸造代币），前端会调用合约实例上的相应方法，如 `await fundContract.mint(recipientAddress, amount)`。
    3.  **交易处理:** 前端监听交易的生命周期（发送、确认、失败），并向用户提供实时的状态反馈。
*   **配置:** 区块链相关的配置，如 RPC 节点地址，位于 `src/config/index.ts` 中。

## 5. 结论

`digital-fund` 是一个架构清晰的 Vue.js 前端应用，作为数字基金的内部管理工具。它在技术上与 `admin-dapp` 非常相似。其完整的业务流程依赖于一个当前未知的后端服务来处理链下审批流，并结合 Ethers.js 直接与智能合约交互来执行最终的链上管理操作。
