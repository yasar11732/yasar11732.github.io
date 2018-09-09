var scrollPos;
var waiting = false;

document.addEventListener('scroll', function(event){
    scrollPos = window.scrollY;

    if(!waiting && scrollPos < 128)
    {
        window.requestAnimationFrame(function(){
           topbar = document.querySelector(".fixed-top");
           if(topbar)
           {
               topbar.style.opacity = Math.max((80 - scrollPos) / 80, 0);
           }
           waiting = false;
        });

        waiting = true;
    }
})