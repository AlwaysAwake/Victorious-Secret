/**
 * Created by Koo Dong Hyun on 2014-12-01.
 */

$('button#submitemail').bind('click', function(){
   $('#record').css("display: block");
   $.ajax({
       url: $SCRIPT_ROOT + "/signin",
       contentType: "application/json; charset=utf-8",
       type: 'POST',
       success: function (response) {
            console.log(response);
       },
       error: function (error) {
            console.log(error);
       }
   });
});