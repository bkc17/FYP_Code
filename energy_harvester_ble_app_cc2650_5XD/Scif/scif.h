/** \mainpage Driver Overview
  *
  * \section section_drv_info Driver Information
  * This Sensor Controller Interface driver has been generated by the Texas Instruments Sensor Controller
  * Studio tool:
  * - <b>Project name</b>:     energyHarvester
  * - <b>Project file</b>:     C:/Users/bhara/workspace_v8/energy_harvester_ble_app_cc2650_5XD/Scif/SCS code.scp
  * - <b>Code prefix</b>:      -
  * - <b>Operating system</b>: TI-RTOS
  * - <b>Tool version</b>:     2.6.0.132
  * - <b>Tool patches</b>:     None
  * - <b>Target chip</b>:      CC2650, package QFN32 5x5 RHB, revision -
  * - <b>Created</b>:          2022-02-09 10:17:16.210
  * - <b>Computer</b>:         BHARAT-DELL-LAP
  * - <b>User</b>:             bhara
  *
  * No user-provided resource definitions were used to generate this driver.
  *
  * No user-provided procedure definitions were used to generate this driver.
  *
  * Do not edit the generated source code files other than temporarily for debug purposes. Any
  * modifications will be overwritten by the Sensor Controller Studio when generating new output.
  *
  * \section section_drv_modules Driver Modules
  * The driver is divided into three modules:
  * - \ref module_scif_generic_interface, providing the API for:
  *     - Initializing and uninitializing the driver
  *     - Task control (for starting, stopping and executing Sensor Controller tasks)
  *     - Task data exchange (for producing input data to and consume output data from Sensor Controller
  *       tasks)
  * - \ref module_scif_driver_setup, containing:
  *     - The AUX RAM image (Sensor Controller code and data)
  *     - I/O mapping information
  *     - Task data structure information
  *     - Driver setup data, to be used in the driver initialization
  *     - Project-specific functionality
  * - \ref module_scif_osal, for flexible OS support:
  *     - Interfaces with the selected operating system
  *
  * It is possible to use output from multiple Sensor Controller Studio projects in one application. Only
  * one driver setup may be active at a time, but it is possible to switch between these setups. When
  * using this option, there is one instance of the \ref module_scif_generic_interface and
  * \ref module_scif_osal modules, and multiple instances of the \ref module_scif_driver_setup module.
  * This requires that:
  * - The outputs must be generated using the same version of Sensor Controller Studio
  * - The outputs must use the same operating system
  * - The outputs must use different source code prefixes (inserted into all globals of the
  *   \ref module_scif_driver_setup)
  *
  *
  * \section section_project_info Project Description
  * Comparator and timer operation for calculating turbine frequency
  *
  *
  * \subsection section_io_mapping I/O Mapping
  * Task I/O functions are mapped to the following pins:
  * - compHandle:
  *     - <b>A: comp1</b>: DIO9
  *     - <b>A: comp2</b>: DIO10
  *     - <b>A: Temperature Vout</b>: DIO8
  *     - <b>O: temperature VDD</b>: DIO7
  *
  *
  * \section section_task_info Task Description(s)
  * This driver supports the following task(s):
  *
  *
  * \subsection section_task_desc_comp_handle compHandle
  * No description entered
  *
  */




/** \addtogroup module_scif_driver_setup Driver Setup
  *
  * \section section_driver_setup_overview Overview
  *
  * This driver setup instance has been generated for:
  * - <b>Project name</b>:     energyHarvester
  * - <b>Code prefix</b>:      -
  *
  * The driver setup module contains the generated output from the Sensor Controller Studio project:
  * - Location of task control and scheduling data structures in AUX RAM
  * - The AUX RAM image, and the size the image
  * - Task data structure information (location, size and buffer count)
  * - I/O pin mapping translation table
  * - Task resource initialization and uninitialization functions
  * - Hooks for run-time logging
  *
  * @{
  */
#ifndef SCIF_H
#define SCIF_H

#include <stdint.h>
#include <stdbool.h>
#include "scif_framework.h"
#include "scif_osal_tirtos.h"


/// Target chip name
#define SCIF_TARGET_CHIP_NAME_CC2650
/// Target chip package
#define SCIF_TARGET_CHIP_PACKAGE_QFN32_5X5_RHB

/// Number of tasks implemented by this driver
#define SCIF_TASK_COUNT 1

/// compHandle: Task ID
#define SCIF_COMP_HANDLE_TASK_ID 0


/// compHandle: 
#define SCIF_COMP_HANDLE_ARRAY_SIZE 3
/// compHandle I/O mapping: comp1
#define SCIF_COMP_HANDLE_DIO_A_COMP1 9
/// compHandle I/O mapping: comp2
#define SCIF_COMP_HANDLE_DIO_A_COMP2 10
/// compHandle I/O mapping: Temperature Vout
#define SCIF_COMP_HANDLE_DIO_A_TEMP_VOUT 8
/// compHandle I/O mapping: temperature VDD
#define SCIF_COMP_HANDLE_DIO_O_TEMP_VDD 7


// All shared data structures in AUX RAM need to be packed
#pragma pack(push, 2)


/// compHandle: Task output data structure
typedef struct {
    int16_t  ADCout;              ///< 
    uint16_t TimeOutHigh;         ///< High bits for timer output
    uint16_t TimeOutHighArray[3]; ///< 
    uint16_t TimeOutLow;          ///< Pulse width for 10 pulses
    uint16_t TimeOutLowArray[3];  ///< 
} SCIF_COMP_HANDLE_OUTPUT_T;


/// compHandle: Task state structure
typedef struct {
    uint16_t compOut; ///< Output of cont.time comparator
} SCIF_COMP_HANDLE_STATE_T;


/// Sensor Controller task data (configuration, input buffer(s), output buffer(s) and internal state)
typedef struct {
    struct {
        SCIF_COMP_HANDLE_OUTPUT_T output;
        SCIF_COMP_HANDLE_STATE_T state;
    } compHandle;
} SCIF_TASK_DATA_T;

/// Sensor Controller task generic control (located in AUX RAM)
#define scifTaskData    (*((volatile SCIF_TASK_DATA_T*) 0x400E00EA))


// Initialized internal driver data, to be used in the call to \ref scifInit()
extern const SCIF_DATA_T scifDriverSetup;


// Restore previous struct packing setting
#pragma pack(pop)


// AUX I/O re-initialization functions
void scifReinitTaskIo(uint32_t bvTaskIds);


// RTC-based tick generation control
void scifStartRtcTicks(uint32_t tickStart, uint32_t tickPeriod);
void scifStartRtcTicksNow(uint32_t tickPeriod);
void scifStopRtcTicks(void);


#endif
//@}


// Generated by BHARAT-DELL-LAP at 2022-02-09 10:17:16.210
