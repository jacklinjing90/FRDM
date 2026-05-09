---
name: imx-bsp-build-integration
description: Make NXP i.MX BSP board ports build in U-Boot and Linux. Use when Codex is asked to revise or verify U-Boot Kconfig, MAINTAINERS, Makefile, defconfig, board .c/.env/spl.c/timing files, or Linux DTS Makefile, defconfig, and imx.config so an i.MX board such as FRDM-IMX93 builds cleanly; also use when build failures involve wrong host compiler use, missing board build hooks, generated .o/.dtb artifacts, or i.MX U-Boot/Linux device-tree integration.
---

# i.MX BSP Build Integration

## Workflow

1. Identify active trees first. Prefer local trees named like `uboot-imx`, `u-boot-*`, `linux-imx`, or `linux-*`. Check `git status --short` in each tree and preserve user changes.

2. Locate the target board and reference board. Search for board names, SoC names, and DTB names across:
   - U-Boot: `board/`, `configs/`, `arch/arm/mach-imx/`, `arch/arm/dts/`, `include/configs/`
   - Linux: `arch/arm64/boot/dts/freescale/`, `arch/arm64/configs/`

3. Edit only source build integration. For U-Boot, typical source files are:
   - `arch/arm/mach-imx/imx9/Kconfig`
   - `board/freescale/<board>/Kconfig`
   - `board/freescale/<board>/MAINTAINERS`
   - `board/freescale/<board>/Makefile`
   - `configs/<board>_defconfig`
   - `include/configs/<board>.h`
   - `board/freescale/<board>/<board>.c`
   - `board/freescale/<board>/<board>.env`
   - `board/freescale/<board>/spl.c`
   - DDR timing `.c` files when SPL needs them

4. Do not hand-edit generated files. Treat `.o`, `.dtb`, `.cmd`, `.su`, `u-boot.bin`, `Image`, and other build outputs as artifacts to regenerate, not source to patch. If a user asks to revise `.o`, interpret that as "fix source so the object builds".

5. For U-Boot i.MX93/ARM64 builds, always set the cross compiler explicitly:

```sh
make -C uboot-imx imx93_11x11_frdm_defconfig
make -C uboot-imx CROSS_COMPILE=aarch64-linux-gnu- -j2
```

If the build fails with `bad value 'armv8-a+crc' for '-march='` or `unknown register name: x18`, it used the host x86 compiler. Do not patch source for that error; rerun with `CROSS_COMPILE=aarch64-linux-gnu-`.

6. For Linux i.MX ARM64 builds, always set both `ARCH` and `CROSS_COMPILE`:

```sh
make -C linux-imx ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- imx_v8_defconfig
make -C linux-imx ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -j2 \
  freescale/imx93-11x11-frdm.dtb \
  freescale/imx93-11x11-frdm-tianma-wvga-panel.dtb \
  freescale/imx93-11x11-frdm-waveshare-7inch-c-panel.dtb
```

Run targeted DTB builds before `Image dtbs`; full kernel builds can take a long time and are usually unnecessary to verify board integration.

## Build Hooks

Confirm these before editing:

- U-Boot target Kconfig selects the SoC and sources the board Kconfig.
- U-Boot board Makefile includes the board object, SPL object, and needed DDR timing objects under `CONFIG_SPL_BUILD`.
- U-Boot defconfig sets `CONFIG_TARGET_*`, `CONFIG_DEFAULT_DEVICE_TREE`, `CONFIG_DEFAULT_FDT_FILE`, SPL settings, PMIC, MMC, serial, pinctrl, and DDR options.
- U-Boot env sets `fdtfile=CONFIG_DEFAULT_FDT_FILE` unless the local board uses another established pattern.
- Linux DTS Makefile lists the base DTB and any combined overlay DTBs.
- Linux defconfig/config fragment enables the drivers used by the board DTS, such as `CONFIG_ARCH_MXC`, `CONFIG_CLK_IMX93`, `CONFIG_PINCTRL_IMX93`, ADC, GPIO expander, audio, display, PHY, MMC, Ethernet, USB, and RTC drivers.

## Validation Order

Use the cheapest reliable validation first:

1. `command -v aarch64-linux-gnu-gcc`
2. U-Boot board defconfig
3. U-Boot full build
4. Linux board defconfig
5. Linux target board DTBs
6. Linux `Image dtbs` only when requested or when source changes affect kernel C code

Use `scripts/check-imx-bsp-build.sh` for the standard U-Boot plus targeted Linux DTB validation. Read `references/imx-frdm-build-notes.md` when working specifically on FRDM-IMX93 or when diagnosing the host-compiler failure.
