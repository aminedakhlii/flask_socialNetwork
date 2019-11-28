var followbtn = document.getElementById("follow");
followbtn.addEventListenner("click" , function()
{
	var request = new XMLHttpRequest(); 
	request.onload = function() {
		if ({{ followed_or_not }} == 'follow') 
			{{ followed_or_not }} = 'following';
		else {{ followed_or_not }} = 'follow' ;
	}
})
/*function is_online(user_id)
{
	$.ajax({
		type: 'GET',
		url: '/is_online/' + user_id,
		success: function(data){
			const status = document.querySelector('.status');
			let i = parseInt(data);
			if (i == 1)
			{
				status.innerHTML = 'online' ; 
			}
			else 
			{
				status.innerHTML = 'offline';
			}
		}
	})
}*/
