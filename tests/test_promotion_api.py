import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.models import Promotion
from app.routes.promotion import apply_promotion
from app.schemas.promotion import ApplyPromotion, PromotionResult


class PromotionApplyApiTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)
        self.db = Session(self.engine)

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def apply_code(self, code):
        result = apply_promotion(
            ApplyPromotion(code=code, order_total=50),
            self.db,
        )
        return PromotionResult.model_validate(result)

    def test_unknown_code_returns_valid_response(self):
        result = self.apply_code("UNKNOWN")

        self.assertFalse(result.is_valid)
        self.assertEqual(result.final_total, 50)
        self.assertIsNone(result.promotion_id)

    def test_valid_code_keeps_promotion_details(self):
        self.db.add(
            Promotion(
                code="SAVE10",
                title="Ten percent off",
                discount_type="percentage",
                discount_value=10,
                min_order_amount=0,
            )
        )
        self.db.commit()

        result = self.apply_code("SAVE10")

        self.assertTrue(result.is_valid)
        self.assertEqual(result.promotion_id, 1)
        self.assertEqual(result.discount_amount, 5)
        self.assertEqual(result.final_total, 45)


if __name__ == "__main__":
    unittest.main()
