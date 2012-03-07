<%inherit file="layout.tpl" />
<div data-role="page"> 
	<div data-role="header"><h1>登录</h1></div>
	<div data-role="content">
		<div style="width:300px;margin:10px auto;"><img src="/static/css/images/@pp_logo.png" alt=""></div>
		<form action="index" method="POST" id="login-form">
		<input type="text" name="username" value="" />
		<input type="password" name="password" value="" />
		<input type="submit" value="登录" />
		</form>
	</div>
</div> 
