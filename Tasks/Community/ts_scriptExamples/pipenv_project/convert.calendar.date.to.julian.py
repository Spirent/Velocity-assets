from novas import compat as novas

print("INFO: Converting Oct 2, 2012 to Julian date...")
jd_tt = novas.julian_date(2012, 10, 2, 12.0)
print("OK: " + str(jd_tt))

