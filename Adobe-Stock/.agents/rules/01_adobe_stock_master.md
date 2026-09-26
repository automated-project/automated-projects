---
trigger: model_decision
---

# Adobe Stock マスター方針 (Adobe Stock Master Rules)

本ドキュメントは、Adobe Stock出品における基本方針およびGemini Web生成ワークフローを定めたものである。

---

## 1. 制作パイプライン
Web版Gemini (Imagen 3) で生成した静止画および動画を `tools/upscale_adobe_stock_4k.py` で4K化・クロップ処理して出品する。

---

## 2. デイリー生成配分
* **静止画 6枚**: コスメ、建築、金融、バイオ、スマート工場、環境建築
* **商用動画 3本**: 水面ポディウム、モダン建築の光と影、朝焼け役員室スカイライン
