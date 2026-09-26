---
trigger: model_decision
---

# Ch 2: Velvet Sunset Audio - 音声整音 ＆ 楽曲仕様 (Audio Spec)

本ドキュメントは、Ch 2 (Velvet Sunset Audio) におけるSunset Pop & R&B楽曲パラメータおよび音響整音規格を定めたものである。

---

## 1. 🎵 Google DeepMind Lyria 3分完全版設計

```text
Create a 3-minute catchy, smooth, and infectious Sunset Pop R&B track at {BPM} BPM in the key of {KEY}. Bouncy funk bassline, snappy acoustic drums with finger snaps, warm Wurlitzer electric piano, rhythmic muted electric guitar, {VOCAL_STYLE} with sweet high falsetto and breathy melodic hooks, and {AESTHETIC_THEME}.

[0:00 - 0:15] Intro: Warm Wurlitzer chords with catchy rhythmic finger snaps and subtle vinyl warmth. Intensity: 3.0/10
[0:15 - 0:45] Verse 1: Bouncy funk bassline and tight acoustic drum groove enter. Intimate, charismatic youthful male vocals singing close to the mic with smooth rhythmic flow. Intensity: 5.0/10
[0:45 - 1:00] Pre-Chorus 1: Rising synth pad and sweet vocal falsetto climbs, building effortless anticipation with drum fills. Intensity: 6.5/10
[1:00 - 1:30] Chorus 1 (Hook): Infectious feel-good pop R&B groove! Punchy bass, rhythmic muted guitar strumming, soaring sweet falsetto harmonies, and ultra-catchy melody. Intensity: 7.5/10
[1:30 - 1:50] Verse 2: Pocket groove continues with conversational smooth vocal delivery and playful ad-libs. Intensity: 5.5/10
[1:50 - 2:05] Pre-Chorus 2: Building layered backing harmonies and syncopated snare snaps rising smoothly. Intensity: 6.8/10
[2:05 - 2:35] Chorus 2 (Peak): Full vibrant pop groove! Multi-track falsetto layers, rich electric piano riffs, bouncy bass, and maximum infectious sunset charm. Intensity: 8.0/10 (Peak)
[2:35 - 2:45] Bridge: Stripped-down to rhythmic Wurlitzer chords and expressive close-mic vocal runs. Intensity: 4.0/10
[2:45 - 3:00] Outro: Catchy vocal hook fading out over smooth bassline and sunset breeze reverb. Intensity: 2.0/10
```

---

## 2. 確定パラメータ
* **ボーカル必須**: すべての楽曲に「若々しい (Youthful) / 高め (High-pitched / Falsetto) / 色気・息遣い (Sultry / Breathy / Sensual)」ボーカルを含めること。
* **BPM範囲**: `96〜106 BPM`
* **曲間接続**: `2.5秒 等エネルギーDJクロスフェード（余白保持・無音トリムなし）`
* **Zero-EQ原則**: EQ・`loudnorm` 完全廃止、原音バランス維持 ＋ ピーク保護。
