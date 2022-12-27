$(document).ready(function() {
    $(document).scroll(function () {
        var $nav = $("#header");
        if ($(this).scrollTop() > 70) {
            $('#header').css({"backdrop-filter":"blur(50px)","top":"0px","padding-bottom":"10px","padding-top":"10px"});
            $('#left-logo').css({"display":"block"})
            $('#center-logo').css({"display":"none"})
            $('#page_title_body').css({"font-size":"1.25rem"})
            $('#page_title_body_sub').css({"display":"none"})
        } else {
            $('#header').css({"backdrop-filter":"blur(0px)","top":"25px"});
            $('#left-logo').css({"display":"none"})
            $('#page_title_body').css({"font-size":"1.75rem"})
            $('#page_title_body_sub').css({"display":"block"})
            $('#center-logo').css({"display":"block"})
        }
    });
});
document.addEventListener("DOMContentLoaded", function(event) {
   
    $(".sidebarItem").hover(function() {
        var root = this;
        $('#page_title_body').animate({
            'opacity' : 0
        }, 200, function(){
            if($(root).attr('value') == 'Toggle Dark/Light Mode')
                $(this).html($(root).attr('value')).animate({'opacity': 1}, 200)
            else $(this).html('Go to ' + $(root).attr('value')).animate({'opacity': 1}, 200);});
    }, function() {
        $('#page_title_body').animate({
            'opacity' : 0
        }, 200, function(){
            $(this).html('BulSU CICT Faculty').animate({'opacity': 1}, 200);});
    })
    var value = localStorage.theme;
    if(value == 'dark') {
        document.documentElement.classList.add('dark');
    }   else {
        document.documentElement.classList.remove('dark');
    }
    
    $('.themeToggler').click(function() {
        var value = localStorage.theme;
        if(value == 'dark') {
            localStorage.theme = 'light'
            document.documentElement.classList.remove('dark');
        }   else {
            localStorage.theme = 'dark'
            document.documentElement.classList.add('dark');
        }
    })
    const showNavbar = (toggleId, navId, bodyId, headerId) =>{
    const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId),
    bodypd = document.getElementById(bodyId),
    headerpd = document.getElementById(headerId)
   
    // Validate that all variables exist
    if(toggle && nav && bodypd && headerpd){
    toggle.addEventListener('click', ()=>{
    // show navbar
    nav.classList.toggle('show_sidebar')
    // change icon
    toggle.classList.toggle('bx-x')
    // add padding to body
    bodypd.classList.toggle('body-pd')
    // add padding to header
    headerpd.classList.toggle('header_pd')
    })
    }
    }
    
    showNavbar('header-toggle','nav-bar','body-pd','header')
    
    /*===== LINK ACTIVE ===== */
  
    const linkColor = document.querySelectorAll('.nav_link')
    
    function colorLink(){
    if(linkColor){
    linkColor.forEach(l=> l.classList.remove('active'))
    this.classList.add('active')
    }
    }
    linkColor.forEach(l=> l.addEventListener('click', colorLink)) 


    /*===== TRANSACTION ACTIVE ===== */

    const trsactLinkColor = document.querySelectorAll('.trsact-link')

    function trsactcolorLink(){
        if(trsactLinkColor){
            trsactLinkColor.forEach(l=> l.classList.remove('navtab-status-active'))
            this.classList.add('navtab-status-active')
    
        }
        }
        trsactLinkColor.forEach(l=> l.addEventListener('click', trsactcolorLink)) 
    
    }); 
