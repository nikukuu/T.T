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

document.querySelectorAll('.menu-links').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();
        
        
        document.querySelectorAll('.menu-links').forEach(link => {
            link.classList.remove('active');
        });

        
        this.classList.add('active');

        
        document.querySelectorAll('.section').forEach(sec => {
            sec.style.display = 'none';
        });

        
        const section = this.getAttribute('data-section');
        document.getElementById(section).style.display = 'block';
    });
});

document.getElementById('saveLinks').addEventListener('click', function() {
    const instagram = document.getElementById('instagram').value;
    const facebook = document.getElementById('facebook').value;
    const twitter = document.getElementById('twitter').value;
    const github = document.getElementById('github').value;

    if (instagram) {
        document.getElementById('instaLink').href = instagram;
        document.getElementById('instaLink').style.display = 'block';
    }
    if (facebook) {
        document.getElementById('fbLink').href = facebook;
        document.getElementById('fbLink').style.display = 'block';
    }
    if (twitter) {
        document.getElementById('twitterLink').href = twitter;
        document.getElementById('twitterLink').style.display = 'block';
    }
    if (github) {
        document.getElementById('githubLink').href = github;
        document.getElementById('githubLink').style.display = 'block';
    }

    document.getElementById('savedLinks').style.display = 'block';
});

document.getElementById('cancelLinks').addEventListener('click', function() {
    document.getElementById('socialMediaLinks').style.display = 'none';
});