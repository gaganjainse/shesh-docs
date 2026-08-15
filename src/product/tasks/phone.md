# Phone control over ADB

The Shesh body can reach through a cable to your phone and tap the screen for you. This
chapter confirms that link is live, safe, and refuses to touch the wrong parts of the
display.

> **Note —** This chapter is section 7 of 16 in the
> [Manual Verification Checklist](../../verification/manual-verification.md).

## Tap safely

- [ ] ADB debugging is enabled on the phone and `adb devices` lists it.
- [ ] `shesh-phone-mcp` connects and safe-area taps land on screen.
- [ ] Taps **outside the status and navigation bars are refused** — try a coordinate
      at `y=10`.
- [ ] The phone does **not** accept destructive commands without confirmation.

## See and describe

- [ ] Screenshots pull successfully.
- [ ] The vision model can describe a screenshot when you wire it in.
