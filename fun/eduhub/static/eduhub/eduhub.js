

(function(){

	$(document).on( 'click', '#eduhub_search_submit', (event)=>{
        event.preventDefault();
        if( $(`#eduhub_search_q`).val().length >0 )
        {
            $(`#eduhub_search_form`).submit();
        }
    } );

    $(document).on('click', '.eduhub_search_filter', (event)=>{
        var urlsearch = new URLSearchParams( location.search );
        if( $(event.currentTarget ).hasClass('labels') )
        {
            urlsearch.set( 'filter', 'labels' );
        }
        else
        {
            urlsearch.set( 'filter', 'funcontents' );
        }
        location.href = location.pathname +"?"+urlsearch.toString();
    });

    $(document).on('click','#top_classification_collapse a',(event)=>{
        Cookies.set('classification',$(event.currentTarget).attr('id'))
        window.location.reload()
    });

    $(document).on('change','#id_cover',(event)=>{
        $('.preview-img').attr(
            'src',URL.createObjectURL( event.target.files[0]) )
    });
    

}());


