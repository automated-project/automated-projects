---
trigger: model_decision
---

# Ch 3: AuraMelody Audio - 音声整音 ＆ 楽曲仕様 (Audio Spec)

本ドキュメントは、Ch 3 (AuraMelody Audio) におけるSunshine Pop楽曲パラメータおよび音響整音規格を定めたものである。

---

## 1. 🎵 Google DeepMind Lyria 3分完全版設計

```text
Create a 3-minute joyful and infectious summer {GENRE_MOOD} track at {BPM} BPM in the key of {KEY}. Upbeat acoustic guitar strumming, bright brass section, crisp handclaps, bouncy bassline, {VOCAL_STYLE}, and {AESTHETIC_THEME}.

[0:00 - 0:15] Intro: Bright acoustic guitar chords with cheerful whistling hook and crisp handclaps. Sunny morning atmosphere. Intensity: 3.5/10
[0:15 - 0:40] Verse 1: Four-on-the-floor kick and bouncy acoustic bass enter. Smooth energetic pop vocals singing an infectious happy rhythm. Intensity: 5.5/10
[0:40 - 0:55] Pre-Chorus 1: Rising brass stabs and driving tambourine build anticipation. Vocals climb in pitch to an energetic drum fill. Intensity: 7.5/10
[0:55 - 1:25] Chorus 1 (Drop): Pure dopamine feel-good explosion! Punchy dance kick, soaring horn lines, bright acoustic guitar, and catchy singalong chorus. Intensity: 9.0/10
[1:25 - 1:45] Verse 2: Bouncy groove with {VERSE2_ELEMENTS} and conversational joyful vocal delivery. Intensity: 6.0/10
[1:45 - 2:00] Pre-Chorus 2: Rapidly building snare snaps, layered group harmonies, and swelling horns rising to maximum excitement. Intensity: 8.5/10
[2:00 - 2:30] Chorus 2 (Main Peak): Ultimate celebratory climax! Full brass section, soaring choir harmonies, driving dance drums, and radiant summer joy. Intensity: 10.0/10 (Peak)
[2:30 - 2:45] Bridge: Stripped-down acoustic guitar and playful vocal ad-libs with clapping rhythm. Intensity: 4.0/10
[2:45 - 3:00] Outro: Catchy whistling hook over fading acoustic guitar strum and morning breeze reverb. Intensity: 2.0/10
```

---

## 2. 確定パラメータ
* **BPM範囲**: `125〜130 BPM`
* **曲間接続**: `2.5秒 等エネルギーDJクロスフェード`
* **Zero-EQ原則**: EQ・`loudnorm` 完全廃止、原音バランス維持 ＋ ピーク保護。
