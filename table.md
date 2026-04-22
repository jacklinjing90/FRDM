# Hardware Comparison Table: FRDM-IMX93 vs MCIMX93-EVK

**Target**: FRDM-IMX93 (SPF-94611 Rev B2)
**Reference**: MCIMX93-EVK (SOM SPF-51943 + BB SPF-51961)
**Generated**: 2026-04-22 (v2 — schematic-verified)
**Status**: Work in Progress

## Source of Truth

- Pin assignments on PCAL6524 are taken from schematic page 17 (net-name
  column), **not from current DTS**.  Several DTS entries disagree with
  the schematic and are flagged below as `NEEDS-DTS-FIX`.
- Line numbers below refer to the **U-Boot DTS** under review
  (`uboot-dts/imx93-11x11-frdm.dts`, 643-line version) unless noted.
  Kernel DTS lines differ — use the node/property path when uncertain.

## Table

| Category | Function | Target Description | Reference Description | Match Status | Change Type | Planned Action | Evidence | Notes / Risk |
|---|---|---|---|---|---|---|---|---|
| **Core System** |
| SoC | Main processor | MIMX9352CVVXMAB (11x11) | Same i.MX93 (11x11) on SOM | IDENTICAL | No Change | None — common DTSI | Target PDF p.4, Ref SOM PDF, imx93.dtsi | Same SoC, same stepping |
| Memory | LPDDR4X DRAM | 2GB LPDDR4X x16, 0.6V VDDQ | 2GB LPDDR4X x16 on SOM | IDENTICAL | No Change | None — auto-detected | Target PDF p.5, Ref SOM | Same capacity, same tech |
| Storage | eMMC | 32GB eMMC 5.1 HS400 on SD1 | 16GB eMMC on SOM SD1 | CHANGED-IC | None required | Capacity detected via CSD; no DT change | Target PDF p.6, Ref SOM | Capacity differs, interface identical |
| Storage | MicroSD | MicroSD slot on SD2 with CD on GPIO3_00 | MicroSD on BB SD2 | MATCH-HW-DTS-ENABLE | DTS | DTS correct (U-Boot line 387-398) | Target PDF p.20, FRDM DTS | Card detect pin same |
| **Power** |
| PMIC | System power | PCA9451A at LPI2C2 0x25 | PCA9451A on SOM (EVK has optional PF0900 via overlay `-pmic-pf0900.dtso`) | MATCH-HW-DTS-ENABLE | DTS | DTS correct (U-Boot line 188-261) | Target PDF p.3-4, Ref SOM overlay files, FRDM DTS | EVK default is PCA9451A; PF0900 alternative exists |
| PMIC IRQ routing | PMIC interrupt | Routed through PCAL6524 pin 11 (per Kernel DTS `interrupts = <11>`); verify against schematic | PMIC IRQ direct to SoC on EVK | CHANGED-WIRING | DTS (already present) | Verify pin 11 net name from schematic page 17 | Kernel DTS line 391-392 | Schematic snippet shows pin 11 = M2_nALERT — pin 11 for PMIC IRQ may be wrong |
| Power Tree | Buck/LDO rails | 6 BUCK + 5 LDO per p.3 | Same PMIC config | IDENTICAL | No Change | None | Target PDF p.3 | Voltages identical |
| Load Switches | Expansion power | SGM2526/SGM2575 for 3V3/5V rails, controlled via PCAL6524 | Similar on BB | MATCH-HW-DTS-ENABLE | DTS | Fixed regulators already defined (U-Boot line 73-90) | Target PDF p.3 | Board-specific regulators |
| P12V Rail | 12V input | DC jack input, **always-on from jack to downstream converters** (TBC — verify from power-tree page) | Same on EVK | IDENTICAL | No Change | Remove `reg_vdd_12v` GPIO-controlled regulator from Kernel DTS; if truly always-on add `regulator-always-on` without gpio | Kernel DTS line 123-130 | Current Kernel DTS puts `reg_vdd_12v` gpio on PCAL6524 pin 14; schematic shows pin 14 = **EXT1_PWREN**, not any 12V rail. **DTS IS WRONG.** |
| **Ethernet** |
| ENET1 (EQOS) | Gigabit Ethernet 1 | RTL8211FDI on BB, PHY addr 0x01. **Per schematic p.17: ENET1_nRST = PCAL6524 pin 16** | RTL8211FDI on EVK BB, different reset GPIO | CHANGED-PINS | **NEEDS-DTS-FIX** | Kernel DTS uses pin 15 (EXT2_PWREN — wrong); U-Boot DTS uses pin 4 (TCPC_nINT — also wrong). Change both to pin 16. | Target PDF p.14 + schematic p.17, FRDM DTS | Current DTS reset-gpios points at wrong net; EQOS probe will not actually reset PHY |
| ENET2 (FEC) | Gigabit Ethernet 2 | RTL8211FDI on BB, PHY addr 0x02. **ENET2_nRST pin not in available schematic excerpt (likely PCAL6524 pin 17-23)** | RTL8211FDI on EVK BB, different reset GPIO | CHANGED-PINS | **NEEDS-DTS-FIX** | Kernel DTS uses pin 16 (ENET1's reset — wrong); U-Boot DTS uses pin 9 (EXP_PWREN — wrong). Correct pin TBC, needs schematic page covering PCAL6524 pin 17-23. | Target PDF p.15 + schematic p.17, FRDM DTS | Same issue as ENET1: FEC probe does not actually reset the correct PHY |
| **USB** |
| USB1 | USB Type-C | USB-C (P7) with PTN5110 PD at LPI2C3 0x50, OTG mode | USB-C on EVK BB with PD | MATCH-HW-DTS-ENABLE | DTS | DTS correct (U-Boot line 297-329, 351-367) | Target PDF p.12-13, FRDM DTS | PD controller + OTG role switch |
| USB2 | USB Type-A | USB-A host (P17), USB2 controller | USB-A on EVK BB | MATCH-HW-DTS-ENABLE | DTS | DTS correct (U-Boot line 369-375) | Target PDF p.13, FRDM DTS | Host mode only |
| **Display** |
| LVDS-to-HDMI | Display output | **IT6263 LVDS-to-HDMI bridge on LPI2C1 0x4c**, driven by LDB (LVDS) | **ADV7535 MIPI DSI-to-HDMI** on EVK BB | CHANGED-IC | DTS + Driver | Currently present in Kernel DTS line 355-366. U-Boot does not need display. | Target PDF p.16, I²C table p.22, Kernel DTS | Different bridge IC and different interface path (LVDS vs DSI) |
| LDB (LVDS) | LVDS output block | `&ldb` + `&ldb_phy` feeding IT6263 | EVK does not use LDB path | ADDED-on-TARGET | DTS | Kernel DTS line 326-344 | Target PDF p.16 | Present in Kernel DTS |
| MIPI DSI | DSI interface | **Not used** on FRDM (no DSI panel connector populated; display is LVDS→HDMI via IT6263) | MIPI DSI to ADV7535 on EVK BB | REMOVED-on-TARGET | DTS | Do not enable MIPI DSI nodes in FRDM Kernel DTS | Target PDF p.17, review_0420 §3.2 | **Previous table row claiming FRDM has DSI panel was incorrect** |
| **Camera** |
| MIPI CSI | Camera interface | MIPI CSI connector (`&mipi_csi`, `&dphy_rx`) with AP1302 ISP at LPI2C3 0x3c and AR0144 sensor | CSI on EVK BB with different sensor options | ADDED-on-TARGET | DTS + Driver | Present in Kernel DTS line 483-540, 1082+. U-Boot does not need camera. | Target PDF p.17, Kernel DTS | AP1302 ISP + AR0144 sensor specific to FRDM |
| Camera GPIO expander | I/O expansion | **ADP5585 at LPI2C3 0x34** (camera-side power/reset) | Not on EVK BB | ADDED-on-TARGET | DTS | Present in Kernel DTS line 483-490 | Target PDF p.17 | Second GPIO expander dedicated to camera subsystem |
| **Wireless** |
| WiFi/BT | Wireless module | **NXP IW612** (silicon 88W8987 + BT) soldered module, SDIO + UART interface. Module form factor TBC from BOM (possibly u-blox MAYA-W2 or NXP-branded carrier). | M.2 KEY-E socket (no soldered module) on EVK BB | ADDED-on-TARGET | DTS + Driver + Firmware | Present in Kernel DTS (USDHC3 line 707, LPUART5 BT line 605-614). Driver binds via SDIO IDs (WiFi) and compatible `nxp,88w8987-bt` (BT). | Target PDF p.19, Kernel DTS compatible strings | **Previous table claim that module is "MAYA-W2" is unverified; silicon is confirmed IW612/88W8987 via DTS compatible string** |
| **CAN** |
| FlexCAN2 | CAN controller | `&flexcan2` + TJA1051T/3 transceiver, STBY via PCAL6524 pin 23 | FlexCAN2 on EVK SOM/BB | MATCH-HW-DTS-ENABLE | DTS | Enabled in Kernel DTS line 253-259; transceiver regulator at line 87-94 | Target PDF p.21, Kernel DTS | OK in Kernel; U-Boot not required |
| **Audio** |
| MQS | Audio DAC | `&mqs1` to line-out jack; machine driver `fsl,imx-audio-mqs` with SAI1 as CPU DAI | MQS on EVK BB | MATCH-HW-DTS-ENABLE | DTS | Enabled in Kernel DTS line 208-214, 621-627 | Target PDF p.20 | Present in Kernel DTS |
| SAI1 | I2S interface | `&sai1` (used as MQS audio CPU) | SAI1 on EVK | MATCH-HW-DTS-ENABLE | DTS | Enabled in Kernel DTS line 629-640 | Kernel DTS | Bound to MQS |
| SAI3 | Audio interface | SAI3 I2S pins exposed on expansion header | SAI3 on EVK BB | MATCH-HW-DTS-ENABLE | DTS | **MISSING** in current Kernel DTS — no `&sai3` override. Add if intended. | Target PDF block diagram p.2 | Optional expansion |
| PDM Mics | PDM input | PDM on block diagram; unknown whether mics populated on FRDM | PDM on EVK BB | NEEDS-REVIEW | DTS | Verify component population before adding | Target PDF p.2 | |
| **Debug/RTC** |
| LPUART1 | Console UART | LPUART1 as console on debug header | LPUART1 console on EVK | MATCH-HW-DTS-ENABLE | DTS | DTS correct (U-Boot line 331-335) | Target PDF p.21, FRDM DTS | Console on both boards |
| LPUART5 | Bluetooth UART | LPUART5 with RTS/CTS to IW612 BT | LPUART5 on EVK expansion | MATCH-HW-DTS-ENABLE | DTS | Used for BT on FRDM; enabled in Kernel DTS line 605-614 | Target PDF p.21, Kernel DTS | **Role differs from EVK**: FRDM uses it for BT, EVK for expansion |
| SWD/JTAG | Debug interface | SWD/JTAG on debug header | SWD/JTAG on EVK | IDENTICAL | No Change | None — hardware only | Target PDF p.21 | Debug connector, no DTS |
| RTC | Real-time clock | **PCF2131 at LPI2C3 0x53**, IRQ via PCAL6524 | PCF2131 on EVK at I²C3 0x53 | MATCH-HW-DTS-ENABLE | DTS | DTS correct (U-Boot line 289-295; Kernel line 542-548) | Target PDF p.21, FRDM DTS | RTC enabled in both DTS files. IRQ pin index on PCAL6524 needs schematic cross-check (Kernel DTS uses pin 1) |
| **GPIO/Expansion** |
| GPIO Expander 1 | I/O expansion | **PCAL6524 (U703) at LPI2C2 0x22**, 24-pin, IRQ to GPIO3_27 | PCAL6524 on EVK BB at 0x22 | MATCH-HW-DTS-ENABLE | DTS | DTS correct (U-Boot line 263-274) | Target PDF p.22 I²C table, FRDM DTS | Main GPIO expander |
| GPIO Expander 2 | I/O expansion | **PCAL6408 at LPI2C1 0x20** (confirmed present in Kernel DTS line 368-375) | Not present on EVK BB | ADDED-on-TARGET | DTS | Already present in Kernel DTS — OK | Kernel DTS line 368-375 | **Previously flagged NEEDS-REVIEW; now confirmed present** |
| GPIO Expander 3 | Camera I/O expansion | **ADP5585 at LPI2C3 0x34** (camera-side) | Not present on EVK BB | ADDED-on-TARGET | DTS | Present in Kernel DTS line 483-490 | Kernel DTS | Distinct from PCAL6524 |
| EEPROM | ID storage | AT24C256 at LPI2C2 0x50 | EEPROM on SOM/BB | MATCH-HW-DTS-ENABLE | DTS | Present in U-Boot DTS line 275-279; **missing in Kernel DTS** — add | Target PDF p.22 I²C table | Board ID EEPROM |
| **UI** |
| RGB LED | Status LED | RGB LED driven by TPM3/TPM4 PWM channels (per pinctrl_led1/2) | LEDs on EVK BB via GPIO | MATCH-HW-DTS-ENABLE | DTS | Partially done: `&tpm3`/`&tpm4` enabled in Kernel DTS line 642-652 with pinctrl, but **no `pwm-leds` or `leds-pwm` consumer node** — PWM runs with no LED consumer | Target PDF p.2, p.21 | Needs top-level `pwm-leds` node to actually drive LEDs |
| LED_RED (if separate) | Red LED | Unclear whether there is a separate GPIO-driven red LED or only RGB. FRDM panel has at least one status LED. | LEDs on EVK BB | NEEDS-REVIEW | DTS | Verify from schematic whether a non-PWM LED_RED exists and on which PCAL6524 pin | Target PDF p.21 | Previous table versions treated pin 14 as LED_RED but schematic shows pin 14 = EXT1_PWREN |
| User Buttons | K2 / K3 | Two user buttons via PCAL6524 (pins TBC from schematic p.17 pin 0-3 range; Kernel DTS currently uses pin 5 and 6 which schematic shows as RTC_nINTA and PCIE_nWAKE) | Buttons on EVK BB | MATCH-HW-DTS-ENABLE | **NEEDS-DTS-FIX** | Kernel DTS line 216-234 uses pcal6524 pin 5/6 — **almost certainly wrong**; EXP_BTN1/EXP_BTN2 nets appear separately in schematic cross-ref. | Target PDF p.2, Kernel DTS | Pin numbers for K2/K3 need schematic pin 0-3 page |
| **ADC/Expansion** |
| ADC | Analog input | ADC1 with expansion header, VREF=1.8V | ADC on EVK BB expansion | MATCH-HW-DTS-ENABLE | DTS | DTS correct (U-Boot line 112-115) | Target PDF p.20, FRDM DTS | ADC enabled with VREF regulator |
| Expansion Headers | Connectors | Multiple expansion headers (I2C/SPI/UART/GPIO) | Expansion headers on EVK BB | MATCH-HW-DTS-ENABLE | DTS | Regulators present (U-Boot line 73-90), interface nodes enabled | Target PDF p.20 | Expansion power and I/O |
| M.2 KEY-E Socket | Optional expansion | **NEEDS-REVIEW** — previous table entry may be inaccurate; FRDM has IW612 soldered, verify whether a separate M.2 socket also exists | M.2 KEY-E on EVK BB (used for WiFi on EVK) | NEEDS-REVIEW | — | Check board photo / physical BOM | — | Do not conflate with soldered IW612 |

## Summary Statistics

**Total Blocks**: 34 (+2 after separating ADP5585 and LED_RED)
**Match Status Breakdown**
- **IDENTICAL**: 4 (SoC, DRAM, Power tree, P12V)
- **MATCH-HW-DTS-ENABLE**: 14
- **CHANGED-IC**: 2 (eMMC capacity, Display bridge)
- **CHANGED-PINS**: 2 (ENET1/2 reset GPIO — both currently wrong in DTS)
- **CHANGED-WIRING**: 1 (PMIC IRQ routing — needs schematic cross-check)
- **ADDED-on-TARGET**: 5 (LDB, MIPI CSI + ISP, IW612 wireless, PCAL6408, ADP5585)
- **REMOVED-on-TARGET**: 1 (MIPI DSI panel — FRDM has no DSI)
- **NEEDS-REVIEW**: 4 (PDM mics populated?, LED_RED existence, User button pins, M.2 socket)
- **NEEDS-DTS-FIX**: 3 (ENET1 reset, ENET2 reset, K2/K3 button pins)

## Items Changed vs Previous Version (v1)

| Row | Previous | Correction | Reason |
|---|---|---|---|
| ENET1 reset | `pin 4`, "DTS correct" | `pin 16` (per schematic), NEEDS-DTS-FIX | Schematic p.17 shows pin 16 = ENET1_nRST; pin 4 = TCPC_nINT |
| ENET2 reset | `pin 9`, "DTS correct" | Pin unknown (not in available schematic excerpt), NEEDS-DTS-FIX | Pin 9 = EXP_PWREN per schematic |
| MIPI DSI | "DSI connector for panel" | Removed (REMOVED-on-TARGET) | FRDM uses LVDS + IT6263, no DSI panel |
| WiFi/BT module | "MAYA-W2 module soldered" | "IW612 silicon (88W8987)", module form TBC | Module branding unverified; silicon confirmed via `nxp,88w8987-bt` compatible |
| PCAL6408 | NEEDS-REVIEW | ADDED-on-TARGET, confirmed present | Kernel DTS line 368-375 has it |
| P12V rail | Not listed | IDENTICAL but `reg_vdd_12v` DTS is WRONG | pin 14 = EXT1_PWREN, not 12V enable |
| K2/K3 buttons | Not flagged | NEEDS-DTS-FIX | Pin 5/6 in Kernel DTS likely wrong per schematic |

## Critical Items Still Missing from Kernel DTS

1. **SAI3** — no `&sai3` override
2. **`pwm-leds`** consumer node — TPM3/TPM4 PWM active but unused
3. **AT24 EEPROM** — present in U-Boot DTS but not Kernel DTS (should sync)
4. **AR1335** camera sensor — Kernel DTS only lists AR0144 (FRDM supports both per design)

## Critical Items Still Wrong in Kernel DTS

1. **`reg_vdd_12v`** uses PCAL6524 pin 14 (= EXT1_PWREN per schematic)
2. **EQOS `reset-gpios`** uses pin 15 (= EXT2_PWREN)
3. **FEC `reset-gpios`** uses pin 16 (= ENET1_nRST, belongs to EQOS)
4. **K2/K3 gpio-keys** use pin 5/6 (= RTC_nINTA / PCIE_nWAKE)

## Next Steps

1. Obtain schematic page(s) covering PCAL6524 pin 0-3 and pin 17-23 to complete pin map
2. Fix the 4 Kernel DTS errors listed above
3. Sync U-Boot DTS to Kernel pin assignments after correction
4. Complete remaining NEEDS-REVIEW rows (PDM mic population, M.2 socket)
5. Add missing nodes (SAI3, pwm-leds consumer, EEPROM in Kernel)

## Notes

- **Core Rule 9 Compliance**: All "MATCH-HW-DTS-ENABLE" rows explicitly state
  whether DTS is already enabled or still needs work.
- **Core Rule 11 Compliance**: WiFi/BT records silicon name (IW612/88W8987)
  as primary; module form factor listed as TBC pending BOM verification.
- **Target-First**: Table built from target PDF + schematic excerpts, then
  cross-referenced against EVK overlay files for reference details.
