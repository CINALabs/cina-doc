# CINA DEX (Carbon Protocol) Product Flow Document

## 1. Overview

CINA DEX Trading System Interface is an advanced decentralized trading strategy management platform based on the Bancor Carbon Protocol. It is not a traditional "Swap" application but allows users to deploy automated, asymmetric trading strategies on-chain as "Strategy Creators".

Its core product value lies in enabling ordinary users to use professional market maker tools to achieve "buy low, sell high" automated arbitrage by setting price ranges, without the need for constant monitoring.

## 2. Core Concept: Automated Trading Strategy

Unlike "Market Orders" or "Limit Orders" in traditional DEXs, the Carbon Protocol introduces the concept of "On-chain Strategy". A strategy consists of one or two "Orders", each working within a specified price **range**.

*   **Asymmetry:** Buy and sell price ranges can be completely different or even non-overlapping. For example, you can set a strategy: Buy ETH in the $1800-$1900 range, and Sell ETH in the $2500-$2600 range.
*   **Automation:** Once a strategy is created, its buy/sell logic executes automatically on-chain without user intervention. Funds flow automatically between buy and sell orders based on price movements.
*   **Irreversibility:** Revenue from sell orders automatically becomes funds for buy orders, and vice versa. This allows the strategy to continuously cycle "buy low, sell high".

## 3. Participating Roles

*   **Strategy Creator / Trader:** The core user of the platform. They set price ranges and budgets based on their market judgment, creating automated trading strategies to earn profit.
*   **Arbitrageur:** When on-chain strategies offer prices better than other markets, arbitrageurs trade against these strategies, helping them achieve their buy/sell goals.

## 4. Core Product Flows

### 4.1. Create New Strategy

This is the platform's core user journey. The application provides three preset strategy templates to simplify the creation process.

#### 4.1.1. Disposable Strategy

Also known as "Range Order", used for one-time "buy low, sell high".

1.  **Select Pair:** User selects two assets to trade, e.g., WETH/USDC.
2.  **Set Buy Range:** User sets a price range (min and max) to buy assets (e.g., buy WETH with USDC).
3.  **Set Sell Range:** User sets a **higher** price range to sell assets (e.g., sell WETH for USDC).
4.  **Allocate Budget:** User decides how much initial capital to invest (e.g., invest 1000 USDC into the buy order).
5.  **Create Strategy:** User submits transaction to create a new strategy on-chain.

**Flow Example:**
*   User sets to buy WETH in $1800-$1900 range, sell WETH in $2500-$2600 range, investing 1000 USDC.
*   When WETH market price enters $1800-$1900, strategy automatically buys WETH with USDC.
*   When WETH market price rises to $2500-$2600, strategy automatically sells the bought WETH back for USDC, completing one arbitrage round.
*   After this, the strategy ends.

#### 4.1.2. Recurring Strategy

Used for continuous "buy low, sell high", implementing mean reversion trading.

1.  **Set Buy/Sell Ranges:** Similar to disposable strategy, user sets a buy range and a sell range.
2.  **Allocate Budget:** User can allocate budget for both buy and sell orders simultaneously.
3.  **Create Strategy:** Submit transaction.

**Flow Example:**
*   User sets to buy WETH in $1800-$1900 range, sell WETH in $2500-$2600 range.
*   As price fluctuates between the two ranges, the strategy automatically buys low and sells high.
*   **Key Difference:** USDC obtained from selling WETH **automatically** replenishes the buy order budget; USDC spent buying WETH returns to budget after WETH is sold. This forms a continuously running automated trading loop.

#### 4.1.3. Overlapping Strategy

This is a more advanced strategy where buy and sell price ranges overlap, aiming to provide more concentrated liquidity to the market.

*   **Set Overlapping Range:** User sets an overlapping price range and a Spread. System automatically generates buy/sell orders based on this.
*   **Effect:** Within the overlapping price area, this strategy acts as both buyer and seller, capturing smaller price fluctuations and earning the spread, similar to a small market maker.

### 4.2. Strategy Simulator (`/simulator`)

Before investing real funds, users can use the simulator to test their strategy ideas.

*   **Function:** Users can input exactly the same parameters (price ranges, budget, etc.) as creating a real strategy.
*   **Result:** The simulator backtests the strategy against historical data or preset models, giving estimated profit, loss, trade count, etc.
*   **Value:** Helps users optimize and verify their trading ideas with zero risk.

### 4.3. Portfolio Management (`/portfolio`)

All strategies created by the user are displayed on the "My Strategies" page.

*   **Function:**
    *   **View List:** Centralized display of all active user strategies.
    *   **Status Monitoring:** Real-time display of each strategy's current status, holdings, budget, accumulated earnings, etc.
    *   **Strategy Management:** Users can "Add/Withdraw" funds to existing strategies or "Pause/Terminate" a strategy at any time.

### 4.4. Explore Market (`/explorer`)

This is a public market page displaying public strategies created by all users on the protocol.

*   **Function:** Users can browse, filter, and analyze others' strategies to find trading opportunities or learn strategy settings.
*   **Transparency:** Provides macro insights into the entire protocol's liquidity distribution and market sentiment.
