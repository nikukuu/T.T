function showSidebar(){
    const sidebar = document.querySelector('.sidebar')
    sidebar.style.display = 'flex'
}
function hideSidebar(){

const sidebar = document.querySelector('.sidebar')
    sidebar.style.display = 'none'
}

let subMenu = document.getElementById('subMenu');

function toggleMenu() {
    subMenu.classList.toggle("open-menu");
    
}

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}

document.getElementById('scan-btn').addEventListener('click', function() {
    fetch('/scan_qr').then(response => {
        if (!response.ok) {
            alert('Failed to start QR scanner.');
        }
    });
});