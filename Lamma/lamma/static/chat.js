function send_message(message , user_id){
	$.ajax({
		type:'POST',
		url: '/chatting/message/'+ message +'/' + user_id ,
		dataType: 'json',
		success: function(data){
			const html = data.map(function(message){
				
				let color , bg , roundedval , mbval , textmessage , floatright; 
				
				if (message.sender == user_id) {
					bg = 'bg-light';
					roundedval = '75';
					floatright = '';
					textmessage = 'message-text';
					mbval = '1';
					color ='black-text'; }
					else {
						bg = '';
						roundedval ='50'; 
						floatright = 'float-right';
						mbval ='2'
						textmessage = '';						
						color = 'text-white';
				}
			return `
              <div class="card ${bg} rounded w-${roundedval} ${floatright} z-depth-0 mb-${mbval} ${textmessage}"
              style="background-color:#dc5379;">
                <div class="card-body p-2">
                  <p class="card-text ${color}">${ message.message }</p>
                </div>
              </div>
              </br></br></br>
          `			
		}).join('');
			const messages_ = document.querySelector('.messages');
			messages.innerHTML = html;
			messages.scrollTop = messages.scrollHeight;
			

		}
	});
}



