    async def get_payment(self, payment_id: str) -> Optional[dict]:
        """Retrieve payment by ID."""
        from bson import ObjectId
        if not ObjectId.is_valid(payment_id):
            return None
        payment = await self.payments_collection.find_one({"_id": ObjectId(payment_id)})
        if payment:
            payment["_id"] = str(payment["_id"])
        return payment

    async def get_quiz_payments(self, quiz_id: str) -> list:
        """Get all payments for a quiz."""
        return list(self.payments_collection.find({"quiz_id": quiz_id}).sort("created_at", -1))