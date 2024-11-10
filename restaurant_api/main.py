from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, schemas  # Import models and schemas

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/restaurants/")
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    db_restaurant = models.Restaurant(
        name=restaurant.name,
        address=restaurant.address,
        hours_of_operation=restaurant.hours_of_operation,
        owner_id=restaurant.owner_id  # assuming owner_id is provided by auth system
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@app.post("/restaurants/{restaurant_id}/menu/")
def add_menu_item(restaurant_id: int, menu_item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    db_menu_item = models.MenuItem(
        restaurant_id=restaurant_id,
        name=menu_item.name,
        description=menu_item.description,
        price=menu_item.price,
        available=menu_item.available
    )
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

@app.put("/menu/{item_id}")
def update_menu_item(item_id: int, menu_item: schemas.MenuItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    for key, value in menu_item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/menu/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(db_item)
    db.commit()
    return {"message": "Menu item deleted successfully"}


@app.get("/restaurants/{restaurant_id}/orders/")
def view_orders(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.restaurant_id == restaurant_id).all()

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order
