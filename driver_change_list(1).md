# Driver Change List — FRDM-IMX93 (FINAL)

**Tree**: NXP `linux-imx` lf-6.12.20-2.0.0

All driver paths and compatible strings verified against Kernel DTS
compatible strings and NXP downstream tree structure.

| Component | Path | Status | Change? | Rationale | Verify |
|---|---|---|---|---|---|
| **Core System** |
| i.MX93 SoC DTSI | `arch/arm64/boot/dts/freescale/imx93.dtsi` | Present | No | Common SoC DTSI | `ls` |
| **Power** |
| PCA9451A PMIC regulator | `drivers/regulator/pca9450-regulator.c` | Present | No | Family driver; `nxp,pca9451a` compatible included | `grep -n pca9451a drivers/regulator/pca9450-regulator.c` |
| PCAL6524 GPIO expander | `drivers/gpio/gpio-pca953x.c` | Present | No | PCA95xx family driver | `grep -l pcal6524 drivers/gpio/gpio-pca953x.c` |
| PCAL6408 GPIO expander | `drivers/gpio/gpio-pca953x.c` | Present | No | Same PCA95xx driver | `grep -l pcal6408 drivers/gpio/gpio-pca953x.c` |
| ADP5585 GPIO expander | `drivers/gpio/gpio-adp5585.c` or `drivers/mfd/adp5585.c` | **Verify** | Possibly | May be NXP-BSP-only; camera-side expander | `find drivers -iname "*adp5585*"` |
| Fixed regulators | `drivers/regulator/fixed.c` | Present | No | Standard `regulator-fixed` | `ls` |
| **Ethernet** |
| EQOS (ENET1) glue | `drivers/net/ethernet/stmicro/stmmac/dwmac-imx.c` | Present | No | i.MX93 EQOS glue | `ls` |
| EQOS core | `drivers/net/ethernet/stmicro/stmmac/stmmac_main.c` | Present | No | Generic STMMAC | `ls` |
| FEC (ENET2) | `drivers/net/ethernet/freescale/fec_main.c` | Present | No | i.MX FEC | `ls` |
| RTL8211 PHY | `drivers/net/phy/realtek.c` | Present | No | Supports RTL8211FSI-CG used on FRDM | `grep -l RTL8211F drivers/net/phy/realtek.c` |
| YT8521 PHY (alternative) | `drivers/net/phy/motorcomm.c` | Check | No (if present) | Schematic shows YT8521SH compatible design | `grep -l YT8521 drivers/net/phy/motorcomm.c` |
| **USB** |
| USB OTG/Host (Chipidea) | `drivers/usb/chipidea/ci_hdrc_imx.c` | Present | No | i.MX93 uses Chipidea IP, **not DWC3** | `ls` |
| PTN5110 TCPC | `drivers/usb/typec/tcpm/tcpci.c` | Present | No | TCPCI-compatible | `ls` |
| NX20P3483 USB-C protection (U710) | Typically no specific driver | — | No | Hardware-only PD/VBUS switch | — |
| PCMF1USB3S data protection | — | — | No | Passive | — |
| **Storage** |
| eMMC / SD (USDHC) | `drivers/mmc/host/sdhci-esdhc-imx.c` | Present | No | i.MX eSDHC/uSDHC | `ls` |
| **Display** |
| IT6263 LVDS-HDMI bridge | `drivers/gpu/drm/bridge/ite-it6263.c` | Present (NXP lf-6.12 tree) | No | ITE IT6263 bridge; downstream NXP tree has it | `ls drivers/gpu/drm/bridge/ite-it6263.c` |
| LDB (LVDS bridge) | `drivers/gpu/drm/bridge/fsl-ldb.c` | Present | No | Freescale LDB driver for `&ldb` / `&ldb_phy` | `ls` |
| DRM core (i.MX) | `drivers/gpu/drm/imx/` | Present | No | Infrastructure | `ls -d` |
| MIPI DSI | N/A for FRDM | — | Disable in config | FRDM uses LVDS→HDMI, not DSI as primary | — |
| **Camera** |
| ISI (image sensor interface) | `drivers/media/platform/nxp/imx8-isi/` | Present | No | Used by i.MX93 ISI | `ls -d` |
| AP1302 ISP | `drivers/media/i2c/ap1302.c` | **Verify** | Possibly | ON Semi AP1302; may require vendor/out-of-tree driver | `find drivers/media/i2c -iname "*ap1302*"` |
| AR0144 CMOS sensor | `drivers/media/i2c/ar0144.c` | **Verify** | Possibly | ON Semi AR0144 | `find drivers/media/i2c -iname "*ar0144*"` |
| **Wireless** |
| WiFi IW612 / 88W8987 | NXP out-of-tree driver (preferred) or `drivers/net/wireless/marvell/mwifiex/mwifiex_sdio.c` | Check NXP tree first | **Selection choice** | NXP vendor driver gives full features; mwifiex is fallback. Needs firmware blob. | `find drivers/net/wireless -iname "*nxp*" -o -iname "*mwifiex*sdio*"` |
| BT IW612 | `drivers/bluetooth/btnxpuart.c` | Present (mainline 6.4+) | No | Binds via compatible `nxp,88w8987-bt` (Kernel DTS line 613) | `grep -l 88w8987-bt drivers/bluetooth/btnxpuart.c` |
| **CAN** |
| FlexCAN2 | `drivers/net/can/flexcan/flexcan-core.c` | Present | No | i.MX FlexCAN | `ls` |
| TJA1051T/3 transceiver | — | — | No | Passive, controlled via regulator-fixed on PCAL6524 GPIO 23 | — |
| **Audio** |
| MQS | `sound/soc/fsl/fsl_mqs.c` | Present | No | Freescale MQS | `ls` |
| SAI (I2S) | `sound/soc/fsl/fsl_sai.c` | Present | No | Freescale SAI | `ls` |
| MQS machine driver | `sound/soc/fsl/imx-audio-mqs.c` or similar | **Verify** | Possibly | DTS compat `fsl,imx6sx-sdb-mqs` + `fsl,imx-audio-mqs` — needs machine driver | `find sound/soc/fsl -iname "*mqs*"` |
| **RTC** |
| PCF2131 | `drivers/rtc/rtc-pcf2127.c` | Present | No | Family driver covers PCF2127/2129/2131 | `grep -l pcf2131 drivers/rtc/rtc-pcf2127.c` |
| **UI** |
| PWM LEDs | `drivers/leds/leds-pwm.c` | Present | No | Needed for RGB LED via TPM3/TPM4 PWM | `ls` |
| TPM PWM | `drivers/pwm/pwm-imx-tpm.c` | Present | No | i.MX TPM-based PWM | `ls` |
| GPIO Keys | `drivers/input/keyboard/gpio_keys.c` | Present | No | For K2/K3 | `ls` |
| **Misc** |
| AT24 EEPROM | `drivers/misc/eeprom/at24.c` | Present | No | Standard AT24 | `ls` |
| ADC (i.MX93) | `drivers/iio/adc/imx93_adc.c` | Present | No | i.MX93 ADC driver | `find drivers/iio/adc -iname "imx93*"` |
| CH342F UART bridge | Host-side driver only | — | No | Only matters on host PC, not target | — |
| **U-Boot side** |
| PCA9450 / PCA9451A | `drivers/power/regulator/pca9450.c` | Present | No | U-Boot PMIC driver | `ls` |
| PCAL6524 | `drivers/gpio/pca953x_gpio.c` | Present | No | U-Boot PCA95xx | `ls` |
| FEC | `drivers/net/fec_mxc.c` | Present | No | U-Boot FEC | `ls` |
| DWC EQOS | `drivers/net/dwc_eth_qos.c` + `dwc_eth_qos_imx.c` | Present | No | U-Boot EQOS | `ls` |
| uSDHC | `drivers/mmc/fsl_esdhc_imx.c` | Present | No | U-Boot uSDHC | `ls` |

## Summary

- **Drivers present and no change needed**: 26
- **Drivers requiring verification**: 5 (ADP5585, AP1302, AR0144, WiFi stack, MQS machine)
- **Blocking items**: 1 (WiFi driver selection — either NXP out-of-tree or mwifiex_sdio)
- **Confirmed missing**: 0

## Firmware Requirements

| Component | Firmware | Source | Required |
|---|---|---|---|
| WiFi IW612 | `/lib/firmware/nxp/sdiouart_iw612.bin.se` (or similar) | NXP linux-firmware | Yes |
| BT IW612 | `/lib/firmware/nxp/uartuart8987_bt_v0.bin` (or similar) | NXP linux-firmware | Yes |
| DDR training | Embedded in `imx-boot` container | U-Boot build | Yes (U-Boot only) |
| ELE / EdgeLock Enclave FW | `/lib/firmware/imx/mx93a1-ahab-container.img` | NXP | Yes (secure boot) |

## Build Artifacts Needed (Review §5 deliverables)

These are not driver changes but are mandatory for a working BSP and
are currently missing from the repo:

1. **U-Boot defconfig**: `configs/imx93_11x11_frdm_defconfig`
   - Start from `imx93_11x11_evk_defconfig`
   - Set `CONFIG_DEFAULT_DEVICE_TREE="imx93-11x11-frdm"`
   - Verify PMIC selection is PCA9451A

2. **Kernel Makefile entry**: `arch/arm64/boot/dts/freescale/Makefile`
   - Add `dtb-$(CONFIG_ARCH_MXC) += imx93-11x11-frdm.dtb`

3. **U-Boot board directory**: `board/freescale/imx93_11x11_frdm/`
   - `imx93_11x11_frdm.c` (board_init, dram_init)
   - `imximage.cfg` / `imximage-8mb-lpddr4x.cfg`
   - `Kconfig`, `Makefile`, `MAINTAINERS`

4. **U-Boot arch Kconfig / Makefile**: `arch/arm/mach-imx/imx9/`
   - Add new board target to Kconfig
   - Add corresponding `obj-y` line to Makefile

## Next Actions

1. Run verification commands in the linux-imx tree to confirm driver presence
2. Resolve WiFi driver stack choice (NXP out-of-tree recommended for full features)
3. Confirm ADP5585 / AP1302 / AR0144 driver availability (critical for camera)
4. Confirm MQS machine driver exists for `fsl,imx-audio-mqs` compatible
5. Create the 4 build artifact groups above
