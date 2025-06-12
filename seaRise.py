from datetime import datetime
from zoneinfo import ZoneInfo   # Python ≥3.9
import time

# ── constants ────────────────────────────────────────────────────────────────
TOTAL_DAILY_HA      = 437.16                 # hectares lost per day (2024 estimate)
SECONDS_PER_DAY     = 24 * 60 * 60           # 86 400
HA_PER_SECOND       = TOTAL_DAILY_HA / SECONDS_PER_DAY
UPDATE_INTERVAL_SEC = 2                      # update frequency
TZ                  = ZoneInfo("America/Los_Angeles")

# ── helper ───────────────────────────────────────────────────────────────────
def hectares_lost_so_far(now: datetime) -> float:
    """Return hectares lost from today's 00:00 (local) up to 'now'."""
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elapsed  = (now - midnight).total_seconds()
    elapsed  = max(0, min(elapsed, SECONDS_PER_DAY))      # clamp to one day
    return HA_PER_SECOND * elapsed

# ── main loop ────────────────────────────────────────────────────────────────
def run_counter():
    #print("🌊 Sea-level-rise land-loss counter started… (Ctrl-C to stop)\n")
    while True:
        now   = datetime.now(TZ)
        lost  = hectares_lost_so_far(now)
        #print(f"{now.isoformat(timespec='seconds')}  →  "
              #f"{lost:,.2f} ha lost so far today")

        # sleep just enough to hit the next 2-second boundary
        time_to_next_tick = UPDATE_INTERVAL_SEC - (now.second % UPDATE_INTERVAL_SEC)
        time.sleep(time_to_next_tick)

        landLost = f"{lost:,.0f}" #land lost                                             DISPLAYED VARIABLE-- landLost
        initial = (lost/1500)*365
        WashingtonDC = f"{initial:,.0f}" #percntage of WashingtonDC gone in a year           DISPLAYED VARIABLE-- WashingtonDC

        #print(landLost)
        #print(WashingtonDC)




# ── run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_counter()
