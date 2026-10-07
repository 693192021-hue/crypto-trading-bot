from app.config import RISK_PER_TRADE, STOP_LOSS_PCT, TAKE_PROFIT_PCT


class RiskManager:
    def __init__(self, balance: float):
        self.balance = balance

    def position_size(self, entry_price: float, side: str) -> float:
        if entry_price <= 0:
            return 0.0

        risk_amount = self.balance * RISK_PER_TRADE
        stop_distance = entry_price * STOP_LOSS_PCT
        if stop_distance <= 0:
            return 0.0

        qty = risk_amount / stop_distance
        return qty if side in {"long", "short"} else 0.0

    def stop_loss_price(self, entry_price: float, side: str) -> float:
        if side == "long":
            return entry_price * (1 - STOP_LOSS_PCT)
        if side == "short":
            return entry_price * (1 + STOP_LOSS_PCT)
        return entry_price

    def take_profit_price(self, entry_price: float, side: str) -> float:
        if side == "long":
            return entry_price * (1 + TAKE_PROFIT_PCT)
        if side == "short":
            return entry_price * (1 - TAKE_PROFIT_PCT)
        return entry_price

