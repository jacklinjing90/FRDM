# Hardware Comparison Table: FRDM-IMX93 vs MCIMX93-EVK

**Target:** FRDM-IMX93 (SPF-94611_B2)  
**Reference:** MCIMX93-EVK (MCIMX93-SOM + MCIMX93-BB)  
**SoC:** i.MX93 (both platforms)

| Function or Hardware Name | Target Document Name | Reference Document Name | Match Status | Change Type |
|---|---|---|---|---|
| **CPU/SoC** |
| CPU Core | i.MX93 MIMX9352CVVXMAB | i.MX93 | Match | No Change |
| ARM Cortex-A55 | 2x 1.8GHz | 2x 1.8GHz | Match | No Change |
| ARM Cortex-M33 | 1x 250MHz | 1x 250MHz | Match | No Change |
| Ethos-U65 NPU | 0.5 TOPs @ 1GHz | 0.5 TOPs @ 1GHz | Match | No Change |
| **Memory** |
| LPDDR4/X | 2GB x16 | 2GB x16 | Match | No Change |
| eMMC | 32GB HS400 | 16GB HS400 | Different | DTS |
| **Boot and Debug** |
| Debug Console (UART1) | LPUART1 | LPUART1 | Match | No Change |
| JTAG/SWD | Standard SWD | Standard SWD | Match | No Change |
| Boot Config | GPIO-based | GPIO-based | Match | DTS |
| **Power Management** |
| PMIC | NXP PCA9451A | NXP PCA9451A | Match | No Change |
| System Power Input | USB-C PD 12-20V | USB-C PD 12-20V | Match | DTS |
| Power Tree | Simplified | Full-featured | Different | DTS |
| **Ethernet** |
| ENET1 (EQOS) PHY | Realtek RTL8211 (RGMII) | Realtek RTL8211FDI (RGMII) | Match | DTS |
| ENET2 (FEC) PHY | Realtek RTL8211 (RGMII) | Realtek RTL8211FDI (RGMII) | Match | DTS |
| ENET1 Reset GPIO | PCAL6524 pin 4 | PCAL6524 pin 15 | Different | DTS |
| ENET2 Reset GPIO | PCAL6524 pin 9 | PCAL6524 pin 16 | Different | DTS |
| **USB** |
| USB1 Type-C | USB 2.0 DRP w/ PD | USB 2.0 DRP w/ PD | Match | DTS |
| USB2 Type-C | USB 2.0 Host | USB 2.0 DRP w/ PD | Different | DTS |
| USB Type-A | Present | Present | Match | DTS |
| USB PD Controller | NXP PTN5110 | NXP PTN5110 x2 | Different | DTS |
| **Storage** |
| SD Card Slot (USDHC2) | MicroSD (SD3.0) | MicroSD (SD3.0) | Match | DTS |
| eMMC (USDHC1) | 32GB on-board | 16GB (SOM) | Different | DTS |
| M.2 Slot (USDHC3) | M.2 Key-E (WiFi/BT) | M.2 Key-E (WiFi/BT) | Match | DTS |
| **Audio** |
| Audio Codec | None (MQS only) | WM8962 I2S Codec | Missing in Target | DTS + Driver |
| Audio Interface | SAI3 (MQS), SAI1 (BT) | SAI3 (I2S), SAI1 (BT) | Different | DTS |
| Microphone | PDM not populated | PDM + onboard mics | Different | DTS |
| Audio Jack | Not present | HP Out + Mic In | Missing in Target | DTS |
| Speaker Output | MQS | Line Out + Speaker | Different | DTS |
| **Display** |
| MIPI DSI | 4-lane DSI | 4-lane DSI | Match | DTS |
| DSI to HDMI Bridge | Not present | ADV7535 | Missing in Target | DTS |
| LVDS | Not present | LVDS TX (IT6263) | Missing in Target | DTS + Driver |
| Backlight Control | TPM5 PWM | ADP5585 PWM | Different | DTS |
| **Camera** |
| MIPI CSI | 2-lane CSI | 2-lane CSI + AP1302 ISP | Different | DTS |
| Camera Sensor | Not present | AR0144 via AP1302 | Missing in Target | DTS + Driver |
| **Connectivity** |
| WiFi/BT Module | M.2 slot (IW612) | M.2 slot (IW612/MAYA-W2) | Match | DTS |
| 802.15.4 | MAYA-W2 via M.2 | MAYA-W2 via M.2 | Match | DTS |
| **CAN Bus** |
| CAN Controller | FlexCAN2 | FlexCAN2 | Match | No Change |
| CAN Transceiver | TJA1051T/3 | TJA1051T/3 | Match | DTS |
| CAN Standby Control | PCAL6524 pin 23 | ADP5585 pin 6 | Different | DTS |
| **GPIO Expanders** |
| Primary GPIO Expander | PCAL6524 @ 0x22 (I2C2) | PCAL6524 @ 0x22 (I2C2) | Match | DTS |
| Secondary GPIO Expander | None | ADP5585 @ 0x34 (I2C2) | Missing in Target | DTS |
| ISP GPIO Expander | None | ADP5585_ISP @ 0x34 (I2C3) | Missing in Target | DTS |
| **I2C Buses** |
| I2C1 (LPI2C1) | General purpose | Codec + HDMI bridge | Different | DTS |
| I2C2 (LPI2C2) | PMIC + PCAL6524 | PMIC + PCAL6524 + ADP5585 | Different | DTS |
| I2C3 (LPI2C3) | RTC + USB-C PD | RTC + USB-C PD + ISP GPIO | Different | DTS |
| **SPI Buses** |
| LPSPI1 | Enabled (exp header) | Not used | Different | DTS |
| LPSPI2 | Enabled (exp header) | Not used | Different | DTS |
| LPSPI3 | Enabled (exp header) | Used (exp header) | Match | DTS |
| LPSPI4 | Enabled (exp header) | Not used | Different | DTS |
| **PWM/Timers** |
| TPM5 | PWM for backlight | Not used | Different | DTS |
| TPM6 | PWM output | Not used | Different | DTS |
| **User Interface** |
| RGB LED | 3x GPIO via PCAL6524 (14,15,16) | Not present | Different | DTS |
| User Button | GPIO3_26 | Not present | Different | DTS |
| **Sensors** |
| IMU/Accelerometer | Not present | LSM6DSOXTR (I2C) | Missing in Target | DTS |
| **RTC** |
| RTC IC | PCF2131 @ 0x53 (I2C3) | PCF2131 @ 0x53 (I2C3) | Match | DTS |
| RTC Interrupt | PCAL6524 pin 1 | PCAL6524 pin 1 | Match | DTS |
| **Expansion Connectors** |
| Expansion Header | Custom pinout | Custom pinout | Different | DTS |
| Arduino Headers | Not present | Not present | Match | No Change |
| **Power Rails** |
| VDD_SOC | 0.65-0.9V (BUCK1) | 0.65-0.9V (BUCK1) | Match | No Change |
| VDD2_DDR | 1.1V (BUCK2) | 1.1V (BUCK2) | Match | No Change |
| VDDQ_DDR | 0.6V (LPDDR4X) | 0.6V (LPDDR4X) | Match | No Change |
| VDD_3V3 | 3.3V (BUCK4) | 3.3V (BUCK4) | Match | No Change |
| Expansion 3.3V Rail | VEXP_3V3 (PCAL6524 pin 2) | VEXT_3V3 (GPIO control) | Different | DTS |
| Expansion 5V Rail | VEXP_5V (PCAL6524 pin 8) | VEXT_5V (GPIO control) | Different | DTS |
| **Pin Multiplexing** |
| UART5 Usage | Console/debug option | BT UART (IW612) | Different | DTS |
| GPIO_IO28/29 | I2C3 SDA/SCL | I2C3 SDA/SCL | Match | DTS |
| SAI3 Pins | Available on exp header | Codec I2S | Different | DTS |
| **Special Features** |
| EEPROM | AT24C256 @ 0x50 (I2C2) | Not present | Different | DTS |

## Summary

**Total Items Compared:** 68

**Breakdown:**
- **Match:** 23 items (No Change required)
- **Different:** 37 items (DTS changes needed)
- **Missing in Target:** 8 items (May need DTS + Driver)

## Key Differences Requiring DTS Changes

1. **Audio Subsystem:** FRDM has no external codec, uses MQS only
2. **Display:** FRDM lacks HDMI bridge and LVDS support
3. **GPIO Expanders:** FRDM uses only PCAL6524, EVK has additional ADP5585 expanders
4. **Ethernet PHY Reset:** Different GPIO pins
5. **USB Configuration:** USB2 is host-only on FRDM vs DRP on EVK
6. **LEDs:** FRDM has RGB LED, EVK does not
7. **User Button:** FRDM has button, EVK does not
8. **SPI Buses:** FRDM enables more SPI ports for expansion
9. **PWM Timers:** FRDM uses TPM5/6 for expansion features
10. **Expansion Rails:** Different GPIO control for power enables

## Driver Changes Likely Needed

1. **Audio Codec (WM8962):** Missing on FRDM, driver may need conditional compilation
2. **ISP (AP1302):** Missing on FRDM, camera path different
3. **HDMI Bridge (ADV7535):** Missing on FRDM
4. **LVDS Bridge (IT6263):** Missing on FRDM

## Next Steps

1. Generate Linux DTS for FRDM from U-Boot DTS
2. Modify according to this comparison table
3. Build and validate DTBs
4. Check driver dependencies
