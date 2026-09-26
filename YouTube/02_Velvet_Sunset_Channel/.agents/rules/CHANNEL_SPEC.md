---
trigger: model_decision
---

# 【Ch 2: Velvet Sunset Audio】チャンネル制作仕様書 (Channel Specifications)

本ファイルは、**Ch 2: Velvet Sunset Audio (@Velvet-Sunset-Audio)** のスクリプトカタログ、Lyria黄金テンプレート＆変数マトリクス、画像型、および確定パラメータを集約した専用仕様書です。

---

## 1. チャンネル概要 & 戦略 (Sunset Pop & R&B — Charlie Puth & Justin Bieber Style)

* **チャンネル名**: `Velvet Sunset Audio`
* **ハンドル**: `@Velvet-Sunset-Audio`
* **時間帯・ターゲット**: 【夕方〜夜 / 17:00 - 22:00】仕事終わりのチルアウト、夕暮れドライブ、カフェ作業、日常を華やかに彩るBGM
* **世界観・ビジュアル**: **【ニューヨーク風の街並み・大自然・浜辺の夕焼け × 秋のイメージ】**
  * 琥珀色（アンバー）とマゼンタのグラデーション、紅葉が舞うブルックリン風の街角、夕暮れのルーフトップから見渡すマンハッタンのスカイライン、黄金色に染まる海岸線と秋のハイウェイ。
  * **「人物完全ゼロ / 一人称視点（POV）の空間美」**。
* **音楽性**: **Charlie Puth / Justin Bieber（Changes / Justice期）風 Sunset Pop & R&B**
  * **【音楽的特徴】**:
    - 弾むファンキーなスラップベース・ムーグベース（Bouncy Funk Bassline）
    - 軽快でタイトなドラムスネア＆フィンガースナップ（Snappy Drums & Finger Snaps）
    - 洗練されたエレクトリックピアノ（Wurlitzer / Rhodes）とカッティングギター
    - **チャーリー・プース風のキャッチーなメロディライン ＆ 艶やかな高音ファルセットボーカル（Catchy Pop Hooks, Sweet High Falsetto, Breathy Modern Vocal Delivery）**
  * **テンポ規格**: **`BPM 95〜108`**（歩く速度〜軽快なドライブに一番気持ちいい極上ミディアムテンポ）
  * **Intensity**: `3.0/10`（イントロ） ➔ `7.5/10`（サビ：キャッチーで心地よいグルーヴ）

---

## 2. 🎵 【黄金テンプレート】Google DeepMind Lyria 3分完全版設計

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

## 3. 📊 【変数マトリクス】20曲パラメータ表 (Charlie Puth & Justin Bieber 風 Sunset Pop & R&B)

| # | 曲名 (Title) | Key | BPM | 主楽器 ({CORE_INSTRUMENTS}) | ボーカル詳細 ({VOCAL_STYLE}) | 情景 ({AESTHETIC_THEME}) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | Autumn Golden Groove | E Maj | 100 | Wurlitzer, bouncy funk bass, snaps | sweet charismatic male falsetto hooks | golden hour autumn beach sunset drive |
| **02** | Brooklyn Sunset Rooftop | D Min | 104 | clean chorus guitar, synth bass, claps | breathy modern R&B vocal runs | NYC skyline rooftop lounge at dusk |
| **03** | Soho Autumn Afternoon | A Maj | 98 | Wurlitzer, muted funky guitar, bass | smooth conversational pop R&B vocals | brownstone street with falling amber leaves |
| **04** | Greenwich Village Latte | F Maj | 102 | jazzy Rhodes, upright slap bass, snaps | soulful high-register male vocals | warm autumn cafe terrace at sunset |
| **05** | Hudson River Night Drive | C Min | 106 | rolling sub-bass, 808 snaps, poly-synth | seductive smooth high-pitched vocal delivery | cinematic NYC riverfront evening cruise |
| **06** | Golden Coast Boulevard | G Maj | 100 | clean funk guitar, warm bassline | bright infectious falsetto melodies | scenic coastal highway with autumn palms |
| **07** | Velvet Twilight Glow | Bb Maj | 105 | Fender Rhodes, punchy funk bass, claps | rich multi-layered sweet vocal harmonies | serene twilight gradient over the city |
| **08** | Amber Dune Breeze | F# Maj | 96 | nylon & electric guitar, analog bass | intimate whisper-pop vocal texture | cool evening breeze over golden sand dunes |
| **09** | Manhattan Sunset Walk | C Maj | 104 | vintage clavinet, groovy slap bass | playful catchy Charlie Puth style hooks | autumn late afternoon Soho avenue walk |
| **10** | Seaside October Twilight | G Min | 98 | soft electric piano, smooth drums | emotional breathy high-tone vocal runs | quiet autumn ocean sunset with gentle surf |
| **11** | Tribeca Loft Afterglow | A Min | 106 | stereo chorus guitar, funk synth bass | syncopated modern R&B vocal ad-libs | dusk settling over cobblestone loft streets |
| **12** | Central Park Golden Hour | D Maj | 100 | acoustic strumming, bouncy Moog bass | warm tender high-falsetto melody | golden leaves and warm park evening light |
| **13** | Chelsea Velvet Lounge | E Min | 102 | muted jazz chords, punchy bass, snaps | smooth soulful pop vocal delivery | boutique hotel lounge in autumn dusk |
| **14** | October Drizzle Cruise | F Maj | 98 | tremolo Rhodes, rain texture, 808s | delicate melodic falsetto runs | October drizzle on convertible glass |
| **15** | Endless Sunset Euphoria | Eb Maj | 105 | rich Wurlitzer, soaring guitar, funk bass | triumphant infectious pop R&B climax | definitive velvet autumn twilight euphoria |
| **16** | Sunset Boulevard Chaser | G Maj | 102 | bouncy slap bass, brass stabs, snaps | effortless Justin Bieber style high-register runs | palm trees silhouetted against purple dusk |
| **17** | Sweet September Lights | B Min | 100 | acoustic guitar, Moog bass, finger snaps | breathy falsetto hooks, rhythmic pocket | warm glowing city street lamps at 6 PM |
| **18** | Highline Sunset Walk | E Min | 104 | Wurlitzer chords, funky chorus guitar | charming conversational male pop delivery | walking the Highline above autumn city streets |
| **19** | Oceanview Amber Horizon | A Maj | 98 | Fender Rhodes, fretless bass, ocean breeze | smooth seductive falsetto harmonies | quiet balcony overlooking twilight sea |
| **20** | Midnight Honey Groove | C Maj | 106 | bouncy synth bass, clavinet, handclaps | addictive celebratory Charlie Puth hooks | vibrant autumn evening finale party drive |

---

## 4. 🖼️ 【黄金テンプレート】Imagen 3 ビジュアル生成（夕暮れの都市交差点 × 鏡面・透明道路の違和感）

```text
An ultra-detailed contemporary urban fine art photography, 16:9 widescreen composition.
An empty, sun-drenched city intersection surrounded by towering brownstone buildings and skyscrapers at a glowing crimson sunset.
The asphalt street surface seamlessly transitions into a flawlessly transparent glass floor, revealing a deep, sunlit underwater cityscape directly beneath the street.
Long golden hour shadows stretching across the warm pavement, traffic lights glowing amber, rich copper and violet twilight sky reflections, no people, gender-neutral, stunning perspective, crisp 85mm lens, 8k resolution, cinematic masterpiece --ar 16:9
```

---

## 5. ⚙️ 【確定パラメータ】& 【絶対禁止】

### 【確定パラメータ】
* **ボーカル必須**: すべての楽曲に**「若々しい（Youthful）/ 高め（High-pitched・Falsetto）/ 色気・息遣い（Sultry・Breathy・Sensual）」**ボーカルを含めること。
* **マスタリング方式**: `Zero-EQ Natural Audio Pipeline`
  * **EQ**: `イコライザー（EQ）加工完全撤廃（Zero-EQ）`
  * **リミッター**: `alimiter=limit=0.95:level=disabled` 直結（`loudnorm` 完全排除）
* **BPM範囲**: **`96〜106 BPM`**
* **曲間接続**: `2.5秒 等エネルギーDJクロスフェード（余白保持・無音トリムなし）`
* **サムネイルデザイン規格**:
  * **フォント**: `/System/Library/Fonts/Supplemental/SignPainter.ttc` (`index=0`, HouseScript)
  * **レイアウト**: **画面中央ジャスト（超巨大インパクト 260px / サブタイトル完全排除）**
  * **カラー & エフェクト**: ソリッドホワイト (`#FFFFFF`) ＋ **Sunset Orange Glow** (`255, 140, 50`) ＋ 濃い黒影

### 【絶対禁止】
* ❌ **ボーカルなし（インストゥルメンタル単体）での出力**
* ❌ 昭和歌謡・スナック感・重厚な低音歌唱（Modern Aesthetic R&Bに限定）
* ❌ **人物（顔・体・手・キャラクター）の配置・プロンプト記述（人物完全ゼロの徹底）**
* ❌ **`loudnorm` フィルタの使用（完全永久禁止）**
* ❌ 実在する自動車メーカー名・車種名・ブランド名のプロンプト記述
* ❌ 動画本体・サムネイルへのチャンネル名・曲名・価格・年号の焼き込み
* ❌ サムネイルへのサブタイトル配置（Ch2はSignPainter中央単体タイトルに限定）
* ❌ **動画タイトルへの再生時間表記（例: 1 Hour, 30-Minute, 2 Hours 等）の記述（Ch2は曲調・世界観表記のみ）**
