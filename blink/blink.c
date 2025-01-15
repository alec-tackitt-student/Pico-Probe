/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "pico/stdlib.h"
#include "hardware/i2c.h"

// Pico W devices use a GPIO on the WIFI chip for the LED,
// so when building for Pico W, CYW43_WL_GPIO_LED_PIN will be defined
#ifdef CYW43_WL_GPIO_LED_PIN
#include "pico/cyw43_arch.h"
#endif

#ifndef LED_DELAY_MS
#define LED_DELAY_MS 250
#endif

// I2C address for BMP280 (default is 0x76)
#define BMP280_ADDR 0x76

// Register addresses for BMP280
#define BMP280_TEMP_REG 0xFA
// I2C setup
i2c_inst_t *i2c = i2c0; // use i2c0 or i2c1

//https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf

void bmp280_init() {
    // Initialize BMP280 and set it to read temperature
    uint8_t data[2] = {0xF4, 0x27}; // 0x27 to read temperature
    i2c_write_blocking(i2c, BMP280_ADDR, data, 2, false);
}
float read_temperature() {
    uint8_t temp_data[3];
    i2c_read_blocking(i2c, BMP280_ADDR, temp_data, 3, false);

    int32_t raw_temp = (temp_data[0] << 12) | (temp_data[1] << 4) | (temp_data[2] >> 4);

    // Temperature conversion (apply calibration if needed)
    float temperature = raw_temp / 16384.0; // Simplified, should apply proper calibration formula
    return temperature;
}
// Perform initialisation
int pico_led_init(void) {
#if defined(PICO_DEFAULT_LED_PIN)
    // A device like Pico that uses a GPIO for the LED will define PICO_DEFAULT_LED_PIN
    // so we can use normal GPIO functionality to turn the led on and off
    gpio_init(PICO_DEFAULT_LED_PIN);
    gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
    return PICO_OK;
#elif defined(CYW43_WL_GPIO_LED_PIN)
    // For Pico W devices we need to initialise the driver etc
    return cyw43_arch_init();
#endif
}

// Turn the led on or off
void pico_set_led(bool led_on) {
#if defined(PICO_DEFAULT_LED_PIN)
    // Just set the GPIO on or off
    gpio_put(PICO_DEFAULT_LED_PIN, led_on);
#elif defined(CYW43_WL_GPIO_LED_PIN)
    // Ask the wifi "driver" to set the GPIO on or off
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, led_on);
#endif
}

int main() {
    stdio_init_all();
    
    // Initialize I2C (assuming SDA on GPIO 4, SCL on GPIO 5, adjust if needed)
    i2c_init(i2c, 100 * 1000);  // 100kHz clock speed
    gpio_set_function(4, GPIO_FUNC_I2C);  // SDA pin
    gpio_set_function(5, GPIO_FUNC_I2C);  // SCL pin
    gpio_pull_up(4);  // Enable pull-up resistors
    gpio_pull_up(5);

    bmp280_init();  // Initialize BMP280 sensor

    int rc = pico_led_init();
    hard_assert(rc == PICO_OK);
    while (true) {
        pico_set_led(true);
        sleep_ms(LED_DELAY_MS);
        pico_set_led(false);
        sleep_ms(LED_DELAY_MS);
         float temperature = read_temperature();  // Get the temperature from BMP280
        printf("Temperature: %.2f°C\n", temperature);  // Output to the console
        sleep_ms(1000);  // Wait for 1 second before reading again
    }
     return 0;
}
