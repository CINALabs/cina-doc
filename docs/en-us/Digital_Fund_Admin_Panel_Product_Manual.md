# Digital Fund Admin Panel - Product Manual

## 1. Overview

This application is a Web-based internal management dashboard designed for administrators of the "Digital Fund". It provides a complete set of tools for managing daily fund operations, processing investment/redemption requests, and maintaining system security and compliance.

**Important Note:** This application is an internal tool and can only be used after authorized administrator addresses connect via wallet. Its backend service implementation is unknown; this document describes it based solely on frontend interface functionality.

## 2. Core Functional Modules

### 2.1. Dashboard

The backend homepage, providing an overview of the fund's Key Performance Indicators (KPIs).
*   **Content Displayed:**
    *   Latest Net Asset Value (NAV) of the fund.
    *   Number of pending Mint (Subscription) and Burn (Redemption) requests.
    *   Total Value Locked (TVL) of the fund.
    *   Logs of key on-chain events.
*   **Purpose:** Help admins quickly understand the overall health and operational load of the fund.

### 2.2. NAV Management

NAV is the core metric measuring fund value; this module is used for its management and verification.
*   **Functions:**
    *   **Submit NAV:** Admins periodically (e.g., daily) submit the latest NAV report of the fund through this interface. This may require filling in asset details, total value, etc.
    *   **Verify NAV:** There may be an approval process requiring another admin to review and "verify" the submitted NAV report. Only verified NAVs become the official standard of the protocol.
    *   **History:** View records of all historical NAV submissions and verifications.

### 2.3. Mint Management

Manage investor subscription (minting fund tokens) requests.
*   **Flow:** Investor subscription requests are not automatically executed on-chain but first enter this admin panel as a "Pending" record.
*   **Functions:**
    *   **Request List:** Display all pending, approved, and rejected mint requests in a list.
    *   **Request Details:** Click to view detailed information of each request, such as investor address, subscription amount, submission time, etc.
    *   **Approval Action:** Admins can "Approve" or "Reject" pending requests.
    *   **Execute Mint:** After "Approving" a request, the admin may need to trigger the final on-chain transaction through this interface to mint corresponding fund tokens for the investor.

### 2.4. Burn Management

Manage investor redemption (burning fund tokens) requests, with a flow similar to Mint Management.
*   **Flow:** Investor redemption requests also require admin approval.
*   **Functions:**
    *   **Request List:** Display all pending, approved, and rejected burn requests.
    *   **Approval Action:** Admins "Approve" or "Reject" requests.
    *   **Execute Burn:** After "Approval", the admin triggers an on-chain transaction to burn the investor's fund tokens and return the corresponding value of underlying assets to the investor.

### 2.5. Blacklist Management

Used to manage address access permissions, an important tool for fund compliance and risk control.
*   **Functions:**
    *   **Add Address to Blacklist:** Admins can input a user address and add it to the blacklist. Blacklisted addresses cannot interact with the fund's smart contracts.
    *   **Remove Address from Blacklist:** Remove an address from the blacklist, restoring its access permissions.
    *   **View Blacklist:** Display a list of all currently blacklisted addresses.

### 2.6. Contract Management

Provides direct management functions for the fund's smart contracts.
*   **Functions:**
    *   **Pause/Unpause:** In emergencies, admins can pause or resume the functions of one or more core contracts through this interface.
    *   **Set Parameters:** Modify adjustable parameters of smart contracts, such as management fees, mint/burn fees, etc.
    *   **Update Addresses:** Change other key addresses depended on by the contract, such as oracle address, fund manager address, etc.
