<%inherit file="layout.tpl" />
<div id="page-settings" data-role="page" data-title="@pp - 艾特爱扑 v0.1"> 
	<div data-role="header" data-position="fixed"><a class="ui-btn-left" href="/home?words=1"><img height="24" width="24" src="/static/css/images/@PP_icon_back.png" alt=""></a><h1><img height="30" width="75" src="/static/css/images/@pp_logo.png" alt=""></h1></div>
	<div data-role="content">
		<div data-role="fieldcontain">
			<fieldset data-role="controlgroup" id="checkboxes">
				% for item in left:
					<a class="delete-word" data-role="button" data-icon="delete" data-word="${item['word']}" data-iconpos="notext">删除</a>
					<input type="checkbox" name="checkbox-${item['id']}" id="checkbox-${item['id']}" class="custom checkbox-item" data-word="${item['word']}"
					% if item['status'] == 1:
						checked
					% endif
					 />
					<label for="checkbox-${item['id']}">${item['word']} @ ${item['created_on']}</label>
				% endfor
			</fieldset>
		</div>
		<div data-role="fieldcontain">
			<input type="text" name="name" id="add-text" value=""  />
			<a href="javascript:void(0)" id="add-button" data-role="button" data-icon="add" data-inline="true">Add</a>
		</div>
	</div>
</div>
