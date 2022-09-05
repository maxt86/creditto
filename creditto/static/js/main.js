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
