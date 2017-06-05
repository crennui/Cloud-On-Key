
/*function getFileName(){
	var file_name = prompt("Please enter the name of the new file","example: new_file");
    
    if (file_name != null) {
       $.get("/create_file",{name:file_name})
    }
} */

$("input[type='image']").click(function() {
    $("input[id='my_file']").click();
});