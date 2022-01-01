

(function(){

    var funtest_text_bc = new BroadcastChannel('funtest_text_bc');
    funtest_text_bc.onmessage = function( message ){
        var message_data = message.data;

        var test_type_template = ( test_num, test_tip )=> `
        <h5>${ test_num }. ${test_tip}</h5>
        `;
        var test_template = ( test_num, test )=> `
        <h6 style='margin-left:10px;'>${ test_num }. ${test}</h6>
        `;
        var test_selector_template = ( test_num, test )=> `
        <label style='margin-left:15px;'>
            <input type='checkbox'></input> 
            ${ test_num }. ${test}
        </label>
        `;

        var pre_title = message_data.split('\n')[0];
        var title = message_data.split('\n')[1];
        var last_title = message_data.split('\n')[2];

        var test_type_pattern = /\n#\s+/g

        test_types = message_data.split( test_type_pattern );
        test_types = test_types.slice( 1 , test_types.length );

        var global_index = 1;
        
        test_types_html = '';

        // Don't rock the boat
        abcdef = ['A', 'B',  'C', 'D', 'E'];

        test_types.forEach( (value, index, array)=>{
            test_types_html += test_type_template( index+1, 
            value.split('\n')[0] );

            test_questions = value.split( /\n##\s+/g );
            test_questions = test_questions.slice(1 , test_questions.length );
            test_questions.forEach( (q_value, q_index, q_array )=>{
                
                test_question = q_value.split('\n')[0];
                if( String( test_question ).indexOf('( )') > -1 ){

                    test_types_html += test_template( global_index ,  
                        test_question );

                    test_selectors = q_value.split(/\n\S./g);
                    console.log( test_selectors );
                    test_selectors = test_selectors.slice(1, 
                        test_selectors.length);
                    
                    test_selectors.forEach( ( s_value, s_index, s_array )=>{
                        test_types_html += test_selector_template( 
                            abcdef[ s_index],
                            s_value );
                    }  );
                }
                else if( String( test_question ).indexOf('__') > -1 ){

                    test_types_html += test_template( global_index ,  
                        test_question );

                    test_types_html += `
                        <input style='margin-left:15px;' type='text'></input>
                    `;
                }
                else if( String( q_value.split('\n')[1] ).indexOf('TF') > -1 ){
                    test_types_html += `
                        <label  style='margin-left:15px;' >
                            ${global_index}. ${test_question }
                            <input style="margin-left:10px;margin-top:10px;" type='checkbox'>
                            </input> 
                        </label>
                        <br/>
                    ` ;
                }
                else{
                    
                    test_types_html += test_template( global_index ,  test_question );

                    test_types_html +=`
                        <textarea rows='8' style='width:80%;'></textarea>
                    `;
                }

                global_index++;

            });

        });

        $('#test_body').html( test_types_html );

        $('#pre_title').text( pre_title );
        $('#title').text( title );
        $('#last_title').text( last_title );
        

    }

    window.onunload = function(){
        Cookies.remove('is_living');
    }
    
}());
