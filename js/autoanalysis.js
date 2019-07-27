function checkfile(sender) {
    // accepted file type
    var validExts = new Array(".mp4");
  
    var fileExt = sender.value;
    fileExt = fileExt.substring(fileExt.lastIndexOf('.'));
    if (validExts.indexOf(fileExt) < 0) {
      alert("檔案類型錯誤，可接受的副檔名有：" + validExts.toString());
      sender.value = null;
      return false;
    }
    else return true;
}

$(function () {
    $('#submit-video').submit(function(e) {
        e.preventDefault(); // avoid to execute the actual submit of the form.
        var data = $('#submit-video').serialize();
        // var url = $(this).attr("action");
        console.log(data);

        $.ajax({
            type: "POST",
            url: '../cgi-bin/test_main.py',
            data: data, // serializes the form's elements.
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