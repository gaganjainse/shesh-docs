# GPU, power, and the MUX switch

The MSI Sword 16 HX carries a discrete NVIDIA GPU alongside integrated graphics, and the
Shesh body must drive both without cooking the machine. This chapter checks the driver,
the power profiles, and the MUX switch that decides which GPU renders.

> **Note —** This chapter is section 4 of 16 in the
> [Manual Verification Checklist](../../verification/manual-verification.md).

## Driver and power profiles

- [ ] The NVIDIA driver is loaded: `nvidia-smi` shows the GPU with temperature and
      power.
- [ ] `powerprofilesctl list` works and switching between performance, balanced, and
      power-saver takes effect:
  - [ ] `shesh-system-mcp` → `set_power_profile("gaming")` changes the profile.
  - [ ] Hyprland blur and shadow auto-reduce on battery (verify visually).

## The MUX switch and memory budget

- [ ] The MUX switch (if you use it): `sudo msi-mux-switcher status` shows the
      current mode, and switching requires a reboot as documented.
- [ ] GPU VRAM stays within the **5.5 GB** budget when two models load
      (`watch nvidia-smi`).
- [ ] Hybrid graphics routes applications correctly, offloading with
      `__NV_PRIME_RENDER_OFFLOAD=1`.
