// $("form[name=signup").submit(function(e) {
//     var $form = $(this);
//     var $error = $form.find(".error")
//     var data = $form.serialize();

//     $.ajex({
//         url: "/sign-up",
//         type: "POST",
//         data: data,
//         dataType: "json",
//         success: function(resp){
//             console.log(resp);
//         },
//         error: function(resp){
//             console.log(resp);
//         },
//     })

//     e.preventDefault();
// });