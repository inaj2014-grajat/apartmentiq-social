#!/usr/bin/env python3
"""sun_facts.py: every sun number an ApartmentIQ post may show comes from here.

WHY THIS FILE EXISTS
ApartmentIQ's rule is "figures are derived, never typed". A post may only show a
number that this script printed. lint_aiq.py re-runs this script for every number
in a post and fails the post if the printed value differs from the slide.

METHOD
NOAA general solar position equations (the low-accuracy set NOAA publishes for
its solar calculator: fractional year, equation of time, declination, hour angle).
Good to about 0.1 degree and about 1 minute, which is finer than any post needs.
Sunrise and sunset use a zenith of 90.833 degrees (refraction + sun's radius).

WHAT IT DOES NOT KNOW
Terrain, buildings, haze, trees. It gives the sun's position for a clear sky
over flat ground. It says nothing about any one flat. Never present its output
as a flat's sun hours: those come only from the ApartmentIQ model.

USE
  python3 -I sun_facts.py --place noida --date 2026-12-21
  python3 -I sun_facts.py --place noida --date 2026-12-21 --time 11:00 --height 100
Prints one JSON object. Field names are stable; lint_aiq.py reads them.
"""
import argparse, json, math, datetime as dt

PLACES = {  # city-centre coordinates, decimal degrees; tz = hours ahead of UTC
    "noida": {"lat": 28.5355, "lon": 77.3910, "tz": 5.5, "label": "Noida"},
    "gurugram": {"lat": 28.4595, "lon": 77.0266, "tz": 5.5, "label": "Gurugram"},
    "delhi": {"lat": 28.6139, "lon": 77.2090, "tz": 5.5, "label": "Delhi"},
}


def _gamma(doy, hour, year):
    days = 366 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 365
    return 2 * math.pi / days * (doy - 1 + (hour - 12) / 24)


def _eqtime_decl(g):
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
                       - 0.014615 * math.cos(2 * g) - 0.040849 * math.sin(2 * g))
    decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g)
            - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g)
            - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    return eqtime, decl  # minutes, radians


def position(place, date, hh, mm):
    """Sun altitude and azimuth (degrees) at local clock time hh:mm."""
    p = PLACES[place]
    doy = date.timetuple().tm_yday
    g = _gamma(doy, hh + mm / 60 - p["tz"], date.year)  # fractional year uses UTC hour
    eqtime, decl = _eqtime_decl(g)
    tst = hh * 60 + mm + eqtime + 4 * p["lon"] - 60 * p["tz"]  # true solar time, minutes
    ha = math.radians(tst / 4 - 180)
    lat = math.radians(p["lat"])
    cosz = math.sin(lat) * math.sin(decl) + math.cos(lat) * math.cos(decl) * math.cos(ha)
    zen = math.acos(max(-1, min(1, cosz)))
    alt = 90 - math.degrees(zen)
    # azimuth, degrees clockwise from north
    cos_az = (math.sin(decl) - math.sin(lat) * math.cos(zen)) / (math.cos(lat) * math.sin(zen))
    az = math.degrees(math.acos(max(-1, min(1, cos_az))))
    if ha > 0:
        az = 360 - az
    return alt, az


def day(place, date):
    """Noon altitude, sunrise, sunset and day length for one date."""
    p = PLACES[place]
    doy = date.timetuple().tm_yday
    eqtime, decl = _eqtime_decl(_gamma(doy, 12 - p["tz"] + 0, date.year))
    lat = math.radians(p["lat"])
    ha = math.degrees(math.acos(math.cos(math.radians(90.833)) / (math.cos(lat) * math.cos(decl))
                                - math.tan(lat) * math.tan(decl)))
    noon_utc = 720 - 4 * p["lon"] - eqtime  # minutes after 00:00 UTC
    rise = noon_utc - 4 * ha + 60 * p["tz"]
    sset = noon_utc + 4 * ha + 60 * p["tz"]
    noon_alt = 90 - p["lat"] + math.degrees(decl)
    return {"noon_alt": noon_alt, "rise": rise, "set": sset, "noon": noon_utc + 60 * p["tz"],
            "length": sset - rise}


def hhmm(minutes):
    m = int(round(minutes))
    return f"{m // 60:02d}:{m % 60:02d}"


def compass(az):
    names = ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"]
    return names[int(((az + 22.5) % 360) // 45)]


def facts(place, date, time=None, height=None):
    d = day(place, date)
    L = int(round(d["length"]))
    out = {
        "place": PLACES[place]["label"], "date": date.isoformat(),
        "latitude_deg": round(PLACES[place]["lat"], 2),
        "noon_altitude_deg": round(d["noon_alt"], 1),
        "solar_noon": hhmm(d["noon"]), "sunrise": hhmm(d["rise"]), "sunset": hhmm(d["set"]),
        "day_length_min": L, "day_length": f"{L // 60} h {L % 60:02d} min",
        "method": "NOAA general solar position equations; sunrise/sunset at zenith 90.833 deg; flat ground, clear sky",
    }
    if height is not None:
        out["height_m"] = height
        out["noon_shadow_m"] = int(round(height / math.tan(math.radians(d["noon_alt"]))))
    if time is not None:
        hh, mm = [int(x) for x in time.split(":")]
        alt, az = position(place, date, hh, mm)
        out["time"] = f"{hh:02d}:{mm:02d}"
        out["altitude_deg"] = round(alt, 1)
        out["azimuth_deg"] = int(round(az))
        out["sun_direction"] = compass(az)
        out["sun_is_up"] = alt > 0
        if height is not None and alt > 0:
            out["shadow_m"] = int(round(height / math.tan(math.radians(alt))))
            out["shadow_falls_towards"] = compass((az + 180) % 360)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--place", required=True, choices=sorted(PLACES))
    ap.add_argument("--date", required=True, help="YYYY-MM-DD")
    ap.add_argument("--time", help="local clock time HH:MM")
    ap.add_argument("--height", type=float, help="height of an object in metres, for shadow length")
    a = ap.parse_args()
    print(json.dumps(facts(a.place, dt.date.fromisoformat(a.date), a.time, a.height), indent=1))
