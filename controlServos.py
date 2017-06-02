import serial
import scriptcontext
myPort = scriptcontext.sticky['serialport']
myPort.reset_input_buffer()
myPort.reset_output_buffer()

out_bytes = [0xAA, 0x00, 0x07, 0x00, None, None, 0xAA, 0x00, 0x07, 0x01, None, None, 0xAA, 0x00, 0x1F, 0x02, 0x00, None, None, None, None]

speed = speed_val * 4
out_bytes[4] = speed & 0x7F #Second byte holds the lower 7 bits of speed.
out_bytes[5] = (speed >> 7) & 0x7F # Third data byte holds the bits 7-13 of speed.
out_bytes[10] = speed & 0x7F #Second byte holds the lower 7 bits of speed.
out_bytes[11] = (speed >> 7) & 0x7F # Third data byte holds the bits 7-13 of speed.

target1 = angle_us1 * 4
target2 = angle_us2 * 4
out_bytes[17] = target1 & 0x7F #Second byte holds the lower 7 bits of target.
out_bytes[18] = (target1 >> 7) & 0x7F # Third data byte holds the bits 7-13 of target.
out_bytes[19] = target2 & 0x7F #Second byte holds the lower 7 bits of target.
out_bytes[20] = (target2 >> 7) & 0x7F # Third data byte holds the bits 7-13 of target.

print out_bytes
myPort.write(bytes(bytearray(out_bytes)))