/**
 * Created by Koo Dong Hyun on 2014-12-01.
 */

$('button#submitemail').bind('click', function(){
   $('#record').css("display: block");
     data= {
           'email': $('#nameinput').val(),
           'url': $('#recordingslist > li > a').attr('href')
     }
    $.post($SCRIPT_ROOT + "/voice", data, function(res){
console.log(res);
    });
    /*
   $.ajax({
       type: 'POST',
       url: $SCRIPT_ROOT + "/voice",
       contentType: "application/json; charset=utf-8",
       data: {
           'email': $('#nameinput').val(),
           'url': $('#recordingslist > li > a').attr('href')
       },
       success: function (response) {
            console.log(response);
       },
       error: function (error) {
            console.log(error);
       }
   });
   */
});