import smbus


class TouchButtons:
    def __init__(self, bus, addr):

        self.bus = smbus.SMBus(bus)
        self.addr = addr
        self.available = True
    
    def is_available(self):
        return self.available

    def wake(self):
        self.available = True

    def use(self):
        self.available = False

    def is_pressed(self, button_number):
        pins = self.calc_pins(self.get_val())
        return button_number in pins

    def get_val(self):
        val = self.bus.read_byte(self.addr)
        return val

    def get_pin(self, val):
        if val == 128:
            return 1
        elif val == 64:
            return 2
        elif val == 32:
            return 3
        elif val == 16:
            return 4
        else:
            return None

    def calc_pins(self, val):
        pins = list()
        divider = 128
        value = val
        while divider >= 16:
            rest = value % divider
            print(str(value) + " % " + str(divider) + " = " + str(rest))
            if rest != value:
                pins.append(self.get_pin(divider))
                divider /= 2
                value = rest
            elif rest == value:
                divider /= 2
                value = rest
            elif rest == 0 and divider == value:
                pins.append(self.get_pin(divider))
                break
            elif value == 0 and rest == 0:
                break
        return pins