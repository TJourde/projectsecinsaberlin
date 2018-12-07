#ifndef _STERRING_H_
#define _STERRING_H_

#include "stm32f1xx_hal.h"
#include "stm32f1xx_hal_gpio.h"


/**
* Set the speed of the steering motor. Speed value has to be between 0 and 100
**/
void steering_set_speed(GPIO_PinState en_steering, int speed);

/**
* Return the steering angle.
**/
int get_steering_angle(void);

/**
* Command the front wheel position (test program 1)
**/
void position_cmd (GPIO_PinState en_steering, int msg_CAN);

/**
* Command the front wheel position (test program 2)
**/
void steering_set_position(GPIO_PinState en_steering, int speed);
#endif
