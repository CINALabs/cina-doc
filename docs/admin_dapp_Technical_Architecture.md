# admin-dapp - 技术架构文档

## 1. 概述

`admin-dapp` 是一个基于 Vue.js 3 构建的单页应用（SPA），作为 WRMB 协议的链上管理后台。其技术选型现代化，代码结构清晰，旨在为协议管理员提供一个稳定、高效的操作界面。

## 2. 技术栈

*   **核心框架:** [Vue.js 3](https://vuejs.org/) (使用 Composition API)
*   **开发语言:** [TypeScript](https://www.typescriptlang.org/)
*   **构建工具:** [Vite](https://vitejs.dev/)
*   **路由管理:** [Vue Router](https://router.vuejs.org/)
*   **状态管理:** [Pinia](https://pinia.vuejs.org/) - Vue.js 官方推荐的状态管理库，提供了类型安全、模块化的状态存储。
*   **UI 组件库:** [Naive UI](https://www.naiveui.com/) - 一个功能丰富、性能优秀的 Vue 3 组件库。
*   **区块链交互:**
    *   **[Ethers.js](https://ethers.io/) v6:** 核心的区块链交互库，用于创建合约实例、调用方法和与以太坊节点通信。
    *   **[Web3Modal](https://web3modal.com/) / [WalletConnect](https://walletconnect.com/):** 用于实现钱包连接功能，支持多种钱包类型（如 MetaMask, WalletConnect）。

## 3. 项目结构

项目采用了典型的 Vue 3 + Vite 的项目结构。

```
src/
├── App.vue       # 根组件
├── main.ts       # 应用入口文件，用于初始化 Vue, Pinia, Router 等
├── assets/       # 静态资源
├── components/   # 可复用的通用 Vue 组件
├── contracts/    # 区块链交互的核心逻辑
│   ├── config.ts # **关键文件**：管理所有合约的地址和 ABI
│   └── index.ts  # 封装获取合约实例的工具函数
├── router/       # Vue Router 的路由配置文件
├── stores/       # Pinia 的状态存储模块 (Store)
├── views/        # 页面级组件，对应于每个路由
└── ...           # 其他工具和类型定义目录
```

## 4. 核心架构与数据流

### 4.1. 状态管理 (Pinia)

Pinia (`src/stores/`) 在应用中扮演着核心角色，用于管理全局共享状态，主要包括：
*   **钱包与连接状态:** 存储当前连接的钱包提供者（Provider）、签名者（Signer）、用户地址和链 ID。
*   **合约实例:** 缓存已创建的 Ethers.js 合约实例，避免重复创建。
*   **全局加载状态:** 管理全局性的加载指示器。

### 4.2. 路由 (Vue Router)

Vue Router (`src/router/index.ts`) 负责定义应用的页面结构。每个路由都映射到一个 `views` 目录下的页面级组件，并通过 `meta` 字段定义页面标题等元数据，用于动态渲染导航和面包屑。

### 4.3. 区块链交互模型

`admin-dapp` 的区块链交互流程清晰且模块化，是整个应用的基石。

**数据流如下:**

1.  **配置层 (`src/contracts/config.ts`):**
    *   该文件是与区块链交互的“真理之源”。
    *   `CONTRACT_ADDRESSES` 对象从环境变量 (`.env`) 中读取并存储了不同网络（如 Sepolia, Mainnet）上所有协议合约的地址。
    *   `CONTRACT_ABI_MAP` 对象硬编码了所有相关合约的 ABI (Application Binary Interface)。
    *   这种将地址和 ABI 集中管理的方式，使得更新合约版本或支持新网络变得非常简单。

2.  **封装层 (`src/contracts/index.ts`):**
    *   该文件提供了一个工具函数，例如 `getContract(contractName)`。
    *   此函数会从 Pinia store 中获取当前的 `signer` 或 `provider`，然后结合 `config.ts` 中提供的地址和 ABI，使用 `new ethers.Contract(address, abi, signer)` 来创建一个可交互的合约实例。

3.  **视图/逻辑层 (`src/views/**/*.vue`):**
    *   页面组件（如 `ActiveLiquidity.vue`）需要与合约交互时，会调用 `getContract('ActiveLiquidityAMO')` 来获取合约实例。
    *   组件中的方法（如 `handleExecuteArbitrage`）会调用该合约实例上的方法，例如 `await contract.executeArbitrage()`。
    *   方法调用会返回一个交易对象（Transaction），组件可以监听交易状态（等待打包、成功、失败）并相应地更新 UI（如显示加载状态、发送成功通知）。

**示例代码流程:**
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
这种分层、清晰的架构使得 `admin-dapp` 成为一个健壮且易于维护的管理工具。
