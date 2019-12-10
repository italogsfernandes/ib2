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


def _invert_msb_and_lsb(val):
    """Invert the MSB with the LSB in a 16bit number"""
    msb = val >> 8  # get the msb
    lsb = val & 0x00FF  # get the lsb
    return (lsb << 8 | msb)  # return a number with lsb a msb inverted


class TMP117(object):
    def __init__(self,
                 i2c=None):
        # Default to the standard I2C bus on Pi.
        self.i2c = i2c if i2c else smbus.SMBus(1)
        # TODO: self.set_mode(MODE_HR)  # Trigger an initial temperature read.

    def get_device_id(self):
        return self.get_register_value(Device_ID_Register)

    def get_register_value(self, register):
        register_value = self.i2c.read_word_data(
            I2C_ADDRESS,
            register,
        )
        return _invert_msb_and_lsb(register_value)

    def get_register_value_as_hex(self, register):
        return hex(self.get_register_value(register))

    def get_register_value_as_bin(self, register):
        return bin(self.get_register_value(register))

    def get_registers(self):
        return {
            "Temp_Result_Register": self.get_register_value(
                Temp_Result_Register,
            ),
            "Configuration_Register": self.get_register_value(
                Configuration_Register,
            ),
            "THigh_Limit_Register": self.get_register_value(
                THigh_Limit_Register,
            ),
            "TLow_Limit_Register": self.get_register_value(
                TLow_Limit_Register,
            ),
            "EEPROM_UL_Register": self.get_register_value(
                EEPROM_UL_Register,
            ),
            "EEPROM1_Register": self.get_register_value(
                EEPROM1_Register,
            ),
            "EEPROM2_Register": self.get_register_value(
                EEPROM2_Register,
            ),
            "Temp_Offset_Register": self.get_register_value(
                Temp_Offset_Register,
            ),
            "EEPROM3_Register": self.get_register_value(
                EEPROM3_Register,
            ),
            "Device_ID_Register": self.get_register_value(
                Device_ID_Register,
            ),
        }

    def get_registers_as_hex(self):
        return {
            "Temp_Result_Register": self.get_register_value_as_hex(
                Temp_Result_Register,
            ),
            "Configuration_Register": self.get_register_value_as_hex(
                Configuration_Register,
            ),
            "THigh_Limit_Register": self.get_register_value_as_hex(
                THigh_Limit_Register,
            ),
            "TLow_Limit_Register": self.get_register_value_as_hex(
                TLow_Limit_Register,
            ),
            "EEPROM_UL_Register": self.get_register_value_as_hex(
                EEPROM_UL_Register,
            ),
            "EEPROM1_Register": self.get_register_value_as_hex(
                EEPROM1_Register,
            ),
            "EEPROM2_Register": self.get_register_value_as_hex(
                EEPROM2_Register,
            ),
            "Temp_Offset_Register": self.get_register_value_as_hex(
                Temp_Offset_Register,
            ),
            "EEPROM3_Register": self.get_register_value_as_hex(
                EEPROM3_Register,
            ),
            "Device_ID_Register": self.get_register_value_as_hex(
                Device_ID_Register,
            ),
        }

    def get_registers_as_bin(self):
        return {
            "Temp_Result_Register": self.get_register_value_as_bin(
                Temp_Result_Register,
            ),
            "Configuration_Register": self.get_register_value_as_bin(
                Configuration_Register,
            ),
            "THigh_Limit_Register": self.get_register_value_as_bin(
                THigh_Limit_Register,
            ),
            "TLow_Limit_Register": self.get_register_value_as_bin(
                TLow_Limit_Register,
            ),
            "EEPROM_UL_Register": self.get_register_value_as_bin(
                EEPROM_UL_Register,
            ),
            "EEPROM1_Register": self.get_register_value_as_bin(
                EEPROM1_Register,
            ),
            "EEPROM2_Register": self.get_register_value_as_bin(
                EEPROM2_Register,
            ),
            "Temp_Offset_Register": self.get_register_value_as_bin(
                Temp_Offset_Register,
            ),
            "EEPROM3_Register": self.get_register_value_as_bin(
                EEPROM3_Register,
            ),
            "Device_ID_Register": self.get_register_value_as_bin(
                Device_ID_Register,
            ),
        }

    def get_temperature(self):
        temp_raw_value = self.get_register_value(Temp_Result_Register)
        temp_value = _twos_complement(temp_raw_value, 16) * 0.0078125
        return temp_value

    def get_configuration_dict(self):
        configuration_register = self.get_register_value(
            Configuration_Register,
        )
        configuration_dict = {
            'HEX': hex(configuration_register),
            'BIN': bin(configuration_register),
            'HIGH_Alert': configuration_register & (1 << 15),
            'LOW_Alert': configuration_register & (1 << 14),
            'Data_Ready': configuration_register & (1 << 13),
            'EEPROM_Busy': configuration_register & (1 << 12),
            'MOD[1:0]': bin((configuration_register >> 10) & (0b11)),
            'CONV[2:0]': bin((configuration_register >> 7) & (0b111)),
            'AVG[1:0]': bin((configuration_register >> 5) & (0b11)),
            'T/nA': configuration_register & (1 << 4),
            'POL': configuration_register & (1 << 3),
            'DR/Alert': configuration_register & (1 << 2),
            'Soft_Reset': configuration_register & (1 << 1),
            '-': configuration_register & (1),
        }
        return configuration_dict

    def get_high_limit(self):
        high_raw_value = self.get_register_value(THigh_Limit_Register)
        high_value = _twos_complement(high_raw_value, 16) * 0.0078125
        return high_value

    def get_low_limit(self):
        low_raw_value = self.get_register_value(TLow_Limit_Register)
        low_value = _twos_complement(low_raw_value, 16) * 0.0078125
        return low_value

    def get_EEPROM_Unlock_dict(self):
        # TODO
        return {}

    def get_EEPROM1(self):
        # TODO
        return 0

    def get_EEPROM2(self):
        # TODO
        return 0

    def get_temperature_offset(self):
        temp_offset_raw_value = self.get_register_value(Temp_Offset_Register)
        temp_offset_value = _twos_complement(
            temp_offset_raw_value, 16
        ) * 0.0078125
        return temp_offset_value

    def get_EEPROM3(self):
        # TODO
        return 0

    def get_device_id_dict(self):
        device_id = self.get_register_value(Device_ID_Register)
        rev = (device_id >> 12) & (0b1111)
        did = (device_id & (0b0000111111111111))
        device_id_dict = {
            'HEX': hex(device_id),
            'BIN': bin(device_id),
            'Rev[3:0]': rev,
            'Rev[3:0]_HEX': hex(rev),
            'DID[11:0]': did,
            'DID[11:0]_HEX': hex(did),
        }
        return device_id_dict

if __name__ == "__main__":
    my_tmp117 = TMP117()
    print(my_tmp117.get_device_id())
    print(my_tmp117.get_temp_result_register_value())
