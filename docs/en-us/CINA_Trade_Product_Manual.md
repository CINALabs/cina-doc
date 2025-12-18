# CINA Trade: Product Manual

## 1. Introduction
CINA Trade is a high-performance decentralized trading interface designed for the CINA Ecosystem. It provides users with advanced trading features, including leveraged long/short positions, flash loans, and real-time position monitoring.

## 2. Key Features
- **Leveraged Trading**: Easily open positions with up to 5x leverage using the integrated flash loan mechanism.
- **Flash Open/Close**: Execute complex multi-step trades (borrowing, swapping, minting) in a single click.
- **Wallet Integration**: Supports popular wallets like MetaMask, Coinbase Wallet, and WalletConnect via RainbowKit.
- **Real-time Analytics**: Track your position health, liquidation price, and PnL in real-time.

## 3. How to Use
### 3.1 Connecting Your Wallet
1. Click the **Connect Wallet** button in the top right corner.
2. Select your preferred wallet and authorize the connection on the Sepolia testnet.

### 3.2 Opening a Position
1. Navigate to the **Trade** section.
2. Select your collateral token (e.g., `wstETH`).
3. Enter the amount of collateral you wish to deposit.
4. Use the leverage slider to select your desired leverage (1x - 5x).
5. Review the "Expected Output" and "Slippage" settings.
6. Click **Open Position** and confirm the transaction in your wallet.

### 3.3 Managing Positions
- View all active positions in the **Dashboard**.
- Monitor the **Health Factor** to avoid liquidation.
- Use the **Close** button to exit a position instantly using the flash close mechanism.

## 4. Safety Tips
- Always ensure you have enough ETH for gas fees.
- Be mindful of the Health Factor; if it drops below 1.0, your position may be liquidated.
- Check slippage settings during high volatility to ensure trade execution.
