function hidden_info_switch(infoblok) {
   var kiekeboe = document.getElementById(infoblok);
   if (kiekeboe.style.display == "none") {
      kiekeboe.style.display = "inline";}
   else {kiekeboe.style.display = "none";}
}

function hidden_info_off(infoblok) {
   var kiekeboe = document.getElementById(infoblok);
   {kiekeboe.style.display = "none";}
}
