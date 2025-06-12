from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+
import pandas as pd
import time

# --- Constants --------------------------------------------------------------
FILE_PATH = "carbon-monitor-carbonmonitorGLOBAL-WORLD(datas).csv"
SECONDS_PER_DAY = 24 * 60 * 60
UPDATE_INTERVAL_SEC = 2
TZ = ZoneInfo("America/Los_Angeles")

# --- Parse and Load Total CO2 Emissions for Today ---------------------------
def load_total_today_emissions() -> float:
    df = pd.read_csv(FILE_PATH, names=["region", "date", "sector", "co2_mt"])
    
    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, "%m/%d/%Y").date()
        except:
            try:
                return datetime.strptime(date_str, "%d/%m/%Y").date()
            except:
                try:
                    return pd.to_datetime(date_str).date()
                except:
                    return None

    df["date"] = df["date"].apply(parse_date)
    df = df.dropna(subset=["date"])

    # Match current day but forced to 2024
    today_2024 = datetime.now(TZ).date().replace(year=2024)
    today_data = df[df["date"] == today_2024]

    total_today_mt = today_data["co2_mt"].sum()
    total_today_metric_tons = total_today_mt * 1_000_000
    return total_today_metric_tons

# --- Format numbers compactly -----------------------------------------------
def k_format(val: float) -> str:
    if val >= 1_000_000_000:
        return f"{val / 1_000_000_000:.1f}B".rstrip('0').rstrip('.')
    elif val >= 1_000_000:
        return f"{val / 1_000_000:.1f}M".rstrip('0').rstrip('.')
    elif val >= 1_000:
        return f"{val / 1_000:.0f}k"
    else:
        return f"{val:,.0f}"

# --- Calculate emissions so far today ---------------------------------------
def emissions_so_far(now: datetime, total_today: float) -> float:
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elapsed_seconds = (now - midnight).total_seconds()
    elapsed_seconds = max(0, min(elapsed_seconds, SECONDS_PER_DAY))
    return total_today * (elapsed_seconds / SECONDS_PER_DAY)

# --- Main loop --------------------------------------------------------------
def run_counter():
    current_day = None
    total_today = 0

    while True:
        now = datetime.now(TZ)
        today = now.date()

        # Reload total if new day
        if today != current_day:
            total_today = load_total_today_emissions()
            current_day = today

        emitted = emissions_so_far(now, total_today)

        # Variables for dashboard
        CarbonDioxideEmissions = f"{emitted:,.0f}"#carbon dioxide emissions for today                               #DISPLAYED VARIABLE: CarbonDioxideEmissions
        GreatPyramidsofGiza = k_format(emitted / 5750000)#great pyramids of giza                                    #DISPLAYED VARIABEL: GreatPyramidsofGiza  
 
        # ✅ Actual Output
        #print(f"{now.isoformat(timespec='seconds')}  →  "
              #f"{CarbonDioxideEmissions} t CO₂ so far today "
              #f"({GreatPyramidsofGiza} Great Pyramids of Gizas)")
        
        

        # Wait until the next 2-second boundary
        time_to_next_tick = UPDATE_INTERVAL_SEC - (now.second % UPDATE_INTERVAL_SEC)
        time.sleep(time_to_next_tick)

# --- Run --------------------------------------------------------------------
if __name__ == "__main__":
    run_counter()
