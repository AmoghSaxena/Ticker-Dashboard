function schedulebuttonenabler(id)
{
    if(id == "scheduleenabler")
    {
        var b = document.getElementById("scheduleenabler");
        if (b.checked)
        {
            document.getElementById("occurancysection").hidden = true;
            document.getElementById("datatimesection").hidden = true;
        }
        else
        {
            document.getElementById("occurancysection").hidden = false;
            document.getElementById("datatimesection").hidden = false;
        }
    }
}