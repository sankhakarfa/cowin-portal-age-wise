# 💉 Cowin Portal Vaccine Slot Availability
Get Cowin Portal slot availability using age

### Requirement:

python3


### Pip Requirement:

~~~
pip install prettytable
~~~

### Usage

~~~
get_available_slots.py [-h] [--state STATE] [--district DISTRICT]
                              [--pincode PINCODE] [--daily] [--min_18_centers]
                              [--date DATE] [--min_age MIN_AGE]

Options to run this Cowin Vaccine Slot availability

optional arguments:
  -h, --help           show this help message and exit
  --state STATE        State
  --district DISTRICT  District
  --pincode PINCODE    Area pincode
  --daily              Get input dates data
  --min_18_centers     Check if center allows 18+
  --date DATE          Date in dd-mm-yyyy
  --min_age MIN_AGE    Min Age Limit Default is 18
