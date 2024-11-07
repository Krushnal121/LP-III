// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BankAccount {
    address public owner;
    uint public balance;

    // Event to emit when a deposit is made
    event Deposit(uint amount, uint newBalance);
    // Event to emit when a withdrawal is made
    event Withdraw(uint amount, uint newBalance);

    constructor() {
        owner = msg.sender; // Set the contract deployer as the owner
    }

    // Modifier to allow only the owner to call certain functions
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function.");
        _;
    }

    // Deposit function to add funds to the account
    function deposit() external payable {
        balance += msg.value;
        emit Deposit(msg.value, balance);
    }

    // Withdraw function to remove funds from the account
    function withdraw(uint _amount) external onlyOwner {
        require(_amount <= balance, "Insufficient balance.");
        balance -= _amount;
        payable(owner).transfer(_amount);
        emit Withdraw(_amount, balance);
    }

    // Function to check the account balance
    function getBalance() external view returns (uint) {
        return balance;
    }
}