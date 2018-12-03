function pop_page(pagina, hoogte, breedte) {
//   var hoog = Math.min(hoogte, 500);
//   var breed = Math.min(breedte, 700);
   var breed = breedte;
   var hoog = hoogte;
   if (breed < 250) breed = 250;
   var bigpic = window.open(pagina, 'page_window', 'toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1,resizable=1,copyhistory=0,width='+breed+',height='+hoog+'');
   bigpic.focus();
}

