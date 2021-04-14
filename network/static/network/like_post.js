document.addEventListener('DOMContentLoaded', function() {
    const like_link = document.querySelector('#like-post-link');
    document.querySelectorAll('#like-post-link').forEach(like_link =>{
        like_link.onclick = function(){
            like_post(this.dataset.postid);
        }
    })
});

function like_post(post_id){
    var is_liking_by_user = false;
    const current_user = document.querySelector('#username_for_like').innerHTML;
    fetch(`/loadLikes/${post_id}`)
        .then(response => response.json())
        .then(post =>{
            let post_likes = post['likes']
            if (post_likes.includes(current_user) === false){
                is_liking_by_user = true;
                fetch(`/likePost/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({likes:true})
                })

                if (is_liking_by_user === true){
                    let change_class = document.querySelector(`.id_color_like${post_id}`);
                    change_class.classList.replace("like-post", "in-like-post");
                    let current_num_likes = document.querySelector(`.id_num_likes${post_id}`).innerHTML;
                    let new_current_num_likes = parseInt(current_num_likes, 10) + 1;
                    document.querySelector(`.id_num_likes${post_id}`).innerHTML = `${new_current_num_likes} Likes`;
                }

            } else if (post_likes.includes(current_user) === true){
                is_liking_by_user = false;
                fetch(`/likePost/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({likes:true})
                })
                if (is_liking_by_user === false){
                    let change_class = document.querySelector(`.id_color_like${post_id}`);
                    change_class.classList.replace("in-like-post", "like-post");
                    let current_num_likes = document.querySelector(`.id_num_likes${post_id}`).innerHTML;
                    let new_current_num_likes = parseInt(current_num_likes, 10) - 1;
                    document.querySelector(`.id_num_likes${post_id}`).innerHTML = `${new_current_num_likes} Likes`;
                }
            }
        })
}
    

   