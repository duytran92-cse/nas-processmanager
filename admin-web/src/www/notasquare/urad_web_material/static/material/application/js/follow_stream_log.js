$(document).ready(function(){
    var follow_interval;
    var is_follow = $("#process_status").attr('value');
    console.log(is_follow);
    if (is_follow == "Succeeded"){
        $('#action_follow_stream').attr('id','no_follow_stream');
        $('#no_follow_stream').html('<a class="btn btn-xs btn-primary">No stream</a>');
    }
    $("#action_follow_stream").click(function(){
        follow_interval = setInterval(follow_stream_log,10000);
    });
    if ($("#process_status").val() == "Succeeded" || $("#process_status").val() == "Terminated"){
        clearInterval(follow_interval);
    }

    function follow_stream_log(){
        href = window.location.href;
        url = href + "/stream_log"
        console.log(url);
        var r = (-0.5)+(Math.random()*(1000.99));
        $.ajax({
            url: url,
            type: "GET",
            success: function(result){

                data = JSON.parse(result)[0].fields;
                console.log(data);
                if (data.status == "Succeeded"){
                    console.log(data.log);
                    //$("#follow_log_stream").text(data.log);
                    $('#follow_log_stream').attr('id','no_follow_stream');
                    $('#no_follo_stream').text('No Stream');
                }else{
                    // do my test;
                    console.log(data.log);
                    $("#follow_log_stream").text('');
                    $("#follow_log_stream").text(data.log);

                    $("#process_status").text('');
                    $("#process_status").text('Status: ' + data.status);

                    $("#process_message").text('');
                    $("#process_message").text('Message: ' + data.message);
                    //Scroll Automatically to the Bottom of the Page
                    window.scrollTo(0,document.body.scrollHeight);
                }
            }
        });
    };
});