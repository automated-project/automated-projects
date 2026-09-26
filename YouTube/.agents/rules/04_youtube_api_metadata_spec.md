# 04: YouTube API ＆ メタデータ運用規約 (YouTube API & Metadata Spec)

本ドキュメントは、YouTube Data APIによる投稿およびメタデータ記述ルールを定めたものである。

---

## 1. メタデータ表記 ＆ API自動反映原則
1. **100% API自動反映**: メタデータ更新はYouTube Data APIスクリプトで自動反映する。
2. **タイトルへの「商用利用OK」等の完全禁止**: 世界観崩壊を防ぐため、タイトルにメタ情報を含めない。
3. **内部技術仕様の排除**: 概要欄やタイトルに「マスタリング方式（LUFS等）」などの内部仕様は書かない。
4. **タイムスタンプ必須化**: 概要欄と固定コメントの両方に `00:00 - Track Title` のタイムスタンプを記載する。
5. **曲名重複時の自動リネーム**: 重複がある場合は世界観に合った一意の曲名へ自動リネームし、完了報告に明記する。

---

## 2. 概要欄 (Description) ライセンスフォーマット

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎁 【CREATOR LICENSE & USAGE】
You can freely use this track in your YouTube videos, Twitch streams, TikToks & Shorts!

✅ Stream-Safe & Content ID Free (No copyright strikes)
✅ Commercial & Non-Commercial Use Free
📋 Required Attribution (Copy & Paste):
   Music: [Channel Name]
   Watch: https://youtu.be/[VideoID]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
