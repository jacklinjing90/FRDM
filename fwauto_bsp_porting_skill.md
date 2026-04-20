# BSP Porting Skill for FWAuto

## Skill Name
BSP Porting, EVK-vs-Target Hardware Analysis, DTS Consistency Validation, Driver/Config Review, and Build Preparation

## Purpose
This skill guides FWAuto through a safe, traceable BSP porting workflow when the user provides a repository containing:

1. Target board hardware documents (preferably PDF)
2. Reference board hardware documents (preferably PDF)
3. Linux kernel source
4. U-Boot source

The goal is to:
- identify the exact **target board** and **reference board**,
- compare **reference board vs target board hardware differences** explicitly,
- locate or derive the target DTS files,
- determine which differences belong in **Linux DTS**, **U-Boot DTS**, **driver code**, **defconfig/Kconfig**, or **firmware/configuration**,
- verify that Linux and U-Boot descriptions are **internally consistent for the same board**,
- build Linux and U-Boot DTBs,
- validate the generated DTBs by reverse decompilation,
- validate that the comparison table is supported by both PDF evidence and implemented DTS content,
- and produce a reproducible build procedure.

If requested by the task, this skill must also generate `build-frdm.sh` as the main FWAuto build entrypoint for Linux kernel and U-Boot.

---

## Scope
Use this skill when the task involves:
- BSP porting
- board bring-up preparation
- target board DTS creation or modification
- Linux kernel DTB build
- U-Boot DTB build
- EVK/reference-board to target-board migration
- identifying whether board differences require DTS, driver, config, or firmware changes

Do **not** use this skill for:
- unrelated driver development
- application-level software build tasks
- hardware flashing steps when no hardware access is available

---

## Core Rules

1. **Preserve original sources.**
   - Never modify originally provided vendor DTS files in place.
   - Always create working copies before editing.

2. **Hardware PDF/schematic is the source of truth.**
   - Do not rely only on existing DTS files.
   - Use PDFs, schematics, notes, footnotes, annotations, and reference designators as primary evidence.

3. **Build success does not prove hardware correctness.**
   - A successful DTB build only proves syntax and partial integration correctness.
   - Final validation still requires PDF evidence, decompiled DTB review, and Linux-vs-U-Boot consistency checks.

4. **The main comparison must be reference board vs target board hardware.**
   - `table.md` must not be replaced by a target-PDF-vs-target-DTS self-check.

5. **Do not classify hardware as missing without strong evidence.**
   - Before marking a block as `Missing in Target`, search exact name, alternate name, reference designator, function name, notes, and annotations.
   - If evidence is incomplete or conflicting, use `Unknown` or `Needs Review`.

6. **Always analyze DTS, driver, config, and firmware impact separately.**
   - Do not stop at “DTS generated”.
   - The result must explicitly state whether driver/config/firmware changes are required, not required, or still unverified.

7. **Always validate via decompiled DTB and report reconciliation.**
   - After building DTBs, decompile them.
   - Cross-check `table.md`, DTS implementation, PDF evidence, and driver/config reports.
   - If a mismatch is found, update the reports instead of ignoring it.

8. **Never use `sudo` to install dependencies.**
   - If a tool is missing, list the exact dependency and let the user install it manually.

---

## Required Repository Inputs
The user-provided repository should contain or make accessible the following:

- Target board hardware document(s), preferably PDF
- Reference board hardware document(s), preferably PDF
- Linux kernel source tree
- U-Boot source tree

Optional but useful:
- Existing board DTS/DTSI files
- Build scripts
- Toolchain notes
- Vendor SDK instructions
- Defconfig files
- Board README or release notes
- Firmware blobs / firmware loading notes

---

## Expected Output
By the end of this skill, FWAuto should produce:

### Mandatory Outputs
1. A working copy of target DTS files for Linux and U-Boot
2. An explicit **reference-vs-target hardware comparison table** in `table.md`
3. A **Linux-vs-U-Boot consistency report** in `consistency_check.md`
4. A **driver/config/firmware change list**
5. Built DTB outputs for Linux and U-Boot
6. Decompiled validation DTS files:
   - `project/validation/linux.dts`
   - `project/validation/uboot.dts`
   - `project/validation/spl.dts` (if SPL is built and available)
7. A list of required tools/software in `dependency_list.md`
8. Reproducible build commands in `build_commands.md`
9. A clear conclusion stating:
   - whether reference-vs-target board differences were covered,
   - whether Linux and U-Boot descriptions are consistent,
   - whether driver/config changes are still required,
   - whether the DTBs are ready for the next BSP stage.
10. A separate grouped summary in `hardware_diff.md` if `table.md` does not already have good category grouping
11. A generated build script (e.g., `build-frdm.sh`) as main build entrypoint
12. Updated FWAuto command configuration to run the build script

---

## Directory and File Conventions
Use the following output locations:

Create these directories and files under `project/`:

project/
  validation/
    linux.dts
    uboot.dts
    spl.dts                    # Optional if SPL DTB exists
  reports/
    table.md
    driver_change_list.md
    config_change_list.md
    build_commands.md
    dependency_list.md
    hardware_diff.md           # Optional when table.md lacks grouping
    FINAL_SUMMARY.md           # Optional but recommended
  work/
    linux-dts/
    uboot-dts/

If these folders do not exist, create them in the working area without altering original source files.

---

## Mandatory PDF Evidence Rule

When comparing hardware from PDFs, classify target-side presence as:
- `Present`
- `Not Present`
- `Needs Review`

Before marking hardware as missing, or before removing an inherited DTS node, perform:
1. exact-name search
2. alternate-name / alias search
3. reference-designator search
4. function-level search
5. note / footnote / errata / annotation check
6. simple connection sanity check

Decision rule:
- explicitly shown and used -> `Present`
- explicitly absent / not populated -> `Not Present`
- partial, inferred, or conflicting evidence -> `Needs Review`

Do **not** conclude `Missing in Target` from first-pass non-detection alone.

### Special Rule for Optional / Pluggable Hardware
For hardware such as M.2 modules, camera modules, bridge boards, and expansion cards, compare these separately:
1. connector / interface presence
2. populated module presence
3. functional capability
Do not collapse them into one row.

---

## Evidence Recording Rule for `table.md`
Every table row must include explicit evidence.

Each row must include at least one of the following:
- target PDF page number and keyword/net/reference-designator note,
- reference PDF page number and keyword/net/reference-designator note,
- DTS path / source file path,
- header file path such as `imx93-pinfunc.h`,
- driver file path when the row involves software impact.

Do **not** write `Different`, `Missing in Target`, or `No Change` without showing what evidence supports that statement.

If later validation shows the evidence is wrong or incomplete, update `table.md` and all dependent reports.

---

## Step-by-Step Procedure

### Step 1: Inspect Repository Contents
Confirm the repository includes:
- target board PDF document(s),
- reference board PDF document(s),
- Linux kernel source,
- U-Boot source.

Actions:
1. Search for PDF files related to target and reference boards.
2. Identify likely Linux kernel root.
3. Identify likely U-Boot root.
4. Record important file paths.

If any required input is missing:
- stop the porting flow,
- report exactly what is missing,
- ask the user to provide it.

---

### Step 2: Identify Target and Reference Board Names
Extract the target and reference SoC/board names from:
- hardware PDFs,
- directory names,
- DTS filenames,
- user-provided metadata.

Actions:
1. Determine the exact target board name.
2. Determine the exact reference board name.
3. Determine whether the reference is at SoC level, EVK level, or board level.
4. Use those names to search for DTS/DTSI files in Linux and U-Boot.

Typical search targets include:
- `arch/*/boot/dts/` in Linux
- `arch/*/dts/` in U-Boot

Requirements:
- The **reference board DTS must be found** in Linux and/or U-Boot as needed for porting.
- The **target board DTS may be missing**.

Document all findings before proceeding.

---



---

### Step 3: Build the Main Hardware Difference Table (Reference vs Target)
This is the primary analysis stage.
Create a comparison table in Markdown format and save it as:

```text
/project/reports/table.md
```

Read the target and reference hardware PDF documents and compare all relevant hardware blocks and board-level differences.
one hardware item at a time, read PDF, write down in table.md file and validate it, and then go to next hardware. Need to record the evidence sources.
Validate it by read the pdf again, check the device is actual present.
At minimum, compare:
- SoC / package / CPU identity
- memory type and size
- storage (eMMC, NAND, NOR, SD)
- boot media
- UART / debug console
- I2C devices
- SPI devices
- GPIO expanders
- GPIO assignments
- pinmux / pad control
- clocks
- regulators / PMIC
- Ethernet / PHY / reset wiring
- USB role and connector differences
- PCIe
- display pipeline / bridge chips / panels
- audio path / codec / MQS / microphone
- camera
- Wi-Fi / Bluetooth modules and enable/reset sequencing
- sensors
- interrupts
- reset lines
- power sequencing
- board-specific peripherals
- LEDs and buttons

Goal:
- determine what is actually different between **reference board** and **target board**,
- determine which differences can be solved by DTS,
- determine which require driver/config/firmware work,
- and record exact evidence sources.

---

### Step 4: Revise `table.md`

#### Required Column Meanings
- **Change Type**: one of
  - `DTS`
  - `Driver`
  - `DTS + Driver`
  - `Defconfig/Kconfig`
  - `Firmware/Config`
  - `No Change`
  - `Needs Review`
- **Evidence** must include page numbers, keywords, signal names, file paths, or header paths.

#### Critical Requirements
- This table must describe **reference board vs target board hardware differences** explicitly.
- A self-check table comparing target PDF vs target DTS may be created later, but it cannot replace `table.md`.
- If any row claims a hardware block is missing, the evidence must be strong; otherwise use `Unknown` or `Needs Review`.

#### Example

```markdown
# Hardware Comparison Table: TARGET vs REFERENCE

| Category | Function | Target Description | Reference Description | Match Status | Change Type | Planned Action | Evidence | Notes / Risk |
|---|---|---|---|---|---|---|---|---|
| Ethernet | ENET1 PHY reset | PCAL6524 pin 4 | PCAL6524 pin 15 | Different | DTS | Fix reset-gpios in Linux/U-Boot | Target PDF p.31 `PHY_RST`; Ref PDF p.29 `ENET1_RST`; Linux DTS path | Must keep Linux/U-Boot consistent |
| LED | STATUS_LED_R | PCAL6524 pin 14 | PCAL6524 pin 14 | Match | DTS | Add `gpio-leds` parent if missing | Target PDF p.42 `STATUS_LED_R`; Linux DTS path | Check regulator conflict |
```

---

### Step 5: Create Driver / Config / Firmware Change Lists
Based on `table.md`, generate:

```text
/project/reports/driver_change_list.md
/project/reports/config_change_list.md
```

#### `driver_change_list.md` must include
1. Component / Subsystem
2. Driver / Subsystem Path
3. Source Tree Status
4. Change Required
5. Reason
6. Verification Method
7. Blocking Status
8. Classification (`Required`, `Not Required`, `Unverified`)

Important rules:
- Consider each component separate, writing down it in driver_change_list.md and then go to next component.
- Do **not** list only changed drivers.
- Every major hardware block from `table.md` must have a corresponding row.
- `Not Required` still needs a reason.
- `Unverified` must state what to check next.
- If runtime firmware is needed, record it even if no driver source change is required.
- If a new driver may be needed, say whether an existing compatible/binding already covers it or whether a new driver/compatible must be added.

Example:

```markdown
| Component | Driver / Subsystem Path | Source Tree Status | Change Required | Reason | Verification Method | Blocking Status | Classification |
|---|---|---|---|---|---|---|---|
| gpio-leds | drivers/leds/leds-gpio.c | Present | No | Standard GPIO LED binding already exists | Check DTS node under `gpio-leds` and kernel binding | Non-blocking | Not Required |
| pcal6524 | drivers/gpio/gpio-pca953x.c | Present | No | Existing PCA95xx family driver should bind | Check compatible and I2C address | Non-blocking | Not Required |
| target_panel_x | drivers/gpu/drm/panel/... | Unknown | Maybe | Panel part not yet confirmed from PDF | Search panel compatible and binding | Blocking | Unverified |
```

#### `config_change_list.md` must include
- Linux defconfig items to check or enable
- U-Boot defconfig items to check or enable
- Kconfig options that may be needed for new peripherals
- firmware path or packaging requirements if applicable
- classification as `Required`, `Not Required`, or `Unverified`

---

### Step 6: Prepare Dependency and Tooling Notice
Before building, check whether required tools are available.

Typical examples include:
- device tree compiler (`dtc`)
- cross compiler / toolchain
- `make`
- `gcc`
- vendor build dependencies
- Python or shell tools required by the build system

Create:

```text
/project/reports/dependency_list.md
```

This file must include:
- required software/tool names,
- why each is needed,
- whether it is already available,
- exact installation action the **user** needs to perform if missing.

Important:
- Do **not** install packages with `sudo`.

---
### Step 7: Decide DTS Availability Strategy
Determine whether the target already has usable DTS files.

#### Case A: Target DTS exists in both Linux and U-Boot
- Use the existing target DTS files as the working base.
- Copy them into a working area before editing.
- If the U-Boot DTS is an official vendor DTS, treat it as a protected reference baseline and do not modify it in place.

#### Case B: Target DTS exists in only one side (Linux or U-Boot)
- Use the existing target DTS as the source to generate the missing side.
- Convert syntax and style as required for the destination tree.
- Keep semantics aligned with the original available target DTS.
- Hardware documentation (PDF / schematic) overrides DTS when conflicts occur, but changes must be evidence-based and not assumed.
#### Case C: Target DTS is missing in both Linux and U-Boot
- Use the reference DTS files as the structural base.
- Derive new target DTS files from the reference after comparing target and reference hardware PDFs.

Important:
- Linux DTS and U-Boot DTS may describe the same hardware with different syntax, include hierarchy, node coverage, and SPL visibility requirements.
- Conversion must adapt to the destination project style rather than blindly copying text.
### Step 8: Modify Target DTS Working Copies
Edit only the working copies of target DTS files.

Rules:
- Before overwrite original DTS files,check the compare table again.
- Keep Linux and U-Boot DTS changes traceable.
- Follow the style and include hierarchy of each destination tree.
- For U-Boot, account for SPL requirements and `bootph-*` visibility where needed.
- Before deleting, disabling, or omitting any inherited node, re-check target-side evidence.
- If presence/absence is uncertain, keep the node under review instead of blindly removing it.

Typical DTS work includes:
- enabling/disabling nodes,
- updating compatible strings,
- changing pinctrl,
- adjusting clock references,
- updating regulator supply bindings,
- changing GPIO assignments,
- changing PHY/MDIO descriptions,
- modifying aliases/chosen nodes,
- updating memory or reserved-memory regions,
- adding or removing `bootph-*` markers in U-Boot when needed,
- fixing include style to match the destination build tree.

---

### Step 9: Board-Specific Required Checks (Apply When Applicable)
This section contains board-specific checks that are mandatory only when the target/reference family actually uses these blocks.

#### 9.1 PCAL6524 pin 14 ownership check
If the board uses PCAL6524 and pin 14 appears in DTS, perform an explicit ownership check.

##### Required PDF/Schematic Verification
Search the target PDF/schematic for all relevant signals, such as:
- `P12V_EN`
- `12V_EN`
- `STATUS_LED_R`
- `LED_R`
- `PCAL6524`

Record:
- which net drives the red status LED,
- which net controls 12V enable,
- which PCAL6524 pin each net is connected to,
- exact page numbers and search keywords used.

##### Required DTS rules
If Linux uses a red LED on PCAL6524 pin 14, it must be placed under a `gpio-leds` parent node. A standalone `led-red {}` node is not enough.

Correct pattern:

```dts
/gpio_leds {
    compatible = "gpio-leds";

    led-red {
        label = "status:red";
        gpios = <&pcal6524 14 GPIO_ACTIVE_HIGH>;
        default-state = "off";
    };
};
```

If `reg_vdd_12v` was also using the same pin, do not keep dual ownership. Only one of the following is allowed:

- **Case A: 12V rail is hardware always-on**
  - remove `gpio = <...>` and `enable-active-high`
  - use `regulator-always-on;`

- **Case B: 12V rail is controlled by another PCAL6524 pin**
  - correct the regulator GPIO to the schematic-confirmed pin number

- **Case C: not confirmed**
  - do not guess
  - mark the row as `Needs Review` / `Unverified`
  - do not claim the conflict is solved

Both `table.md` and `consistency_check.md` must explicitly record:
- the LED pin evidence,
- the regulator pin evidence,
- the chosen fix,
- whether the conflict is fully resolved or still unverified.

#### 9.2 Ethernet PHY reset GPIO consistency
If Ethernet PHY reset is described in Linux and U-Boot, use the same GPIO mapping unless the schematic shows an intentional stage-specific difference.

Record exact PDF evidence and DTS file paths.

#### 9.3 U-Boot LPSPI1 / LPSPI2 pinmux conflict check
If U-Boot enables LPSPI1 or LPSPI2, verify pinmux against boot console and boot-critical peripherals.

For the FRDM-style i.MX93 case, this check is mandatory:
- verify whether the vendor U-Boot DTS actually enables `lpspi1` or `lpspi2`,
- verify pin ownership using `imx93-pinfunc.h`,
- if LPSPI2 SIN/PCS0 uses `UART1_RXD` / `UART1_TXD` pads with no alternative mux, U-Boot must not enable LPSPI2,
- remove or disable the conflicting node in the working DTS,
- remove the corresponding pinctrl group if it is no longer used,
- record the exact DTS path and header path used as evidence.

This is not satisfied by saying “NXP already did it” unless the source tree really proves it.

#### 9.4 U-Boot include path sanity
Normalize include paths to match the local vendor tree style.
Prefer same-directory include style when the tree expects it.

---

### Step 10: Perform Mandatory Linux-vs-U-Boot Consistency Checks
Create:

```text
/project/reports/consistency_check.md
```

At minimum, verify:
1. compatible string consistency
2. Ethernet PHY reset GPIO consistency
3. regulator / GPIO expander pin ownership consistency
4. console / boot-critical peripheral consistency
5. pinmux conflict check
6. include path sanity check
7. node enablement consistency for devices needed in both stages
8. results of all applicable board-specific required checks from Step 10

Any contradiction found here is blocking until either:
- it is fixed, or
- it is documented with a clear board-level reason.

---

### Step 11: Build Linux and U-Boot DTBs
Build the target DTB outputs for both Linux and U-Boot.

Requirements:
- Produce both DTBs if both trees are available.
- Capture the exact build command lines.
- Store the build instructions in:

```text
/project/reports/build_commands.md
```

This file must include:
- environment variables if needed,
- toolchain prefix if needed,
- exact `make` or build script commands,
- target names,
- output artifact paths.

If U-Boot uses SPL, also record how SPL artifacts are located and validated.

---

### Step 12: Validate DTBs by Reverse Decompilation
After the DTBs are built, decompile them and save:

```text
project/validation/linux.dts
project/validation/uboot.dts
project/validation/spl.dts  (if SPL DTB exists)
```

Typical commands:

```bash
dtc -I dtb -O dts -o project/validation/linux.dts <linux_target.dtb>
dtc -I dtb -O dts -o project/validation/uboot.dts <uboot_target.dtb>
```

If SPL is built, locate and validate `u-boot-spl.dtb` as well.

Check:
- expected nodes exist,
- required properties are preserved,
- `bootph-*` markers are effective when SPL is relevant,
- dependency chains remain intact for boot-critical nodes.

---

### Step 13: Run the Mandatory Validation Loop
This step is mandatory after decompilation.

Cross-check all of the following:
1. DTS ↔ `table.md`
2. DTS ↔ PDF evidence
3. Linux ↔ U-Boot consistency
4. DTS ↔ driver/config/firmware reports

#### Required behavior if a mismatch is found
If you discover any of the following:
- the DTS implementation disagrees with `table.md`,
- the PDF evidence does not support the current table entry,
- the pin mapping or net mapping is wrong,
- Linux and U-Boot contradict each other,
- a board-specific conflict was only partially fixed,

then you must:
1. go back to the PDFs/schematics and search again,
2. correct `table.md`,
3. update `consistency_check.md`,
4. update `driver_change_list.md`,
5. update `config_change_list.md` if impacted,
6. clearly mark the item as `Correct`, `Partial`, `Missing`, or `Unknown`.

Do **not** leave stale tables after validation reveals a mistake.

---

### Step 14: Apply Driver or Config Changes If Needed
If the reports show any item whose change type is:
- `Driver`
- `DTS + Driver`
- `Defconfig/Kconfig`
- `Firmware/Config`

then perform the appropriate analysis or modification at this stage.

Guideline:
- Only change drivers after DTS-side validation is completed.
- Keep DTS, driver, config, and firmware responsibilities separate.
- If full modification is not possible, at least produce an explicit actionable list.

---

### Step 15: Produce Final Build and Validation Summary
At the end, generate a concise final summary containing:

1. Which DTS files were found originally
2. Whether any target DTS had to be generated
3. Main hardware differences between reference board and target board
4. Driver/config/firmware items identified
5. Where changes were made:
   - Linux DTS
   - U-Boot DTS
   - Driver
   - Defconfig/Kconfig
6. Whether Linux DTB built successfully
7. Whether U-Boot DTB built successfully
8. Whether SPL artifact was found and validated
9. Whether validation DTS matches `table.md`
10. Whether Linux and U-Boot are internally consistent
11. Whether reports were updated after validation if mismatches were found
12. Remaining risks or unverified items
13. Required user-installed dependencies
14. Exact commands needed to rebuild

The summary must explicitly mention the result of all applicable board-specific checks from Step 10.

---

### Step 16: Generate Build Script and FWAuto Command Configuration (Optional When Requested)
If the task explicitly asks for a reusable build entrypoint, generate:
1. `build-frdm.sh`
2. updated FWAuto command configuration that runs the script
3. exact rebuild commands
4. a short explanation of produced artifacts

The build script should:
- set required environment variables such as `ARCH` and `CROSS_COMPILE`,
- define Linux, U-Boot, output, and log paths,
- check prerequisites before building,
- build at minimum Linux DTB and U-Boot binary/DTB,
- optionally build Linux `Image`, modules, or full bootable images if requested,
- collect artifacts into an organized output directory,
- validate built DTBs by decompilation,
- provide clear success/failure status,
- exit with appropriate error codes.

The FWAuto command should run:

```bash
bash ./build-frdm.sh
```

If full image generation cannot be completed, still generate the script and clearly mark which stages are blocked.

---

## Critical Validation Checklist
Before declaring the result acceptable, explicitly check:

- [ ] `table.md` is really **reference board vs target board**
- [ ] `table.md` has category grouping, or `hardware_diff.md` exists
- [ ] Every table row includes explicit evidence
- [ ] Driver/config/firmware change lists exist
- [ ] Driver review includes `Required`, `Not Required`, and `Unverified`
- [ ] Driver review includes driver/source paths, not just yes/no statements
- [ ] Any node removal decision is backed by confirmed target-side evidence
- [ ] Notes / footnotes / annotations were checked where relevant
- [ ] Official vendor U-Boot DTS files were not modified in place without justification
- [ ] Optional hardware was split into connector / module / capability comparisons where needed
- [ ] Linux and U-Boot use consistent board compatible naming or the difference is explained
- [ ] Ethernet PHY reset GPIOs are consistent across stages or intentionally documented
- [ ] GPIO expander pins are not double-assigned to conflicting functions
- [ ] If PCAL6524 pin 14 is used, LED/regulator ownership was verified from PDF evidence and fully resolved or clearly marked unverified
- [ ] If LPSPI2 conflicts with UART1 pads, U-Boot does not leave LPSPI2 enabled
- [ ] U-Boot include paths match the local tree style
- [ ] U-Boot boot-critical nodes include necessary `bootph-*` markers where required
- [ ] Validation DTS files were generated
- [ ] `table.md` was revalidated after DTB decompilation
- [ ] Reports were corrected if validation exposed mistakes

---

## Decision Logic Summary

```text
If target DTS exists in Linux and U-Boot:
    use both as working base
Else if target DTS exists in only one side:
    generate the missing side from the existing target DTS
Else:
    derive both from reference DTS + target/reference PDF comparison

Always compare reference board vs target board hardware explicitly
Always generate table.md as the main hardware-difference table with evidence
Generate hardware_diff.md only if table.md lacks grouped summary
Always generate driver/config/firmware change lists
Always run Linux-vs-U-Boot consistency checks
Always build DTBs
Always decompile DTBs for validation
Always run the validation loop and update reports when mismatches are found
Only modify drivers after DTS validation if the reports say driver work is needed
```

---

## What Counts as Success
The skill is successful only if all of the following are true:

- target/reference hardware PDFs were actually reviewed,
- reference DTS was found and used as needed,
- original DTS files were not modified in place,
- the main table describes **reference board vs target board hardware differences**,
- each significant row in `table.md` has explicit evidence,
- driver/config/firmware implications were explicitly identified,
- the driver review includes changed, unchanged, and unverified items with source paths,
- Linux and U-Boot contradictions were checked and resolved or documented,
- target Linux and U-Boot DTBs were built or the blocking issue was clearly reported,
- validation DTS files were generated (Linux, U-Boot, and SPL if built),
- no hardware block was declared absent solely from first-pass non-detection,
- official vendor U-Boot baselines were preserved unless a justified derivative was created,
- optional hardware was not flattened into one misleading row,
- `table.md` matches the implemented changes or was corrected after validation,
- dependency requirements were clearly communicated without using `sudo`.

---

## Failure Conditions
Stop and report clearly if any of the following occur:

- target or reference hardware PDF is missing,
- reference DTS cannot be found,
- source tree is incomplete,
- required build tools are missing and the user has not installed them yet,
- DTB build fails,
- validation DTS cannot be generated,
- the main table is not based on reference-vs-target hardware comparison,
- a node was removed or marked missing without confirmed target-side evidence,
- notes / annotations / errata were not checked for ambiguous hardware presence,
- Linux/U-Boot contradictions remain unresolved for boot-critical signals,
- SPL is built but was not validated when SPL DTB is available,
- driver/config/firmware implications are not analyzed,
- the validation loop was skipped,
- a known blocking conflict such as GPIO double ownership or UART/pinmux conflict remains unresolved.

Do not hide these failures. Report them explicitly.

---

## Practical Notes for FWAuto

### Always Required
- `table.md` with reference-vs-target hardware comparison and evidence
- `consistency_check.md` for Linux-vs-U-Boot validation
- `driver_change_list.md` and `config_change_list.md`
- `dependency_list.md` and `build_commands.md`
- Decompiled validation DTS for Linux and U-Boot
- Report reconciliation after validation

### Conditionally Required
- `hardware_diff.md`: only if `table.md` lacks good grouping
- `spl.dts` validation: only if U-Boot builds SPL DTB
- Build script generation: only when explicitly requested
- Full kernel/U-Boot image build: only when explicitly requested

### General Principles
- Prefer concise logs over continuous verbose monitoring.
- Keep analysis traceable and file-based.
- Always distinguish between:
  - assumptions from software trees,
  - facts confirmed from hardware PDFs,
  - facts confirmed from built validation DTS.
- Never state that BSP porting is complete based only on a successful compile.
- If full image build is outside the current request, stop after validated DTBs and a complete report set.

---

## Final Self-Review Before Delivery
Before returning the result, FWAuto must read the generated reports and this skill logic once more and confirm:

1. There is no contradiction between:
   - “hardware missing”
   - “node removed”
   - “needs review”

2. No step requires deleting target nodes before target-side evidence has been confirmed.

3. Official vendor U-Boot DTS files were either:
   - preserved untouched, or
   - copied into a clearly marked working derivative before modification.

4. SPL build / locate / validation logic is reflected consistently in:
   - build commands
   - validation outputs
   - final summary

5. The workflow has no circular logic, such as using DTS edits to prove the original hardware difference.

6. If `hardware_diff.md` exists, it is a grouped summary, not a duplicate of `table.md`.

7. `driver_change_list.md` includes rows for:
   - changed items,
   - unchanged items,
   - unverified items,
   - and includes source/driver paths.

8. The validation loop was actually run after decompilation, not just mentioned.

9. For applicable FRDM-style i.MX93 work, the reports explicitly state the result of:
   - PCAL6524 pin 14 ownership check
   - Ethernet PHY reset GPIO check
   - U-Boot LPSPI pin conflict check
   - U-Boot include path style check

If any contradiction is found, fix the report structure before final delivery.

---

## Suggested Skill Invocation Intent
Use this skill when the user asks for tasks such as:
- BSP porting
- porting DTS from one SoC/board to another
- generating target DTS from reference board support
- validating Linux/U-Boot DTB correctness
- checking whether a hardware difference requires DTS, driver, config, or firmware modification
