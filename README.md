# 333_EMProject
Houses code for the Energy Monitoring Project owned by Princeton University and advised by Behavioral Science Consultancy Evidn.

The web app link is energymonitor.princeton.edu

See the old web app here: https://energy-monitoring-project.herokuapp.com/

## Application Summary
A real time, constantly updating, energy monitoring dashboard. At least for the fume hood widget, we need to update every second.

### Tech Stack
- HTML, CSS, JS
- Flask
- Python
- PHP
- PostgreSQL
- cPanel

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

### DBMS
Lab Information
- Metrics are updated every 5 seconds

Fume Hood Information
- Active State 
- Time in Use 
- Power Consumption
- Energy Consumption

Once the day is past, compress the data into averages (or other informative forms) and store them separately.

