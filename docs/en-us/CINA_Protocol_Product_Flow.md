# CINA Protocol Product Flow Document

## 1. Overview

The CINA Protocol is an advanced decentralized stablecoin protocol designed to issue FxUSD, a stablecoin pegged 1:1 to the US Dollar. Users can mint (borrow) FxUSD by over-collateralizing accepted crypto assets (such as WETH).

The core features of the protocol are its efficient liquidation mechanism and robust peg stability module, enabling it to scale robustly to serve a large number of users.

This document aims to describe in detail the workflows of different roles and core product functions within the protocol.

## 2. Participating Roles

There are four main categories of core participants in the protocol:

*   **Borrower/Position Manager:** Users who deposit collateral to mint FxUSD. They are the core users of the protocol.
*   **FxUSD Holder:** Users who use FxUSD for payments, trading, or participating in other DeFi protocols.
*   **Liquidator:** Participants who monitor unhealthy positions (under-collateralized) in the protocol and trigger liquidations to earn profit. They are key to maintaining the protocol's solvency.
*   **Arbitrageur:** Users who arbitrage the price difference between FxUSD in secondary markets (like Curve) and the protocol's internal price. They are an important external force for maintaining the FxUSD price peg.

## 3. Core Product Flows

### 3.1. Minting FxUSD (Opening a Position)

This is the starting point for user interaction with the protocol.

1.  **Select Collateral:** The user selects an asset accepted by the protocol (e.g., WETH) as collateral.
2.  **Deposit Collateral:** The user deposits a selected amount of collateral into the corresponding protocol Pool.
3.  **Borrow/Mint FxUSD:** Based on the value of the deposited collateral and the collateralization ratio of that asset, the user can borrow a certain amount of FxUSD. For example, if the collateralization ratio for WETH is 80%, depositing $1000 worth of WETH allows the user to borrow up to 800 FxUSD.
4.  **Receive Position NFT:** The protocol creates an NFT for the user representing their debt position. This NFT is the unique proof of ownership for their position and can be transferred.

**User Interface (UI) Interaction:**
*   A clear dashboard allowing users to select collateral types.
*   Input fields for users to enter the amount of collateral to deposit or FxUSD to borrow.
*   Real-time display of key information such as position health (collateralization ratio/debt ratio) and liquidation price.
*   User confirms the transaction via wallet to complete position opening.

### 3.2. Managing Existing Positions

Users can adjust their positions at any time to respond to market changes or manage risk.

*   **Add Collateral:** Users can add more collateral to an existing position to improve its health and reduce liquidation risk.
*   **Remove Collateral:** If a position is very healthy (far above the minimum collateral requirement), users can withdraw part of the collateral.
*   **Repay FxUSD:** Users can repay part or all of their FxUSD debt at any time. After repayment, their debt decreases.
*   **Withdraw All Collateral:** When users fully repay all FxUSD debt, they can withdraw all collateral and close the position.

**UI Interaction:**
*   On the position management page, provide clear buttons like "Add Collateral", "Withdraw Collateral", "Repay Debt".
*   Interactive sliders or input fields allowing users to precisely control operation amounts.
*   Real-time simulation of position status changes after the transaction.

### 3.3. Position Liquidation

Liquidation is the protocol's automatic risk control mechanism, ensuring the protocol always remains solvent.

1.  **Trigger Condition:** When the market price of collateral falls, causing the ratio of debt value to collateral value of a position to exceed the liquidation threshold, the position becomes liquidatable.
2.  **Liquidator Intervention:** Anyone (usually liquidators running monitoring bots) can trigger liquidation of unhealthy positions.
3.  **Liquidation Process:**
    *   The liquidator repays part or all of the FxUSD debt on behalf of the position.
    *   In return, the liquidator receives a portion of the collateral in that position at a discount. This discount is the incentive for liquidators to maintain protocol health.
4.  **Protocol's Efficient Implementation:** The CINA Protocol technically optimizes the liquidation process. It aggregates positions with similar health status on the same "Tick". When liquidation occurs, it targets the entire "Tick" rather than individual positions, greatly improving efficiency.

### 3.4. FxUSD Peg Stability Mechanism

The protocol actively maintains the peg of FxUSD to the US Dollar through a smart contract called `PegKeeper`.

1.  **Price Monitoring:** `PegKeeper` continuously monitors the trading price of FxUSD in key external liquidity pools (such as the FxUSD/USDC pool on Curve).
2.  **De-peg Response (Price < $1):**
    *   **Pause Borrowing:** If the FxUSD price falls below a threshold (e.g., $0.995), `PegKeeper` pauses the protocol's new FxUSD borrowing function. This prevents further increase in FxUSD supply in the market, alleviating selling pressure.
    *   **Enable Arbitrage:** Simultaneously, the protocol allows users to redeem collateral from the protocol at a discount (e.g., redeem $0.998 worth of collateral with 1 FxUSD). Arbitrageurs will seize this opportunity: buy FxUSD in the market at a price below $1, then redeem assets in the protocol at a price close to $1 to make a profit. This buying behavior pushes up the market price of FxUSD, returning it to the peg.
3.  **De-peg Response (Price > $1):**
    *   If the FxUSD price is above a threshold (e.g., $1.005), it means market demand is strong. The protocol ensures borrowing is enabled, encouraging users to generate more FxUSD to meet market demand, thereby pushing the price back to $1.

This active, automated mechanism is the core guarantee for FxUSD to maintain its value stability.
