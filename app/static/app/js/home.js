// app/static/app/js/home.js

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Find the new elements
    const fixedNavbar = document.querySelector('.fixed-navbar-container');
    const sidebarLeft = document.querySelector('.sidebar-left');
    const scrollingContent = document.querySelector('.scrolling-content');
    
    if (fixedNavbar && sidebarLeft && scrollingContent) {
        
        // 2. Get the total height of the top bar (height + 10px offset)
        const navbarTotalOffset = fixedNavbar.offsetHeight + fixedNavbar.offsetTop;
        
        console.log('Total navbar offset:', navbarTotalOffset, 'px');

        // 3. Set the sidebar to start *under* the navbar
        sidebarLeft.style.top = navbarTotalOffset + 'px';
        
        // 4. Set the main scrolling content to start *under* the navbar
        scrollingContent.style.marginTop = navbarTotalOffset + 'px';
    }
});