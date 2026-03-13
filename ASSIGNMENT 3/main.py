from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Product Schema
class Product(BaseModel):
    name: str
    price: float
    category: str
    in_stock: bool


# Initial Inventory
inventory = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 3, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "Pen Pack", "price": 59, "category": "Stationery", "in_stock": True}
]


# Generate new ID
def create_product_id():
    return max(item["id"] for item in inventory) + 1


# Q1 – Add Product
@app.post("/products", status_code=201)
def register_product(product_data: Product):

    # Check duplicate names
    for item in inventory:
        if item["name"].lower() == product_data.name.lower():
            raise HTTPException(status_code=400, detail="Product already exists")

    new_item = {
        "id": create_product_id(),
        **product_data.dict()
    }

    inventory.append(new_item)

    return {
        "message": "New product registered",
        "product": new_item
    }


# Q2 – Update Product
@app.put("/products/{product_id}")
def modify_product(product_id: int, product_data: Product):

    for index, item in enumerate(inventory):
        if item["id"] == product_id:

            inventory[index] = {
                "id": product_id,
                **product_data.dict()
            }

            return {
                "message": "Product details updated",
                "product": inventory[index]
            }

    raise HTTPException(status_code=404, detail="Product not found")


# Q3 – Delete Product
@app.delete("/products/{product_id}")
def remove_product(product_id: int):

    for index, item in enumerate(inventory):
        if item["id"] == product_id:

            removed_product = inventory.pop(index)

            return {
                "message": "Product removed from inventory",
                "product": removed_product
            }

    raise HTTPException(status_code=404, detail="Product not found")


# Q4 – View Inventory
@app.get("/products")
def view_products():

    return {
        "total_items": len(inventory),
        "product_list": inventory
    }


# Q5 – Inventory Summary
@app.get("/products/audit")
def audit_inventory():

    total_items = len(inventory)
    available = sum(1 for item in inventory if item["in_stock"])
    unavailable = total_items - available

    return {
        "total_products": total_items,
        "available_products": available,
        "out_of_stock_products": unavailable
    }


# BONUS – Discount API
@app.put("/products/discount/{category}")
def category_discount(category: str, discount: float):

    changed_products = []

    for item in inventory:
        if item["category"].lower() == category.lower():

            item["price"] = round(item["price"] * (1 - discount / 100), 2)
            changed_products.append(item)

    if not changed_products:
        raise HTTPException(status_code=404, detail="Category not found")

    return {
        "message": f"{discount}% discount applied to {category}",
        "updated_products": changed_products
    }