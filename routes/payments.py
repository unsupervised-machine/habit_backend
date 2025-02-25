# payments.py
from fastapi import APIRouter, HTTPException, status
from models import PaymentCreate
import crud

router = APIRouter()


@router.post("/payments", status_code=status.HTTP_201_CREATED, response_description="Creates a payment", response_model=PaymentCreate)
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

# @router.put("/payments/{payment_id}")
# def update_payment(payment_id: int, payment_update: PaymentUpdate):
#     update_data = payment_update.model_dump(exclude_unset=True)  # Only include changed fields
#
#     if not update_data:  # If no fields were updated, return the existing payment or an error
#         raise HTTPException(status_code=400, detail="No fields provided for update")
#
#     updated_payment = crud.update_payment(payment_id, **update_data)
#
#     if not updated_payment:
#         raise HTTPException(status_code=404, detail="Payment not found")
#
#     return updated_payment

@router.delete("/payments/{payment_id}")
def delete_payment(payment_id: int):
    success = crud.delete_payment(payment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"message": "Payment deleted successfully"}
