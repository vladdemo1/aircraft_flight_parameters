"""This file created for working with navigation data"""

# For example
# 0GPGGA,060355.00,4950.4828,N,03638.5901,E,1,05,4.3,144.5,M,16.2,M,,*67
# Where next elements

# 0GPGGA     - command about write current message
# 060355.00  - 06 hours 03 minutes 55.00 seconds
# 4950.4828  - latitude: 49 degrees 50.4828 minutes
# N          - Nord
# 03638.5901 - longitude: 036 degrees 38.5901 minutes
# E          - East
# 1    - trash
# 05   - trash
# 4.3  - trash
# 144.5      - height
# M          - meters
# 16.2 - trash
# *67        - control summ message in 0x16 by module 16

from message import MESSAGE


for element in MESSAGE:
    print(element)
