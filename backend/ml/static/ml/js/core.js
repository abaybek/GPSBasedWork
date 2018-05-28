// // Variable to store your files
// var files;

// // Add events
// $('input[type=file]').on('change', prepareUpload);

// // Grab the files and set them to our variable
// function prepareUpload(event)
// {
//     files = event.target.files;
// }

// $(document).ready(function(){
//     console.log('Doc is ready');

// });

// $('form').on('submit', uploadFiles);

// // Catch the form submit and upload the files
// function uploadFiles(event)
// {
//   event.stopPropagation(); // Stop stuff happening
//     event.preventDefault(); // Totally stop stuff happening

//     // START A LOADING SPINNER HERE

//     // Create a formdata object and add the files
//     var data = new FormData();
//     $.each(files, function(key, value)
//     {
//         data.append(key, value);
//     });

//     data.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value);
//     data.append('name', document.getElementsByName('name')[0].value);
//     data.append('email', document.getElementsByName('email')[0].value);

//     $.ajax({
//         url: '',
//         type: 'POST',
//         data: data,
//         cache: false,
//         dataType: 'multipart/form-data',
//         processData: false, // Don't process the files
//         contentType: false, // Set content type to false as jQuery will tell the server its a query string request
//         success: function(data, textStatus, jqXHR)
//         {
//             if(typeof data.error === 'undefined')
//             {
//                 // Success so call function to process the form
//                 submitForm(event, data);
//             }
//             else
//             {
//                 // Handle errors here
//                 console.log('ERRORS: ' + data.error);
//             }
//         },
//         error: function(jqXHR, textStatus, errorThrown)
//         {
//             // Handle errors here
//             console.log('ERRORS: ' + textStatus);
//             // STOP LOADING SPINNER
//         }
//     });
// }



// // $('#submitbtn').click(function(e){
// //     e.preventDefault();

// //     $.ajax({
// //         url : url,
// //         type: "POST",
// //         data : {csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value},
// //         dataType : "json",
// //         success: function( data ){
// //             console.log(data);
// //         },
// //         error: function(e){
// //             console.log('Error');
// //             console.log(e);
// //         }
    
// //     })
// // })


function get_map(pk){
    $.ajax({
        type: "GET",
        url: "/ml/result/"+pk+ "/",
        headers: {
            "Content-Type": "Application/Json"
        },
        error: function(data){
            console.log(data);
        },
        success: function (data){
            console.log(data);
            var mapobj = $("#map_canvas");
            mapobj.append(data);
        }
    })
}


$(document).ready(function(){
    console.log('Doc is ready');
    var pk = parseInt($("#pk").val());
    console.log('Value of pk is '+ pk);
    get_map(pk);
});