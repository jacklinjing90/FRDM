# FRDM i.MX Build Notes

Use these notes for FRDM-IMX93 style BSP build integration.

## Known Good Commands

U-Boot:

```sh
make -C uboot-imx imx93_11x11_frdm_defconfig
make -C uboot-imx CROSS_COMPILE=aarch64-linux-gnu- -j2
```

Linux targeted DTBs:

```sh
make -C linux-imx ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- imx_v8_defconfig
make -C linux-imx ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- -j2 \
  freescale/imx93-11x11-frdm.dtb \
  freescale/imx93-11x11-frdm-tianma-wvga-panel.dtb \
  freescale/imx93-11x11-frdm-waveshare-7inch-c-panel.dtb
```

## Host Compiler Failure

If U-Boot fails with:

```text
cc1: error: bad value 'armv8-a+crc' for '-march=' switch
```

or warnings about `x18`, the build is using host GCC. Rerun with `CROSS_COMPILE=aarch64-linux-gnu-`.

## Generated Artifacts

Do not patch generated objects or binaries. Examples:

- `board/freescale/*/*.o`
- `arch/arm/dts/*.dtb`
- `arch/arm64/boot/dts/freescale/*.dtb`
- `.cmd`, `.su`, `u-boot.bin`, `spl/u-boot-spl.bin`, `Image`

Fix source and regenerate these artifacts instead.
