---
layout: default
title: Adventures
permalink: /adventures/
show_hero: false
---

Here are all our adventures:

<ul>
{% for post in site.posts %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <small>{{ post.date | date: "%B %-d, %Y" }}</small>
  </li>
{% endfor %}
</ul>