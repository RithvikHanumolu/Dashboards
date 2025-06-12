from datetime import datetime, timedelta
from zoneinfo import ZoneInfo   # Python 3.9+
import time

# --- constants --------------------------------------------------------------
TOTAL_DAILY_ACRES    = 202_513               # acres of forest lost per day in 2024
SECONDS_PER_DAY      = 24 * 60 * 60          # 86,400
ACRES_PER_SECOND     = TOTAL_DAILY_ACRES / SECONDS_PER_DAY
UPDATE_INTERVAL_SEC  = 2                     # update frequency (seconds)
TZ                   = ZoneInfo("America/Los_Angeles")

# --- helper -----------------------------------------------------------------
def acres_lost_so_far(now: datetime) -> float:
    """Return acres lost from today's 00:00 up to 'now'."""
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elapsed  = (now - midnight).total_seconds()
    elapsed  = max(0, min(elapsed, SECONDS_PER_DAY))
    return ACRES_PER_SECOND * elapsed

# --- helper: nice formatter -----------------------------------------------
def k_format(val: float) -> str:
    """
    Return '130k' for 130 000, '1.5M' for 1 500 000, etc.
    Extend as needed for millions/billions.
    """
    if val >= 1_000_000:
        return f"{val/1_000_000:.1f}M".rstrip('0').rstrip('.')
    elif val >= 1_000:
        return f"{val/1_000:.0f}k"
    else:
        return f"{val:,.0f}"


# --- main loop --------------------------------------------------------------
def run_counter():
    #print("🌲 Forest loss counter started… (Ctrl-C to stop)\n")
    while True:
        now   = datetime.now(TZ)
        lost  = acres_lost_so_far(now)
        #print(f"{now.isoformat(timespec='seconds')}  →  "
              #f"{lost:,.2f} acres lost so far today")

        # Sleep until the next 2-second boundary
        time_to_next_tick = UPDATE_INTERVAL_SEC - (now.second % UPDATE_INTERVAL_SEC)
        time.sleep(time_to_next_tick)

        acresLost = f"{lost:,.0f}" #acres lost                                                          DISPLAYED VARIABLE-- acresLost
        initial = lost/1.32
        FootballFields = k_format(initial) #football fields                                             DISPLAYED VARIABLE-- FootballFields    

        print(acresLost)                                                      

# --- run --------------------------------------------------------------------
if __name__ == "__main__":
    run_counter()
