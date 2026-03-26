import click
import requests
import os
from http.cookiejar import MozillaCookieJar

API_URL = "http://127.0.0.1:5000/inventory"
COOKIE_FILE = "session_cookies.txt"

session = requests.Session()
session.cookies = MozillaCookieJar(COOKIE_FILE)

# Load cookies if file exists
if os.path.exists(COOKIE_FILE):
    session.cookies.load(ignore_discard=True, ignore_expires=True)


@click.group()
def cli():
    """Inventory Management CLI"""
    pass


# --- Auth commands ---
@cli.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
def login(username, password):
    """Login and store session cookie"""
    response = session.post(
        API_URL + "/login", json={"username": username, "password": password}
    )
    try:
        click.echo(response.json())
    except ValueError:
        click.echo(response.text)
    # Save cookies to file
    session.cookies.save(ignore_discard=True, ignore_expires=True)


@cli.command()
def logout():
    """Logout and clear session cookie"""
    response = session.post(API_URL + "/logout")
    try:
        click.echo(response.json())
    except ValueError:
        click.echo(response.text)
    # Clear cookie file
    if os.path.exists(COOKIE_FILE):
        os.remove(COOKIE_FILE)


# --- Inventory commands ---
@cli.command()
def list():
    """List all inventory items"""
    response = session.get(API_URL + "/")
    try:
        click.echo(response.json())
    except ValueError:
        click.echo(response.text)


@cli.command()
@click.argument("item_id")
def view(item_id):
    """View a single item by ID"""
    response = session.get(f"{API_URL}/{item_id}")
    try:
        click.echo(response.json())
    except ValueError:
        click.echo(response.text)


@cli.command()
@click.option("--name", required=True)
@click.option("--brand", required=True)
@click.option("--price", required=True, type=float)
@click.option("--stock", required=True, type=int)
@click.option("--barcode", required=True)
def add(name, brand, price, stock, barcode):
    """Add a new item"""
    data = {
        "product_name": name,
        "brands": brand,
        "price": price,
        "stock": stock,
        "barcode": barcode,
    }
    response = session.post(API_URL + "/", json=data)
    try:
        click.echo(response.json())
    except ValueError:
        click.echo(response.text)


@cli.command()
@click.argument("item_id")
@click.option("--stock", type=int)
@click.option("--price", type=float)
def update(item_id, stock, price):
    """Update stock or price of an item"""
    data = {}
    if stock is not None:
        data["stock"] = stock
    if price is not None:
        data["price"] = price
    response = session.patch(f"{API_URL}/{item_id}", json=data)
    try:
        click.echo(response.json())
    except ValueError:
        click.echo(response.text)


@cli.command()
@click.argument("item_id")
def delete(item_id):
    """Delete an item"""
    response = session.delete(f"{API_URL}/{item_id}")
    try:
        click.echo(response.json())
    except ValueError:
        click.echo(response.text)


@cli.command()
@click.argument("barcode")
def fetch(barcode):
    """Fetch product details from OpenFoodFacts"""
    response = session.get(f"{API_URL}/fetch/{barcode}")
    try:
        click.echo(response.json())
    except ValueError:
        click.echo(response.text)


@cli.command()
@click.option("--username", required=True)
@click.option("--password", required=True)
@click.option("--role", default="viewer", help="Role: admin, staff, or viewer")
def register(username, password, role):
    """Register a new user"""
    response = session.post(
        API_URL + "/register",
        json={"username": username, "password": password, "role": role},
    )
    try:
        click.echo(response.json())
    except ValueError:
        click.echo(response.text)


if __name__ == "__main__":
    cli()


# python3 app/cli.py register --username Herman --password herman123 --role admin
# python3 app/cli.py register --username Herman --password herman123 --role admin
# python3 app/cli.py login --username staff --password staff123
# python3 app/cli.py add --name "Orange Juice" --brand "Tropicana" --price 4.50 --stock 12 --barcode 555555555555
# python3 app/cli.py update 1 --stock 20
# python3 app/cli.py delete 1
# python3 app/cli.py logout
