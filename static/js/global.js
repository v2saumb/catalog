(function($) {
    $(".back-btn").bind('click', backButton);

    function backButton() {
        window.history.back();
    }

})(jQuery);