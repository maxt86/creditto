function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function deleteNotification(url, elemId) {
    const csrftoken = getCookie('csrftoken');
    const config = {
        headers: {
            'X-CSRFToken': csrftoken,
        }
    };
    
    axios.delete(url, config)
        .then((response) => {
            if (response.data != 'success') {
                alert('Notification Not Deleted');
                return;
            }
            
            const numNotifications = document.querySelectorAll('.notification').length;
            
            if (numNotifications <= 1) {
                document.getElementById('notification-container').remove();
                return;
            }
            
            const elem = document.getElementById(elemId);
            const firstElem = document.getElementById('notification-list').firstElementChild;
            if (elem === firstElem) {
                elem.nextElementSibling.remove();
            } else {
                elem.previousElementSibling.remove();
            }
            
            elem.remove();
            document.getElementById('notification-counter').innerText -= 1;
        })
        .catch((error) => {
            alert('Internal Error');
        });
}

function likePost(url, dislikeUrl) {
    let likes = document.querySelector(`form[action="${url}"] .like-count`);
    let dislikes = document.querySelector(`form[action="${dislikeUrl}"] .dislike-count`);
    
    let numLikes = parseInt(likes.innerText);
    let numDislikes = parseInt(dislikes.innerText);
    
    const csrftoken = getCookie('csrftoken');
    const config = {
        headers: {
            'X-CSRFToken': csrftoken,
        }
    };
    
    axios.post(url, {}, config)
        .then((response) => {
            let [status, likeAction, wasDisliked] = response.data.split(' ');
            
            if (status != 'success') {
                alert('Error: Liking Failed');
                return;
            }
            
            likeAction = parseInt(likeAction);
            wasDisliked = parseInt(wasDisliked);
            
            numLikes += likeAction;
            numDislikes -= wasDisliked;
            
            likes.innerText = numLikes;
            dislikes.innerText = numDislikes;
        })
        .catch((error) => {
            alert('Internal Error');
        });
}

function dislikePost(url, likeUrl) {
    let dislikes = document.querySelector(`form[action="${url}"] .dislike-count`);
    let likes = document.querySelector(`form[action="${likeUrl}"] .like-count`);
    
    let numDislikes = parseInt(dislikes.innerText);
    let numLikes = parseInt(likes.innerText);
    
    const csrftoken = getCookie('csrftoken');
    const config = {
        headers: {
            'X-CSRFToken': csrftoken,
        }
    };
    
    axios.post(url, {}, config)
        .then((response) => {
            let [status, dislikeAction, wasLiked] = response.data.split(' ');
            
            if (status != 'success') {
                alert('Error: Disliking Failed');
                return;
            }
            
            dislikeAction = parseInt(dislikeAction);
            wasLiked = parseInt(wasLiked);
            
            numDislikes += dislikeAction;
            numLikes -= wasLiked;
            
            dislikes.innerText = numDislikes;
            likes.innerText = numLikes;
        })
        .catch((error) => {
            alert('Internal Error');
        });
}
