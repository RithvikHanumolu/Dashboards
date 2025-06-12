from datetime import datetime, timedelta
from zoneinfo import ZoneInfo   # Python 3.9+
import time

# --- constants --------------------------------------------------------------
TOTAL_DAILY_MG      = 714.0                 # average mg of microplastic ingested per person per day
SECONDS_PER_DAY     = 24 * 60 * 60          # 86,400
MG_PER_SECOND       = TOTAL_DAILY_MG / SECONDS_PER_DAY
UPDATE_INTERVAL_SEC = 2                     # update frequency in seconds
TZ                  = ZoneInfo("America/Los_Angeles")

# --- helper -----------------------------------------------------------------
def mg_ingested_so_far(now: datetime) -> float:
    """Return milligrams ingested from today's 00:00 up to 'now'."""
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elapsed  = (now - midnight).total_seconds()
    elapsed  = max(0, min(elapsed, SECONDS_PER_DAY))
    return MG_PER_SECOND * elapsed

# --- main loop --------------------------------------------------------------
def run_counter():
    #print("Continuous microplastic-ingestion counter started… (Ctrl-C to stop)\n")
    while True:
        now      = datetime.now(TZ)
        ingested = mg_ingested_so_far(now)
        #print(f"{now.isoformat(timespec='seconds')}  →  "
              #f"{ingested:,.2f} mg ingested so far today")

        # Sleep until the next 2-second boundary
        time_to_next_tick = UPDATE_INTERVAL_SEC - (now.second % UPDATE_INTERVAL_SEC)
        time.sleep(time_to_next_tick)

        plasticIngested = f"{ingested:,.0f}" #plastic ingested                           DISPLAYED VARIABLE-- plasticIngested
        initial = (ingested/5000)*7
        CreditCard = initial * 100            
        CreditCard_display = f"{CreditCard:.0f}%"                                                            #I don't think you should display, but you can if you want to (credit card in a week)

        print(CreditCard_display)

        #just keep one displayed for credit card becuase that would be a weekly value, and if I don't do that it would just be a very small decimal (unless you want that)




# --- run --------------------------------------------------------------------
if __name__ == "__main__":
    run_counter()
