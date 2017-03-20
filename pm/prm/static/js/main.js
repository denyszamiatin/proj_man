$( document ).ready(function() {

    var show_content = load_more($('table tbody tr'), $( ".btn_load_more" ), 5, 2)
    show_content()


    $(".members .dropdown-menu li").each(function(){
        checkbox = $(this).find('input')
        if (checkbox.is(":checked")){
            var l_members =  $(".members_list").text()  +  $(this).text() + ', '
            $(".members_list").text(l_members)
        }
    })

    $(".members .dropdown-menu li").on( "click", function(event) {
        event.stopPropagation();

        checkbox = $(this).find('input')

        if (checkbox.is(":checked")){
            $(this).find('input').prop('checked', false);
            var l_members =  $(".members_list").text().replace($(this).text() + ', ', '')
            $(".members_list").text(l_members)
        }else{
            $(this).find('input').prop('checked', true);
            var l_members =  $(".members_list").text()  +  $(this).text() + ', '
            $(".members_list").text(l_members)
        }

    });

    $(".members .dropdown-menu li input").on( "click", function(event) {
        if ($(this).is(":checked")){
            $(this).prop('checked', false);
        }else{
            $(this).prop('checked', true);
        }

    });


});




function load_more(list_of_obj, button, start, step){
    var count = 0

    button.on( "click", function() {
      show_content(step)
    });

    console.log($('table tbody tr').length)

    function show_content (nmb) {
        number = nmb || start
        count +=number
        list_of_obj.each(function(index) {
            if (index < count){
                $(this).css('display', 'table-row')
                $(this).animate({opacity : 1}, 300)
            }
        })

        if ( count >= list_of_obj.length) {
            button.css('display', 'none')
        }

    }

    return show_content
}