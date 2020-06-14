$(document).ready(function(){
    array_btn_stop = $('[id="btn_stop"]');
    //console.log(array_btn_stop);

    function select_tr_running(array_btn_stop){
        var i = 0;
        array_is_show = [];
        array_btn_stop.each(function(){
            i += 1;
            //console.log(this);
            //console.log($(this).closest('table').attr('id'));
            //console.log($("table tbody tr:nth-child(2)"));
            show_btn_stop = $(this).attr('value').split(",")[0]
            // test = Succeeded | Running
            if (String(show_btn_stop) == "Running"){
                array_is_show.push(i);
                console.log(show_btn_stop);
            }
        });
        return array_is_show;
    }
    function enable_btn_stop(array_is_show){
        for (var i = 0; i < array_is_show.length; i++) {
            console.log(array_is_show[i]);
            $("table tbody tr:nth-child("+array_is_show[i]+") #btn_stop").css("display","block");
        };
        console.log(array_is_show);
    }
    array_is_show = select_tr_running(array_btn_stop);
    enable_btn_stop(array_is_show);

    $("#data-table-basic #btn_stop").click(function(){
        url = location.protocol + "//" + location.hostname + "/process/stop";
        console.log($(this).attr('value'));
        value = $(this).attr('value').split(",");
        url += "/" + value[1];
        console.log(url);

        $.ajax({
            url: url,
            type: "GET",
            success: function(result){
                data = JSON.parse(result)[0].fields
                if (String(data.status) == 'Stop'){
                    location.reload();
                }
                console.log(data);
            }
        });

    });
});