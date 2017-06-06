
/*function getFileName(){
	var file_name = prompt("Please enter the name of the new file","example: new_file");
    
    if (file_name != null) {
       $.get("/create_file",{name:file_name})
    }
} */


function myOnSubmit(aForm) {
    //Getting the two input objects
    var inputPassword = aForm['password'];

    //Hashing the values before submitting
    inputPassword.value = sha256_hash(inputPassword.value);
	alert(aForm['password']);
    //Submitting
    return true;
}

function downloadKeyInfo(){
	var win = window.open("https://127.0.0.1:5000/download_key_info", '_blank');
	console.log("open new");
}
