# Set bulb to measure and corresponding powermeter
delay_time_secs = 30
entity_id = data.get("entity_id", " ")
powermeter = data.get("powermeter", " ")

for bri in range(1, 10):
    for r in range(1, 10):
        for g in range(1, 10):
            for b in range(1, 10):
                print(bri, r, g, b)
                # 1.Set specified Bulb to current bri,r,g,b values
                service_data = {"entity_id": entity_id, "rgb_color": [r, g, b], "brightness": bri}
                hass.services.call("light", "turn_on", service_data, False)
                # 2.Wait 30 Seconds to get correct power values
                time.sleep(delay_time_secs)
                # 3.Read power values
                powerconsumption = hass.states.get(powermeter)
                # 4.Write power values with bri,r,g,b values to specified database
                try:
                    connection = psycopg2.connect(user="simon", password="cmonmpw1", host="192.168.178.3", port="5442", database="ha_sensordata")
                    cursor = connection.cursor()
                    # YOU HAVE TO CREATE THE TABLE MANUALLY BEFORE YOU TRY TO INSERT SOME VALUES!
                    # CREATE TABLE powermeasures_rgb (manufacturer CHAR, bulb CHAR, bri INTEGER, r INTEGER, g INTEGER, b INTEGER);
                    postgres_insert_query = """ INSERT INTO powermeasures_rgb (manufacturer, bulb, bri, r, g, b) VALUES (%s,%s,%s,%s,%s,%s)"""
                    record_to_insert = ("signify", "testbulb", bri, r, g, b)
                    cursor.execute(postgres_insert_query, record_to_insert)

                    connection.commit()
                    count = cursor.rowcount
                    print(count, "Record inserted successfully into powermeasures_rgb table")

                except (Exception, psycopg2.Error) as error:
                    print("Failed to insert record into powermeasures_rgb table", error)

                finally:
                    # closing database connection.
                    if connection:
                        cursor.close()
                        connection.close()
                        print("PostgreSQL connection is closed")
