

(function(){

    var funtest_text_bc = new BroadcastChannel('funtest_text_bc');
    $(document).on( 'click', '#id_funtest_content_live' , (event)=>{
        if( ! Cookies.get('is_living') ){
            window.open('/eduhub/funtest_content_preview' , 
                'funtest_content_preview' , '_blank' );
            Cookies.set('is_living',1);
        }

        funtest_text_bc.postMessage( $('#id_test_text').val() );
    });

    $(document).on( 'keyup', '#id_test_text' , (event)=>{
        funtest_text_bc.postMessage( $('#id_test_text').val() );
    });

    
}());
