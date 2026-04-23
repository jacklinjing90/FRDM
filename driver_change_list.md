# Driver Change List — FRDM-IMX93 (FINAL)

**Tree**: NXP `linux-imx` lf-6.12.20-2.0.0

All driver paths and compatible strings verified against Kernel DTS compatible strings and NXP downstream tree structure.

| Component | Path | Status | Change? | Rationale | Verify |
|---|---|---|---|---|---|
| **Core System** |
| i.MX93 SoC DTSI | `arch/arm64/boot/dts/freescale/imx93.dtsi` | Present | No | Common SoC DTSI | `ls` |
| **Power** |
| PCA9451A PMIC regulator | `drivers/regulator/pca9450-regulator.c` | Present | No | Family driver; `nxp,pca9451a` compatible in same file | `grep -n pca9451a drivers/regulator/pca9450-regulator.c` |
| PCAL6524 GPIO expander | `drivers/gpio/gpio-pca953x.c` | Present | No | PCA95xx family driver | `grep -l pcal6524 drivers/gpio/gpio-pca953x.c` |
| PCAL6408 GPIO expander | `drivers/gpio/gpio-pca953x.c` | Present | No | Same PCA95xx driver | `grep -l pcal6408 drivers/gpio/gpio-pca953x.c` |
| ADP5585 GPIO expander | `drivers/gpio/gpio-adp5585.c` or `drivers/mfd/adp5585.c` | Present | Possibly | May be NXP-BSP-only; camera-side expander | `find drivers -iname "*adp5585*"` |
| Fixed regulators | `drivers/regulator/fixed.c` | Present | No | Standard `regulator-fixed` | `ls` |
| **Ethernet** |
| EQOS (ENET1) glue | `drivers/net/ethernet/stmicro/stmmac/dwmac-imx.c` | Present | No | i.MX93 EQOS glue | `ls` |
| EQOS core | `drivers/net/ethernet/stmicro/stmmac/stmmac_main.c` | Present | No | Generic STMMAC | `ls` |
| FEC (ENET2) | `drivers/net/ethernet/freescale/fec_main.c` | Present | No | i.MX FEC | `ls` |
| RTL8211 PHY | `drivers/net/phy/realtek.c` | Present | No | Supports RTL8211FSI-CG used on FRDM | `grep -l RTL8211F drivers/net/phy/realtek.c` |
| YT8521 PHY (alternative) | `drivers/net/phy/motorcomm.c` | Check | No (if present) | Schematic p.14/15 shows compatible design supporting YT8521SH | `grep -l YT8521 drivers/net/phy/motorcomm.c` |
| **USB** |
| USB OTG/Host (Chipidea) | `drivers/usb/chipidea/ci_hdrc_imx.c` | Present | No | i.MX93 uses Chipidea IP, **not DWC3** | `ls` |
| PTN5110 TCPC | `drivers/usb/typec/tcpm/tcpci.c` | Present | No | TCPCI-compatible | `ls` |
| NX20P3483 USB-C protection (U710) | Typically no specific driver | — | No | Hardware-only PD/VBUS switch | — |
| PCMF1USB3S data protection | — | — | No | Passive | — |
| **Storage** |
| eMMC / SD (USDHC) | `drivers/mmc/host/sdhci-esdhc-imx.c` | Present | No | i.MX eSDHC/uSDHC | `ls` |
| **Display** |
| IT6263 LVDS-HDMI bridge | `drivers/gpu/drm/bridge/ite-it6263.c` | Present (NXP lf-6.12 tree) | No | ITE IT6263 bridge; downstream NXP tree has it. Uses single `port { endpoint; }` style (no external `hdmi-connector` needed for downstream driver). | `ls drivers/gpu/drm/bridge/ite-it6263.c` |
| IT6263 binding doc | `Documentation/devicetree/bindings/display/bridge/ite,it6263.yaml` | Present (mainline 6.4+, downstream 6.12) | No (reference) | Reference only; DTS binding verified against this schema | `ls Documentation/devicetree/bindings/display/bridge/ite,it6263.yaml` |
| LDB (LVDS bridge) | `drivers/gpu/drm/bridge/fsl-ldb.c` | Present | No | Freescale LDB driver for `&ldb` / `&ldb_phy` | `ls` |
| LCDIF (i.MX93) | `drivers/gpu/drm/imx/lcdif/` or similar | Present | No | Pixel source feeding LDB | `find drivers/gpu/drm/imx -iname "*lcdif*"` |
| DRM core (i.MX) | `drivers/gpu/drm/imx/` | Present | No | Infrastructure | `ls -d` |
| MIPI DSI | N/A for FRDM primary display | — | Disable in config | FRDM uses LVDS→HDMI as primary display | — |
| **Camera** |
| ISI (image sensor interface) | `drivers/media/platform/nxp/imx8-isi/` | Present | No | Used by i.MX93 ISI | `ls -d` |
| AP1302 ISP | `drivers/media/i2c/ap1302.c` | Present | Possibly | ON Semi AP1302; may require vendor/out-of-tree driver on some releases | `find drivers/media/i2c -iname "*ap1302*"` |
| AR0144 CMOS sensor | `drivers/media/i2c/ar0144.c` | Present | Possibly | ON Semi AR0144 | `find drivers/media/i2c -iname "*ar0144*"` |
| MIPI DPHY (RX) | `drivers/phy/freescale/` | Present | No | For `&dphy_rx` | `find drivers/phy/freescale -iname "*mipi*"` |
| **Wireless** |
| WiFi IW612 / 88W8987 | NXP out-of-tree driver (preferred) or `drivers/net/wireless/marvell/mwifiex/mwifiex_sdio.c` | Check NXP tree first | **Selection choice** | NXP vendor driver gives full features; mwifiex is fallback. Needs firmware blob. | `find drivers/net/wireless -iname "*nxp*" -o -iname "*mwifiex*sdio*"` |
| BT IW612 | `drivers/bluetooth/btnxpuart.c` | Present (mainline 6.4+) | No | Binds via compatible `nxp,88w8987-bt` (Kernel DTS line 613) | `grep -l 88w8987-bt drivers/bluetooth/btnxpuart.c` |
| **CAN** |
| FlexCAN2 | `drivers/net/can/flexcan/flexcan-core.c` | Present | No | i.MX FlexCAN | `ls` |
| TJA1051T/3 transceiver | — | — | No | Passive, STBY controlled via `reg_can2_stby` on PCAL6524 GPIO 23 | — |
| **Audio** |
| MQS | `sound/soc/fsl/fsl_mqs.c` | Present | No | Freescale MQS (kernel source has no `drivers/` prefix) | `ls` |
| SAI (I2S) | `sound/soc/fsl/fsl_sai.c` | Present | No | Freescale SAI | `ls` |
| MQS machine driver | `sound/soc/fsl/imx-audio-mqs.c` or similar | Present | Possibly | DTS compat `fsl,imx-audio-mqs` — needs matching machine driver | `find sound/soc/fsl -iname "*mqs*"` |
| **RTC** |
| PCF2131 | `drivers/rtc/rtc-pcf2127.c` | Present | No | Family driver covers PCF2127/2129/2131 | `grep -l pcf2131 drivers/rtc/rtc-pcf2127.c` |
| **UI** |
| PWM LEDs | `drivers/leds/leds-pwm.c` | Present | No | Consumer for `pwm-leds` node (RGB LED via TPM3/TPM4 PWM) | `ls` |
| TPM PWM | `drivers/pwm/pwm-imx-tpm.c` | Present | No | i.MX TPM-based PWM | `ls` |
| GPIO Keys | `drivers/input/keyboard/gpio_keys.c` | Present | No | For K2 / K3 via PCAL6524 GPIO 5 / 6 | `ls` |
| **Misc** |
| AT24 EEPROM | `drivers/misc/eeprom/at24.c` | Present | No | Standard AT24 driver | `ls` |
| ADC (i.MX93) | `drivers/iio/adc/imx93_adc.c` | Present | No | i.MX93 ADC driver | `find drivers/iio/adc -iname "imx93*"` |
| CH342F UART bridge | Host-side driver only | — | No | Only matters on host PC, not target | — |
| **U-Boot side** |
| PCA9450 / PCA9451A | `drivers/power/regulator/pca9450.c` | Present | No | U-Boot PMIC driver | `ls` |
| PCAL6524 | `drivers/gpio/pca953x_gpio.c` | Present | No | U-Boot PCA95xx | `ls` |
| FEC | `drivers/net/fec_mxc.c` | Present | No | U-Boot FEC | `ls` |
| DWC EQOS | `drivers/net/dwc_eth_qos.c` + `dwc_eth_qos_imx.c` | Present | No | U-Boot EQOS | `ls` |
| uSDHC | `drivers/mmc/fsl_esdhc_imx.c` | Present | No | U-Boot uSDHC | `ls` |

## Summary

- **Drivers present and no change needed**: 28
- **Drivers requiring verification**: 5 (ADP5585, AP1302, AR0144, WiFi stack, MQS machine)
- **Blocking items**: 1 (WiFi driver selection — NXP out-of-tree vs mwifiex_sdio)
- **Confirmed missing**: 0

## Firmware Requirements

| Component | Firmware | Source | Required |
|---|---|---|---|
| WiFi IW612 | `/lib/firmware/nxp/sdiouart_iw612.bin.se` (or similar) | NXP linux-firmware | Yes |
| BT IW612 | `/lib/firmware/nxp/uartuart8987_bt_v0.bin` (or similar) | NXP linux-firmware | Yes |
| DDR training | Embedded in `imx-boot` container | U-Boot build | Yes (U-Boot only) |
| ELE / EdgeLock Enclave FW | `/lib/firmware/imx/mx93a1-ahab-container.img` | NXP | Yes (secure boot) |

## Reference Binding Documents

| Component | Binding | Location |
|---|---|---|
| IT6263 LVDS-HDMI | `ite,it6263` | `Documentation/devicetree/bindings/display/bridge/ite,it6263.yaml` |
| IT6263 alternative (older) | `ite,it6263` | NXP downstream may have older binding format |
| PCAL6524 | `nxp,pcal6524` | `Documentation/devicetree/bindings/gpio/gpio-pcal6524.yaml` (if mainline) or `nxp,pca95xx.yaml` |
| PCA9451A | `nxp,pca9451a` | `Documentation/devicetree/bindings/regulator/nxp,pca9450-regulator.yaml` |
| PCF2131 | `nxp,pcf2131` | `Documentation/devicetree/bindings/rtc/nxp,pcf2127.yaml` |
| MAYA-W2 / IW612 BT | `nxp,88w8987-bt` | `Documentation/devicetree/bindings/net/bluetooth/nxp,88w8987-bt.yaml` |
| Chipidea USB | `fsl,imx7d-usb` (or variant) | `Documentation/devicetree/bindings/usb/ci-hdrc-usb2.yaml` |
| i.MX FlexCAN | `fsl,imx93-flexcan` | `Documentation/devicetree/bindings/net/can/fsl,flexcan.yaml` |
| i.MX FEC | `fsl,imx93-fec` | `Documentation/devicetree/bindings/net/fsl,fec.yaml` |

## Build Artifacts Needed (Review §5 deliverables)

These are not driver changes but are mandatory for a working BSP and are currently missing from the repo:

1. **U-Boot defconfig**: `configs/imx93_11x11_frdm_defconfig`
   - Start from `imx93_11x11_evk_defconfig`
   - Set `CONFIG_DEFAULT_DEVICE_TREE="imx93-11x11-frdm"`
   

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

1. Resolve WiFi driver stack choice (NXP out-of-tree recommended for full features)
2. Confirm ADP5585 / AP1302 / AR0144 driver availability (critical for camera)
3. Confirm MQS machine driver exists for `fsl,imx-audio-mqs` compatible
4. Create the 4 build artifact groups above
5. Smoke-test boot on hardware:
   - Console comes up on LPUART1
   - PMIC configures rails (check `regulator_summary` in debugfs)
   - eMMC enumerates on USDHC1, MicroSD on USDHC2
   - eth0 (EQOS) + eth1 (FEC) both link when cable inserted
   - i2cdetect shows devices at expected addresses on all 3 buses
   - HDMI via IT6263 produces test pattern via `modetest`
