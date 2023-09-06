from lewis.adapters.stream import StreamInterface, Cmd
from lewis.core.logging import has_log
from lewis.utils.byte_conversions import int_to_raw_bytes, BYTE
from lewis.utils.replies import conditional_reply


def log_replies(f):
    def _wrapper(self, *args, **kwargs):
        result = f(self, *args, **kwargs)
        self.log.info(f"Reply in {f.__name__}: {result}")
        return result
    return _wrapper


def bytes_to_int(bytes):
    return int.from_bytes(bytes, byteorder="big", signed=True)


def crc16(data):
    """
    CRC algorithm - translated from section 3-5 of eurotherm manual.
    :param data: the data to checksum
    :return: the checksum
    """
    crc = 0xFFFF

    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1

            crc %= BYTE ** 2

    return int_to_raw_bytes(crc, 2, low_byte_first=True)


@has_log
class Pre4500StreamInterface(StreamInterface):
    """
    This implements the modbus stream interface for a eurotherm.

    Note: Eurotherm uses modbus RTU, not TCP, so cannot use lewis' normal modbus implementation here.
    """
    commands = {
        Cmd("any_command", r"^([\s\S]*)$", return_mapping=lambda x: x),
    }

    def __init__(self):
        super().__init__()

    in_terminator = ""
    out_terminator = ""
    readtimeout = 10

    def handle_error(self, request, error):
        error_message = "An error occurred at request " + repr(request) + ": " + repr(error)
        print(error_message)
        self.log.error(error_message)
        return str(error)

    @log_replies
    @conditional_reply("connected")
    def any_command(self, command):
        self.log.info(command)
        comms_address = command[0]
        function_code = int(command[1])
        data = command[2:-2]
        crc = command[-2:]

        assert(crc16(command) == b"\x00\x00", "Invalid checksum from IOC")

        if len(data) != 4:
            raise ValueError(f"Invalid message length {len(data)}")
        
        if  not 0 < comms_address < 5:
            raise Exception(f"invalid comms_address {comms_address}")

        if function_code == 3:
            return self.handle_read(comms_address, data)
        else:
            raise ValueError(f"Unknown modbus function code: {function_code}")

    def handle_read(self, comms_address, data):
        mem_address = bytes_to_int(data[0:2])
        words_to_read = bytes_to_int(data[2:4])
        self.log.info(f"Attempting to read {words_to_read} words from mem address: {mem_address}")
        if mem_address == 1001:
            if comms_address == 1:
                reply_data = self.device.spare_temperature
            elif comms_address == 2:
                reply_data = self.device.chopper_body
            elif comms_address == 3:
                reply_data = self.device.cooling_water
            elif comms_address == 4:
                reply_data = self.device.chopper_pit
            else: 
                raise Exception(f"invalid address {mem_address}")

        else: 
            raise Exception("TODO")
        

        self.log.info(f"reply_data = {reply_data}")
        assert -0x8000 <= reply_data <= 0x7FFF, f"reply {reply_data} was outside modbus range, bug?"

        reply = comms_address.to_bytes(1, byteorder="big", signed=True) \
            + b"\x03\x02" \
            + reply_data.to_bytes(2, byteorder="big", signed=True)

        return reply + crc16(reply)

  
