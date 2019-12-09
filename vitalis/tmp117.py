"""
Super biblioteca pro tmp117 com a raspberry.

developed by italogsfernandes.github.io
"""
import smbus

Temp_Result_Register = 0x00  # 8000h Temperature result register
Configuration_Register = 0x01  # 0220h Configuration register
THigh_Limit_Register = 0x02  # 6000h Temperature high limit register
TLow_Limit_Register = 0x03  # 8000h Temperature low limit register
EEPROM_UL_Register = 0x04  # 0000h EEPROM unlock register
EEPROM1_Register = 0x05  # EEPROM1 register
EEPROM2_Register = 0x06  # EEPROM2 register
Temp_Offset_Register = 0x07  # 0000h Temperature offset register
EEPROM3_Register = 0x08  # EEPROM3 register
Device_ID_Register = 0x0F  # 0117h Device ID register

I2C_ADDRESS = 0x48  # I2C address of the TMP117 device


def _twos_complement(val, bits):
    """compute the 2's complement of int value val"""
    # if sign bit is set e.g., 8bit: 128-255
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


class TMP117(object):
    def __init__(self,
                 i2c=None):
        # Default to the standard I2C bus on Pi.
        self.i2c = i2c if i2c else smbus.SMBus(1)
        # TODO: self.set_mode(MODE_HR)  # Trigger an initial temperature read.

    def get_temperature(self):
        temp_raw_value = self.get_temp_result_register_value()
        temp_value = _twos_complement(temp_raw_value) * 0.0078125
        return temp_value

    def get_temp_result_register_value(self):
        return self.i2c.read_word_data(I2C_ADDRESS, Temp_Result_Register)

    def get_device_id(self):
        return self.i2c.read_word_data(I2C_ADDRESS, Device_ID_Register)

    def get_registers(self):
        return {
            "Temp_Result_Register": self.i2c.read_word_data(
                I2C_ADDRESS,
                Temp_Result_Register,
            ),
            "Configuration_Register": self.i2c.read_word_data(
                I2C_ADDRESS,
                Configuration_Register,
            ),
            "THigh_Limit_Register": self.i2c.read_word_data(
                I2C_ADDRESS,
                THigh_Limit_Register,
            ),
            "TLow_Limit_Register": self.i2c.read_word_data(
                I2C_ADDRESS,
                TLow_Limit_Register,
            ),
            "EEPROM_UL_Register": self.i2c.read_word_data(
                I2C_ADDRESS,
                EEPROM_UL_Register,
            ),
            "EEPROM1_Register": self.i2c.read_word_data(
                I2C_ADDRESS,
                EEPROM1_Register,
            ),
            "EEPROM2_Register": self.i2c.read_word_data(
                I2C_ADDRESS,
                EEPROM2_Register,
            ),
            "Temp_Offset_Register": self.i2c.read_word_data(
                I2C_ADDRESS,
                Temp_Offset_Register,
            ),
            "EEPROM3_Register": self.i2c.read_word_data(
                I2C_ADDRESS,
                EEPROM3_Register,
            ),
            "Device_ID_Register": self.i2c.read_word_data(
                I2C_ADDRESS,
                Device_ID_Register,
            ),
        }


if __name__ == "__main__":
    my_tmp117 = TMP117()
    print(my_tmp117.get_device_id())
    print(my_tmp117.get_temp_result_register_value())
