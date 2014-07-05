//CSRF validation functions for POST requests//

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

//END CSRF functions //
    

$(document).ready(function() {
    
    
    var csrftoken = getCookie('csrftoken');
    var answer;
    var question;
    var true_back;
    var side = $('#side').text();
    var groupname = $("#groupname").text();
    
    //Hides the continue button initially (so the user only sees "submit")
    $("#continue").hide();
    
    //Prevents the page from reloading if the user hits enter
    $("form").submit(function(e) {
        e.preventDefault();
    })
    
    
    //Controlling for when a user hits the ENTER key (id = 13)
    $('#answer').keypress(function(e) {

        
        
        
        continueVisible = $("#continue").is(':visible');
        submitVisible = $("#submit").is(':visible');
        
        //If the user pushes enter and the submit button is visible (meaning continue must be hidden)
        //Then we can proceed with POSTing his results and getting a new flashcard
        if (e.which == 13) {
            //Grabs the user's input (the answer) and the other side of the flashcard (the question)
            
            if (submitVisible) {

                answer = $('#answer').val();
                question = $('#question').text();
                true_back = $('#true_back').text();
                console.log(question);
                console.log(true_back);
                //Makes the input field blank after a response is entered
                $('#answer').val("");

                $.ajax({
                        //Allows the request to proceed while protecting from CSRF attacks
                        beforeSend: function(xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        },
                        type: "POST",
                        url: "/check_flashcard/",
                        data: {"answer": answer, "question": question, "groupname": groupname, "true_back": true_back, 'side': side},
                        success: function(response) {
                            $("#question").html(response);

                            //Switches out the "submit" and "continue" buttons after the request is processed
                            $("#continue").show();
                            $("#submit").hide();
                        }
                });
            }
            else if (continueVisible) {

                $.ajax({
                        beforeSend: function(xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            }
                        },
                        type: "POST",
                        url: "generate_flashcard/",
                        data: {"answer": answer, "question": question, "result": $("#result").html(), 'side': side},
                        context:this,
                        success: function(response) {
                            $('#flashcard').html(response);
                            if (response == "Drill finished!") {
                                console.log("Got here");
                                window.location.replace("results/");
                            }
                        }
                });
            
            
                $("#result").html("&nbsp;");
            
                $("#continue").hide();
                $("#submit").show();
            
            }   
            
        }
    });
    
    //Same as above function, but for when the user pushes the submit button
    $('#submit').click(function() {
       
        var csrftoken = getCookie('csrftoken');
        var answer = $('#answer').val();
        var question = $('#question').html();
        $('#answer').val("");
        
        $.ajax({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                type: "POST",
                url: "/check_flashcard/",
                data: {"answer": answer, "question": question, "groupname": groupname},
                success: function(response) {
                    $("#question").html(response);
                    $("#continue").show();
                    $("#submit").hide();
                }
        });
        
        
    });
    
    //Same code as before, but for when user clicks the button
    $('#continue').click(function() {
        
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            type: "POST",
            url: "/generate_flashcard/",
            data: {"answer": answer, "question": question, "result": $("#result").html()},
            success: function(response) {
                $('#question').html(response);
                        
            }
        });
        

        $("#result").html("&nbsp;");
            
            $("#continue").hide();
            $("#submit").show();
        
    });
});