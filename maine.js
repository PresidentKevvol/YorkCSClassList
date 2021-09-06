//the root div element of the graph
var rootDiv;

function setup()
{
    //all the class boxes
    var allBoxes = document.getElementsByClassName("classBox");
    rootDiv = document.getElementById("root");

    for(var ct=0; ct<allBoxes.length; ct++)
    {
        allBoxes[ct].addEventListener("mouseover", boxOnHover);
        allBoxes[ct].addEventListener("mouseout", boxOnLeave);
        allBoxes[ct].addEventListener("click", boxOnClick);
    }
    rootDiv.addEventListener("click", rootDivClicked);

    setupArrows();
    
    //add the toggle color mode button's event listener
    document.getElementById("switch-color-code").addEventListener("click", toggle_color_code_clicked);
    //add the zoom size slider's event listener
    document.getElementById("zoom-range-slider").addEventListener("input", zoom_slider_update);
    document.getElementById("zoom-range-slider").addEventListener("change", zoom_slider_update);
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
    //if a specific box is under focus, then don't change anything
    if (box_focused != false) {
       return;
    }
    //the element that fired the event
    var source = event.target || event.srcElement;
    highlightCourse(source);
}

//function for highlighting a course and it's immediate dependencies and dependents
function highlightCourse(source) {
    //loop selecting a box's parent until reaching the box itself
    //(instead of the divs inside it)
    while (!source.classList.contains("classBox")) {
        source = source.parentElement;
    }
    
    //the id of element
    var sourceId = source.id;

    //hide all elements first
    var allElements = rootDiv.getElementsByClassName("classBox");
    for(var ct=0; ct<allElements.length; ct++)
    {
        allElements[ct].style.opacity = "0.3";
    }

    source.style.opacity = "1.0";

    //these are the arrows need to appear
    var arrows = document.getElementsByClassName(sourceId);
    //console.log(arrows.length);
    for(var ct=0; ct<arrows.length; ct++) {
        //arrows[ct].style.opacity = "1.0";
        //all the classes of the arrows are related boxes
        var related = arrows[ct].classList;
        for(var ctt=0; ctt<related.length; ctt++) {
            if (document.getElementById(related[ctt])) {
                document.getElementById(related[ctt]).style.opacity = "1.0";
            }
        }
    }
    //these are all the arrows
    var allArrows = rootDiv.getElementsByTagName("line");
    for(var ct=0; ct<allArrows.length; ct++) {
        //hide all arrows first
        allArrows[ct].style.opacity = "0.08";
    }
    //show all arrows that needed to be shown
    for(var ct=0; ct<arrows.length; ct++) {
        //console.log("one arrow");
        arrows[ct].style.opacity = "1.0";
    }
}

function boxOnLeave()
{
    //if a specific box is under focus, then don't change anything
    if (box_focused != false) {
       return;
    }
    //otherwise show all elements again
    showAllElements();
}

function showAllElements() {
    //show all elements again
    var allElements = rootDiv.getElementsByTagName("*");
    for(var ct=0; ct<allElements.length; ct++)
    {
        allElements[ct].style.opacity = "1.0";
    }
}

//record the box currently focused
var box_focused = false;

//when a box is clicked, highlight it and disable hover highlight
function boxOnClick(event) {
    //get the element that fired the event
    var source = event.target || event.srcElement;
    focusBox(source);
}

//focus a box when it is clicked, disabling hovering and showing description
function focusBox(source) {
    //loop selecting a box's parent until reaching the box itself
    //(instead of the divs inside it)
    while (!source.classList.contains("classBox")) {
        source = source.parentElement;
    }
    
    //record the highlighted box
    box_focused = source.id;
    //highlight the course
    highlightCourse(source);

    //show the description div
    document.getElementById("explain-main").style.display = "block";
    document.getElementById("explain-hint").style.display = "none";

    //the title (full code and name)
    var course_code_full = source.getElementsByClassName("course-code-full")[0].innerHTML; 
    var course_name = source.getElementsByClassName("course-name")[0].innerHTML;
    var course_title = course_code_full + "<br>" + course_name;
    document.getElementById("explain-topp").innerHTML = course_title;
    //the description
    var description_hidden = source.getElementsByClassName("course-description")[0].innerHTML;
    document.getElementById("explain-desc").innerHTML = description_hidden;
    //and the prerequsite list
    var prereq_div = document.getElementById("explain-prereq-list-div");
    var prereq_ul = document.getElementById("explain-prereq-list");
    var prereqs = source.getAttribute("prereq");
    if (prereqs === "") {
        prereq_div.style.display = "none"; //hide it if there is no prerequsite
    } else {
        prereq_div.style.display = "block";
        prereq_ul.innerHTML = "";
        var prereqs_split = prereqs.split(" ");
        for (var i=0; i<prereqs_split.length; i++) {
            prereq_ul.innerHTML += "<li>" + prereqs_split[i] + "</li>";
        }
    }
}

//unfocus any box when the background is clicked
function unfocusBox() {
    box_focused = false;
    showAllElements();

    //hide the description div
    document.getElementById("explain-main").style.display = "none";
    document.getElementById("explain-hint").style.display = "block";
}

//whenever root div is clicked (so includes when boxes are clicked)
function rootDivClicked(event) {
    //we just make sure it's only the background and not the boxes
    var source = event.target || event.srcElement;
    if (!source.classList.contains("classBox") && !source.classList.contains("course-code-full") && !source.classList.contains("course-name")) {
        unfocusBox();
    }
}

//when the button for toggling color code format for the boxes
function toggle_color_code_clicked(event) {
    var targ = event.target;
    if (targ.innerHTML === "Color code by year") {
        rootDiv.setAttribute("colorcode", "level");
        targ.innerHTML = "Color code by dept";
    } else if (targ.innerHTML === "Color code by dept") {
        rootDiv.setAttribute("colorcode", "dept");
        targ.innerHTML = "Color code by year";
    }
}

//when the slider for zooming is changed
function zoom_slider_update(event) {
    //get the value of the slider bar
    var zoom_value = event.target.value;
    //update the text
    document.getElementById("zoom-value").innerHTML = zoom_value;
    //and update the inline css of the root div
    rootDiv.style.fontSize = (zoom_value + "em");
}

document.addEventListener("DOMContentLoaded", setup);

