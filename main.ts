let Left_wheel_speed = 0
let Right_wheel_speed = 0
let B_was_pressed_times = 0
let B_was_pressed = 0
let A_was_pressed_times = 0
let A_was_pressed = 0
let start_time_2 = 0
let Distance = 0
let Ultrasonic_time = 0
let start_time = 0
let Left_IR = 0
let Right_IR = 0
let Temperature = 0
PCA9685.init(PCA9685.chipAddress("0x40"), 50)
pins.digitalWritePin(DigitalPin.P14, 1)
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
    if (input.logoIsPressed()) {
        while (true) {
            Right_IR = pins.analogReadPin(AnalogPin.P1)
            Left_IR = pins.analogReadPin(AnalogPin.P2)
            if (input.runningTime() - start_time >= 100) {
                pins.digitalWritePin(DigitalPin.P12, 0)
                pins.digitalWritePin(DigitalPin.P12, 1)
                control.waitMicros(10)
                pins.digitalWritePin(DigitalPin.P12, 0)
                Ultrasonic_time = pins.pulseIn(DigitalPin.P13, PulseValue.High)
                Distance = Ultrasonic_time / 1000000 * (100 * (330.45 + 0.61 * Temperature)) / 2
                start_time = input.runningTime()
            }
            if (input.runningTime() - start_time_2 < 1000) {
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
            } else if (input.runningTime() - start_time_2 >= 1000) {
                Right_wheel_speed = A_was_pressed_times / 12 * 60
                A_was_pressed_times = 0
                Left_wheel_speed = B_was_pressed_times / 12 * 60
                B_was_pressed_times = 0
                start_time_2 = input.runningTime()
                serial.writeLine("Right wheel speed=" + ("" + Right_wheel_speed) + "|Left wheel speed=" + ("" + Left_wheel_speed))
                serial.writeLine("Distance=" + ("" + Distance))
                serial.writeLine("Right_IR_A=" + ("" + Right_IR) + "|Left_IR_A=" + ("" + Left_IR))
            }
            if (Right_IR >= 500 && Left_IR >= 500 && Distance > 10) {
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin0,
                0,
                1024,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin1,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin2,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin3,
                0,
                1024,
                PCA9685.chipAddress("0x40")
                )
            } else if (Right_IR < 500 && Left_IR < 500 && Distance > 10) {
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin0,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin1,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin2,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin3,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
            } else if (Right_IR >= 500 && Left_IR < 500 && Distance > 10) {
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin0,
                0,
                1024,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin1,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin2,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin3,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
            } else if (Right_IR < 500 && Left_IR >= 500 && Distance > 10) {
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin0,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin1,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin2,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin3,
                0,
                1024,
                PCA9685.chipAddress("0x40")
                )
            } else if (Distance <= 10) {
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin0,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin1,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin2,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
                PCA9685.setPinPulseRange(
                PCA9685.PinNum.Pin3,
                0,
                0,
                PCA9685.chipAddress("0x40")
                )
            } else {
            	
            }
        }
    } else if (input.soundLevel() >= 40) {
        basic.showIcon(IconNames.EigthNote)
        basic.pause(500)
    } else {
    	
    }
})
