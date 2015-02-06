$(document).ready(function(){

    /* django requires a security token to prevent cross-site request forgery */
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var csrftoken = getCookie('csrftoken');

    $('#sort_button').click(function(){
    	
        // read the data into a javascript object
    	input_items = $('#unsorted').val().split('\n')
    	
        // write simple sorted data to panel 2
    	$("#simple_title").html("A simple alphanumeric sort illustrates the problems outlined above:");
        simple_output = "<ul class=\"list-unstyled\">"
        $.each(input_items.sort(), function(index, value) { 
            simple_output += "<li>" + value + "</li>";
        });
        simple_output += "</ul>";
        $("#simple_data").html(simple_output);
    	
        // smart sort the data for panel 3
    	var inputData={values:input_items};

        // serialize the object into a json string 
        var jsonString = JSON.stringify(inputData);
       
        // post it to the api
        $.post(
            'api/', 	// url 
            jsonString, // data 
            function(data,status){ // callback function, executed if request succeeds 

                // use the json string returned by the API to build the list 
                var result_list = "<ul class=\"list-unstyled\">";
                var matchedCount = 0;
                var unmatchedCount = 0;

                $.each(data.matched, function(index, value) { 
                    result_list += "<li class=\"text-success\">" + value + "</li>";
                    matchedCount++;
                });

                $.each(data.unmatched, function(index, value) {
                    result_list += "<li class=\"text-danger\">" + value + "</li>";
                    unmatchedCount++;
                });
                
                result_list += "</ul>";

                var subtitle = "<span class=\"text-success\">" + matchedCount + " matched</span> ";
                if (unmatchedCount > 0)
                    {subtitle += "and <span class=\"text-danger\">" + unmatchedCount + " unmatched</span> ";}
                subtitle += "items were returned by the API:";
                $("#smart_title").html(subtitle);
                $("#smart_data").html(result_list);
            },        // end callback func 
            'json'    // data type expected from the server 
        ); // end $.post
   	
    	// swap classes on panels and button to make result look primary
        $('#panel_input').removeClass('panel-primary').addClass('panel-default');
        $('#panel_result').removeClass('panel-default').addClass('panel-success');
        $('#panel_simple_sort').removeClass('panel-default').addClass('panel-warning');
        $('#sort_button').blur();
        $('#sort_button').removeClass('btn-primary').addClass('btn-default');
    });
    
    // swap panel and button classes to make input primary
    $( "#unsorted" ).focus(function() {
        $('#panel_input').removeClass('panel-default').addClass('panel-primary');
        $('#panel_result').removeClass('panel-success').addClass('panel-default');
        $('#panel_simple_sort').removeClass('panel-warning').addClass('panel-default');
        $('#sort_button').removeClass('btn-default').addClass('btn-primary');
    });

});  // end document ready 
