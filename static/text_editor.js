
if (window.addEventListener) { // Mozilla, Netscape, Firefox
    window.addEventListener('load', WindowLoad, false);
} else if (window.attachEvent) { // IE
    window.attachEvent('onload', WindowLoad);
}
window.onload = function WindowLoad(event) {
	//if (document.getElementById('my_text').value.equals'""')
	  //{
	//	  alert("hello")
		//  $('#my_text').val('')
	  //}
	alert(document.getElementById('my_text'))
}
function sendUpdate()
	  {
	  var textArea = document.getElementById('my_text');
	  var text = textArea.value;
	  var ourRequest = new XMLHttpRequest();
	  var params = text;
	  ourRequest.open('POST','/update',true)
	  ourRequest.send(params);
	  }