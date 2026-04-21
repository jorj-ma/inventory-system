Inventory Management System (CLI)
A Python-based Command Line Interface (CLI) for managing inventory, interacting with a REST API backend. It supports user authentication, CRUD operations on inventory items, and integration with external product data.

 Features
User Authentication: Register, Login (with session persistence), and Logout.

Inventory Management: List, View, Add, Update, and Delete items.

Session Management: Cookies are stored locally in session_cookies.txt to keep you logged in between commands.

External Integration: Fetch product data via barcode.


Pip (Python package manager)

Running Backend: This CLI expects an API to be running at http://127.0.0.1:5000/inventory.

  Installation
Clone the repository and navigate to the project folder:
        cd inventory_system

Set up a virtual environment (as seen in your file structure):
        python3 -m venv venv
        source venv/bin/activate

Install dependencies:
        pip install -r requirements.txt
    
    
    Usage
The CLI is executed through the app/cli.py file.

--- Authentication
Register a new user:
        python3 app/cli.py register --username YourName --password YourPassword --role admin

Login:
        python3 app/cli.py login --username YourName --password YourPassword

Logout:
        python3 app/cli.py logout


 Inventory Operations
List all items:
        python3 app/cli.py list

Add a new item:
        python3 app/cli.py add --name "Orange Juice" --brand "Tropicana" --price 4.50 --stock 12 --barcode 555555555555


Update an item (by ID):
        python3 app/cli.py update 1 --stock 20 --price 4.99

View a specific item:
        python3 app/cli.py view 1

Delete an item:
        python3 app/cli.py delete 1



  File Structure
app/cli.py: The main entry point for the CLI.

session_cookies.txt: Created automatically after login to store session data.

