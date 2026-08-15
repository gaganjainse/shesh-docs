# First boot on the MSI Sword 16 HX

The first boot is the moment the Shesh body first meets the hardware it was built for.
This chapter lists the hand checks that confirm the MSI Sword 16 HX is running CachyOS
and Hyprland cleanly before any agent is allowed to work.

> **Note —** This chapter is section 0 of 16 in the
> [Manual Verification Checklist](../../verification/manual-verification.md).

## Boot and display

- [ ] Boots into CachyOS and Hyprland without errors.
- [ ] `hyprctl version` works and the keybinds from the desktop fork are active.
- [ ] Resolution holds at **1920×1200 @ 144 Hz** (verify with `hyprctl monitors`).
- [ ] The Quickshell status bar and settings render with no pink placeholders.

## Sound and input

- [ ] Audio works through speakers and the headphone jack — check `wpctl status` and
      play a sound.
- [ ] The microphone works for the wake word and speech-to-text.

## Network and data

- [ ] Network connects over both Wi-Fi and Ethernet.
- [ ] The `~/.local/share/shesh/` directory tree exists after the first run.
