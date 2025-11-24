# CINA DEX (Carbon Protocol) 技术架构文档

## 1. 概述

CINA DEX Trading System Interface 是一个基于 React 和 Vite 构建的现代化单页应用（SPA）。它作为 Bancor Carbon 协议的用户界面，为用户提供了创建和管理链上自动化交易策略的能力。

该项目的技术架构设计精良，采用了行业推荐的最新实践，实现了类型安全、组件化和逻辑分离，具有良好的可维护性和扩展性。

## 2. 技术栈

*   **核心框架:** [React](https://react.dev/) 18, [Vite](https://vitejs.dev/)
*   **开发语言:** [TypeScript](https://www.typescriptlang.org/)
*   **路由管理:** [TanStack Router](https://tanstack.com/router/) - 一个完全类型安全的路由库，其将路由配置和状态（包括搜索参数）集成到应用类型系统中。
*   **服务端状态与缓存:** [TanStack Query (React Query)](https://tanstack.com/query/) - 用于获取、缓存和同步异步数据（包括区块链数据），极大地简化了数据获取和加载状态的管理。
*   **区块链交互:**
    *   **[Wagmi](https://wagmi.sh/):** 核心的 React Hooks 库，用于处理钱包连接、网络切换、交易签名和合约调用等所有与以太坊的直接交互。
    *   **[Ethers.js](https://ethers.io/):** 被 Wagmi 底层使用，提供了与以太坊节点通信和处理区块链数据结构的核心功能。
    *   **[@bancor/carbon-sdk](https://www.npmjs.com/package/@bancor/carbon-sdk):** 一个关键的辅助库，用于处理 Carbon 协议复杂的业务逻辑，特别是将用户输入的策略参数（价格、预算）编码为智能合约调用所需的数据格式。
*   **UI 组件库:** 无特定的第三方组件库（如 Material-UI），项目采用自定义的 CSS Modules 和组件，以实现高度定制化的视觉风格。
*   **代码生成:** [TypeChain](https://github.com/dethcrypto/TypeChain) - 用于根据智能合约的 ABI 自动生成 TypeScript 类型定义，使得与合约的交互完全类型安全。

## 3. 项目结构

项目遵循功能优先的目录结构，清晰地分离了不同层面的关注点。

```
src/
├── abis/         # 智能合约的 ABI JSON 文件和 TypeChain 生成的类型
├── assets/       # 图片、SVG 等静态资源
├── components/   # 可复用的 React 组件 (如 Button, Modal, Chart)
│   └── strategies/ # 与策略相关的核心组件 (如 CreateForm, StrategyChart)
├── config/       # 应用配置，包括各链的合约地址
├── hooks/        # 自定义的 React Hooks (如 useApproval, useCreateStrategy)
├── libs/         # 第三方库的封装和核心工具函数
│   ├── queries/  # TanStack Query 的查询和变更 (mutations) 定义
│   ├── routing/  # TanStack Router 的路由树定义
│   └── wagmi/    # Wagmi 客户端的配置
├── pages/        # 对应于每个路由的页面级组件
├── services/     # 外部服务 (如事件分析)
├── store/        # 全局 UI 状态管理 (Zustand)
└── utils/        # 通用的辅助函数
```

## 4. 核心架构与数据流

### 4.1. 状态管理策略

项目采用了现代前端推荐的混合状态管理模式：

*   **UI 状态:** 使用 [Zustand](https://github.com/pmndrs/zustand) (`src/store/`) 管理全局的、与 UI 相关的简单状态，例如当前选择的法币类型。
*   **URL 状态:** 使用 TanStack Router 将瞬态的、可分享的表单状态（如策略创建时的价格范围、点差等）存储在 URL 的搜索参数中。这提供了出色的用户体验，允许用户刷新页面或分享链接而不会丢失进度。
*   **服务端/区块链状态:** 所有来自区块链或后端 API 的异步数据都由 TanStack Query (`src/libs/queries/`) 管理。它负责处理数据的获取、缓存、后台刷新和失效，避免了重复请求，并自动管理加载和错误状态。

### 4.2. “创建策略”端到端数据流

这是理解该应用如何与区块链交互的最佳示例。

1.  **UI 层 (`/pages/trade/overlapping.tsx`):**
    *   用户在 `CreateOverlappingPrice` 和 `CreateOverlappingBudget` 组件中输入策略参数。
    *   这些参数通过回调函数被存储到 URL 的搜索参数中。
    *   用户点击 `CreateForm` 组件中的“Create”按钮，触发表单的 `onSubmit` 事件。

2.  **表单逻辑层 (`CreateForm.tsx`):**
    *   `onSubmit` 事件处理器调用 `createStrategy()` 函数。
    *   这个 `createStrategy` 函数来自 `useCreateStrategy` Hook。

3.  **Hook 逻辑层 (`useCreateStrategy.ts`):**
    *   **获取参数:** Hook 从其 props 中接收到策略的完整参数（交易对、买卖订单配置）。
    *   **检查授权:** 调用 `useApproval` Hook，检查 Carbon 合约地址（`spenderAddress`）是否已被授权足额的代币。
    *   **发起授权 (如果需要):** 如果授权不足，`useApproval` Hook 内部会使用 Wagmi 的 `useContractWrite` 来准备并发送一笔 `approve` 交易。
    *   **发起创建 (授权后):**
        *   调用 `useCreateStrategyQuery` Hook 返回的 `mutation.mutate()` 函数。
        *   `useCreateStrategyQuery` 是对 TanStack Query `useMutation` 的封装。其核心 `mutationFn` 如下：
            1.  **SDK 编码:** 调用 `@bancor/carbon-sdk` 的相关函数，将前端的策略参数（如 `{ min: '1800', max: '1900', budget: '1000' }`）转换为智能合约 `createStrategy` 函数所需的复杂字节码。
            2.  **Wagmi 发送交易:** 使用 Wagmi 的 `useContractWrite` Hook，将编码后的交易数据发送到区块链。

4.  **交易后处理 (在 `useCreateStrategy` Hook 中):**
    *   交易被发送后，`onSuccess` 回调被触发。
    *   应用会等待交易被确认 (`tx.wait()`)。
    *   确认后，它会使相关的 TanStack Query 缓存失效（如 `QueryKey.strategiesByUser`），这会触发 UI 自动重新获取最新的策略列表和用户余额。

这个流程清晰地展示了各层如何协作：UI 组件负责用户输入，自定义 Hooks 封装业务逻辑和交易状态，而 Wagmi 和 SDK 则处理底层的区块链交互细节。
