# FRDM-IMX93 Build Scripts

## Overview

This document describes the automated build scripts generated for the FRDM-IMX93 BSP porting project.

## Generated Scripts

### 1. `linux_build_frdm.sh`
- **Location:** `/home/lin/TEST/linux_build_frdm.sh`
- **Purpose:** Builds Linux kernel DTB for FRDM-IMX93
- **Output:** `linux-imx/arch/arm64/boot/dts/freescale/imx93-11x11-frdm.dtb`
- **Validation:** Generates decompiled DTS to `project/validation/linux.dts`

### 2. `u-boot_build_frdm.sh`
- **Location:** `/home/lin/TEST/u-boot_build_frdm.sh`
- **Purpose:** Builds U-Boot DTB for FRDM-IMX93
- **Output:** `uboot-imx/arch/arm/dts/imx93-11x11-frdm.dtb`
- **Validation:** Generates decompiled DTS to `project/validation/uboot.dts`

## Usage

### Build Both DTBs
```bash
cd /home/lin/TEST
./linux_build_frdm.sh
./u-boot_build_frdm.sh
```

### Using FWAuto
The build scripts are integrated with FWAuto. Use the `/build` command:
```
/build
```

This will execute both scripts automatically as configured in `.fwauto/config.toml`.

## Build Process

Each script follows the BSP porting skill methodology:

1. **Copy DTS:** Copies the working DTS file to source tree
2. **Preprocess:** Uses C preprocessor to expand includes and macros
3. **Compile:** Uses device tree compiler (dtc) to generate DTB
4. **Validate:** Decompiles DTB back to DTS for verification

## Outputs

### Linux DTB
- **Binary:** 42 KB
- **Decompiled:** 2018 lines
- **Status:** ✅ Built and validated

### U-Boot DTB
- **Binary:** 37 KB
- **Decompiled:** 1696 lines
- **Status:** ✅ Built and validated

## Dependencies

All required tools are available:
- `dtc` v1.7.0
- `cpp` (C preprocessor)
- `aarch64-linux-gnu-gcc` v13.3.0

See `dependency_list.md` for complete tool information.

## Validation

Both scripts include automatic validation:
- DTB is decompiled back to DTS format
- Line count is reported
- Output file existence is verified
- Build errors are caught and reported

## Integration with BSP Porting Workflow

These scripts complete Step 10-12 of the BSP porting skill:
- ✅ Step 10: Cross-checked validation DTS against table.md
- ✅ Step 11: No driver changes required
- ✅ Step 12: Final build summary and reproducible commands

## Troubleshooting

### Script Execution Errors
```bash
# Ensure scripts are executable
chmod +x linux_build_frdm.sh u-boot_build_frdm.sh

# Check environment variables
echo $ARCH $CROSS_COMPILE
```

### DTB Build Failures
Check:
1. DTS syntax errors in source files
2. Missing include files
3. Toolchain availability

### Validation Failures
If decompiled DTS is missing nodes:
1. Check preprocessing output
2. Verify include paths
3. Review dtc warnings

## Next Steps

After successful DTB builds:
1. Flash DTBs to target hardware
2. Boot test with real FRDM-IMX93 board
3. Verify peripheral functionality against `table.md`
4. Update DTS based on runtime testing

## Related Documentation

- `table.md` - Hardware comparison (68 items)
- `build_commands.md` - Detailed build instructions
- `FINAL_SUMMARY.md` - Complete BSP analysis
- `CHECKLIST.md` - Progress tracking
