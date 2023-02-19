function logins() {
	var text = document.getElementById("password").value;
	var url = "/token?pass=" + text
	$.get(url, function(datas) {
		var url = "token/verify?token=" + datas
		$.get(url, function(data) {
			console.log(data)
			if (data == "Yes") {
				setCookie("token", datas, 90)
				window.location.href = '/'
			} else if (data == "No") {
				alert("密码错误")
				document.getElementById("password").value = ""
			}
		})

	})
}
