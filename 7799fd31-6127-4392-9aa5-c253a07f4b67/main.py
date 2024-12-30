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

        if not ohlcv or len(ohlcv) < 30:  # Ensure we have at least 30 days of data
            log("Not enough data for 30-day low calculation.")
            return None

        # Calculate 30-day low
        past_month_data = ohlcv[-30:]  # Get the last 30 days of data
        prices = [day["NKE"]["low"] for day in past_month_data]
        thirty_day_low = min(prices)

        current_price = ohlcv[-1]["NKE"]["close"]

        # Define dip threshold (e.g., within 5% of 30-day low)
        dip_threshold = 0.05
        buy_zone_upper_limit = thirty_day_low * (1 + dip_threshold)

        # Define allocation percentage (e.g., 50% of portfolio)
        allocation_percentage = 0.50

        if current_price <= buy_zone_upper_limit:
            log(f"NKE is within {dip_threshold*100}% of its 30-day low. Allocating {allocation_percentage*100}%.")
            return TargetAllocation({"NKE": allocation_percentage})
        else:
            log("NKE is not near its 30-day low. No allocation.")
            return None