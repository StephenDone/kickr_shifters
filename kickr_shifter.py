#!/usr/bin/python

import smbus
import time

bus = smbus.SMBus(1)

DEVICE_ADDRESS = 0x34

REG_CFG = 0x01
REG_INT_STAT = 0x02
REG_KEY_LCK_EC = 0x03
REG_KEY_EVENT_A = 0x04
REG_GPIO_INT_STAT = 0x11
REG_GPIO_DAT_STAT = 0x14
REG_GPIO_DAT_OUT = 0x17
REG_GPIO_INT_EN = 0x1A
REG_KP_GPIO = 0x1D
REG_GPI_EM = 0x20
REG_GPIO_DIR = 0x23
REG_GPIO_INT_LVL = 0x26
REG_DEBOUNCE_DIS = 0x29
REG_GPIO_PULL = 0x2C

def ToHex(data):
    return '[{}]'.format(', '.join(f"0x{x:02x}" for x in data))

def ToBin(data):
    return '[{}]'.format(', '.join(f"0x{x:08b}" for x in data))

def HexByte(data):
    return f"0x{data:02x}"

def GetGpioData():
    return bus.read_i2c_block_data(DEVICE_ADDRESS, REG_GPIO_DAT_STAT, 3)
    # Read GPIO State

def GetKey():
    result = bus.read_byte_data(DEVICE_ADDRESS, REG_KEY_EVENT_A)
    return result

def GetIntStat():
    result = bus.read_byte_data(DEVICE_ADDRESS, REG_INT_STAT)
    print(f'IntStat = {HexByte(result)}')
    return result

def GetInterrupt():
    result = GetIntStat() & 0x01 == 0x01
    print(f'GetInterrupt = {HexByte(result)}')
    return result

def GetKeyLockEc():
    result = bus.read_byte_data(DEVICE_ADDRESS, REG_KEY_LCK_EC)
    print(f'Key Lock & Ev Cnt = {HexByte(result)}')
    return result

def GetCfg():
    result = bus.read_byte_data(DEVICE_ADDRESS, REG_CFG)
    print(f'GetCfg = {HexByte(result)}')
    return result

def PrintReg(count, reg, name):
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, reg, count)
    print(f'0x{reg:02X} {name:18} {ToHex(data)} {ToBin(data)}')

def PrintRegisters():
    PrintReg(3, REG_GPIO_INT_STAT,'REG_GPIO_INT_STAT')
    PrintReg(3, REG_GPIO_DAT_STAT,'REG_GPIO_DAT_STAT')
    PrintReg(3, REG_KP_GPIO,'REG_KP_GPIO')
    PrintReg(3, REG_GPI_EM,'REG_GPI_EM')
    PrintReg(3, REG_GPIO_DIR,'REG_GPIO_DIR')
    PrintReg(3, REG_GPIO_INT_LVL,'REG_GPIO_INT_LVL')
    PrintReg(3, REG_DEBOUNCE_DIS,'REG_DEBOUNCE_DIS')
    PrintReg(3, REG_GPIO_PULL,'REG_GPIO_PULL')
    print()

def ConfigureRegisters():
    # Auto-increment enabled, Overflow mode enabled.
    bus.write_byte_data(DEVICE_ADDRESS, REG_CFG, 0xA0)

    # All pins in GPIO mode
    bus.write_i2c_block_data(DEVICE_ADDRESS, REG_KP_GPIO, [0x00, 0x00, 0x00])

    # R7 R6 R5 R4 R3 R2 part of event FIFO
    bus.write_i2c_block_data(DEVICE_ADDRESS, REG_GPI_EM, [0xFC, 0x00, 0x00])

    # All GPIO as inputs
    bus.write_i2c_block_data(DEVICE_ADDRESS, REG_GPIO_DIR, [0x00, 0x00, 0x00])

    # High to low transitions trigger interrupt.
    bus.write_i2c_block_data(DEVICE_ADDRESS, REG_GPIO_INT_LVL, [0x00, 0x00, 0x00])

    # Debounce enabled
    bus.write_i2c_block_data(DEVICE_ADDRESS, REG_DEBOUNCE_DIS, [0x00, 0x00, 0x00])

    # R7 R6 R5 R4 R3 R2 C8 C9 Pull-Up Disabled
    bus.write_i2c_block_data(DEVICE_ADDRESS, REG_GPIO_PULL, [0xFC, 0x00, 0x03])

def PrintGpioData(data):
    print(f'GPIO Data = {ToHex(data)}')
    print(f'               RRRRRRRR    CCCCCCCC    ------CC')
    print(f'               76543210,   76543210,   ------98')
    print(f'GPIO Data = {ToBin(data)}')

def GetKeyId( Right, Index ):
    return int(Right) * 6 + (Index - 2)

def KeyIdToName(Index):
    match Index:
        case 0:
            return 'Left Brake'
        case 1:
            return 'Left Forward'
        case 2:
            return 'Left Back'
        case 3:
            return 'Left Gear Inner'
        case 4:
            return 'Left Gear Outer'
        case 5:
            return 'Left Inner'
        case 6:
            return 'Right Brake'
        case 7:
            return 'Right Back'
        case 8:
            return 'Right Forward'
        case 9:
            return 'Right Gear Inner'
        case 10:
            return 'Right Gear Outer'
        case 11:
            return 'Right Inner'

# Loop iteration each time there is an exception that we handle
while(True):
    try:
        ConfigureRegisters()
        PrintRegisters()

        while(GetKey()!=0): 
            pass

        GpioData = GetGpioData()
        PrintGpioData(GpioData)

        RightShifter = GpioData[2] & 0x02 == 0x02
        print('This is a right shifter' if RightShifter else 'This is a left shifter')

        MainShifter = GpioData[2] & 0x01 == 0x01
        print('This is a main shifter' if MainShifter else '*** This is an UNKNOWN shifter!!! ***')

        # Loop iteration each time we poll the TCA8418 for Key Events
        while(True):

            # Loop iteration for each Key Event in the FIFO
            while True:
                KeyEvent=GetKey()
                if KeyEvent==0:
                    break

                KeyDown = KeyEvent & 0x80 == 0x80
                KeyCode = KeyEvent & 0x7F
                Row = KeyCode < 105
                Index = KeyCode - 97 if Row else KeyCode - 105

                # Since we've setup the fifo for row R2-R7 only, we cannot get column key codes
                assert Row and Index >= 2 and Index <= 7

                KeyId = GetKeyId(RightShifter, Index)

                print(f"R[{Index}] {'Down' if KeyDown else 'Up  '} {KeyIdToName(KeyId)}")

            time.sleep(0.5)

    except OSError as E:
        print(f'E:    {E}')
        if(E.args[0] != 5 and E.args[0] != 121): raise
        time.sleep(1)
    


