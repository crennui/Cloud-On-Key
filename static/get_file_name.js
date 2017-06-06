
/*function getFileName(){
	var file_name = prompt("Please enter the name of the new file","example: new_file");
    
    if (file_name != null) {
       $.get("/create_file",{name:file_name})
    }
} */



function downloadKeyInfo(){
	var win = window.open("https://192.168.1.157:5000/download_key_info", '_blank');
	console.log("open new");
}
