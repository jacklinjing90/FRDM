#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
UBOOT_DIR="${UBOOT_DIR:-$ROOT/uboot-imx}"
LINUX_DIR="${LINUX_DIR:-$ROOT/linux-imx}"
CROSS_COMPILE="${CROSS_COMPILE:-aarch64-linux-gnu-}"
JOBS="${JOBS:-2}"
UBOOT_DEFCONFIG="${UBOOT_DEFCONFIG:-imx93_11x11_frdm_defconfig}"
LINUX_DEFCONFIG="${LINUX_DEFCONFIG:-imx_v8_defconfig}"

need_tool() {
	local tool="$1"
	if ! command -v "$tool" >/dev/null 2>&1; then
		echo "missing required tool: $tool" >&2
		exit 127
	fi
}

need_dir() {
	local dir="$1"
	if [ ! -d "$dir" ]; then
		echo "missing directory: $dir" >&2
		exit 2
	fi
}

need_tool "${CROSS_COMPILE}gcc"
need_dir "$UBOOT_DIR"
need_dir "$LINUX_DIR"

echo "== U-Boot: $UBOOT_DEFCONFIG =="
make -C "$UBOOT_DIR" "$UBOOT_DEFCONFIG"

echo "== U-Boot: full build =="
make -C "$UBOOT_DIR" CROSS_COMPILE="$CROSS_COMPILE" -j"$JOBS"

echo "== Linux: $LINUX_DEFCONFIG =="
make -C "$LINUX_DIR" ARCH=arm64 CROSS_COMPILE="$CROSS_COMPILE" "$LINUX_DEFCONFIG"

echo "== Linux: FRDM i.MX93 DTBs =="
make -C "$LINUX_DIR" ARCH=arm64 CROSS_COMPILE="$CROSS_COMPILE" -j"$JOBS" 	freescale/imx93-11x11-frdm.dtb 	freescale/imx93-11x11-frdm-tianma-wvga-panel.dtb 	freescale/imx93-11x11-frdm-waveshare-7inch-c-panel.dtb
