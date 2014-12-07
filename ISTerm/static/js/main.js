/**
 * Created by Koo Dong Hyun on 2014-12-01.
 */

$('button#faceenroll').on('click', function(){
    alert('Wait and adjust your angle to allocate eyes, nose, mouth boxes. Then Press R key to enroll your face.');
    $.ajax({
       type: 'POST',
       url: $SCRIPT_ROOT + "/faceregister",
       data: {id:$('#email').val()},
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

$('button#faceauth').on('click', function(){
    alert('Press A key to authenticate your face!');
    $.ajax({
       type: 'POST',
       url: $SCRIPT_ROOT + "/faceauth",
       data: {id:$('#email').val()},
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