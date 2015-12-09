(function($) {
    $(".back-btn").bind('click', backButton);

    if ($("form[name='add_edit_item']") !== undefined) {
        $("form[name='add_edit_item']").find("#pictureurl").bind("change blur", updateImage);

    }

    if ($(".left-nav-trigger") !== undefined) {
        $(".left-nav-trigger").each(function(event) {
            $(this).bind("click", navTriggerClick)
        });
    }
    if ($("ul.left-nav-ul li.left-nav-item") !== undefined) {
        $("ul.left-nav-ul li.left-nav-item").each(function(event) {
            $(this).bind("click", nav_item_click)
        });
    }

    if ($(".catalog-item") !== undefined) {
        $(".catalog-item").each(function(event) {
            $(this).bind("click", nav_item_click)
        });
    }


    if ($("form[name='category_form']") !== undefined) {
        $("form[name='category_form']").find("#name").bind("keydown", inputValidator);
    }



    function nav_item_click(event) {
        window.location.href = $(this).attr('data-items-url');
    }

    function inputValidator(event) {
        var blockedKeys = [192, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 189, 187, 188, 190, 191]
        if ($.inArray(event.keyCode, blockedKeys) >= 0) {
            event.keyCode = 0;
            event.preventDefault();
            return;
        }
    }

    function backButton() {
        window.history.back();
    }


    function updateImage() {
        src = $(this).val();
        $("form[name='add_edit_item']").find("#uploadedimage").attr("src", src);
    }

    function navTriggerClick(event) {
        var targetElm = "cat_" + $(this).attr('id');
        $("#" + targetElm).toggleClass("hide-element");
    }




})(jQuery);