---
trigger: model_decision
---

# 【Ch 3: AuraMelody Audio】チャンネル制作仕様書 (Channel Specifications)

本ファイルは、**Ch 3: AuraMelody Audio (@AuraMelody-Audio)** のスクリプトカタログ、Lyria黄金テンプレート＆変数マトリクス、画像型、および確定パラメータを集約した専用仕様書です。

---

## 1. チャンネル概要 & 戦略 (Sunshine Feel-Good Pop)

* **チャンネル名**: `AuraMelody Audio`
* **ハンドル**: `@AuraMelody-Audio`
* **時間帯・ターゲット**: 【朝〜昼 / 07:00 - 15:00】一日の始まり、朝の目覚め、青空ドライブ、夏のモチベーション・エネルギー向上
* **世界観・ビジュアル**: **【Ch 2の朝バージョン（実写シネマティックPOV × 夏の朝の大自然・海岸・都会）】**
  * Ch2と同じくフォトリアル＆シネマティック8Kの高品質実写質感。
  * 眩しい夏の朝陽、青空が広がる海岸線ハイウェイのオープンカー車窓POV、エメラルドグリーンの砂浜、朝の光が差し込むモダンなカフェテラス。
  * **「人物完全ゼロ / 一人称視点（POV）の爽快な朝景色」**。
* **音楽性**: 洋楽アコースティックポップ / アップテンポ・サマーダンスポップ（BPM 125〜130）
  * 明るいアコースティックギター、弾むホーンセクション、軽快な手拍子（Handclaps）、爽快でキャッチーなメロディ。

---

## 2. 🎵 【黄金テンプレート】Google DeepMind Lyria 3分完全版設計

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

## 3. 📊 【変数マトリクス】15曲パラメータ表 (夏の朝・Sunshine Pop)

| # | 曲名 (Title) | Key | BPM | 主楽器 ({CORE_INSTRUMENTS}) | ボーカル ({VOCAL_STYLE}) | 情景 ({AESTHETIC_THEME}) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | Pacific Coast Morning | G Maj | 128 | acoustic guitar, brass horns, handclaps | energetic charismatic male pop vocals | sunny coastal road under clear blue sky |
| **02** | Summer Beachfront Drive | D Maj | 126 | acoustic guitar, joyful whistling, ukulele | bright uplifting female pop vocals | sparkling ocean road with palm trees |
| **03** | Sunrise Canyon Highway | A Maj | 130 | brass stabs, rhythm guitar, bouncy bass | catchy singalong duet harmonies | epic canyon highway under brilliant morning sun |
| **04** | Turquoise Bay Boardwalk | E Maj | 127 | steel drum accents, acoustic guitar, horns | warm energetic male summer vocals | sparkling emerald ocean waves on white sand |
| **05** | Manhattan Morning Sun | C Maj | 128 | whistling hook, piano chords, tambourine | playful sunny male pop vocals | crisp morning sunshine over city avenues |
| **06** | Seaside Terrace Breakfast | F Maj | 125 | acoustic guitar, soft accordion, brass | cheerful sweet female vocals | open-air wooden deck overlooking calm harbor |
| **07** | Golden Summer Horizon | Bb Maj | 129 | driving acoustic strumming, horn fanfare | powerful feel-good chorus vocals | radiant morning sunlight filling the landscape |
| **08** | Island Palms Boulevard | G Maj | 128 | nylon & acoustic guitar, marimba, brass | breezy relaxed male pop vocals | winding tropical island highway to the horizon |
| **09** | Sparkling Surf Morning | D Maj | 130 | crisp handclaps, funk bassline, guitar | uplifting soaring vocal melody | sparkling morning waves rolling onto shore |
| **10** | Rooftop Sunrise Cafe | A Maj | 126 | acoustic guitar, flute, energetic brass | joyful bright female lead vocals | modern rooftop cafe looking over morning city |
| **11** | Open Sky Summer Vibe | E Maj | 128 | full brass section, dance kick, claps | anthem-like summer group choir | vast open blue skies with zero clouds |
| **12** | Malibu Coastline Cruise | C Maj | 127 | ukulele strumming, brass, glockenspiel | sweet lively playful vocals | coastal highway convertible cruise |
| **13** | Sunny Valley Sunrise | F Maj | 125 | acoustic guitar, violin, whistling | heartwarming fresh morning vocals | lush green valley waking up under golden rays |
| **14** | Beachfront Promenade | Bb Maj | 129 | rhythm guitar, brass stabs, handclaps | bouncy fast-paced male vocals | paved beachfront promenade on a fresh morning |
| **15** | Endless Summer Joy | G Maj | 130 | explosive brass fanfare, soaring guitars | triumphant feel-good pop climax | timeless perfect summer morning euphoria |

---

## 4. 🖼️ 【黄金テンプレート】Imagen 3 ビジュアル生成（都会のカフェテラス × 目の前に広がる波打ち際の違和感）

```text
An ultra-detailed bright lifestyle art photography, 16:9 widescreen composition.
A chic, sunlit urban coffee shop terrace on a brilliant morning.
A clean wooden cafe table with an iced glass of coffee, bathed in pure morning sunlight.
Right at the edge of the polished concrete cafe floor, the city pavement suddenly disappears, giving way to a pristine white-sand beach where gentle, sparkling turquoise ocean waves are softly rolling directly onto the edge of the terrace.
Crisp shadows, fresh sea breeze atmosphere meets urban sophistication, vibrant blue morning sky, no people, gender-neutral, uplifting and refreshing surrealism, 85mm lens, 8k resolution, masterpiece --ar 16:9
```

---

## 5. ⚙️ 【確定パラメータ】& 【絶対禁止】

### 【確定パラメータ】
* **マスタリング方式**: `Sunshine Pop & Vocal Air Mastering`
  * **EQ**: `50Hz +4.0dB`, `100Hz +2.5dB`, `250Hz -2.0dB`, `3.5kHz +4.0dB`, `8kHz〜16kHz +3.0dB (Air)`
  * **リミッター**: `alimiter=limit=0.95:level=disabled` 直結（`loudnorm` 完全排除）
* **BPM範囲**: `125〜130 BPM`
* **曲間接続**: `2.5秒 等エネルギーDJクロスフェード`
* **サムネイルフォント**: `Futura.ttc` (`index=2`, Bold), Electric Cyan Glow (`0, 229, 255`)

### 【絶対禁止】
* ❌ **人物（顔・体・手・キャラクター）の配置・プロンプト記述（人物完全ゼロの徹底）**
* ❌ **アニメ調・イラスト調の出力（Ch3はCh2と同じ実写シネマティック8Kに統一）**
* ❌ **`loudnorm` フィルタの使用（完全永久禁止）**
* ❌ 実在する自動車メーカー名・車種名・ブランド名のプロンプト記述
* ❌ 動画本体・サムネイルへのチャンネル名・曲名・価格・年号の焼き込み
