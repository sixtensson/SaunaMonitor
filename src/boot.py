# boot.py -- run on boot-up
import pycom

pycom.lte_modem_en_on_boot(False) # Disable LTE on boot
