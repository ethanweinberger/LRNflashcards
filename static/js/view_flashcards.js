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

//CSRF validation functions for POST requests//


$(document).ready(function() {

    $('.antiscroll-wrap').antiscroll();

        var csrftoken = getCookie('csrftoken');
    
    $('.delete').click(function() {
        
        var linkToDelete = $(this).siblings('a');
        var groupname = $('h1').text();
        var flashcardName = linkToDelete.text();
        
        $.ajax({
            beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
            context: this,
            type:"POST",
            url:"/delete_flashcard/",
            data: {"groupname":groupname, "flashcardName": flashcardName},
            success:function(response) {
                $(this).closest('li').remove();
                if ($('#flashcards li').length == 0) {
                    $('#practice').hide();
                }
            }
        });
        
    });
    
    
});