# BSP Porting Skill for FWAuto

## Skill Name
BSP Porting and DTS Build Validation for Target SoC

## Purpose
This skill guides FWAuto through a safe, traceable BSP porting workflow when the user provides a repository containing:

1. Target SoC hardware documents:FRDM
2. Reference SoC hardware documents:imx93 EVK
3. Linux kernel source
4. U-Boot source

The goal is to:
- locate or derive the target DTS files,
- compare target and reference hardware,
- determine whether changes belong in DTS or driver code,
- build both Linux and U-Boot DTBs,
- validate the generated DTBs by reverse decompilation,
- and produce a reproducible build procedure.
- generate `build-frdm.sh` as the main FWAuto build entrypoint for Linux kernel and U-Boot

This skill must preserve original source data and avoid risky system actions.

---

## Scope
Use this skill when the task involves BSP porting, board bring-up preparation, DTS creation/modification, Linux kernel DTB build, or U-Boot DTB build for a target SoC/board based on a reference SoC/board.

Do **not** use this skill for:
- driver development unrelated to board DTS,
- application-level software build tasks,
- tasks that require flashing hardware when no hardware access is available.

---

## Mandatory Rules

1. **Never modify the originally provided DTS files directly.**
   - Always create copied working files before editing.
   - Preserve the original source tree state as much as possible.

2. **Never use `sudo` to install software or dependencies.**
   - If a build tool or package is missing, tell the user exactly what needs to be installed.
   - Ask the user to install it manually.

3. **Always prioritize hardware PDF documents over software guesses.**
   - Do not rely only on existing DTS files.
   - Hardware PDFs are the source of truth for BSP comparison.

4. **Do not assume a successful build means the DTS is fully correct.**
   - Build success only proves syntax and partial integration correctness.
   - Functional validation still requires comparison against hardware documents and decompiled DTB review.

5. **Do not monitor or print excessively verbose build output unless needed.**
   - Keep logs concise and structured.
   - Avoid producing huge outputs that can block the workflow.

---

## Required Repository Inputs
The user-provided repository should contain or make accessible the following:

- Target SoC hardware document(s), preferably PDF
- Reference SoC hardware document(s), preferably PDF
- Linux kernel source tree
- U-Boot source tree

Optional but useful:
- Existing board DTS/DTSI files
- Build scripts
- Toolchain notes
- Vendor SDK instructions

---

## Expected Output
By the end of this skill, FWAuto should produce:

1. A working copy of target DTS files for Linux and U-Boot
2. A hardware comparison table in `table.md`
3. Built DTB outputs for Linux and U-Boot
4. Decompiled validation DTS files:
   - `/project/validation/linux.dts`
   - `/project/validation/uboot.dts`
5. A list of required tools/software for the user to install
6. A reproducible build command list
7. A generated `build-frdm.sh` build script
8. Updated FWAuto command configuration to run `build-frdm.sh`
9. A clear conclusion stating:
   - whether DTS coverage matches the comparison table,
   - whether driver changes are still required,
   - whether the DTBs are ready for the next BSP stage.

---

## Directory and File Conventions
Use the following output locations when possible:

```text
/project/
  validation/
    linux.dts
    uboot.dts
  reports/
    table.md
    build_commands.md
    dependency_list.md
  work/
    linux-dts/
    uboot-dts/
```

If these folders do not exist, create them in the working area without altering original source files.

---

## Step-by-Step Procedure

### Step 1: Inspect Repository Contents
Confirm the repository includes:
- target SoC PDF document(s),
- reference SoC PDF document(s),
- Linux kernel source,
- U-Boot source.

Actions:
1. Search for PDF files related to target and reference SoCs.
2. Identify likely Linux kernel root.
3. Identify likely U-Boot root.
4. Record important file paths.

If any required input is missing:
- stop the porting flow,
- report exactly what is missing,
- ask the user to provide it.

---

### Step 2: Identify Target and Reference SoC Names
Extract the target and reference SoC/board names from:
- hardware PDFs,
- directory names,
- DTS filenames,
- user-provided metadata.

Actions:
1. Determine the exact target SoC/board name.
2. Determine the exact reference SoC/board name.
3. Use those names to search for DTS/DTSI files in Linux and U-Boot.

Typical search targets include:
- `arch/*/boot/dts/` in Linux
- `arch/*/dts/` in U-Boot

Requirements:
- The **reference SoC DTS must be found** in both Linux and/or U-Boot as needed for porting.
- The **target SoC DTS may be missing**.

Document all findings before proceeding.

---

### Step 3: Decide DTS Availability Strategy
Determine whether the target already has usable DTS files.

#### Case A: Target DTS exists in both Linux and U-Boot
- Use the existing target DTS files as the working base.
- Copy them into a working area before editing.
- Proceed to hardware comparison.

#### Case B: Target DTS exists in only one side (Linux or U-Boot)
- Use the existing target DTS as the source to generate the missing side.
- Convert syntax and style as required for the destination tree.
- Keep semantics aligned with the original available target DTS.
- Then proceed to hardware comparison.

Examples:
- If target Linux DTS exists but U-Boot DTS is missing, generate a U-Boot-target DTS from Linux-target DTS.
- If target U-Boot DTS exists but Linux DTS is missing, generate a Linux-target DTS from U-Boot-target DTS.

#### Case C: Target DTS is missing in both Linux and U-Boot
- Use the reference DTS files as the structural base.
- Derive new target DTS files from the reference after comparing target and reference hardware PDFs.

Important:
- Linux DTS and U-Boot DTS may describe the same hardware with different syntax, conventions, include hierarchy, or node coverage.
- Conversion must adapt to the destination project style rather than blindly copying text.

---

### Step 4: Compare Target vs Reference Hardware PDFs
This is the most important analysis stage.

Read the target and reference hardware PDF documents and compare all relevant hardware blocks and board-level differences.

At minimum, compare:
- CPU / SoC identity
- memory type and size
- storage (eMMC, NAND, NOR, SD)
- boot media
- UART / debug console
- I2C devices
- SPI devices
- GPIO usage
- pinmux / pad control
- clocks
- regulators / PMIC
- Ethernet / PHY
- USB
- PCIe
- display
- audio
- camera
- Wi-Fi / Bluetooth
- sensors
- interrupts
- reset lines
- power sequencing
- board-specific peripherals

#### Special Rule for Derived DTS Case
If in Step 3 one DTS was generated from the other:
- compare the Linux and U-Boot DTS contents with each other,
- focus the PDF comparison only on items that may not be fully represented or may differ between Linux and U-Boot conventions.

Goal:
- determine which differences can be solved by DTS edits,
- and which require driver modification.

---

### Step 5: Generate `table.md`
Create a comparison table in Markdown format.

Save it as:

```text
/project/reports/table.md
```

The table must use:
- **rows** = hardware blocks / functions
- **columns** =
  1. Function or Hardware Name
  2. Target Document Name
  3. Reference Document Name
  4. Match Status
  5. Change Type

#### Required Column Meanings
- **Function or Hardware Name**: the subsystem or device name
- **Target Document Name**: how it appears in the target PDF
- **Reference Document Name**: how it appears in the reference PDF
- **Match Status**: one of
  - `Match`
  - `Different`
  - `Missing in Target`
  - `Missing in Reference`
  - `Unknown`
- **Change Type**: one of
  - `DTS`
  - `Driver`
  - `DTS + Driver`
  - `No Change`
  - `Needs Review`

#### Example Table Format

```md
| Function or Hardware Name | Target Document Name | Reference Document Name | Match Status | Change Type |
|---|---|---|---|---|
| UART Console | LPUART1 | LPUART1 | Match | No Change |
| Ethernet PHY | RTL8211F | AR8031 | Different | DTS |
| PMIC | PCA9450 | BD71837 | Different | DTS + Driver |
| Touch Panel | Goodix GT911 | - | Missing in Reference | Driver |
```

This table must be designed for **human visual review**.

---

### Step 6: Prepare Dependency and Tooling Notice
Before building, check whether the required tools are available.

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
- Tell the user what to install and wait for the environment to provide it.

---

### Step 7: Modify Target DTS Working Copies
Edit only the working copies of target DTS files.

Rules:
- Never overwrite the original downloaded DTS directly.
- Keep Linux and U-Boot DTS changes traceable.
- Follow the style and include hierarchy of each destination tree.

When editing, align with:
- hardware PDFs,
- comparison table,
- destination project conventions.

Typical DTS work includes:
- enabling/disabling nodes,
- updating compatible strings,
- changing pinctrl,
- adjusting clock references,
- updating regulator supply bindings,
- changing GPIO assignments,
- changing PHY/MDIO descriptions,
- modifying aliases/chosen nodes,
- updating memory or reserved-memory regions.

---

### Step 8: Build Linux and U-Boot DTBs
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

Example categories to document:
- Linux DTB build command
- U-Boot DTB build command
- full image build command if later needed

Do not claim image build is required unless the project specifically needs it.
At this skill stage, DTB build validation is the core requirement.

---

### Step 9: Validate DTBs by Reverse Decompilation
After the DTBs are built, validate them by decompiling them back into DTS.

Save the outputs as:

```text
/project/validation/linux.dts
/project/validation/uboot.dts
```

Typical validation method:

```bash
dtc -I dtb -O dts -o /project/validation/linux.dts <linux_target.dtb>
dtc -I dtb -O dts -o /project/validation/uboot.dts <uboot_target.dtb>
```

Validation goals:
- confirm the built DTB contains the intended nodes and properties,
- confirm no important property was dropped during include expansion or build preprocessing,
- confirm the output structure still matches hardware expectations.

Important:
- Decompiled DTS is a validation artifact, not a replacement source file.

---

### Step 10: Cross-Check Validation DTS Against `table.md`
Compare the decompiled validation DTS files with the hardware comparison table.

Check whether every row marked as `DTS` or `DTS + Driver` has been reflected correctly in:
- `/project/validation/linux.dts`
- `/project/validation/uboot.dts`

For each relevant row, determine:
- implemented correctly,
- partially implemented,
- missing,
- uncertain.

Update conclusions in the report if mismatches remain.

---

### Step 11: Apply Driver Changes If Needed
If `table.md` shows any row whose Change Type is:
- `Driver`
- `DTS + Driver`

then perform driver-side analysis and modification at this stage.

Guideline:
- Only change drivers after DTS-side validation has been completed.
- Keep DTS and driver responsibilities separate.

Driver change examples may include:
- missing compatible support,
- missing regulator driver support,
- PHY driver mismatch,
- panel or touch controller enablement,
- PMIC integration,
- clock or reset driver support.

If no driver changes are required, explicitly skip this step.

---

### Step 12: Produce Final Build and Validation Summary
At the end, generate a concise final summary containing:

1. Which DTS files were found originally
2. Whether any target DTS had to be generated
3. Main hardware differences between target and reference
4. Where changes were made:
   - Linux DTS
   - U-Boot DTS
   - Driver
5. Whether Linux DTB built successfully
6. Whether U-Boot DTB built successfully
7. Whether validation DTS matches `table.md`
8. Remaining risks or unverified items
9. Required user-installed dependencies
10. Exact commands needed to rebuild

---

### Step 13: Generate Build Script and FWAuto Command Configuration

After DTS modification and validation are complete, do **not** stop at building DTS/DTB only.  
The final deliverable must include a **reusable build script** and an updated **FWAuto command configuration** so the project can be rebuilt consistently.

#### Objective
Generate a complete build entrypoint for FWAuto that builds the modified Linux kernel and U-Boot sources, instead of only compiling DTS into DTB.

#### Required Outputs
You must produce all of the following:

1. A build script named `build-frdm.sh`
2. An updated FWAuto command configuration that runs `build-frdm.sh`
3. A list of exact rebuild commands
4. A short explanation of what artifacts are produced

#### Build Script Requirements
Create `build-frdm.sh` as a full build script, not a DTS-only helper.

The script must:

- set and export required build environment variables, including:
  - `ARCH`
  - `CROSS_COMPILE`
- define source directories for:
  - Linux kernel
  - U-Boot
- verify that required directories exist before building
- verify that the toolchain exists before building
- create a log directory and log file
- support building:
  - Linux kernel `Image`
  - Linux kernel `dtbs`
  - Linux kernel `modules`
  - U-Boot binary
  - `flash.bin` or equivalent bootable image if supported
- collect build artifacts into a dedicated output directory
- print clear success/failure messages
- exit immediately on fatal errors
- only build our target dts not every dts in folder 

#### Important Constraint
Do **not** interpret the task as “only compile DTS into DTB”.

The goal is to:

- generate a **complete build script file**
- use that script as the **main build entrypoint**
- make FWAuto invoke that script directly

`dtb` generation is only one sub-step of the full build flow, not the final objective.

#### FWAuto Command Configuration
Edit FWAuto command configuration so that the build entrypoint calls the generated script rather than individual `make dtbs` commands.

The FWAuto command must run:

```bash
bash ./build-frdm.sh
```

If the environment requires a different path, use the correct absolute or workspace-relative path, but keep the command centered around the generated script.

#### Exact Rebuild Commands
In the final report, provide the exact commands needed for a future rebuild, including at minimum:

```bash
chmod +x ./build-frdm.sh
bash ./build-frdm.sh
```

If separate modes are supported, also include them, for example:

```bash
bash ./build-frdm.sh --kernel-only
bash ./build-frdm.sh --uboot-only
bash ./build-frdm.sh --clean
```

#### Required Final Reporting
At the end, explicitly report:

1. Where `build-frdm.sh` was created
2. Whether FWAuto command config was updated successfully
3. What the script builds:
   - kernel Image
   - DTB(s)
   - modules
   - U-Boot
   - `flash.bin` or equivalent
4. Where output artifacts are stored
5. Any dependencies that must still be installed by the user
6. Any remaining risks, such as:
   - missing firmware blobs
   - unverified runtime boot behavior
   - build success without real board validation

#### Failure Handling
If full image generation cannot be completed, do not stop at DTS compilation silently.

Instead:

- still generate `build-frdm.sh`
- make the script build as much as possible
- clearly mark which stages succeeded
- clearly mark which stages remain blocked and why

---

## Decision Logic Summary

```text
If target DTS exists in Linux and U-Boot:
    use both as working base
Else if target DTS exists in only one side:
    generate the missing side from the existing target DTS
Else:
    derive both from reference DTS + target/reference PDF comparison

Always compare target/reference PDFs
Always generate table.md
Always build DTBs
Always decompile DTBs for validation
Only modify drivers after DTS validation if table.md says driver work is needed
```

---

## What Counts as Success
The skill is successful only if all of the following are true:

- target/reference hardware PDFs were actually reviewed,
- reference DTS was found and used as needed,
- original DTS files were not modified in place,
- target Linux and U-Boot DTBs were built or the blocking issue was clearly reported,
- validation DTS files were generated,
- `table.md` exists and matches the implemented changes,
- required driver changes were identified or completed,
- dependency requirements were clearly communicated to the user without using `sudo`.

---

## Failure Conditions
Stop and report clearly if any of the following occur:

- target or reference hardware PDF is missing,
- reference DTS cannot be found,
- source tree is incomplete,
- required build tools are missing and the user has not installed them yet,
- DTB build fails,
- validation DTS cannot be generated,
- table and validation results do not agree.

Do not hide these failures. Report them explicitly.

---

## Practical Notes for FWAuto

- Prefer concise logs over continuous verbose monitoring.
- Keep analysis traceable and file-based.
- Always distinguish between:
  - assumptions from software trees,
  - facts confirmed from hardware PDFs,
  - facts confirmed from built validation DTS.
- Never state that BSP porting is complete based only on a successful compile.
- If full image build is outside the current request, stop after validated DTBs and build instructions.

---

## Recommended Deliverables Checklist

- [ ] Target hardware PDF identified
- [ ] Reference hardware PDF identified
- [ ] Linux source tree identified
- [ ] U-Boot source tree identified
- [ ] Target SoC name identified
- [ ] Reference SoC name identified
- [ ] Reference DTS found
- [ ] Target DTS status determined
- [ ] Working DTS copies created
- [ ] Hardware comparison completed
- [ ] `/project/reports/table.md` generated
- [ ] `/project/reports/dependency_list.md` generated
- [ ] Target Linux DTS updated
- [ ] Target U-Boot DTS updated
- [ ] Linux DTB built
- [ ] U-Boot DTB built
- [ ] `/project/validation/linux.dts` generated
- [ ] `/project/validation/uboot.dts` generated
- [ ] Validation cross-check completed
- [ ] Driver changes completed or explicitly skipped
- [ ] `/project/reports/build_commands.md` generated
- [ ] `build-frdm.sh` generated
- [ ] FWAuto command config updated to run `build-frdm.sh`
- [ ] Final summary produced

---

## Suggested Skill Invocation Intent
Use this skill when the user asks for tasks such as:
- BSP porting
- porting DTS from one SoC/board to another
- generating target DTS from reference board support
- validating Linux/U-Boot DTB correctness
- checking whether a hardware difference requires DTS or driver modification

