import csv

# Set bulb to measure and corresponding powermeter
delay_time_secs = 10
entity_id = data.get("entity_id", " ")
powermeter = data.get("powermeter", " ")

for bri in range(1, 256):
    for m in range(153, 501):
        print(bri, m)
        # 1.Set specified Bulb to current bri,r,g,b values
        service_data = {"entity_id": entity_id, "color_temp": m, "brightness": bri}
        hass.services.call("light", "turn_on", service_data, False)
        # 2.Wait 30 Seconds to get correct power values
        time.sleep(delay_time_secs)
        # 3.Read power values
        w = hass.states.get(powermeter)
        # 4.Write power values with bri and m values to csv
        with open("light_measures_mired.csv", mode="w", newline="") as csv_file:
            fieldnames = ["manufacturer", "bulb", "brightness", "mired", "power"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # writer.writeheader()
            writer.writerow({"manufacturer": "Signify", "bulb": "Test", "brightness": bri, "mired": m, "power": w})
