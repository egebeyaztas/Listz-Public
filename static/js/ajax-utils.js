function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  //FUNCTION FOR GETTING THE COMMON LISTS PAGE
  $(function () {
    $('#lists-common-button').click(function (event) {
      var csrftoken = getCookie('csrftoken');
      event.preventDefault()
      $.ajax({
        type: "POST",
        async: true,
        url: "{% url 'lists-common-by-ajax' %}",
        headers: {
          "HTTP_X_CSRF_TOKEN": csrftoken
        },
        data: {
          'csrfmiddlewaretoken': csrftoken
        },
        success: function (data) {
          $('#grid_view').html(data);
        }
      })

    });
  });