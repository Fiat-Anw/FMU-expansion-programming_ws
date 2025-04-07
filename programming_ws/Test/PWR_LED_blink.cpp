#include <JetsonGPIO.h>
#include <iostream>
#include <thread>
#include <chrono>

#define LED_PIN 7  // Change this to the GPIO number you're using

int main() {
    // Set up the GPIO pin
    GPIO::setmode(GPIO::BOARD);  // Use physical pin numbering
    GPIO::setup(LED_PIN, GPIO::OUT, GPIO::HIGH);  // Set pin as output, initial state HIGH

    try {
        while (true) {
            GPIO::output(LED_PIN, GPIO::HIGH);  // Turn LED on
            std::this_thread::sleep_for(std::chrono::seconds(1));  // Wait 1 second
            GPIO::output(LED_PIN, GPIO::LOW);   // Turn LED off
            std::this_thread::sleep_for(std::chrono::seconds(1));  // Wait 1 second
        }
    } catch (const std::exception& e) {
        std::cerr << "Exception: " << e.what() << std::endl;
    }

    // Clean up GPIO settings
    GPIO::cleanup();
    return 0;
}
