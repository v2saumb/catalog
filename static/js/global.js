(function($) {
    /*add the back button functionality*/
    $(".back-btn").bind('click', backButton);

    /*bind method for picture preview */
    if ($("form[name='add_edit_item']") !== undefined) {
        $("form[name='add_edit_item']").find("#pictureurl").bind("change blur", updateImage);

    }
    /* navigation trigger for parent categories */
    if ($(".left-nav-trigger") !== undefined) {
        $(".left-nav-trigger").each(function(event) {
            $(this).bind("click", navTriggerClick);
        });
    }
    /* navigation trigger for sub categories */
    if ($("ul.left-nav-ul li.left-nav-item") !== undefined) {
        $("ul.left-nav-ul li.left-nav-item").each(function(event) {
            $(this).bind("click", nav_item_click);
        });
    }

    /* bind click to the catalog tiles */
    if ($(".catalog-item") !== undefined) {
        $(".catalog-item").each(function(event) {
            $(this).bind("click", nav_item_click);
        });
    }

    /* bind validation for category name */
    if ($("form[name='category_form']") !== undefined) {
        $("form[name='category_form']").find("#name").bind("keydown", inputValidator);
    }
        /* bind validation for category name */
    if ($("form[name='add_edit_item']") !== undefined) {
        $("form[name='add_edit_item']").find("#name").bind("keydown", inputValidator);
    }
    /* bind method to scroll top */
    if ($("#back-to-top") !== undefined) {
        $("#back-to-top").bind("click", goToTop);
    }
    /* Auto close alerts */
    $("#alert-message").fadeTo(2000, 500).slideUp(500, function() {
        $("#alert-message").each(
            function(event) {
                $(this).alert('close');
            }
        );
    });

    /*function to scroll to the top of the page*/
    function goToTop(event) {
        $("html, body").animate({
            scrollTop: $('#backtotop').offset().top
        }, 1500);
        event.preventDefault();
        event.stopPropagation();
        return false;
    }

    /*function open left navigation */
    function nav_item_click(event) {
        window.location.href = $(this).attr('data-items-url');
    }

    /*function for key up validation to avoid special characters*/
    function inputValidator(event) {
        var blockedKeys = [192, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 189, 187, 188, 190, 191]
        if ($.inArray(event.keyCode, blockedKeys) >= 0) {
            event.keyCode = 0;
            event.preventDefault();
            return;
        }
    }
    /*function back button */
    function backButton() {
        window.history.back();
    }

    /*function to show image preview*/
    function updateImage() {
        src = $(this).val();
        if (src != undefined && src !=""){
           $("form[name='add_edit_item']").find("#uploadedimage").attr("src", src);
        }
    }

    /*function showing and hiding the category menu items */
    function navTriggerClick(event) {
        var targetElm = "cat_" + $(this).attr('id');
        var icon = $(this).find(".nav-parent-icon > i")
        if(icon.hasClass('fa-minus')){
            icon.removeClass('fa-minus').addClass('fa-plus');
        }else{
            icon.removeClass('fa-plus').addClass('fa-minus');
        }
        $("#" + targetElm).toggleClass("hide-element");
    }

})(jQuery);