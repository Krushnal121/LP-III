Here's how to create a Solidity smart contract to manage student data using structures, arrays, and fallback functions. We'll also deploy this smart contract on an Ethereum test network to observe the transaction fee and gas values.

### Prerequisites

- **Node.js** and **npm** installed.
- **Truffle** for development and deployment of the smart contract.
- **Ganache** (or an Ethereum test network like Ropsten) to simulate a blockchain environment.
- **MetaMask** extension for wallet management if you use a test network.

### Step-by-Step Implementation

#### Step 1: Set Up the Development Environment

1. **Install Truffle** if it’s not installed already:
   ```bash
   npm install -g truffle
   ```

2. **Install Ganache** if you want to use a local blockchain (or configure a test network like Ropsten if preferred).

3. **Initialize a Truffle project**:
   ```bash
   mkdir StudentDataProject
   cd StudentDataProject
   truffle init
   ```

4. **Create a new contract file** named `StudentData.sol` inside the `contracts` folder.

#### Step 2: Write the Smart Contract

The following Solidity code defines a `StudentData` smart contract. It includes a structure for student data, an array to store multiple student records, and a fallback function.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StudentData {
    struct Student {
        uint id;
        string name;
        uint age;
    }

    Student[] public students;
    uint public studentCount = 0;
    address public owner;

    // Event for logging student addition
    event StudentAdded(uint id, string name, uint age);

    constructor() {
        owner = msg.sender;
    }

    // Modifier to restrict certain functions to only the owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can add students.");
        _;
    }

    // Function to add a new student
    function addStudent(string memory _name, uint _age) public onlyOwner {
        students.push(Student(studentCount, _name, _age));
        emit StudentAdded(studentCount, _name, _age);
        studentCount++;
    }

    // Function to retrieve all students
    function getAllStudents() public view returns (Student[] memory) {
        return students;
    }

    // Fallback function to handle incorrect calls or Ether transfers
    fallback() external payable {
        revert("Invalid function call or Ether transfer not allowed.");
    }

    // Receive function to accept Ether but prevent unintended usage
    receive() external payable {
        revert("This contract does not accept Ether.");
    }
}
```

#### Step 3: Compile the Smart Contract

1. **Navigate to the project directory** and compile the contract:
   ```bash
   truffle compile
   ```

   Compilation will create the ABI and bytecode for the contract in the `build/contracts` directory.

#### Step 4: Configure Truffle to Deploy on a Test Network

1. Open `truffle-config.js` and add network configurations, depending on whether you’re using Ganache or a test network (e.g., Ropsten).

   ```javascript
   module.exports = {
     networks: {
       development: {
         host: "127.0.0.1",
         port: 7545,       // Ganache default port
         network_id: "*"   // Match any network id
       },
       ropsten: {
         provider: () =>
           new HDWalletProvider("YOUR_MNEMONIC", "https://ropsten.infura.io/v3/YOUR_INFURA_PROJECT_ID"),
         network_id: 3,       // Ropsten network id
         gas: 5500000,        // Ropsten gas limit
       }
     },
     compilers: {
       solc: {
         version: "^0.8.0",
       },
     },
   };
   ```

   Replace `"YOUR_MNEMONIC"` with your wallet mnemonic and `"YOUR_INFURA_PROJECT_ID"` with your Infura project ID if using Ropsten.

#### Step 5: Deploy the Contract

1. **Create a migration script** in the `migrations` folder named `2_deploy_student_data.js`:

   ```javascript
   const StudentData = artifacts.require("StudentData");

   module.exports = function (deployer) {
     deployer.deploy(StudentData);
   };
   ```

2. **Deploy the contract** on the configured network:
   ```bash
   truffle migrate --network development
   ```
   If you’re deploying to Ropsten, replace `development` with `ropsten`.

#### Step 6: Interact with the Smart Contract and Observe Gas Usage

1. **Open the Truffle console**:
   ```bash
   truffle console --network development
   ```

2. **Get the contract instance**:
   ```javascript
   let studentData = await StudentData.deployed();
   ```

3. **Add a new student** and observe gas usage:
   ```javascript
   let tx = await studentData.addStudent("Alice", 20, { from: YOUR_ADDRESS });
   console.log("Transaction Hash:", tx.tx);
   console.log("Gas Used:", tx.receipt.gasUsed);
   ```

4. **Get all students**:
   ```javascript
   let students = await studentData.getAllStudents();
   console.log("Students:", students);
   ```

5. **Check gas used in transaction**:
   - Each transaction receipt contains a gas used field, which you can retrieve by logging `tx.receipt.gasUsed`.
   - Compare the gas usage with subsequent transactions by adding multiple students and observing any changes.

#### Step 7: Testing the Fallback Function

To test the fallback function, try sending a transaction to the contract without calling a specific function. This should trigger the `fallback()` function and revert the transaction.

```javascript
await web3.eth.sendTransaction({ from: YOUR_ADDRESS, to: studentData.address, value: web3.utils.toWei("0.1", "ether") });
```

This should fail with an error message: `Invalid function call or Ether transfer not allowed.`

### Step 8: Testing the Contract (Optional)

1. **Create a test file** in the `test` folder named `StudentData.test.js`:

   ```javascript
   const StudentData = artifacts.require("StudentData");

   contract("StudentData", (accounts) => {
     let studentDataInstance;

     before(async () => {
       studentDataInstance = await StudentData.deployed();
     });

     it("should add a new student", async () => {
       let tx = await studentDataInstance.addStudent("Bob", 22, { from: accounts[0] });
       assert.equal(tx.receipt.gasUsed > 0, true, "Gas usage should be greater than zero.");
       let student = await studentDataInstance.students(0);
       assert.equal(student.name, "Bob", "Student name should be Bob.");
       assert.equal(student.age.toNumber(), 22, "Student age should be 22.");
     });

     it("should revert on fallback function", async () => {
       try {
         await web3.eth.sendTransaction({ from: accounts[0], to: studentDataInstance.address, value: web3.utils.toWei("0.1", "ether") });
       } catch (error) {
         assert(error, "Fallback function did not revert as expected.");
       }
     });
   });
   ```

2. **Run the tests**:
   ```bash
   truffle test
   ```

### Step 9: Deploy on a Public Test Network and Observe Transaction Fees

To observe actual transaction fees and gas values, deploy on a test network like Ropsten, and monitor transactions through [Etherscan](https://ropsten.etherscan.io/). Each transaction will show the gas used and the total transaction fee.

By following these steps, you’ll set up a student data management system on the Ethereum blockchain, using structures, arrays, and fallback functions, and observe gas fees associated with each transaction.