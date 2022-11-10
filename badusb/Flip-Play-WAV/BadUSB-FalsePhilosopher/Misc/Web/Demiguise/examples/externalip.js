<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>

var getKey = function (){
   var ip = $.ajax({ 
      url: 'https://api.ipify.org?format=json', 
      async: false
   }).responseJSON.ip;
   return ip;
}