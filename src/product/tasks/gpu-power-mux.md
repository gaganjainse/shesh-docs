# 4. GPU, power, and MUX (MSI-specific)

> Part of the [Manual Verification Checklist](../../verification/manual-verification.md) — section 4 of 16.

- [ ] **NVIDIA driver loaded**: `nvidia-smi` shows the GPU and temp/power
- [ ] `powerprofilesctl list`; switching performance↔balanced↔power-saver works
  - [ ] `shesh-system-mcp` → `set_power_profile("gaming")` changes it
  - [ ] Hyprland blur/shadow auto-reduce on battery (verify visually)
- [ ] **MUX switch** (if you use it): `sudo msi-mux-switcher status` shows the
      current mode; switching requires a reboot as documented
- [ ] GPU VRAM doesn't exceed the 5.5 GB budget when two models load
      (`watch nvidia-smi`)
- [ ] Hybrid graphics routes apps correctly (offload with `__NV_PRIME_RENDER_OFFLOAD=1`)

---
