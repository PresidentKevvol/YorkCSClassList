//the root div element of the graph
var rootDiv;

function setup()
{
    //all the class boxes
    var allBoxes = document.getElementsByClassName("classBox");
    for(var ct=0; ct<allBoxes.length; ct++)
    {
        allBoxes[ct].addEventListener("mouseover", boxOnHover);
        allBoxes[ct].addEventListener("mouseout", boxOnLeave);
    }
    
    rootDiv = document.getElementById("root");
}

//called when a box have the cursor hovered on
function boxOnHover(event)
{
    //the element that fired the event
    var source = event.target || event.srcElement;
    //the id of element
    var sourceId = source.id;
    
    //hide all elements first
    var allElements = rootDiv.getElementsByTagName("div");
    for(var ct=0; ct<allElements.length; ct++)
    {
        allElements[ct].style.opacity = "0.3";
    }
    
    source.style.opacity = "1.0";
    
    //these are the arrows need to appear
    var arrows = document.getElementsByClassName(sourceId);
    console.log(arrows.length);
    for(var ct=0; ct<arrows.length; ct++)
    {
        //arrows[ct].style.opacity = "1.0";
        //all the classes of the arrows are related boxes
        var related = arrows[ct].classList;
        for(var ctt=0; ctt<related.length; ctt++)
        {
            document.getElementById(related[ctt]).style.opacity = "1.0";
        }
    }
    
    //these are all the arrows
    var allArrows = rootDiv.getElementsByTagName("line");
    for(var ct=0; ct<allArrows.length; ct++)
    {
        /*
        //if this arrow is a related arrow
        if(arrows.includes(allArrows[ct]))
        {
            allArrows[ct].style.opacity = "1.0";
        }
        else
        {
            allArrows[ct].style.opacity = "0.4";
        }
        */
        //hide all arrows first
        allArrows[ct].style.opacity = "0.2";
    }
    
    for(var ct=0; ct<arrows.length; ct++)
    {
        console.log("one arrow");
        arrows[ct].style.opacity = "1.0";
    }
}

function boxOnLeave()
{
    //show all elements again
    var allElements = rootDiv.getElementsByTagName("*");
    for(var ct=0; ct<allElements.length; ct++)
    {
        allElements[ct].style.opacity = "1.0";
    }
}

document.addEventListener("DOMContentLoaded", setup);