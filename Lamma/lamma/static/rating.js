function story_Modal()
{
		$('#storyModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-body img').val(recipient)
})
	
}
function story_view(story_id)
{
	$.ajax({
		type:'GET',
		url: '/stories/' + story_id,
		success: function(data){

		}
	})
}

function likehandle(getValue , post_liked_id , liker_id)
{	
	$.ajax({
		type:'GET',
		url:'/like/handle/' + liker_id + post_liked_id + getValue,
		success: function(data){	
		document.getElementById("nbr").innerHTML = data ;
			}
	});

}

function acceptrequest(choice , id)
{
	$.ajax({
		type:'GET',
		url: '/requests/accept_or_delete/' + id + choice,
		success: function(data){
		var number_of_holder = id.toString();
		console.log(number_of_holder);	
		var requestholdername = 'requestwaiting '.concat(number_of_holder);
		console.log(requestholdername);	
		document.getElementById(requestholdername).remove() ;

		}
	});
}
function is_online(user_id)
{
	$.ajax({
		type: 'GET',
		url: '/is_online' + user_id,
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
}