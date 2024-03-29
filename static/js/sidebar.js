$(document).ready(function() {
    var $search = $('#top-search-button, #top-search-input');
    $(document).on('click', function (e) {
        // If element is opened and click target is outside it, hide it
        if ($search.is(':visible') && !$search.is(e.target) && !$search.has(e.target).length) {
            $('#top-search-input').removeClass('toggled');
            $('#top-search-button').removeClass('toggled');
            $('#center-logo').show();
        }
    });
    $('#top-search-button').click(function() {
        $('#top-search-input').addClass('toggled');
        $('#top-search-button').addClass('toggled');
        $('#center-logo').hide();
        $('#top-search-input > input').focus();
    })
     // Add slideup & fadein animation to dropdown
   $('.dropdown').on('show.bs.dropdown', function(e){
    var $dropdown = $(this).find('.dropdown-menu');
    var orig_margin_top = parseInt($dropdown.css('margin-top'));
    $dropdown.css({'margin-top': (orig_margin_top + 10) + 'px', opacity: 0}).animate({'margin-top': orig_margin_top + 'px', opacity: 1}, 300, function(){
       $(this).css({'margin-top':''});
    });
 });
 // Add slidedown & fadeout animation to dropdown
 $('.dropdown').on('hide.bs.dropdown', function(e){
    var $dropdown = $(this).find('.dropdown-menu');
    var orig_margin_top = parseInt($dropdown.css('margin-top'));
    $dropdown.css({'margin-top': orig_margin_top + 'px', opacity: 1, display: 'block'}).animate({'margin-top': (orig_margin_top + 10) + 'px', opacity: 0}, 300, function(){
       $(this).css({'margin-top':'', display:''});
    });
 });
    $(document).scroll(function () {
        var $nav = $("#header");
        if ($(this).scrollTop() > 70) {
            $('#header').css({"backdrop-filter":"blur(50px)","top":"0px","padding-bottom":"20px","padding-top":"20px"});
            $('#header').addClass('scrolled');
            $('#header').css({"position":"fixed !important"});
            $('#left-logo').css({"display":"block"})
            $('#center-logo').css({"display":"none"})
            $('#page_title_body').css({"font-size":"1.25rem"})
            $('#page_title_body_sub').css({"display":"none"})
        } else {
            $('#header').css({"backdrop-filter":"blur(0px)","top":"5px", "position":"relative !important"});
            $('#header').removeClass('scrolled');
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
        $('#page_title_body').stop().animate({
            'opacity' : 0
        }, 200, function(){
            if($(root).attr('value') == 'Toggle Dark/Light Mode')
                $(this).html($(root).attr('value')).stop().animate({'opacity': 1}, 200)
            else $(this).html('Go to ' + $(root).attr('value')).stop().animate({'opacity': 1}, 200);});
    }, function() {
        $('#page_title_body').stop().animate({
            'opacity' : 0
        }, 200, function(){
            $(this).html('Faculty Management System').stop().animate({'opacity': 1}, 200);});
    })
    $('.selected-from-url').length==0 && $("#nav-highlighter").hide()
    var pos = $('.selected-from-url').position()
    $('.selected-from-url').length > 0 && $("#nav-highlighter").css('top', pos.top-10);
    
    /* 
    OWN IMPLEMENTATION OF NO-RELOAD NAVIGATION BY JERSON REYES 
    INSPIRED BY REACTJS (WITH MATCHING TRANSITION ANIMATIONS PLUS ELEMENT DELAYS)
    */
    $("a").click(function(e) {
        e.preventDefault();
        if(e.currentTarget.getAttribute('value') != "Toggle Dark/Light Mode") {
            e.preventDefault();
            var root = this;
            var pos;
            if(e.currentTarget.getAttribute('sidebarItem') || e.currentTarget.href == '/') {
                pos = $('#home-nav-item').position()
            } else {
                pos = $(root).position()
            }
            $("#nav-highlighter").css('top', pos.top);
                $("#nav-highlighter").css('left', pos.left);

            e.currentTarget.getAttribute('value') ? $("#nav-highlighter").fadeIn() : $("#nav-highlighter").fadeOut();
            window.history.pushState('FacMaSys', 'FacMaSys - ' + e.currentTarget.getAttribute('value') ? e.currentTarget.getAttribute('value') : '', e.currentTarget.href);
            $('title').html('FacMaSys - ' + e.currentTarget.getAttribute('value'))
            $("#main-body").animate({opacity: '0'}, 100).load(e.currentTarget.href + "#main-body").animate({opacity: '1'}, 100);      
        } 
    })
    
    $('.themeToggler').click(function() {
        var value = $.cookie("theme");
        if(value == 'dark') {
            $.cookie('theme', 'light', { expires: 9999999, path: '/' });
            document.documentElement.classList.remove('dark');
        }   else {
            $.cookie('theme', 'dark', { expires: 9999999, path: '/' });
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
