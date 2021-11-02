# 333_EMProject
Houses code for the Energy Monitoring Project owned by Princeton University and advised by Behavioral Science Consultancy Evidn.

## Application Summary
A real time, constantly updating, energy monitoring dashboard. At least for the fume hood widget, we need to update every second.

### Tech Stack
- HTML, CSS, JS
- Flask
- Python
- PostgreSQL (TimescaleDB)
- Heroku

### Client-Side (HTML, CSS, JS, jQuery)
- Formats Widgets (Interface in general)
- Update Widgets at a local level using Ajax
- Detect and act on Navigation Events

Files
- index.html (multiple lab dashboard)
- lab.html (individual lab summary page)
- fumehood.html (individual fume hood summary page)

Individual html files per widget
Each html file will be included into the main layouts
Include jQuery into the script of each html file

### Server-Side (Flask, Python)
Files
- restFetch.py (fetches information from REST API, formats and stores into our database)
- monitor.py (detects and handles page change requests from client)
- database.py (fetches info from our database and formats it for display)
- runserver.py (runs the web application)
- emp.py (provides paths to different files for flask)

### DBMS (TimescaleDB)
Lab Information
- Energy Consumption updates every 30 seconds
- Power Consumption updates every 30 seconds
- Occupancy data updates every 15 minutes

Fume Hood Information
- Active State updates every second
- Time in Use updates every second via Active State
- Power Consumption updates every second
- Energy Consumption updates every second

Once the day is past, compress the data into averages (or other informative forms) and store them separately, if that is possible given the database schematic. If not innately supported, we can add our own structures.

