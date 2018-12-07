#ifndef _SOLENOID_H_
#define _SOLENOID_H_

#include "stm32f1xx_hal.h"
#include "stm32f1xx_hal_gpio.h"

void set_solenoid_position(GPIO_PinState en_solenoid);

#endif
