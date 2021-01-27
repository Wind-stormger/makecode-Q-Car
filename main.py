def Motor_control(Right_motor_Positive: number, Right_motor_Negative: number, Left_motor_Positive: number, Left_motor_Negative: number):
    PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN0,
        0,
        Right_motor_Positive,
        PCA9685.chip_address("0x40"))
    PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN1,
        0,
        Right_motor_Negative,
        PCA9685.chip_address("0x40"))
    PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN3,
        0,
        Left_motor_Positive,
        PCA9685.chip_address("0x40"))
    PCA9685.set_pin_pulse_range(PCA9685.PinNum.PIN2,
        0,
        Left_motor_Negative,
        PCA9685.chip_address("0x40"))
def Velocity_measurement():
    global A_was_pressed, A_was_pressed_times, B_was_pressed, B_was_pressed_times, Right_wheel_speed, Left_wheel_speed, Last_end_time_2
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
def Ultrasonic_ranging():
    global Ultrasonic_time, Distance, Last_end_time_1
    if input.running_time() - Last_end_time_1 >= 100:
        pins.digital_write_pin(DigitalPin.P12, 0)
        pins.digital_write_pin(DigitalPin.P12, 1)
        control.wait_micros(10)
        pins.digital_write_pin(DigitalPin.P12, 0)
        Ultrasonic_time = pins.pulse_in(DigitalPin.P13, PulseValue.HIGH)
        Distance = Ultrasonic_time / 1000000 * (100 * (330.45 + 0.61 * Temperature)) / 2
        Last_end_time_1 = input.running_time()
# Searching for the dark line
def IR_calibration():
    global Right_IR_minimum, Left_IR_minimum
    Line_partol_IR()
    if Right_IR <= 700 and Right_IR >= 100 and Right_IR < Right_IR_minimum - 200:
        Right_IR_minimum = Right_IR + 200
    elif Left_IR <= 700 and Left_IR >= 100 and Left_IR < Left_IR_minimum - 200:
        Left_IR_minimum = Left_IR + 200
    elif Right_IR < 100:
        Right_IR_minimum = 300
    elif Left_IR < 100:
        Left_IR_minimum = 300
    serial.write_line("Right_IR_minimum=" + ("" + str(Right_IR_minimum)) + "|Left_IR_minimum=" + ("" + str(Left_IR_minimum)))
    serial.write_line("Right_IR_A=" + ("" + str(Right_IR)) + "|Left_IR_A=" + ("" + str(Left_IR)))
    basic.pause(100)
def Serial_write():
    global Last_end_time_3
    if input.running_time() - Last_end_time_3 >= 1000:
        serial.write_line("Right wheel speed=" + ("" + str(Right_wheel_speed)) + "|Left wheel speed=" + ("" + str(Left_wheel_speed)))
        serial.write_line("Distance=" + ("" + str(Distance)) + ("|Temperature=" + ("" + str(Temperature))))
        serial.write_line("Right_IR_A=" + ("" + str(Right_IR)) + "|Left_IR_A=" + ("" + str(Left_IR)))
        Last_end_time_3 = input.running_time()
def Line_partol_IR():
    global Right_IR, Left_IR
    Right_IR = pins.analog_read_pin(AnalogPin.P1)
    Left_IR = pins.analog_read_pin(AnalogPin.P2)
def Line_patrol_control():
    if Right_IR >= Right_IR_minimum and Left_IR >= Left_IR_minimum and Distance > 10:
        Motor_control(1024, 0, 1024, 0)
    elif Right_IR < Right_IR_minimum and Left_IR < Left_IR_minimum and Distance > 10:
        Motor_control(0, 0, 0, 0)
    elif Right_IR >= Right_IR_minimum and Left_IR < Left_IR_minimum and Distance > 10:
        Motor_control(1024, 0, 0, 0)
    elif Right_IR < Right_IR_minimum and Left_IR >= Left_IR_minimum and Distance > 10:
        Motor_control(0, 0, 1024, 0)
    elif Distance <= 10:
        Motor_control(0, 0, 0, 0)
IR_corrected = 0
Last_end_time_3 = 0
Left_IR = 0
Right_IR = 0
Distance = 0
Ultrasonic_time = 0
Last_end_time_1 = 0
Left_wheel_speed = 0
Right_wheel_speed = 0
B_was_pressed_times = 0
B_was_pressed = 0
A_was_pressed_times = 0
A_was_pressed = 0
Last_end_time_2 = 0
Temperature = 0
Left_IR_minimum = 0
Right_IR_minimum = 0
PCA9685.init(PCA9685.chip_address("0x40"), 50)
pins.digital_write_pin(DigitalPin.P14, 0)
Right_IR_minimum = 900
Left_IR_minimum = 900
Temperature = input.temperature()
basic.show_icon(IconNames.SMALL_DIAMOND)
basic.show_icon(IconNames.SMALL_SQUARE)
basic.show_icon(IconNames.DIAMOND)
basic.show_icon(IconNames.SQUARE)
basic.clear_screen()

def on_forever():
    global IR_corrected
    if IR_corrected == 0:
        basic.show_arrow(ArrowNames.EAST)
    elif IR_corrected == 1:
        basic.show_arrow(ArrowNames.WEST)
    if input.button_is_pressed(Button.B) and not (input.button_is_pressed(Button.A)):
        pins.digital_write_pin(DigitalPin.P14, 1)
        basic.show_icon(IconNames.ASLEEP)
        for index in range(20):
            IR_calibration()
        basic.show_icon(IconNames.HAPPY)
        pins.digital_write_pin(DigitalPin.P14, 0)
        IR_corrected = 1
    if input.button_is_pressed(Button.A) and not (input.button_is_pressed(Button.B)):
        basic.show_icon(IconNames.SWORD)
        while True:
            pins.digital_write_pin(DigitalPin.P14, 1)
            Line_partol_IR()
            Ultrasonic_ranging()
            Line_patrol_control()
            Velocity_measurement()
            Serial_write()
basic.forever(on_forever)
