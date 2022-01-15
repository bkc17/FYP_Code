################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
build-1281562081:
	@$(MAKE) --no-print-directory -Onone -f TOOLS/subdir_rules.mk build-1281562081-inproc

build-1281562081-inproc: ../TOOLS/app_uartlog.cfg
	@echo 'Building file: "$<"'
	@echo 'Invoking: XDCtools'
	"C:/ti/xdctools_3_32_00_06_core/xs" --xdcpath="C:/ti/tirtos_cc13xx_cc26xx_2_20_01_08/packages;C:/ti/tirtos_cc13xx_cc26xx_2_20_01_08/products/tidrivers_cc13xx_cc26xx_2_20_01_10/packages;C:/ti/tirtos_cc13xx_cc26xx_2_20_01_08/products/bios_6_46_01_38/packages;C:/ti/tirtos_cc13xx_cc26xx_2_20_01_08/products/uia_2_00_06_52/packages;" xdc.tools.configuro -o configPkg -t ti.targets.arm.elf.M3 -p ti.platforms.simplelink:CC2650F128 -r release -c "C:/ti/ccsv8/tools/compiler/ti-cgt-arm_18.1.3.LTS" --compileOptions "-mv7M3 --code_state=16 -me -O4 --opt_for_speed=0 --include_path=\"C:/Users/bhara/workspace_v8/adc_ranger_cc2650_launchxl\" --include_path=\"c:/ti/simplelink_academy_01_11_00_0000/modules/projects/support_files/Components/uart_log\" --include_path=\"C:/Users/bhara/workspace_v8/adc_ranger_cc2650_launchxl/Application\" --include_path=\"C:/Users/bhara/workspace_v8/adc_ranger_cc2650_launchxl/Scif\" --include_path=\"C:/Users/bhara/workspace_v8/adc_ranger_cc2650_launchxl/Board\" --include_path=\"c:/ti/tirtos_cc13xx_cc26xx_2_20_01_08/products/cc26xxware_2_24_02_17393\" --include_path=\"C:/ti/ccsv8/tools/compiler/ti-cgt-arm_18.1.3.LTS/include\" --define=POWER_SAVING --define=xdc_runtime_Assert_DISABLE_ALL --define=Xxdc_runtime_Log_DISABLE_ALL --define=CC26XXWARE --define=xdc_FILE=\"\"\"\" --define=UARTLOG_NUM_EVT_BUF=32 -g --c99 --gcc --diag_warning=225 --diag_warning=255 --diag_wrap=off --display_error_number --gen_func_subsections=on --abi=eabi  " "$<"
	@echo 'Finished building: "$<"'
	@echo ' '

configPkg/linker.cmd: build-1281562081 ../TOOLS/app_uartlog.cfg
configPkg/compiler.opt: build-1281562081
configPkg/: build-1281562081


