# 💉 Cowin Portal Vaccine Slot Availability
Get Cowin Portal slot availability using the following options
- (State & District) or Pincode
- Minimum Age Limit
- If centers are allowing 18+
- Daily [Default is 7 days]
- Output as HTML

### Requirement:

- python3


### Pip Requirement:

~~~
pip install prettytable
~~~

### Usage

~~~
get_available_slots.py [-h] [--state STATE] [--district DISTRICT]
                              [--pincode PINCODE] [--daily] [--all-centers]
                              [--date DATE] [--min-age MIN_AGE]
                              [--output-html OUTPUT_HTML]

Options to run this Co-WIN Vaccine Slot availability

optional arguments:
  -h, --help            show this help message and exit
  --state STATE         State
  --district DISTRICT   District
  --pincode PINCODE     Area pincode
  --daily               Get input dates data
  --all-centers         Show all centers irrespective of availability
  --date DATE           Date in dd-mm-yyyy
  --min-age MIN_AGE     Min Age Limit [Default is 18]
  --output-html OUTPUT_HTML
                        Output html to OUTPUT_HTML file
~~~

### TODO
- Website
- Table formatting