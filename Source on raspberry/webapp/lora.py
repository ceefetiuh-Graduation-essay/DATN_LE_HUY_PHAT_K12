import serial

ser = serial.Serial(
        port = '/dev/ttyAMA0',
        baudrate = 9600,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 2
    )

class Lora():
    def __init__(self,ser):
        self.ser = ser

    def lorasend(self, text):
        self.text = text
        try:
            self.ser.write(self.text)
            self.ser.flush()

        except KeyboardInterrupt:
            self.ser.close()

    def lorareceive(self):
        try:
            s = self.ser.readline()
            data = s.decode()           # decode s
            data = data.rstrip()        # cut "\r\n" at last of string
            return data

        except KeyboardInterrupt:
            ser.close()