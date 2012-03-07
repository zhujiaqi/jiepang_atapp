<%inherit file="layout.tpl" />
<div id="page-home" class="page-home" data-role="page" data-title="@pp - 艾特爱扑 v0.1" data-role="page" data-title="@pp - 艾特爱扑 v0.1"> 
	<div data-role="header" data-position="fixed"><a class="ui-btn-left" data-icon="delete" href="/logout">登出</a><h1><img height="30" width="75" src="/static/css/images/@pp_logo.png" alt=""></h1><a class="ui-btn-right" href="/settings" data-transition="slide"><img height="24" width="24" src="/static/css/images/@PP_icon_forward.png" alt=""></a></div>
	<div data-role="content">
		<ul data-role="listview" data-theme="g">
		% for item in feeds:
			<li style="height:60px; overflow:hidden;">
				<img src="${item['user']['avatar'] and item['user']['avatar'] + '?size=120' or 'http://jiepang.com/static/img/avatar-default-120.gif'}" alt="${item['user']['nick']}" />
				<div class="feed-content">
					<h3>${item['header']}</h3>
					% if 'photo' in item and item['photo']:
						<img height="180" width="180" class="feed-photo" data-src="${item['photo']['url'] + '?size=300'}" src="" alt="loading...">
					% endif
					<div>${item['body']}</div>
				</div>
			</li>
		% endfor
		</ul>
		<!-- <audio controls="controls" autoplay="autoplay" src="http://translate.google.com/translate_tts?ie=UTF-8&q=%E4%BD%A0%E4%BB%96%E5%A6%88%E7%9A%84&tl=zh-CN">不支持</audio> -->
		<a href="/logout">登出</a>
	</div>
</div>
