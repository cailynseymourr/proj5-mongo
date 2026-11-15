# Project 5: Brevet Time Calculator with Ajax and MongoDB

**Author:** Cailyn Seymour
**Email:** cailyn@uoregon.edu

## Description

A web calculator for ACP-sanctioned brevets (200 to 1000 km). When you enter a control distance in miles or kilometers, the open and close times fill in automatically using Ajax, with no page reload. This project adds a MongoDB database:

- **Submit** saves the control times on the page to the database.
- **Display** opens a new page listing the saved control times.

## How to run

1. Install and start Docker Desktop.
2. In the `DockerMongo` folder, run:

   ```
   docker compose up --build
   ```

3. Open http://localhost:5000.

The app runs in one container (Flask) and MongoDB runs in another, defined in `docker-compose.yml`. Stop everything with `docker compose down`.

## Using the page

1. Choose the brevet distance and the start date and time.
2. Enter control distances in the Miles or Km column. The other column and the Open and Close times fill in automatically.
3. Click **Submit** to save the rows that have times.
4. Click **Display** to see the saved controls on a new page.

Submit replaces any earlier submission, so Display always shows the most recent one.

## Error handling

Submit returns a clear message (and saves nothing) when:

- no control times have been entered,
- the brevet distance is missing or not one of 200, 300, 400, 600, or 1000,
- a control distance is not a number or is negative,
- a control distance is more than 20% longer than the brevet distance,
- a control is missing its open or close time,
- the database cannot be reached.

Display shows "No control times have been saved yet" when the database is empty, and an error message if the database cannot be reached.

## Tests

`test_brevets.py` tests both buttons: Submit with no controls, an out-of-range distance, a non-numeric distance, and a valid submission; and Display with an empty database and with saved entries. With the containers running:

```
docker compose exec web python -m unittest test_brevets -v
```

## Brevet control time rules

A brevet is a long-distance cycling event. Riders must reach each control (checkpoint) within a window set by the control's distance from the start. The window is based on a minimum and maximum speed for each distance range.

| Control distance (km) | Minimum speed (km/h) | Maximum speed (km/h) |
|---|---|---|
| 0 to 200 | 15 | 34 |
| 200 to 400 | 15 | 32 |
| 400 to 600 | 15 | 30 |
| 600 to 1000 | 11.428 | 28 |

**Opening time:** the earliest time a rider can arrive. Take the part of the distance that falls in each range, divide it by that range's maximum speed, and add the results. Add the total to the start time.

**Closing time:** the latest time a rider can arrive. Do the same calculation with each range's minimum speed.

**Example:** a control at 350 km. The opening time is 200/34 + 150/32 = 5 h 53 min + 4 h 41 min = 10 h 34 min after the start. The closing time is 350/15 = 23 h 20 min after the start.

Other rules:

- Times are rounded to the nearest minute.
- A control at 0 km opens at the start time and closes one hour later.
- A control located beyond the end of the brevet (up to 20% longer) is calculated as if it were at the brevet's total distance.
- The final control (at the brevet's total distance) closes at a fixed time after the start: 13 h 30 min for 200 km, 20 h for 300 km, 27 h for 400 km, 40 h for 600 km, and 75 h for 1000 km. Its opening time uses the normal maximum-speed calculation.
- For controls closer than 60 km to the start (but not at 0 km), the closing time is distance / 20 km/h plus one hour (the French variation).

The rules follow the RUSA descriptions at https://rusa.org/octime_alg.html and https://rusa.org/octime_acp.html.