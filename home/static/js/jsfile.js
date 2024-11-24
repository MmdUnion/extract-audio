



$(document).ready(function(){
    $("progress").hide()
    $(".file-status").hide()

})


$("input:file").change(function (){
    var filePath = $(this).val();
    var filename = filePath.replace(/^.*[\\\/]/, '')
    $(".custom-file-label").html(filename);
})



$('.upload-button').on('click', function (event) {
    if (!$('.upload-button').attr("href")){
        event.preventDefault();
        fileElem = $("input:file").val()
        if (fileElem) {
            $.ajax({
                beforeSend: function () {
                    $("progress").show()
                    $(".upload-button").hide()
                    $(".file-status").html("Uploading...")
                    $(".text-headers").html("Uploading...")

                    $(".file-status").show()
    
    
                },
                  success: function (data) {
                    
                    if (data.status === "ok") {
                        $(".file-status").html("Processing...")
                        $(".text-headers").html("Processing...")

                        let timerId = setInterval(function() {
                            $.ajax({
                                url: window.location.origin+"/status/",
                                data: { file_id: data.file_id, csrfmiddlewaretoken:$('input[name="csrfmiddlewaretoken"]').val()},
                                type: 'POST',
                                dataType: 'json',
                                success: function(response) {
                                    if (response.status === "Success") {
                                        $("progress").hide()
                                        $(".file-status").hide()
                                        $(".download-button").show()
                                        
                                        var media = $('.input-group');
                                        media.append(`<audio controls class="justify-content-center mx-auto mb-3" style="width: 600px;"><source class="audio-source" src="${window.location.origin + "/"+ response.audio_url}" type="${response.mime_type}"></audio>`);
                                        $(".download-button").attr({href:window.location.origin + "/"+ response.audio_url})
                                        $(".custom-file-label").hide()
                                        $(".custom-file-input").hide()

                                        $(".download-button").html("Download Audio")
										$(".download-button").attr("download", "")
                                        $(".download-button").css("background-color", "#2999d6")
                                        $(".text-headers").html("Your audio file is ready...")
                                        clearInterval(timerId);
                                    }
                                    else if (response.status === "Failed") {
                                        $("progress").hide()
                                        $(".file-status").html("Failed")
                                        $(".text-headers").html("Failed")

                                        $(".upload-button").show()
                                        clearInterval(timerId);
                                        
                                    }
                                    else if (response.status === "File not found") {
                                        $(".file-status").html("File not found")
                                        $(".text-headers").html("File not found")

                                        clearInterval(timerId);
                                        
                                    }
                                },

                                
                            })
                            
                          }, 3500);







                        




                    }
                    else{
                        $("progress").hide()
                        $(".text-headers").html("Failed...")

                        $(".file-status").html("Failed...")
                        $(".upload-button").show()
    
    
                    }
    
                  },
                  error: function () {
                    $("progress").hide()
                    $(".file-status").html("Failed...")
                    $(".text-headers").html("Failed...")

                },
                
                url: window.location.origin +'/upload/',
                type: 'POST',
                // data:$('form')[0].serialize(),
                data: new FormData($('form')[0]),
                cache: false,
                contentType: false,
                processData: false,
            
                xhr: function () {
                    var myXhr = $.ajaxSettings.xhr();
                    if (myXhr.upload) {
                        // For handling the progress of the upload
                        myXhr.upload.addEventListener('progress', function (e) {
                        if (e.lengthComputable) {
                            $('progress').attr({
                            value: e.loaded,
                            max: e.total,
                            });
                        }
                        }, false);
                    }
                
                    return myXhr;
                }
                });
    
        }
        else{
            alert("Please first Choose a file! ");
        }
    }
    else{
        alert("Please first Choose a file! ");
    }
    });







