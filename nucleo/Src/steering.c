#include "steering.h"
#include "stdlib.h"

#define MAX_SPEED_STEERING 60 //Left or right steering ?
#define MIN_SPEED_STEERING 40 //Left or right steering ?
#define NO_SPEED_STEERING 50

#define LEFT_STEERING 0x09A0 // Left steering
#define RIGHT_STEERING 0x0700 // Right steering
#define NO_STEERING 0x087A // Front wheels are in the middle - car not turning

#define MAX_CMD_STEERING 0xFF // Left steering
#define MIN_CMD_STEERING 0x80 // Right steering
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
	/*
	int cmd_rot;
	*/
	
	cpt_centre = cpt_pos - NO_STEERING;
	msg_corr = 4*(msg_CAN - MEDIUM_CMD_STEERING);
	
	// Limit the steering
	if (cpt_centre > 0xFF){cpt_centre = 0xFF;}
	else if (cpt_centre < -0xFF){cpt_centre = -0xFF;}
	
	angle_diff = msg_corr - cpt_centre;
	
	// Discrete command 0/1
	if (abs(angle_diff)<50){steering_set_speed(GPIO_PIN_RESET, 50);}
	else if (angle_diff < 0){steering_set_speed(en_steering, 60);}
	else {steering_set_speed(en_steering, 40);}	
	
	/*
	// Progressive command
	cmd_rot = 50 + angle_diff / 2^5;
	steering_set_speed(en_steering, cmd_rot);
	*/
}

/*
void steering_set_position (GPIO_PinState en_steering, int angle_obj){

	int steering_speed, angle, angle_diff;
	int angle_current = get_steering_angle() - NO_STEERING;
	float alpha;
	
	// Wheel in abutment - signal stopped
	if (angle_current <= RIGHT_STEERING | angle_current >= LEFT_STEERING){
		en_steering = GPIO_PIN_RESET;
		steering_speed = 50;
		steering_set_speed(en_steering,steering_speed);}
	
	// Wheel rotating normally
	else {
		angle = angle_obj - MEDIUM_CMD_STEERING;
		alpha = (float)(MAX_STEERING-MIN_STEERING)/(float)(MAX_CMD_STEERING-MIN_CMD_STEERING);
		angle_diff = angle_current - (angle*alpha);
				
		// Wheels close to the desired position
		if (abs(angle_diff) < 100){
			en_steering = GPIO_PIN_RESET;
			steering_speed = 50;
			steering_set_speed(en_steering,steering_speed);
			}
		// Wheels away from the desired position
		else{
			en_steering = GPIO_PIN_SET;
			steering_speed = 50 + angle_diff * 50/(MAX_STEERING-MIN_STEERING + MAX_CMD_STEERING-MIN_CMD_STEERING);
			steering_set_speed(en_steering,steering_speed);
		}
	}
}
*/
