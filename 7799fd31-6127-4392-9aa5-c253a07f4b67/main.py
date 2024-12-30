from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.technical_indicators import ATR

class TradingStrategy(Strategy):

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return ["NKE"]

    def run(self, data):
        ohlcv = data.get("ohlcv")
        holdings = data.get("holdings")

        if not ohlcv or len(ohlcv) < 90:
            log("Not enough data for calculations.")
            return None

        # Calculate 90-day low
        past_90_days_data = ohlcv[-90:]
        prices = [day["NKE"]["low"] for day in past_90_days_data]
        ninety_day_low = min(prices)

        # Calculate 14-day ATR
        atr_14 = ATR("NKE", ohlcv, 14)

        if atr_14 is None:
            log("Not enough data for ATR calculation")
            return None

        current_price = ohlcv[-1]["NKE"]["close"]

        # Dynamic Buy Zone: 90-day low + (ATR * 0.5)
        # We're using 50% of the ATR as our buffer. You can adjust this multiplier.
        buy_zone_upper_limit = ninety_day_low + (atr_14[-1] * 0.5)

        # Partial Purchase Logic (3 tiers)
        if holdings.get("NKE", 0) == 0:
            if current_price <= buy_zone_upper_limit:
                log(f"NKE is within the dynamic buy zone. Initiating first purchase (30%).")
                return TargetAllocation({"NKE": 0.3}) # First purchase: 30%

        elif holdings.get("NKE",0) > 0 and holdings.get("NKE", 0) < 0.6:
          if current_price <= ninety_day_low + (atr_14[-1] * 0.3):
            log(f"NKE is within the dynamic buy zone. Initiating second purchase (30%).")
            return TargetAllocation({"NKE": holdings.get("NKE",0)+0.3}) # Second purchase

        elif holdings.get("NKE", 0) >= 0.6 and holdings.get("NKE", 0) < 1:
            if current_price <= ninety_day_low:
                log(f"NKE is at 90-day low. Initiating final purchase (40%).")
                return TargetAllocation({"NKE": 1})  # Final purchase to reach 100%

        log("NKE is not within the dynamic buy zone, or position already held at max. No action.")
        return None