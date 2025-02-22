# payments.py
from fastapi import APIRouter, HTTPException
from models import PaymentCreate, PaymentUpdate
import crud

router = APIRouter()


@router.post("/payments", status_code=201)
def create_payment(payment: PaymentCreate):
    payment_id = crud.create_payment(
        payment.user_id,
        payment.stripe_charge_id,
        payment.amount,
        payment.currency,
        payment.payment_status
    )
    return {"message": "Payment created successfully", "payment_id": payment_id}

@router.get("/payments/{payment_id}")
def get_payment(payment_id: int):
    payment = crud.get_payment_by_id(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.put("/payments/{payment_id}")
def update_payment(payment_id: int, payment_update: PaymentUpdate):
    updated_payment = crud.update_payment(
        payment_id,
        stripe_charge_id=payment_update.stripe_charge_id,
        amount=payment_update.amount,
        currency=payment_update.currency,
        payment_status=payment_update.payment_status
    )
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment

@router.delete("/payments/{payment_id}")
def delete_payment(payment_id: int):
    success = crud.delete_payment(payment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted successfully"}
