import machine
from machine import Pin,SoftSPI
import utime
import sys
###############################################################################
# Constants

# Registers
REG_DEVID = 0x0F
REG_POWER_CTL = 0x20
REG_DATAX0 = 0x28

# Other constants
DEVID = 0x44
SENSITIVITY_2G = 1.0 / 256  # (g/LSB)
EARTH_GRAVITY = 9.80665     # Earth's gravity in [m/s^2]

###############################################################################
# Settings
# Assign chip select (CS) pin (and start it high)
cs = Pin(("GPIO_0", 28), Pin.OUT)
# Initialize SPI
spi = SPI("SPI_1")
spi.init(baudrate=500000, polarity=1, phase=1, bits=8, firstbit=SPI.MSB)
###############################################################################
# Functions

def reg_write(spi, cs, reg, data):
    """
    Write 1 byte to the specified register.
    """
    
    # Construct message (set ~W bit low, MB bit low)
    msg = bytearray()
    msg.append(0x00 | reg)
    msg.append(data)
    
    # Send out SPI message
    cs.value(0)
    spi.write(msg)
    cs.value(1)
    
def reg_read(spi, cs, reg, nbytes=1):
    """
    Read byte(s) from specified register. If nbytes > 1, read from consecutive
    registers.
    """
    
    # Determine if multiple byte (MB) bit should be set
    if nbytes < 1:
        return bytearray()
    elif nbytes == 1:
        mb = 0
    else:
        mb = 1
    
    # Construct message (set ~W bit high)
    msg = bytearray()
    msg.append(0x80 | (mb << 6) | reg)
    
    # Send out SPI message and read
    cs.value(0)
    spi.write(msg)
    data = spi.read(nbytes)
    cs.value(1)
    
    return data

###############################################################################
# Main

# Start CS pin high
cs.value(1)

# Workaround: perform throw-away read to make SCK idle high
reg_read(spi, cs, REG_DEVID)

# Read device ID to make sure that we can communicate with the ADXL343
data = reg_read(spi, cs, REG_DEVID)
if (data != bytearray((DEVID,))):
    print("ERROR: Could not communicate with Accel click")
    sys.exit()
    
# Read Power Control register
data = reg_read(spi, cs, REG_POWER_CTL)
print(data)

# Tell ADXL343 to start taking measurements by setting Measure bit to high
data = int.from_bytes(data, "big") | (1 << 3)
reg_write(spi, cs, REG_POWER_CTL, data)

# Test: read Power Control register back to make sure Measure bit was set
data = reg_read(spi, cs, REG_POWER_CTL)
print(data)

# Wait before taking measurements
utime.sleep(2.0)

cs = Pin(("GPIO_0", 8),Pin.OUT)
# Initialize SPI
spi = SPI("SPI_0")
spi.init(baudrate=200000, polarity=1, phase=1, bits=8, firstbit=SPI.MSB)

while True:
    
    # Read X, Y, and Z values from registers (16 bits each)
    data = reg_read(spi, cs, REG_DATAX0, 6)

    # Convert 2 bytes (little-endian) into 16-bit integer (signed)
    acc_x = ustruct.unpack_from("<h", data, 0)[0]
    acc_y = ustruct.unpack_from("<h", data, 2)[0]
    acc_z = ustruct.unpack_from("<h", data, 4)[0]

    # Convert measurements to [m/s^2]
    acc_x = acc_x * SENSITIVITY_2G * EARTH_GRAVITY
    acc_y = acc_y * SENSITIVITY_2G * EARTH_GRAVITY
    acc_z = acc_z * SENSITIVITY_2G * EARTH_GRAVITY

    # Print results
    print("X:", "{:.2f}".format(acc_x), \
          "| Y:", "{:.2f}".format(acc_y), \
          "| Z:", "{:.2f}".format(acc_z))
    
    utime.sleep(0.1)