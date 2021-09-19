import spidev 

REGADR_ABS_POS = 0x01
REGADR_EL_POS = 0x02
REGADR_MARK = 0x03
REGADR_SPEED = 0x04
REGADR_ACC = 0x05
REGADR_DEC = 0x06
REGADR_MAX_SPEED = 0x07
REGADR_MIN_SPEED = 0x08
REGADR_FS_SPD = 0x15
REGADR_KVAL_HOLD = 0x09
REGADR_KVAL_RUN = 0x0A
REGADR_KVAL_ACC = 0x0B
REGADR_KVAL_DEC = 0x0C
REGADR_INT_SPEED = 0x0D
REGADR_ST_SLP = 0x0E
REGADR_FN_SLP_ACC = 0x0F
REGADR_FN_SLP_DEC = 0x10
REGADR_K_THERM = 0x11
REGADR_ADC_OUT = 0x12
REGADR_OCD_TH = 0x13
REGADR_STALL_TH = 0x14
REGADR_STEP_MODE = 0x16
REGADR_ALARM_EN = 0x17
REGADR_CONFIG = 0x18
REGADR_STATUS = 0x19

class L6470:
   def __init__(self, spiNum, spiCS):
      self.spi = spidev.SpiDev()
      self.spi.open(spiNum, spiCS)
      self.spi.max_speed_hz = 500000
		
   def Move(self, n_step):
      if n_step >= 0:
         cmd = 0b01000000
      else:
         cmd = 0b01000001
         n_step = -n_step
      n_step0 = n_step & 0x000000FF
      n_step1 = (n_step >> 8) & 0x000000FF
      n_step2 = (n_step >> 16) & 0x000000FF  
      self.spi.writebytes([cmd])
      self.spi.writebytes([n_step2])
      self.spi.writebytes([n_step1])
      self.spi.writebytes([n_step0])

   def HardHiZ(self):
      self.spi.writebytes([0b10100000])

   def HardStop(self):
      self.spi.writebytes([0b10111000])

   def Run(self, speed):
      if speed >= 0:
         cmd = 0b01010000
      else:
         cmd = 0b01010001
         speed = -speed
      speed0 = speed & 0x000000FF
      speed1 = (speed >> 8) & 0x000000FF
      speed2 = (speed >> 16) & 0x000000FF  
      self.spi.writebytes([cmd])
      self.spi.writebytes([speed2])
      self.spi.writebytes([speed1])
      self.spi.writebytes([speed0])

   def SetParam(self, param, value):
      cmd = param & 0b00011111
      self.spi.writebytes([cmd])
      self.spi.writebytes([value]) 
