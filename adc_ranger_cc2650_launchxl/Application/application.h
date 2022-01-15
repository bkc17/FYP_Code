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

#ifndef APPLICATION_H
#define APPLICATION_H

/*********************************************************************
 * INCLUDES
 */
#include <xdc/std.h>

#include <ti/sysbios/knl/Clock.h>
#include <ti/sysbios/knl/Event.h>

/*********************************************************************
 * MACROS
 */
// Bitvector macro
#define BV(n)               (1 << (n))

// Clock tick conversion
#define TICK_TO_MS(tick)    ((tick) * Clock_tickPeriod / 1000)
#define MS_TO_TICK(ms)      ((ms) * 1000 / Clock_tickPeriod)


/*********************************************************************
 * CONSTANTS
 */
// Event defines
#define EVENT_NONE             Event_Id_NONE
#define EVENT_ALL              ~Event_Id_NONE
#define EVENT_SC_CTRL_READY    Event_Id_00
#define EVENT_SC_TASK_ALERT    Event_Id_01
#define EVENT_SC_EXEC_RANGER   Event_Id_02


/*********************************************************************
 * FUNCTIONS
 */
// Main Task
void Main_createTask(void);

void Main_signalEvents(uint32_t events);
Bool Main_eventsActive(uint32_t events);
void Main_toggleLed(uint8_t led);

// SC Task
void SC_init(void);
void SC_processCtrlReady(void);
void SC_processTaskAlert(void);
void SC_execRanger(void);

#endif /* APPLICATION_H */
