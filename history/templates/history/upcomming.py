{% load i18n %}
{% load history_tags %}  

{% if isFirst %}
	<h1>{% blocktrans %}Upcomming events{% endblocktrans %}</h1>
{% else %}
    {# no header #}
{% endif %}
 
{% for tle in events %}
    <div id="history_event_container_{{ tle.id }}">
        {{ request|renderHistoryEvent:tle|safe }}
		<hr>
    </div>
{% empty %}
    {% blocktrans %}No events scheduled!{% endblocktrans %}
{% endfor %} 
 
{% if hasMoreEvents %}
	<a href="#">{% blocktrans %}Load more events.{% endblocktrans %}</a>
{% else %}
	<!-- the end -->
{% endif %}
