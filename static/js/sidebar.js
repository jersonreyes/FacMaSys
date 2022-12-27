document.addEventListener("DOMContentLoaded", function(event) {
   
    $(".sidebarItem").hover(function() {
        var root = this;
        $('#page_title_body').animate({
            'opacity' : 0
        }, 400, function(){
            $(this).html('Go to ' + $(root).attr('value')).animate({'opacity': 1}, 400);});
    }, function() {
        $('#page_title_body').animate({
            'opacity' : 0
        }, 400, function(){
            $(this).html('BulSU CICT Faculty').animate({'opacity': 1}, 400);});
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
