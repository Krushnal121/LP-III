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