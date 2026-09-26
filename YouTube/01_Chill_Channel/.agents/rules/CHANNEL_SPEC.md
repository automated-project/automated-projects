---
trigger: model_decision
---

# 【Ch 1: Haven Chill Audio】チャンネル制作仕様書 (Channel Specifications)

本ファイルは、**Ch 1: Haven Chill Audio (@Haven-Chill-Audio)** のスクリプトカタログ、Lyria黄金テンプレート＆変数マトリクス、画像型、および確定パラメータを集約した専用仕様書です。

---

## 1. チャンネル概要 & 戦略 (Midnight Study With Me Lofi)

* **チャンネル名**: `Haven Chill Audio`
* **ハンドル**: `@Haven-Chill-Audio`
* **時間帯・ターゲット**: 【深夜〜就寝 / 23:00 - 05:00】3 AM Study、深夜の勉強・作業・読書、深い集中（Deep Focus）、睡眠・癒やし
* **実績・検証結果**:
* **世界観・ビジュアル**: **【非現実リアル現代アート × 深夜の静寂サンクチュアリ（人物完全ゼロ・一人称POV）】**
  * 琥珀色のデスクランプ、雨が打ち付ける大きな窓、静寂な夜の書斎空間。
  * **【1つの美しい超現実（90%リアル × 10%の嘘）】**: 部屋の床一面が穏やかな水鏡（静水面）になっており、満天の星空やランプの光がリアルに反射している。
  * **【映像スタイル】**: **4K静止画アート単体（波形完全OFF・人物完全ゼロ）**。睡眠・深い思考を邪魔しない圧倒的な静寂の空間美。
* **音楽性**: ノスタルジックLofi × 温もりフェルトピアノ
  * 柔らかいフェルトピアノの旋律、心地よいアナログレコードノイズ、控えめで丸みのあるローファイビート（BPM 65〜75）。
  * 休憩曲（雨音・静寂ピアノ）を等間隔（4〜5曲ごと）に配置し、2時間飽きずに勉強・作業できる構成。

---

## 2. 🎵 【黄金テンプレート】Google DeepMind Lyria 3分完全版設計

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

## 3. 📊 【変数マトリクス】15曲パラメータ表 (深夜雨音＆フェルトピアノ)

| # | 曲名 (Title) | Key | BPM | 主楽器 ({CORE_INSTRUMENTS}) | メロディ ({VERSE_MELODY}) | 情景 ({AESTHETIC_THEME}) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | 3 AM Rainy Town | C Maj | 68 | felt upright piano, soft cello | melancholic felt piano motifs | quiet cobblestone night town in rain |
| **02** | Lantern Lit Alley | A Min | 70 | vintage Rhodes, muted acoustic guitar | tender arpeggiated guitar lines | amber lantern glow in a quiet alley |
| **03** | Sleepless Attic Window | F Maj | 66 | upright piano, music box accents | gentle lullaby-like piano notes | rain trickling down a cozy skylight |
| **04** | Midnight Clock Tower | G Maj | 72 | jazzy felt piano, muted upright bass | unhurried walking jazz phrases | distant clock tower over sleeping rooftops |
| **05** | Rain on the Slate Roof | D Min | 67 | soft marimba, tape-saturated piano | hypnotic rhythmic wooden tones | rhythmic rain hitting vintage slate roofs |
| **06** | Quiet Library at Midnight | E Maj | 69 | intimate acoustic piano, warm pads | contemplative slow chord progressions | empty wooden library by rain window |
| **07** | Tram at Last Stop | Bb Maj | 71 | Rhodes piano, soft flute phrases | nostalgic distant melody | vintage tram sitting in quiet night depot |
| **08** | Foggy Canal Bridge | G Min | 65 | cello, delicate piano arpeggios | deep emotive strings and piano | misty canal waters reflecting streetlights |
| **09** | Bakery After Hours | Eb Maj | 70 | warm electric piano, acoustic guitar | comforting sweet chord movements | dark bakery shop with single yellow light |
| **10** | Whispering Pine Rain | D Maj | 68 | felt piano, subtle kalimba chimes | soothing gentle raindrop melody | wet pine trees outside a hillside cottage |
| **11** | Forgotten Toy Workshop | A Maj | 66 | toy piano, felt upright piano | whimsical nostalgic melody | quiet craftsman workshop at 3 AM |
| **12** | Harbor in the Mist | F Min | 72 | muted trumpet, slow piano chords | lonely expressive jazz tones | sleeping fishing harbor under night drizzle |
| **13** | Starless Night Haven | B Min | 67 | upright piano, ambient synth pad | deep reflective piano voicings | peaceful bedroom sanctuary from the storm |
| **14** | Damp Cobblestone Echo | C Min | 70 | nylon guitar, Rhodes, vinyl crackle | delicate Latin-influenced lofi chords | wet reflections on empty old town streets |
| **15** | Dawn Will Come | Ab Maj | 65 | felt piano, soft string quartet swells | hopeful warm resolving harmonies | final quiet hour before the first blue dawn |

---

## 4. 🖼️ 【黄金テンプレート】Imagen 3 ビジュアル生成（暖かい安全な部屋 × 窓の外の静かな違和感・巨大な月）

```text
An ultra-detailed cinematic interior photography, 16:9 widescreen composition.
A cozy, warm minimalist bedroom at midnight, a safe sanctuary from the dark.
A warm wooden desk with an open notebook and an amber glowing vintage desk lamp casting a soft golden pool of light.
Beside the desk, a massive arched floor-to-ceiling glass window with soft rain droplets trickling down.
Just outside the glass, hanging impossibly close in the clear dark starry night sky, is a colossal, softly glowing crescent moon, casting ethereal silver moonlight across the warm wooden floor.
Deep comfort, tranquil solitude, no people, gender-neutral, 85mm f/1.4 lens, hyper-realistic cozy textures, 8k resolution, cinematic masterpiece --ar 16:9
```

---

## 5. ⚙️ 【確定パラメータ】& 【絶対禁止】

### 【確定パラメータ】
* **尺構成**: **2時間長尺（全40〜44曲 / 2時間0分以上）**
* **マスタリング方式**: `Warm Tape Midnight Mastering`
  * **EQ**: `35Hz HPF`, `180Hz +1.8dB` (温かい中低域), `8.5kHz -1.8dB` (耳障りな高域カット), `15kHz LPF`
  * **リミッター**: `alimiter=limit=0.95:level=disabled` 直結（`loudnorm` 完全排除）
* **BPM範囲**: `65〜72 BPM`
* **曲間接続**: `2.5秒 等エネルギーDJクロスフェード`
* **サムネイル制作規約**:
  * **【絶対厳守】動画からのフレーム切り出しは完全禁止。必ずImagen 3等で生成した「高解像度元画像（RAW）」からダイレクト生成する**。
  * **フォント**: `Futura.ttc` (`index=0`, Medium), `100px` / `#FFFFFF`, Amber Glow (`255, 235, 180`)

### 【絶対禁止】
* ❌ **サムネイル生成時の動画切り出し（元画像以外からの作成禁止）**
* ❌ **現代的な派手なネオンサイン・サイバーパンク調・電子機器の過度な露出**
* ❌ **`loudnorm` フィルタの使用（完全永久禁止）**
* ❌ ポモドーロ機能、タイマーUI、電子チャイム音
