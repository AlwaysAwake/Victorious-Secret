/**
 * Created by Koo Dong Hyun on 2014-12-01.
 */

$('button#submitemail').on('click', function(){
    alert('Wait and adjust your angle to allocate eyes, nose, mouth boxes. Then Press R key to enroll your face.');
    $.ajax({
       type: 'POST',
       url: $SCRIPT_ROOT + "/faceregister",
       data: {id:$('#nameinput').val()},
       success: function (response) {
            if(response['result']) {
                alert(response['result']);
                $('#record').css('display', 'block');
            }
        },
       error: function (error) {
            console.log(error);
       }
   });
});

$('button#submitface').bind('click', function () {
    data = {
        'url': $('#recordingslist > li > a').attr('href')
    }
    $.post($SCRIPT_ROOT + "/voice", data, function (res) {
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

$('button#face').on('click', function(){
    alert('Press A key to authenticate your face!');
    $.ajax({
       type: 'POST',
       url: $SCRIPT_ROOT + "/faceauth",
       data: {id:$('#nameinput').val()},
       success: function (response) {
            if(response['result']) {
                alert(response['result']);
            }
        },
       error: function (error) {
            console.log(error);
       }
   });
});