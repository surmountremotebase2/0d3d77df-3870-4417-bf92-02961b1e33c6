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

        if not ohlcv or len(ohlcv) < 252:
            log("Not enough data for 52-week low calculation.")
            return None  # Return None instead of empty TargetAllocation

        past_year_data = ohlcv[-252:]
        prices = [day["NKE"]["low"] for day in past_year_data]
        fifty_two_week_low = min(prices)

        current_price = ohlcv[-1]["NKE"]["close"]
        dip_threshold = 0.05
        buy_zone_upper_limit = fifty_two_week_low * (1 + dip_threshold)
        allocation_percentage = 0.5

        if current_price <= buy_zone_upper_limit:
            log(f"NKE is within {dip_threshold*100}% of its 52-week low. Allocating {allocation_percentage*100}%.")
            return TargetAllocation({"NKE": allocation_percentage})
        else:
            log("NKE is not near its 52-week low. No allocation.")
            return None  # Return None instead of empty TargetAllocation