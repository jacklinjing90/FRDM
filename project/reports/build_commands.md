# Build Commands for FRDM-IMX93 DTBs

## Environment Setup

```bash
export ARCH=arm64
export CROSS_COMPILE=aarch64-linux-gnu-
export PROJECT_ROOT=/home/lin/TEST
```

## Linux Kernel DTB Build

### Preparation

1. Copy generated Linux DTS to kernel source:
```bash
cp ${PROJECT_ROOT}/project/work/linux-dts/imx93-11x11-frdm.dts \
   ${PROJECT_ROOT}/linux-imx/arch/arm64/boot/dts/freescale/
```

2. Update Makefile to include the new DTB:
```bash
cd ${PROJECT_ROOT}/linux-imx/arch/arm64/boot/dts/freescale
# Add to Makefile: dtb-$(CONFIG_ARCH_MXC) += imx93-11x11-frdm.dtb
```

### Build Command

```bash
cd ${PROJECT_ROOT}/linux-imx
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- freescale/imx93-11x11-frdm.dtb
```

**Output Location:**
```
${PROJECT_ROOT}/linux-imx/arch/arm64/boot/dts/freescale/imx93-11x11-frdm.dtb
```

### Alternative: Direct DTC Compilation

```bash
cd ${PROJECT_ROOT}/linux-imx/arch/arm64/boot/dts/freescale
cpp -nostdinc \
    -I ${PROJECT_ROOT}/linux-imx/include \
    -I ${PROJECT_ROOT}/linux-imx/arch/arm64/boot/dts/freescale \
    -I ${PROJECT_ROOT}/linux-imx/arch/arm64/boot/dts \
    -undef -x assembler-with-cpp \
    imx93-11x11-frdm.dts \
    | dtc -I dts -O dtb -o imx93-11x11-frdm.dtb -
```

## U-Boot DTB Build

### Method 1: Full U-Boot Build with DTB

```bash
cd ${PROJECT_ROOT}/uboot-imx
make ARCH=arm CROSS_COMPILE=aarch64-linux-gnu- imx93_11x11_frdm_defconfig
make ARCH=arm CROSS_COMPILE=aarch64-linux-gnu- dtbs
```

**Output Location:**
```
${PROJECT_ROOT}/uboot-imx/arch/arm/dts/imx93-11x11-frdm.dtb
```

### Method 2: DTB Only (if defconfig exists)

```bash
cd ${PROJECT_ROOT}/uboot-imx
make ARCH=arm CROSS_COMPILE=aarch64-linux-gnu- imx93-11x11-frdm.dtb
```

### Method 3: Direct DTC Compilation

```bash
cd ${PROJECT_ROOT}/uboot-imx/arch/arm/dts
cpp -nostdinc \
    -I ${PROJECT_ROOT}/uboot-imx/include \
    -I ${PROJECT_ROOT}/uboot-imx/arch/arm/dts \
    -I ${PROJECT_ROOT}/uboot-imx/dts/upstream/src/arm64/freescale \
    -undef -x assembler-with-cpp \
    imx93-11x11-frdm.dts \
    | dtc -I dts -O dtb -o imx93-11x11-frdm.dtb -
```

## Validation: Decompile DTBs

### Linux DTB Validation

```bash
dtc -I dtb -O dts \
    -o ${PROJECT_ROOT}/project/validation/linux.dts \
    ${PROJECT_ROOT}/linux-imx/arch/arm64/boot/dts/freescale/imx93-11x11-frdm.dtb
```

### U-Boot DTB Validation

```bash
dtc -I dtb -O dts \
    -o ${PROJECT_ROOT}/project/validation/uboot.dts \
    ${PROJECT_ROOT}/uboot-imx/arch/arm/dts/imx93-11x11-frdm.dtb
```

## Full Kernel Build (Optional - For Reference)

### Linux Kernel

```bash
cd ${PROJECT_ROOT}/linux-imx
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- imx_v8_defconfig
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- Image dtbs modules -j$(nproc)
```

**Outputs:**
- Kernel: `arch/arm64/boot/Image`
- DTBs: `arch/arm64/boot/dts/freescale/*.dtb`
- Modules: Built in tree

### U-Boot

```bash
cd ${PROJECT_ROOT}/uboot-imx
make ARCH=arm CROSS_COMPILE=aarch64-linux-gnu- imx93_11x11_frdm_defconfig
make ARCH=arm CROSS_COMPILE=aarch64-linux-gnu- -j$(nproc)
```

**Outputs:**
- U-Boot binary: `u-boot.bin`
- SPL: `spl/u-boot-spl.bin`
- DTBs: `arch/arm/dts/*.dtb`

## Notes

1. **Include Paths:** The C preprocessor needs access to DT binding headers
2. **DTC Version:** Minimum 1.4.7, tested with 1.7.0
3. **Kernel Config:** DTB build doesn't require full kernel configuration
4. **U-Boot Config:** defconfig may be needed for proper DT includes

## Troubleshooting

### Missing Include Files

If you encounter "file not found" errors for includes:

```bash
# For Linux
find ${PROJECT_ROOT}/linux-imx/include -name "*.h" | grep dt-bindings

# For U-Boot
find ${PROJECT_ROOT}/uboot-imx/include -name "*.h" | grep dt-bindings
```

### DTC Errors

If DTC reports syntax errors:
1. Check that all referenced phandles exist in imx93.dtsi
2. Verify GPIO/IRQ constants are defined in dt-bindings
3. Ensure memory regions don't overlap

### Build Failures

Common issues:
- Missing CROSS_COMPILE: Set `export CROSS_COMPILE=aarch64-linux-gnu-`
- Wrong ARCH: Use `ARCH=arm64` for Linux, `ARCH=arm` for U-Boot
- Toolchain not found: Install `gcc-aarch64-linux-gnu`
