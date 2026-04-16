| **Hardware Function** | **Schematic Requirement** | **Linux Kernel DTB** | **Comparison Result** |
|----------------------|--------------------------|----------------|---------------------|---------------------|
| **USB Type-C (P13)** | USB_OTG1 with PD controller (PTN5110 @I2C3:0x50) |  ✅ usbotg1: OTG mode, role-switch, ptn5110 tcpc | ✅ Match |
| **USB Type-A Host (P17)** | USB_OTG2 as host, 5V power via U731 | ✅ usbotg2: host mode | ✅ Match |
| **Ethernet ENET1 (P15)** | RGMII, RTL8211 PHY @MDIO:1, Reset via PCAL6524:15 | ✅ eqos: RGMII-ID, PHY@1, Reset GPIO pcal6524:15 | ⚠️ Reset GPIO differ (U-Boot: pin 4, Kernel: pin 15) |
| **Ethernet ENET2 (P14)** | RGMII, RTL8211 PHY @MDIO:2, Reset via PCAL6524:16 | ✅ fec: RGMII-ID, PHY@2, Reset GPIO pcal6524:16 | ⚠️ Reset GPIO differ (U-Boot: pin 9, Kernel: pin 16) |
| **CAN2 (P22)** | TJA1051T/3, TX: GPIO_IO25, RX: GPIO_IO27| ✅ flexcan2: Enabled, regulator can2_stby |  ✅ Match  |
| **eMMC (USDHC1)** | 32GB HS400, 8-bit bus | ✅ usdhc1: 8-bit, non-removable, tuning-step=1 | ✅ Match |
| **MicroSD (USDHC2)** | SD3.0, 4-bit, CD GPIO3:0, VSD_3V3 regulator |  ✅ usdhc2: 4-bit, CD gpio3:0, vmmc regulator, tuning-step=1     | ✅ Match |
| **WiFi/BT (USDHC3)** | M.2 KEY-E IW612 (MAYA-W2), WLAN_EN via PCAL6524:20  ✅ usdhc3: 4-bit, vmmc+pwrseq, wifi-wake-host | ✅ Match |
| **PMIC (PCA9451A)** | @I2C2:0x25, BUCK1-6, LDO1/4/5, INT via PCAL6524:11  | ✅ pmic@25: All regulators configured | ✅ Match |
| **GPIO Expander (PCAL6524)** | @I2C2:0x22, 24 GPIO pins, INT via GPIO3:27  | ✅ pcal6524@22: Configured with pin definitions | ✅ Match |
| **UART1 Console** | lpuart1, RX/TX |✅ lpuart1: Enabled, stdout-path | ✅ Match |
| **UART5 BT** | lpuart5 for Bluetooth (IW612) | ✅ lpuart5: Enabled + BT nxp,88w8987-bt | ✅ Match|
| **I2C1** | LVDS Bridge IT6263 @0x4C |PCAL6408 @0x20 |✅ Match |
| **I2C2** | PMIC, GPIO Expander, EEPROM AT24C256 @0x50 |  ✅ lpi2c2: PMIC, PCAL6524 |  ✅ Match |
| **I2C3** | RTC PCF2131 @0x53, PTN5110 @0x50, Camera ISP| ✅ lpi2c3: RTC, PTN5110, ADP5585, AP1302 camera |  ✅ Match|
| **SPI (LPSPI3)** | SPI expansion header, CS via GPIO2:8 | ✅ lpspi3: Enabled, spidev |  ✅ Match |
| **RTC (PCF2131)** | @I2C3:0x53, INT via PCAL6524:1 | ✅ rtc@53: INT edge-falling | ⚠️ INT type differ |
| **ADC** | ADC1, 1.8V vref |✅ adc1: vref 1.8V | ✅ Match|
| **LED PWM (TPM3/4)** | RGB LED via TPM3/4 channels | ✅ tpm3/tpm4: Enabled with pinctrl |  ✅ Match |
| **Audio (SAI1+MQS)** | MQS audio output | ✅ sai1+mqs1: sound-mqs configured |  ✅ Match |
| **LVDS to HDMI** | IT6263 bridge, reset via PCAL6524:21 |  ✅ IT6263, ldb, ldb_phy configured |  ✅ Match |
| **MIPI CSI Camera** | AP1302 ISP + AR0144 sensor | ✅ mipi_csi, isi, ap1302, camera regulators |  ✅ Match|
| **User Buttons** | K2/K3 via PCAL6524:5/6 | ✅ sw-keys: user_btn1/2 configured |  ✅ Match |
| **Cortex-M33** | Remote processor via MU1 |  ✅ cm33: mbox + memory regions | ✅ Match (kernel has more detail) |
| **Watchdog** | WDOG3 |  ✅ wdog3: Enabled |  ✅ Match |
| **Power Regulators** | VEXP_3V3, VEXP_5V, VDD_12V via PCAL6524 |  ✅ All regulators configured |  ✅ Match|

## Summary:

**✅ Full Match (9):** USB Type-C, USB Host, eMMC, MicroSD, PMIC, GPIO Expander,UART1, ADC, Cortex-M33

**⚠️ Partial Match (5):** ENET1/2 (wrong GPIO pins), UART5 (BT device missing), I2C2/3 (some devices missing), RTC (INT type)


