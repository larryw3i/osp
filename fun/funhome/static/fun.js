

function checkCookies(){
    if( Cookies.get('read_privacy') == undefined ){
        makeGlobalAlert(
            gettext("Read our Privacy & Cookies")+
            `<button type="button" class="btn btn-info add-privacy-cookies" `+
            `data-url='/data_privacy'>`+
            gettext("Read Privacy & Cookies")+
            `&gt;&gt;</button>`,
            60*60
        )
    }
}


function makeGlobalAlert( message='Hello',timeout=2.5, type='info' )
{
    $(`<div class="text-center rounded global-alert alert-${type}" role="alert">
        ${message}</div>`)
        .prependTo('body');

    setTimeout(()=>{
        $('.global-alert').remove();
    }, timeout*1000);
}


function refreshLabelList( event )
{
    is_my_label_list = Boolean( Cookies.get('is_my_label_list') );
    Cookies.set(
        'is_my_label_list' ,
        is_my_label_list?'':'1' , { expires: 365 } );
    location.reload();
}


function changeTheme(event){
    Cookies.set(
        'theme',
        event.target.dataset.theme,
        { expires: 365 } );
    location.reload();
}


(function(){
    
    checkCookies();
    
    $('<br/>').insertBefore('.django-ckeditor-widget')

    $(document).on('click', `.theme-dropdown-menu a` , (event) =>{
        changeTheme(event);
    });

    $(document).on('click', `#id_label_list_view_mine_only` , (event) =>{
        refreshLabelList(event);
    });
    
    $(document).on('click', `.language-dropdown-menu .language-dropdown-item` , 
        (event) =>{
            $(`#language_form input[name='language']`)
                .val(event.target.dataset.language);
            $(`#language_form`).trigger('submit');
    });

    $(document).on('click', `.add-privacy-cookies` , (event) =>{
        Cookies.set('read_privacy','1',{ expires: 365 });
        privacy_url = event.currentTarget.dataset.url;
        $('.global-alert').remove();
        window.location = privacy_url;
    });

    $(document).on('click', `[click-to]` , (event) =>{
        $(`${$(event.currentTarget).attr('click-to')}`).trigger('click');
    });   

    $(document).on('click', `.eduhub-label-card` , (event) =>{
        window.location = event.currentTarget.dataset.url;
    });

    $(document).on('click', `.eduhub-label-card` , (event) =>{
        window.location = event.currentTarget.dataset.url;
    });
 
    $(document).on('click', `.click-to-url` , (event) =>{
        window.location = event.currentTarget.dataset.url;
    });

    if( $('.beian_text').text().trim().length < 1 ) $('.beian_text').remove();

})();
