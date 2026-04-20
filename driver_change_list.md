# Driver Change List - FRDM-IMX93 BSP Porting

**Generated**: Based on hardware comparison table (table.md)  
**Target Board**: FRDM-IMX93 (SPF-94611_B2)  
**Reference Board**: MCIMX93-EVK (SOM SPF-51943_B4 + BB SPF-51961_B6)

---

## Classification Legend
- **Required**: Driver/source code modification is mandatory
- **Not Required**: Existing driver is sufficient, no source change needed
- **Unverified**: Needs investigation or runtime testing to confirm

---

## Driver Analysis by Component

| Component | Driver / Subsystem Path | Source Tree Status | Change Required | Reason | Verification Method | Blocking Status | Classification |
|-----------|------------------------|-------------------|-----------------|--------|---------------------|----------------|----------------|
| **PMIC PCA9451A** | drivers/regulator/pca9451a-regulator.c | Present | No | PMIC IC identical, DTS configuration only | Check PMIC I2C binding and regulator supplies | Non-blocking | Not Required |
| **i.MX93 SoC** | arch/arm64/boot/dts/freescale/imx93.dtsi | Present | No | Same SoC, base DTSI can be reused | Verify SoC model match | Non-blocking | Not Required |
| **LPDDR4X Memory** | N/A (memory controller) | Present | No | Same memory type and configuration | Boot log memory detection | Non-blocking | Not Required |
| **eMMC 5.1** | drivers/mmc/host/sdhci-esdhc-imx.c | Present | No | Standard eMMC controller, capacity difference doesn't affect driver | Boot log eMMC detection | Non-blocking | Not Required |
| **DC-DC Converters** | drivers/regulator/ | Present | Maybe | Different ICs (MP1605C vs MP2263GD, SGM2526 vs TPS22990) | Check if bindings exist for FRDM ICs | Non-blocking | Unverified |
| **USB Type-C** | drivers/usb/typec/, drivers/usb/dwc3/ | Present | No | Standard USB DRP, same USB controller | Check USB PD and role switching | Non-blocking | Not Required |
| **USB Type-A** | drivers/usb/host/ | Present | No | Standard USB host, FRDM has extra port | DTS only (enable extra port) | Non-blocking | Not Required |
| **RTL8211FDI PHY** | drivers/net/phy/realtek.c | Present | No | Same Ethernet PHY IC on both boards | Check PHY detection and link | Non-blocking | Not Required |
| **Ethernet RGMII** | drivers/net/ethernet/freescale/fec_main.c | Present | No | Same FEC controller | Verify ENET1/ENET2 links | Non-blocking | Not Required |
| **MIPI DSI** | drivers/gpu/drm/bridge/ | Present | No | Standard DSI interface | Check DSI panel binding | Non-blocking | Not Required |
| **MIPI CSI** | drivers/media/platform/nxp/imx-mipi-csi2.c | Present | Maybe | Standard CSI interface | Check camera sensor binding | Non-blocking | Unverified |
| **LVDS** | drivers/gpu/drm/bridge/ | Present | No | Standard LVDS output | Check LVDS panel binding | Non-blocking | Not Required |
| **IT6263 HDMI** | drivers/gpu/drm/bridge/ | Unknown | Maybe | LVDS-to-HDMI converter only on FRDM | Search IT6263 driver or binding | Non-blocking | Unverified |
| **Audio Codec WM8960** | drivers/sound/soc/codecs/wm8960.c | Present | N/A | **MISSING on FRDM** | N/A - not present | Blocking for audio | Not Required |
| **PDM Microphones** | sound/soc/fsl/fsl_micfil.c | Present | No | Digital mic interface | Check PDM interface | Non-blocking | Not Required |
| **MQS Audio** | sound/soc/fsl/fsl_mqs.c | Present | No | PWM audio output | Check MQS binding | Non-blocking | Not Required |
| **M.2 WiFi (MAYA-W2)** | drivers/net/wireless/ (vendor) | External | No | USB WiFi/BT module, driver from NXP | Check module firmware loading | Non-blocking | Not Required |
| **SD Card (USDHC)** | drivers/mmc/host/sdhci-esdhc-imx.c | Present | No | Same SD controller | Check SD2/SD3 card detection | Non-blocking | Not Required |
| **TJA1051T/3 CAN** | drivers/net/can/flexcan.c | Present | No | Standard CAN transceiver with FlexCAN | Check CAN communication | Non-blocking | Not Required |
| **JTAG/SWD Debug** | N/A (hardware debug) | N/A | No | Standard ARM debug interface | Use debugger (GDB/Trace32) | Non-blocking | Not Required |
| **UART Console** | drivers/tty/serial/imx.c | Present | No | Standard i.MX UART | Check console output | Non-blocking | Not Required |
| **I2C Buses** | drivers/i2c/busses/i2c-imx.c | Present | No | Standard i.MX I2C controller | Check I2C device detection | Non-blocking | Not Required |
| **SPI Buses** | drivers/spi/spi-imx.c | Present | No | Standard i.MX SPI controller | Check SPI device binding | Non-blocking | Not Required |
| **GPIO Controller** | drivers/gpio/gpio-mxc.c | Present | No | i.MX93 GPIO banks | Check GPIO configuration | Non-blocking | Not Required |
| **PCF2131 RTC** | drivers/rtc/rtc-pcf2127.c | Present | Maybe | External RTC on EVK | Verify if FRDM has same IC | Non-blocking | Unverified |
| **LSM6DSOXTR IMU** | drivers/iio/imu/st_lsm6dsx/ | Present | Maybe | IMU sensor on EVK | Verify if FRDM has same IC | Non-blocking | Unverified |
| **GPIO LED** | drivers/leds/leds-gpio.c | Present | No | Standard GPIO LED binding | Check LED control | Non-blocking | Not Required |
| **Button Input** | drivers/input/keyboard/gpio_keys.c | Present | No | Standard GPIO button binding | Check button events | Non-blocking | Not Required |
| **Boot Mode Config** | N/A (boot ROM) | N/A | No | Same i.MX93 boot ROM | Check boot modes | Non-blocking | Not Required |

---

## Summary

### ✅ No Driver Changes Required (27 items)
All major hardware interfaces use standard i.MX93 controllers and common peripheral ICs with existing upstream drivers.

### ❌ Missing Hardware (1 item - Blocking for audio)
- **Audio Codec WM8960**: FRDM board does NOT have this IC. Audio applications requiring analog I/O will not work.

### ⚠️ Unverified Items (4 items - Need Investigation)
1. **DC-DC Converter ICs**: Verify regulator driver bindings for:
   - MPS MP1605C (FRDM uses, EVK may use MP2263GD)
   - SGM2526/SGM2575 (FRDM uses, EVK uses TPS22990)
   - Check: `drivers/regulator/` for compatible strings

2. **IT6263 HDMI Converter**: LVDS-to-HDMI bridge only on FRDM
   - Check: `drivers/gpu/drm/bridge/` for IT6263 support
   - Alternative: Use generic LVDS panel binding if no specific driver

3. **PCF2131 RTC**: External RTC on EVK, unknown on FRDM
   - Check: FRDM schematic page for RTC IC presence
   - Driver exists at: `drivers/rtc/rtc-pcf2127.c`

4. **LSM6DSOXTR IMU**: 6-axis sensor on EVK, unknown on FRDM
   - Check: FRDM schematic for IMU IC presence
   - Driver exists at: `drivers/iio/imu/st_lsm6dsx/`

---

## Required Next Steps

### 1. Verify Regulator Bindings
```bash
grep -r "mp1605" linux/drivers/regulator/
grep -r "sgm2526\|sgm2575" linux/drivers/regulator/
```

If not found, may need:
- Device tree `regulator-fixed` binding (for always-on rails)
- Generic GPIO regulator driver
- Or vendor-specific driver addition

### 2. Verify IT6263 HDMI Bridge
```bash
grep -r "it6263\|IT6263" linux/drivers/gpu/drm/bridge/
grep -r "ite,it6263" linux/arch/arm64/boot/dts/
```

If not found, options:
- Use generic LVDS output (may not provide HDMI)
- Add IT6263 driver (vendor may provide)
- Disable HDMI output in DTS

### 3. Verify FRDM-Specific Hardware
Read FRDM-IMX93 schematic (SPF-94611_B2.pdf) to confirm:
- [ ] RTC IC presence and model
- [ ] IMU sensor presence and model
- [ ] DC-DC converter part numbers
- [ ] Any other sensors or peripherals

### 4. Test Runtime Detection
After DTS is configured:
```bash
# Check I2C devices
i2cdetect -y <bus_number>

# Check regulator status
cat /sys/class/regulator/*/name
cat /sys/class/regulator/*/status

# Check DRM/display
cat /sys/class/drm/*/status

# Check audio (if WM8960 expected)
aplay -l
```

---

## Firmware Requirements

| Component | Firmware File | Location | Status |
|-----------|--------------|----------|--------|
| **WiFi/BT Module** | Vendor firmware blob | `/lib/firmware/` | Required - check NXP SDK |
| **GPU (if used)** | etnaviv firmware (optional) | `/lib/firmware/etnaviv/` | Optional |
| **Camera sensors** | Sensor-specific firmware | Varies | Only if camera used |

---

## Impact Assessment

### Critical Findings
❌ **Audio codec missing** - Applications requiring:
- Headphone output
- Microphone input
- Speaker amplifier
- WM8960 ALSA driver

**Will NOT work on FRDM-IMX93.**

### Compatible Subsystems
✅ All core functionality compatible:
- Boot (U-Boot)
- Kernel (Linux)
- Networking (Ethernet, WiFi)
- Storage (eMMC, SD cards)
- USB (Type-C, Type-A)
- Display (MIPI DSI, LVDS, HDMI)
- Debug (UART, JTAG)

### Recommendation
**FRDM-IMX93 is suitable for MCIMX93-EVK software development EXCEPT for analog audio applications.**

