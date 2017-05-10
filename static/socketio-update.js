var socket = io.connect();

function sendUpdate(content) {
	socket.emit('update', content); 
}

socket.on('connect', function() {
socket.emit('joined');}
);
				
				
socket.on('update', function(data_update){
tinyMCE.get('texteditor').setContent(data_update);
	});

socket.on('file_created',function(new_file){
	console.log("created file");
	$("#files-view").append(new_file);
	console.log(new_file);
});

function getFileName(){
	var file_name = prompt("Please enter the name of the new file","example: new_file.txt");
    
    if (file_name != null) {
       socket.emit("create_file",file_name);
    }
}

socket.on('popup-msg', function(msg){
	document.getElementById("myPopup").innerHTML = msg;
	var popup = document.getElementById("myPopup");
	function popMsg() {popup.classList.toggle("show");}
	setTimeout(popMsg, 3500);
	popMsg(); 
	});

socket.on('file-deleted',function(id) {
	console.log(id);
    document.getElementById(id).innerHTML = "";
    var elem = document.getElementById(id);
    elem.parentNode.removeChild(elem);
});