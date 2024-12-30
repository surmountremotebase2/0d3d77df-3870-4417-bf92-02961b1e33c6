from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

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

        if not ohlcv or len(ohlcv) < 90:  # Ensure we have at least 90 days of data
            log("Not enough data for 90-day low calculation.")
            return None

        # Calculate 90-day low
        past_90_days_data = ohlcv[-90:]  # Get the last 90 days of data
        prices = [day["NKE"]["low"] for day in past_90_days_data]
        ninety_day_low = min(prices)

        current_price = ohlcv[-1]["NKE"]["close"]

        # Buy only if the current price is the 90-day low and we don't already own it
        if holdings.get("NKE", 0) == 0 and current_price == ninety_day_low:
            log(f"NKE is at its 90-day low. Buying.")
            return TargetAllocation({"NKE": 1}) # Allocate 100%
        else:
            log("NKE is not at its 90-day low, or position already held. No action.")
            return None