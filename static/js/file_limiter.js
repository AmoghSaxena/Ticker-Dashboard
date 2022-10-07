function Filevalidation(id)
{
    FileTypeChecker(id);
    var fi;
    if (id=="static_image_cond")
    {fi = document.getElementById("static_image_cond");}

    if (id=="primary_logo_cond")
    {fi = document.getElementById("primary_logo_cond");}
    
    if (id=="animation_video_cond")
    {fi = document.getElementById("animation_video_cond");}
    
    if (fi.files.length > 0)
    {
        for (const i = 0; i <= fi.files.length - 1; i++)
        { 
            const fsize = fi.files.item(i).size;
            const file = Math.round((fsize / 1024));
            // The size of the file.
            if (file >= 5120)
            {
                alert("File too Big, please select a file less than 5MB");
                if (id=="static_image_cond")
                {
                    document.getElementById("static_image_cond").value='';
                }
                if (id=="primary_logo_cond")
                {
                    document.getElementById("primary_logo_cond").value='';
                }
                
                if (id=="animation_video_cond")
                {
                    document.getElementById("animation_video_cond").value='';
                }
            }
        }
    }
}

function FileTypeChecker(id)
{
    if (id=="static_image_cond" || id=="primary_logo_cond")
    {
        var fileInput;

        if (id=="static_image_cond")
        {fileInput = document.getElementById("static_image_cond").files[0];}

        if(id=="primary_logo_cond")
        {fileInput = document.getElementById("primary_logo_cond").files[0];}

        var allowed = ["png"];
        var found = false;

        allowed.forEach(function(extension) {
        if (fileInput.type.match('.'+extension)) {
            found = true;
        }
        })

        if(found) {
        }
        else{
        alert("Allowed file type is PNG");

        if (id=="static_image_cond")
        {document.getElementById("static_image_cond").value='';}

        if(id=="primary_logo_cond")
        {document.getElementById("primary_logo_cond").value='';}        
        }
    }

    if (id=="animation_video_cond")
    {
        var fileInput = document.getElementById("animation_video_cond").files[0];
        var allowed = ["mp4"];
        var found = false;

        allowed.forEach(function(extension) {
        if (fileInput.type.match('.'+extension)) {
            found = true;
        }
        })

        if(found){
        }
        else{
        alert("Allowed file type is MP4");
        document.getElementById("animation_video_cond").value='';
        }
    }

}
