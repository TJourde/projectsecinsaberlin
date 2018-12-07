#include "solenoid.h"
#include "stdlib.h"

void set_solenoid_position (GPIO_PinState en_solenoid){
		
	/*        Enable moteurs        */
	/* GPIO_PIN_SET : activation    */
	/* GPIO_PIN_RESET : pont ouvert */
	
	HAL_GPIO_WritePin(GPIOA, GPIO_PIN_6, en_solenoid); //PA6 Solenoid	
}
