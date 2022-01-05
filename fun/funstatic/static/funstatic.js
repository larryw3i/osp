



(function(){

    $(document).on('change','[src-for]',(event)=>{
        $(String($(event.target).attr('src-for'))).attr(
            'src',URL.createObjectURL( event.target.files[0]) )
    });    

}());


