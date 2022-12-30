
$(document).ready(function() {

  new ClipboardJS('.copy');
  $(document).on("click", ".form-modal-toggler", function(e){
    fetch(e.currentTarget.getAttribute('href'), {
        dataType: "html",
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => {
        return response.text();
    })
    .then(data => {
      $("#form-modal").toggle();
        $("#form-modal-body").html(data).animate({opacity: '1'}, 100);      
        $('#form-modal').addClass('active')
        $('#form-modal form').attr("action", e.currentTarget.getAttribute('value') );
        $('#form-modal-title').html(e.currentTarget.title)
        $('#form-modal-extra').html(e.currentTarget.getAttribute('value').split('/')[1] ? e.currentTarget.getAttribute('value').split('/')[1] : e.currentTarget.getAttribute('value'))
    })
    return false;
})
$("#form-modal-child").on("click", function(e){
  if(e.target !== e.currentTarget) return;

  $("#form-modal").hide();
  $('#form-modal').removeClass('active')
});

  var drawer = function () {
    /**
    * Element.closest() polyfill
    * https://developer.mozilla.org/en-US/docs/Web/API/Element/closest#Polyfill
    */
    if (!Element.prototype.closest) {
      if (!Element.prototype.matches) {
        Element.prototype.matches = Element.prototype.msMatchesSelector || Element.prototype.webkitMatchesSelector;
      }
      Element.prototype.closest = function (s) {
        var el = this;
        var ancestor = this;
        if (!document.documentElement.contains(el)) return null;
        do {
          if (ancestor.matches(s)) return ancestor;
          ancestor = ancestor.parentElement;
        } while (ancestor !== null);
        return null;
      };
    }

    //
    // Settings
    //
    var settings = {
      speedOpen: 50,
      speedClose: 350,
      activeClass: 'is-active',
      visibleClass: 'is-visible',
      selectorTarget: '[data-drawer-target]',
      selectorTrigger: '[data-drawer-trigger]',
      selectorClose: '[data-drawer-close]',
    };

    //
    // Methods
    //
    // Toggle accessibility
    var toggleccessibility = function (event) {
      if (event.getAttribute('aria-expanded') === 'true') {
        event.setAttribute('aria-expanded', false);
      } else {
        event.setAttribute('aria-expanded', true);
      }
    };
    // Open Drawer
    var openDrawer = function (trigger) {
      // Find target
      var target = document.getElementById(trigger.getAttribute('aria-controls'));
      

      // Make it active
      target.classList.add(settings.activeClass);
      // Make body overflow hidden so it's not scrollable
      document.documentElement.style.overflow = 'hidden';
      // Toggle accessibility
      toggleccessibility(trigger);
      // Make it visible
      setTimeout(function () {
        target.classList.add(settings.visibleClass);
      }, settings.speedOpen);
    };
    // Close Drawer
    var closeDrawer = function (event) {
      // Find target
      var closestParent = event.closest(settings.selectorTarget),
        childrenTrigger = document.querySelector('[aria-controls="' + closestParent.id + '"');
      // Make it not visible
      closestParent.classList.remove(settings.visibleClass);
      // Remove body overflow hidden
      document.documentElement.style.overflow = '';
      // Toggle accessibility
      toggleccessibility(childrenTrigger);
      // Make it not active
      setTimeout(function () {
        closestParent.classList.remove(settings.activeClass);
      }, settings.speedClose);
    };
    // Click Handler
    var clickHandler = function (event) {
      // Find elements
      var toggle = event.target,
        open = toggle.closest(settings.selectorTrigger),
        close = toggle.closest(settings.selectorClose);
      // Open drawer when the open button is clicked
      if (open) {
        openDrawer(open);
      }
      // Close drawer when the close button (or overlay area) is clicked
      if (close) {
        closeDrawer(close);
      }
      // Prevent default link behavior
      if (open || close) {
        event.preventDefault();
      }
    };
    // Keydown Handler, handle Escape button
    var keydownHandler = function (event) {
      if (event.key === 'Escape' || event.keyCode === 27) {
        // Find all possible drawers
        var drawers = document.querySelectorAll(settings.selectorTarget),
          i;
        // Find active drawers and close them when escape is clicked
        for (i = 0; i < drawers.length; ++i) {
          if (drawers[i].classList.contains(settings.activeClass)) {
            closeDrawer(drawers[i]);
          }
        }
      }
    };

    //
    // Inits & Event Listeners
    //
    document.addEventListener('click', clickHandler, false);
    document.addEventListener('keydown', keydownHandler, false);

  };
  drawer();
    var $search = $('#top-search-button, #top-search-input');
    $(document).on('click', function (e) {
        // If element is opened and click target is outside it, hide it
        if ($search.is(':visible') && !$search.is(e.target) && !$search.has(e.target).length) {
            $('#top-search-input').removeClass('toggled');
            $('#top-search-button').removeClass('toggled');
            $('#center-logo').show();
        }
    });
    $(document).on("click", "#top-search-button", function(e){
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
    $(document).on("click", ".research-item", function(e){
        fetch("http://127.0.0.1:8000/researches/get/"+e.currentTarget.id.split('-')[1], {
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => {
            return response.json() //Convert response to JSON
        })
        .then(data => {
            $('#drawer-title').html(data.research.research_title);
            $('#drawer-category').html(data.research.content_type);
            $('#drawer-available').html(data.research.research_progress);
            $('#drawer-download').html(data.research.document != '' ? 'File Available' : 'File Not Available');
            data.research.document != '' ? $('#drawer-download').addClass('available') : $('#drawer-download').removeClass('available');
            console.log(`/media/`+data.research.document.split('/'))
            $('#drawer-download').attr('onclick',`
            var anchor = document.createElement('a');
            anchor.href = '/media/`+data.research.document+`';
            anchor.target = '_blank';
            anchor.download = '`+data.research.document.split('/')[1]+`';
            $('#drawer-download').hasClass('available') && anchor.click();
            `);
            $('#drawer-abstract').html(data.research.abstract);
            var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            $('#drawer-date').html(new Date(data.research.date_added).toLocaleDateString("en-US", options));
            fetch("http://127.0.0.1:8000/user/get/"+data.user.user_id, {
                headers:{
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => {
                return response.json() //Convert response to JSON
            })
            .then(data => {
              $('#drawer-author').html(data[0].first_name + ' ' + data[0].last_name );
            })
            
        })

    })
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
    $(document).on("click", "a", function(e){
        e.preventDefault();
        if(e.currentTarget.getAttribute('value') != "Toggle Dark/Light Mode" && !e.currentTarget.classList.contains("paginate_button")) {
            e.preventDefault();
            if(e.currentTarget.getAttribute('sidebarItem')) {
              var root = this;
              var pos;
              if(e.currentTarget.getAttribute('sidebarItem') || e.currentTarget.href == '/') {
                  pos = $('#home-nav-item').position()
              } else {
                  pos = $(root).position()
              }
              $("#nav-highlighter").css('top', pos.top);
                  $("#nav-highlighter").css('left', pos.left);
            }
            e.currentTarget.getAttribute('value') ? $("#nav-highlighter").fadeIn() : $("#nav-highlighter").fadeOut();
              (!e.currentTarget.classList.contains('ignore-url')) && window.history.pushState('FacMaSys', 'FacMaSys - ' + e.currentTarget.getAttribute('value') ? e.currentTarget.getAttribute('value') : '', e.currentTarget.href);
            $('title').html('FacMaSys - ' + e.currentTarget.getAttribute('value'))
            if(e.currentTarget.classList.contains('form-modal-toggler'))
              $("#form-modal-body").animate({opacity: '0'}, 100).load(e.currentTarget.href + "#form-modal-body").animate({opacity: '1'}, 100);      
            else $("#main-body").animate({opacity: '0'}, 100).load(e.currentTarget.href + "#main-body").animate({opacity: '1'}, 100);      
        } 
    })
    $('.themeToggler').click(function(e){
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