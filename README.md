# Advanced Student Management System

## Project Description

The Advanced Student Management System is a Python-based command-line application designed to manage student records efficiently.

It allows users to add, display, search, update, and delete student records. It also calculates student results, generates class statistics, filters and sorts student records, and stores data permanently using JSON file handling.

## Features

- Add Regular and Merit Students
- Display All Students
- Search Students by ID or Name
- Update Student Information
- Delete Student Records
- Calculate Total Marks and Average
- Calculate Grades and Pass/Fail Status
- Class Statistics and Department-wise Count
- Display Passed and Failed Students
- Generate Individual Result Reports
- Filter Students by Department and Grade
- Sort Students by Name and Average
- Display Top 3 Students
- Permanent Data Storage using JSON

## Technologies Used

- Python 3
- JSON
- Object-Oriented Programming (OOP)
- File Handling
- Exception Handling
- Python Data Structures

## Python Concepts Demonstrated

- Classes and Objects
- Inheritance
- Encapsulation
- Abstraction
- Polymorphism
- Constructors
- Properties and Setters
- Functions and Methods
- Lambda Functions
- List Comprehensions
- Exception Handling
- JSON Serialization and Deserialization
- File Handling

## Project Structure

```text
Advanced-Student-Management-System/
│
├── assessment.py
├── students.json
└── README.md
```

## Requirements

- Python 3.x
- No external libraries required.

## How to Run

1. Download or clone this repository.
2. Open the project folder in VS Code.
3. Run the following command:

```bash
python main.py
```

4. Select an option from the menu to manage student records.

## Data Storage

Student records are stored permanently in a JSON file named `students.json`.

The application automatically loads existing student records when it starts and saves changes when student records are added, updated, or deleted.

## Student Grading System

| Average Marks | Grade |
|      ---      |  ---  |
|     90–100    |   A+  |
|     80–89     |   A   |
|     70–79     |   B   |
|     60–69     |   C   |
|    Below 60   |  Fail |

**Merit Student:** Receives A+ grade when the average is 85 or above.

## Project Purpose

This project was developed to practice Python programming fundamentals and demonstrate practical understanding of Object-Oriented Programming, data management, validation, exception handling, and JSON file handling.

---

**Developed by:** Burhan Ali  
**Project:** Advanced Student Management System  
**Language:** Python