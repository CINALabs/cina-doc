# CINA DOLLAR (ETH Shanghai 2025) - Product Manual

## 1. Project Overview

`CINA DOLLAR` is a project developed for the ETH Shanghai 2025 Hackathon, aiming to demonstrate the powerful composability and financial application potential of the CINA Core Protocol (based on f(x) Protocol).

This project is not a complete, independent protocol, but a Proof of Concept (PoC) focused on a single innovative feature: **Zero Initial Capital Leveraged Trading**.

## 2. Core Concept & Problem Solved

**Core Concept:** Leveraging the "Atomic Composability" of the DeFi world, especially Flash Loans, to allow users to establish a high-leverage Collateralized Debt Position (CDP) with extremely low initial capital.

**Problem Solved:** In traditional leveraged trading, users need to possess sufficient capital themselves to perform leveraged operations. For example, to open a 5x leverage ETH long position, a user needs to provide 20% margin themselves. This project aims to remove this capital barrier.

## 3. Target Users

*   **DeFi Advanced Traders:** Professional traders seeking high capital efficiency and wishing to quickly establish leveraged positions.
*   **Tech Judges & Community:** Showcasing the advanced capabilities of the CINA Protocol to hackathon judges and the broader DeFi community.

## 4. Core Feature: Leveraged Long Flow

The following is the complete product flow for a user to open a leveraged long position with one click via the `CINA DOLLAR` DApp interface.

**Scenario:** Assume a user is bullish on ETH and wants to use a small amount of ETH as principal to establish a 5x leveraged ETH long position.

1.  **Initiate Transaction:**
    *   User selects collateral (ETH) and sets leverage multiple (e.g., 5x) on the DApp interface.
    *   User deposits a small amount of initial capital (e.g., 1 ETH).
    *   User clicks the "Open Leveraged Position" button to sign and send a transaction via wallet.

2.  **On-Chain Atomic Operation (Automatically completed by `PositionOperateFlashLoanFacetV2.sol` within one transaction):**
    *   **a. Flash Loan:** The smart contract borrows a large amount of ETH (e.g., based on user's 1 ETH principal and 5x leverage, the contract might borrow 4 ETH) from the Morpho Protocol's lending pool as a "Flash Loan".
    *   **b. Aggregate Capital:** The contract combines the user's 1 ETH principal and the 4 ETH borrowed via flash loan to form a total of 5 ETH collateral.
    *   **c. Mint Stablecoin:** The contract deposits this 5 ETH into the CINA Protocol's core Vault and mints the maximum amount of `fxUSD` stablecoin (e.g., worth 4 ETH) based on the current collateralization ratio (e.g., 80%).
    *   **d. Repay Flash Loan:** The contract immediately swaps a portion of the newly minted `fxUSD` into ETH on an integrated DEX (like Uniswap), the amount being just enough to repay the 4 ETH principal borrowed from Morpho in step (a) plus the flash loan fee.
    *   **e. Transaction Complete:** Flash loan repaid, transaction successful.

3.  **Final Result:**
    *   With 1 ETH of initial capital, the user successfully established a position with 5 ETH collateral and `fxUSD` debt worth 4 ETH.
    *   The user's net equity is still 1 ETH, but their position size is magnified 5 times, successfully achieving a 5x leveraged long on ETH. If the ETH price rises, the profit of this position will also be 5x.

## 5. Risk Warning

*   **Liquidation Risk:** Like any leveraged position, if the price of the collateral (ETH) falls, causing the position's health factor to drop below the liquidation threshold, the position faces the risk of liquidation, and the user may lose their entire initial capital.
*   **Smart Contract Risk:** This flow relies on multiple external protocols (Morpho, Uniswap), increasing system complexity and potential risk points.
