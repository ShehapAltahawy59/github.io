document.getElementById("search-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form submission

    // Get the search query
    var query = document.getElementById("search-input").value.trim();

    // Construct the URL with the search query
    var url = "/search?query=" + encodeURIComponent(query);

    // Redirect the user to the search route
    window.location.href = url;
});


function checkIfSaved(button, url) {
    fetch(`/is_saved?url=${encodeURIComponent(url)}`)
        .then(response => response.json())
        .then(data => {
            if (data.is_saved) {
                button.classList.add('saved');
                button.innerHTML = '❤️'; // Update to display 'Saved'
            } else {
                button.classList.remove('saved');
                button.innerHTML = '&#9825;'; // Update to display heart
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}




function toggleSaveArticle(button) {
    
    var title = button.getAttribute('data-title');
    var description = button.getAttribute('data-description');
    var url = button.getAttribute('data-url');
    var urlToImage = button.getAttribute('data-urlToImage');
    
    const isSaved = button.classList.contains('saved');
    if (isSaved) {
        
        unsaveArticle(button,url);
    } else {
    // Toggle the saved class
            
            saveArticle(button,title, description, url,urlToImage);    
            
            }
}
function saveArticle(button,title, description, url,urlToImage,user_id) {
    fetch('/save_news', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: title, description: description, url: url,urlToImage:urlToImage,user_id:user_id })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            button.classList.add('saved');
            button.innerHTML = '❤️'; // Update to display 'Saved' 
        } 
    })
    .catch(error => {
        alert('There was a problem with your fetch operation: ' + error.message);
    });
    
    
}



function unsaveArticle(button,url) {
    fetch('/del_news', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            button.classList.remove('saved');
            button.innerHTML = '&#9825;'; // Update to display heart
        } 
    })
    .catch(error => {
        alert('There was a problem with your fetch operation: ' + error.message);
    });
}


function toggleremoveArticle(button){
    url = button.getAttribute('data-url');
    fetch('/del_news', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(error => {
        alert('There was a problem with your fetch operation: ' + error.message);
    });

}


function toggleremoveNews(button) {
    var url = button.getAttribute('data-url');

    $.ajax({
        type: 'POST',
        url: '/del_news',
        contentType: 'application/json',
        data: JSON.stringify({ url: url }),
        success: function(data) {
            if (data.success) {
                // Remove the news article from the DOM
                var newsArticle = button.closest('#news-article');
                if (newsArticle) {
                    newsArticle.remove();
                }
            } else {
                alert(data.message);
            }
        },
        error: function(xhr, status, error) {
            alert('There was a problem with your request: ' + error);
        }
    });
}

document.querySelectorAll('.heart-button').forEach(button => {
    const title = button.getAttribute('data-title');
    const description = button.getAttribute('data-description');
    const url = button.getAttribute('data-url');
    const urlToImage = button.getAttribute('data-urlToImage');
    checkIfSaved(button, url);

    button.addEventListener('click', () => {
        toggleSaveArticle(button, title, description, url,urlToImage);
    });
});
