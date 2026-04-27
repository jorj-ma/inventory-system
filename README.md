# Inventory Management System (CLI)

A Python-based Command Line Interface (CLI) for managing inventory, interacting with a REST API backend. It supports user authentication, CRUD operations on inventory items, and integration with external product data.

## Features
- **User Authentication**: Register, Login (with session persistence), and Logout
- **Inventory Management**: List, View, Add, Update, and Delete items
- **Session Management**: Cookies are stored locally in `session_cookies.txt` to keep you logged in between commands
- **External Integration**: Fetch product data via barcode

## Requirements
- Python 3.x
- Pip (Python package manager)
- Running backend API at: `http://127.0.0.1:5000/inventory`

## Installation
```bash
cd inventory_system
```
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```
## USAGE
The CLI is executed through the app/cli.py file.
### Authentication
```bash
python3 app/cli.py register --username YourName --password YourPassword --role admin
```
```bash
python3 app/cli.py login --username YourName --password YourPassword
```
```bash
python3 app/cli.py logout
```

#### List all items
```bash
python3 app/cli.py list
```

#### Add a new item
```bash
python3 app/cli.py add --name "Orange Juice" --brand "Tropicana" --price 4.50 --stock 12 --barcode 555555555555
```

#### Update an item (by ID)
```bash
python3 app/cli.py update 1 --stock 20 --price 4.99
```

#### View a specific item
```bash
python3 app/cli.py view 1
```

#### Delete an item
```bash
python3 app/cli.py delete 1
```