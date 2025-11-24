# WRMB Protocol Admin Dashboard - Product Manual

## 1. Overview

This application is the internal management dashboard for the WRMB Protocol, a powerful on-chain tool designed for protocol administrators and core developers. It provides full control over the core parameters and Algorithmic Market Operations (AMO) modules of the WRMB Protocol.

**Unauthorized access or operation is strictly prohibited. Any operation may have a direct and significant impact on the protocol's fund security, price stability, and overall health.**

## 2. Core Functional Modules

The admin dashboard is divided into several main pages based on functionality, accessible via the left navigation bar.

### 2.1. Dashboard

This is the homepage of the backend, aiming to provide an overview of the protocol's current status indicators.
*   **Key Metrics:** Typically displays Total WRMB Supply, Total Value Locked (TVL), asset distribution of key AMOs, current oracle prices, etc.
*   **Action:** This page is mainly for monitoring and does not contain write operations.

### 2.2. AMO Management

AMO (Algorithmic Market Operations) is the core module for the WRMB Protocol to actively manage its balance sheet and maintain the stablecoin peg. This dashboard provides fine-grained control over these modules.

#### 2.2.1. Active Liquidity AMO

This module may be responsible for providing WRMB liquidity on mainstream DEXs (like Uniswap).
*   **Executable Actions:**
    *   **Execute Arbitrage:** When the external market price deviates from the protocol's internal price, admins can trigger this function to execute arbitrage trades, returning the price to peg while earning profit for the protocol.
    *   **Rebalance:** Adjust the ratio and range of WRMB and other assets (like USDC) in the liquidity pool.
    *   **Update Parameters:** Modify AMO operating parameters, such as trading fees, slippage tolerance, target price range, etc.
    *   **Withdraw Funds:** Withdraw a portion of funds from the AMO to the protocol vault.
    *   **Pause/Unpause:** Pause all activities of this AMO under extreme market conditions.

#### 2.2.2. Bond Liquidity AMO

This module may be related to bonds or certificates issued by the protocol, used to manage the liquidity of this specific asset part.
*   **Executable Actions:**
    *   Similar to Active Liquidity AMO, but the object of operation is the protocol's bond-like assets.
    *   May include functions for managing bond issuance, redemption, and secondary market liquidity.

### 2.3. Oracle Management

Oracles are key infrastructure for the protocol to obtain external asset prices.
*   **Functions:**
    *   **View Price:** Display the latest asset prices provided by all price feed sources (like Chainlink).
    *   **Update Price:** In case of oracle failure or need for manual intervention, admins can force update asset prices through this function. **This is a high-risk operation** and may lead to incorrect liquidations.

### 2.4. Savings Vault Management

This is likely the protocol's central treasury or the deposit contract for sRMB.
*   **Functions:**
    *   **Update Parameters:** Adjust deposit interest rates (APY), deposit/withdrawal fees, etc.
    *   **Fund Management:** Manage the vault's investment strategies, such as allocating funds to different yield-bearing protocols.
    *   **Pause/Unpause:** Pause deposit and withdrawal functions of the vault.

### 2.5. Token Management

This module is used to manage core tokens within the WRMB Protocol ecosystem.
*   **WRMB/sRMB Management:**
    *   **Mint/Burn:** Under specific authorization, directly mint new WRMB or burn circulating WRMB.
    *   **Set Admin:** Change the administrative permissions of the token contract.
*   **sRMB Factory:**
    *   **Deploy New sRMB:** If the protocol supports multiple types of interest-bearing tokens, new sRMB contracts can be deployed via this factory contract.

### 2.6. System Control

Contains highest-privilege operations with global impact on the protocol.
*   **Pause/Unpause All:** One-click pause or resume of all core contract activities of the protocol, used to respond to emergency security incidents.
*   **Set Fees:** Set protocol-level fees, such as transaction fees, stability fees, etc.
*   **Set Keeper/Admin:** Change the addresses of key roles in the protocol (like Keeper, Oracle Admin).
