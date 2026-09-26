---
trigger: model_decision
---

# Ch 1: Haven Chill Audio - 音声整音 ＆ 楽曲パラメータ仕様 (Audio Spec)

本ドキュメントは、Ch 1 (Haven Chill Audio) における楽曲生成パラメータおよび音声整音規格を定めたものである。

---

## 1. 🎵 Google DeepMind Lyria 3分完全版設計

```text
Create a 3-minute gentle and intimate {GENRE_MOOD} track at {BPM} BPM in the key of {KEY}. {CORE_INSTRUMENTS}, soft ambient rain soundscape, warm vinyl crackle, mellow tape saturation, and {AESTHETIC_THEME}.

[0:00 - 0:20] Intro: {INTRO_DESC} with gentle rain and tape hiss. Intensity: 2.0/10
[0:20 - 0:50] Verse 1: Slow dusty drum loop (soft muted kick, brushed snare) and {BASS_STYLE} enter. {VERSE_MELODY}. Intensity: 3.5/10
[0:50 - 1:20] Chorus 1: Soft harmonic expansion. Warm felt piano chords, {CHORUS_ACCOMP}, and deep soothing low-end envelopment. Intensity: 5.0/10
[1:20 - 1:50] Verse 2: Beat continues peaceful flow with {VERSE2_FILLS} maintaining deep calming rhythm. Intensity: 3.8/10
[1:50 - 2:20] Chorus 2: Lush cozy texture. Layered piano voicings, {PEAK_ACCOMP}, and continuous gentle rain. Intensity: 5.5/10 (Gentle Peak)
[2:20 - 2:45] Bridge: Stripped-down to {BRIDGE_INST} and isolated rain ambiance. Intensity: 2.5/10
[2:45 - 3:00] Outro: {OUTRO_DESC}, slowly fading out into peaceful night silence. Intensity: 1.0/10
```

---

## 2. 確定パラメータ
* **尺構成**: 2時間長尺（全40〜44曲 / 2時間0分以上）
* **BPM範囲**: `65〜72 BPM`
* **曲間接続**: `2.5秒 等エネルギーDJクロスフェード`
* **Zero-EQ原則**: EQや `loudnorm` は適用せず、原音バランス維持 ＋ ピークリミッターのみ。
