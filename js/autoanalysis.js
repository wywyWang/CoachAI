function checkfile(sender) {
    // accepted file type
    var validExts = new Array(".mp4");
  
    var fileExt = sender.value;
    fileExt = fileExt.substring(fileExt.lastIndexOf('.'));
    if (validExts.indexOf(fileExt) < 0) {
      alert("File tpye is not acceptable,please upload correct file extension：" + validExts.toString());
      sender.value = null;
      return false;
    }
    else return true;
}

$(function () {
    $('#submit-video').submit(function(e) {
        // avoid empty file upload
        if(document.getElementById('video-uploader').value.length == 0){
            alert("Please upload file.");
            return false;
        }
        e.preventDefault(); // avoid to execute the actual submit of the form.

        var formData = new FormData();
        var dataFile = document.getElementById('video-uploader').files[0];
        formData.append('video_uploader', dataFile);

        for (var key of formData.entries()) {
            console.log(key[0] + ', ' + key[1]);
        }
        console.log("video size in js = ",formData.get('video_uploader')['size'])

        $.ajax({
            type: "POST",
            url: '../cgi-bin/auto_main.py',
            data: formData, 
            contentType: false,
            cache: false,
            processData: false,
            xhr: function() {
                var myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload){
                    myXhr.upload.addEventListener('progress',updateProgress, false);
                    myXhr.upload.addEventListener("load", updateComplete);
                }
                return myXhr;
            },
            success: function(response)
            {
                // console.log(response)
            },
            error: function(error) {
                console.log('Error: ' + error);
            }
        }).done(function(data) {
            console.log(data)
            $('.container').append(data);
        });

    });

    function updateProgress(e){
        console.log("total size",e.total)
        console.log("current upload size",e.loaded)
        if(e.lengthComputable){
            var max = e.total;
            var current = e.loaded;
            var Percentage = (current * 100)/max;
            console.log(Percentage);
        } 
        else{
            console.log("Unable to compute progress information since the total size is unknown")
        } 
     }

    function updateComplete(evt) {
        console.log("The transfer is complete.");
    }
});