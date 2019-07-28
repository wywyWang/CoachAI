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
        formData.append('video', dataFile);
        // var url = $(this).attr("action");

        for (var key of formData.entries()) {
            console.log(key[0] + ', ' + key[1]);
        }

        $.ajax({
            type: "POST",
            url: '../cgi-bin/test_main.py',
            data: formData, // serializes the form's elements.
            processData: false,
            success: function(data)
            {
                // console.log(data)
            },
            error: function(error) {
                console.log('Error: ' + error);
            }
        }).done(function(data) {
            console.log(data)
            $('.container').append(data);
            // alert('finished python script');
        });

    });
});