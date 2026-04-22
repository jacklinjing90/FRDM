# Hardware Comparison Table: FRDM-IMX93 vs MCIMX93-EVK

**Target**: FRDM-IMX93 (SPF-94611 Rev B2)
**Reference**: MCIMX93-EVK (SOM SPF-51943 + BB SPF-51961)
**Generated**: 2026-04-22 (FINAL — schematic + DTS cross-verified)

**DTS state of truth**:
- U-Boot DTS: `uboot-dts/imx93-11x11-frdm.dts`, 645 lines (minimal-edit fix of original 643-line file)
- Kernel DTS: `work/linux-dts/imx93-11x11-frdm.dts`, 1156 lines (3 edits applied on original 1111-line file)

## Source of Truth

1. **FRDM-IMX93 schematic SPF-94611 Rev B2** — primary hardware ground truth
   - Page 3: Power tree (load switch wiring)
   - Page 10/11: PMIC, system power, user buttons, RGB LED
   - Page 14/15: ENET1 / ENET2 PHY
   - Page 16: LVDS-HDMI bridge (IT6263)
   - Page 17: MIPI DSI/CSI + **PCAL6524 full pin map**
   - Page 19: WiFi/BT (MAYA-W2 module title)
   - Page 22: I²C device address table

2. **Kernel DTS** compatible strings and reg addresses cross-referenced with schematic p.22 I²C table

3. **NXP `linux-imx` lf-6.12.20-2.0.0 downstream tree** for driver availability

## Verified PCAL6524 Ground Truth Pin Map

Complete 24-pin map read directly from schematic page 17 (high-resolution image). Load switch EN paths verified against pages 3 and 20 (U732, U733, U742 detail views).

| DTS GPIO | Chip pin | Net | Direction | DTS usage | Status |
|---|---|---|---|---|---|
| 0 | 1 | TCPC_nINT | in | (unused) | — |
| 1 | 2 | RTC_nINTA | in | PCF2131 RTC IRQ | ✅ |
| 2 | 3 | PCIE_nWAKE * | dual | `reg_vexp_3v3` enable (drives U732 SGM2575 EN via R2888 1K) | ✅ |
| 3 | 4 | UART_nWAKE | in | (unused) | — |
| 4 | 5 | ENET1_nINT | in | (unused) | — |
| 5 | 6 | EXP_BTN1 | in | K2 user button (gpio-keys) | ✅ |
| 6 | 7 | EXP_BTN2 | in | K3 user button (gpio-keys) | ✅ |
| 7 | 8 | DSI_CTP_nINT | in | (unused) | — |
| 8 | 9 | EXP_PWREN | out | `reg_vexp_5v` enable (drives U733 SGM2526 EN via R2892 1K) | ✅ |
| 9 | 10 | ENET2_nINT | in | (unused) | — |
| 10 | 11 | M2_nALERT | in | (unused) | — |
| 11 | 12 | PMIC_nINT | in | PCA9451A PMIC IRQ | ✅ |
| 12 | 13 | SD3_nRST | out | USDHC3 pwrseq reset (WiFi SDIO) | ✅ |
| 13 | 14 | EXT1_PWREN | out | (reserved; U723 MP1605C path is DNP) | — |
| 14 | 15 | EXT2_PWREN | out | U742 SGM2526 EN → VBUS_USB2_5V (`reg_vbus_usb2` in 1156-line DTS) | ✅ renamed |
| 15 | 16 | ENET1_nRST | out | EQOS (ENET1) PHY reset | ✅ |
| 16 | 17 | ENET2_nRST | out | FEC (ENET2) PHY reset | ✅ |
| 17 | 18 | CTP_RST | out | (unused; for DSI touch panel) | — |
| 18 | 19 | M2_nRST | out | (unused) | — |
| 19 | 20 | M2_nDIS2 | out | (unused; M.2 BT disable) | — |
| 20 | 21 | M2_nDIS1 | out | `reg_usdhc3_vmmc` (WLAN_EN) — active-high deassert disable | ✅ |
| 21 | 22 | LVDS_nRST | out | IT6263 LVDS-HDMI bridge reset | ✅ |
| 22 | 23 | CSI_nRST | out | AP1302 ISP reset | ✅ |
| 23 | 24 | CAN_STBY | out | `reg_can2_stby` (TJA1051T/3 standby) | ✅ |

\* GPIO 2 is a **multi-purpose net**. The same physical trace carries M.2 PCIE_nWAKE signal (from M.2 connector) and drives U732 SGM2575 EN pin through R2888 1K populated. When PCAL6524 GPIO 2 is asserted as output, it overrides the M.2 input and enables VEXP_3V3.

## Load Switch → GPIO Cross-Reference

Verified from schematic page 3 (power tree overview) + page 20 (EXPI detail) + U732/U733/U742 detail schematics.

| Load switch | Part | Output rail | EN source | PCAL6524 GPIO | Series R | Notes |
|---|---|---|---|---|---|---|
| U732 | SGM2575 | VEXP_3V3 (EXPI P11 pin 1) | PCIE_nWAKE | **2** | R2888 1K (populated) | R3016 1K on EXP_PWREN path is DNP |
| U733 | SGM2526 | VEXP_5V (EXPI P11 pin 2) | EXP_PWREN | **8** | R2892 1K (populated) | R2894 1K on EXT1_PWREN path is DNP |
| U742 | SGM2526 | VBUS_USB2_5V (USB-A P17) | EXT2_PWREN | **14** | — | User-confirmed |

## Comparison Table

| Category | Function | Target Description | Reference Description | Match Status | Change Type | Action | Evidence |
|---|---|---|---|---|---|---|---|
| **Core System** |
| SoC | Main processor | MIMX9352CVVXMAB (11×11) | Same i.MX93 on SOM | IDENTICAL | No Change | Common DTSI | PDF p.4 |
| Memory | LPDDR4X DRAM | 2GB x16, 0.6V VDDQ | 2GB x16 on SOM | IDENTICAL | No Change | Auto-detected | PDF p.5 |
| Storage | eMMC | 32GB FEMDRM032G-A3A55 (HS400) on USDHC1 | 16GB eMMC on SOM USDHC1 | CHANGED-IC | None | CSD auto-detect | PDF p.8 |
| Storage | MicroSD | MicroSD on USDHC2, CD=GPIO3_00 | MicroSD on BB USDHC2 | MATCH-HW-DTS-ENABLE | DTS | DTS correct | PDF p.20 |
| **Power** |
| PMIC | System power | PCA9451A @ LPI2C2 0x25 | PCA9451A on SOM (PF0900 overlay option on EVK) | MATCH-HW-DTS-ENABLE | DTS | DTS correct | PDF p.10, sch p.22 |
| PMIC IRQ | IRQ routing | PMIC_nINT → PCAL6524 GPIO 11 | Direct to SoC on EVK | CHANGED-WIRING | DTS | DTS correct (`interrupts = <11>`) | sch p.17 |
| Power Tree | Buck/LDO rails | 6 BUCK + 5 LDO per p.3 | Same | IDENTICAL | No Change | — | PDF p.3 |
| P12V Input | Input rail | Always-on from DC jack / USB-C PD via MP8759GD DCDC; no GPIO enable on board | Same | IDENTICAL | No Change | No GPIO regulator needed | PDF p.3 |
| VEXP_3V3 | Expansion 3V3 | U732 SGM2575 EN via R2888 1K ← PCAL6524 GPIO 2 | Similar on EVK | MATCH-HW-DTS-ENABLE | DTS | DTS correct | PDF p.3, p.20, sch p.17 |
| VEXP_5V | Expansion 5V | U733 SGM2526 EN via R2892 1K ← PCAL6524 GPIO 8 | Similar on EVK | MATCH-HW-DTS-ENABLE | DTS | DTS correct | PDF p.3, p.20, sch p.17 |
| VBUS_USB2_5V | USB-A host VBUS | U742 SGM2526 EN ← PCAL6524 GPIO 14 (EXT2_PWREN) | Similar on EVK | MATCH-HW-DTS-ENABLE | DTS rename applied | `reg_vdd_12v` → `reg_vbus_usb2`, voltage 12V → 5V | PDF p.3, p.13, sch p.17 |
| **Ethernet** |
| ENET1 (EQOS) | Gigabit 1 | RTL8211FSI-CG @ MDIO 0x01, RST=PCAL6524 GPIO 15 | RTL8211FDI on EVK BB | CHANGED-PINS | DTS correct | pin 15 ✓ verified | PDF p.14, sch p.17 |
| ENET2 (FEC) | Gigabit 2 | RTL8211FSI-CG @ MDIO 0x02, RST=PCAL6524 GPIO 16 | RTL8211FDI on EVK BB | CHANGED-PINS | DTS correct | pin 16 ✓ verified | PDF p.15, sch p.17 |
| **USB** |
| USB1 | USB Type-C (P1) | USB-C with PTN5110 PD @ LPI2C3 0x50, OTG mode | USB-C on EVK BB | MATCH-HW-DTS-ENABLE | DTS | DTS correct | PDF p.12, sch p.22 |
| USB2 | Type-C P2 + USB-A P17 | Secondary PD @ 0x52 + USB-A host via VBUS_USB2_5V | USB-A on EVK BB | MATCH-HW-DTS-ENABLE | DTS | Add `vbus-supply = <&reg_vbus_usb2>;` to USB2 host node | PDF p.13, p.21 |
| Debug UART-USB | Console bridge | CH342F dual UART-USB on debug Type-C (P16) | Similar on EVK | IDENTICAL | No Change | — | PDF p.21 |
| **Display** |
| LVDS-HDMI Bridge | Primary display | **IT6263 @ LPI2C1 0x4c**, RST=PCAL6524 GPIO 21, fed by LDB | ADV7535 DSI-HDMI on EVK | CHANGED-IC | DTS + Driver | Kernel DTS line 394-405 | PDF p.16, sch p.22 |
| LDB | LVDS block | `&ldb` + `&ldb_phy` single-channel to IT6263 | EVK uses DSI path | ADDED-on-TARGET | DTS | Kernel DTS line 365-383 | PDF p.16 |
| LCDIF | Pixel source | `&lcdif` with clock config feeding LDB | Same on EVK | MATCH-HW-DTS-ENABLE | DTS | Kernel DTS line 355-358 | |
| MIPI DSI | Alt display | Connector P7 for optional panel; not primary | Primary display on EVK | REMOVED-on-TARGET | DTS | Do not enable for main display | PDF p.17, p.2 |
| **Camera** |
| MIPI CSI | Camera pipeline | `&mipi_csi` + `&dphy_rx` from AP1302 via connector P6 | CSI on EVK BB, different sensors | ADDED-on-TARGET | DTS + Driver | Present in Kernel DTS | PDF p.17 |
| AP1302 | ISP | @ LPI2C3 0x3c, reset via ADP5585 | Not on EVK BB | ADDED-on-TARGET | DTS + Driver | Kernel DTS line 491 | PDF p.17, sch p.22 |
| AR0144 | Sensor | CMOS sensor attached to AP1302 | Different sensors on EVK | ADDED-on-TARGET | DTS + Driver | Kernel DTS ~line 530 | PDF p.17 |
| ADP5585 | Camera I/O exp | @ LPI2C3 0x34 (camera-side GPIOs) | Not on EVK BB | ADDED-on-TARGET | DTS | Kernel DTS line 483 | PDF p.22 |
| **Wireless** |
| WiFi/BT Module | Package | **u-blox MAYA-W2** (NXP IW612 / 88W8987 silicon inside), soldered | M.2 KEY-E socket only on EVK | ADDED-on-TARGET | DTS + Driver + FW | Present in Kernel DTS | PDF p.2 block, p.19 title "MAYA-W27x" |
| WiFi | SDIO via USDHC3 | `&usdhc3` with `reg_usdhc3_vmmc` (WLAN_EN) via PCAL6524 GPIO 20 | — | MATCH-HW-DTS-ENABLE | DTS + FW | Kernel DTS line 707 | PDF p.19 |
| BT | UART via LPUART5 | `&lpuart5` with `bluetooth { compatible = "nxp,88w8987-bt"; }` | — | MATCH-HW-DTS-ENABLE | DTS + FW | Kernel DTS line 612-614 | PDF p.19 |
| M.2 KEY-E Socket | Secondary wireless | M.2 slot P8 parallel path for optional module | Same on EVK | IDENTICAL | DTS | Separate from soldered MAYA-W2 | PDF p.18 |
| **CAN** |
| FlexCAN2 | CAN controller | `&flexcan2` + TJA1051T/3 transceiver (U741) | FlexCAN2 on EVK | MATCH-HW-DTS-ENABLE | DTS | Kernel DTS line 253 | PDF p.21 |
| CAN_STBY | Transceiver standby | PCAL6524 GPIO 23 (CAN_STBY net) | Similar | MATCH-HW-DTS-ENABLE | DTS | `reg_can2_stby` correct | sch p.17 |
| **Audio** |
| MQS | Audio DAC | `&mqs1` → 3.5mm jack (P15), CPU DAI = SAI1 | MQS on EVK | MATCH-HW-DTS-ENABLE | DTS | Kernel DTS line 208 / 621 | PDF p.20 |
| SAI1 | I2S (MQS CPU) | `&sai1` bound to MQS | SAI1 on EVK | MATCH-HW-DTS-ENABLE | DTS | Kernel DTS line 629 | |
| SAI3 | I2S (expansion) | On EXPI 40-pin header | SAI3 on EVK | MATCH-HW-DTS-ENABLE | DTS (optional) | Not added to Kernel DTS; only needed for audio HAT | PDF p.2, p.20 |
| PDM Mics | PDM input | On block diagram, component population unverified | PDM on EVK BB | NEEDS-REVIEW | DTS | Verify population before adding | PDF p.2 |
| **Debug/RTC** |
| LPUART1 | Console | Via CH342F on debug USB | Same | MATCH-HW-DTS-ENABLE | DTS | DTS correct | PDF p.21 |
| LPUART5 | Bluetooth UART | Dedicated to IW612 BT (role differs from EVK expansion use) | Expansion on EVK | MATCH-HW-DTS-ENABLE | DTS | Kernel DTS line 605-614 | PDF p.19 |
| SWD/JTAG | Debug interface | Header P14 | Same | IDENTICAL | No Change | — | PDF p.20 |
| RTC | Real-time clock | PCF2131 @ LPI2C3 0x53, IRQ → PCAL6524 GPIO 1 | PCF2131 on EVK 0x53 | MATCH-HW-DTS-ENABLE | DTS | DTS correct | PDF p.21, sch p.22 |
| Coin cell | RTC backup | Rechargeable cell + charge circuit (P18) | Same | IDENTICAL | No Change | — | PDF p.21 |
| **GPIO/Expansion** |
| GPIO Exp 1 | Main I/O | PCAL6524 @ LPI2C2 0x22, IRQ → GPIO3_27 | PCAL6524 on EVK BB at 0x22 | MATCH-HW-DTS-ENABLE | DTS | DTS correct | PDF p.22 |
| GPIO Exp 2 | M.2 support | PCAL6408 @ LPI2C1 0x20 | Not on EVK BB | ADDED-on-TARGET | DTS | Kernel DTS line 407 | PDF p.19, p.22 |
| GPIO Exp 3 | Camera I/O | ADP5585 @ LPI2C3 0x34 | Not on EVK BB | ADDED-on-TARGET | DTS | Kernel DTS line 483 | PDF p.22 |
| EEPROM | Board ID | AT24C256D @ LPI2C2 0x50 | EEPROM on SOM | MATCH-HW-DTS-ENABLE | DTS | Present in U-Boot DTS; **added to Kernel DTS (1156-line)** | PDF p.6, p.22 |
| **UI** |
| RGB LED | Status | 3× PWM via TPM3 CH0, TPM3 CH2, TPM4 CH2 | GPIO LEDs on EVK | CHANGED-INTF | DTS | TPMs enabled; **`pwm-leds` consumer node added (1156-line)** | PDF p.11 |
| K2 / K3 buttons | User input | PCAL6524 GPIO 5/6 (EXP_BTN1/BTN2) via gpio-keys | Buttons on EVK | MATCH-HW-DTS-ENABLE | DTS | Kernel DTS line 216-234 | PDF p.11, sch p.17 |
| K1 ONOFF | Power button | Direct to SoC ONOFF pin | Same | IDENTICAL | No Change | SoC handles | PDF p.11 |
| **ADC/Expansion** |
| ADC | Analog input | ADC1 to EXP GPIO P12, VREF=1.8V | ADC on EVK | MATCH-HW-DTS-ENABLE | DTS | U-Boot DTS line 112 | PDF p.20 |
| Board ID | Version detect | Vn.x / Vx.n resistor dividers into ADC2/3 | Same | IDENTICAL | No Change | Software reads at boot | PDF p.9 |
| EXPI Header | 40-pin expansion | UART/I2C/SPI/GPIO + lcdif alt on P11 | Same | MATCH-HW-DTS-ENABLE | DTS | Regulators present | PDF p.20 |

## Summary Statistics

**Match Status Breakdown**
- **IDENTICAL**: 9 (SoC, DRAM, Power tree, P12V, Debug USB, SWD, Coin cell, K1 ONOFF, Board ID divider)
- **MATCH-HW-DTS-ENABLE**: 17
- **CHANGED-IC**: 2 (eMMC capacity, display bridge)
- **CHANGED-PINS**: 2 (ENET1/ENET2 reset — DTS is correct, just different from EVK)
- **CHANGED-WIRING**: 1 (PMIC IRQ routed via PCAL6524)
- **CHANGED-INTF**: 1 (RGB LED uses PWM, not GPIO)
- **ADDED-on-TARGET**: 5 (LDB, MIPI CSI+ISP, MAYA-W2/IW612, PCAL6408, ADP5585)
- **REMOVED-on-TARGET**: 1 (MIPI DSI as primary display)
- **NEEDS-REVIEW**: 1 (PDM mic population)
- **NEEDS-DTS-FIX**: 0 (all DTS items corrected in 1156-line Kernel DTS)

## DTS Changes Applied

### Kernel DTS (1111 → 1156 lines, 3 edits)

1. `reg_vdd_12v` → `reg_vbus_usb2`, voltage 12V → 5V (fixes misnamed regulator on GPIO 14 = EXT2_PWREN driving U742 USB-A VBUS)
2. `pwm-leds` consumer node added (TPM3/TPM4 PWMs were previously enabled but no LED consumer existed)
3. AT24 EEPROM node added to `&lpi2c2` (syncs with U-Boot DTS)

### U-Boot DTS (643 → 645 lines, 4 edits)

1. Include path: `<../../../dts/upstream/src/arm64/freescale/imx93.dtsi>` → `"imx93.dtsi"`
2. Compatible: `"fsl,imx93-11x11-frdm"` → `"fsl,frdm-imx93"` (matches Kernel)
3. EQOS `reset-gpios`: pin 4 → pin 15 (was ENET1_nINT input, now ENET1_nRST output)
4. FEC `reset-gpios`: pin 9 → pin 16 (was ENET2_nINT input, now ENET2_nRST output)

## Correction Log (vs v2 of this table)

| v2 claim | Corrected (FINAL) | Why |
|---|---|---|
| "ENET1 reset should be pin 16, DTS wrong" | GPIO 15 (DTS correct all along) | Schematic p.17 hi-res: R2766 on chip pin 16 = P1_6 = DTS GPIO 15 = ENET1_nRST |
| "ENET2 reset pin unknown" | GPIO 16 (DTS correct) | Schematic: R2770 on chip pin 17 = P2_0 = DTS GPIO 16 = ENET2_nRST |
| "`reg_vdd_12v` on pin 14 = EXT1_PWREN — DTS IS WRONG" | GPIO 14 = EXT2_PWREN driving U742 VBUS_USB2_5V; functional, misnamed only (renamed in 1156-line DTS) | U742 schematic detail + user confirmation |
| "K2/K3 on pin 5/6 almost certainly wrong" | GPIO 5/6 = EXP_BTN1 / EXP_BTN2 (DTS correct) | Schematic p.17 hi-res verifies EXP_BTN1/2 labels |
| "PMIC IRQ pin 11 = M2_nALERT, wrong" | GPIO 11 = PMIC_nINT (DTS correct) | Schematic p.17 hi-res + DTS `interrupts = <11>` match |
| "MAYA-W2 module form unverified" | Confirmed MAYA-W2 | PDF p.2 block diagram + p.19 title "MAYA-W27x" |
| "AR1335 missing from Kernel DTS" | AR1335 is not on FRDM | No evidence in schematic or block diagram; FRDM only supports AR0144 via AP1302 |
| "`usdhc3_pwrseq` reset on pin 12 = EXT1_PWREN, wrong" | GPIO 12 = SD3_nRST (DTS correct) | Schematic p.17 hi-res |
| "Critical Items Still Wrong: 4" | Only 1 cosmetic rename needed | All PHY resets, buttons, usdhc3_pwrseq verified correct |
| "Items Missing: 4 (SAI3, pwm-leds, EEPROM, AR1335)" | Missing: 1 optional (SAI3 only if audio HAT) | pwm-leds and EEPROM added in 1156-line; AR1335 not applicable |

**Root cause of v2 errors**: v2 worked from partial text OCR of schematic page 17, which missed several rows and misaligned pin numbers. FINAL is based on the high-resolution image of page 17 (all 24 pins readable) plus U732/U733/U742 load-switch detail views. Every pin claim in the ground truth table has a direct visual source.

## Next Steps (BSP Delivery)

DTS side is complete. Remaining items are build artifacts (review §5):

1. **U-Boot defconfig**: `configs/imx93_11x11_frdm_defconfig` (from `imx93_11x11_evk_defconfig`, change default DT, verify PMIC = PCA9451A)
2. **Kernel Makefile**: add `dtb-$(CONFIG_ARCH_MXC) += imx93-11x11-frdm.dtb` to `arch/arm64/boot/dts/freescale/Makefile`
3. **U-Boot board directory**: `board/freescale/imx93_11x11_frdm/` with `imx93_11x11_frdm.c`, `imximage.cfg`, `Kconfig`, `Makefile`, `MAINTAINERS`
4. **U-Boot arch Kconfig + Makefile** in `arch/arm/mach-imx/imx9/`
5. **Boot verification**:
   - `ip link` shows eth0 (EQOS) + eth1 (FEC)
   - Both PHYs link up: `ethtool eth0 && ethtool eth1`
   - `i2cdetect` shows all expected devices
   - MicroSD mounts
   - USB-A (P17) enumerates devices (requires `reg_vbus_usb2` wired to USB2 host)
   - HDMI via IT6263: `modetest -M imx-drm -s <conn>:1920x1080`

## Methodology Notes

- **Target-first**: Built from FRDM schematic as primary ground truth; EVK comparison is secondary.
- **Silicon vs module**: WiFi/BT records both silicon (IW612 / 88W8987) and module form (MAYA-W2), both verified.
- **Traceability**: Every row cites schematic page or DTS line. No claim is based on net-name inference alone — pin directions and assignments come from visible series/pull resistors and populated/DNP markings.
- **Symptom of past errors**: Earlier versions repeatedly inverted ENET pin assignments because net names (e.g., "PCIE_nWAKE") implied input direction while the physical network actually drove an output via populated series resistors. Only the full pin-level schematic view resolved this reliably.
