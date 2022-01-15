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
#include <string.h>
#include <stdio.h>

#include <xdc/std.h>

//#define xdc_runtime_Log_DISABLE_ALL 1  // Add to disable logs from this file
#include <xdc/runtime/Log.h>

#include <Board.h>

// Sensor Controller API
#include "scif.h"

#include "application.h"


/*********************************************************************
 * GLOBAL VARIABLES
 */


/*********************************************************************
 * LOCAL FUNCTION DECLARATIONS
 */
// HWI context
static void SC_ctrlReadyHwiCb(void);
static void SC_taskAlertHwiCb(void);

// SWI context
static void SC_rangerClockSwiFxn(UArg a0);

// Task context
static void SC_processAdc(void);
static void SC_processRanger(void);


/*********************************************************************
 * HWI CALLBACKS
 */

/*
 * @brief   Callback from Scif driver on Control READY interrupt.
 *
 *          Signals main task with EVENT_SC_CTRL_READY event.
 *
 * @param   None.
 *
 * @return  None.
 */
static void SC_ctrlReadyHwiCb(void)
{

} // SC_ctrlReadyHwiCb


/*
 * @brief   Callback from Scif driver on Task ALERT interrupt.
 *
 *          Signals main task with EVENT_SC_TASK_ALERT event.
 *
 * @param   None.
 *
 * @return  None.
 */
static void SC_taskAlertHwiCb(void)
{

} // SC_taskAlertHwiCb


/*********************************************************************
 * SWI CALLBACKS
 */

/*
 * @brief   Callback from Clock module on timeout.
 *
 *          Stores current clock tick, and signals main task with
 *          EVENT_SC_EXEC_RANGER event.
 *
 * @param   None.
 *
 * @return  None.
 */
static void SC_rangerClockSwiFxn(UArg a0)
{

} // SC_rangerClockSwiFxn


/*********************************************************************
 * LOCAL FUNCTIONS
 */

/*
 * @brief   Processing function for the ADC SC task.
 *
 *          Is called whenever the EVENT_SC_TASK_ALERT event is active
 *          and ADC SC task has generated an alert.
 *
 *          Retrieves ADC value from SC, and calculates and sets new period and
 *          timeout for Clock object.
 *
 * @param   None.
 *
 * @return  None.
 */
static void SC_processAdc(void)
{
    // Toggle LED0 (Red) on LP
    Main_toggleLed(Board_LED0);

} // SC_processAdc


/*
 * @brief   Processing function for the Ranger SC task.
 *
 *          Is called whenever the EVENT_SC_TASK_ALERT event is active
 *          and Ranger SC task has generated an alert.
 *
 *          Retrieves both high and low tdc values from SC, extends into 32-bit,
 *          converts into cm, and prints out the value on Log.
 *
 * @param   None.
 *
 * @return  None.
 */
static void SC_processRanger(void)
{
    // Toggle LED1 (Green) on LP
    Main_toggleLed(Board_LED1);

} // SC_processRanger


/*********************************************************************
 * EXTERN FUNCTIONS
 */

/*
 * @brief   Called before main loop.
 *
 *          Initializes Scif driver, registers callbacks, configures RTC, and
 *          starts SC tasks.
 *
 * @param   None.
 *
 * @return  None.
 */
void SC_init(void)
{
    Log_info0("scTask initialization done");
} // SC_init


/*
 * @brief   Processing function for the EVENT_SC_CTRL_READY event.
 *
 *          Is called from main loop whenever the EVENT_SC_CTRL_READY event is
 *          active.
 *
 *          Currently does nothing.
 *
 * @param   None.
 *
 * @return  None.
 */
void SC_processCtrlReady(void)
{

} // SC_processCtrlReady


/*
 * @brief   Processing function for the EVENT_SC_TASK_ALERT event.
 *
 *          Is called from main loop whenever the EVENT_SC_TASK_ALERT event is
 *          active.
 *
 *          Checks which SC tasks are active, and calls their corresponding
 *          processing function. Also clears and ACKs the interrupts to the
 *          Scif driver.
 *
 * @param   None.
 *
 * @return  None.
 */
void SC_processTaskAlert(void)
{

} // SC_processTaskAlert


/*
 * @brief   Processing function for the EVENT_SC_TASK_ALERT event.
 *
 *          Is called from main loop whenever the EVENT_SC_TASK_ALERT event is
 *          active.
 *
 *          Executes the Ranger SC task once.
 *
 * @param   None.
 *
 * @return  None.
 */
void SC_execRanger(void)
{

} // SC_execRanger
