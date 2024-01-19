# AHI_blocks_selector
Select blocks for AHI (HIMAWARI-8/9) files in HSD format

## Usage
```shell
#!/usr/bin/bash
ahi_sat_id='H08'
year=2020
month=10; day=31
hour=18; minute=00
band_name="BAND13"
latitude=12; latitude_span=5
python ahi_blocks.py -id $ahi_sat_id -t "$year$month$day$hour$minute" -b "$band_name" -lat $latitude -latspan $latitude_span
```
