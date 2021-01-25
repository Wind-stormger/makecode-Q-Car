Left_wheel_speed = 0
Right_wheel_speed = 0
B_was_pressed_times = 0
B_was_pressed = 0
A_was_pressed_times = 0
A_was_pressed = 0
Last_end_time_2 = 0
Distance = 0
Ultrasonic_time = 0
Last_end_time_1 = 0
Left_IR = 0
Right_IR = 0
Temperature = 0
PCA9685.init(PCA9685.chip_address("0x40"), 50)
pins.digital_write_pin(DigitalPin.P14, 1)
basic.show_icon(IconNames.SMALL_DIAMOND)
basic.show_icon(IconNames.SMALL_SQUARE)
basic.show_icon(IconNames.DIAMOND)
basic.show_icon(IconNames.SQUARE)
basic.clear_screen()

def on_forever():
    global Temperature, Right_IR, Left_IR, Ultrasonic_time, Distance, Last_end_time_1, A_was_pressed, A_was_pressed_times, B_was_pressed, B_was_pressed_times, Right_wheel_speed, Left_wheel_speed, Last_end_time_2
    Temperature = input.temperature()
    serial.write_line("sound LV=" + ("" + str(input.sound_level())))
    serial.write_line("temperature=" + ("" + str(input.temperature())))
    basic.show_icon(IconNames.SWORD)
    if input.logo_is_pressed():
        while True:
            Right_IR = pins.analog_read_pin(AnalogPin.P1)
            Left_IR = pins.analog_read_pin(AnalogPin.P2)
            if input.running_time() - Last_end_time_1 >= 100:
                pins.digital_write_pin(DigitalPin.P12, 0)
                pins.digital_write_pin(DigitalPin.P12, 1)
                control.wait_micros(10)
                pins.digital_write_pin(DigitalPin.P12, 0)
                Ultrasonic_time = pins.pulse_in(DigitalPin.P13, PulseValue.HIGH)
                Distance = Ultrasonic_time / 1000000 * (100 * (330.45 + 0.61 * Temperature)) / 2
                Last_end_time_1 = input.running_time()
            if input.running_time() - Last_end_time_2 < 1000:
                if pins.digital_read_pin(DigitalPin.P5) == 1 and A_was_pressed == 0:
                    A_was_pressed = 1
                if pins.digital_read_pin(DigitalPin.P5) == 0 and A_was_pressed == 1:
                    A_was_pressed_times = A_was_pressed_times + 1
                    A_was_pressed = 0
                if pins.digital_read_pin(DigitalPin.P11) == 1 and B_was_pressed == 0:
                    B_was_pressed = 1
                if pins.digital_read_pin(DigitalPin.P11) == 0 and B_was_pressed == 1:
                    B_was_pressed_times = B_was_pressed_times + 1
                    B_was_pressed = 0
            elif input.running_time() - Last_end_time_2 >= 1000:
                Right_wheel_speed = A_was_pressed_times / 12 * 60
                A_was_pressed_times = 0
                Left_wheel_speed = B_was_pressed_times / 12 * 60
                B_was_pressed_times = 0
                Last_end_time_2 = input.running_time()
                serial.write_line("Right wheel speed=" + ("" + str(Right_wheel_speed)) + "|Left wheel speed=" + ("" + str(Left_wheel_speed)))
                serial.write_line("Distance=" + ("" + str(Distance)))
                serial.write_line("Right_IR_A=" + ("" + str(Right_IR)) + "|Left_IR_A=" + ("" + str(Left_IR)))
            if Right_IR >= 500 and Left_IR >= 500 and Distance > 10:
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN0, 0, 1024, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN1, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN2, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN3, 0, 1024, PCA9685.chip_address("0x40"))
            elif Right_IR < 500 and Left_IR < 500 and Distance > 10:
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN0, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN1, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN2, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN3, 0, 0, PCA9685.chip_address("0x40"))
            elif Right_IR >= 500 and Left_IR < 500 and Distance > 10:
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN0, 0, 1024, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN1, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN2, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN3, 0, 0, PCA9685.chip_address("0x40"))
            elif Right_IR < 500 and Left_IR >= 500 and Distance > 10:
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN0, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN1, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN2, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN3, 0, 1024, PCA9685.chip_address("0x40"))
            elif Distance <= 10:
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN0, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN1, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN2, 0, 0, PCA9685.chip_address("0x40"))
                PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN3, 0, 0, PCA9685.chip_address("0x40"))
            else:
                pass
    elif input.sound_level() >= 40:
        basic.show_icon(IconNames.EIGTH_NOTE)
        basic.pause(500)
    else:
        pass
basic.forever(on_forever)
