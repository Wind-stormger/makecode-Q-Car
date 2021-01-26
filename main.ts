function Motor_control (Right_motor_Positive: number, Right_motor_Negative: number, Left_motor_Positive: number, Left_motor_Negative: number) {
    PCA9685.setPinPulseRange(
    PCA9685.PinNum.Pin0,
    0,
    Right_motor_Positive,
    PCA9685.chipAddress("0x40")
    )
    PCA9685.setPinPulseRange(
    PCA9685.PinNum.Pin1,
    0,
    Right_motor_Negative,
    PCA9685.chipAddress("0x40")
    )
    PCA9685.setPinPulseRange(
    PCA9685.PinNum.Pin3,
    0,
    Left_motor_Positive,
    PCA9685.chipAddress("0x40")
    )
    PCA9685.setPinPulseRange(
    PCA9685.PinNum.Pin2,
    0,
    Left_motor_Negative,
    PCA9685.chipAddress("0x40")
    )
}
function Velocity_measurement () {
    if (input.runningTime() - Last_end_time_2 < 1000) {
        if (pins.digitalReadPin(DigitalPin.P5) == 1 && A_was_pressed == 0) {
            A_was_pressed = 1
        }
        if (pins.digitalReadPin(DigitalPin.P5) == 0 && A_was_pressed == 1) {
            A_was_pressed_times = A_was_pressed_times + 1
            A_was_pressed = 0
        }
        if (pins.digitalReadPin(DigitalPin.P11) == 1 && B_was_pressed == 0) {
            B_was_pressed = 1
        }
        if (pins.digitalReadPin(DigitalPin.P11) == 0 && B_was_pressed == 1) {
            B_was_pressed_times = B_was_pressed_times + 1
            B_was_pressed = 0
        }
    } else if (input.runningTime() - Last_end_time_2 >= 1000) {
        Right_wheel_speed = A_was_pressed_times / 12 * 60
        A_was_pressed_times = 0
        Left_wheel_speed = B_was_pressed_times / 12 * 60
        B_was_pressed_times = 0
        Last_end_time_2 = input.runningTime()
    }
}
function Ultrasonic_ranging () {
    if (input.runningTime() - Last_end_time_1 >= 100) {
        pins.digitalWritePin(DigitalPin.P12, 0)
        pins.digitalWritePin(DigitalPin.P12, 1)
        control.waitMicros(10)
        pins.digitalWritePin(DigitalPin.P12, 0)
        Ultrasonic_time = pins.pulseIn(DigitalPin.P13, PulseValue.High)
        Distance = Ultrasonic_time / 1000000 * (100 * (330.45 + 0.61 * Temperature)) / 2
        Last_end_time_1 = input.runningTime()
    }
}
function Serial_write () {
    if (input.runningTime() - Last_end_time_3 >= 1000) {
        serial.writeLine("Right wheel speed=" + ("" + Right_wheel_speed) + "|Left wheel speed=" + ("" + Left_wheel_speed))
        serial.writeLine("Distance=" + ("" + Distance))
        serial.writeLine("Right_IR_A=" + ("" + Right_IR) + "|Left_IR_A=" + ("" + Left_IR))
        Last_end_time_3 = input.runningTime()
    }
}
function Line_partol_IR () {
    Right_IR = pins.analogReadPin(AnalogPin.P1)
    Left_IR = pins.analogReadPin(AnalogPin.P2)
}
function Line_patrol_control () {
    if (Right_IR >= 500 && Left_IR >= 500 && Distance > 10) {
        Motor_control(1024, 0, 1024, 0)
    } else if (Right_IR < 500 && Left_IR < 500 && Distance > 10) {
        Motor_control(0, 0, 0, 0)
    } else if (Right_IR >= 500 && Left_IR < 500 && Distance > 10) {
        Motor_control(1024, 0, 0, 0)
    } else if (Right_IR < 500 && Left_IR >= 500 && Distance > 10) {
        Motor_control(0, 0, 1024, 0)
    } else if (Distance <= 10) {
        Motor_control(0, 0, 0, 0)
    } else {
    	
    }
}
let Left_IR = 0
let Right_IR = 0
let Last_end_time_3 = 0
let Temperature = 0
let Distance = 0
let Ultrasonic_time = 0
let Last_end_time_1 = 0
let Left_wheel_speed = 0
let Right_wheel_speed = 0
let B_was_pressed_times = 0
let B_was_pressed = 0
let A_was_pressed_times = 0
let A_was_pressed = 0
let Last_end_time_2 = 0
PCA9685.init(PCA9685.chipAddress("0x40"), 50)
pins.digitalWritePin(DigitalPin.P14, 0)
basic.showIcon(IconNames.SmallDiamond)
basic.showIcon(IconNames.SmallSquare)
basic.showIcon(IconNames.Diamond)
basic.showIcon(IconNames.Square)
basic.clearScreen()
basic.forever(function () {
    Temperature = input.temperature()
    serial.writeLine("sound LV=" + ("" + input.soundLevel()))
    serial.writeLine("temperature=" + ("" + input.temperature()))
    basic.showIcon(IconNames.Sword)
    if (input.buttonIsPressed(Button.A)) {
        while (true) {
            pins.digitalWritePin(DigitalPin.P14, 1)
            Line_partol_IR()
            Ultrasonic_ranging()
            Line_patrol_control()
            Velocity_measurement()
            Serial_write()
        }
    }
    if (input.soundLevel() >= 40) {
        basic.showIcon(IconNames.EigthNote)
        basic.pause(500)
    }
})
