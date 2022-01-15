/*
 * Copyright (c) 2016, Texas Instruments Incorporated
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * *  Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * *  Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * *  Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/*********************************************************************
 * INCLUDES
 */
#include <xdc/std.h>

#include <ti/sysbios/BIOS.h>
#include <ti/sysbios/knl/Event.h>
#include <ti/sysbios/knl/Task.h>

#include <ti/drivers/PIN.h>

#include <Board.h>

#include "application.h"


/*********************************************************************
 * LOCAL VARIABLES
 */
// Main Task data
Task_Struct mainTask;
char mainTaskStack[1024];

// Event state
Event_Struct mainEventState;
Event_Handle hMainEventState;

// Initial LED pin configuration table
//   - LEDs Board_LED0 & Board_LED1 are off.
static PIN_Config ledPinTable[] = {
  Board_LED0 | PIN_GPIO_OUTPUT_EN | PIN_GPIO_LOW | PIN_PUSHPULL | PIN_DRVSTR_MAX,
  Board_LED1 | PIN_GPIO_OUTPUT_EN | PIN_GPIO_LOW | PIN_PUSHPULL | PIN_DRVSTR_MAX,
  PIN_TERMINATE
};

// PIN driver LED state and handle
PIN_State  ledPinState;
PIN_Handle ledPinHandle;


/*********************************************************************
 * LOCAL FUNCTIONS DECLARATIONS
 */
static void Main_init(void);
static void Main_processEvents(uint32_t events);
static void Main_taskFxn(UArg a0, UArg a1);


/*********************************************************************
 * LOCAL FUNCTIONS
 */

/*
 * @brief   Called before main loop. Opens LED pin table.
 *
 * @param   None.
 *
 * @return  None.
 */
static void Main_init(void)
{
    // Open LED pins
    ledPinHandle = PIN_open(&ledPinState, ledPinTable);
    if (!ledPinHandle) {
        Task_exit();
    }
} // Main_init


/*
 * @brief   Find which events are active and dispatch corresponding
 *          processing function.
 *
 * @param   bvEvents  Bitvector of active events.
 *
 * @return  None.
 */
static void Main_processEvents(uint32_t bvEvents)
{
    if (bvEvents == 0) {
        return;
    }

    // Check which events are active and dispatch corresponding function
    uint32_t mask = 1;
    while (bvEvents) {
        switch (bvEvents & mask) {
        case EVENT_SC_CTRL_READY:  SC_processCtrlReady(); break;
        case EVENT_SC_TASK_ALERT:  SC_processTaskAlert(); break;
        case EVENT_SC_EXEC_RANGER: SC_execRanger();       break;
        }
        bvEvents &= ~mask;
        mask <<= 1;
    }
} // Main_processEvents


/*
 * @brief   Application task entry point.
 *
 *          Invoked by TI-RTOS when BIOS_start is called. Calls init function
 *          and enters an infinite loop waiting for events.
 *
 *          When an events occurs, it dispatches a corresponding processing
 *          function, set in Main_processEvents().
 *
 * @param   a0, a1  Not used.
 *
 * @return  None.
 */
static void Main_taskFxn(UArg a0, UArg a1)
{
	// Call init functions
    Main_init();
    SC_init();

    // Main loop
    while (1) {
        // Pend for events
        uint32_t events = Event_pend(hMainEventState, EVENT_NONE, EVENT_ALL, BIOS_WAIT_FOREVER);

        // Process posted events
        Main_processEvents(events);
    }
} // Main_taskFxn


/*********************************************************************
 * EXTERN LOCAL FUNCTIONS
 */

/*
 * @brief   Task creation function for the user task.
 *
 *          Constructs and sets the handles for TI-RTOS objects used.
 *
 * @param   None.
 *
 * @return  None.
 */
void Main_createTask(void)
{
    Task_Params mainTaskParams;

    // Create the OS task
    Task_Params_init(&mainTaskParams);
    mainTaskParams.stack = mainTaskStack;
    mainTaskParams.stackSize = sizeof(mainTaskStack);
    mainTaskParams.priority = 3;
    Task_construct(&mainTask, Main_taskFxn, &mainTaskParams, NULL);

    // Initialize Event handler
    Event_Params eventParams;
    Event_Params_init(&eventParams);
    Event_construct(&mainEventState, &eventParams);
    hMainEventState = Event_handle(&mainEventState);
} // Main_createTask


/*
 * @brief   Posts events to the event struct.
 *
 * @param   bvEvents  Bit vector of events to signal.
 *
 * @return  None.
 */
void Main_signalEvents(uint32_t bvEvents)
{
    // Post event
    Event_post(hMainEventState, bvEvents);
} // Main_signalEvents


/*
 * @brief   Tests if given events are active.
 *
 * @param   bvEvents  Bit vector of events to test if active.
 *
 * @return  Bool if all events in bvEvents are active.
 */
Bool Main_eventsActive(uint32_t bvEvents)
{
    uint32_t postedEvents = Event_getPostedEvents(hMainEventState);
    return (postedEvents & bvEvents) == bvEvents;
} // Main_eventsActive


/*
 * @brief   Convenience function to toggle LEDs on the launchpad.
 *
 * @param   led  LED on the LaunchPad to toggle.
 *
 * @return  None.
 */
void Main_toggleLed(uint8_t led)
{
    if (led != Board_LED0 && led != Board_LED1) return;
    PIN_setOutputValue(ledPinHandle, led, !PIN_getOutputValue(led));
} // Main_toggleLed
