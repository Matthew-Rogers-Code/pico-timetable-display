# pico-timetable-display

A MicroPython-powered timetable display built on a Raspberry Pi Pico. Designed for schools operating on a two-week A/B timetable rotation, the device shows the current week type on an I2C LCD display alongside the time, date, and ambient temperature. A physical switch handles daylight saving time adjustments without any code changes required.

Built as a collaboration — hardware and enclosure by my dad, software by me.

---

## Features

- Displays current week type (A or B) based on a user-maintained schedule file
- Shows real-time clock data: date, time, and day of the week
- Displays ambient temperature via the DS3231's onboard sensor
- Physical daylight saving time switch — flick it twice a year, no code changes needed
- Automatic LCD backlight — turns off outside of 07:00–16:00 to save power and reduce distraction
- Falls back to `?` gracefully if the current week isn't found in the schedule

---

## Hardware

| Component | Details |
|---|---|
| Microcontroller | Raspberry Pi Pico |
| Display | I2C LCD (16x2, address `0x27`) |
| Real-time clock | DS3231 RTC module |
| DST input | Physical switch on GPIO 28 |
| Enclosure | Custom 3D printed case |

---

## Wiring

| Component | Pico Pin |
|---|---|
| LCD SDA | GPIO 0 |
| LCD SCL | GPIO 1 |
| RTC SDA | GPIO 2 |
| RTC SCL | GPIO 3 |
| DST Switch | GPIO 28 |

---

## Dependencies

The following MicroPython libraries are required. Copy them to the Pico's filesystem:

- [`urtc`](https://github.com/adafruit/Adafruit_CircuitPython_DS3231) — DS3231 RTC driver
- `lcd_api` — Generic I2C LCD API
- `pico_i2c_lcd` — Pico-specific I2C LCD driver

---

## Setup

1. Copy `main.py` and all dependencies to your Pico using [Thonny](https://thonny.org/) or `rshell`
2. Create a `data.txt` file on the Pico with your school's timetable schedule (see format below)
3. On first run, the device will sync the RTC to the system time — make sure your PC clock is correct before flashing
4. Wire up the hardware according to the wiring table above
5. Power on — the display will show the current week type, time, date, and temperature

---

## Schedule File Format

Create a file called `data.txt` on the Pico with one entry per week in the following format:

```
2025-09-01: A
2025-09-08: B
2025-09-15: A
2025-09-22: B
```

Each entry represents the Monday of that school week and its corresponding week type. This file will need to be updated manually at the start of each term.

If a week is not found in the file, the display will show `?` as the week type.

---

## Daylight Saving Time

A physical switch on GPIO 28 controls DST. When the switch is in the ON position, one hour is added to the displayed time. Flip it when the clocks change — no reprogramming needed.

---

## Photos

*Coming soon*

---

## Notes

- The DS3231 is battery-backed, so the time is preserved even when the Pico is unplugged
- The schedule file must be updated each term with the new week rotation dates
- The backlight automatically turns off before 07:00 and after 16:00

---

## License

MIT License — free to use, modify, and build on.
