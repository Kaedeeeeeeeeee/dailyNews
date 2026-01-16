# 🤖 AI最新ニュース【{{ date }}】

> 本日のAI業界の最新ニュースをお届けします。

## 目次

{% for item in news_items %}
{{ loop.index }}. [{{ item.source }}] {{ item.title }}
{% endfor %}

---

{% for item in news_items %}
## {{ loop.index }}. 【{{ item.source }}】{{ item.title }} {{ item.emoji }}

{% if item.images %}
{% for image in item.images %}
![{{ item.source }}の画像]({{ image }})
{% endfor %}
{% endif %}

{{ item.summary_ja }}

📎 [原文を見る]({{ item.url }})

---

{% endfor %}

📅 更新日時：{{ datetime }}
🔗 [フォローしているアカウント一覧](#)
