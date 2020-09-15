# python_sim800
Python_sim800 is a Python library for managing sim800 modules 

## Requirements
```bash
pip install pyserial
```
## Usage
```python
#initializing
import sim800
sim = sim800.sim(port='/dev/ttyTHS1', baudrate=9600, timeout=5)
if sim.isOpen() :
  print( sim.signal_quality() )

# Sending SMS
phone = '+ZZxxxxxxxxxx'
text = 'Test'
r = sim.send_sms(phone, text)
if r :
  print(r[0]) #prints "+CMGS: 180"

# Making call
sim.call(phone, 20) # wait for 20 seconds
