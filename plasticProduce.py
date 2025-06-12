from datetime import datetime, timedelta
from zoneinfo import ZoneInfo   # Python 3.9+
import time

# --- constants
TOTAL_DAILY_KG      = 1_260_273_973            # daily plastic production
SECONDS_PER_DAY     = 24 * 60 * 60             # 86,400
KG_PER_SECOND       = TOTAL_DAILY_KG / SECONDS_PER_DAY
UPDATE_INTERVAL_SEC = 2                        # update frequency (s)
TZ                  = ZoneInfo("America/Los_Angeles")

# --- helper 
def kg_produced_so_far(now: datetime) -> float:
    """Return kilograms produced from today's 00:00 up to 'now'."""
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elapsed  = (now - midnight).total_seconds()
    elapsed  = max(0, min(elapsed, SECONDS_PER_DAY))  # clamp elapsed seconds to a day
    return KG_PER_SECOND * elapsed

# --- main loop
def run_counter():
    #print("Continuous plastic-production counter started… (Ctrl-C to stop)\n")
    while True:
        now      = datetime.now(TZ)
        produced = kg_produced_so_far(now)
        #print(f"{now.isoformat(timespec='seconds')}  →  "
              #f"{produced:,.0f} kg produced so far today")

        # Sleep until the next 2-second boundary
        time_to_next_tick = UPDATE_INTERVAL_SEC - (now.second % UPDATE_INTERVAL_SEC)
        time.sleep(time_to_next_tick)

        plasticProduce = f"{produced:,.0f}" #plastic produced                                               DISPLAYED VARIABLE-- plasticProduce
        initial = produced/1500
        cars = f"{initial:,.0f}" #cars                                                                      DISPLAYED VARIABLE-- cars

        #print(plasticProduce)
        #print(cars)

# --- run
if __name__ == "__main__":
    run_counter()
