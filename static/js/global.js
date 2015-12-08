(function($) {
    $(".back-btn").bind('click', backButton);

    function backButton() {
        window.history.back();
    }

    if ($("form[name='add_edit_item']") !== undefined) {
        $("form[name='add_edit_item']").find("#pictureurl").bind("change blur", updateImage);

    }

    function updateImage() {
        src = $(this).val();
        $("form[name='add_edit_item']").find("#uploadedimage").attr("src", src);
    }

    function navTriggerClick(event) {
        var targetElm = "cat_" + $(this).attr('id');
        $("#"+targetElm).toggleClass("hide-element");
    }

    if ($(".left-nav-trigger") !== undefined) {
        $(".left-nav-trigger").each(function(event) {
            $(this).bind("click", navTriggerClick)
        });
    }



})(jQuery);