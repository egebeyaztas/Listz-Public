     //FUNCTION FOR FILTERBAR SUGGESTIONS
     var get_data = {};
     $(function () {
         $('#deniyorum').click(function (event) {
             href_url = $(this).closest('.deniyorum-divi').find('p').attr('value')
             //console.log(href_url);
             $.ajax({
                 type: "GET",
                 url: href_url,
                 data: {},
                 success: function (data) {
                     get_data = data;
                     console.log(get_data);
                     //console.log(searchItems2);
                 }
             })
         });
     });

     $(document).ready(function () {
         $('.sidebar_filter').keyup(function () {
             search_ = $(this).parents('h4').next('div').find('.col-xs-12');
             //console.log(search_.closest('div'));
             search_.empty();
             filter_id = $(this).attr('id');
             for (var i = 0; i < get_data[filter_id].length; i++) {
                 if (get_data[filter_id][i].toLowerCase().includes(($(this)).val().toLowerCase().trim()) &&
                     $(this).val().trim().length > 0) {
                     search_.append("<li class='filter-sug-li'><button type='button' id='filterbut' value='" + get_data[filter_id][i] + "' " + "class='filterbut'>" + get_data[filter_id][i] + "</button></li>");
                 }
             }
         });
     });

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

     function remove_from_search(arr, value) {
         var index = arr.indexOf(value);
         if (index > -1) {
             arr.splice(index, 1);
         }
         return arr;
     };

     var post_search_items_cast = {
         "genres": [],
         "actors": [],
         "countries": [],
         "directors": [],
     };

     function ajax_post_filter_data(event, URL_for_post, post_data) {

         var csrftoken = getCookie('csrftoken');
         post_data['csrfmiddlewaretoken'] = csrftoken
         var max = 150;
         var tot, str;
         console.log($('.grid').children('div'));
         event.preventDefault();
         $.ajax({
             type: 'POST',
             url: URL_for_post,
             headers: {
                 "HTTP_X_CSRF_TOKEN": csrftoken
             },

             data: post_data,
             success: function (data) {
                $('#grid').html(data);
                let firstGradient = randomNumber(10,90);
                let colors = ["#ffd0d2","#fffdd0","#d0fffd","#d0d2ff"];
                    $(".grid").children('div').each(function(){   
                        $(".grid").find('.grad-filter').css(
                            "background", "linear-gradient(141deg, "+colors[randomNumber(0,4)]+" "+firstGradient+"%, "+colors[randomNumber(0,4)] + ")"
                        );
                    });
                    function randomNumber(min,max){
                        return Math.floor((Math.random() * max) + min);
                    }
                setTimeout(function()
                {
                    var max = 150;
                    var tot, str;
                    $('.plot').each(function() {
                        str = String($('.plot').html());
                        tot = str.length;
                    str = (tot <= max)
                        ? str
                        : str.substring(0,(max + 1))+"...";
                    $('.plot').html(str);
                    });
                }); // Delayed for example only.
             },
         })
     }
     $(document).on('click', '.filterbut', function () {
         var chosen = $(this).attr("value");

         current_container_for_search_items = $(this).closest('div');
         console.log("fadetoblack", $(this).closest('div'));
         first_parent = current_container_for_search_items.closest('.row')
             .closest('.container-fluid')
             .closest('.responsive-container-for-filters')
             .find('.sidebar_filter');
         post_search_items_cast[first_parent.attr('id')].push(chosen);
         console.log(post_search_items_cast);
         document.getElementById(first_parent.attr('id')).value = "";
         current_container_for_search_items.empty();

         current_container_for_search_items.closest('.row')
             .find('.keep-filter')
             .append("<li><span id='keep-filter-tag'>" + chosen + "</span></li>");
         remove_from_search(get_data[first_parent.attr('id')], chosen);
         var URL_for_post = first_parent.closest('div').closest('aside').find('.deniyorum-divi').find('.for-ajax-posts').attr('value');
         ajax_post_filter_data(event, URL_for_post, post_search_items_cast);
     })

     $(document).on('click', '#keep-filter-tag', function () {
         var span_val = $(this);
         var span_val_to = $(this).html();
         var location_of_span = span_val.closest('div')
             .closest('.row')
             .closest('.container-fluid')
             .closest('.responsive-container-for-filters')
             .find('.sidebar_filter')
         get_data[location_of_span.attr('id')].push(span_val_to);
         span_val.remove();
         remove_from_search(post_search_items_cast[location_of_span.attr('id')], span_val_to);
         var URL_for_post = first_parent.closest('div').closest('aside').find('.deniyorum-divi').find('.for-ajax-posts').attr('value');
         ajax_post_filter_data(event, URL_for_post, post_search_items_cast);
     });