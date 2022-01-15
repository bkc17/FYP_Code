//*****************************************************************************
//  SENSOR CONTROLLER STUDIO EXAMPLE: ADC DATA LOGGER FOR LAUNCHPAD
//  Operating system: TI-RTOS
//
//  The Sensor Controller is used to sample and buffer a single ADC channel.
//  The ADC samples are stored in a ring-buffer, and the Sensor Controller
//  maintains a head index indicating where the next sample will be written.
//  The sampling interval is specified in the call to scifStartRtcTicksNow().
//
//  The application wakes up at a fixed interval that is asynchronous to the
//  Sensor Controller wake-ups, and transfers over UART (57600 baud, 8-N-1):
//  - The ADC samples
//  - Statistics: Number of samples, average, minimum and maximum
//
//  Use a terminal window to connect to the LaunchPad's USB Serial Port.
//
//
//  Copyright (C) 2014 Texas Instruments Incorporated - http://www.ti.com/
//
//
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions
//  are met:
//
//    Redistributions of source code must retain the above copyright
//    notice, this list of conditions and the following disclaimer.
//
//    Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
//
//    Neither the name of Texas Instruments Incorporated nor the names of
//    its contributors may be used to endorse or promote products derived
//    from this software without specific prior written permission.
//
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
//  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
//  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
//  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
//  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
//  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
//  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
//  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
//  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
//  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
//  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//****************************************************************************/

/*********************************************************************
 * INCLUDES
 */
#include <xdc/std.h>
#include <xdc/runtime/Error.h>

#include <ti/sysbios/BIOS.h>

#include <ti/drivers/PIN.h>
#include <ti/drivers/UART.h>

#include <uart_logs.h>

#include <Board.h>

#include "application.h"


/*********************************************************************
 * FUNCTIONS
 */

/*
 * @brief   Main function. Initializes tasks and start BIOS.
 *
 * @param   None.
 *
 * @return  None.
 */
int main(void)
{
    // Initialize PIN
	PIN_init(BoardGpioInitTable);

    // Initialize the RTOS Log formatting and output to UART in Idle thread.
    // Note: Define xdc_runtime_Log_DISABLE_ALL to remove all impact of Log.
    // Note: NULL as Params gives 115200,8,N,1 and Blocking mode
    UART_init();
    UartLog_init(UART_open(Board_UART, NULL));

    // Initialize and create Main task
    Main_createTask();

    // Start TI-RTOS
    BIOS_start();

    return 0;
} // main
