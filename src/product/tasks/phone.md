# 7. Phone (shesh-phone, Realme Narzo)

> Part of the [Manual Verification Checklist](../../verification/manual-verification.md) — section 7 of 16.

- [ ] ADB debugging enabled on the phone; `adb devices` lists it
- [ ] `shesh-phone-mcp` connects (safe-area taps land on screen)
- [ ] Taps **outside the status/nav bars are refused** (try a coordinate at y=10)
- [ ] Screenshots pull successfully
- [ ] Vision model can describe a screenshot if you wire it
- [ ] The phone does **not** accept destructive commands without confirmation

---
