from fastapi import APIRouter, Form, Depends, HTTPException, status, Request
from datetime import datetime, timedelta
from app.dependencies import check_jwt_token, get_db
from app.config import settings
from jose import jwt
from typing import Optional
from app.core.schemas.users import UserBase
from sqlalchemy.orm import Session
from app.core.models.coin import Base, Apply, Consume, Bill
from app.core.models.users import Users
from app.core.models.item import Item
from app.database import engine
import json

Base.metadata.create_all(bind=engine)

item = APIRouter(
    prefix="/api/item",
    tags=["item"],
    responses={404: {"description": "Not found"}},
)

@coin.get("/fetch_apply")
async def fetch_apply(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    apply_items = db.query(Apply).filter_by(user_id=user.id, apply_status=None).all()
    all_apply = [{"id":row.id, "repo":row.repo, "role":row.role, "content":row.content, "record_time":row.record_time} for row in apply_items]
    return all_apply

@item.get("/fetch_item")
async def fetch_item(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    return db.query(Item).all()

@item.post("/add_item")
async def add_item(item: Item,user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    new_item = item
    new_item.create_time=datetime.now()
    new_item.create_user=user.id
    try:
        db.add(new_item)
        db.commit()
        return {"code": 200, "message":"OK"}
    except Exception as e:
        return {"code":500,"message":e}
@item.get()
@coin.post("/handle_apply")
async def handle_apply(action: str = Form(...), id: int = Form(...), db: Session = Depends(get_db)):
    applyitem = db.query(Apply).filter_by(id=id).first()
    applyitem.apply_time = datetime.now()
    if action=="cancel":
        applyitem.apply_status = False
    elif action=="apply":
        applyitem.apply_status = True
    db.commit()
    return {"code": 200, "message":"OK"}


@coin.get("/fetch_supervise")
async def fetch_supervise(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    supervise_items = db.query(Apply).filter(
        Apply.user_id==user.id, 
        Apply.apply_status!=None,
        Apply.decision==None,
        ).all()
    all_supervise = []
    for row in supervise_items:
        temp = {"id":row.id, 
                "user_id":row.user_id, 
                "repo":row.repo, 
                "role":row.role, 
                "content":row.content, 
                "record_time":row.record_time, 
                "apply_status":row.apply_status,
                "apply_time":row.apply_time}
        temp["user_name"] = db.query(Users).filter_by(id=user.id).first().username
        all_supervise.append(temp)
    return all_supervise

@coin.post("/handle_supervise")
async def handle_supervise(action: str = Form(...), notes: str = Form(...), id: int = Form(...), amount: int = Form(...), user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    superviseitem = db.query(Apply).filter_by(id=id).first()
    superviseitem.confirm_time = datetime.now()
    superviseitem.notes = notes
    superviseitem.supervisor_id = user.id
    if action=="reject":
        superviseitem.decision = False
    elif action=="grant":
        superviseitem.decision = True
        superviseitem.coin_amount = amount
        useritem = db.query(Users).filter_by(id=id).first()
        useritem.coin = useritem.coin + amount
        new_bill = Bill(
            user_id=id,
            type="奖励",
            content=superviseitem.content,
            change_amount=amount,
            balance=useritem.coin,
            create_time=datetime.now()
        )
        db.add(new_bill)
    db.commit()
    return {"code": 200, "message":"OK"}

@coin.get("/fetch_consume")
async def fetch_consume(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    consume_items = db.query(Consume).all()
    all_consume = []
    for row in consume_items:
        temp = {"id":row.id, 
                "user_id":row.user_id, 
                "content":row.content, 
                "record_time":row.confirm_time, 
                "amount":row.price}
        temp["user_name"] = db.query(Users).filter_by(id=row.user_id).first().username
        temp["balance"] = db.query(Users).filter_by(id=row.user_id).first().coin
        all_consume.append(temp)
    all_consume.reverse()
    return all_consume

@coin.post("/handle_consume")
async def handle_consume(content: str = Form(...), user_id: int = Form(...), amount: int = Form(...), user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    useritem = db.query(Users).filter_by(id=user_id).first()
    useritem.coin = useritem.coin - amount
    new_consume = Consume(
        user_id=user_id,
        content=content,
        confirm_time=datetime.now(),
        price=amount,
    )
    db.add(new_consume)
    db.flush()
    new_bill = Bill(
        user_id=user_id,
        type="消费",
        content=content,
        change_amount=amount,
        balance=useritem.coin,
        create_time=datetime.now()
    )
    db.add(new_bill)
    db.commit()
    return {"code": 200, "balance":useritem.coin, "consume_id":new_consume.id}


@coin.get("/fetch_bill")
async def fetch_bill(user: UserBase = Depends(check_jwt_token), db: Session = Depends(get_db)):
    bill_items = db.query(Bill).filter(
        Bill.user_id==user.id, 
        ).all()
    all_bill = []
    for row in bill_items:
        temp = {"id":row.id, 
                "type":row.type, 
                "content":row.content, 
                "change_amount":row.change_amount,
                "balance":row.balance,
                "create_time":row.create_time}
        all_bill.append(temp)
    all_bill.reverse()
    return all_bill