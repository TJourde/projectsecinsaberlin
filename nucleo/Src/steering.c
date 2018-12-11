#include "steering.h"
#include "stdlib.h"

#define MAX_SPEED_STEERING 60 //Left steering
#define MIN_SPEED_STEERING 40 //Right steering
#define NO_SPEED_STEERING 50

#define gauche_volant 0x9F0 // valeur initiale = 2395  
#define droite_volant 0x6E0 // valeur initiale = 1825  
#define centre_volant (gauche_volant + droite_volant)/2 // valeur initiale = 2110

#define MAX_CMD_STEERING 60 // Left steering command
#define MIN_CMD_STEERING 40 // Right steering command
#define MEDIUM_CMD_STEERING (MAX_CMD_STEERING + MIN_CMD_STEERING)/2

extern uint32_t ADCBUF[5];

void steering_set_speed(GPIO_PinState en_steering, int speed){
	
		/* Threshold */
		/* The speed */
		if (speed < MIN_SPEED_STEERING){
			speed = MIN_SPEED_STEERING;
		} else if (speed > MAX_SPEED_STEERING){
			speed  = MAX_SPEED_STEERING;
		}
		
		speed = 3200 * ( speed/ 100.0 );
		
		TIM1->CCR3 = speed;
		
		/*        Enable moteurs        */
		/* GPIO_PIN_SET : activation    */
		/* GPIO_PIN_RESET : pont ouvert */
		
		HAL_GPIO_WritePin( GPIOC, GPIO_PIN_12, en_steering);  //PC12  AV
}

int get_steering_angle(void){
	return ADCBUF[1];
}

void position_cmd (GPIO_PinState en_steering, int msg_CAN){
	
	int cpt_pos = get_steering_angle();
	int cpt_centre, msg_corr, angle_diff;
	
	cpt_centre = cpt_pos - centre_volant;
	msg_corr = 5*(msg_CAN - MEDIUM_CMD_STEERING);
	
	// Limit the steering
	if (cpt_centre > 0xFF){cpt_centre = 0xFF;}
	else if (cpt_centre < -0xFF){cpt_centre = -0xFF;}
	
	angle_diff = msg_corr - cpt_centre;
	
	// Discrete command turning/steady
	if (abs(angle_diff)<30){steering_set_speed(GPIO_PIN_RESET, 50);}
	else if (angle_diff > 0){steering_set_speed(en_steering, 57);}
	else {steering_set_speed(en_steering, 43);}	
}
