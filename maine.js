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
    setupArrows();
}

//function for setting up (procedurally generating) all the arrows
function setupArrows()
{
    var classBoxes = document.getElementsByClassName("classBox");
    var arrow_template = document.getElementById("templates").getElementsByClassName("svg-arrow")[0];
    
    for(var i = 0; i<classBoxes.length; i++){
        var boxx = classBoxes[i];
        var preq = boxx.getAttribute("prereq");
        //if there is prereq attribute
        if (preq){
            var preqs = preq.split(" ");
            //for each prereq
            for (var j = 0; j<preqs.length; j++){
                var prereq_tag = preqs[j];
                //get the connecting element and draw the arrow
                var ancestor = document.getElementById(prereq_tag);
                if(ancestor){//if such ancestor exist
                    //clone arrow node
                    //var clon = arrow_template.cloneNode(true);
                    var clon = document.createElementNS("http://www.w3.org/2000/svg", 'line');
                    clon.setAttribute("style", "stroke:rgb(0,0,0);stroke-width:1");
                    clon.setAttribute("marker-end", "url(#arrow)");
                    //get and set the x y coordinates of starting and ending of line
                    var x1 = parseFloat(ancestor.style.left) + 6;
                    var y1 = parseFloat(ancestor.style.top) + 4.5;
                    var x2 = parseFloat(boxx.style.left) + 6;
                    var y2 = parseFloat(boxx.style.top);
                    clon.setAttribute("x1", x1 + "em");
                    clon.setAttribute("y1", y1 + "em");
                    clon.setAttribute("x2", x2 + "em");
                    clon.setAttribute("y2", y2 + "em");
                    //add class list
                    clon.classList.add(prereq_tag);
                    clon.classList.add(boxx.getAttribute("id"));
                    //put into svg tag
                    document.getElementsByClassName("svgConns")[0].appendChild(clon);
                }
            }
        }
    }
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
            if (document.getElementById(related[ctt])){
                document.getElementById(related[ctt]).style.opacity = "1.0";
            }
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
        allArrows[ct].style.opacity = "0.08";
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