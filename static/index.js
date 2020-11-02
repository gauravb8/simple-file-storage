function listEntries(){
    $.ajax({
        url: '/list',
        cache: false,
        success: function (res) {
            var filenames = res['result']['filenames']
            console.log(filenames)
            content = ""
            for (var name of filenames) {
                content += ('<tr class="listentry"> \
                                             <td><a href="#" id="filelink">'+ name + '</a></td></tr>\n');
            }
            // console.log(content)
            $('#results').html(content);
        },
        error: function (err) {
            console.log(err);
        }
    });
}

$(document).ready(listEntries);


$(document).on('submit', '#uploadform', function(e){
    e.preventDefault();
    //do some verification
    // console.log($('#uploadform').serialize())
    $.ajax({
        url: '/upload',
        method: 'POST',
        data: new FormData(this),
        processData: false,
        contentType: false,
        success: function (res) {
            $('#status').html(res['result']);
            $('#fileinput').val('');
            listEntries();
        }
    });
});


$(document).on('click', '#filelink', function(e){
    console.log('Hi')
    console.log(this.text)
    $.ajax({
        url: 'download/'+this.text,
        method: 'GET',
        success: function(res){
            // window.location.href = res['result']['url']
            $('#image').show()
            $('#image').attr('src', res['result']['url'])

        }
    })    
})