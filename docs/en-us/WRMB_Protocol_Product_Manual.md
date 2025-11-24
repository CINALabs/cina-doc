# WRMB Savings & Yield Protocol - Product Manual

## 1. Ecosystem Overview

The WRMB Protocol is an innovative decentralized savings and yield protocol. Its core is not a traditional stablecoin, but a system that provides users with real yield through a value accumulation model.

The entire ecosystem consists of three parts working in synergy:

1.  **`WRMB-protocol-contracts`:** The core smart contracts defining all rules and mechanisms of the protocol.
2.  **`wrmb-dapp`:** The full-featured main DApp, providing interfaces to interact with all protocol functions (Savings, Bonds, Wrapping).
3.  **`wrap-dapp`:** A lightweight, single-function DApp dedicated to quick swaps between `WRMB` and `sRMB`.

### Unique Token Model

The key to understanding the WRMB Protocol lies in understanding the roles of its three "tokens":

*   **`WRMB` (Liquid Token):**
    *   **What is it:** A standard ERC20 token that can be freely traded on secondary markets like Uniswap.
    *   **Role:** The protocol's **Value Carrier** and **Liquidity Medium**. Users acquire it from external markets, and yield is ultimately realized in this form.

*   **`sRMB` (Savings Certificate Token):**
    *   **What is it:** A restricted, **non-transferable** ERC20 token.
    *   **Role:** It is the **"Entry Ticket" and "Exit Ticket"** for users to participate in the protocol's internal savings system. Users can only obtain it by exchanging `WRMB` 1:1 through the official "Wrap" contract. Its existence ensures that all savings activities must go through the protocol's official channels.

*   **`sWRMB` (Vault Share):**
    *   **What is it:** This is **not a token**, but an internal accounting unit for the **share** a user holds in the `SavingsVault`.
    *   **Role:** Represents the user's ownership in the vault. As the vault generates profit through its investment strategies (e.g., market making via the AMO module), the total assets of the vault increase, causing the Net Asset Value (NAV) of each `sWRMB` share to grow.

## 2. Core User Journey: The Savings & Yield "Flywheel"

The complete user yield cycle is as follows:

**Step 1: Enter the System (Wrap)**
1.  User acquires liquid `WRMB` tokens on the secondary market (e.g., Uniswap).
2.  User visits the "Wrap" page of `wrmb-dapp` or uses the simpler `wrap-dapp`.
3.  User executes the "Wrap" operation, exchanging their `WRMB` for restricted `sRMB` tokens at a 1:1 ratio.
    *   *Example: User wraps 1000 `WRMB` to get 1000 `sRMB`.*

**Step 2: Deposit into Vault, Start Earning (Deposit)**
1.  User visits the "Savings" page of `wrmb-dapp`.
2.  User executes the "Deposit" operation, depositing their `sRMB` into the `SavingsVault`.
3.  In return, the vault credits the user with a corresponding amount of `sWRMB` shares based on the current share NAV.
    *   *Example: User deposits 1000 `sRMB` and receives 1000 `sWRMB` shares.*

**Step 3: Value Accumulation**
1.  No action required from the user.
2.  The `SavingsVault` utilizes its pooled funds to generate profit through various strategies (such as the `v4-pool-amo` module).
3.  These profits increase the total assets of the `SavingsVault`, thereby constantly increasing the value of each `sWRMB` share.

**Step 4: Withdraw Yield (Withdraw)**
1.  After some time, the user decides to withdraw their yield.
2.  User returns to the "Savings" page of `wrmb-dapp`.
3.  User executes the "Withdraw" operation, redeeming their `sWRMB` shares back into `sRMB` tokens.
4.  Since the value of `sWRMB` shares has grown, the user will now receive **more** `sRMB` tokens than originally deposited.
    *   *Example: The user's original 1000 `sWRMB` shares are now worth 10% more, so they can redeem 1100 `sRMB`. This extra 100 `sRMB` is the user's yield.*

**Step 5: Exit the System (Unwrap)**
1.  User returns to the "Wrap" page or `wrap-dapp`.
2.  User executes the "Unwrap" operation, exchanging their `sRMB` back into freely circulating `WRMB` tokens at a 1:1 ratio.
    *   *Example: User unwraps 1100 `sRMB` into 1100 `WRMB`.*
3.  The user can now sell these 1100 `WRMB` on the secondary market, realizing the final profit.

## 3. Other Features

### Bonds
*   `wrmb-dapp` also provides a "Bonds" feature.
*   This is a protocol financing mechanism. Users can use other assets (like USDT) to purchase bonds issued by the protocol and receive `WRMB` tokens at a discount in the future.
*   For the protocol, this is a way for its Treasury to acquire core assets (like stablecoins).
*   For users, this provides a way to acquire `WRMB` at a discount.
