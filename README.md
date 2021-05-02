# 💉 Cowin Portal Vaccine Slot Availability
Get Cowin Portal slot availability using the following options
- (State & District) or Pincode
- Minimum Age Limit
- All Centers even if no slot is available  ```[--all-centers]```
- Daily [Default is 7 days]
- Output as HTML

### Requirement:

- Python3


### Pip Requirement:

``` bash
pip3 install prettytable
```

### Usage

```

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

for argument values with space use quotes example --state="west bengal"
```

### Examples

``` bash
#State: West Bengal , District:Purulia
./get_available_slots.py --min-age=45 --state="West Bengal" --district="Purulia" --all-centers

#State: West Bengal , District:Purulia Output in html
./get_available_slots.py --min-age=45 --state="West Bengal" --district="Purulia" --all-centers --output-html=test_table.html

#State: West Bengal , District:Purulia from Date 15-05-2021
./get_available_slots.py --min-age=45 --state="West Bengal" --district="Purulia" --all-centers --date="15-05-2021"

#State: West Bengal , Pincode:110001 from Date 15-05-2021
./get_available_slots.py --min-age=45 --pincode="110001" --all-centers --date="15-05-2021"

```

### TODO
- Website
- Table formatting