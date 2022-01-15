# invoke SourceDir generated makefile for app_uartlog.pem3
app_uartlog.pem3: .libraries,app_uartlog.pem3
.libraries,app_uartlog.pem3: package/cfg/app_uartlog_pem3.xdl
	$(MAKE) -f C:\Users\bhara\workspace_v8\adc_ranger_cc2650_launchxl\TOOLS/src/makefile.libs

clean::
	$(MAKE) -f C:\Users\bhara\workspace_v8\adc_ranger_cc2650_launchxl\TOOLS/src/makefile.libs clean

