(function($) {
    $(".back-btn").bind('click', backButton);

    function backButton() {
        window.history.back();
    }

    if($("form[name='add_edit_item']") !== undefined){
    	$("form[name='add_edit_item']").find("#pictureurl").bind("change blur", updateImage);
    	
    }

    function updateImage(){
    	src = $(this).val();
    	$("form[name='add_edit_item']").find("#uploadedimage").attr("src", src);
    }

})(jQuery);