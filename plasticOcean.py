from datetime import datetime, timedelta
from zoneinfo import ZoneInfo   # Python 3.9+
import time

# --- constants --------------------------------------------------------------
TOTAL_DAILY_KG      = 30_136_986               # daily ocean-bound plastic
SECONDS_PER_DAY     = 24 * 60 * 60             # 86,400
KG_PER_SECOND       = TOTAL_DAILY_KG / SECONDS_PER_DAY
UPDATE_INTERVAL_SEC = 2
TZ                  = ZoneInfo("America/Los_Angeles")

# --- helper -----------------------------------------------------------------
def kg_entered_so_far(now: datetime) -> float:
    """Kilograms of plastic that have entered the ocean since midnight today."""
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elapsed  = (now - midnight).total_seconds()
    elapsed  = max(0, min(elapsed, SECONDS_PER_DAY))
    return KG_PER_SECOND * elapsed

# --- main loop --------------------------------------------------------------
def run_counter():
    #print("Continuous ocean-plastic counter started… (Ctrl-C to stop)\n")
    while True:
        now     = datetime.now(TZ)
        entered = kg_entered_so_far(now)
        #print(f"{now.isoformat(timespec='seconds')}  →  "
              #f"{entered:,.0f} kg entered the ocean today")

        time_to_next_tick = UPDATE_INTERVAL_SEC - (now.second % UPDATE_INTERVAL_SEC)
        time.sleep(time_to_next_tick)

        plasticEnteredOcean = f"{entered:,.0f}" #plastic entering ocean                                    DISPLAYED VARIABLE-- plasticEnteredOcean
        initial = entered/204116
        StatueOfLiberty = f"{initial:,.0f}" #Statue of liberties                                           DISPLAYED VARIABLE-- StatueOfLiberty



# --- run --------------------------------------------------------------------
if __name__ == "__main__":
    run_counter()
